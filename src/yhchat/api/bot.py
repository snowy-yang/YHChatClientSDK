"""机器人开放接口（``/open-apis/v1``）。

对应 yhchatAPI 文档站 ``src/api/bot/v1/bot.md`` 里的 6 个消息接口，
外加文档未收录、但云端实际提供的 3 个上传接口。
"""

from collections.abc import AsyncIterable, AsyncIterator, Iterable, Mapping
from typing import Any, Literal, cast

from ..errors import TransportError
from ..models import BaseSegment, BatchSendResult, MessageInfo, MessagePage
from ..records import MessageRegistry
from ..transport import HttpTransport, data_of

_SEND = "/open-apis/v1/bot/send"
_BATCH_SEND = "/open-apis/v1/bot/batch_send"
_SEND_STREAM = "/open-apis/v1/bot/send-stream"
_EDIT = "/open-apis/v1/bot/edit"
_RECALL = "/open-apis/v1/bot/recall"
_MESSAGES = "/open-apis/v1/bot/messages"


class BotMessageAPI:
    """消息发送、编辑、撤回与查询。"""

    def __init__(self, http: HttpTransport, records: MessageRegistry) -> None:
        self._http = http
        self._records = records

    async def send(
        self,
        recv_type: str,
        recv_id: str,
        message: BaseSegment,
        *,
        parent_id: str | None = None,
    ) -> MessageInfo:
        """发送一条消息。``recv_type`` 取 ``user`` 或 ``group``。"""
        payload = await self._http.request(
            "POST",
            _SEND,
            json={
                "recvId": recv_id,
                "recvType": recv_type,
                "contentType": message.content_type,
                "content": message.to_content(),
                "parentId": parent_id,
            },
        )
        info = _message_info(payload, _SEND)
        self._records.add(info)
        return info

    async def send_many(
        self,
        recv_type: str,
        recv_id: str,
        messages: Iterable[BaseSegment],
        *,
        parent_id: str | None = None,
    ) -> list[MessageInfo]:
        """按顺序逐条发送多个消息段（云湖没有多段接口，这里只是循环）。"""
        return [await self.send(recv_type, recv_id, message, parent_id=parent_id) for message in messages]

    async def batch_send(
        self,
        recv_ids: Iterable[str],
        recv_type: str,
        message: BaseSegment,
        *,
        parent_id: str | None = None,
    ) -> BatchSendResult:
        """向多个会话发送同一条消息；重复的 ``recv_id`` 只发一次。"""
        payload = await self._http.request(
            "POST",
            _BATCH_SEND,
            json={
                "recvIds": list(recv_ids),
                "recvType": recv_type,
                "contentType": message.content_type,
                "content": message.to_content(),
                "parentId": parent_id,
            },
        )
        result = BatchSendResult.model_validate(dict(data_of(payload, endpoint=_BATCH_SEND)))
        for info in result.success_list:
            self._records.add(info)
        return result

    async def send_stream(
        self,
        recv_type: str,
        recv_id: str,
        message_type: Literal["text", "markdown"],
        chunks: AsyncIterable[str],
        *,
        parent_id: str | None = None,
    ) -> MessageInfo:
        """流式发送：请求体走 chunked，最终只返回一条消息信息。

        ``parent_id`` 当前未出现在文档的查询参数里，仅在需要引用时透传（云端可能忽略）。
        """
        params: dict[str, Any] = {"recvId": recv_id, "recvType": recv_type, "contentType": message_type}
        if parent_id is not None:
            params["parentId"] = parent_id

        async def body() -> AsyncIterator[bytes]:
            async for chunk in chunks:
                yield chunk.encode()

        payload = await self._http.request_stream("POST", _SEND_STREAM, chunks=body(), params=params)
        info = _message_info(payload, _SEND_STREAM)
        self._records.add(info)
        return info

    async def edit(
        self,
        msg_id: str,
        message: BaseSegment,
        *,
        recv_id: str | None = None,
        recv_type: str | None = None,
    ) -> int:
        """编辑已发送的消息，返回成功数量。

        ``recv_id`` / ``recv_type`` 省略时从 :class:`~yhchat.records.MessageRegistry` 里补全。
        """
        target = self._resolve(msg_id, recv_id, recv_type)
        payload = await self._http.request(
            "POST",
            _EDIT,
            json={
                "msgId": msg_id,
                "recvId": target.recv_id,
                "recvType": target.recv_type,
                "contentType": message.content_type,
                "content": message.to_content(),
            },
        )
        count = data_of(payload, endpoint=_EDIT).get("successCount", 0)
        return count if isinstance(count, int) else 0

    async def recall(
        self,
        msg_id: str,
        *,
        chat_id: str | None = None,
        chat_type: str | None = None,
    ) -> None:
        """撤回消息；``chat_id`` / ``chat_type`` 省略时从消息记录里补全。"""
        info = self._resolve(msg_id, chat_id, chat_type)
        await self._http.request(
            "POST",
            _RECALL,
            json={"msgId": msg_id, "chatId": info.recv_id, "chatType": info.recv_type},
        )
        self._records.pop(msg_id)

    async def list(
        self,
        chat_id: str,
        chat_type: str,
        *,
        message_id: str | None = None,
        before: int = 0,
        after: int = 0,
    ) -> MessagePage:
        """拉取会话内的消息列表。

        文档写的是 ``message-id`` 查询参数（旧版实现里用的却是 ``msg-id``），这里按文档实现。
        """
        params: dict[str, Any] = {
            "chat-id": chat_id,
            "chat-type": chat_type,
            "before": before,
            "after": after,
        }
        if message_id is not None:
            params["message-id"] = message_id
        payload = await self._http.request("POST", _MESSAGES, params=params)
        return MessagePage.model_validate(dict(data_of(payload, endpoint=_MESSAGES)))

    def _resolve(self, msg_id: str, recv_id: str | None, recv_type: str | None) -> MessageInfo:
        """补全会话信息：显式参数优先，其次查消息记录。"""
        if recv_id is not None and recv_type is not None:
            return MessageInfo.model_validate({"msgId": msg_id, "recvId": recv_id, "recvType": recv_type})
        record = self._records.get(msg_id)
        if record is None:
            raise ValueError(f"找不到 {msg_id} 的会话信息，请显式传入 recv_id 与 recv_type")
        return MessageInfo.model_validate(
            {
                "msgId": msg_id,
                "recvId": recv_id or record.recv_id,
                "recvType": recv_type or record.recv_type,
            }
        )


