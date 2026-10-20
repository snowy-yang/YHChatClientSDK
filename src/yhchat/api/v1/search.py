"""``search`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/search.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class SearchAPI(V1GroupAPI):
    """``search`` 组，共 2 个 JSON 端点。"""

    async def home_search(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """群聊首页搜索。

        ``POST /v1/search/home-search``
        请求字段: word。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/search/home-search", body=body)

    async def chat_search(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """聊天记录搜索。

        ``POST /v1/search/chat-search``
        请求字段: word, chatId, chatType, type, size, time, direction。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/search/chat-search", body=body)
