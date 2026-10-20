"""``web_bot`` 组：由 ``tools/gen_v1_api.py`` 根据 ``web/v1/bot.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class WebBotAPI(V1GroupAPI):
    """``web_bot`` 组，共 2 个 JSON 端点。"""

    async def bot_info(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取机器人信息。

        ``POST /v1/bot/bot-info``
        请求字段: botId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/bot-info", body=body)

    async def bot_link_reset(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """恢复机器人订阅。

        ``POST /v1/bot/bot-link-reset``
        请求字段: botId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/bot-link-reset", body=body)
