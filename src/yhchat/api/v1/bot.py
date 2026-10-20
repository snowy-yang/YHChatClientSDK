"""``bot`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/bot.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class BotAPI(V1GroupAPI):
    """``bot`` 组，共 21 个 JSON 端点。"""

    async def banner(self) -> dict[str, Any]:
        """机器人商店banner。

        ``POST /v1/bot/banner``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/banner")

    async def new_list(self) -> dict[str, Any]:
        """机器人商店列表。

        ``POST /v1/bot/new-list``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/new-list")

    async def bot_detail(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """使用该机器人的群组。

        ``POST /v1/bot/bot-detail``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/bot-detail", body=body)

    async def bot_group_list(self) -> dict[str, Any]:
        """获取创建的所有机器人信息。

        ``POST /v1/bot/bot-group-list``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/bot-group-list")

    async def edit_setting_json(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """更改机器人设置。

        ``POST /v1/bot/edit-setting-json``
        请求字段: id, settingJson。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/edit-setting-json", body=body)

    async def web_edit_bot(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """更改机器人信息。

        ``POST /v1/bot/web-edit-bot``
        请求字段: nickname, introduction, avatarUrl, botId, private。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/web-edit-bot", body=body)

    async def remove_follower(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除用户对机器人的添加。

        ``POST /v1/bot/remove-follower``
        请求字段: botId, userId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/remove-follower", body=body)

    async def remove_group(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除群聊对机器人的添加。

        ``POST /v1/bot/remove-group``
        请求字段: botId, groupId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/remove-group", body=body)

    async def llm_llm_setting_list(self) -> dict[str, Any]:
        """获取可用AI模型列表。

        ``POST /v1/bot/llm/llm-setting-list``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/llm/llm-setting-list")

    async def llm_llm_setting_ref_info(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取机器人大模型设置。

        ``POST /v1/bot/llm/llm-setting-ref-info``
        请求字段: botId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/llm/llm-setting-ref-info", body=body)

    async def reset_bot_token(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """重置机器人token。

        ``POST /v1/bot/reset-bot-token``
        请求字段: botId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/reset-bot-token", body=body)

    async def edit_subscribed_link(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """设置机器人消息订阅接口。

        ``POST /v1/bot/edit-subscribed-link``
        请求字段: botId, link, subscribeType。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/edit-subscribed-link", body=body)

    async def get_user_settings_json(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取群聊内机器人设置。

        ``POST /v1/bot/get-user-settings-json``
        请求字段: botId, chatId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/get-user-settings-json", body=body)

    async def send_setting_json(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """群聊内机器人设置保存。

        ``POST /v1/bot/send-setting-json``
        请求字段: id, groupId, settingJson。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/send-setting-json", body=body)

    async def llm_clean_content(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """智能体机器人清除上下文。

        ``POST /v1/bot/llm/clean-content``
        请求字段: botId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/llm/clean-content", body=body)

    async def llm_knowledge_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取智能体机器人知识库。

        ``POST /v1/bot/llm/knowledge/list``
        请求字段: botId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/llm/knowledge/list", body=body)

    async def llm_knowledge_create(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """智能体机器人上传知识文件。

        ``POST /v1/bot/llm/knowledge/create``
        请求字段: botId, knowledgeId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/llm/knowledge/create", body=body)

    async def console_my_bots(self) -> dict[str, Any]:
        """获取我创建的机器人。

        ``POST /v1/bot/console/my-bots``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/console/my-bots")

    async def group_permission_get(self) -> dict[str, Any]:
        """获取群机器人权限列表。

        ``POST /v1/bot/group-permission-get``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/group-permission-get")

    async def llm_llm_setting_ref_params(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取智能体机器人参数参考。

        ``POST /v1/bot/llm/llm-setting-ref-params``
        请求字段: chatId, chatType。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/llm/llm-setting-ref-params", body=body)

    async def group_permission_edit(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """更改群机器人权限。

        ``POST /v1/bot/group-permission-edit``
        请求字段: botId, groupId, allowEditGroupInfo, allowGagMember, allowRemoveMember, allowGroupTagManage。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/bot/group-permission-edit", body=body)
