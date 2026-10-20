"""``file`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/file.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class FileAPI(V1GroupAPI):
    """``file`` 组，共 3 个 JSON 端点。"""

    async def send(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """发送超级文件分享申请。

        ``POST /v1/file/send``
        请求字段: userId, deviceId, fileData。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/file/send", body=body)

    async def reply(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """拒绝超级文件分享。

        ``POST /v1/file/reply``
        请求字段: deviceId, isAccept, userId, fileData。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/file/reply", body=body)

    async def offer(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """建立超级文件分享。

        ``POST /v1/file/offer``
        请求字段: deviceId, description, userId, sessionId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/file/offer", body=body)
