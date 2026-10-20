"""``web_common`` 组：由 ``tools/gen_v1_api.py`` 根据 ``web/v1/common.md`` 生成，勿手改。"""

from typing import Any

from ._base import V1GroupAPI


class WebCommonAPI(V1GroupAPI):
    """``web_common`` 组，共 1 个 JSON 端点。"""

    async def get_version(self) -> dict[str, Any]:
        """获取全平台最新版本。

        ``GET /v1/common/get-version``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/common/get-version")
