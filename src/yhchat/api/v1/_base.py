"""``v1/*`` 分组的公共基类：由 ``tools/gen_v1_api.py`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ...transport import HttpTransport


class V1GroupAPI:
    """一组 ``v1/*`` 端点：请求带着 header 里的用户 token。"""

    def __init__(self, http: HttpTransport) -> None:
        self._http = http

    async def _call(
        self,
        method: str,
        path: str,
        *,
        body: Mapping[str, Any] | None = None,
        params: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """发请求并原样返回响应体（含 ``code`` / ``msg`` / ``data``）。"""
        return await self._http.request(method, path, json=body, params=params)
