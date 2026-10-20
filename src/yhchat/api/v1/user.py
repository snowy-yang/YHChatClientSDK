"""``user`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/user.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class UserAPI(V1GroupAPI):
    """``user`` 组，共 23 个 JSON 端点。"""

    async def captcha(self) -> dict[str, Any]:
        """获取人机验证图片。

        ``POST /v1/user/captcha``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/captcha")

    async def verification_login(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """短信验证码登录。

        ``POST /v1/user/verification-login``
        请求字段: mobile, captcha, deviceId, platform。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/verification-login", body=body)

    async def email_login(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """用户邮箱密码登录。

        ``POST /v1/user/email-login``
        请求字段: email, password, deviceId, platform。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/email-login", body=body)

    async def logout(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """退出登录。

        ``POST /v1/user/logout``
        请求体见文档。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/logout", body=body)

    async def recommend_category_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取发现群聊分区。

        ``POST /v1/user/recommend-category-list``
        请求体见文档。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/recommend-category-list", body=body)

    async def recommend_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取发现群聊列表。

        ``POST /v1/user/recommend-list``
        请求字段: category, keyword, size, page。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/recommend-list", body=body)

    async def recommend(self) -> dict[str, Any]:
        """获取机器人推荐列表。

        ``POST /v1/user/recommend``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/recommend")

    async def module_ignore_info(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """模块忽略信息获取。

        ``POST /v1/user/module-ignore-info``
        请求体见文档。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/module-ignore-info", body=body)

    async def module_ignore(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """设置自定义模块。

        ``POST /v1/user/module-ignore``
        请求体见文档。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/module-ignore", body=body)

    async def notification_status(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取通知状态。

        ``POST /v1/user/notification-status``
        请求字段: deviceId, registrationId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/notification-status", body=body)

    async def notification_info(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取通知注册信息。

        ``POST /v1/user/notification-info``
        请求字段: deviceId, registrationId, isOpen, type。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/notification-info", body=body)

    async def gold_coin_increase_decrease_record(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """金币增减记录。

        ``POST /v1/user/gold-coin-increase-decrease-record``
        请求字段: size, page。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/gold-coin-increase-decrease-record", body=body)

    async def bing_phone(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """绑定手机号。

        ``POST /v1/user/bing-phone``
        请求字段: phone, captcha。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/bing-phone", body=body)

    async def bing_email(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """绑定邮箱。

        ``POST /v1/user/bing-email``
        请求字段: email, captcha。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/bing-email", body=body)

    async def change_phone_check(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """更改绑定手机号。

        ``POST /v1/user/change-phone-check``
        请求字段: phone, captcha。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/change-phone-check", body=body)

    async def change_email_check(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """更改绑定邮箱。

        ``POST /v1/user/change-email-check``
        请求字段: email, captcha。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/change-email-check", body=body)

    async def forget_password(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """更改登录密码。

        ``POST /v1/user/forget-password``
        请求字段: email, captcha, password。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/forget-password", body=body)

    async def save_user_data(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """修改自身个人资料。

        ``POST /v1/user/save-user-data``
        请求字段: introduction, gender, birthday, province, city, district, locationCode。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/save-user-data", body=body)

    async def get_user_data(self) -> dict[str, Any]:
        """获取自身个人资料。

        ``POST /v1/user/get-user-data``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/get-user-data")

    async def get_user_show_adv(self) -> dict[str, Any]:
        """获取用户显示广告。

        ``POST /v1/user/get-user-show-adv``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/get-user-show-adv")

    async def save_user_remarks(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """设置好友备注。

        ``POST /v1/user/save-user-remarks``
        请求字段: friendId, name, phone, others。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/save-user-remarks", body=body)

    async def cancel_user(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """注销账号。

        ``POST /v1/user/cancel-user``
        请求字段: phone, email, captcha。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/cancel-user", body=body)

    async def device_offline(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """下线设备。

        ``POST /v1/user/device-offline``
        请求字段: deviceId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/user/device-offline", body=body)
