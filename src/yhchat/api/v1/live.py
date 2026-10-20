"""``live`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/live.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class LiveAPI(V1GroupAPI):
    """``live`` 组，共 7 个 JSON 端点。"""

    async def add(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取语音频道进入 token。

        ``POST /v1/live/add``
        请求字段: roomId, chatId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/live/add", body=body)

    async def close(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """关闭语音频道。

        ``POST /v1/live/close``
        请求字段: roomId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/live/close", body=body)

    async def hang_up(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """挂断语音频道。

        ``POST /v1/live/hang_up``
        请求字段: roomId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/live/hang_up", body=body)

    async def room_info(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取语音频道信息。

        ``POST /v1/live/room-info``
        请求字段: roomId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/live/room-info", body=body)

    async def title_edit(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """编辑语音频道标题。

        ``POST /v1/live/title-edit``
        请求字段: roomId, title。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/live/title-edit", body=body)

    async def get_calling(self) -> dict[str, Any]:
        """获取正在发起的通话。

        ``POST /v1/live/get-calling``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/live/get-calling")

    async def stream_info(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取推流信息。

        ``POST /v1/live/stream-info``
        请求体见文档。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/live/stream-info", body=body)
