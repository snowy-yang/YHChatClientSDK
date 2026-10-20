"""云湖（YHChat）非官方 Python SDK。"""

from .client import YHChatClient
from .errors import APIError, TransportError, YHChatError
from .models import (
    ApiModel,
    BaseSegment,
    BatchSendResult,
    Button,
    FileSegment,
    HtmlSegment,
    ImageSegment,
    MarkdownSegment,
    MessageInfo,
    MessagePage,
    ReceivedContent,
    ReceivedMessage,
    TextSegment,
    VideoSegment,
)
from .records import MessageRegistry

__version__ = "0.1.0"

__all__ = [
    "APIError",
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
    "MessageRegistry",
    "ReceivedContent",
    "ReceivedMessage",
    "TextSegment",
    "TransportError",
    "VideoSegment",
    "YHChatClient",
    "YHChatError",
    "__version__",
]
