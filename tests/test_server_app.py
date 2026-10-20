"""HTTP 服务层测试：健康检查、webhook → Satori 事件、Satori 挂载。"""

import asyncio
from collections.abc import AsyncIterator
from typing import Any

import httpx
import pytest

from yhchat import YHChatClient
from yhchat.server.app import YHChatServer

MESSAGE_EVENT: dict[str, Any] = {
    "header": {"eventId": "e1", "eventTime": 1700000000000, "eventType": "message.receive.normal"},
    "event": {
        "sender": {"senderId": "u1", "senderType": "user", "senderNickname": "小明"},
        "chat": {"chatId": "g1", "chatType": "group"},
        "message": {
            "msgId": "m1",
            "parentId": "m0",
            "sendTime": 1700000000001,
            "contentType": "text",
            "content": {"text": "hi", "at": ["u2"]},
        },
    },
}


@pytest.fixture
async def sdk_client() -> AsyncIterator[YHChatClient]:
    async with YHChatClient("test-token", http2=False, trust_env=False) as client:
        yield client


@pytest.fixture
def server(sdk_client: YHChatClient) -> YHChatServer:
    return YHChatServer(sdk_client, self_id="bot-1", satori_token="satori-tk")


@pytest.fixture
async def http(server: YHChatServer) -> AsyncIterator[httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=server.build_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


async def test_health(http: httpx.AsyncClient) -> None:
    response = await http.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "satori": True, "subscribers": 0}


async def test_webhook_publishes_satori_event(server: YHChatServer, http: httpx.AsyncClient) -> None:
    async with server.bus.subscribe() as queue:
        response = await http.post("/webhook", json=MESSAGE_EVENT)

        assert response.status_code == 200
        assert response.json() == {}
        event = await asyncio.wait_for(queue.get(), timeout=1)

        assert event.type == "message-created"
        assert event.sn == 1
        assert event.timestamp == 1700000000001
        assert event.login.platform == "yhchat"
        assert event.channel is not None
        assert event.channel.id == "g1"
        assert event.channel.type == 0
        assert event.guild is not None and event.guild.id == "g1"
        assert event.member is not None
        assert event.message is not None
        assert event.message.id == "m1"
        assert event.message.content == '<quote id="m0"/><at id="u2"/>hi'
        assert event.message.user is not None and event.message.user.name == "小明"
        assert event.referrer == {"event_id": "e1", "event_type": "message.receive.normal"}
        # 入站事件学到的会话类型要进注册表，供后续发送使用
        assert server.backend.registry.recv_type("g1") == "group"


async def test_webhook_direct_chat_has_no_guild(server: YHChatServer, http: httpx.AsyncClient) -> None:
    payload = {
        "header": {"eventId": "e2", "eventType": "message.receive.normal"},
        "event": {
            "sender": {"senderId": "u1", "senderType": "user"},
            "chat": {"chatId": "u1", "chatType": "user"},
            "message": {"msgId": "m2", "sendTime": 1, "contentType": "text", "content": {"text": "hi"}},
        },
    }
    async with server.bus.subscribe() as queue:
        assert (await http.post("/webhook", json=payload)).status_code == 200
        event = await asyncio.wait_for(queue.get(), timeout=1)

        assert event.channel is not None and event.channel.type == 1
        assert event.guild is None
        assert event.member is None
        assert server.backend.registry.recv_type("u1") == "user"


async def test_webhook_ignores_non_message_events(server: YHChatServer, http: httpx.AsyncClient) -> None:
    payload = {"header": {"eventId": "e3", "eventType": "group.join"}, "event": {}}
    async with server.bus.subscribe() as queue:
        response = await http.post("/webhook", json=payload)

        assert response.status_code == 200
        with pytest.raises(TimeoutError):
            await asyncio.wait_for(queue.get(), timeout=0.05)


async def test_webhook_rejects_broken_payload(server: YHChatServer, http: httpx.AsyncClient) -> None:
    broken = await http.post("/webhook", json={"header": {"eventType": "message.receive.normal"}})
    assert broken.status_code == 400

    not_json = await http.post("/webhook", headers={"Content-Type": "application/json"}, content=b"{not json")
    assert not_json.status_code == 400


async def test_satori_is_mounted(http: httpx.AsyncClient) -> None:
    response = await http.post(
        "/satori/v1/reaction.create",
        headers={"Authorization": "Bearer satori-tk"},
        json={"channel_id": "g1"},
    )

    assert response.status_code == 404
    assert "reaction.create" in response.json()["message"]


async def test_satori_mount_requires_token(http: httpx.AsyncClient) -> None:
    response = await http.post("/satori/v1/message.get", json={"channel_id": "g1", "message_id": "m1"})

    assert response.status_code == 401


async def test_webhook_path_is_configurable(sdk_client: YHChatClient) -> None:
    custom = YHChatServer(sdk_client, self_id="bot-1", webhook_path="/yh/callback")
    transport = httpx.ASGITransport(app=custom.build_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        assert (await client.post("/yh/callback", json=MESSAGE_EVENT)).status_code == 200
        assert (await client.post("/webhook", json=MESSAGE_EVENT)).status_code == 404


async def test_webhook_dedupes_by_event_id(server: YHChatServer, http: httpx.AsyncClient) -> None:
    async with server.bus.subscribe() as queue:
        first = await http.post("/webhook", json=MESSAGE_EVENT)
        second = await http.post("/webhook", json=MESSAGE_EVENT)

        assert first.json() == {}
        assert second.json() == {"duplicated": True}
        event = await asyncio.wait_for(queue.get(), timeout=1)
        assert event.sn == 1
        assert queue.empty()
