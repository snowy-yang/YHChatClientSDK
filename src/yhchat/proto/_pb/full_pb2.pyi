from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    unknown1: _ClassVar[ChatType]
    user: _ClassVar[ChatType]
    group: _ClassVar[ChatType]
    bot: _ClassVar[ChatType]

class ContentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    unknown2: _ClassVar[ContentType]
    text: _ClassVar[ContentType]
    image: _ClassVar[ContentType]
    markdown: _ClassVar[ContentType]
    file: _ClassVar[ContentType]
    form: _ClassVar[ContentType]
    sticker: _ClassVar[ContentType]
    html: _ClassVar[ContentType]
    tip: _ClassVar[ContentType]
    audio: _ClassVar[ContentType]
    call: _ClassVar[ContentType]
    a2ui: _ClassVar[ContentType]

class VipStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VIP_STATUS_NONE: _ClassVar[VipStatus]
    VIP_STATUS_ACTIVE: _ClassVar[VipStatus]
    VIP_STATUS_EXPIRED: _ClassVar[VipStatus]

class ContentTypeTextOnly(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TEXT_UNSPECIFIED: _ClassVar[ContentTypeTextOnly]
    TEXT_text: _ClassVar[ContentTypeTextOnly]
    TEXT_markdown: _ClassVar[ContentTypeTextOnly]
    TEXT_html: _ClassVar[ContentTypeTextOnly]
unknown1: ChatType
user: ChatType
group: ChatType
bot: ChatType
unknown2: ContentType
text: ContentType
image: ContentType
markdown: ContentType
file: ContentType
form: ContentType
sticker: ContentType
html: ContentType
tip: ContentType
audio: ContentType
call: ContentType
a2ui: ContentType
VIP_STATUS_NONE: VipStatus
VIP_STATUS_ACTIVE: VipStatus
VIP_STATUS_EXPIRED: VipStatus
TEXT_UNSPECIFIED: ContentTypeTextOnly
TEXT_text: ContentTypeTextOnly
TEXT_markdown: ContentTypeTextOnly
TEXT_html: ContentTypeTextOnly

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Status(_message.Message):
    __slots__ = ("request_id", "code", "msg")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    code: int
    msg: str
    def __init__(self, request_id: _Optional[int] = ..., code: _Optional[int] = ..., msg: _Optional[str] = ...) -> None: ...

class StatusResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: Status
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ...) -> None: ...

class Tag(_message.Message):
    __slots__ = ("id", "group_id", "text", "color")
    ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    id: int
    group_id: str
    text: str
    color: str
    def __init__(self, id: _Optional[int] = ..., group_id: _Optional[str] = ..., text: _Optional[str] = ..., color: _Optional[str] = ...) -> None: ...

class Sender(_message.Message):
    __slots__ = ("chat_id", "chat_type", "name", "avatar_url", "is_vip", "tag_old", "tag")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    IS_VIP_FIELD_NUMBER: _ClassVar[int]
    TAG_OLD_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    chat_type: ChatType
    name: str
    avatar_url: str
    is_vip: bool
    tag_old: _containers.RepeatedScalarFieldContainer[str]
    tag: _containers.RepeatedCompositeFieldContainer[Tag]
    def __init__(self, chat_id: _Optional[str] = ..., chat_type: _Optional[_Union[ChatType, str]] = ..., name: _Optional[str] = ..., avatar_url: _Optional[str] = ..., is_vip: _Optional[bool] = ..., tag_old: _Optional[_Iterable[str]] = ..., tag: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ...) -> None: ...

class Cmd(_message.Message):
    __slots__ = ("cmd_id", "name", "type")
    CMD_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    cmd_id: int
    name: str
    type: int
    def __init__(self, cmd_id: _Optional[int] = ..., name: _Optional[str] = ..., type: _Optional[int] = ...) -> None: ...

class MsgContent(_message.Message):
    __slots__ = ("text", "buttons", "image_url", "file_name", "file_url", "mentioned_id", "form", "quote_msg_text", "image", "post_id", "post_title", "post_content", "post_content_type", "expression_id", "quote_image_url", "quote_image_name", "file_size", "video_url", "video_time", "audio_url", "audio_time", "quote_video_url", "quote_video_time", "sticker_item_id", "sticker_pack_id", "room_name", "call_status_text", "width", "height", "tip")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_URL_FIELD_NUMBER: _ClassVar[int]
    MENTIONED_ID_FIELD_NUMBER: _ClassVar[int]
    FORM_FIELD_NUMBER: _ClassVar[int]
    QUOTE_MSG_TEXT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    POST_TITLE_FIELD_NUMBER: _ClassVar[int]
    POST_CONTENT_FIELD_NUMBER: _ClassVar[int]
    POST_CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_ID_FIELD_NUMBER: _ClassVar[int]
    QUOTE_IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    QUOTE_IMAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    VIDEO_URL_FIELD_NUMBER: _ClassVar[int]
    VIDEO_TIME_FIELD_NUMBER: _ClassVar[int]
    AUDIO_URL_FIELD_NUMBER: _ClassVar[int]
    AUDIO_TIME_FIELD_NUMBER: _ClassVar[int]
    QUOTE_VIDEO_URL_FIELD_NUMBER: _ClassVar[int]
    QUOTE_VIDEO_TIME_FIELD_NUMBER: _ClassVar[int]
    STICKER_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    STICKER_PACK_ID_FIELD_NUMBER: _ClassVar[int]
    ROOM_NAME_FIELD_NUMBER: _ClassVar[int]
    CALL_STATUS_TEXT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    TIP_FIELD_NUMBER: _ClassVar[int]
    text: str
    buttons: str
    image_url: str
    file_name: str
    file_url: str
    mentioned_id: _containers.RepeatedScalarFieldContainer[str]
    form: str
    quote_msg_text: str
    image: str
    post_id: str
    post_title: str
    post_content: str
    post_content_type: str
    expression_id: str
    quote_image_url: str
    quote_image_name: str
    file_size: int
    video_url: str
    video_time: int
    audio_url: str
    audio_time: int
    quote_video_url: str
    quote_video_time: int
    sticker_item_id: int
    sticker_pack_id: int
    room_name: str
    call_status_text: str
    width: int
    height: int
    tip: str
    def __init__(self, text: _Optional[str] = ..., buttons: _Optional[str] = ..., image_url: _Optional[str] = ..., file_name: _Optional[str] = ..., file_url: _Optional[str] = ..., mentioned_id: _Optional[_Iterable[str]] = ..., form: _Optional[str] = ..., quote_msg_text: _Optional[str] = ..., image: _Optional[str] = ..., post_id: _Optional[str] = ..., post_title: _Optional[str] = ..., post_content: _Optional[str] = ..., post_content_type: _Optional[str] = ..., expression_id: _Optional[str] = ..., quote_image_url: _Optional[str] = ..., quote_image_name: _Optional[str] = ..., file_size: _Optional[int] = ..., video_url: _Optional[str] = ..., video_time: _Optional[int] = ..., audio_url: _Optional[str] = ..., audio_time: _Optional[int] = ..., quote_video_url: _Optional[str] = ..., quote_video_time: _Optional[int] = ..., sticker_item_id: _Optional[int] = ..., sticker_pack_id: _Optional[int] = ..., room_name: _Optional[str] = ..., call_status_text: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., tip: _Optional[str] = ...) -> None: ...

