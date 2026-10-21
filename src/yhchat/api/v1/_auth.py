"""用户账号登录封装（``client.auth``）。

文档事实（``v1/user.md`` / ``wss/chat-ws-go.jwzhd.com.md``）：

- ``deviceId``："登录设备唯一标识符，可自定义"（WS 文档写"可随便写"），默认随机生成；
- HTTP 登录的 ``platform``："可自定义,不校验"；但 **WS 登录**要求 ``windows`` / ``macos`` /
  ``android`` 等固定值且大小写敏感，所以默认填 ``windows``，登录后能直接拿去连 WS；
- 登录响应只有 ``{"code": 1, "data": {"token": ...}}``，文档没给过期时间；
- ``logout`` 的请求体字段名是 ``device-id``（带连字符），且 token 要放请求头。

登录端点**不需要 token**，所以这些方法挂在 ``client.auth``（``auth="none"`` 的连接池）上，
和需要用户 token 的 ``client.v1`` 分开。
"""

import secrets
from dataclasses import dataclass
from typing import Any, cast

from ...errors import YHChatError
from ._base import V1GroupAPI

DEFAULT_PLATFORM = "windows"
"""默认平台：HTTP 登录不校验，WS 登录要求固定值且大小写敏感，windows 两边都能用。"""


@dataclass(frozen=True, slots=True)
class LoginSession:
    """登录结果；``device_id`` 要留着，退出登录/下线设备时用同一个。"""

    token: str
    device_id: str
    platform: str


def new_device_id() -> str:
    """生成登录用的设备 ID（文档允许自定义，用随机值区分设备）。"""
    return secrets.token_hex(8)


class AuthAPI(V1GroupAPI):
    """``client.auth``：用户账号登录、退出。"""

    async def captcha(self) -> dict[str, Any]:
        """获取人机验证图片。``POST /v1/user/captcha``（返回原始 JSON）"""
        return await self._call("POST", "/v1/user/captcha")

    async def login_with_verification(
        self,
        mobile: str,
        captcha: str,
        *,
        device_id: str | None = None,
        platform: str = DEFAULT_PLATFORM,
    ) -> LoginSession:
        """短信验证码登录。``POST /v1/user/verification-login``"""
        device = device_id or new_device_id()
        response = await self._call(
            "POST",
            "/v1/user/verification-login",
            body={"mobile": mobile, "captcha": captcha, "deviceId": device, "platform": platform},
        )
        return _session_of(response, device_id=device, platform=platform, endpoint="/v1/user/verification-login")

    async def login_with_email(
        self,
        email: str,
        password: str,
        *,
        device_id: str | None = None,
        platform: str = DEFAULT_PLATFORM,
    ) -> LoginSession:
        """邮箱密码登录。``POST /v1/user/email-login``

        :param password: 文档示例是明文密码，SDK 不做哈希/加密，原样提交。
        """
        device = device_id or new_device_id()
        response = await self._call(
            "POST",
            "/v1/user/email-login",
            body={"email": email, "password": password, "deviceId": device, "platform": platform},
        )
        return _session_of(response, device_id=device, platform=platform, endpoint="/v1/user/email-login")

    async def logout(self, session: LoginSession) -> None:
        """退出登录。``POST /v1/user/logout``（请求体是 ``device-id``，token 走请求头）"""
        await self._http.request(
            "POST",
            "/v1/user/logout",
            json={"device-id": session.device_id},
            headers={"token": session.token},
        )


def _session_of(response: dict[str, Any], *, device_id: str, platform: str, endpoint: str) -> LoginSession:
    """从登录响应里取 token；缺失时明确报错，不返回空 token。"""
    data = response.get("data")
    token = cast("dict[str, Any]", data).get("token") if isinstance(data, dict) else None
    if not isinstance(token, str) or not token:
        raise YHChatError(f"{endpoint} 的响应里没有 token: {response}")
    return LoginSession(token=token, device_id=device_id, platform=platform)
