"""HTTP 传输层：统一注入 token、解析 ``{code, msg, data}`` 包装、映射异常。"""

from collections.abc import AsyncIterable, Mapping
from typing import Any, Literal, TypeVar, cast

import httpx
from google.protobuf.message import Message

from .errors import APIError, TransportError

DEFAULT_BASE_URL = "https://chat-go.jwzhd.com"
"""云湖接口域名；``open-apis`` 与 ``v1`` 都是它下面的路径。"""

_SUCCESS_CODE = 1

MessageT = TypeVar("MessageT", bound=Message)


class HttpTransport:
    """对 :class:`httpx.AsyncClient` 的薄封装。

    - 默认把 ``token`` 放在查询参数里（``/open-apis/v1`` 的 bot 约定）；
      ``v1/*`` 的用户接口改放请求头（``auth="header"``）；
    - 所有响应按 ``{code, msg, data}`` 解析，``code != 1`` 抛 :class:`APIError`；
    - 网络层失败统一抛 :class:`TransportError`。
    """

    def __init__(
        self,
        *,
        token: str,
        base_url: str = DEFAULT_BASE_URL,
        auth: Literal["query", "header"] = "query",
        token_name: str = "token",
        timeout: float = 15.0,
        http2: bool = True,
        trust_env: bool = True,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._token = token
        self._auth = auth
        self._token_name = token_name
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            http2=http2,
            trust_env=trust_env,
            transport=transport,
            headers={"User-Agent": "yhchat-client-sdk/0.1.0"},
        )

    @property
    def token(self) -> str:
        """当前 token。"""
        return self._token

    def _auth_headers(self, headers: Mapping[str, str] | None) -> dict[str, str]:
        merged = dict(headers or {})
        if self._auth == "header":
            merged[self._token_name] = self._token
        return merged

    def _auth_params(self, params: Mapping[str, Any] | None) -> dict[str, Any] | None:
        if self._auth != "query":
            return dict(params) if params else None
        return self._with_token(params)

    async def aclose(self) -> None:
        """关闭底层连接池。"""
        await self._client.aclose()

    async def request(
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
        """发起请求并返回完整响应体（已确认 ``code == 1``）。"""
        try:
            response = await self._client.request(
                method,
                path,
                params=self._auth_params(params),
                json=json,
                content=content,
                files=files,
                headers=self._auth_headers(headers),
            )
        except httpx.HTTPError as exc:  # 超时、连接失败、协议错误
            raise TransportError(f"{method} {path} 请求失败: {exc}") from exc
        return self._parse(method, path, response)

    async def request_pb(
        self,
        method: str,
        path: str,
        message: Message,
        response_type: type[MessageT],
        *,
        params: Mapping[str, Any] | None = None,
    ) -> MessageT:
        """发送 protobuf 请求体，并按 ``response_type`` 解析响应。

        ``v1/*`` 有 29 个端点是 protobuf 收发，响应不是 ``{code, msg, data}`` 包装，
        错误码在消息体内的 ``Status`` 里，交由调用方检查。
        """
        headers = self._auth_headers({"Content-Type": "application/x-protobuf"})
        try:
            response = await self._client.request(
                method,
                path,
                params=self._auth_params(params),
                content=message.SerializeToString(),
                headers=headers,
            )
        except httpx.HTTPError as exc:
            raise TransportError(f"{method} {path} 请求失败: {exc}") from exc
        if response.status_code >= 400:
            raise TransportError(f"{method} {path} 返回 HTTP {response.status_code}")
        return response_type.FromString(response.content)

    async def request_stream(
        self,
        method: str,
        path: str,
        *,
        chunks: AsyncIterable[bytes],
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        """以分块传输方式发送流式请求体，返回响应体。"""
        request_headers = {"Transfer-Encoding": "chunked", **self._auth_headers(headers)}
        try:
            async with self._client.stream(
                method,
                path,
                params=self._auth_params(params),
                content=chunks,
                headers=request_headers,
            ) as response:
                await response.aread()
        except httpx.HTTPError as exc:
            raise TransportError(f"{method} {path} 流式请求失败: {exc}") from exc
        return self._parse(method, path, response)

    def _with_token(self, params: Mapping[str, Any] | None) -> dict[str, Any]:
        merged = dict(params or {})
        merged.setdefault("token", self._token)
        return merged

    @staticmethod
    def _parse(method: str, path: str, response: httpx.Response) -> dict[str, Any]:
        try:
            payload = response.json()
        except ValueError as exc:
            raise TransportError(f"{method} {path} 返回非 JSON（HTTP {response.status_code}）") from exc
        if not isinstance(payload, dict):
            raise TransportError(f"{method} {path} 返回体不是 JSON 对象: {payload!r}")
        body = cast("dict[str, Any]", payload)

        if response.is_error:
            raise APIError(
                _int_or(cast("object", body.get("code")), response.status_code), str(body.get("msg", "")), endpoint=path
            )

        code = _int_or(cast("object", body.get("code")), 0)
        if code != _SUCCESS_CODE:
            raise APIError(code, str(body.get("msg", "")), endpoint=path)
        return body


def _int_or(value: object, fallback: int) -> int:
    """把云湖返回的 ``code`` 转成 ``int``，无法转换时用 ``fallback``。"""
    if isinstance(value, bool):  # bool 是 int 的子类，显式排除
        return fallback
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return fallback
    return fallback


def data_of(payload: Mapping[str, Any], *, endpoint: str) -> Mapping[str, Any]:
    """取出响应中的 ``data`` 字段，缺失或类型不对时抛 :class:`TransportError`。"""
    data = payload.get("data")
    if not isinstance(data, dict):
        raise TransportError(f"{endpoint} 响应缺少 data 对象: {payload!r}")
    return cast("Mapping[str, Any]", data)