class SendMsgRequest(_message.Message):
    __slots__ = ("msg_id", "chat_id", "chat_type", "content", "content_type", "command_id", "quote_msg_id")
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    QUOTE_MSG_ID_FIELD_NUMBER: _ClassVar[int]
    msg_id: str
    chat_id: str
    chat_type: ChatType
    content: MsgContent
    content_type: ContentType
    command_id: int
    quote_msg_id: str
    def __init__(self, msg_id: _Optional[str] = ..., chat_id: _Optional[str] = ..., chat_type: _Optional[_Union[ChatType, str]] = ..., content: _Optional[_Union[MsgContent, _Mapping]] = ..., content_type: _Optional[_Union[ContentType, str]] = ..., command_id: _Optional[int] = ..., quote_msg_id: _Optional[str] = ...) -> None: ...

class ListMsgRequest(_message.Message):
    __slots__ = ("msg_count", "msg_id", "chat_type", "chat_id")
    MSG_COUNT_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    msg_count: int
    msg_id: str
    chat_type: ChatType
    chat_id: str
    def __init__(self, msg_count: _Optional[int] = ..., msg_id: _Optional[str] = ..., chat_type: _Optional[_Union[ChatType, str]] = ..., chat_id: _Optional[str] = ...) -> None: ...

class ListMsgBySeqRequest(_message.Message):
    __slots__ = ("msg_start", "chat_type", "chat_id")
    MSG_START_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    msg_start: int
    chat_type: ChatType
    chat_id: str
    def __init__(self, msg_start: _Optional[int] = ..., chat_type: _Optional[_Union[ChatType, str]] = ..., chat_id: _Optional[str] = ...) -> None: ...

class ListMsgByMidSeqRequest(_message.Message):
    __slots__ = ("msg_seq", "chat_type", "chat_id", "unknown", "msg_count", "msg_id")
    MSG_SEQ_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    MSG_COUNT_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    msg_seq: int
    chat_type: ChatType
    chat_id: str
    unknown: int
    msg_count: int
    msg_id: str
    def __init__(self, msg_seq: _Optional[int] = ..., chat_type: _Optional[_Union[ChatType, str]] = ..., chat_id: _Optional[str] = ..., unknown: _Optional[int] = ..., msg_count: _Optional[int] = ..., msg_id: _Optional[str] = ...) -> None: ...

class PicListMsgByMidSeqRequest(_message.Message):
    __slots__ = ("image_id", "chat_type", "chat_id", "earlier_quantities", "latest_quantities")
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    EARLIER_QUANTITIES_FIELD_NUMBER: _ClassVar[int]
    LATEST_QUANTITIES_FIELD_NUMBER: _ClassVar[int]
    image_id: int
    chat_type: ChatType
    chat_id: str
    earlier_quantities: int
    latest_quantities: int
    def __init__(self, image_id: _Optional[int] = ..., chat_type: _Optional[_Union[ChatType, str]] = ..., chat_id: _Optional[str] = ..., earlier_quantities: _Optional[int] = ..., latest_quantities: _Optional[int] = ...) -> None: ...

class ButtonReportRequest(_message.Message):
    __slots__ = ("msg_id", "chat_type", "chat_id", "user_id", "button_value")
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    BUTTON_VALUE_FIELD_NUMBER: _ClassVar[int]
    msg_id: str
    chat_type: ChatType
    chat_id: str
    user_id: str
    button_value: str
    def __init__(self, msg_id: _Optional[str] = ..., chat_type: _Optional[_Union[ChatType, str]] = ..., chat_id: _Optional[str] = ..., user_id: _Optional[str] = ..., button_value: _Optional[str] = ...) -> None: ...

class RecallMsg(_message.Message):
    __slots__ = ("msg_id", "chat_id", "chat_type")
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    msg_id: _containers.RepeatedScalarFieldContainer[str]
    chat_id: str
    chat_type: ChatType
    def __init__(self, msg_id: _Optional[_Iterable[str]] = ..., chat_id: _Optional[str] = ..., chat_type: _Optional[_Union[ChatType, str]] = ...) -> None: ...

class MedalInfo(_message.Message):
    __slots__ = ("id", "name", "sort")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    sort: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., sort: _Optional[int] = ...) -> None: ...

class RemarkInfo(_message.Message):
    __slots__ = ("remark_name", "phone", "extra_remark")
    REMARK_NAME_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    EXTRA_REMARK_FIELD_NUMBER: _ClassVar[int]
    remark_name: str
    phone: str
    extra_remark: str
    def __init__(self, remark_name: _Optional[str] = ..., phone: _Optional[str] = ..., extra_remark: _Optional[str] = ...) -> None: ...

