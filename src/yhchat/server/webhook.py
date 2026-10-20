"""云湖事件回调（webhook）的解析与 Satori 事件映射。

回调体形如 ``{"header": {...}, "event": {...}}``，``header.eventType`` 区分事件类型。
目前只处理消息事件：``message.receive.normal``、``message.receive.instruction``。
"""

from typing import Any, cast

from pydantic import Field

from ..models import ApiModel, ReceivedMessage
from ..satori.backend import CHANNEL_DIRECT, CHANNEL_TEXT, ChannelRegistry, render_message_content
from ..satori.models import Channel, Event, Guild, Login, Member, MessageObject, User, now_millis

MESSAGE_EVENT_TYPES = frozenset({"message.receive.normal", "message.receive.instruction"})


class WebhookHeader(ApiModel):
    """回调头。"""

    event_id: str = Field(alias="eventId")
    event_time: int | None = Field(default=None, alias="eventTime")
    event_type: str = Field(alias="eventType")


class WebhookSender(ApiModel):
    """消息发送者。"""

    sender_id: str = Field(alias="senderId")
    sender_type: str = Field(default="user", alias="senderType")
    sender_nickname: str | None = Field(default=None, alias="senderNickname")
    sender_user_level: str | None = Field(default=None, alias="senderUserLevel")


class WebhookChat(ApiModel):
    """消息所属会话。"""

    chat_id: str = Field(alias="chatId")
    chat_type: str = Field(alias="chatType")


class WebhookMessage(ApiModel):
    """消息本体；``content`` 结构与 ``/bot/messages`` 返回的一致。"""

    msg_id: str = Field(alias="msgId")
    parent_id: str | None = Field(default=None, alias="parentId")
    send_time: int | None = Field(default=None, alias="sendTime")
    chat_id: str | None = Field(default=None, alias="chatId")
    chat_type: str | None = Field(default=None, alias="chatType")
    content_type: str = Field(alias="contentType")
    content: dict[str, Any] = Field(default_factory=dict[str, Any])
    command_id: int | None = Field(default=None, alias="commandId")
    command_name: str | None = Field(default=None, alias="commandName")


class WebhookEvent(ApiModel):
    """``event`` 字段。"""

    sender: WebhookSender
    chat: WebhookChat
    message: WebhookMessage


class WebhookPayload(ApiModel):
    """一条完整的回调。"""

    header: WebhookHeader
    event: WebhookEvent


def parse_webhook(raw: object) -> WebhookPayload | None:
    """解析回调体；不是消息事件时返回 ``None``（调用方照常 200 应答）。"""
    if not isinstance(raw, dict):
        raise ValueError("回调必须是 JSON 对象")
    payload = cast("dict[str, object]", raw)
    header = WebhookHeader.model_validate(payload.get("header"))
    if header.event_type not in MESSAGE_EVENT_TYPES:
        return None
    return WebhookPayload.model_validate(payload)


def to_satori_event(payload: WebhookPayload, *, login: Login, registry: ChannelRegistry) -> Event:
    """把云湖消息回调映射成 Satori ``message-created`` 事件。"""
    sender = payload.event.sender
    chat = payload.event.chat
    message = payload.event.message

    recv_type = "group" if chat.chat_type == "group" else "user"
    registry.remember(chat.chat_id, recv_type)
    channel = Channel(id=chat.chat_id, type=CHANNEL_TEXT if recv_type == "group" else CHANNEL_DIRECT)
    guild = Guild(id=chat.chat_id) if channel.type == CHANNEL_TEXT else None
    user = User(id=sender.sender_id, name=sender.sender_nickname)
    member = Member(user=user, nick=sender.sender_nickname) if guild is not None else None

    received = ReceivedMessage.model_validate(
        {
            "msgId": message.msg_id,
            "parentId": message.parent_id,
            "senderId": sender.sender_id,
            "senderType": sender.sender_type,
            "senderNickname": sender.sender_nickname,
            "contentType": message.content_type,
            "content": message.content,
            "sendTime": message.send_time,
        }
    )
    referrer: dict[str, object] = {
        "event_id": payload.header.event_id,
        "event_type": payload.header.event_type,
    }
    if message.command_name is not None:
        referrer["command_name"] = message.command_name

    return Event(
        type="message-created",
        timestamp=message.send_time or payload.header.event_time or now_millis(),
        login=login,
        channel=channel,
        guild=guild,
        member=member,
        message=MessageObject(
            id=message.msg_id,
            content=render_message_content(received),
            channel=channel,
            guild=guild,
            member=member,
            user=user,
            created_at=message.send_time,
            updated_at=message.send_time,
        ),
        user=user,
        referrer=referrer,
    )
