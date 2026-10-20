"""``vip`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/vip.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class VipAPI(V1GroupAPI):
    """``vip`` 组，共 2 个 JSON 端点。"""

    async def vip_product_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """vip价格获取。

        ``POST /v1/vip/vip-product-list``
        请求字段: platform。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/vip/vip-product-list", body=body)

    async def vip_benefits_list(self) -> dict[str, Any]:
        """vip特权获取。

        ``GET /v1/vip/vip-benefits-list``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/vip/vip-benefits-list")
