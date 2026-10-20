"""Satori v1 聊天子集的模型、元素与后端适配。

- :mod:`yhchat.satori.server` 依赖 ``server`` extra（starlette）；
- 其余模块只依赖核心 SDK 与 pydantic。
"""

from .backend import (
    ChannelRegistry,
    SatoriBackend,
    SatoriNotFoundError,
    SatoriUnsupportedError,
    YHChatBackend,
    render_message_content,
    segment_from_content,
)
from .bus import EventBus
from .elements import parse, serialize
from .models import Channel, Event, Friend, Guild, Login, Member, MessageObject, Page, User

__all__ = [
    "Channel",
    "ChannelRegistry",
    "Event",
    "EventBus",
    "Friend",
    "Guild",
    "Login",
    "Member",
    "MessageObject",
    "Page",
    "SatoriBackend",
    "SatoriNotFoundError",
    "SatoriUnsupportedError",
    "User",
    "YHChatBackend",
    "parse",
    "render_message_content",
    "segment_from_content",
    "serialize",
]
