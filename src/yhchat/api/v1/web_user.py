"""``web_user`` 组：由 ``tools/gen_v1_api.py`` 根据 ``web/v1/user.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class WebUserAPI(V1GroupAPI):
    """``web_user`` 组，共 3 个 JSON 端点。"""

    async def homepage(self, *, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取用户主页信息。

        ``GET /v1/user/homepage``
        查询参数: ``userId={你要查询的用户ID(例如1231230)}``。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/user/homepage", params=params)

    async def get_token(self, *, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """复制用户token。

        ``GET /v1/user/get-token``
        查询参数: ``token={需要复制的用户token}``。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/user/get-token", params=params)

    async def gold_coin_increase_decrease_record(self, *, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """金币增减记录。

        ``GET /v1/user/gold-coin-increase-decrease-record``
        查询参数: ``size=<条数>&page=<页数>``。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/user/gold-coin-increase-decrease-record", params=params)
