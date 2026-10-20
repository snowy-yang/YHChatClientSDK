"""``check`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/check.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class CheckAPI(V1GroupAPI):
    """``check`` 组，共 3 个 JSON 端点。"""

    async def check_version_mobile(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取云湖新版本（Android 版本）。

        ``POST /v1/check/check-version-mobile``
        请求体见文档。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/check/check-version-mobile", body=body)

    async def get_latest_version(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取云湖新版本（Android 版本）。

        ``POST /v1/check/get-latest-version``
        请求体见文档。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/check/get-latest-version", body=body)

    async def check_version(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取云湖新版本（Windows 版本）。

        ``POST /v1/check/check-version``
        请求字段: packageInfo, platform, deviceinfo, deviceId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/check/check-version", body=body)
