"""``web_misc`` 组：由 ``tools/gen_v1_api.py`` 根据 ``web/v1/misc.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class WebMiscAPI(V1GroupAPI):
    """``web_misc`` 组，共 1 个 JSON 端点。"""

    async def updates(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取更新日志。

        ``POST /v1/misc/updates``
        请求字段: platform, size, page。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/misc/updates", body=body)
