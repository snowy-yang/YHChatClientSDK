"""``friend`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/friend.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class FriendAPI(V1GroupAPI):
    """``friend`` 组，共 6 个 JSON 端点。"""

    async def apply(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """添加用户/群聊/机器人。

        ``POST /v1/friend/apply``
        请求字段: chatId, chatType, remark。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/friend/apply", body=body)

    async def delete_friend(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除用户/群聊/机器人。

        ``POST /v1/friend/delete-friend``
        请求字段: chatId, chatType。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/friend/delete-friend", body=body)

    async def agree_apply(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """处理用户/群聊/机器人添加申请。

        ``POST /v1/friend/agree-apply``
        请求字段: id, agree。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/friend/agree-apply", body=body)

    async def ignore_apply(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """忽略申请。

        ``POST /v1/friend/ignore-apply``
        请求字段: id, ignore。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/friend/ignore-apply", body=body)

    async def no_notify(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """设置会话免打扰。

        ``POST /v1/friend/no-notify``
        请求字段: chatId, noNotify。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/friend/no-notify", body=body)

    async def delete_request(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除好友/邀请请求。

        ``POST /v1/friend/delete-request``
        请求字段: id。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/friend/delete-request", body=body)
