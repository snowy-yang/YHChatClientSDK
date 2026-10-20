"""``verification`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/verification.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class VerificationAPI(V1GroupAPI):
    """``verification`` 组，共 2 个 JSON 端点。"""

    async def get_verification_code(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取短信验证码。

        ``POST /v1/verification/get-verification-code``
        请求字段: mobile, code, captcha_type, id, x, platform。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/verification/get-verification-code", body=body)

    async def get_email_verification_code(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取邮箱验证码。

        ``POST /v1/verification/get-email-verification-code``
        请求字段: email, typ, code, id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/verification/get-email-verification-code", body=body)
