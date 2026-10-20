"""云湖后端适配：content ↔ 消息段、云湖消息 → Satori 模型。"""

import json
from collections.abc import AsyncIterator
from typing import Any, cast

import httpx
import pytest
import respx

from yhchat import YHChatClient
from yhchat.models import FileSegment, ImageSegment, ReceivedMessage, TextSegment
from yhchat.proto._pb import full_pb2
from yhchat.satori.backend import (
    SatoriNotFoundError,
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


def protobuf(message: Any) -> httpx.Response:
    return httpx.Response(200, content=message.SerializeToString())


@pytest.fixture
async def backend() -> AsyncIterator[YHChatBackend]:
    async with YHChatClient("test-token", user_token="user-token", http2=False, trust_env=False) as client:
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


async def test_guild_list_uses_join_group_list(backend: YHChatBackend) -> None:
    payload = full_pb2.JoinGroupListResponse(
        status=full_pb2.Status(code=1),
        group=[
            full_pb2.JoinGroupListResponse.Group(id="g1", name="群一", avatar_url="https://a/1.png"),
            full_pb2.JoinGroupListResponse.Group(id="g2", name="群二"),
        ],
    )
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/v1/bot/join-group-list").mock(return_value=protobuf(payload))

        page = await backend.guild_list("3")

        request = full_pb2.JoinGroupListRequest.FromString(route.calls.last.request.content)
        assert request.bot_id == "bot-1"
        assert request.data.page == 3
        assert route.calls.last.request.headers["token"] == "user-token"
        assert [(guild.id, guild.name) for guild in page.data] == [("g1", "群一"), ("g2", "群二")]
        assert page.next is None


async def test_guild_get_uses_group_info(backend: YHChatBackend) -> None:
    payload = full_pb2.GroupInfoResponse(
        status=full_pb2.Status(code=1),
        data=full_pb2.GroupData(group_id="g1", name="测试群", avatar_url="https://a/g.png"),
    )
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/group/info").mock(return_value=protobuf(payload))

        guild = await backend.guild_get("g1")

        assert guild.name == "测试群"
        assert guild.avatar == "https://a/g.png"


async def test_guild_member_list_and_get(backend: YHChatBackend) -> None:
    payload = full_pb2.ListMemberResponse(
        status=full_pb2.Status(code=1),
        total=1,
        user=[
            full_pb2.ListMemberResponse.User(
                group_id="g1",
                permission_level=2,
                user_info=full_pb2.ListMemberResponse.User.UserInfo(user_id="u1", name="小明"),
            )
        ],
    )
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/v1/group/list-member").mock(return_value=protobuf(payload))

        page = await backend.guild_member_list("g1", None)
        member = await backend.guild_member_get("g1", "u1")

        request = full_pb2.ListMemberRequest.FromString(route.calls.last.request.content)
        assert request.data.page == 1
        assert page.data[0].user is not None and page.data[0].user.name == "小明"
        assert page.data[0].roles[0].id == "2"
        assert member.user is not None and member.user.id == "u1"


async def test_guild_member_get_missing(backend: YHChatBackend) -> None:
    payload = full_pb2.ListMemberResponse(status=full_pb2.Status(code=1), user=[])
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/group/list-member").mock(return_value=protobuf(payload))

        with pytest.raises(SatoriNotFoundError):
            await backend.guild_member_get("g1", "nobody")


async def test_user_get_parses_remark_and_maps_banned(backend: YHChatBackend) -> None:
    found = full_pb2.GetUserResponse(
        status=full_pb2.Status(code=1),
        data=full_pb2.GetUserResponse.Data(
            id="u1", name="小明", avatar_url="https://a/u.png", remark_info=full_pb2.RemarkInfo(remark_name="备注")
        ),
    )
    banned = full_pb2.GetUserResponse(status=full_pb2.Status(code=4402, msg="该用户不存在"))
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/user/get-user").mock(return_value=protobuf(found))
        user = await backend.user_get("u1")

        mock.post("/v1/user/get-user").mock(return_value=protobuf(banned))
        with pytest.raises(SatoriNotFoundError):
            await backend.user_get("u2")

    assert user.name == "小明"
    assert user.nick == "备注"


async def test_friend_list_only_users(backend: YHChatBackend) -> None:
    payload = full_pb2.AddressBookListResponse(
        status=full_pb2.Status(code=1),
        md5="next-md5",
        data=[
            full_pb2.AddressBookListResponse.Data(
                list_name="好友",
                chat_type=full_pb2.ChatType.user,
                data=[
                    full_pb2.AddressBookListResponse.Data.DataList(
                        chat_id="u1", name="小明", remark="备注", avatar_url="https://a/u.png"
                    )
                ],
            ),
            full_pb2.AddressBookListResponse.Data(
                list_name="群聊",
                chat_type=full_pb2.ChatType.group,
                data=[full_pb2.AddressBookListResponse.Data.DataList(chat_id="g1", name="群一")],
            ),
        ],
    )
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/v1/friend/address-book-list").mock(return_value=protobuf(payload))

        page = await backend.friend_list(None)

        request = full_pb2.AddressBookListRequest.FromString(route.calls.last.request.content)
        assert request.md5 == ""
        assert len(page.data) == 1
        assert page.data[0].user is not None and page.data[0].user.id == "u1"
        assert page.data[0].nick == "备注"
        assert page.next == "next-md5"


async def test_channel_list_without_guild_uses_conversations(backend: YHChatBackend) -> None:
    payload = full_pb2.ConversationListResponse(
        status=full_pb2.Status(code=1),
        data=[
            full_pb2.ConversationListResponse.Data(
                chat_id="g1", chat_type=full_pb2.ChatType.group, name="群一", remark="群备注"
            ),
            full_pb2.ConversationListResponse.Data(chat_id="u1", chat_type=full_pb2.ChatType.user, name="小明"),
        ],
    )
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/conversation/list").mock(return_value=protobuf(payload))

        page = await backend.channel_list(None)

        assert [(channel.id, channel.type) for channel in page.data] == [("g1", 0), ("u1", 1)]
        assert page.data[0].name == "群一"


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
