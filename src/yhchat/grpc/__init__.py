"""gRPC 门面：只做传输与类型约束，业务逻辑在核心 SDK。

- :class:`YHChatServicer` / :func:`serve`：把 SDK 暴露成 RPC；
- :class:`YHChatRpcClient`：强类型客户端；
- :mod:`yhchat.grpc.convert`：proto 与 SDK 模型的互转。
"""

from .client import YHChatRpcClient
from .convert import content_from_segment, message_info_to_proto, received_message_to_proto, segment_from_content
from .server import YHChatServicer, serve

__all__ = [
    "YHChatRpcClient",
    "YHChatServicer",
    "content_from_segment",
    "message_info_to_proto",
    "received_message_to_proto",
    "segment_from_content",
    "serve",
]
