"""``msg`` 组：由 ``tools/gen_v1_api.py`` 根据 ``v1/msg.md`` 生成，勿手改。"""

from collections.abc import Mapping
from typing import Any

from ._base import V1GroupAPI


class MsgAPI(V1GroupAPI):
    """``msg`` 组，共 5 个 JSON 端点。"""

    async def list_message_edit_record(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """获取信息历史编辑内容。

        ``POST /v1/msg/list-message-edit-record``
        请求字段: msgId, size, page。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/msg/list-message-edit-record", body=body)

    async def file_download_record(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """文件消息下载记录。

        ``POST /v1/msg/file-download-record``
        请求字段: msgId, downloadPath。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/msg/file-download-record", body=body)

    async def msg_forward(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """转发消息。

        ``POST /v1/msg/msg-forward``
        请求字段: msgId, chatType, receive, chatId。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/msg/msg-forward", body=body)

    async def delete(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """删除消息。

        ``POST /v1/msg/delete``
        请求字段: chatId, msgId, chatType。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/msg/delete", body=body)

    async def a2ui_form_report(self, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """触发A2UI表单提交信息。

        ``POST /v1/msg/a2ui-form-report``
        请求字段: msgId, chatType, chatId, senderId, actionName, sourceComponentId, formContext, subLink, interactionJson。
        返回原始 JSON 响应（未逐字段建模），见文档。
        """
        return await self._call("POST", "/v1/msg/a2ui-form-report", body=body)
