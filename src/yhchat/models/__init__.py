"""云湖 SDK 的数据模型与消息段。"""

from .base import ApiModel
from .bot import BatchSendResult, MessageInfo, MessagePage, ReceivedContent, ReceivedMessage, RecvType
from .segments import (
    BaseSegment,
    Button,
    FileSegment,
    HtmlSegment,
    ImageSegment,
    MarkdownSegment,
    TextSegment,
    VideoSegment,
)

__all__ = [
    "ApiModel",
    "BaseSegment",
    "BatchSendResult",
    "Button",
    "FileSegment",
    "HtmlSegment",
    "ImageSegment",
    "MarkdownSegment",
    "MessageInfo",
    "MessagePage",
    "ReceivedContent",
    "ReceivedMessage",
    "RecvType",
    "TextSegment",
    "VideoSegment",
]
