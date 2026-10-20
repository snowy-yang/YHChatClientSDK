"""``web_community`` 组：由 ``tools/gen_v1_api.py`` 根据 ``web/v1/community.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class WebCommunityAPI(V1GroupAPI):
    """``web_community`` 组，共 2 个 JSON 端点。"""

    async def c_following_ba_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取分区列表。

        ``POST /v1/community/c/following-ba-list``
        请求字段: size, page。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/c/following-ba-list", body=body)

    async def c_info(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取分区信息。

        ``POST /v1/community/c/info``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/community/c/info", body=body)
