"""SDK 入口。"""

from collections.abc import Mapping
from typing import Any, Self

import httpx

from .api.bot import BotAPI
from .api.v1 import V1API
from .errors import YHChatError
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
        user_token: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 15.0,
        http2: bool = True,
        trust_env: bool = True,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._base_url = base_url
        self._timeout = timeout
        self._http2 = http2
        self._trust_env = trust_env
        self._raw_transport = transport
        self._user_token = user_token
        self._v1_http: HttpTransport | None = None
        self._v1: V1API | None = None
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

    @property
    def v1(self) -> V1API:
        """用户接口（``v1/*``）：token 放请求头，需要构造时传 ``user_token``。

        首次访问才创建连接池；没传 ``user_token`` 时抛 :class:`~yhchat.errors.YHChatError`。
        """
        if self._v1 is None:
            if self._user_token is None:
                raise YHChatError("调用 v1 接口需要 user_token：YHChatClient(token, user_token=...)")
            self._v1_http = HttpTransport(
                token=self._user_token,
                base_url=self._base_url,
                auth="header",
                timeout=self._timeout,
                http2=self._http2,
                trust_env=self._trust_env,
                transport=self._raw_transport,
            )
            self._v1 = V1API(self._v1_http)
        return self._v1

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
        """关闭底层连接池（含 v1 的连接池）。"""
        await self._http.aclose()
        if self._v1_http is not None:
            await self._v1_http.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        await self.aclose()
