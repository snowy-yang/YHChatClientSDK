"""``sticky`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/sticky.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class StickyAPI(V1GroupAPI):
    """``sticky`` 组，共 4 个 JSON 端点。"""

    async def list(self) -> dict[str, Any]:
        """首页置顶信息获取。

        ``POST /v1/sticky/list``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticky/list")

    async def add(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """置顶会话。

        ``POST /v1/sticky/add``
        请求字段: chatId, chatType。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticky/add", body=body)

    async def delete(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """取消置顶会话。

        ``POST /v1/sticky/delete``
        请求字段: chatId, chatType。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticky/delete", body=body)

    async def topping(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """把其中一个已置顶会话移到最前。

        ``POST /v1/sticky/topping``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticky/topping", body=body)
