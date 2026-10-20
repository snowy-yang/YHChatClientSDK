"""gRPC 服务端：把 :class:`~yhchat.client.YHChatClient` 暴露成 RPC。"""

import contextlib
from collections.abc import AsyncGenerator, AsyncIterator, Callable
from typing import Any, Literal, cast

import grpc

from ..client import YHChatClient
from ..errors import APIError, TransportError
from ._pb import yhchat_pb2, yhchat_pb2_grpc
from .convert import message_info_to_proto, received_message_to_proto, segment_from_content

# 生成的 add_*_to_server 没有类型标注，这里收窄成可检查的函数类型。
_ADD_SERVICER = cast(
    "Callable[[object, grpc.aio.Server], None]",
    yhchat_pb2_grpc.add_YHChatServicer_to_server,  # pyright: ignore[reportUnknownMemberType]  # 生成代码无类型标注
)


@contextlib.asynccontextmanager
async def _grpc_errors(
    context: grpc.aio.ServicerContext[Any, Any],
) -> AsyncGenerator[None]:
    """把 SDK 异常映射成 gRPC 状态码。"""
    try:
        yield
    except APIError as exc:
        await context.abort(grpc.StatusCode.FAILED_PRECONDITION, f"[{exc.code}] {exc.message}")
    except (TransportError, ValueError) as exc:
        await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))


class YHChatServicer:
    """``yhchat.v1.YHChat`` 的实现，业务逻辑全部委托给核心 SDK。"""

    def __init__(self, client: YHChatClient) -> None:
        self._client = client

    async def Send(
        self,
        request: yhchat_pb2.SendRequest,
        context: grpc.aio.ServicerContext[yhchat_pb2.SendRequest, yhchat_pb2.SendReply],
    ) -> yhchat_pb2.SendReply:
        async with _grpc_errors(context):
            info = await self._client.bot.message.send(
                request.recv_type,
                request.recv_id,
                segment_from_content(request.content),
                parent_id=_none_if_empty(request.parent_id),
            )
        return yhchat_pb2.SendReply(message=message_info_to_proto(info))

    async def BatchSend(
        self,
        request: yhchat_pb2.BatchSendRequest,
        context: grpc.aio.ServicerContext[yhchat_pb2.BatchSendRequest, yhchat_pb2.BatchSendReply],
    ) -> yhchat_pb2.BatchSendReply:
        async with _grpc_errors(context):
            result = await self._client.bot.message.batch_send(
                request.recv_ids,
                request.recv_type,
                segment_from_content(request.content),
                parent_id=_none_if_empty(request.parent_id),
            )
        return yhchat_pb2.BatchSendReply(
            success_count=result.success_count,
            success_list=[message_info_to_proto(info) for info in result.success_list],
        )

    async def SendStream(
        self,
        request_iterator: AsyncIterator[yhchat_pb2.SendStreamRequest],
        context: grpc.aio.ServicerContext[yhchat_pb2.SendStreamRequest, yhchat_pb2.SendReply],
    ) -> yhchat_pb2.SendReply:
        async with _grpc_errors(context):
            try:
                first = await anext(request_iterator)
            except StopAsyncIteration:
                raise TransportError("SendStream 至少需要一块数据") from None

            message_type = _stream_content_type(first.content_type)

            async def chunks() -> AsyncIterator[str]:
                yield first.chunk.decode()
                async for request in request_iterator:
                    yield request.chunk.decode()

            info = await self._client.bot.message.send_stream(
                first.recv_type,
                first.recv_id,
                message_type,
                chunks(),
            )
        return yhchat_pb2.SendReply(message=message_info_to_proto(info))

    async def Edit(
        self,
        request: yhchat_pb2.EditRequest,
        context: grpc.aio.ServicerContext[yhchat_pb2.EditRequest, yhchat_pb2.EditReply],
    ) -> yhchat_pb2.EditReply:
        async with _grpc_errors(context):
            count = await self._client.bot.message.edit(
                request.msg_id,
                segment_from_content(request.content),
                recv_id=_none_if_empty(request.recv_id),
                recv_type=_none_if_empty(request.recv_type),
            )
        return yhchat_pb2.EditReply(success_count=count)

    async def Recall(
        self,
        request: yhchat_pb2.RecallRequest,
        context: grpc.aio.ServicerContext[yhchat_pb2.RecallRequest, yhchat_pb2.RecallReply],
    ) -> yhchat_pb2.RecallReply:
        async with _grpc_errors(context):
            await self._client.bot.message.recall(
                request.msg_id,
                chat_id=_none_if_empty(request.chat_id),
                chat_type=_none_if_empty(request.chat_type),
            )
        return yhchat_pb2.RecallReply()

    async def ListMessages(
        self,
        request: yhchat_pb2.ListMessagesRequest,
        context: grpc.aio.ServicerContext[yhchat_pb2.ListMessagesRequest, yhchat_pb2.ListMessagesReply],
    ) -> yhchat_pb2.ListMessagesReply:
        async with _grpc_errors(context):
            page = await self._client.bot.message.list(
                request.chat_id,
                request.chat_type,
                message_id=_none_if_empty(request.message_id),
                before=request.before,
                after=request.after,
            )
        return yhchat_pb2.ListMessagesReply(
            messages=[received_message_to_proto(message) for message in page.messages],
            total=page.total,
        )

    async def Upload(
        self,
        request: yhchat_pb2.UploadRequest,
        context: grpc.aio.ServicerContext[yhchat_pb2.UploadRequest, yhchat_pb2.UploadReply],
    ) -> yhchat_pb2.UploadReply:
        async with _grpc_errors(context):
            key = await self._upload(request)
        return yhchat_pb2.UploadReply(key=key)

    async def _upload(self, request: yhchat_pb2.UploadRequest) -> str:
        filename = request.filename or None
        mime_type = _none_if_empty(request.mime_type)
        match request.kind:
            case yhchat_pb2.UploadRequest.KIND_IMAGE:
                return await self._client.bot.upload.image(
                    request.data, filename=filename or "image.png", mime_type=mime_type
                )
            case yhchat_pb2.UploadRequest.KIND_VIDEO:
                return await self._client.bot.upload.video(
                    request.data, filename=filename or "video.mp4", mime_type=mime_type
                )
            case yhchat_pb2.UploadRequest.KIND_FILE:
                return await self._client.bot.upload.file(
                    request.data, filename=filename or "file.bin", mime_type=mime_type
                )
            case _:
                raise TransportError(f"未知的上传类型: {request.kind}")


async def serve(
    client: YHChatClient,
    *,
    host: str = "127.0.0.1",
    port: int = 50051,
) -> tuple[grpc.aio.Server, int]:
    """启动 gRPC 服务，返回 ``(server, 实际端口)``；``port=0`` 时由系统分配。"""
    server = grpc.aio.server()
    _ADD_SERVICER(YHChatServicer(client), server)
    bound_port = server.add_insecure_port(f"{host}:{port}")
    if bound_port == 0:
        raise TransportError(f"gRPC 端口绑定失败: {host}:{port}")
    await server.start()
    return server, bound_port


def _none_if_empty(value: str) -> str | None:
    return value or None


def _stream_content_type(value: str) -> Literal["text", "markdown"]:
    if value not in ("text", "markdown"):
        raise TransportError(f"SendStream 只支持 text / markdown，收到 {value!r}")
    return value
