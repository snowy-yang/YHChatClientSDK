"""Satori 服务端的协议契约测试：HTTP RPC + WebSocket 事件通道。"""

from collections.abc import AsyncIterator
from typing import Any

import httpx
import pytest
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from yhchat.satori.backend import SatoriNotFoundError, SatoriUnsupportedError
from yhchat.satori.bus import EventBus
from yhchat.satori.models import Channel, Event, Guild, Login, Member, MessageObject, Page, User, now_millis
from yhchat.satori.server import SatoriChatServer

TOKEN = "tk"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


class FakeBackend:
    """只实现聊天子集中已支撑的动作，用于验证协议层。"""

    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[object, ...]]] = []

    async def login(self) -> Login:
        return Login(platform="yhchat", user=User(id="bot-1"))

    async def message_create(
        self, channel_id: str, content: str, referrer: dict[str, object] | None
    ) -> list[MessageObject]:
        self.calls.append(("message_create", (channel_id, content, referrer)))
        return [MessageObject(id="m1", content=content, channel=Channel(id=channel_id), created_at=1700000000000)]

    async def message_get(self, channel_id: str, message_id: str) -> MessageObject:
        if message_id == "missing":
            raise SatoriNotFoundError(f"消息不存在: {message_id}")
        return MessageObject(id=message_id, content="hi", channel=Channel(id=channel_id))

    async def message_list(
        self, channel_id: str, next_token: str | None, direction: str, limit: int, order: str
    ) -> Page[MessageObject]:
        return Page(data=[MessageObject(id="m2", content="a")], next=next_token)

    async def message_update(self, channel_id: str, message_id: str, content: str) -> None:
        self.calls.append(("message_update", (channel_id, message_id, content)))

    async def message_delete(self, channel_id: str, message_id: str) -> None:
        self.calls.append(("message_delete", (channel_id, message_id)))

    async def channel_get(self, channel_id: str) -> Channel:
        return Channel(id=channel_id, type=1)

    async def channel_list(self, guild_id: str | None) -> Page[Channel]:
        raise SatoriUnsupportedError("channel.list 需要 guild_id")

    async def guild_get(self, guild_id: str) -> Guild:
        return Guild(id=guild_id, name=guild_id)

    async def guild_list(self, next_token: str | None) -> Page[Guild]:
        raise SatoriUnsupportedError("guild.list 依赖尚未接入的群列表端点")

    async def guild_member_get(self, guild_id: str, user_id: str) -> Member:
        raise SatoriUnsupportedError("guild.member.get 依赖尚未接入的群成员端点")

    async def guild_member_list(self, guild_id: str, next_token: str | None) -> Page[Any]:
        raise SatoriUnsupportedError("guild.member.list 依赖尚未接入的群成员端点")

    async def user_get(self, user_id: str) -> User:
        return User(id=user_id)

    async def friend_list(self, next_token: str | None) -> Page[Any]:
        raise SatoriUnsupportedError("friend.list 依赖尚未接入的好友端点")


@pytest.fixture
def backend() -> FakeBackend:
    return FakeBackend()


@pytest.fixture
def server(backend: FakeBackend) -> SatoriChatServer:
    return SatoriChatServer(backend, token=TOKEN)


