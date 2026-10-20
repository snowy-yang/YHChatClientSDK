"""Satori 后端协议与云湖实现。

``SatoriChatServer`` 只依赖 :class:`SatoriBackend` 协议，不直接依赖 ``YHChatClient``，
这样协议层与 SDK/HTTP 层解耦；云湖的字段假设集中在 :class:`YHChatBackend`。
"""

from typing import Protocol, runtime_checkable

from ..client import YHChatClient
from ..errors import APIError
from ..models import BaseSegment, FileSegment, ImageSegment, ReceivedMessage, TextSegment, VideoSegment
from ..proto._pb import full_pb2
from .elements import At, Br, File, Image, Quote, SatoriElement, Text, Video, parse, serialize
from .models import Channel, Friend, Guild, Login, Member, MessageObject, Page, Role, User, now_millis

CHANNEL_TEXT = 0
CHANNEL_DIRECT = 1

_MEDIA_LIMITATION = "云湖不支持该消息类型"
_PAGE_SIZE = 50
"""分页大小：Satori 的 next_token 不透明，这里直接放页码，配合云湖的 page/size。"""
_USER_BANNED_CODES = {4402, 7100}
"""``user/get-user`` 的分页错误码：用户不存在 / 被封禁。"""


class SatoriUnsupportedError(NotImplementedError):
    """协议里存在、但当前实现尚未支撑的动作（映射成 HTTP 404）。"""


class SatoriNotFoundError(LookupError):
    """资源不存在（映射成 HTTP 404）。"""


@runtime_checkable
class SatoriBackend(Protocol):
    """Satori 聊天子集的后端契约。"""

    async def login(self) -> Login:
        """当前机器人账号。"""
        ...

    async def message_create(
        self, channel_id: str, content: str, referrer: dict[str, object] | None
    ) -> list[MessageObject]:
        """发送消息。"""
        ...

    async def message_get(self, channel_id: str, message_id: str) -> MessageObject:
        """取单条消息。"""
        ...

    async def message_list(
        self,
        channel_id: str,
        next_token: str | None,
        direction: str,
        limit: int,
        order: str,
    ) -> Page[MessageObject]:
        """拉取频道消息。"""
        ...

    async def message_update(self, channel_id: str, message_id: str, content: str) -> None:
        """编辑消息。"""
        ...

    async def message_delete(self, channel_id: str, message_id: str) -> None:
        """撤回消息。"""
        ...

    async def channel_get(self, channel_id: str) -> Channel:
        """取频道。"""
        ...

    async def channel_list(self, guild_id: str | None) -> Page[Channel]:
        """取频道列表。"""
        ...

    async def guild_get(self, guild_id: str) -> Guild:
        """取群组。"""
        ...

    async def guild_list(self, next_token: str | None) -> Page[Guild]:
        """取群组列表。"""
        ...

    async def guild_member_get(self, guild_id: str, user_id: str) -> Member:
        """取群成员。"""
        ...

    async def guild_member_list(self, guild_id: str, next_token: str | None) -> Page[Member]:
        """取群成员列表。"""
        ...

    async def user_get(self, user_id: str) -> User:
        """取用户。"""
        ...

    async def friend_list(self, next_token: str | None) -> Page[Friend]:
        """取好友列表。"""
        ...


class ChannelRegistry:
    """记录「频道 → 会话类型」的映射。

    云湖发送接口必须带 ``recvType``，而 Satori 只给 ``channel_id``；
    所以入站事件里学到的类型要记下来，未知时退回 ``default_recv_type``。
    """

    def __init__(self, default_recv_type: str = "group") -> None:
        self.default_recv_type = default_recv_type
        self._recv_types: dict[str, str] = {}

    def remember(self, channel_id: str, recv_type: str) -> None:
        """记住某个频道的会话类型。"""
        self._recv_types[channel_id] = recv_type

    def recv_type(self, channel_id: str) -> str:
        """取会话类型。"""
        return self._recv_types.get(channel_id, self.default_recv_type)

    def channel_type(self, channel_id: str) -> int:
        """映射成 Satori 的 ``Channel.type``。"""
        return CHANNEL_TEXT if self.recv_type(channel_id) == "group" else CHANNEL_DIRECT


