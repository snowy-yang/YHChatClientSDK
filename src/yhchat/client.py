"""SDK 入口。"""

from collections.abc import Mapping
from typing import Any, Self

import httpx

from .api.bot import BotAPI
from .records import MessageRegistry
from .transport import DEFAULT_BASE_URL, HttpTransport


class YHChatClient:
    """云湖 SDK 的异步客户端。

    用法::

        async with YHChatClient(token) as client:
            await client.bot.message.send("group", "群 ID", TextSegment(text="hi"))
    """

    def __init__(
        self,
        token: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 15.0,
        http2: bool = True,
        trust_env: bool = True,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._http = HttpTransport(
            token=token,
            base_url=base_url,
            timeout=timeout,
            http2=http2,
            trust_env=trust_env,
            transport=transport,
        )
        self.records = MessageRegistry()
        """``msgId`` 到会话信息的缓存，编辑/撤回时可省略 ``recv_id``。"""
        self.bot = BotAPI(self._http, self.records)
        """机器人开放接口（``/open-apis/v1``）。"""

    @property
    def token(self) -> str:
        """当前机器人 token。"""
        return self._http.token

    async def call(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
        content: Any = None,
        files: Any = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        """调用任意端点，返回完整响应体（``code != 1`` 时抛 :class:`~yhchat.errors.APIError`）。

        这是给尚未封装的接口留的逃生口，参数直接透传给 httpx。
        """
        return await self._http.request(
            method, path, params=params, json=json, content=content, files=files, headers=headers
        )

    async def aclose(self) -> None:
        """关闭底层连接池。"""
        await self._http.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        await self.aclose()
