"""``v1`` 的 protobuf 端点（``msg`` / ``user``）：请求编码、响应解析、Status 错误映射。"""

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
        mock.post("/v1/msg/recall-msg").mock(return_value=httpx.Response(200, content=status_response(-101, "未登录")))

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
        ("get_user", "/v1/user/get-user", full_pb2.GetUserRequest(id="u1")),
        ("get_self_medal", "/v1/user/medal", full_pb2.Empty()),
        ("edit_nickname", "/v1/user/edit-nickname", full_pb2.EditNicknameRequest(name="新名字")),
        ("edit_avatar", "/v1/user/edit-avatar", full_pb2.EditAvatarRequest(url="https://a/b.png")),
    ],
)
async def test_endpoint_paths(client: YHChatClient, method: str, path: str, request_message: Message) -> None:
    user_methods = {"get_user", "get_self_medal", "edit_nickname", "edit_avatar"}
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post(path).mock(return_value=httpx.Response(200, content=status_response()))
        if method == "get_self_medal":  # 这个端点没有请求体
            await client.v1.proto.user.get_self_medal()
        elif method in user_methods:
            user_call: Any = getattr(client.v1.proto.user, method)
            await user_call(request_message)
        else:
            msg_call: Any = getattr(client.v1.proto.msg, method)
            await msg_call(request_message)
        assert route.called


async def test_get_user_parses_nested_profile(client: YHChatClient) -> None:
    payload = full_pb2.GetUserResponse(
        status=full_pb2.Status(code=1, msg="success"),
        data=full_pb2.GetUserResponse.Data(
            id="u1",
            name="小明",
            medal=[full_pb2.MedalInfo(id=3, name="元老", sort=1)],
            vip_status=full_pb2.VipStatus.VIP_STATUS_ACTIVE,
            remark_info=full_pb2.RemarkInfo(remark_name="备注名"),
            profile_info=full_pb2.ProfileInfo(introduction="简介", gender=1),
        ),
    )
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/v1/user/get-user").mock(
            return_value=httpx.Response(200, content=payload.SerializeToString())
        )

        response = await client.v1.proto.user.get_user(full_pb2.GetUserRequest(id="u1"))

        assert full_pb2.GetUserRequest.FromString(route.calls.last.request.content).id == "u1"
        assert response.data.name == "小明"
        assert response.data.medal[0].name == "元老"
        assert response.data.vip_status == full_pb2.VipStatus.VIP_STATUS_ACTIVE
        assert response.data.remark_info.remark_name == "备注名"


async def test_medal_request_has_no_body(client: YHChatClient) -> None:
    payload = full_pb2.GetSelfMedal(
        status=full_pb2.Status(code=1, msg="success"),
        medal=[full_pb2.MedalInfo(id=1, name="新人")],
    )
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/v1/user/medal").mock(return_value=httpx.Response(200, content=payload.SerializeToString()))

        response = await client.v1.proto.user.get_self_medal()

        assert route.calls.last.request.content == b""
        assert [item.name for item in response.medal] == ["新人"]
