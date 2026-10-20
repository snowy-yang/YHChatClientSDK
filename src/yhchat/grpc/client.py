"""gRPC 客户端：用 ``grpc.aio.Channel`` 建强类型多路调用器。

不使用生成的 stub（它没有类型标注），这样 strict 模式下调用点仍然有类型。
"""

from collections.abc import AsyncIterator

import grpc

from ._pb import yhchat_pb2

_SERVICE = "/yhchat.v1.YHChat"


class YHChatRpcClient:
    """``yhchat.v1.YHChat`` 的强类型客户端。"""

    def __init__(self, channel: grpc.aio.Channel) -> None:
        self._send: grpc.aio.UnaryUnaryMultiCallable[yhchat_pb2.SendRequest, yhchat_pb2.SendReply] = (
            channel.unary_unary(
                f"{_SERVICE}/Send",
                request_serializer=yhchat_pb2.SendRequest.SerializeToString,
                response_deserializer=yhchat_pb2.SendReply.FromString,
            )
        )
        self._batch_send: grpc.aio.UnaryUnaryMultiCallable[yhchat_pb2.BatchSendRequest, yhchat_pb2.BatchSendReply] = (
            channel.unary_unary(
                f"{_SERVICE}/BatchSend",
                request_serializer=yhchat_pb2.BatchSendRequest.SerializeToString,
                response_deserializer=yhchat_pb2.BatchSendReply.FromString,
            )
        )
        self._send_stream: grpc.aio.StreamUnaryMultiCallable[yhchat_pb2.SendStreamRequest, yhchat_pb2.SendReply] = (
            channel.stream_unary(
                f"{_SERVICE}/SendStream",
                request_serializer=yhchat_pb2.SendStreamRequest.SerializeToString,
                response_deserializer=yhchat_pb2.SendReply.FromString,
            )
        )
        self._edit: grpc.aio.UnaryUnaryMultiCallable[yhchat_pb2.EditRequest, yhchat_pb2.EditReply] = (
            channel.unary_unary(
                f"{_SERVICE}/Edit",
                request_serializer=yhchat_pb2.EditRequest.SerializeToString,
                response_deserializer=yhchat_pb2.EditReply.FromString,
            )
        )
        self._recall: grpc.aio.UnaryUnaryMultiCallable[yhchat_pb2.RecallRequest, yhchat_pb2.RecallReply] = (
            channel.unary_unary(
                f"{_SERVICE}/Recall",
                request_serializer=yhchat_pb2.RecallRequest.SerializeToString,
                response_deserializer=yhchat_pb2.RecallReply.FromString,
            )
        )
        self._list_messages: grpc.aio.UnaryUnaryMultiCallable[
            yhchat_pb2.ListMessagesRequest, yhchat_pb2.ListMessagesReply
        ] = channel.unary_unary(
            f"{_SERVICE}/ListMessages",
            request_serializer=yhchat_pb2.ListMessagesRequest.SerializeToString,
            response_deserializer=yhchat_pb2.ListMessagesReply.FromString,
        )
        self._upload: grpc.aio.UnaryUnaryMultiCallable[yhchat_pb2.UploadRequest, yhchat_pb2.UploadReply] = (
            channel.unary_unary(
                f"{_SERVICE}/Upload",
                request_serializer=yhchat_pb2.UploadRequest.SerializeToString,
                response_deserializer=yhchat_pb2.UploadReply.FromString,
            )
        )

    async def send(self, request: yhchat_pb2.SendRequest, *, timeout: float | None = None) -> yhchat_pb2.SendReply:
        """发送一条消息。"""
        return await self._send(request, timeout=timeout)

    async def batch_send(
        self, request: yhchat_pb2.BatchSendRequest, *, timeout: float | None = None
    ) -> yhchat_pb2.BatchSendReply:
        """批量发送。"""
        return await self._batch_send(request, timeout=timeout)

    async def send_stream(
        self,
        requests: AsyncIterator[yhchat_pb2.SendStreamRequest],
        *,
        timeout: float | None = None,
    ) -> yhchat_pb2.SendReply:
        """流式发送：传入 ``SendStreamRequest`` 的异步迭代器。"""
        return await self._send_stream(requests, timeout=timeout)

    async def edit(self, request: yhchat_pb2.EditRequest, *, timeout: float | None = None) -> yhchat_pb2.EditReply:
        """编辑消息。"""
        return await self._edit(request, timeout=timeout)

    async def recall(
        self, request: yhchat_pb2.RecallRequest, *, timeout: float | None = None
    ) -> yhchat_pb2.RecallReply:
        """撤回消息。"""
        return await self._recall(request, timeout=timeout)

    async def list_messages(
        self, request: yhchat_pb2.ListMessagesRequest, *, timeout: float | None = None
    ) -> yhchat_pb2.ListMessagesReply:
        """拉取消息列表。"""
        return await self._list_messages(request, timeout=timeout)

    async def upload(
        self, request: yhchat_pb2.UploadRequest, *, timeout: float | None = None
    ) -> yhchat_pb2.UploadReply:
        """上传文件，返回 key。"""
        return await self._upload(request, timeout=timeout)
