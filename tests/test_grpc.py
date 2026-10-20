"""gRPC 门面的契约测试：起真实 gRPC 服务，HTTP 层用 respx 模拟。"""

import json
from collections.abc import AsyncIterator
from typing import Any, cast

import grpc
import httpx
import pytest
import respx

from yhchat import YHChatClient
from yhchat.grpc import YHChatRpcClient, content_from_segment, segment_from_content, serve
from yhchat.grpc._pb import yhchat_pb2
from yhchat.models import Button, ImageSegment, MarkdownSegment, TextSegment

BASE_URL = "https://chat-go.jwzhd.com"

MESSAGE_INFO: dict[str, Any] = {"msgId": "m1", "recvId": "g1", "recvType": "group"}


def ok(data: dict[str, Any]) -> httpx.Response:
    return httpx.Response(200, json={"code": 1, "msg": "success", "data": data})


def body_of(request: httpx.Request) -> dict[str, Any]:
    return cast("dict[str, Any]", json.loads(request.content))


@pytest.fixture
async def rpc() -> AsyncIterator[tuple[YHChatRpcClient, YHChatClient]]:
    """起一个 gRPC 服务（端口由系统分配），返回强类型客户端与它背后的 SDK 客户端。"""
    async with YHChatClient("test-token", http2=False, trust_env=False) as client:
        server, port = await serve(client, port=0)
        channel = grpc.aio.insecure_channel(f"127.0.0.1:{port}")
        try:
            yield YHChatRpcClient(channel), client
        finally:
            await channel.close()
            await server.stop(grace=0)


def test_text_content_roundtrip() -> None:
    segment = TextSegment(
        text="你好",
        at=["u1", "u2"],
        buttons=[[Button.model_validate({"text": "跳转", "actionType": 1, "url": "https://example.com"})]],
    )

    content = content_from_segment(segment)

    assert content.type == yhchat_pb2.CONTENT_TYPE_TEXT
    assert content.text == "你好"
    assert content.at == "u1,u2"
    assert content.buttons[0].buttons[0].action_type == 1

    restored = segment_from_content(content)
    assert isinstance(restored, TextSegment)
    assert restored.text == "你好"
    assert list(restored.at or []) == ["u1", "u2"]
    assert restored.buttons is not None
    assert restored.buttons[0][0].url == "https://example.com"


def test_media_content_roundtrip() -> None:
    assert isinstance(segment_from_content(content_from_segment(ImageSegment(key="a.png"))), ImageSegment)
    assert isinstance(segment_from_content(content_from_segment(MarkdownSegment(text="**x**"))), MarkdownSegment)


async def test_send_roundtrip(rpc: tuple[YHChatRpcClient, YHChatClient]) -> None:
    stub, _ = rpc
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/open-apis/v1/bot/send").mock(return_value=ok({"messageInfo": MESSAGE_INFO}))

        reply = await stub.send(
            yhchat_pb2.SendRequest(
                recv_type="group",
                recv_id="g1",
                content=yhchat_pb2.Content(type=yhchat_pb2.CONTENT_TYPE_TEXT, text="hi", at="u1"),
            )
        )

        assert reply.message.msg_id == "m1"
        assert reply.message.recv_id == "g1"
        assert body_of(route.calls.last.request) == {
            "recvId": "g1",
            "recvType": "group",
            "contentType": "text",
            "content": {"text": "hi", "at": "u1"},
            "parentId": None,
        }


