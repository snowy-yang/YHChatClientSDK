"""``disk`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/disk.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class DiskAPI(V1GroupAPI):
    """``disk`` 组，共 6 个 JSON 端点。"""

    async def create_folder(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """创建群网盘文件夹。

        ``POST /v1/disk/create-folder``
        请求字段: chatId, chatType, folderName, parentFolderId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/disk/create-folder", body=body)

    async def file_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取群网盘文件列表。

        ``POST /v1/disk/file-list``
        请求字段: chatId, chatType, folderId, sort。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/disk/file-list", body=body)

    async def file_size(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取群网盘文件总大小。

        ``POST /v1/disk/file-size``
        请求字段: chatId, chatType。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/disk/file-size", body=body)

    async def upload_file(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """上传文件。

        ``POST /v1/disk/upload-file``
        请求字段: chatId, chatType, fileSize, fileName, fileMd5, fileEtag, qiniuKey, folderId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/disk/upload-file", body=body)

    async def rename(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """更改文件名。

        ``POST /v1/disk/rename``
        请求字段: id, objectType, name。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/disk/rename", body=body)

    async def remove(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除文件。

        ``POST /v1/disk/remove``
        请求字段: id, objectType。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/disk/remove", body=body)
