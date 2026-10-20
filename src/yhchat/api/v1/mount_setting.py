"""``mount-setting`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/mount-setting.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class MountSettingAPI(V1GroupAPI):
    """``mount-setting`` 组，共 2 个 JSON 端点。"""

    async def create(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """添加群WebDAV挂载。

        ``POST /v1/mount-setting/create``
        请求字段: groupId, mountName, webdavUrl, webdavUserName, webdavPassword, webdavRootPath。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/mount-setting/create", body=body)

    async def delete(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除群WebDAV挂载。

        ``POST /v1/mount-setting/delete``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/mount-setting/delete", body=body)
