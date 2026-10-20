"""``v1`` 的 protobuf 端点：请求编码、响应解析、Status 错误映射。"""

from collections.abc import AsyncIterator
from typing import Any

import httpx
import pytest
import respx
from google.protobuf.message import Message

from yhchat import YHChatClient
from yhchat.errors import APIError, TransportError
from yhchat.proto._pb import full_pb2

BASE_URL = "https://chat-go.jwzhd.com"
PROTOBUF = "application/x-protobuf"


@pytest.fixture
async def client() -> AsyncIterator[YHChatClient]:
    async with YHChatClient("bot-token", user_token="user-token", http2=False, trust_env=False) as sdk:
        yield sdk


def status_response(code: int = 1, msg: str = "success") -> bytes:
    return full_pb2.StatusResponse(status=full_pb2.Status(code=code, msg=msg)).SerializeToString()


def message_list() -> full_pb2.ListMsgResponse:
    return full_pb2.ListMsgResponse(
        status=full_pb2.Status(code=1, msg="success"),
        total=2,
        data=[
            full_pb2.ListMsgResponse.MsgData(
                msg_id="m1",
                content_type=full_pb2.ContentType.text,
                content=full_pb2.MsgContent(text="第一条"),
                sender=full_pb2.Sender(chat_id="u1", chat_type=full_pb2.ChatType.user, name="小明"),
                msg_seq=11,
            ),
            full_pb2.ListMsgResponse.MsgData(msg_id="m2", content=full_pb2.MsgContent(text="第二条"), msg_seq=12),
        ],
    )


async def test_send_message_encodes_request_and_parses_status(client: YHChatClient) -> None:
    request = full_pb2.SendMsgRequest(
        chat_id="group-1",
        chat_type=full_pb2.ChatType.group,
        content_type=full_pb2.ContentType.text,
        content=full_pb2.MsgContent(text="你好"),
    )
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/v1/msg/send-message").mock(return_value=httpx.Response(200, content=status_response()))

        response = await client.v1.proto.msg.send_message(request)

        sent = route.calls.last.request
        assert sent.headers["content-type"] == PROTOBUF
        assert sent.headers["token"] == "user-token"
        decoded = full_pb2.SendMsgRequest.FromString(sent.content)
        assert decoded.chat_id == "group-1"
        assert decoded.chat_type == full_pb2.ChatType.group
        assert decoded.content.text == "你好"
        assert response.status.code == 1


async def test_list_message_parses_nested_messages(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/msg/list-message").mock(
            return_value=httpx.Response(200, content=message_list().SerializeToString())
        )

        response = await client.v1.proto.msg.list_message(
            full_pb2.ListMsgRequest(chat_id="group-1", chat_type=full_pb2.ChatType.group, msg_count=2)
        )

        assert response.total == 2
        assert [item.msg_id for item in response.data] == ["m1", "m2"]
        assert response.data[0].content.text == "第一条"
        assert response.data[0].sender.name == "小明"
        assert response.data[0].content_type == full_pb2.ContentType.text


async def test_status_code_maps_to_api_error(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/msg/recall-msg").mock(
            return_value=httpx.Response(200, content=status_response(-101, "未登录"))
        )

        with pytest.raises(APIError) as excinfo:
            await client.v1.proto.msg.recall_message(full_pb2.RecallMsg(chat_id="c1", msg_id=["m1"]))

        assert excinfo.value.code == -101
        assert excinfo.value.message == "未登录"
        assert excinfo.value.endpoint == "/v1/msg/recall-msg"


async def test_http_error_maps_to_transport_error(client: YHChatClient) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/msg/send-message").mock(return_value=httpx.Response(502, content=b""))

        with pytest.raises(TransportError, match="502"):
            await client.v1.proto.msg.send_message(full_pb2.SendMsgRequest(chat_id="c1"))


@pytest.mark.parametrize(
    ("method", "path", "request_message"),
    [
        ("edit_message", "/v1/msg/edit-message", full_pb2.SendMsgRequest(chat_id="c1")),
        ("list_message_by_seq", "/v1/msg/list-message-by-seq", full_pb2.ListMsgBySeqRequest(chat_id="c1")),
        (
            "list_message_by_mid_seq",
            "/v1/msg/list-message-by-mid-seq",
            full_pb2.ListMsgByMidSeqRequest(chat_id="c1", msg_id="m1"),
        ),
        (
            "list_message_image",
            "/v1/msg/pic-list-message-by-mid-seq",
            full_pb2.PicListMsgByMidSeqRequest(chat_id="c1", image_id=7),
        ),
        ("recall_messages", "/v1/msg/recall-msg-batch", full_pb2.RecallMsg(chat_id="c1", msg_id=["m1", "m2"])),
        (
            "report_button",
            "/v1/msg/button-report",
            full_pb2.ButtonReportRequest(msg_id="m1", chat_id="c1", button_value="ok"),
        ),
    ],
)
async def test_endpoint_paths(
    client: YHChatClient, method: str, path: str, request_message: Message
) -> None:
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post(path).mock(return_value=httpx.Response(200, content=status_response()))
        call: Any = getattr(client.v1.proto.msg, method)
        await call(request_message)
        assert route.called
