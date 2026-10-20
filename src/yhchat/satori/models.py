"""Satori v1 的数据模型（聊天子集）。

字段与 satori-protocol 一致：全部 snake_case，未知字段保留在 ``__pydantic_extra__``。
"""

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class SatoriModel(BaseModel):
    """Satori 模型基类：宽松解析，未知字段保留。"""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class Channel(SatoriModel):
    """频道：云湖里对应一个会话（群聊或私聊）。"""

    id: str
    type: int = 0  # 0=TEXT 1=DIRECT 2=CATEGORY 3=VOICE
    name: str | None = None
    parent_id: str | None = None


class Guild(SatoriModel):
    """群组：云湖里对应一个群。"""

    id: str
    name: str | None = None
    avatar: str | None = None


class User(SatoriModel):
    """用户。"""

    id: str
    name: str | None = None
    nick: str | None = None
    avatar: str | None = None
    is_bot: bool | None = None


class Role(SatoriModel):
    """角色。"""

    id: str
    name: str | None = None


class Member(SatoriModel):
    """群成员。"""

    user: User | None = None
    nick: str | None = None
    avatar: str | None = None
    joined_at: int | None = None
    roles: list[Role] = Field(default_factory=list[Role])


class Friend(SatoriModel):
    """好友。"""

    user: User | None = None
    nick: str | None = None


class MessageObject(SatoriModel):
    """消息。``content`` 是元素标记文本。"""

    id: str
    content: str = ""
    channel: Channel | None = None
    guild: Guild | None = None
    member: Member | None = None
    user: User | None = None
    created_at: int | None = None  # 毫秒时间戳
    updated_at: int | None = None
    referrer: dict[str, object] | None = None


class Login(SatoriModel):
    """机器人账号。"""

    sn: int = 0
    status: int = 1  # 1=ONLINE
    adapter: str = "satori"
    platform: str
    user: User
    features: list[str] = Field(default_factory=list[str])


class Event(SatoriModel):
    """事件推送体（WS ``op: 0`` 的 body）。"""

    sn: int = 0
    type: str
    timestamp: int
    login: Login
    channel: Channel | None = None
    guild: Guild | None = None
    member: Member | None = None
    message: MessageObject | None = None
    operator: User | None = None
    user: User | None = None
    referrer: dict[str, object] | None = None


class Page[T](SatoriModel):
    """分页结果：``{data, next}``。"""

    data: list[T]
    next: str | None = None


def now_millis() -> int:
    """当前毫秒时间戳。"""
    return int(datetime.now(tz=UTC).timestamp() * 1000)
