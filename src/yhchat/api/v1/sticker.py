"""``sticker`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/sticker.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class StickerAPI(V1GroupAPI):
    """``sticker`` 组，共 12 个 JSON 端点。"""

    async def list(self) -> dict[str, Any]:
        """获取收藏表情包。

        ``POST /v1/sticker/list``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticker/list")

    async def detail(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """查看表情包详情。

        ``POST /v1/sticker/detail``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticker/detail", body=body)

    async def add(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """添加表情包。

        ``POST /v1/sticker/add``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticker/add", body=body)

    async def remove_sticker_pack(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """移除收藏表情包。

        ``POST /v1/sticker/remove-sticker-pack``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticker/remove-sticker-pack", body=body)

    async def sort(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """更改收藏表情包的排序。

        ``POST /v1/sticker/sort``
        请求字段: sort。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticker/sort", body=body)

    async def create_pack(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """创建表情包。

        ``POST /v1/sticker/create-pack``
        请求字段: name。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticker/create-pack", body=body)

    async def rename_pack(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """重命名表情包。

        ``POST /v1/sticker/rename-pack``
        请求字段: id, name。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticker/rename-pack", body=body)

    async def add_sticker(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """添加表情至表情包。

        ``POST /v1/sticker/add-sticker``
        请求字段: name, url, stickerPackId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticker/add-sticker", body=body)

    async def delete_pack(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除表情包。

        ``POST /v1/sticker/delete-pack``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticker/delete-pack", body=body)

    async def import_pack(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """导入表情包。

        ``POST /v1/sticker/import-pack``
        请求字段: name, fileKey。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticker/import-pack", body=body)

    async def rename_sticker(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """重命名表情包里的表情。

        ``POST /v1/sticker/rename-sticker``
        请求字段: id, name。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticker/rename-sticker", body=body)

    async def remove_sticker(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除表情。

        ``POST /v1/sticker/remove-sticker``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/sticker/remove-sticker", body=body)