class BotUploadAPI:
    """图片 / 视频 / 文件上传，返回发送消息所需的 key。"""

    def __init__(self, http: HttpTransport) -> None:
        self._http = http

    async def image(self, data: bytes, *, filename: str = "image.png", mime_type: str | None = None) -> str:
        """上传图片，返回 ``imageKey``。"""
        return await self._upload("/open-apis/v1/image/upload", "image", data, filename, mime_type, "imageKey")

    async def video(self, data: bytes, *, filename: str = "video.mp4", mime_type: str | None = None) -> str:
        """上传视频，返回 ``videoKey``。"""
        return await self._upload("/open-apis/v1/video/upload", "video", data, filename, mime_type, "videoKey")

    async def file(self, data: bytes, *, filename: str = "file.bin", mime_type: str | None = None) -> str:
        """上传文件，返回 ``fileKey``。"""
        return await self._upload("/open-apis/v1/file/upload", "file", data, filename, mime_type, "fileKey")

    async def _upload(
        self,
        path: str,
        field: str,
        data: bytes,
        filename: str,
        mime_type: str | None,
        response_key: str,
    ) -> str:
        files: Mapping[str, tuple[str, bytes, str]] = {field: (filename, data, mime_type or "application/octet-stream")}
        payload = await self._http.request("POST", path, files=files)
        value = data_of(payload, endpoint=path).get(response_key)
        if not isinstance(value, str):
            raise TransportError(f"{path} 响应缺少 {response_key}: {payload!r}")
        return value


class BotAPI:
    """``/open-apis/v1`` 下的接口集合。"""

    def __init__(self, http: HttpTransport, records: MessageRegistry) -> None:
        self.message = BotMessageAPI(http, records)
        self.upload = BotUploadAPI(http)


def _message_info(payload: Mapping[str, Any], endpoint: str) -> MessageInfo:
    """从 ``{"data": {"messageInfo": {...}}}`` 里取出消息信息。"""
    data = data_of(payload, endpoint=endpoint)
    raw = data.get("messageInfo")
    if not isinstance(raw, dict):
        raise TransportError(f"{endpoint} 响应缺少 messageInfo: {payload!r}")
    return MessageInfo.model_validate(cast("dict[str, Any]", raw))
