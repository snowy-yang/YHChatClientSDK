"""``share`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/share.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class ShareAPI(V1GroupAPI):
    """``share`` 组，共 2 个 JSON 端点。"""

    async def info(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """分享链接获取群聊信息。

        ``POST /v1/share/info``
        请求字段: key, ts。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/share/info", body=body)

    async def create(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """创建分享链接。

        ``POST /v1/share/create``
        请求字段: chatId, chatType, chatName。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/share/create", body=body)
