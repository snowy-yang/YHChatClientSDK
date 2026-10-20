"""``v1`` 的 protobuf 端点（msg / user / group / group-tag / instruction）：编码、解析、错误映射。"""

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
    ("group_name", "method", "path", "request_message"),
    [
        ("msg", "edit_message", "/v1/msg/edit-message", full_pb2.SendMsgRequest(chat_id="c1")),
        ("msg", "list_message_by_seq", "/v1/msg/list-message-by-seq", full_pb2.ListMsgBySeqRequest(chat_id="c1")),
        (
            "msg",
            "list_message_by_mid_seq",
            "/v1/msg/list-message-by-mid-seq",
            full_pb2.ListMsgByMidSeqRequest(chat_id="c1", msg_id="m1"),
        ),
        (
            "msg",
            "list_message_image",
            "/v1/msg/pic-list-message-by-mid-seq",
            full_pb2.PicListMsgByMidSeqRequest(chat_id="c1", image_id=7),
        ),
        ("msg", "recall_messages", "/v1/msg/recall-msg-batch", full_pb2.RecallMsg(chat_id="c1", msg_id=["m1", "m2"])),
        (
            "msg",
            "report_button",
            "/v1/msg/button-report",
            full_pb2.ButtonReportRequest(msg_id="m1", chat_id="c1", button_value="ok"),
        ),
        ("user", "get_user", "/v1/user/get-user", full_pb2.GetUserRequest(id="u1")),
        ("user", "get_self_medal", "/v1/user/medal", full_pb2.Empty()),
        ("user", "edit_nickname", "/v1/user/edit-nickname", full_pb2.EditNicknameRequest(name="新名字")),
        ("user", "edit_avatar", "/v1/user/edit-avatar", full_pb2.EditAvatarRequest(url="https://a/b.png")),
        ("group", "info", "/v1/group/info", full_pb2.GroupInfoRequest(group_id="g1")),
        ("group", "list_member", "/v1/group/list-member", full_pb2.ListMemberRequest(group_id="g1")),
        ("group", "edit_group", "/v1/group/edit-group", full_pb2.EditGroupRequest(group_id="g1", name="新群名")),
        ("group", "bot_list", "/v1/group/bot-list", full_pb2.BotListRequest(group_id="g1")),
        (
            "group",
            "info_add_friend",
            "/v1/group/info-add-friend",
            full_pb2.InfoAddFriendRequest(keyword="口令"),
        ),
        ("group", "create_group", "/v1/group/create-group", full_pb2.CreateGroupRequest(name="新群")),
        ("group", "dismiss_group", "/v1/group/dismiss-group", full_pb2.DismissGroupRequest(group_id="g1")),
        ("group_tag", "members", "/v1/group-tag/members", full_pb2.TagMemberRequest(group_id="g1", tag_id=3)),
        (
            "instruction",
            "list_instructions",
            "/v1/instruction/list",
            full_pb2.GetBotInstructionRequest(bot_id="b1"),
        ),
    ],
)
async def test_endpoint_paths(
    client: YHChatClient, group_name: str, method: str, path: str, request_message: Message
) -> None:
    group: Any = getattr(client.v1.proto, group_name)
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post(path).mock(return_value=httpx.Response(200, content=status_response()))
        if method == "get_self_medal":  # 这个端点没有请求体
            await group.get_self_medal()
        else:
            await getattr(group, method)(request_message)
        assert route.called


async def test_group_info_parses_group_data_and_bots(client: YHChatClient) -> None:
    payload = full_pb2.GroupInfoResponse(
        status=full_pb2.Status(code=1, msg="success"),
        data=full_pb2.GroupData(
            group_id="g1",
            name="测试群",
            headcount=42,
            admin=["u1", "u2"],
            tag=[full_pb2.Tag(id=5, text="标签")],
            my_group_nickname="我的群名片",
        ),
        bot=[full_pb2.BotData(bot_id="b1", name="机器人", headcount=7)],
    )
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/group/info").mock(return_value=httpx.Response(200, content=payload.SerializeToString()))

        response = await client.v1.proto.group.info(full_pb2.GroupInfoRequest(group_id="g1"))

        assert response.data.name == "测试群"
        assert list(response.data.admin) == ["u1", "u2"]
        assert response.data.tag[0].text == "标签"
        assert response.bot[0].name == "机器人"


async def test_list_member_parses_nested_user_info(client: YHChatClient) -> None:
    payload = full_pb2.ListMemberResponse(
        status=full_pb2.Status(code=1, msg="success"),
        total=1,
        user=[
            full_pb2.ListMemberResponse.User(
                group_id="g1",
                permission_level=2,
                user_info=full_pb2.ListMemberResponse.User.UserInfo(
                    user_id="u1", name="小明", avatar_url="https://a/b.png", is_vip=True
                ),
            )
        ],
    )
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/group/list-member").mock(return_value=httpx.Response(200, content=payload.SerializeToString()))

        response = await client.v1.proto.group.list_member(full_pb2.ListMemberRequest(group_id="g1"))

        assert response.total == 1
        assert response.user[0].user_info.name == "小明"
        assert response.user[0].permission_level == 2


async def test_instruction_list_parses_command(client: YHChatClient) -> None:
    payload = full_pb2.GetBotInstructionResponse(
        status=full_pb2.Status(code=1, msg="success"),
        data=full_pb2.GetBotInstructionResponse.Data(
            command_id=9, bot_id="b1", command_name="/help", instruction_type=1
        ),
    )
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/instruction/list").mock(return_value=httpx.Response(200, content=payload.SerializeToString()))

        response = await client.v1.proto.instruction.list_instructions(full_pb2.GetBotInstructionRequest(bot_id="b1"))

        assert response.data.command_name == "/help"
        assert response.data.command_id == 9
