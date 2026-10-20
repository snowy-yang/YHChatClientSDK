"""``report`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/report.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class ReportAPI(V1GroupAPI):
    """``report`` 组，共 1 个 JSON 端点。"""

    async def create(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """提交举报。

        ``POST /v1/report/create``
        请求字段: chatId, chatType, chatName, content, url, reason。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/report/create", body=body)