class ProfileInfo(_message.Message):
    __slots__ = ("last_active_time", "introduction", "gender", "birthday_timestamp", "city", "district", "address")
    LAST_ACTIVE_TIME_FIELD_NUMBER: _ClassVar[int]
    INTRODUCTION_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    BIRTHDAY_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    DISTRICT_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    last_active_time: str
    introduction: str
    gender: int
    birthday_timestamp: int
    city: str
    district: str
    address: str
    def __init__(self, last_active_time: _Optional[str] = ..., introduction: _Optional[str] = ..., gender: _Optional[int] = ..., birthday_timestamp: _Optional[int] = ..., city: _Optional[str] = ..., district: _Optional[str] = ..., address: _Optional[str] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("status", "data")
    class Data(_message.Message):
        __slots__ = ("id", "name", "name_id", "avatar_url", "avatar_id", "medal", "register_time", "do_not_disturb", "ban_id", "ban_until_timestamp", "online_day", "continuous_online_day", "is_vip", "vip_expired_timestamp", "vip_status", "is_blocked", "top", "remark_info", "profile_info", "ip_geo", "ban_reason")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        NAME_ID_FIELD_NUMBER: _ClassVar[int]
        AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
        AVATAR_ID_FIELD_NUMBER: _ClassVar[int]
        MEDAL_FIELD_NUMBER: _ClassVar[int]
        REGISTER_TIME_FIELD_NUMBER: _ClassVar[int]
        DO_NOT_DISTURB_FIELD_NUMBER: _ClassVar[int]
        BAN_ID_FIELD_NUMBER: _ClassVar[int]
        BAN_UNTIL_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        ONLINE_DAY_FIELD_NUMBER: _ClassVar[int]
        CONTINUOUS_ONLINE_DAY_FIELD_NUMBER: _ClassVar[int]
        IS_VIP_FIELD_NUMBER: _ClassVar[int]
        VIP_EXPIRED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        VIP_STATUS_FIELD_NUMBER: _ClassVar[int]
        IS_BLOCKED_FIELD_NUMBER: _ClassVar[int]
        TOP_FIELD_NUMBER: _ClassVar[int]
        REMARK_INFO_FIELD_NUMBER: _ClassVar[int]
        PROFILE_INFO_FIELD_NUMBER: _ClassVar[int]
        IP_GEO_FIELD_NUMBER: _ClassVar[int]
        BAN_REASON_FIELD_NUMBER: _ClassVar[int]
        id: str
        name: str
        name_id: int
        avatar_url: str
        avatar_id: int
        medal: _containers.RepeatedCompositeFieldContainer[MedalInfo]
        register_time: str
        do_not_disturb: bool
        ban_id: int
        ban_until_timestamp: int
        online_day: int
        continuous_online_day: int
        is_vip: bool
        vip_expired_timestamp: int
        vip_status: VipStatus
        is_blocked: bool
        top: bool
        remark_info: RemarkInfo
        profile_info: ProfileInfo
        ip_geo: str
        ban_reason: str
        def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., name_id: _Optional[int] = ..., avatar_url: _Optional[str] = ..., avatar_id: _Optional[int] = ..., medal: _Optional[_Iterable[_Union[MedalInfo, _Mapping]]] = ..., register_time: _Optional[str] = ..., do_not_disturb: _Optional[bool] = ..., ban_id: _Optional[int] = ..., ban_until_timestamp: _Optional[int] = ..., online_day: _Optional[int] = ..., continuous_online_day: _Optional[int] = ..., is_vip: _Optional[bool] = ..., vip_expired_timestamp: _Optional[int] = ..., vip_status: _Optional[_Union[VipStatus, str]] = ..., is_blocked: _Optional[bool] = ..., top: _Optional[bool] = ..., remark_info: _Optional[_Union[RemarkInfo, _Mapping]] = ..., profile_info: _Optional[_Union[ProfileInfo, _Mapping]] = ..., ip_geo: _Optional[str] = ..., ban_reason: _Optional[str] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    status: Status
    data: GetUserResponse.Data
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., data: _Optional[_Union[GetUserResponse.Data, _Mapping]] = ...) -> None: ...

class GetSelfMedal(_message.Message):
    __slots__ = ("status", "medal")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MEDAL_FIELD_NUMBER: _ClassVar[int]
    status: Status
    medal: _containers.RepeatedCompositeFieldContainer[MedalInfo]
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., medal: _Optional[_Iterable[_Union[MedalInfo, _Mapping]]] = ...) -> None: ...

class EditNicknameRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class EditAvatarRequest(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class ListMsgResponse(_message.Message):
    __slots__ = ("status", "data", "total")
    class MsgData(_message.Message):
        __slots__ = ("msg_id", "sender", "direction", "content_type", "content", "send_timestamp_ms", "cmd", "recall_timestamp", "quote_msg_id", "msg_seq", "edit_timestamp")
        MSG_ID_FIELD_NUMBER: _ClassVar[int]
        SENDER_FIELD_NUMBER: _ClassVar[int]
        DIRECTION_FIELD_NUMBER: _ClassVar[int]
        CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        CONTENT_FIELD_NUMBER: _ClassVar[int]
        SEND_TIMESTAMP_MS_FIELD_NUMBER: _ClassVar[int]
        CMD_FIELD_NUMBER: _ClassVar[int]
        RECALL_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        QUOTE_MSG_ID_FIELD_NUMBER: _ClassVar[int]
        MSG_SEQ_FIELD_NUMBER: _ClassVar[int]
        EDIT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        msg_id: str
        sender: Sender
        direction: str
        content_type: ContentType
        content: MsgContent
        send_timestamp_ms: int
        cmd: Cmd
        recall_timestamp: int
        quote_msg_id: str
        msg_seq: int
        edit_timestamp: int
        def __init__(self, msg_id: _Optional[str] = ..., sender: _Optional[_Union[Sender, _Mapping]] = ..., direction: _Optional[str] = ..., content_type: _Optional[_Union[ContentType, str]] = ..., content: _Optional[_Union[MsgContent, _Mapping]] = ..., send_timestamp_ms: _Optional[int] = ..., cmd: _Optional[_Union[Cmd, _Mapping]] = ..., recall_timestamp: _Optional[int] = ..., quote_msg_id: _Optional[str] = ..., msg_seq: _Optional[int] = ..., edit_timestamp: _Optional[int] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    status: Status
    data: _containers.RepeatedCompositeFieldContainer[ListMsgResponse.MsgData]
    total: int
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., data: _Optional[_Iterable[_Union[ListMsgResponse.MsgData, _Mapping]]] = ..., total: _Optional[int] = ...) -> None: ...

class BotData(_message.Message):
    __slots__ = ("bot_id", "name", "name_id", "avatar_url", "avatar_id", "introduction", "create_by", "create_timestamp", "headcount", "private", "is_stop", "always_agree", "prevent_deletion", "do_not_disturb", "ban_id", "ban_until_timestamp", "top", "is_deleted", "group_limit", "field21", "ban_reason")
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_ID_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    AVATAR_ID_FIELD_NUMBER: _ClassVar[int]
    INTRODUCTION_FIELD_NUMBER: _ClassVar[int]
    CREATE_BY_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    HEADCOUNT_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_FIELD_NUMBER: _ClassVar[int]
    IS_STOP_FIELD_NUMBER: _ClassVar[int]
    ALWAYS_AGREE_FIELD_NUMBER: _ClassVar[int]
    PREVENT_DELETION_FIELD_NUMBER: _ClassVar[int]
    DO_NOT_DISTURB_FIELD_NUMBER: _ClassVar[int]
    BAN_ID_FIELD_NUMBER: _ClassVar[int]
    BAN_UNTIL_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TOP_FIELD_NUMBER: _ClassVar[int]
    IS_DELETED_FIELD_NUMBER: _ClassVar[int]
    GROUP_LIMIT_FIELD_NUMBER: _ClassVar[int]
    FIELD21_FIELD_NUMBER: _ClassVar[int]
    BAN_REASON_FIELD_NUMBER: _ClassVar[int]
    bot_id: str
    name: str
    name_id: int
    avatar_url: str
    avatar_id: int
    introduction: str
    create_by: str
    create_timestamp: int
    headcount: int
    private: bool
    is_stop: bool
    always_agree: bool
    prevent_deletion: bool
    do_not_disturb: bool
    ban_id: int
    ban_until_timestamp: int
    top: bool
    is_deleted: bool
    group_limit: bool
    field21: int
    ban_reason: str
    def __init__(self, bot_id: _Optional[str] = ..., name: _Optional[str] = ..., name_id: _Optional[int] = ..., avatar_url: _Optional[str] = ..., avatar_id: _Optional[int] = ..., introduction: _Optional[str] = ..., create_by: _Optional[str] = ..., create_timestamp: _Optional[int] = ..., headcount: _Optional[int] = ..., private: _Optional[bool] = ..., is_stop: _Optional[bool] = ..., always_agree: _Optional[bool] = ..., prevent_deletion: _Optional[bool] = ..., do_not_disturb: _Optional[bool] = ..., ban_id: _Optional[int] = ..., ban_until_timestamp: _Optional[int] = ..., top: _Optional[bool] = ..., is_deleted: _Optional[bool] = ..., group_limit: _Optional[bool] = ..., field21: _Optional[int] = ..., ban_reason: _Optional[str] = ...) -> None: ...

class GroupData(_message.Message):
    __slots__ = ("group_id", "name", "avatar_url", "avatar_id", "introduction", "headcount", "create_by", "direct_join", "permisson_level", "history_msg", "category_name", "category_id", "private", "do_not_disturb", "community_id", "community_name", "ban_id", "ban_until_timestamp", "top", "admin", "gag_until_timestamp", "limited_msg_type", "owner", "recommandation", "is_gag", "tag_old", "tag", "my_group_nickname", "group_code", "hide_group_members", "field31", "auto_delete_message", "deny_members_upload_to_group_disk", "ban_reason")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    AVATAR_ID_FIELD_NUMBER: _ClassVar[int]
    INTRODUCTION_FIELD_NUMBER: _ClassVar[int]
    HEADCOUNT_FIELD_NUMBER: _ClassVar[int]
    CREATE_BY_FIELD_NUMBER: _ClassVar[int]
    DIRECT_JOIN_FIELD_NUMBER: _ClassVar[int]
    PERMISSON_LEVEL_FIELD_NUMBER: _ClassVar[int]
    HISTORY_MSG_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_NAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_FIELD_NUMBER: _ClassVar[int]
    DO_NOT_DISTURB_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_ID_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_NAME_FIELD_NUMBER: _ClassVar[int]
    BAN_ID_FIELD_NUMBER: _ClassVar[int]
    BAN_UNTIL_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TOP_FIELD_NUMBER: _ClassVar[int]
    ADMIN_FIELD_NUMBER: _ClassVar[int]
    GAG_UNTIL_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LIMITED_MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    RECOMMANDATION_FIELD_NUMBER: _ClassVar[int]
    IS_GAG_FIELD_NUMBER: _ClassVar[int]
    TAG_OLD_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    MY_GROUP_NICKNAME_FIELD_NUMBER: _ClassVar[int]
    GROUP_CODE_FIELD_NUMBER: _ClassVar[int]
    HIDE_GROUP_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    FIELD31_FIELD_NUMBER: _ClassVar[int]
    AUTO_DELETE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DENY_MEMBERS_UPLOAD_TO_GROUP_DISK_FIELD_NUMBER: _ClassVar[int]
    BAN_REASON_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    name: str
    avatar_url: str
    avatar_id: int
    introduction: str
    headcount: int
    create_by: str
    direct_join: bool
    permisson_level: int
    history_msg: bool
    category_name: str
    category_id: int
    private: bool
    do_not_disturb: bool
    community_id: int
    community_name: str
    ban_id: int
    ban_until_timestamp: int
    top: bool
    admin: _containers.RepeatedScalarFieldContainer[str]
    gag_until_timestamp: int
    limited_msg_type: str
    owner: str
    recommandation: bool
    is_gag: bool
    tag_old: _containers.RepeatedScalarFieldContainer[str]
    tag: _containers.RepeatedCompositeFieldContainer[Tag]
    my_group_nickname: str
    group_code: str
    hide_group_members: bool
    field31: int
    auto_delete_message: bool
    deny_members_upload_to_group_disk: bool
    ban_reason: str
    def __init__(self, group_id: _Optional[str] = ..., name: _Optional[str] = ..., avatar_url: _Optional[str] = ..., avatar_id: _Optional[int] = ..., introduction: _Optional[str] = ..., headcount: _Optional[int] = ..., create_by: _Optional[str] = ..., direct_join: _Optional[bool] = ..., permisson_level: _Optional[int] = ..., history_msg: _Optional[bool] = ..., category_name: _Optional[str] = ..., category_id: _Optional[int] = ..., private: _Optional[bool] = ..., do_not_disturb: _Optional[bool] = ..., community_id: _Optional[int] = ..., community_name: _Optional[str] = ..., ban_id: _Optional[int] = ..., ban_until_timestamp: _Optional[int] = ..., top: _Optional[bool] = ..., admin: _Optional[_Iterable[str]] = ..., gag_until_timestamp: _Optional[int] = ..., limited_msg_type: _Optional[str] = ..., owner: _Optional[str] = ..., recommandation: _Optional[bool] = ..., is_gag: _Optional[bool] = ..., tag_old: _Optional[_Iterable[str]] = ..., tag: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ..., my_group_nickname: _Optional[str] = ..., group_code: _Optional[str] = ..., hide_group_members: _Optional[bool] = ..., field31: _Optional[int] = ..., auto_delete_message: _Optional[bool] = ..., deny_members_upload_to_group_disk: _Optional[bool] = ..., ban_reason: _Optional[str] = ...) -> None: ...

class GroupInfoRequest(_message.Message):
    __slots__ = ("group_id",)
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    def __init__(self, group_id: _Optional[str] = ...) -> None: ...

class GroupInfoResponse(_message.Message):
    __slots__ = ("status", "data", "bot")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    BOT_FIELD_NUMBER: _ClassVar[int]
    status: Status
    data: GroupData
    bot: _containers.RepeatedCompositeFieldContainer[BotData]
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., data: _Optional[_Union[GroupData, _Mapping]] = ..., bot: _Optional[_Iterable[_Union[BotData, _Mapping]]] = ...) -> None: ...

