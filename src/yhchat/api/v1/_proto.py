"""``v1`` 的 protobuf 端点（手写；JSON 端点由 ``tools/gen_v1_api.py`` 生成）。

``v1`` 里有 29 个端点用 protobuf 收发，无法像 JSON 端点那样按路径自动生成，
所以在这里按文档 + ``full.proto`` 的字段号显式实现，挂在 ``client.v1.proto`` 下。
"""

from typing import TypeVar, cast

from google.protobuf.message import Message

from ...errors import APIError
from ...proto._pb import full_pb2
from ...transport import HttpTransport

MessageT = TypeVar("MessageT", bound=Message)

PROTO_ENDPOINTS: frozenset[str] = frozenset(
    {
        "/v1/msg/send-message",
        "/v1/msg/edit-message",
        "/v1/msg/list-message",
        "/v1/msg/list-message-by-seq",
        "/v1/msg/list-message-by-mid-seq",
        "/v1/msg/pic-list-message-by-mid-seq",
        "/v1/msg/recall-msg",
        "/v1/msg/recall-msg-batch",
        "/v1/msg/button-report",
        "/v1/user/get-user",
        "/v1/user/medal",
        "/v1/user/edit-nickname",
        "/v1/user/edit-avatar",
        "/v1/group/info",
        "/v1/group/list-member",
        "/v1/group/edit-group",
        "/v1/group/bot-list",
        "/v1/group/info-add-friend",
        "/v1/group/create-group",
        "/v1/group/dismiss-group",
        "/v1/group-tag/members",
        "/v1/instruction/list",
    }
)
"""已经实现的 protobuf 端点路径，生成器据此算覆盖率、写 ``implemented.txt``。"""


class V1ProtoAPI:
    """``client.v1.proto``：protobuf 端点按文档分组挂属性。"""

    def __init__(self, http: HttpTransport) -> None:
        self.msg = MsgProtoAPI(http)
        """``v1/msg`` 的 protobuf 端点。"""
        self.user = UserProtoAPI(http)
        """``v1/user`` 的 protobuf 端点。"""
        self.group = GroupProtoAPI(http)
        """``v1/group`` 的 protobuf 端点。"""
        self.group_tag = GroupTagProtoAPI(http)
        """``v1/group-tag`` 的 protobuf 端点。"""
        self.instruction = InstructionProtoAPI(http)
        """``v1/instruction`` 的 protobuf 端点。"""


class ProtoGroupAPI:
    """protobuf 分组的基类：统一把 ``Status.code != 1`` 转成 :class:`APIError`。"""

    def __init__(self, http: HttpTransport) -> None:
        self._http = http

    async def _call(self, path: str, message: Message, response_type: type[MessageT]) -> MessageT:
        response = await self._http.request_pb("POST", path, message, response_type)
        status = cast("full_pb2.Status | None", getattr(response, "status", None))
        if status is not None and status.code != 1:
            raise APIError(status.code, status.msg, endpoint=path)
        return response


class MsgProtoAPI(ProtoGroupAPI):
    """``v1/msg`` 的 protobuf 端点（9 个）。"""

    async def send_message(self, request: full_pb2.SendMsgRequest) -> full_pb2.StatusResponse:
        """发送消息。``POST /v1/msg/send-message``"""
        return await self._call("/v1/msg/send-message", request, full_pb2.StatusResponse)

    async def edit_message(self, request: full_pb2.SendMsgRequest) -> full_pb2.StatusResponse:
        """编辑消息（请求结构与发送相同）。``POST /v1/msg/edit-message``"""
        return await self._call("/v1/msg/edit-message", request, full_pb2.StatusResponse)

    async def list_message(self, request: full_pb2.ListMsgRequest) -> full_pb2.ListMsgResponse:
        """按消息 ID 列出消息。``POST /v1/msg/list-message``"""
        return await self._call("/v1/msg/list-message", request, full_pb2.ListMsgResponse)

    async def list_message_by_seq(self, request: full_pb2.ListMsgBySeqRequest) -> full_pb2.ListMsgResponse:
        """按消息序列列出消息（不含指定消息）。``POST /v1/msg/list-message-by-seq``"""
        return await self._call("/v1/msg/list-message-by-seq", request, full_pb2.ListMsgResponse)

    async def list_message_by_mid_seq(self, request: full_pb2.ListMsgByMidSeqRequest) -> full_pb2.ListMsgResponse:
        """按消息 ID + 序列列出消息（含指定消息）。``POST /v1/msg/list-message-by-mid-seq``"""
        return await self._call("/v1/msg/list-message-by-mid-seq", request, full_pb2.ListMsgResponse)

    async def list_message_image(self, request: full_pb2.PicListMsgByMidSeqRequest) -> full_pb2.ListMsgResponse:
        """取消息列表里的图片。``POST /v1/msg/pic-list-message-by-mid-seq``"""
        return await self._call("/v1/msg/pic-list-message-by-mid-seq", request, full_pb2.ListMsgResponse)

    async def recall_message(self, request: full_pb2.RecallMsg) -> full_pb2.StatusResponse:
        """撤回单条消息。``POST /v1/msg/recall-msg``"""
        return await self._call("/v1/msg/recall-msg", request, full_pb2.StatusResponse)

    async def recall_messages(self, request: full_pb2.RecallMsg) -> full_pb2.StatusResponse:
        """批量撤回消息（同一个请求结构，多条 ``msg_id``）。``POST /v1/msg/recall-msg-batch``"""
        return await self._call("/v1/msg/recall-msg-batch", request, full_pb2.StatusResponse)

    async def report_button(self, request: full_pb2.ButtonReportRequest) -> full_pb2.StatusResponse:
        """发送按钮点击事件。``POST /v1/msg/button-report``"""
        return await self._call("/v1/msg/button-report", request, full_pb2.StatusResponse)


