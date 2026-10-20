"""云湖后端适配：content ↔ 消息段、云湖消息 → Satori 模型。"""

import json
from collections.abc import AsyncIterator
from typing import Any, cast

import httpx
import pytest
import respx

from yhchat import YHChatClient
from yhchat.models import FileSegment, ImageSegment, ReceivedMessage, TextSegment
from yhchat.satori.backend import (
    SatoriNotFoundError,
    SatoriUnsupportedError,
    YHChatBackend,
    render_message_content,
    segment_from_content,
)

BASE_URL = "https://chat-go.jwzhd.com"
MESSAGE_INFO: dict[str, Any] = {"msgId": "m1", "recvId": "g1", "recvType": "group"}


def ok(data: dict[str, Any]) -> httpx.Response:
    return httpx.Response(200, json={"code": 1, "msg": "success", "data": data})


def body_of(request: httpx.Request) -> dict[str, Any]:
    return cast("dict[str, Any]", json.loads(request.content))


@pytest.fixture
async def backend() -> AsyncIterator[YHChatBackend]:
    async with YHChatClient("test-token", http2=False, trust_env=False) as client:
        yield YHChatBackend(client, self_id="bot-1")


async def test_message_create_text_with_at_and_quote(backend: YHChatBackend) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/open-apis/v1/bot/send").mock(return_value=ok({"messageInfo": MESSAGE_INFO}))

        objects = await backend.message_create("g1", 'hi <at id="u1"/><quote id="m0"/>', {"message_id": "m0"})

        assert body_of(route.calls.last.request) == {
            "recvId": "g1",
            "recvType": "group",
            "contentType": "text",
            "content": {"text": "hi ", "at": "u1"},
            "parentId": "m0",
        }
        assert objects[0].id == "m1"
        assert objects[0].channel is not None
        assert objects[0].channel.type == 0
        assert objects[0].guild is not None
        assert objects[0].guild.id == "g1"
        assert objects[0].referrer == {"message_id": "m0"}


async def test_message_create_direct_channel_uses_registry(backend: YHChatBackend) -> None:
    backend.registry.remember("u9", "user")
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/open-apis/v1/bot/send").mock(
            return_value=ok({"messageInfo": {"msgId": "m2", "recvId": "u9", "recvType": "user"}})
        )

        objects = await backend.message_create("u9", "hi", None)

        assert body_of(route.calls.last.request)["recvType"] == "user"
        assert objects[0].channel is not None
        assert objects[0].channel.type == 1
        assert objects[0].guild is None
        assert objects[0].member is None


async def test_message_get_found(backend: YHChatBackend) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/open-apis/v1/bot/messages").mock(
            return_value=ok(
                {
                    "list": [
                        {
                            "msgId": "m9",
                            "senderId": "u1",
                            "senderType": "user",
                            "senderNickname": "小明",
                            "contentType": "text",
                            "content": {"text": "hi", "at": ["u2"]},
                            "sendTime": 1700000000000,
                        }
                    ],
                    "total": 1,
                }
            )
        )

        message = await backend.message_get("g1", "m9")

        assert message.id == "m9"
        assert message.content == '<at id="u2"/>hi'
        assert message.user is not None
        assert message.user.name == "小明"
        assert message.member is not None
        assert message.created_at == 1700000000000


async def test_message_get_missing_raises_not_found(backend: YHChatBackend) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/open-apis/v1/bot/messages").mock(return_value=ok({"list": [], "total": 0}))

        with pytest.raises(SatoriNotFoundError):
            await backend.message_get("g1", "nope")


async def test_message_list_uses_cursor_and_direction(backend: YHChatBackend) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/open-apis/v1/bot/messages").mock(
            return_value=ok(
                {
                    "list": [
                        {"msgId": "m1", "senderId": "u1", "senderType": "user", "contentType": "text"},
                        {"msgId": "m2", "senderId": "u1", "senderType": "user", "contentType": "text"},
                    ],
                    "total": 2,
                }
            )
        )

        page = await backend.message_list("g1", "cursor", "after", 2, "desc")

        params = route.calls.last.request.url.params
        assert params["chat-id"] == "g1"
        assert params["message-id"] == "cursor"
        assert params["before"] == "0"
        assert params["after"] == "2"
        assert [item.id for item in page.data] == ["m2", "m1"]
        assert page.next == "m2"


async def test_message_update_and_delete(backend: YHChatBackend) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        edit = mock.post("/open-apis/v1/bot/edit").mock(return_value=ok({"successCount": 1}))
        recall = mock.post("/open-apis/v1/bot/recall").mock(return_value=ok({}))

        await backend.message_update("g1", "m1", "**改后**")
        await backend.message_delete("g1", "m1")

        assert body_of(edit.calls.last.request) == {
            "msgId": "m1",
            "recvId": "g1",
            "recvType": "group",
            "contentType": "text",
            "content": {"text": "**改后**"},
        }
        assert body_of(recall.calls.last.request) == {"msgId": "m1", "chatId": "g1", "chatType": "group"}


async def test_unsupported_actions_raise(backend: YHChatBackend) -> None:
    for call in (
        lambda: backend.guild_list(None),
        lambda: backend.guild_member_get("g1", "u1"),
        lambda: backend.guild_member_list("g1", None),
        lambda: backend.friend_list(None),
        lambda: backend.channel_list(None),
    ):
        with pytest.raises(SatoriUnsupportedError):
            await call()


async def test_login_and_channel_get(backend: YHChatBackend) -> None:
    login = await backend.login()
    channel = await backend.channel_get("g1")

    assert login.platform == "yhchat"
    assert login.user.id == "bot-1"
    assert channel.id == "g1"
    assert channel.type == 0


def test_segment_from_content_maps_media_and_text() -> None:
    assert isinstance(segment_from_content('<img src="a.png"/>'), ImageSegment)
    assert isinstance(segment_from_content('<file src="f.bin"/>'), FileSegment)
    text = segment_from_content('hi <at id="u1"/><at id="u2"/>')
    assert isinstance(text, TextSegment)
    assert text.text == "hi "
    assert text.at == ["u1", "u2"]


def test_render_message_content_image_and_quote() -> None:
    message = ReceivedMessage.model_validate(
        {
            "msgId": "m1",
            "parentId": "m0",
            "senderId": "u1",
            "senderType": "user",
            "contentType": "image",
            "content": {"at": ["u2"], "imageName": "a.png"},
        }
    )

    assert render_message_content(message) == '<quote id="m0"/><at id="u2"/><img src="a.png"/>'
