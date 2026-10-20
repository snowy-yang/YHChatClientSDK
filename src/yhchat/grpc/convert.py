"""proto 与核心 SDK 模型之间的转换。"""

from collections.abc import Sequence

from ..errors import TransportError
from ..models import (
    BaseSegment,
    Button,
    FileSegment,
    HtmlSegment,
    ImageSegment,
    MarkdownSegment,
    MessageInfo,
    ReceivedMessage,
    TextSegment,
    VideoSegment,
)
from ._pb import yhchat_pb2

_UNSUPPORTED = "不支持的消息类型"


def content_from_segment(segment: BaseSegment) -> yhchat_pb2.Content:
    """把发送用消息段转成 proto ``Content``。"""
    if isinstance(segment, TextSegment):
        content = yhchat_pb2.Content(type=yhchat_pb2.CONTENT_TYPE_TEXT, text=segment.text)
        if segment.at:
            content.at = ",".join(segment.at)
        content.buttons.extend(_button_groups_to_proto(segment.buttons))
        return content
    if isinstance(segment, MarkdownSegment):
        return yhchat_pb2.Content(type=yhchat_pb2.CONTENT_TYPE_MARKDOWN, text=segment.text)
    if isinstance(segment, HtmlSegment):
        return yhchat_pb2.Content(type=yhchat_pb2.CONTENT_TYPE_HTML, text=segment.text)
    if isinstance(segment, ImageSegment):
        return yhchat_pb2.Content(type=yhchat_pb2.CONTENT_TYPE_IMAGE, image_key=segment.key)
    if isinstance(segment, VideoSegment):
        return yhchat_pb2.Content(type=yhchat_pb2.CONTENT_TYPE_VIDEO, video_key=segment.key)
    if isinstance(segment, FileSegment):
        return yhchat_pb2.Content(type=yhchat_pb2.CONTENT_TYPE_FILE, file_key=segment.key)
    raise TransportError(f"{_UNSUPPORTED}: {type(segment).__name__}")


def segment_from_content(content: yhchat_pb2.Content) -> BaseSegment:
    """把 proto ``Content`` 转成发送用消息段。"""
    match content.type:
        case yhchat_pb2.CONTENT_TYPE_TEXT:
            return TextSegment(
                text=content.text,
                at=content.at.split(",") if content.at else None,
                buttons=_button_groups_from_proto(content.buttons) or None,
            )
        case yhchat_pb2.CONTENT_TYPE_MARKDOWN:
            return MarkdownSegment(text=content.text)
        case yhchat_pb2.CONTENT_TYPE_HTML:
            return HtmlSegment(text=content.text)
        case yhchat_pb2.CONTENT_TYPE_IMAGE:
            return ImageSegment(key=content.image_key)
        case yhchat_pb2.CONTENT_TYPE_VIDEO:
            return VideoSegment(key=content.video_key)
        case yhchat_pb2.CONTENT_TYPE_FILE:
            return FileSegment(key=content.file_key)
        case _:
            raise TransportError(f"未知的 ContentType: {content.type}")


def message_info_to_proto(info: MessageInfo) -> yhchat_pb2.MessageInfo:
    """``MessageInfo`` → proto。"""
    return yhchat_pb2.MessageInfo(msg_id=info.msg_id, recv_id=info.recv_id, recv_type=info.recv_type)


def received_message_to_proto(message: ReceivedMessage) -> yhchat_pb2.ReceivedMessage:
    """``ReceivedMessage`` → proto。"""
    result = yhchat_pb2.ReceivedMessage(
        msg_id=message.msg_id,
        sender_id=message.sender_id,
        sender_type=message.sender_type,
        content_type=message.content_type,
    )
    if message.parent_id:
        result.parent_id = message.parent_id
    if message.sender_nickname:
        result.sender_nickname = message.sender_nickname
    if message.content.text is not None:
        result.text = message.content.text
    result.at.extend(message.content.at or [])
    if message.content.buttons:
        result.buttons.extend(_button_groups_to_proto(message.content.buttons))
    if message.send_time is not None:
        result.send_time = message.send_time
    return result


def _button_groups_to_proto(groups: Sequence[Sequence[Button]] | None) -> list[yhchat_pb2.ButtonGroup]:
    if not groups:
        return []
    return [yhchat_pb2.ButtonGroup(buttons=[_button_to_proto(button) for button in group]) for group in groups]


def _button_to_proto(button: Button) -> yhchat_pb2.Button:
    result = yhchat_pb2.Button(text=button.text, action_type=button.action_type)
    if button.url:
        result.url = button.url
    if button.value:
        result.value = button.value
    return result


def _button_groups_from_proto(groups: Sequence[yhchat_pb2.ButtonGroup]) -> list[list[Button]]:
    return [
        [
            Button.model_validate(
                {
                    "text": button.text,
                    "actionType": button.action_type,
                    "url": button.url or None,
                    "value": button.value or None,
                }
            )
            for button in group.buttons
        ]
        for group in groups
    ]