class UserProtoAPI(ProtoGroupAPI):
    """``v1/user`` 的 protobuf 端点（4 个）。"""

    async def get_user(self, request: full_pb2.GetUserRequest) -> full_pb2.GetUserResponse:
        """获取指定用户信息。``POST /v1/user/get-user``"""
        return await self._call("/v1/user/get-user", request, full_pb2.GetUserResponse)

    async def get_self_medal(self) -> full_pb2.GetSelfMedal:
        """获取自身勋章。``POST /v1/user/medal``（无请求体）"""
        return await self._call("/v1/user/medal", full_pb2.Empty(), full_pb2.GetSelfMedal)

    async def edit_nickname(self, request: full_pb2.EditNicknameRequest) -> full_pb2.StatusResponse:
        """更改自身昵称。``POST /v1/user/edit-nickname``"""
        return await self._call("/v1/user/edit-nickname", request, full_pb2.StatusResponse)

    async def edit_avatar(self, request: full_pb2.EditAvatarRequest) -> full_pb2.StatusResponse:
        """更改自身头像。``POST /v1/user/edit-avatar``"""
        return await self._call("/v1/user/edit-avatar", request, full_pb2.StatusResponse)


class GroupProtoAPI(ProtoGroupAPI):
    """``v1/group`` 的 protobuf 端点（7 个）。"""

    async def info(self, request: full_pb2.GroupInfoRequest) -> full_pb2.GroupInfoResponse:
        """获取群聊信息。``POST /v1/group/info``"""
        return await self._call("/v1/group/info", request, full_pb2.GroupInfoResponse)

    async def list_member(self, request: full_pb2.ListMemberRequest) -> full_pb2.ListMemberResponse:
        """获取群成员列表（分页在 ``request.data``）。``POST /v1/group/list-member``"""
        return await self._call("/v1/group/list-member", request, full_pb2.ListMemberResponse)

    async def edit_group(self, request: full_pb2.EditGroupRequest) -> full_pb2.StatusResponse:
        """编辑群聊信息。``POST /v1/group/edit-group``"""
        return await self._call("/v1/group/edit-group", request, full_pb2.StatusResponse)

    async def bot_list(self, request: full_pb2.BotListRequest) -> full_pb2.BotListResponse:
        """获取群机器人列表（含指令与菜单）。``POST /v1/group/bot-list``"""
        return await self._call("/v1/group/bot-list", request, full_pb2.BotListResponse)

    async def info_add_friend(self, request: full_pb2.InfoAddFriendRequest) -> full_pb2.InfoAddFriendResponse:
        """用群口令查群聊。``POST /v1/group/info-add-friend``"""
        return await self._call("/v1/group/info-add-friend", request, full_pb2.InfoAddFriendResponse)

    async def create_group(self, request: full_pb2.CreateGroupRequest) -> full_pb2.CreateGroupResponse:
        """创建群聊。``POST /v1/group/create-group``"""
        return await self._call("/v1/group/create-group", request, full_pb2.CreateGroupResponse)

    async def dismiss_group(self, request: full_pb2.DismissGroupRequest) -> full_pb2.StatusResponse:
        """解散群聊。``POST /v1/group/dismiss-group``"""
        return await self._call("/v1/group/dismiss-group", request, full_pb2.StatusResponse)


class GroupTagProtoAPI(ProtoGroupAPI):
    """``v1/group-tag`` 的 protobuf 端点（1 个）。"""

    async def members(self, request: full_pb2.TagMemberRequest) -> full_pb2.ListMemberResponse:
        """获取标签绑定的用户列表。``POST /v1/group-tag/members``"""
        return await self._call("/v1/group-tag/members", request, full_pb2.ListMemberResponse)


class InstructionProtoAPI(ProtoGroupAPI):
    """``v1/instruction`` 的 protobuf 端点（1 个）。"""

    async def list_instructions(self, request: full_pb2.GetBotInstructionRequest) -> full_pb2.GetBotInstructionResponse:
        """获取机器人私聊指令。``POST /v1/instruction/list``"""
        return await self._call("/v1/instruction/list", request, full_pb2.GetBotInstructionResponse)
