"""Satori v1 聊天子集的 ASGI 服务端（Starlette）。

- ``POST /v1/{action}``：HTTP RPC，参数 snake_case，响应是裸 JSON（无包封）；
- ``GET /v1/events``：WebSocket，``op:3 IDENTIFY`` → ``op:4 READY``，``op:1``/``op:2`` 心跳，
  ``op:0`` 推事件；
- 未实现的动作按协议返回 404（不是 501）。
"""

import asyncio
import contextlib
import json
from typing import Any, cast

from pydantic import BaseModel
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route, WebSocketRoute
from starlette.websockets import WebSocket, WebSocketDisconnect

from ..errors import APIError, TransportError
from .backend import SatoriBackend, SatoriNotFoundError, SatoriUnsupportedError
from .bus import EventBus
from .models import Event

_OP_EVENT = 0
_OP_PING = 1
_OP_PONG = 2
_OP_IDENTIFY = 3
_OP_READY = 4
_BAD_TOKEN_CLOSE_CODE = 3000
_DEFAULT_LIMIT = 50


class SatoriChatServer:
    """把 :class:`~yhchat.satori.backend.SatoriBackend` 暴露成 Satori v1 服务。"""

    def __init__(self, backend: SatoriBackend, *, bus: EventBus | None = None, token: str | None = None) -> None:
        self._backend = backend
        self._bus = bus or EventBus()
        self._token = token

    @property
    def bus(self) -> EventBus:
        """事件总线，供 webhook 等入口投递事件。"""
        return self._bus

    def build_app(self) -> Starlette:
        """构造 Starlette 应用。"""
        return Starlette(
            routes=[
                WebSocketRoute("/v1/events", self.handle_events),
                Route("/v1/{action:path}", self.handle_rpc, methods=["POST"]),
            ]
        )

    async def handle_rpc(self, request: Request) -> Response:
        """HTTP RPC 入口。"""
        if not self._authorized(request.headers.get("authorization")):
            return _error(401, "invalid token")
        action = request.path_params["action"]
        try:
            params = await _json_body(request)
            result = await self._dispatch(action, params)
        except (SatoriUnsupportedError, SatoriNotFoundError) as exc:
            return _error(404, str(exc))
        except APIError as exc:
            return _error(502, f"[{exc.code}] {exc.message}")
        except TransportError as exc:
            return _error(502, str(exc))
        except (KeyError, TypeError, ValueError) as exc:
            return _error(400, f"参数错误: {exc}")
        return JSONResponse(_dump(result))

    async def handle_events(self, websocket: WebSocket) -> None:
        """WebSocket 事件通道。"""
        await websocket.accept()
        try:
            frame = _as_dict(await websocket.receive_json())
        except (WebSocketDisconnect, RuntimeError, ValueError):
            return
        if frame is None or frame.get("op") != _OP_IDENTIFY:
            await websocket.close(code=_BAD_TOKEN_CLOSE_CODE)
            return
        body = _as_dict(frame.get("body"))
        token = body.get("token") if body is not None else None
        if self._token is not None and token != self._token:
            await websocket.close(code=_BAD_TOKEN_CLOSE_CODE)
            return

        login = await self._backend.login()
        await websocket.send_json(
            {
                "op": _OP_READY,
                "body": {
                    "logins": [login.model_dump(mode="json", exclude_none=True)],
                    "proxy_urls": [],
                },
            }
        )

        async with self._bus.subscribe() as queue:
            pump = asyncio.create_task(self._pump(websocket, queue))
            try:
                await self._receive_loop(websocket)
            except (WebSocketDisconnect, RuntimeError):
                pass
            finally:
                pump.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await pump

    async def _receive_loop(self, websocket: WebSocket) -> None:
        while True:
            frame = _as_dict(await websocket.receive_json())
            if frame is not None and frame.get("op") == _OP_PING:
                await websocket.send_json({"op": _OP_PONG})

    async def _pump(self, websocket: WebSocket, queue: asyncio.Queue[Event]) -> None:
        while True:
            event = await queue.get()
            await websocket.send_json({"op": _OP_EVENT, "body": event.model_dump(mode="json", exclude_none=True)})

    async def _dispatch(self, action: str, params: dict[str, object]) -> object:
        backend = self._backend
        match action:
            case "message.create":
                return await backend.message_create(
                    _required(params, "channel_id"),
                    _required(params, "content"),
                    _optional_dict(params, "referrer"),
                )
            case "message.get":
                return await backend.message_get(_required(params, "channel_id"), _required(params, "message_id"))
            case "message.list":
                return await backend.message_list(
                    _required(params, "channel_id"),
                    _optional_str(params, "next_token"),
                    _optional_str(params, "direction") or "before",
                    _optional_int(params, "limit", _DEFAULT_LIMIT),
                    _optional_str(params, "order") or "asc",
                )
            case "message.update":
                await backend.message_update(
                    _required(params, "channel_id"),
                    _required(params, "message_id"),
                    _required(params, "content"),
                )
                return None
            case "message.delete":
                await backend.message_delete(_required(params, "channel_id"), _required(params, "message_id"))
                return None
            case "channel.get":
                return await backend.channel_get(_required(params, "channel_id"))
            case "channel.list":
                return await backend.channel_list(_optional_str(params, "guild_id"))
            case "guild.get":
                return await backend.guild_get(_required(params, "guild_id"))
            case "guild.list":
                return await backend.guild_list(_optional_str(params, "next_token"))
            case "guild.member.get":
                return await backend.guild_member_get(_required(params, "guild_id"), _required(params, "user_id"))
            case "guild.member.list":
                return await backend.guild_member_list(
                    _required(params, "guild_id"), _optional_str(params, "next_token")
                )
            case "user.get":
                return await backend.user_get(_required(params, "user_id"))
            case "friend.list":
                return await backend.friend_list(_optional_str(params, "next_token"))
            case "login.get":
                return [await backend.login()]
            case _:
                raise SatoriUnsupportedError(f"未实现的动作: {action}")

    def _authorized(self, authorization: str | None) -> bool:
        if self._token is None:
            return True
        return authorization == f"Bearer {self._token}"


