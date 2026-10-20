"""``captcha`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/captcha.md`` 生成，勿手改。"""

from typing import Any

from ._base import V1GroupAPI


class CaptchaAPI(V1GroupAPI):
    """``captcha`` 组，共 1 个 JSON 端点。"""

    async def get(self) -> dict[str, Any]:
        """获取滑动验证码。

        ``POST /v1/captcha/get``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/captcha/get")