class ListMemberRequest(_message.Message):
    __slots__ = ("data", "group_id", "keywords")
    class Data(_message.Message):
        __slots__ = ("size", "page")
        SIZE_FIELD_NUMBER: _ClassVar[int]
        PAGE_FIELD_NUMBER: _ClassVar[int]
        size: int
        page: int
        def __init__(self, size: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    data: ListMemberRequest.Data
    group_id: str
    keywords: str
    def __init__(self, data: _Optional[_Union[ListMemberRequest.Data, _Mapping]] = ..., group_id: _Optional[str] = ..., keywords: _Optional[str] = ...) -> None: ...

class ListMemberResponse(_message.Message):
    __slots__ = ("status", "user", "total")
    class User(_message.Message):
        __slots__ = ("group_id", "user_info", "permission_level", "gag_timestamp", "is_gag")
        class UserInfo(_message.Message):
            __slots__ = ("user_id", "name", "avatar_url", "is_vip")
            USER_ID_FIELD_NUMBER: _ClassVar[int]
            NAME_FIELD_NUMBER: _ClassVar[int]
            AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
            IS_VIP_FIELD_NUMBER: _ClassVar[int]
            user_id: str
            name: str
            avatar_url: str
            is_vip: bool
            def __init__(self, user_id: _Optional[str] = ..., name: _Optional[str] = ..., avatar_url: _Optional[str] = ..., is_vip: _Optional[bool] = ...) -> None: ...
        GROUP_ID_FIELD_NUMBER: _ClassVar[int]
        USER_INFO_FIELD_NUMBER: _ClassVar[int]
        PERMISSION_LEVEL_FIELD_NUMBER: _ClassVar[int]
        GAG_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        IS_GAG_FIELD_NUMBER: _ClassVar[int]
        group_id: str
        user_info: ListMemberResponse.User.UserInfo
        permission_level: int
        gag_timestamp: int
        is_gag: bool
        def __init__(self, group_id: _Optional[str] = ..., user_info: _Optional[_Union[ListMemberResponse.User.UserInfo, _Mapping]] = ..., permission_level: _Optional[int] = ..., gag_timestamp: _Optional[int] = ..., is_gag: _Optional[bool] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    status: Status
    user: _containers.RepeatedCompositeFieldContainer[ListMemberResponse.User]
    total: int
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., user: _Optional[_Iterable[_Union[ListMemberResponse.User, _Mapping]]] = ..., total: _Optional[int] = ...) -> None: ...

class EditGroupRequest(_message.Message):
    __slots__ = ("group_id", "name", "introduction", "avatar_url", "direct_join", "history_msg", "category_name", "category_id", "private", "hide_group_members")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    INTRODUCTION_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    DIRECT_JOIN_FIELD_NUMBER: _ClassVar[int]
    HISTORY_MSG_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_NAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_FIELD_NUMBER: _ClassVar[int]
    HIDE_GROUP_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    name: str
    introduction: str
    avatar_url: str
    direct_join: bool
    history_msg: bool
    category_name: str
    category_id: int
    private: bool
    hide_group_members: bool
    def __init__(self, group_id: _Optional[str] = ..., name: _Optional[str] = ..., introduction: _Optional[str] = ..., avatar_url: _Optional[str] = ..., direct_join: _Optional[bool] = ..., history_msg: _Optional[bool] = ..., category_name: _Optional[str] = ..., category_id: _Optional[int] = ..., private: _Optional[bool] = ..., hide_group_members: _Optional[bool] = ...) -> None: ...

class BotListRequest(_message.Message):
    __slots__ = ("group_id",)
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    def __init__(self, group_id: _Optional[str] = ...) -> None: ...

class BotListResponse(_message.Message):
    __slots__ = ("status", "bot", "instruction", "menu")
    class InstructionData(_message.Message):
        __slots__ = ("id", "bot_id", "name", "desc", "type", "hint_text", "default_text", "sort", "form", "bot_name")
        ID_FIELD_NUMBER: _ClassVar[int]
        BOT_ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        DESC_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        HINT_TEXT_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_TEXT_FIELD_NUMBER: _ClassVar[int]
        SORT_FIELD_NUMBER: _ClassVar[int]
        FORM_FIELD_NUMBER: _ClassVar[int]
        BOT_NAME_FIELD_NUMBER: _ClassVar[int]
        id: int
        bot_id: str
        name: str
        desc: str
        type: int
        hint_text: str
        default_text: str
        sort: int
        form: str
        bot_name: str
        def __init__(self, id: _Optional[int] = ..., bot_id: _Optional[str] = ..., name: _Optional[str] = ..., desc: _Optional[str] = ..., type: _Optional[int] = ..., hint_text: _Optional[str] = ..., default_text: _Optional[str] = ..., sort: _Optional[int] = ..., form: _Optional[str] = ..., bot_name: _Optional[str] = ...) -> None: ...
    class MenuData(_message.Message):
        __slots__ = ("id", "bot_id", "name", "content", "menu_type", "create_timestamp", "menu_action", "select")
        ID_FIELD_NUMBER: _ClassVar[int]
        BOT_ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        CONTENT_FIELD_NUMBER: _ClassVar[int]
        MENU_TYPE_FIELD_NUMBER: _ClassVar[int]
        CREATE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        MENU_ACTION_FIELD_NUMBER: _ClassVar[int]
        SELECT_FIELD_NUMBER: _ClassVar[int]
        id: int
        bot_id: str
        name: str
        content: str
        menu_type: int
        create_timestamp: int
        menu_action: int
        select: str
        def __init__(self, id: _Optional[int] = ..., bot_id: _Optional[str] = ..., name: _Optional[str] = ..., content: _Optional[str] = ..., menu_type: _Optional[int] = ..., create_timestamp: _Optional[int] = ..., menu_action: _Optional[int] = ..., select: _Optional[str] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BOT_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTION_FIELD_NUMBER: _ClassVar[int]
    MENU_FIELD_NUMBER: _ClassVar[int]
    status: Status
    bot: _containers.RepeatedCompositeFieldContainer[BotData]
    instruction: _containers.RepeatedCompositeFieldContainer[BotListResponse.InstructionData]
    menu: _containers.RepeatedCompositeFieldContainer[BotListResponse.MenuData]
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., bot: _Optional[_Iterable[_Union[BotData, _Mapping]]] = ..., instruction: _Optional[_Iterable[_Union[BotListResponse.InstructionData, _Mapping]]] = ..., menu: _Optional[_Iterable[_Union[BotListResponse.MenuData, _Mapping]]] = ...) -> None: ...

class InfoAddFriendRequest(_message.Message):
    __slots__ = ("keyword",)
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    keyword: str
    def __init__(self, keyword: _Optional[str] = ...) -> None: ...

class InfoAddFriendResponse(_message.Message):
    __slots__ = ("status", "data")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    status: Status
    data: GroupData
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., data: _Optional[_Union[GroupData, _Mapping]] = ...) -> None: ...

