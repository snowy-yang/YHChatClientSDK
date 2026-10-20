"""``web_rss`` 组：由 ``tools/gen_v1_api.py`` 根据 ``web/v1/rss.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class WebRssAPI(V1GroupAPI):
    """``web_rss`` 组，共 2 个 JSON 端点。"""

    async def recommend_list(self) -> dict[str, Any]:
        """获取 RSS 推荐大全。

        ``GET /v1/rss/recommend-list``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/rss/recommend-list")

    async def recommend_apply(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """提交 RSS。

        ``POST /v1/rss/recommend-apply``
        请求字段: title, rssUrl, siteUrl, description。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/rss/recommend-apply", body=body)
