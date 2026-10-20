"""``chat-background`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/chat-background.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class ChatBackgroundAPI(V1GroupAPI):
    """``chat-background`` 组，共 2 个 JSON 端点。"""

    async def edit(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """设置聊天背景。

        ``POST /v1/chat-background/edit``
        请求字段: userId, chatId, url。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/chat-background/edit", body=body)

    async def list(self) -> dict[str, Any]:
        """获取背景设置列表。

        ``POST /v1/chat-background/list``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/chat-background/list")