class CreateGroupRequest(_message.Message):
    __slots__ = ("name", "introduction", "avatar_url")
    NAME_FIELD_NUMBER: _ClassVar[int]
    INTRODUCTION_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    name: str
    introduction: str
    avatar_url: str
    def __init__(self, name: _Optional[str] = ..., introduction: _Optional[str] = ..., avatar_url: _Optional[str] = ...) -> None: ...

class CreateGroupResponse(_message.Message):
    __slots__ = ("status", "group_id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    status: Status
    group_id: str
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., group_id: _Optional[str] = ...) -> None: ...

class DismissGroupRequest(_message.Message):
    __slots__ = ("group_id",)
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    def __init__(self, group_id: _Optional[str] = ...) -> None: ...

class TagMemberRequest(_message.Message):
    __slots__ = ("data", "group_id", "tag_id")
    class Data(_message.Message):
        __slots__ = ("size", "page")
        SIZE_FIELD_NUMBER: _ClassVar[int]
        PAGE_FIELD_NUMBER: _ClassVar[int]
        size: int
        page: int
        def __init__(self, size: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TAG_ID_FIELD_NUMBER: _ClassVar[int]
    data: TagMemberRequest.Data
    group_id: str
    tag_id: int
    def __init__(self, data: _Optional[_Union[TagMemberRequest.Data, _Mapping]] = ..., group_id: _Optional[str] = ..., tag_id: _Optional[int] = ...) -> None: ...

class GetBotInstructionRequest(_message.Message):
    __slots__ = ("bot_id",)
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    bot_id: str
    def __init__(self, bot_id: _Optional[str] = ...) -> None: ...

class GetBotInstructionResponse(_message.Message):
    __slots__ = ("status", "data")
    class Data(_message.Message):
        __slots__ = ("command_id", "bot_id", "command_name", "instruction_type", "command_default_text", "command_settings_json")
        COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
        BOT_ID_FIELD_NUMBER: _ClassVar[int]
        COMMAND_NAME_FIELD_NUMBER: _ClassVar[int]
        INSTRUCTION_TYPE_FIELD_NUMBER: _ClassVar[int]
        COMMAND_DEFAULT_TEXT_FIELD_NUMBER: _ClassVar[int]
        COMMAND_SETTINGS_JSON_FIELD_NUMBER: _ClassVar[int]
        command_id: int
        bot_id: str
        command_name: str
        instruction_type: int
        command_default_text: str
        command_settings_json: str
        def __init__(self, command_id: _Optional[int] = ..., bot_id: _Optional[str] = ..., command_name: _Optional[str] = ..., instruction_type: _Optional[int] = ..., command_default_text: _Optional[str] = ..., command_settings_json: _Optional[str] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    status: Status
    data: GetBotInstructionResponse.Data
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., data: _Optional[_Union[GetBotInstructionResponse.Data, _Mapping]] = ...) -> None: ...

class BotBoardMessage(_message.Message):
    __slots__ = ("bot_id", "chat_id", "chat_type", "content", "content_type", "last_update_timestamp", "bot_name")
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    BOT_NAME_FIELD_NUMBER: _ClassVar[int]
    bot_id: str
    chat_id: str
    chat_type: ChatType
    content: str
    content_type: ContentTypeTextOnly
    last_update_timestamp: int
    bot_name: str
    def __init__(self, bot_id: _Optional[str] = ..., chat_id: _Optional[str] = ..., chat_type: _Optional[_Union[ChatType, str]] = ..., content: _Optional[str] = ..., content_type: _Optional[_Union[ContentTypeTextOnly, str]] = ..., last_update_timestamp: _Optional[int] = ..., bot_name: _Optional[str] = ...) -> None: ...

class BotInfoRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class BotInfoResponse(_message.Message):
    __slots__ = ("status", "data")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    status: Status
    data: BotData
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., data: _Optional[_Union[BotData, _Mapping]] = ...) -> None: ...

class BoardRequest(_message.Message):
    __slots__ = ("id", "chat_type")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    chat_type: ChatType
    def __init__(self, id: _Optional[str] = ..., chat_type: _Optional[_Union[ChatType, str]] = ...) -> None: ...

class BoardResponse(_message.Message):
    __slots__ = ("status", "data")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    status: Status
    data: BotBoardMessage
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., data: _Optional[_Union[BotBoardMessage, _Mapping]] = ...) -> None: ...

class CreateBotRequest(_message.Message):
    __slots__ = ("name", "introduction", "avatar_url", "private")
    NAME_FIELD_NUMBER: _ClassVar[int]
    INTRODUCTION_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_FIELD_NUMBER: _ClassVar[int]
    name: str
    introduction: str
    avatar_url: str
    private: bool
    def __init__(self, name: _Optional[str] = ..., introduction: _Optional[str] = ..., avatar_url: _Optional[str] = ..., private: _Optional[bool] = ...) -> None: ...

