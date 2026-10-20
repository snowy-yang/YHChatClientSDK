"""机器人开放接口（``/open-apis/v1``）的请求/响应模型。"""

from typing import Any

from pydantic import Field

from .base import ApiModel
from .segments import Button

type RecvType = str
"""会话类型：``user`` 或 ``group``（云湖文档未把它枚举化，用字符串保持兼容）。"""


class MessageInfo(ApiModel):
    """发送成功后返回的消息信息。"""

    msg_id: str = Field(alias="msgId")
    recv_id: str = Field(alias="recvId")
    recv_type: str = Field(alias="recvType")


class BatchSendResult(ApiModel):
    """批量发送结果。"""

    success_count: int = Field(alias="successCount", default=0)
    success_list: list[MessageInfo] = Field(alias="successList", default_factory=list[MessageInfo])


class ReceivedContent(ApiModel):
    """接收到的消息内容，字段随 ``contentType`` 变化，未覆盖的字段靠 ``extra="allow"`` 保留。"""

    text: str | None = None
    at: list[str] | None = None
    buttons: list[list[Button]] | None = None
    parent: str | None = None
    etag: str | None = None
    image_name: str | None = Field(default=None, alias="imageName")
    image_width: int | None = Field(default=None, alias="imageWidth")
    image_height: int | None = Field(default=None, alias="imageHeight")
    video_url: str | None = Field(default=None, alias="videoUrl")
    video_duration: int | None = Field(default=None, alias="videoDuration")
    audio_url: str | None = Field(default=None, alias="audioUrl")
    audio_duration: int | None = Field(default=None, alias="audioDuration")
    form_json: dict[str, Any] | None = Field(default=None, alias="formJson")


class ReceivedMessage(ApiModel):
    """``/bot/messages`` 返回的单条消息。"""

    msg_id: str = Field(alias="msgId")
    parent_id: str | None = Field(default=None, alias="parentId")
    sender_id: str = Field(alias="senderId")
    sender_type: str = Field(alias="senderType")
    sender_nickname: str | None = Field(default=None, alias="senderNickname")
    content_type: str = Field(alias="contentType")
    content: ReceivedContent = Field(default_factory=ReceivedContent)
    send_time: int | None = Field(default=None, alias="sendTime")
    command_name: str | None = Field(default=None, alias="commandName")
    command_id: int | None = Field(default=None, alias="commandId")


class MessagePage(ApiModel):
    """``/bot/messages`` 的分页结果。"""

    messages: list[ReceivedMessage] = Field(alias="list", default_factory=list[ReceivedMessage])
    total: int = 0
