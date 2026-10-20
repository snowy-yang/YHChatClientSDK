from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ContentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONTENT_TYPE_UNSPECIFIED: _ClassVar[ContentType]
    CONTENT_TYPE_TEXT: _ClassVar[ContentType]
    CONTENT_TYPE_IMAGE: _ClassVar[ContentType]
    CONTENT_TYPE_VIDEO: _ClassVar[ContentType]
    CONTENT_TYPE_FILE: _ClassVar[ContentType]
    CONTENT_TYPE_MARKDOWN: _ClassVar[ContentType]
    CONTENT_TYPE_HTML: _ClassVar[ContentType]
CONTENT_TYPE_UNSPECIFIED: ContentType
CONTENT_TYPE_TEXT: ContentType
CONTENT_TYPE_IMAGE: ContentType
CONTENT_TYPE_VIDEO: ContentType
CONTENT_TYPE_FILE: ContentType
CONTENT_TYPE_MARKDOWN: ContentType
CONTENT_TYPE_HTML: ContentType

class Button(_message.Message):
    __slots__ = ("text", "action_type", "url", "value")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    text: str
    action_type: int
    url: str
    value: str
    def __init__(self, text: _Optional[str] = ..., action_type: _Optional[int] = ..., url: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class ButtonGroup(_message.Message):
    __slots__ = ("buttons",)
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    buttons: _containers.RepeatedCompositeFieldContainer[Button]
    def __init__(self, buttons: _Optional[_Iterable[_Union[Button, _Mapping]]] = ...) -> None: ...

class Content(_message.Message):
    __slots__ = ("type", "text", "at", "buttons", "image_key", "video_key", "file_key")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    AT_FIELD_NUMBER: _ClassVar[int]
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    IMAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    VIDEO_KEY_FIELD_NUMBER: _ClassVar[int]
    FILE_KEY_FIELD_NUMBER: _ClassVar[int]
    type: ContentType
    text: str
    at: str
    buttons: _containers.RepeatedCompositeFieldContainer[ButtonGroup]
    image_key: str
    video_key: str
    file_key: str
    def __init__(self, type: _Optional[_Union[ContentType, str]] = ..., text: _Optional[str] = ..., at: _Optional[str] = ..., buttons: _Optional[_Iterable[_Union[ButtonGroup, _Mapping]]] = ..., image_key: _Optional[str] = ..., video_key: _Optional[str] = ..., file_key: _Optional[str] = ...) -> None: ...

class MessageInfo(_message.Message):
    __slots__ = ("msg_id", "recv_id", "recv_type")
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    RECV_ID_FIELD_NUMBER: _ClassVar[int]
    RECV_TYPE_FIELD_NUMBER: _ClassVar[int]
    msg_id: str
    recv_id: str
    recv_type: str
    def __init__(self, msg_id: _Optional[str] = ..., recv_id: _Optional[str] = ..., recv_type: _Optional[str] = ...) -> None: ...

class SendRequest(_message.Message):
    __slots__ = ("recv_type", "recv_id", "content", "parent_id")
    RECV_TYPE_FIELD_NUMBER: _ClassVar[int]
    RECV_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    recv_type: str
    recv_id: str
    content: Content
    parent_id: str
    def __init__(self, recv_type: _Optional[str] = ..., recv_id: _Optional[str] = ..., content: _Optional[_Union[Content, _Mapping]] = ..., parent_id: _Optional[str] = ...) -> None: ...

class SendReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: MessageInfo
    def __init__(self, message: _Optional[_Union[MessageInfo, _Mapping]] = ...) -> None: ...

class BatchSendRequest(_message.Message):
    __slots__ = ("recv_ids", "recv_type", "content", "parent_id")
    RECV_IDS_FIELD_NUMBER: _ClassVar[int]
    RECV_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    recv_ids: _containers.RepeatedScalarFieldContainer[str]
    recv_type: str
    content: Content
    parent_id: str
    def __init__(self, recv_ids: _Optional[_Iterable[str]] = ..., recv_type: _Optional[str] = ..., content: _Optional[_Union[Content, _Mapping]] = ..., parent_id: _Optional[str] = ...) -> None: ...

class BatchSendReply(_message.Message):
    __slots__ = ("success_count", "success_list")
    SUCCESS_COUNT_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_LIST_FIELD_NUMBER: _ClassVar[int]
    success_count: int
    success_list: _containers.RepeatedCompositeFieldContainer[MessageInfo]
    def __init__(self, success_count: _Optional[int] = ..., success_list: _Optional[_Iterable[_Union[MessageInfo, _Mapping]]] = ...) -> None: ...

class SendStreamRequest(_message.Message):
    __slots__ = ("recv_type", "recv_id", "content_type", "chunk")
    RECV_TYPE_FIELD_NUMBER: _ClassVar[int]
    RECV_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    recv_type: str
    recv_id: str
    content_type: str
    chunk: bytes
    def __init__(self, recv_type: _Optional[str] = ..., recv_id: _Optional[str] = ..., content_type: _Optional[str] = ..., chunk: _Optional[bytes] = ...) -> None: ...

class EditRequest(_message.Message):
    __slots__ = ("msg_id", "content", "recv_id", "recv_type")
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    RECV_ID_FIELD_NUMBER: _ClassVar[int]
    RECV_TYPE_FIELD_NUMBER: _ClassVar[int]
    msg_id: str
    content: Content
    recv_id: str
    recv_type: str
    def __init__(self, msg_id: _Optional[str] = ..., content: _Optional[_Union[Content, _Mapping]] = ..., recv_id: _Optional[str] = ..., recv_type: _Optional[str] = ...) -> None: ...

class EditReply(_message.Message):
    __slots__ = ("success_count",)
    SUCCESS_COUNT_FIELD_NUMBER: _ClassVar[int]
    success_count: int
    def __init__(self, success_count: _Optional[int] = ...) -> None: ...

class RecallRequest(_message.Message):
    __slots__ = ("msg_id", "chat_id", "chat_type")
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    msg_id: str
    chat_id: str
    chat_type: str
    def __init__(self, msg_id: _Optional[str] = ..., chat_id: _Optional[str] = ..., chat_type: _Optional[str] = ...) -> None: ...

class RecallReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListMessagesRequest(_message.Message):
    __slots__ = ("chat_id", "chat_type", "message_id", "before", "after")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    chat_type: str
    message_id: str
    before: int
    after: int
    def __init__(self, chat_id: _Optional[str] = ..., chat_type: _Optional[str] = ..., message_id: _Optional[str] = ..., before: _Optional[int] = ..., after: _Optional[int] = ...) -> None: ...

class ReceivedMessage(_message.Message):
    __slots__ = ("msg_id", "parent_id", "sender_id", "sender_type", "sender_nickname", "content_type", "text", "at", "buttons", "send_time")
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    SENDER_NICKNAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    AT_FIELD_NUMBER: _ClassVar[int]
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    SEND_TIME_FIELD_NUMBER: _ClassVar[int]
    msg_id: str
    parent_id: str
    sender_id: str
    sender_type: str
    sender_nickname: str
    content_type: str
    text: str
    at: _containers.RepeatedScalarFieldContainer[str]
    buttons: _containers.RepeatedCompositeFieldContainer[ButtonGroup]
    send_time: int
    def __init__(self, msg_id: _Optional[str] = ..., parent_id: _Optional[str] = ..., sender_id: _Optional[str] = ..., sender_type: _Optional[str] = ..., sender_nickname: _Optional[str] = ..., content_type: _Optional[str] = ..., text: _Optional[str] = ..., at: _Optional[_Iterable[str]] = ..., buttons: _Optional[_Iterable[_Union[ButtonGroup, _Mapping]]] = ..., send_time: _Optional[int] = ...) -> None: ...

class ListMessagesReply(_message.Message):
    __slots__ = ("messages", "total")
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[ReceivedMessage]
    total: int
    def __init__(self, messages: _Optional[_Iterable[_Union[ReceivedMessage, _Mapping]]] = ..., total: _Optional[int] = ...) -> None: ...

class UploadRequest(_message.Message):
    __slots__ = ("kind", "filename", "mime_type", "data")
    class Kind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        KIND_UNSPECIFIED: _ClassVar[UploadRequest.Kind]
        KIND_IMAGE: _ClassVar[UploadRequest.Kind]
        KIND_VIDEO: _ClassVar[UploadRequest.Kind]
        KIND_FILE: _ClassVar[UploadRequest.Kind]
    KIND_UNSPECIFIED: UploadRequest.Kind
    KIND_IMAGE: UploadRequest.Kind
    KIND_VIDEO: UploadRequest.Kind
    KIND_FILE: UploadRequest.Kind
    KIND_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    kind: UploadRequest.Kind
    filename: str
    mime_type: str
    data: bytes
    def __init__(self, kind: _Optional[_Union[UploadRequest.Kind, str]] = ..., filename: _Optional[str] = ..., mime_type: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class UploadReply(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: str
    def __init__(self, key: _Optional[str] = ...) -> None: ...