async def _json_body(request: Request) -> dict[str, object]:
    raw = await request.body()
    if not raw.strip():
        # login.get 这类动作没有参数，客户端可能直接发空 body
        return {}
    try:
        body: object = json.loads(raw)
    except ValueError as exc:
        raise ValueError("请求体不是合法 JSON") from exc
    if not isinstance(body, dict):
        raise TypeError("请求体必须是对象")
    return cast("dict[str, object]", body)


def _dump(value: object) -> Any:
    if value is None:
        return {}
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json", exclude_none=True)
    if isinstance(value, list):
        return [_dump(item) for item in cast("list[object]", value)]
    return value


def _as_dict(value: object) -> dict[str, object] | None:
    return cast("dict[str, object]", value) if isinstance(value, dict) else None


def _error(status: int, message: str) -> JSONResponse:
    return JSONResponse({"message": message}, status_code=status)


def _required(params: dict[str, object], key: str) -> str:
    value = params.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"缺少参数 {key}")
    return value


def _optional_str(params: dict[str, object], key: str) -> str | None:
    value = params.get(key)
    return value if isinstance(value, str) and value else None


def _optional_int(params: dict[str, object], key: str, default: int) -> int:
    value = params.get(key)
    if value is None:
        return default
    if not isinstance(value, int):
        raise TypeError(f"{key} 必须是整数")
    return value


def _optional_dict(params: dict[str, object], key: str) -> dict[str, object] | None:
    value = params.get(key)
    if value is None:
        return None
    if not isinstance(value, dict):
        raise TypeError(f"{key} 必须是对象")
    return cast("dict[str, object]", value)
