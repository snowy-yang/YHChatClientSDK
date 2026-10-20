"""``group-tag`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/group-tag.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class GroupTagAPI(V1GroupAPI):
    """``group-tag`` 组，共 6 个 JSON 端点。"""

    async def list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取群组标签列表。

        ``POST /v1/group-tag/list``
        请求字段: groupId, size, page, tag。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group-tag/list", body=body)

    async def relate(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """关联用户标签。

        ``POST /v1/group-tag/relate``
        请求字段: userId, tagGroupId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group-tag/relate", body=body)

    async def relate_cancel(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """取消关联用户标签。

        ``POST /v1/group-tag/relate-cancel``
        请求字段: userId, tagGroupId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group-tag/relate-cancel", body=body)

    async def edit(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """编辑群组标签。

        ``POST /v1/group-tag/edit``
        请求字段: id, groupId, tag, color, desc, sort。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group-tag/edit", body=body)

    async def create(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """新增群组标签。

        ``POST /v1/group-tag/create``
        请求字段: groupId, tag, color, desc, sort。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group-tag/create", body=body)

    async def delete(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除群组标签。

        ``POST /v1/group-tag/delete``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group-tag/delete", body=body)