class YHChatBackend:
    """用 ``YHChatClient`` 实现 Satori 聊天子集。

    已支撑：``message.*`` / ``login.get`` / ``channel.*`` / ``guild.*`` /
    ``guild.member.*`` / ``user.get`` / ``friend.list``。云湖没有跨群频道列表，
    ``channel.list()`` 用最近会话列表代替；群列表来自「机器人加入的群」。
    """

    def __init__(
        self,
        client: YHChatClient,
        *,
        self_id: str,
        platform: str = "yhchat",
        registry: ChannelRegistry | None = None,
    ) -> None:
        self._client = client
        self._self_id = self_id
        self._platform = platform
        self.registry = registry or ChannelRegistry()

    async def login(self) -> Login:
        """当前机器人账号。"""
        return Login(platform=self._platform, user=User(id=self._self_id), adapter="satori")

    async def message_create(
        self, channel_id: str, content: str, referrer: dict[str, object] | None
    ) -> list[MessageObject]:
        """把 Satori content 转成云湖消息段后发送。"""
        segment = segment_from_content(content)
        info = await self._client.bot.message.send(
            self.registry.recv_type(channel_id),
            channel_id,
            segment,
            parent_id=_quote_of(content),
        )
        return [
            MessageObject(
                id=info.msg_id,
                content=content,
                channel=self._channel(channel_id),
                guild=self._guild(channel_id),
                created_at=now_millis(),
                referrer=referrer,
            )
        ]

    async def message_get(self, channel_id: str, message_id: str) -> MessageObject:
        """按 ID 取消息（云湖只能列出后筛选）。"""
        page = await self._client.bot.message.list(
            channel_id, self.registry.recv_type(channel_id), message_id=message_id
        )
        for message in page.messages:
            if message.msg_id == message_id:
                return self._message_object(channel_id, message)
        raise SatoriNotFoundError(f"消息不存在: {message_id}")

    async def message_list(
        self,
        channel_id: str,
        next_token: str | None,
        direction: str,
        limit: int,
        order: str,
    ) -> Page[MessageObject]:
        """拉取消息；云湖用 ``before``/``after`` 计数 + ``message-id`` 游标。"""
        before = limit if direction != "after" else 0
        after = limit if direction == "after" else 0
        page = await self._client.bot.message.list(
            channel_id,
            self.registry.recv_type(channel_id),
            message_id=next_token,
            before=before,
            after=after,
        )
        messages = [self._message_object(channel_id, message) for message in page.messages]
        if order == "desc":
            messages.reverse()
        next_token_out = page.messages[-1].msg_id if len(page.messages) >= limit > 0 else None
        return Page(data=messages, next=next_token_out)

    async def message_update(self, channel_id: str, message_id: str, content: str) -> None:
        """编辑消息。"""
        await self._client.bot.message.edit(
            message_id,
            segment_from_content(content),
            recv_id=channel_id,
            recv_type=self.registry.recv_type(channel_id),
        )

    async def message_delete(self, channel_id: str, message_id: str) -> None:
        """撤回消息。"""
        await self._client.bot.message.recall(
            message_id, chat_id=channel_id, chat_type=self.registry.recv_type(channel_id)
        )

    async def channel_get(self, channel_id: str) -> Channel:
        """取频道（云湖会话即频道，名称未知时用 ID 顶替）。"""
        return self._channel(channel_id)

    async def channel_list(self, guild_id: str | None) -> Page[Channel]:
        """群内只有「群」这一层频道；不带 ``guild_id`` 时用最近会话列表兜底。

        云湖没有「跨群频道列表」端点，Satori 的这个语义只能近似：会话列表里的每个
        聊天映射成一个频道，群聊是 TEXT，私聊/机器人是 DIRECT。
        """
        if guild_id is not None:
            return Page(data=[Channel(id=guild_id, type=CHANNEL_TEXT, name=guild_id)])
        response = await self._client.v1.proto.conversation.list_conversations(full_pb2.ConversationListRequest())
        channels = [
            Channel(
                id=item.chat_id,
                type=_channel_type(item.chat_type),
                name=item.name or item.remark or item.chat_id,
            )
            for item in response.data
        ]
        return Page(data=channels)

    async def guild_get(self, guild_id: str) -> Guild:
        """取群组（云湖群聊即 guild）。"""
        response = await self._client.v1.proto.group.info(full_pb2.GroupInfoRequest(group_id=guild_id))
        group = response.data
        if not group.group_id:
            raise SatoriNotFoundError(f"群不存在: {guild_id}")
        return Guild(id=group.group_id, name=group.name or group.group_id, avatar=group.avatar_url or None)

    async def guild_list(self, next_token: str | None) -> Page[Guild]:
        """机器人加入的群聊列表；``next_token`` 是页码。"""
        page = int(next_token) if next_token else 1
        response = await self._client.v1.proto.bot.join_group_list(
            full_pb2.JoinGroupListRequest(
                bot_id=self._self_id,
                data=full_pb2.JoinGroupListRequest.Data(size=_PAGE_SIZE, page=page),
            )
        )
        guilds = [
            Guild(id=group.id, name=group.name or group.id, avatar=group.avatar_url or None) for group in response.group
        ]
        return Page(data=guilds, next=str(page + 1) if len(guilds) >= _PAGE_SIZE else None)

    async def guild_member_get(self, guild_id: str, user_id: str) -> Member:
        """按用户 ID 在群成员里查（云湖没有单个成员端点，用 keywords 过滤）。"""
        response = await self._client.v1.proto.group.list_member(
            full_pb2.ListMemberRequest(
                group_id=guild_id,
                keywords=user_id,
                data=full_pb2.ListMemberRequest.Data(size=_PAGE_SIZE, page=1),
            )
        )
        for item in response.user:
            if item.user_info.user_id == user_id:
                return _member_of(item)
        raise SatoriNotFoundError(f"群 {guild_id} 里没有成员 {user_id}")

    async def guild_member_list(self, guild_id: str, next_token: str | None) -> Page[Member]:
        """群成员列表；``next_token`` 是页码。"""
        page = int(next_token) if next_token else 1
        response = await self._client.v1.proto.group.list_member(
            full_pb2.ListMemberRequest(
                group_id=guild_id,
                data=full_pb2.ListMemberRequest.Data(size=_PAGE_SIZE, page=page),
            )
        )
        members = [_member_of(item) for item in response.user]
        return Page(data=members, next=str(page + 1) if len(members) >= _PAGE_SIZE else None)

    async def user_get(self, user_id: str) -> User:
        """用户资料；用户不存在/被封禁时转成 :class:`SatoriNotFoundError`。"""
        try:
            response = await self._client.v1.proto.user.get_user(full_pb2.GetUserRequest(id=user_id))
        except APIError as exc:
            if exc.code in _USER_BANNED_CODES:
                raise SatoriNotFoundError(f"用户不可用: {user_id}") from exc
            raise
        user = response.data
        return User(
            id=user.id or user_id,
            name=user.name or None,
            nick=user.remark_info.remark_name or None,
            avatar=user.avatar_url or None,
        )

    async def friend_list(self, next_token: str | None) -> Page[Friend]:
        """好友列表（通讯录里 ``chat_type == user`` 的分组）；``next_token`` 是 ``md5``。"""
        response = await self._client.v1.proto.friend.address_book_list(
            full_pb2.AddressBookListRequest(md5=next_token or "")
        )
        friends = [
            Friend(
                user=User(id=entry.chat_id, name=entry.name or None, avatar=entry.avatar_url or None),
                nick=entry.remark or None,
            )
            for group in response.data
            if group.chat_type == full_pb2.ChatType.user
            for entry in group.data
        ]
        return Page(data=friends, next=response.md5 or None)

    def _channel(self, channel_id: str) -> Channel:
        return Channel(id=channel_id, type=self.registry.channel_type(channel_id), name=channel_id)

    def _guild(self, channel_id: str) -> Guild | None:
        return Guild(id=channel_id, name=channel_id) if self.registry.channel_type(channel_id) == CHANNEL_TEXT else None

    def _message_object(self, channel_id: str, message: ReceivedMessage) -> MessageObject:
        channel = self._channel(channel_id)
        user = User(id=message.sender_id, name=message.sender_nickname)
        return MessageObject(
            id=message.msg_id,
            content=render_message_content(message),
            channel=channel,
            guild=self._guild(channel_id),
            member=Member(user=user, nick=message.sender_nickname) if channel.type == CHANNEL_TEXT else None,
            user=user,
            created_at=message.send_time,
            updated_at=message.send_time,
        )


