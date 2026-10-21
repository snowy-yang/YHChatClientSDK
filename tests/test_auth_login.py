"""用户账号登录：免鉴权登录端点、deviceId/platform、退出登录、登录后切换 token。"""

import json
from collections.abc import AsyncIterator
from typing import Any, cast

import httpx
import pytest
import respx

from yhchat import YHChatClient
from yhchat.errors import YHChatError

BASE_URL = "https://chat-go.jwzhd.com"


def body_of(request: httpx.Request) -> dict[str, Any]:
    return cast("dict[str, Any]", json.loads(request.content))


def ok_token(token: str) -> httpx.Response:
    return httpx.Response(200, json={"code": 1, "msg": "success", "data": {"token": token}})


@pytest.fixture
async def client() -> AsyncIterator[YHChatClient]:
    # 故意不传 user_token：登录端点不需要 token
    async with YHChatClient("bot-token", http2=False, trust_env=False) as sdk:
        yield sdk


async def test_auth_is_available_without_user_token(client: YHChatClient) -> None:
    assert client.auth is not None


async def test_email_login_sends_docs_fields_without_token(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/v1/user/email-login").mock(return_value=ok_token("user-token-1"))

        session = await client.auth.login_with_email("me@example.com", "pw", device_id="my-device", platform="android")

        request = route.calls.last.request
        assert "token" not in request.headers
        assert "token" not in request.url.params
        assert body_of(request) == {
            "email": "me@example.com",
            "password": "pw",
            "deviceId": "my-device",
            "platform": "android",
        }
        assert session.token == "user-token-1"
        assert session.device_id == "my-device"
        assert session.platform == "android"


async def test_verification_login_generates_random_device_id(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/v1/user/verification-login").mock(return_value=ok_token("user-token-2"))

        session = await client.auth.login_with_verification("13800000000", "123456")

        sent = body_of(route.calls.last.request)
        assert sent["mobile"] == "13800000000"
        assert sent["captcha"] == "123456"
        assert sent["platform"] == "windows"  # 默认平台：WS 登录也认
        assert len(cast("str", sent["deviceId"])) == 16
        assert session.device_id == sent["deviceId"]


async def test_logout_uses_device_id_body_key_and_token_header(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        login = mock.post("/v1/user/email-login").mock(return_value=ok_token("user-token-3"))
        logout = mock.post("/v1/user/logout").mock(return_value=httpx.Response(200, json={"code": 1, "msg": "success"}))

        session = await client.auth.login_with_email("a@b.c", "pw")
        await client.auth.logout(session)

        assert login.called
        request = logout.calls.last.request
        assert request.headers["token"] == "user-token-3"
        assert body_of(request) == {"device-id": session.device_id}


async def test_login_without_token_in_response_raises(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/user/email-login").mock(
            return_value=httpx.Response(200, json={"code": 1, "msg": "success", "data": {}})
        )

        with pytest.raises(YHChatError, match="没有 token"):
            await client.auth.login_with_email("a@b.c", "pw")


async def test_use_user_token_switches_v1(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/user/email-login").mock(return_value=ok_token("user-token-4"))
        appcast = mock.get("/v1/misc/auto-update").mock(
            return_value=httpx.Response(200, text="<rss/>", headers={"Content-Type": "application/xml"})
        )

        session = await client.auth.login_with_email("a@b.c", "pw")
        await client.use_user_token(session.token)
        await client.v1.extra.auto_update(platform="windows")

        assert appcast.calls.last.request.headers["token"] == "user-token-4"
        assert "token" not in appcast.calls.last.request.url.params
