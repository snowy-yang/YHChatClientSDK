"""机器人消息接口的契约测试。

HTTP 层用 respx 模拟，只验证"请求长什么样"和"响应怎么解析"，不触碰真实云湖接口。
"""

import json
from collections.abc import AsyncIterator
from typing import Any, cast

import httpx
import pytest
import respx

from yhchat import TextSegment, YHChatClient
from yhchat.errors import APIError, TransportError
from yhchat.models import ImageSegment

BASE_URL = "https://chat-go.jwzhd.com"

MESSAGE_INFO: dict[str, Any] = {"msgId": "m1", "recvId": "g1", "recvType": "group"}


def ok(data: dict[str, Any]) -> httpx.Response:
    """构造一个云湖风格的成功响应。"""
    return httpx.Response(200, json={"code": 1, "msg": "success", "data": data})


def body_of(request: httpx.Request) -> dict[str, Any]:
    """读取请求体 JSON。"""
    return cast("dict[str, Any]", json.loads(request.content))


@pytest.fixture
async def client() -> AsyncIterator[YHChatClient]:
    """指向模拟后端的客户端（http2 关掉、不读环境代理，便于 respx 拦截）。"""
    async with YHChatClient("test-token", http2=False, trust_env=False) as value:
        yield value


async def test_send_builds_documented_body(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/open-apis/v1/bot/send").mock(return_value=ok({"messageInfo": MESSAGE_INFO}))

        info = await client.bot.message.send("group", "g1", TextSegment(text="你好", at=["u1", "u2"]), parent_id="p1")

        request = route.calls.last.request
        assert request.url.params["token"] == "test-token"
        assert body_of(request) == {
            "recvId": "g1",
            "recvType": "group",
            "contentType": "text",
            "content": {"text": "你好", "at": "u1,u2"},
            "parentId": "p1",
        }
        assert info.msg_id == "m1"
        assert len(client.records) == 1
        assert client.records.get("m1") is not None


async def test_buttons_are_serialized_with_camel_case_alias(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/open-apis/v1/bot/send").mock(return_value=ok({"messageInfo": MESSAGE_INFO}))
        segment = TextSegment.model_validate(
            {"text": "带按钮", "buttons": [[{"text": "跳转", "actionType": 1, "url": "https://example.com"}]]}
        )

        await client.bot.message.send("group", "g1", segment)

        assert body_of(route.calls.last.request)["content"]["buttons"] == [
            [{"text": "跳转", "actionType": 1, "url": "https://example.com"}]
        ]


async def test_edit_fills_session_from_records(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/open-apis/v1/bot/send").mock(return_value=ok({"messageInfo": MESSAGE_INFO}))
        edit = mock.post("/open-apis/v1/bot/edit").mock(return_value=ok({"successCount": 1}))

        await client.bot.message.send("group", "g1", TextSegment(text="原文"))
        count = await client.bot.message.edit("m1", TextSegment(text="改后"))

        assert count == 1
        assert body_of(edit.calls.last.request) == {
            "msgId": "m1",
            "recvId": "g1",
            "recvType": "group",
            "contentType": "text",
            "content": {"text": "改后"},
        }


async def test_recall_uses_chat_fields_and_drops_record(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/open-apis/v1/bot/send").mock(return_value=ok({"messageInfo": MESSAGE_INFO}))
        recall = mock.post("/open-apis/v1/bot/recall").mock(
            return_value=httpx.Response(200, json={"code": 1, "msg": "success"})
        )

        await client.bot.message.send("group", "g1", TextSegment(text="待撤回"))
        await client.bot.message.recall("m1")

        assert body_of(recall.calls.last.request) == {"msgId": "m1", "chatId": "g1", "chatType": "group"}
        assert client.records.get("m1") is None


async def test_recall_without_record_raises(client: YHChatClient) -> None:
    with pytest.raises(ValueError, match="找不到"):
        await client.bot.message.recall("unknown")


async def test_list_messages_passes_query_params(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/open-apis/v1/bot/messages").mock(
            return_value=ok(
                {
                    "list": [
                        {
                            "msgId": "m9",
                            "senderId": "u1",
                            "senderType": "user",
                            "contentType": "text",
                            "content": {"text": "hi", "imageWidth": 12},
                            "sendTime": 1700000000000,
                        }
                    ],
                    "total": 1,
                }
            )
        )

        page = await client.bot.message.list("g1", "group", message_id="m9", before=5, after=0)

        params = route.calls.last.request.url.params
        assert params["chat-id"] == "g1"
        assert params["chat-type"] == "group"
        assert params["message-id"] == "m9"
        assert params["before"] == "5"
        assert page.total == 1
        assert page.messages[0].msg_id == "m9"
        assert page.messages[0].content.image_width == 12


async def test_batch_send_returns_success_list(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/open-apis/v1/bot/batch_send").mock(
            return_value=ok(
                {"successCount": 2, "successList": [MESSAGE_INFO, {"msgId": "m2", "recvId": "g2", "recvType": "group"}]}
            )
        )

        result = await client.bot.message.batch_send(["g1", "g2"], "group", TextSegment(text="广播"))

        assert body_of(route.calls.last.request)["recvIds"] == ["g1", "g2"]
        assert result.success_count == 2
        assert len(client.records) == 2


async def test_send_stream_uses_chunked_body(client: YHChatClient) -> None:
    async def chunks() -> AsyncIterator[str]:
        yield "第"
        yield "一段"

    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/open-apis/v1/bot/send-stream").mock(return_value=ok({"messageInfo": MESSAGE_INFO}))

        info = await client.bot.message.send_stream("group", "g1", "text", chunks())

        request = route.calls.last.request
        assert request.url.params["recvId"] == "g1"
        assert request.url.params["recvType"] == "group"
        assert request.url.params["contentType"] == "text"
        assert request.headers["Transfer-Encoding"] == "chunked"
        assert request.content == "第一段".encode()
        assert info.recv_id == "g1"


async def test_upload_image_returns_key(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/open-apis/v1/image/upload").mock(return_value=ok({"imageKey": "abc.png"}))

        key = await client.bot.upload.image(b"\x89PNG", filename="abc.png", mime_type="image/png")

        request = route.calls.last.request
        assert request.headers["Content-Type"].startswith("multipart/form-data; boundary=")
        assert b'name="image"; filename="abc.png"' in request.content
        assert request.url.params["token"] == "test-token"
        assert key == "abc.png"


async def test_upload_without_key_raises_transport_error(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/open-apis/v1/video/upload").mock(return_value=ok({}))

        with pytest.raises(TransportError, match="videoKey"):
            await client.bot.upload.video(b"xx")


async def test_api_error_carries_code_and_message(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/open-apis/v1/bot/send").mock(
            return_value=httpx.Response(200, json={"code": 0, "msg": "token 无效"})
        )

        with pytest.raises(APIError) as excinfo:
            await client.bot.message.send("group", "g1", TextSegment(text="x"))

        assert excinfo.value.code == 0
        assert excinfo.value.message == "token 无效"
        assert excinfo.value.endpoint == "/open-apis/v1/bot/send"


async def test_http_error_with_json_body_becomes_api_error(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/open-apis/v1/bot/send").mock(return_value=httpx.Response(502, json={"code": 0, "msg": "boom"}))

        with pytest.raises(APIError) as excinfo:
            await client.bot.message.send("group", "g1", TextSegment(text="x"))

        assert excinfo.value.code == 0
        assert excinfo.value.message == "boom"


async def test_non_json_response_becomes_transport_error(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/open-apis/v1/bot/send").mock(return_value=httpx.Response(200, text="<html>502</html>"))

        with pytest.raises(TransportError, match="非 JSON"):
            await client.bot.message.send("group", "g1", TextSegment(text="x"))


async def test_connection_failure_becomes_transport_error(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/open-apis/v1/bot/send").mock(side_effect=httpx.ConnectError("no route"))

        with pytest.raises(TransportError, match="请求失败"):
            await client.bot.message.send("group", "g1", TextSegment(text="x"))


async def test_image_segment_content_shape(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/open-apis/v1/bot/send").mock(return_value=ok({"messageInfo": MESSAGE_INFO}))

        await client.bot.message.send("user", "u1", ImageSegment(key="k.png"))

        payload = body_of(route.calls.last.request)
        assert payload["contentType"] == "image"
        assert payload["content"] == {"imageKey": "k.png"}