def segment_from_content(content: str) -> BaseSegment:
    """Satori content（元素标记）→ 云湖发送消息段。

    云湖一段消息只承载一种内容，所以：唯一媒体元素 → 媒体段；否则按文本处理，
    ``<at>`` 收集成 ``at`` 列表，``<quote>`` 变成引用（由调用方处理）。
    """
    elements = parse(content)
    meaningful = [element for element in elements if not isinstance(element, Br)]
    media = [element for element in meaningful if isinstance(element, (Image, File, Video))]
    if len(meaningful) == 1 and media:
        element = media[0]
        if isinstance(element, Image):
            return ImageSegment(key=element.src)
        if isinstance(element, File):
            return FileSegment(key=element.src)
        return VideoSegment(key=element.src)
    text = "".join(element.text for element in elements if isinstance(element, Text))
    at = [element.id for element in elements if isinstance(element, At) and element.id]
    return TextSegment(text=text, at=at or None)


def _quote_of(content: str) -> str | None:
    for element in parse(content):
        if isinstance(element, Quote) and element.id:
            return element.id
    return None


def render_message_content(message: ReceivedMessage) -> str:
    """云湖消息 → Satori content。

    图片/视频用云湖的 key 填 ``src``（不是真实 URL，客户端需要自行换取），文本原样输出。
    """
    elements: list[SatoriElement] = []
    if message.parent_id:
        elements.append(Quote(id=message.parent_id))
    elements.extend(At(id=user_id) for user_id in message.content.at or [])
    if message.content_type == "image":
        elements.append(Image(src=message.content.image_name or ""))
    elif message.content_type == "video":
        elements.append(Video(src=message.content.video_url or ""))
    else:
        elements.append(Text(message.content.text or ""))
    return serialize(elements)


def _channel_type(chat_type: int) -> int:
    """云湖会话类型 → Satori 频道类型。"""
    return CHANNEL_TEXT if chat_type == full_pb2.ChatType.group else CHANNEL_DIRECT


def _member_of(item: full_pb2.ListMemberResponse.User) -> Member:
    """群成员 → Satori ``Member``；云湖的权限级别塞进角色 ID，便于客户端区分。"""
    info = item.user_info
    user = User(id=info.user_id, name=info.name or None, avatar=info.avatar_url or None, is_bot=False)
    roles: list[Role] = []
    if item.permission_level:
        roles.append(Role(id=str(item.permission_level)))
    return Member(user=user, nick=info.name or None, joined_at=None, roles=roles)
