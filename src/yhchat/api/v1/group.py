"""``group`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/group.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class GroupAPI(V1GroupAPI):
    """``group`` 组，共 18 个 JSON 端点。"""

    async def live_room(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取群聊语音房间。

        ``POST /v1/group/live-room``
        请求字段: groupId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/live-room", body=body)

    async def instruction_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取群指令列表。

        ``POST /v1/group/instruction-list``
        请求字段: groupId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/instruction-list", body=body)

    async def invite(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """邀请加入群聊。

        ``POST /v1/group/invite``
        请求字段: chatId, chatType, groupId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/invite", body=body)

    async def remove_member(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """踢出用户。

        ``POST /v1/group/remove-member``
        请求字段: groupId, userId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/remove-member", body=body)

    async def gag_member(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """禁言用户。

        ``POST /v1/group/gag-member``
        请求字段: groupId, userId, gag。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/gag-member", body=body)

    async def category(self) -> dict[str, Any]:
        """获取群聊推荐分类。

        ``GET /v1/group/category``
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/group/category")

    async def recommend_list(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """搜索推荐群聊。

        ``POST /v1/group/recommend/list``
        请求字段: categoryId, keyword。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/recommend/list", body=body)

    async def msg_type_limit(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """设置消息类型限制。

        ``POST /v1/group/msg-type-limit``
        请求字段: groupId, type。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/msg-type-limit", body=body)

    async def remove_bot(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """移除群聊内机器人。

        ``POST /v1/group/remove-bot``
        请求字段: groupId, botId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/remove-bot", body=body)

    async def edit_my_group_nickname(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """设置我的群昵称。

        ``POST /v1/group/edit-my-group-nickname``
        请求字段: groupId, nickname。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/edit-my-group-nickname", body=body)

    async def edit_group_keyword(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """设置群口令。

        ``POST /v1/group/edit-group-keyword``
        请求字段: groupId, keyword。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/edit-group-keyword", body=body)

    async def edit_auto_delete_message(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """设置群聊消息自动销毁时间。

        ``POST /v1/group/edit-auto-delete-message``
        请求字段: groupId, autoDeleteMessage。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/edit-auto-delete-message", body=body)

    async def edit_stop_member_upload_group_file(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """设置禁止群成员上传到群云盘。

        ``POST /v1/group/edit-stop-member-upload-group-file``
        请求体见文档。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/edit-stop-member-upload-group-file", body=body)

    async def agree_invite(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """同意进群申请、同意机器人进群。

        ``POST /v1/group/agree-invite``
        请求字段: id, agree。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/agree-invite", body=body)

    async def member_is_removed(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """用户被是否被该群踢过。

        ``POST /v1/group/member-is-removed``
        请求字段: userId, groupId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/member-is-removed", body=body)

    async def switch(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """加入群推荐。

        ``POST /v1/group/switch``
        请求字段: groupId, hide。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/switch", body=body)

    async def event_sse(self, *, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """连接群聊 SSE。

        ``GET /v1/group/event-sse``
        查询参数: ``groupId=`<groupId>```。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("GET", "/v1/group/event-sse", params=params)

    async def edit_shop_entry(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """编辑商城入口状态。

        ``POST /v1/group/edit-shop-entry``
        请求字段: groupId, entryPosition。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/group/edit-shop-entry", body=body)
