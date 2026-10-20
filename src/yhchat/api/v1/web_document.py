"""``web_document`` 组：由 ``tools/gen_v1_api.py`` 根据 ``web/v1/document.md`` 生成，勿手改。"""

from typing import Any

from ._base import V1GroupAPI


class WebDocumentAPI(V1GroupAPI):
    """``web_document`` 组，共 2 个 JSON 端点。"""

    async def menus(self) -> dict[str, Any]:
        """获取开放文档菜单选项。

        ``GET /v1/document/menus``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/document/menus")

    async def detail(self) -> dict[str, Any]:
        """获取开放文档(Markdown版本)。

        ``GET /v1/document/detail``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/document/detail")
