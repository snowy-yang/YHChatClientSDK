"""JSON/protobuf 之外的杂项端点（手写）。

目前只有 ``/v1/misc/auto-update``：它返回 Sparkle appcast XML，不是 JSON 也不是 protobuf。
"""

from typing import Any

from ...transport import HttpTransport

EXTRA_ENDPOINTS: frozenset[str] = frozenset({"/v1/misc/auto-update"})
"""已经实现的非 JSON/protobuf 端点路径，生成器据此算覆盖率。"""


class V1ExtraAPI:
    """``client.v1.extra``：收发格式不属于 JSON/protobuf 的端点。"""

    def __init__(self, http: HttpTransport) -> None:
        self._http = http

    async def auto_update(self, *, platform: str, user_id: str | None = None) -> str:
        """检查客户端更新，返回 appcast XML 原文。``GET /v1/misc/auto-update``

        :param platform: ``windows`` / ``android`` / ``macos`` / ``ios``。
        :param user_id: 可选，文档里的 ``userId`` 查询参数。
        """
        params: dict[str, Any] = {"platform": platform}
        if user_id is not None:
            params["userId"] = user_id
        return await self._http.request_text("GET", "/v1/misc/auto-update", params=params)
