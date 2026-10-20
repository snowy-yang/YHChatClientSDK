"""``expression`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/expression.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class ExpressionAPI(V1GroupAPI):
    """``expression`` 组，共 5 个 JSON 端点。"""

    async def list(self) -> dict[str, Any]:
        """获取个人表情收藏。

        ``POST /v1/expression/list``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/expression/list")

    async def create(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """添加图片到个人表情收藏。

        ``POST /v1/expression/create``
        请求字段: url。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/expression/create", body=body)

    async def delete(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除个人表情收藏中的表情。

        ``POST /v1/expression/delete``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/expression/delete", body=body)

    async def topping(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """置顶个人表情收藏中的表情。

        ``POST /v1/expression/topping``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/expression/topping", body=body)

    async def add(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """添加已有表情包。

        ``POST /v1/expression/add``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/expression/add", body=body)
