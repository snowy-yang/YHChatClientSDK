"""``event`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/event.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class EventAPI(V1GroupAPI):
    """``event`` 组，共 2 个 JSON 端点。"""

    async def list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取机器人事件订阅配置。

        ``POST /v1/event/list``
        请求字段: botId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/event/list", body=body)

    async def edit(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """机器人消息订阅设置。

        ``POST /v1/event/edit``
        请求字段: botId, messageReceiveNormal, messageReceiveInstruction, botFollowed, botUnfollowed, groupJoin, groupLeave, botSetting, typ。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/event/edit", body=body)