async def test_edit_reuses_message_record(rpc: tuple[YHChatRpcClient, YHChatClient]) -> None:
    stub, _ = rpc
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/open-apis/v1/bot/send").mock(return_value=ok({"messageInfo": MESSAGE_INFO}))
        edit = mock.post("/open-apis/v1/bot/edit").mock(return_value=ok({"successCount": 1}))

        await stub.send(
            yhchat_pb2.SendRequest(
                recv_type="group",
                recv_id="g1",
                content=yhchat_pb2.Content(type=yhchat_pb2.CONTENT_TYPE_TEXT, text="原文"),
            )
        )
        reply = await stub.edit(
            yhchat_pb2.EditRequest(
                msg_id="m1", content=yhchat_pb2.Content(type=yhchat_pb2.CONTENT_TYPE_MARKDOWN, text="**改后**")
            )
        )

        assert reply.success_count == 1
        assert body_of(edit.calls.last.request) == {
            "msgId": "m1",
            "recvId": "g1",
            "recvType": "group",
            "contentType": "markdown",
            "content": {"text": "**改后**"},
        }


async def test_list_messages_roundtrip(rpc: tuple[YHChatRpcClient, YHChatClient]) -> None:
    stub, _ = rpc
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
                            "content": {"text": "hi", "at": ["u1"]},
                            "sendTime": 1700000000000,
                        }
                    ],
                    "total": 1,
                }
            )
        )

        reply = await stub.list_messages(yhchat_pb2.ListMessagesRequest(chat_id="g1", chat_type="group", before=5))

        assert route.calls.last.request.url.params["chat-id"] == "g1"
        assert reply.total == 1
        assert reply.messages[0].msg_id == "m9"
        assert reply.messages[0].text == "hi"
        assert list(reply.messages[0].at) == ["u1"]


async def test_upload_roundtrip(rpc: tuple[YHChatRpcClient, YHChatClient]) -> None:
    stub, _ = rpc
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/open-apis/v1/image/upload").mock(return_value=ok({"imageKey": "abc.png"}))

        reply = await stub.upload(
            yhchat_pb2.UploadRequest(
                kind=yhchat_pb2.UploadRequest.KIND_IMAGE,
                filename="abc.png",
                mime_type="image/png",
                data=b"\x89PNG",
            )
        )

        assert reply.key == "abc.png"
        assert b'name="image"; filename="abc.png"' in route.calls.last.request.content


async def test_send_stream_roundtrip(rpc: tuple[YHChatRpcClient, YHChatClient]) -> None:
    stub, _ = rpc

    async def requests() -> AsyncIterator[yhchat_pb2.SendStreamRequest]:
        yield yhchat_pb2.SendStreamRequest(recv_type="group", recv_id="g1", content_type="text", chunk="第".encode())
        yield yhchat_pb2.SendStreamRequest(chunk="二段".encode())

    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/open-apis/v1/bot/send-stream").mock(return_value=ok({"messageInfo": MESSAGE_INFO}))

        reply = await stub.send_stream(requests())

        assert route.calls.last.request.url.params["contentType"] == "text"
        assert route.calls.last.request.content == "第二段".encode()
        assert reply.message.msg_id == "m1"


async def test_api_error_maps_to_grpc_status(rpc: tuple[YHChatRpcClient, YHChatClient]) -> None:
    stub, _ = rpc
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/open-apis/v1/bot/send").mock(
            return_value=httpx.Response(200, json={"code": 0, "msg": "token 无效"})
        )

        with pytest.raises(grpc.aio.AioRpcError) as excinfo:
            await stub.send(
                yhchat_pb2.SendRequest(
                    recv_type="group",
                    recv_id="g1",
                    content=yhchat_pb2.Content(type=yhchat_pb2.CONTENT_TYPE_TEXT, text="x"),
                )
            )

        assert excinfo.value.code() == grpc.StatusCode.FAILED_PRECONDITION
        assert "token 无效" in (excinfo.value.details() or "")


async def test_unknown_content_type_maps_to_invalid_argument(rpc: tuple[YHChatRpcClient, YHChatClient]) -> None:
    stub, _ = rpc

    with pytest.raises(grpc.aio.AioRpcError) as excinfo:
        await stub.send(yhchat_pb2.SendRequest(recv_type="group", recv_id="g1", content=yhchat_pb2.Content()))

    assert excinfo.value.code() == grpc.StatusCode.INVALID_ARGUMENT
