"""服务端会话保存：文件权限、登录/退出路由、重启恢复、token 不返回给调用方。"""

import json
import stat
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

import httpx
import pytest
import respx

from yhchat import YHChatClient
from yhchat.errors import YHChatError
from yhchat.proto._pb import full_pb2
from yhchat.server.app import YHChatServer
from yhchat.server.sessions import SessionStore, StoredSession

BASE_URL = "https://chat-go.jwzhd.com"


def protobuf(message: Any) -> httpx.Response:
    return httpx.Response(200, content=message.SerializeToString())


def ok_token(token: str) -> httpx.Response:
    return httpx.Response(200, json={"code": 1, "msg": "success", "data": {"token": token}})


def user_info(user_id: str = "u1", name: str = "小明") -> httpx.Response:
    return protobuf(
        full_pb2.UserInfo(
            status=full_pb2.Status(code=1, msg="success"),
            data=full_pb2.UserInfo.Data(id=user_id, name=name),
        )
    )


@pytest.fixture
def store(tmp_path: Path) -> SessionStore:
    return SessionStore(tmp_path / "session.json")


@pytest.fixture
async def sdk_client() -> AsyncIterator[YHChatClient]:
    async with YHChatClient("bot-token", http2=False, trust_env=False) as client:
        yield client


@pytest.fixture
def server(sdk_client: YHChatClient, store: SessionStore) -> YHChatServer:
    return YHChatServer(sdk_client, self_id="bot-1", session_store=store)


@pytest.fixture
async def http(server: YHChatServer) -> AsyncIterator[httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=server.build_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


async def test_store_round_trip_and_permissions(store: SessionStore) -> None:
    session = StoredSession(user_id="u1", token="tk", device_id="dev", platform="windows", created_at=1.0)

    await store.save(session)

    assert await store.load() == session
    assert stat.S_IMODE(store.path.stat().st_mode) == 0o600
    assert stat.S_IMODE(store.path.parent.stat().st_mode) == 0o700

    await store.clear()
    assert await store.load() is None
    assert not store.path.exists()


async def test_store_rejects_corrupt_file(store: SessionStore) -> None:
    store.path.parent.mkdir(parents=True, exist_ok=True)
    store.path.write_text(json.dumps({"user_id": "u1"}), encoding="utf-8")

    with pytest.raises(ValueError, match="缺字段"):
        await store.load()


async def test_login_persists_session_without_leaking_token(store: SessionStore, http: httpx.AsyncClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/user/email-login").mock(return_value=ok_token("user-token"))
        mock.get("/v1/user/info").mock(return_value=user_info())

        response = await http.post("/session/login", json={"email": "a@b.c", "password": "pw"})

    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == "u1"
    assert body["name"] == "小明"
    assert body["device_id"]
    assert "token" not in body
    stored = await store.load()
    assert stored is not None
    assert stored.token == "user-token"
    assert stored.user_id == "u1"


async def test_login_reuses_persisted_token_for_requests(
    store: SessionStore, server: YHChatServer, http: httpx.AsyncClient
) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/user/email-login").mock(return_value=ok_token("user-token"))
        mock.get("/v1/user/info").mock(return_value=user_info())
        request_list = mock.post("/v1/friend/request-list").mock(
            return_value=protobuf(full_pb2.RequestListResponse(status=full_pb2.Status(code=1)))
        )

        await http.post("/session/login", json={"email": "a@b.c", "password": "pw"})
        await server._client.v1.proto.friend.request_list()  # pyright: ignore[reportPrivateUsage]

        assert request_list.calls.last.request.headers["token"] == "user-token"


async def test_login_with_mobile_uses_verification_endpoint(
    http: httpx.AsyncClient,
) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/v1/user/verification-login").mock(return_value=ok_token("tk-2"))
        mock.get("/v1/user/info").mock(return_value=user_info("u2", "小红"))

        response = await http.post("/session/login", json={"mobile": "13800000000", "captcha": "1234"})

    assert response.status_code == 200
    sent = route.calls.last.request
    assert b"13800000000" in sent.content


async def test_login_wrong_password_returns_401_and_keeps_store_empty(
    store: SessionStore, http: httpx.AsyncClient
) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/user/email-login").mock(return_value=httpx.Response(200, json={"code": -1, "msg": "密码错误"}))

        response = await http.post("/session/login", json={"email": "a@b.c", "password": "bad"})

    assert response.status_code == 401
    assert response.json() == {"message": "密码错误", "code": -1}
    assert await store.load() is None


async def test_login_requires_known_fields(http: httpx.AsyncClient) -> None:
    response = await http.post("/session/login", json={"foo": "bar"})

    assert response.status_code == 400
    assert "email+password" in response.json()["message"]


async def test_session_get_and_logout(store: SessionStore, http: httpx.AsyncClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/user/email-login").mock(return_value=ok_token("user-token"))
        mock.get("/v1/user/info").mock(return_value=user_info())
        logout = mock.post("/v1/user/logout").mock(return_value=httpx.Response(200, json={"code": 1, "msg": "success"}))

        assert (await http.get("/session")).status_code == 404
        await http.post("/session/login", json={"email": "a@b.c", "password": "pw"})

        current = await http.get("/session")
        assert current.status_code == 200
        assert current.json()["user_id"] == "u1"
        assert "token" not in current.json()

        out = await http.post("/session/logout")

    assert out.json() == {"logged_out": True}
    assert logout.calls.last.request.headers["token"] == "user-token"
    assert await store.load() is None


async def test_restore_session_injects_token(store: SessionStore, server: YHChatServer) -> None:
    await store.save(
        StoredSession(user_id="u1", token="restored-token", device_id="dev", platform="windows", created_at=1.0)
    )
    with respx.mock(base_url=BASE_URL) as mock:
        request_list = mock.post("/v1/friend/request-list").mock(
            return_value=protobuf(full_pb2.RequestListResponse(status=full_pb2.Status(code=1)))
        )

        restored = await server.restore_session()
        await server._client.v1.proto.friend.request_list()  # pyright: ignore[reportPrivateUsage]

    assert restored is not None
    assert restored.token == "restored-token"
    assert request_list.calls.last.request.headers["token"] == "restored-token"


async def test_logout_without_session_is_noop(http: httpx.AsyncClient) -> None:
    response = await http.post("/session/logout")

    assert response.status_code == 200
    assert response.json() == {"logged_out": False}


async def test_routes_absent_without_store(sdk_client: YHChatClient) -> None:
    server = YHChatServer(sdk_client, self_id="bot-1")
    transport = httpx.ASGITransport(app=server.build_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http:
        assert (await http.get("/session")).status_code == 404


async def test_cleared_token_makes_v1_unavailable(store: SessionStore, sdk_client: YHChatClient) -> None:
    await sdk_client.use_user_token("tk")
    await sdk_client.clear_user_token()

    with pytest.raises(YHChatError, match="user_token"):
        _ = sdk_client.v1


async def test_session_routes_require_token_when_configured(sdk_client: YHChatClient, store: SessionStore) -> None:
    server = YHChatServer(sdk_client, self_id="bot-1", session_store=store, session_token="secret")
    transport = httpx.ASGITransport(app=server.build_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http:
        assert (await http.get("/session")).status_code == 401
        assert (await http.post("/session/login", json={})).status_code == 401
        assert (await http.post("/session/logout")).status_code == 401
        allowed = await http.get("/session", headers={"Authorization": "Bearer secret"})
        assert allowed.status_code == 404  # 已鉴权，只是还没登录
