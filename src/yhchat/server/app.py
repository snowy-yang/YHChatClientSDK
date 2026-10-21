"""HTTP/2 ASGI 服务：健康检查、云湖 webhook 接收、Satori 挂载、登录会话保存。"""

import time
from collections import OrderedDict
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, cast

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount, Route

from ..api.v1._auth import DEFAULT_PLATFORM, LoginSession
from ..client import YHChatClient
from ..errors import APIError, TransportError
from ..satori.backend import YHChatBackend
from ..satori.bus import EventBus
from ..satori.server import SatoriChatServer
from .sessions import SessionStore, StoredSession
from .webhook import parse_webhook, to_satori_event


class YHChatServer:
    """把云湖 SDK、Satori 协议端和 webhook 接收组合成一个 ASGI 应用。

    - ``GET /health``：健康检查；
    - ``POST /webhook``（可配置）：接收云湖回调，转成 Satori 事件后投进 :class:`EventBus`；
    - ``/satori``（可配置）：挂载 Satori v1 的 ``/v1/{action}`` 与 ``/v1/events``；
    - ``/session``（可配置）：登录会话保存（``GET`` 查状态 / ``POST /login`` / ``POST /logout``），
      只在传入 ``session_store`` 时挂载。

    会话持久化归服务端：SDK 的 ``client.auth`` 只返回 :class:`LoginSession`，不落盘；
    服务端把它写进 ``--session-file``，重启后由 :meth:`restore_session` 重新注入。
    """

    def __init__(
        self,
        client: YHChatClient,
        *,
        self_id: str,
        satori_token: str | None = None,
        platform: str = "yhchat",
        webhook_path: str = "/webhook",
        satori_path: str = "/satori",
        bus: EventBus | None = None,
        dedupe_size: int = 1024,
        session_store: SessionStore | None = None,
        session_path: str = "/session",
        session_token: str | None = None,
    ) -> None:
        self._client = client
        self._backend = YHChatBackend(client, self_id=self_id, platform=platform)
        self._satori = SatoriChatServer(self._backend, bus=bus, token=satori_token)
        self._webhook_path = webhook_path
        self._satori_path = satori_path
        self._dedupe_size = dedupe_size
        self._seen_events: OrderedDict[str, None] = OrderedDict()
        self._sessions = session_store
        self._session_path = session_path
        self._session_token = session_token

    @property
    def backend(self) -> YHChatBackend:
        """云湖后端适配器（含频道类型注册表）。"""
        return self._backend

    @property
    def satori(self) -> SatoriChatServer:
        """Satori 协议端。"""
        return self._satori

    @property
    def bus(self) -> EventBus:
        """事件总线。"""
        return self._satori.bus

    @property
    def session_store(self) -> SessionStore | None:
        """会话存储（未启用时为 ``None``）。"""
        return self._sessions

    def build_app(self) -> Starlette:
        """构造 Starlette 应用，交给 granian / uvicorn 运行。"""
        routes: list[Route | Mount] = [
            Route("/health", self._health, methods=["GET"]),
            Route(self._webhook_path, self._webhook, methods=["POST"]),
            Mount(self._satori_path, app=self._satori.build_app()),
        ]
        if self._sessions is not None:
            routes.extend(
                [
                    Route(self._session_path, self._session_get, methods=["GET"]),
                    Route(f"{self._session_path}/login", self._session_login, methods=["POST"]),
                    Route(f"{self._session_path}/logout", self._session_logout, methods=["POST"]),
                ]
            )
        return Starlette(routes=routes, lifespan=self._lifespan)

    @asynccontextmanager
    async def _lifespan(self, app: Starlette) -> AsyncGenerator[None]:
        """启动时恢复会话，让重启后的服务直接带上用户 token。"""
        await self.restore_session()
        yield

    async def restore_session(self) -> StoredSession | None:
        """把落盘的 token 注入 client；返回恢复的会话，没有则 ``None``。"""
        if self._sessions is None:
            return None
        stored = await self._sessions.load()
        if stored is None:
            return None
        await self._client.use_user_token(stored.token)
        return stored

    async def _health(self, request: Request) -> Response:
        return JSONResponse({"status": "ok", "satori": True, "subscribers": self.bus.subscriber_count})

    async def _webhook(self, request: Request) -> Response:
        try:
            raw: object = await request.json()
        except ValueError:
            return JSONResponse({"message": "回调不是合法 JSON"}, status_code=400)
        try:
            payload = parse_webhook(raw)
        except (TypeError, ValueError) as exc:
            return JSONResponse({"message": f"回调结构不合法: {exc}"}, status_code=400)
        if payload is None:
            return JSONResponse({})
        if payload.header.event_id and self._already_seen(payload.header.event_id):
            # 云湖会重投回调；按 eventId 去重，避免同一条消息推两次事件
            return JSONResponse({"duplicated": True})
        event = to_satori_event(payload, login=await self._backend.login(), registry=self._backend.registry)
        await self.bus.publish(event)
        return JSONResponse({})

    def _session_authorized(self, request: Request) -> bool:
        """会话路由鉴权：设了 ``session_token`` 就要求 ``Authorization: Bearer``。"""
        if self._session_token is None:
            return True
        return request.headers.get("authorization") == f"Bearer {self._session_token}"

    async def _session_get(self, request: Request) -> Response:
        store = self._sessions
        if store is None:
            return _not_enabled()
        if not self._session_authorized(request):
            return _unauthorized()
        stored = await store.load()
        if stored is None:
            return JSONResponse({"message": "尚未登录"}, status_code=404)
        return JSONResponse(stored.public())

    async def _session_login(self, request: Request) -> Response:
        store = self._sessions
        if store is None:
            return _not_enabled()
        if not self._session_authorized(request):
            return _unauthorized()
        try:
            raw: object = await request.json()
        except ValueError:
            return JSONResponse({"message": "请求体不是合法 JSON"}, status_code=400)
        if not isinstance(raw, dict):
            return JSONResponse({"message": "请求体必须是 JSON 对象"}, status_code=400)
        try:
            session = await self._login(cast("dict[str, Any]", raw))
        except ValueError as exc:
            return JSONResponse({"message": str(exc)}, status_code=400)
        except APIError as exc:
            return JSONResponse({"message": exc.message, "code": exc.code}, status_code=401)
        except TransportError as exc:
            return JSONResponse({"message": f"调用云湖失败: {exc}"}, status_code=502)
        await self._client.use_user_token(session.token)
        try:
            info = await self._client.v1.proto.user.info()
        except (APIError, TransportError) as exc:
            await self._client.clear_user_token()
            return JSONResponse({"message": f"登录后取用户信息失败: {exc}"}, status_code=502)
        stored = StoredSession(
            user_id=info.data.id,
            token=session.token,
            device_id=session.device_id,
            platform=session.platform,
            created_at=time.time(),
        )
        await store.save(stored)
        return JSONResponse({**stored.public(), "name": info.data.name})

    async def _session_logout(self, request: Request) -> Response:
        store = self._sessions
        if store is None:
            return _not_enabled()
        if not self._session_authorized(request):
            return _unauthorized()
        stored = await store.load()
        if stored is None:
            return JSONResponse({"logged_out": False})
        remote_error: str | None = None
        try:
            await self._client.auth.logout(
                LoginSession(token=stored.token, device_id=stored.device_id, platform=stored.platform)
            )
        except (APIError, TransportError) as exc:
            # token 可能已经失效；本地照样清掉，避免服务端一直拿着死 token
            remote_error = str(exc)
        finally:
            await store.clear()
            await self._client.clear_user_token()
        body: dict[str, Any] = {"logged_out": True}
        if remote_error is not None:
            body["remote_error"] = remote_error
        return JSONResponse(body)

    async def _login(self, payload: dict[str, Any]) -> LoginSession:
        """按 body 里的字段选登录方式：``email+password`` 或 ``mobile+captcha``。"""
        email = payload.get("email")
        password = payload.get("password")
        mobile = payload.get("mobile")
        captcha = payload.get("captcha")
        device_id = payload.get("device_id")
        platform = payload.get("platform")
        options: dict[str, Any] = {
            "device_id": None if device_id is None else str(device_id),
            "platform": DEFAULT_PLATFORM if platform is None else str(platform),
        }
        if email is not None and password is not None:
            return await self._client.auth.login_with_email(str(email), str(password), **options)
        if mobile is not None and captcha is not None:
            return await self._client.auth.login_with_verification(str(mobile), str(captcha), **options)
        raise ValueError("需要 email+password 或 mobile+captcha")

    def _already_seen(self, event_id: str) -> bool:
        """按 eventId 去重：见过返回 True，否则记下并淘汰最旧的。"""
        if event_id in self._seen_events:
            return True
        self._seen_events[event_id] = None
        while len(self._seen_events) > self._dedupe_size:
            self._seen_events.popitem(last=False)
        return False


def _not_enabled() -> Response:
    return JSONResponse({"message": "未启用会话保存（构造时传 session_store）"}, status_code=404)


def _unauthorized() -> Response:
    return JSONResponse({"message": "会话接口需要 Authorization: Bearer <session_token>"}, status_code=401)
