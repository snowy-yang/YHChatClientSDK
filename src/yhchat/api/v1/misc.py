"""``misc`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/misc.md`` 生成，勿手改。"""

from typing import Any

from ._base import V1GroupAPI


class MiscAPI(V1GroupAPI):
    """``misc`` 组，共 8 个 JSON 端点。"""

    async def configure_distribution(self) -> dict[str, Any]:
        """获取功能路由。

        ``GET /v1/misc/configure-distribution``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/misc/configure-distribution")

    async def qiniu_token(self) -> dict[str, Any]:
        """获取图片上传 token。

        ``GET /v1/misc/qiniu-token``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/misc/qiniu-token")

    async def qiniu_token_audio(self) -> dict[str, Any]:
        """获取音频上传 token。

        ``GET /v1/misc/qiniu-token-audio``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/misc/qiniu-token-audio")

    async def qiniu_token2(self) -> dict[str, Any]:
        """获取文件上传 token。

        ``GET /v1/misc/qiniu-token2``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/misc/qiniu-token2")

    async def qiniu_token_video(self) -> dict[str, Any]:
        """获取视频上传token。

        ``GET /v1/misc/qiniu-token-video``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/misc/qiniu-token-video")

    async def qiniu_token_group_disk(self) -> dict[str, Any]:
        """获取群文件上传 token。

        ``GET /v1/misc/qiniu-token-group-disk``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/misc/qiniu-token-group-disk")

    async def setting(self) -> dict[str, Any]:
        """获取云端设置。

        ``GET /v1/misc/setting``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/misc/setting")

    async def gray_status(self) -> dict[str, Any]:
        """获取灰色状态。

        ``GET /v1/misc/gray-status``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/misc/gray-status")
