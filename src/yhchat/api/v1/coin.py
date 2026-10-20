"""``coin`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/coin.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class CoinAPI(V1GroupAPI):
    """``coin`` 组，共 4 个 JSON 端点。"""

    async def shop_product_recommend(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """商品获取。

        ``POST /v1/coin/shop/product-recommend``
        请求字段: size, page。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/coin/shop/product-recommend", body=body)

    async def task_my_task_info(self) -> dict[str, Any]:
        """我的金币任务获取。

        ``POST /v1/coin/task/my-task-info``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/coin/task/my-task-info")

    async def shop_product_detail(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取商品详情。

        ``POST /v1/coin/shop/product-detail``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/coin/shop/product-detail", body=body)

    async def task_raffle(self) -> dict[str, Any]:
        """让金币机器人给你发领金币信息。

        ``POST /v1/coin/task/raffle``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/coin/task/raffle")