@pytest.fixture
async def client(server: SatoriChatServer) -> AsyncIterator[httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=server.build_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http:
        yield http


async def test_rpc_requires_token(client: httpx.AsyncClient) -> None:
    response = await client.post("/v1/message.create", json={"channel_id": "c1", "content": "x"})

    assert response.status_code == 401
    assert response.json()["message"] == "invalid token"


async def test_message_create_returns_list(client: httpx.AsyncClient, backend: FakeBackend) -> None:
    response = await client.post(
        "/v1/message.create",
        headers=HEADERS,
        json={"channel_id": "c1", "content": 'hi <at id="u1"/>', "referrer": {"message_id": "m0"}},
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["id"] == "m1"
    assert payload[0]["channel"] == {"id": "c1", "type": 0}
    assert payload[0]["created_at"] == 1700000000000
    assert backend.calls[0] == ("message_create", ("c1", 'hi <at id="u1"/>', {"message_id": "m0"}))


async def test_message_get_and_not_found(client: httpx.AsyncClient) -> None:
    found = await client.post("/v1/message.get", headers=HEADERS, json={"channel_id": "c1", "message_id": "m9"})
    missing = await client.post("/v1/message.get", headers=HEADERS, json={"channel_id": "c1", "message_id": "missing"})

    assert found.json()["id"] == "m9"
    assert missing.status_code == 404
    assert "missing" in missing.json()["message"]


async def test_message_list_returns_page(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/v1/message.list", headers=HEADERS, json={"channel_id": "c1", "next_token": None, "limit": 10}
    )

    assert response.status_code == 200
    assert response.json() == {"data": [{"id": "m2", "content": "a"}]}


async def test_message_delete_returns_empty_object(client: httpx.AsyncClient, backend: FakeBackend) -> None:
    response = await client.post("/v1/message.delete", headers=HEADERS, json={"channel_id": "c1", "message_id": "m1"})

    assert response.status_code == 200
    assert response.json() == {}
    assert backend.calls[-1] == ("message_delete", ("c1", "m1"))


async def test_unknown_action_is_404(client: httpx.AsyncClient) -> None:
    response = await client.post("/v1/reaction.create", headers=HEADERS, json={"channel_id": "c1"})

    assert response.status_code == 404
    assert "reaction.create" in response.json()["message"]


async def test_unsupported_backend_action_is_404(client: httpx.AsyncClient) -> None:
    response = await client.post("/v1/guild.list", headers=HEADERS, json={})

    assert response.status_code == 404


async def test_bad_params_is_400(client: httpx.AsyncClient) -> None:
    response = await client.post("/v1/message.create", headers=HEADERS, json={"content": "x"})

    assert response.status_code == 400
    assert "channel_id" in response.json()["message"]


async def test_broken_json_is_400(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/v1/message.create", headers={**HEADERS, "Content-Type": "application/json"}, content=b"{not json"
    )

    assert response.status_code == 400


def test_websocket_identify_ready_and_ping(server: SatoriChatServer) -> None:
    with TestClient(server.build_app()) as test_client, test_client.websocket_connect("/v1/events") as websocket:
        websocket.send_json({"op": 3, "body": {"token": TOKEN}})
        ready = websocket.receive_json()

        assert ready["op"] == 4
        assert ready["body"]["proxy_urls"] == []
        assert ready["body"]["logins"][0]["platform"] == "yhchat"
        assert ready["body"]["logins"][0]["user"] == {"id": "bot-1"}

        websocket.send_json({"op": 1})
        assert websocket.receive_json() == {"op": 2}


def test_websocket_bad_token_closes_3000(server: SatoriChatServer) -> None:
    with (
        TestClient(server.build_app()) as test_client,
        pytest.raises(WebSocketDisconnect) as excinfo,
        test_client.websocket_connect("/v1/events") as websocket,
    ):
        websocket.send_json({"op": 3, "body": {"token": "bad"}})
        websocket.receive_json()

    assert excinfo.value.code == 3000


def test_websocket_pushes_events_with_sn(server: SatoriChatServer) -> None:
    app = server.build_app()
    with TestClient(app) as test_client, test_client.websocket_connect("/v1/events") as websocket:
        websocket.send_json({"op": 3, "body": {"token": TOKEN}})
        assert websocket.receive_json()["op"] == 4

        event = Event(
            type="message-created",
            timestamp=now_millis(),
            login=Login(platform="yhchat", user=User(id="bot-1")),
            message=MessageObject(id="m1", content="hi"),
        )
        assert test_client.portal is not None
        test_client.portal.call(server.bus.publish, event)

        pushed = websocket.receive_json()
        assert pushed["op"] == 0
        assert pushed["body"]["sn"] == 1
        assert pushed["body"]["type"] == "message-created"
        assert pushed["body"]["message"]["id"] == "m1"


def test_bus_drops_oldest_when_full() -> None:
    import asyncio

    async def scenario() -> None:
        bus = EventBus(queue_size=1)
        login = Login(platform="yhchat", user=User(id="bot-1"))
        async with bus.subscribe() as queue:
            await bus.publish(Event(type="a", timestamp=1, login=login))
            await bus.publish(Event(type="b", timestamp=2, login=login))
            assert queue.qsize() == 1
            assert (await queue.get()).type == "b"

    asyncio.run(scenario())
