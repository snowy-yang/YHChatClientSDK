"""``menu`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/menu.md`` 生成，勿手改。"""

from typing import Any

from ._base import V1GroupAPI


class MenuAPI(V1GroupAPI):
    """``menu`` 组，共 1 个 JSON 端点。"""

    async def event(self) -> dict[str, Any]:
        """触发快捷菜单事件。

        ``POST /v1/menu/event``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/menu/event")
