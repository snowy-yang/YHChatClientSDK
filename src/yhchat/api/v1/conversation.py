"""``conversation`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/conversation.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class ConversationAPI(V1GroupAPI):
    """``conversation`` 组，共 3 个 JSON 端点。"""

    async def dismiss_notification(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """将对话设为已读。

        ``POST /v1/conversation/dismiss-notification``
        请求体见文档。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/conversation/dismiss-notification", body=body)

    async def sort_change(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """更改对话排序。

        ``POST /v1/conversation/sort-change``
        请求字段: userId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/conversation/sort-change", body=body)

    async def remove(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除对话。

        ``POST /v1/conversation/remove``
        请求字段: chatId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/conversation/remove", body=body)
