"""``instruction`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/instruction.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class InstructionAPI(V1GroupAPI):
    """``instruction`` 组，共 3 个 JSON 端点。"""

    async def web_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取机器人指令列表（网页控制台）。

        ``POST /v1/instruction/web-list``
        请求字段: botId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/instruction/web-list", body=body)

    async def create(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """创建机器人指令。

        ``POST /v1/instruction/create``
        请求字段: name, desc, hintText, defaultText, type, botId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/instruction/create", body=body)

    async def edit(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """编辑机器人指令。

        ``POST /v1/instruction/edit``
        请求字段: id, name, desc, botId, customJson, type, delFlag。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/instruction/edit", body=body)
