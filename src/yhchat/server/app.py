"""HTTP/2 ASGI 服务：健康检查、云湖 webhook 接收、Satori 挂载。"""

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount, Route

from ..client import YHChatClient
from ..satori.backend import YHChatBackend
from ..satori.bus import EventBus
from ..satori.server import SatoriChatServer
from .webhook import parse_webhook, to_satori_event


class YHChatServer:
    """把云湖 SDK、Satori 协议端和 webhook 接收组合成一个 ASGI 应用。

    - ``GET /health``：健康检查；
    - ``POST /webhook``（可配置）：接收云湖回调，转成 Satori 事件后投进 :class:`EventBus`；
    - ``/satori``（可配置）：挂载 Satori v1 的 ``/v1/{action}`` 与 ``/v1/events``。
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
    ) -> None:
        self._backend = YHChatBackend(client, self_id=self_id, platform=platform)
        self._satori = SatoriChatServer(self._backend, bus=bus, token=satori_token)
        self._webhook_path = webhook_path
        self._satori_path = satori_path

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

    def build_app(self) -> Starlette:
        """构造 Starlette 应用，交给 granian / uvicorn 运行。"""
        return Starlette(
            routes=[
                Route("/health", self._health, methods=["GET"]),
                Route(self._webhook_path, self._webhook, methods=["POST"]),
                Mount(self._satori_path, app=self._satori.build_app()),
            ]
        )

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
        event = to_satori_event(payload, login=await self._backend.login(), registry=self._backend.registry)
        await self.bus.publish(event)
        return JSONResponse({})
