"""``web_group`` 组：由 ``tools/gen_v1_api.py`` 根据 ``web/v1/group.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class WebGroupAPI(V1GroupAPI):
    """``web_group`` 组，共 1 个 JSON 端点。"""

    async def group_info(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取群聊信息。

        ``POST /v1/group/group-info``
        请求字段: groupId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/group-info", body=body)
