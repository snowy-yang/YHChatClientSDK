"""``beta`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/beta.md`` 生成，勿手改。"""

from typing import Any

from ._base import V1GroupAPI


class BetaAPI(V1GroupAPI):
    """``beta`` 组，共 1 个 JSON 端点。"""

    async def info(self) -> dict[str, Any]:
        """获取内测状态。

        ``POST /v1/beta/info``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/beta/info")