class CreateBotResponse(_message.Message):
    __slots__ = ("status", "data")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    status: Status
    data: BotData
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., data: _Optional[_Union[BotData, _Mapping]] = ...) -> None: ...

class ListFollowerRequest(_message.Message):
    __slots__ = ("data", "bot_id", "keywords")
    class Data(_message.Message):
        __slots__ = ("size", "page")
        SIZE_FIELD_NUMBER: _ClassVar[int]
        PAGE_FIELD_NUMBER: _ClassVar[int]
        size: int
        page: int
        def __init__(self, size: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    data: ListFollowerRequest.Data
    bot_id: str
    keywords: str
    def __init__(self, data: _Optional[_Union[ListFollowerRequest.Data, _Mapping]] = ..., bot_id: _Optional[str] = ..., keywords: _Optional[str] = ...) -> None: ...

class ListFollowerResponse(_message.Message):
    __slots__ = ("status", "user", "totol")
    class User(_message.Message):
        __slots__ = ("user_id", "name", "avatar_url", "is_vip")
        USER_ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
        IS_VIP_FIELD_NUMBER: _ClassVar[int]
        user_id: str
        name: str
        avatar_url: str
        is_vip: bool
        def __init__(self, user_id: _Optional[str] = ..., name: _Optional[str] = ..., avatar_url: _Optional[str] = ..., is_vip: _Optional[bool] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    TOTOL_FIELD_NUMBER: _ClassVar[int]
    status: Status
    user: _containers.RepeatedCompositeFieldContainer[ListFollowerResponse.User]
    totol: int
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., user: _Optional[_Iterable[_Union[ListFollowerResponse.User, _Mapping]]] = ..., totol: _Optional[int] = ...) -> None: ...

class JoinGroupListRequest(_message.Message):
    __slots__ = ("data", "bot_id", "keywords")
    class Data(_message.Message):
        __slots__ = ("size", "page")
        SIZE_FIELD_NUMBER: _ClassVar[int]
        PAGE_FIELD_NUMBER: _ClassVar[int]
        size: int
        page: int
        def __init__(self, size: _Optional[int] = ..., page: _Optional[int] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    data: JoinGroupListRequest.Data
    bot_id: str
    keywords: str
    def __init__(self, data: _Optional[_Union[JoinGroupListRequest.Data, _Mapping]] = ..., bot_id: _Optional[str] = ..., keywords: _Optional[str] = ...) -> None: ...

class JoinGroupListResponse(_message.Message):
    __slots__ = ("status", "group", "total")
    class Group(_message.Message):
        __slots__ = ("id", "name", "avatar_url")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
        id: str
        name: str
        avatar_url: str
        def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., avatar_url: _Optional[str] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    status: Status
    group: _containers.RepeatedCompositeFieldContainer[JoinGroupListResponse.Group]
    total: int
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., group: _Optional[_Iterable[_Union[JoinGroupListResponse.Group, _Mapping]]] = ..., total: _Optional[int] = ...) -> None: ...

class ConversationListRequest(_message.Message):
    __slots__ = ("md5",)
    MD5_FIELD_NUMBER: _ClassVar[int]
    md5: str
    def __init__(self, md5: _Optional[str] = ...) -> None: ...

class ConversationListResponse(_message.Message):
    __slots__ = ("status", "data", "total", "md5")
    class Data(_message.Message):
        __slots__ = ("chat_id", "chat_type", "remark", "chat_content", "timestamp_ms", "unread_msg", "at", "avatar_id", "avatar_url", "do_not_disturb", "send_timestamp", "is_vip", "at_data", "name", "certification_level")
        class AtData(_message.Message):
            __slots__ = ("unknown", "mentioned_id", "mentioned_name", "mentioned_in", "mentioner_id", "mentioner_name", "msg_seq")
            UNKNOWN_FIELD_NUMBER: _ClassVar[int]
            MENTIONED_ID_FIELD_NUMBER: _ClassVar[int]
            MENTIONED_NAME_FIELD_NUMBER: _ClassVar[int]
            MENTIONED_IN_FIELD_NUMBER: _ClassVar[int]
            MENTIONER_ID_FIELD_NUMBER: _ClassVar[int]
            MENTIONER_NAME_FIELD_NUMBER: _ClassVar[int]
            MSG_SEQ_FIELD_NUMBER: _ClassVar[int]
            unknown: int
            mentioned_id: str
            mentioned_name: str
            mentioned_in: str
            mentioner_id: str
            mentioner_name: str
            msg_seq: int
            def __init__(self, unknown: _Optional[int] = ..., mentioned_id: _Optional[str] = ..., mentioned_name: _Optional[str] = ..., mentioned_in: _Optional[str] = ..., mentioner_id: _Optional[str] = ..., mentioner_name: _Optional[str] = ..., msg_seq: _Optional[int] = ...) -> None: ...
        CHAT_ID_FIELD_NUMBER: _ClassVar[int]
        CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
        REMARK_FIELD_NUMBER: _ClassVar[int]
        CHAT_CONTENT_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_MS_FIELD_NUMBER: _ClassVar[int]
        UNREAD_MSG_FIELD_NUMBER: _ClassVar[int]
        AT_FIELD_NUMBER: _ClassVar[int]
        AVATAR_ID_FIELD_NUMBER: _ClassVar[int]
        AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
        DO_NOT_DISTURB_FIELD_NUMBER: _ClassVar[int]
        SEND_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        IS_VIP_FIELD_NUMBER: _ClassVar[int]
        AT_DATA_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        CERTIFICATION_LEVEL_FIELD_NUMBER: _ClassVar[int]
        chat_id: str
        chat_type: ChatType
        remark: str
        chat_content: str
        timestamp_ms: int
        unread_msg: int
        at: bool
        avatar_id: int
        avatar_url: str
        do_not_disturb: bool
        send_timestamp: int
        is_vip: bool
        at_data: ConversationListResponse.Data.AtData
        name: str
        certification_level: int
        def __init__(self, chat_id: _Optional[str] = ..., chat_type: _Optional[_Union[ChatType, str]] = ..., remark: _Optional[str] = ..., chat_content: _Optional[str] = ..., timestamp_ms: _Optional[int] = ..., unread_msg: _Optional[int] = ..., at: _Optional[bool] = ..., avatar_id: _Optional[int] = ..., avatar_url: _Optional[str] = ..., do_not_disturb: _Optional[bool] = ..., send_timestamp: _Optional[int] = ..., is_vip: _Optional[bool] = ..., at_data: _Optional[_Union[ConversationListResponse.Data.AtData, _Mapping]] = ..., name: _Optional[str] = ..., certification_level: _Optional[int] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    MD5_FIELD_NUMBER: _ClassVar[int]
    status: Status
    data: _containers.RepeatedCompositeFieldContainer[ConversationListResponse.Data]
    total: int
    md5: str
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., data: _Optional[_Iterable[_Union[ConversationListResponse.Data, _Mapping]]] = ..., total: _Optional[int] = ..., md5: _Optional[str] = ...) -> None: ...

class AddressBookListRequest(_message.Message):
    __slots__ = ("md5",)
    MD5_FIELD_NUMBER: _ClassVar[int]
    md5: str
    def __init__(self, md5: _Optional[str] = ...) -> None: ...

class AddressBookListResponse(_message.Message):
    __slots__ = ("status", "data", "md5")
    class Data(_message.Message):
        __slots__ = ("list_name", "data", "chat_type")
        class DataList(_message.Message):
            __slots__ = ("chat_id", "remark", "avatar_url", "permisson_level", "no_disturb", "name")
            CHAT_ID_FIELD_NUMBER: _ClassVar[int]
            REMARK_FIELD_NUMBER: _ClassVar[int]
            AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
            PERMISSON_LEVEL_FIELD_NUMBER: _ClassVar[int]
            NO_DISTURB_FIELD_NUMBER: _ClassVar[int]
            NAME_FIELD_NUMBER: _ClassVar[int]
            chat_id: str
            remark: str
            avatar_url: str
            permisson_level: int
            no_disturb: bool
            name: str
            def __init__(self, chat_id: _Optional[str] = ..., remark: _Optional[str] = ..., avatar_url: _Optional[str] = ..., permisson_level: _Optional[int] = ..., no_disturb: _Optional[bool] = ..., name: _Optional[str] = ...) -> None: ...
        LIST_NAME_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
        list_name: str
        data: _containers.RepeatedCompositeFieldContainer[AddressBookListResponse.Data.DataList]
        chat_type: ChatType
        def __init__(self, list_name: _Optional[str] = ..., data: _Optional[_Iterable[_Union[AddressBookListResponse.Data.DataList, _Mapping]]] = ..., chat_type: _Optional[_Union[ChatType, str]] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    MD5_FIELD_NUMBER: _ClassVar[int]
    status: Status
    data: _containers.RepeatedCompositeFieldContainer[AddressBookListResponse.Data]
    md5: str
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., data: _Optional[_Iterable[_Union[AddressBookListResponse.Data, _Mapping]]] = ..., md5: _Optional[str] = ...) -> None: ...

class RequestListResponse(_message.Message):
    __slots__ = ("status", "requests", "total", "pending")
    class Request(_message.Message):
        __slots__ = ("receiver_name", "receiver_avatar", "name", "avatar", "group_name", "group_avatar", "inviter_id", "source_type", "target_type", "target_id", "receiver_id", "result", "processed_at", "invite_at", "invite_at_str", "request_id", "bot_name", "bot_avatar", "processor_name", "note", "is_vip")
        RECEIVER_NAME_FIELD_NUMBER: _ClassVar[int]
        RECEIVER_AVATAR_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        AVATAR_FIELD_NUMBER: _ClassVar[int]
        GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
        GROUP_AVATAR_FIELD_NUMBER: _ClassVar[int]
        INVITER_ID_FIELD_NUMBER: _ClassVar[int]
        SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
        TARGET_TYPE_FIELD_NUMBER: _ClassVar[int]
        TARGET_ID_FIELD_NUMBER: _ClassVar[int]
        RECEIVER_ID_FIELD_NUMBER: _ClassVar[int]
        RESULT_FIELD_NUMBER: _ClassVar[int]
        PROCESSED_AT_FIELD_NUMBER: _ClassVar[int]
        INVITE_AT_FIELD_NUMBER: _ClassVar[int]
        INVITE_AT_STR_FIELD_NUMBER: _ClassVar[int]
        REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
        BOT_NAME_FIELD_NUMBER: _ClassVar[int]
        BOT_AVATAR_FIELD_NUMBER: _ClassVar[int]
        PROCESSOR_NAME_FIELD_NUMBER: _ClassVar[int]
        NOTE_FIELD_NUMBER: _ClassVar[int]
        IS_VIP_FIELD_NUMBER: _ClassVar[int]
        receiver_name: str
        receiver_avatar: str
        name: str
        avatar: str
        group_name: str
        group_avatar: str
        inviter_id: str
        source_type: int
        target_type: int
        target_id: str
        receiver_id: str
        result: int
        processed_at: int
        invite_at: int
        invite_at_str: str
        request_id: int
        bot_name: str
        bot_avatar: str
        processor_name: str
        note: str
        is_vip: bool
        def __init__(self, receiver_name: _Optional[str] = ..., receiver_avatar: _Optional[str] = ..., name: _Optional[str] = ..., avatar: _Optional[str] = ..., group_name: _Optional[str] = ..., group_avatar: _Optional[str] = ..., inviter_id: _Optional[str] = ..., source_type: _Optional[int] = ..., target_type: _Optional[int] = ..., target_id: _Optional[str] = ..., receiver_id: _Optional[str] = ..., result: _Optional[int] = ..., processed_at: _Optional[int] = ..., invite_at: _Optional[int] = ..., invite_at_str: _Optional[str] = ..., request_id: _Optional[int] = ..., bot_name: _Optional[str] = ..., bot_avatar: _Optional[str] = ..., processor_name: _Optional[str] = ..., note: _Optional[str] = ..., is_vip: _Optional[bool] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    PENDING_FIELD_NUMBER: _ClassVar[int]
    status: Status
    requests: _containers.RepeatedCompositeFieldContainer[RequestListResponse.Request]
    total: int
    pending: int
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ..., requests: _Optional[_Iterable[_Union[RequestListResponse.Request, _Mapping]]] = ..., total: _Optional[int] = ..., pending: _Optional[int] = ...) -> None: ...
