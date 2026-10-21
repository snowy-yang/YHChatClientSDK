"""命令行入口：``yhchat serve``。

HTTP 服务用 Granian 跑 ASGI（``http2`` 打开时同时接受 h2 与 h2c），
另有 webhook 接收、Satori 挂载和登录会话保存。
"""

import argparse
import asyncio
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any


def build_parser() -> argparse.ArgumentParser:
    """构造参数解析器。"""
    parser = argparse.ArgumentParser(prog="yhchat", description="云湖 SDK 命令行入口")
    subcommands = parser.add_subparsers(dest="command")

    serve = subcommands.add_parser("serve", help="启动 HTTP/2 ASGI 服务（webhook 接收 + Satori 挂载）")
    serve.add_argument("--token", required=True, help="云湖机器人 token")
    serve.add_argument("--self-id", required=True, help="机器人 ID（Satori login 用）")
    serve.add_argument("--host", default="127.0.0.1", help="监听地址（默认 127.0.0.1）")
    serve.add_argument("--port", type=int, default=5140, help="监听端口（默认 5140）")
    serve.add_argument("--satori-token", default=None, help="Satori 侧 token；不传则不鉴权")
    serve.add_argument("--platform", default="yhchat", help="Satori platform（默认 yhchat）")
    serve.add_argument("--base-url", default=None, help="云湖 API 基地址（默认官方地址）")
    serve.add_argument("--webhook-path", default="/webhook", help="云湖回调路径（默认 /webhook）")
    serve.add_argument("--satori-path", default="/satori", help="Satori 挂载路径（默认 /satori）")
    serve.add_argument("--session-path", default="/session", help="会话路由前缀（默认 /session）")
    serve.add_argument(
        "--session-file",
        type=Path,
        default=None,
        help="登录会话落盘路径（默认 $XDG_CONFIG_HOME/yhchat/session.json，权限 0600）",
    )
    serve.add_argument("--no-session", action="store_true", help="不启用登录会话保存")
    serve.add_argument(
        "--session-token",
        default=None,
        help="会话接口的 Bearer token；公网部署务必设置（默认不鉴权，只应监听 127.0.0.1）",
    )
    serve.add_argument("--no-http2", action="store_true", help="只启用 HTTP/1.1")
    serve.add_argument(
        "--no-trust-env",
        action="store_true",
        help="不读取 HTTP(S)_PROXY 等环境变量（代理变量含非法值时用）",
    )
    serve.add_argument("--ssl-cert", type=Path, default=None, help="TLS 证书文件（PEM），需与 --ssl-key 同时给")
    serve.add_argument("--ssl-key", type=Path, default=None, help="TLS 私钥文件（PEM）")
    serve.add_argument("--ssl-key-password", default=None, help="TLS 私钥口令")
    serve.add_argument("--ssl-ca", type=Path, default=None, help="客户端证书 CA（mTLS）")
    serve.add_argument("--ssl-client-verify", action="store_true", help="要求客户端证书（mTLS）")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLI 入口，返回进程退出码。"""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command != "serve":
        parser.print_help()
        return 2
    try:
        return asyncio.run(_serve(args))
    except KeyboardInterrupt:
        return 130


async def _serve(args: argparse.Namespace) -> int:
    from .client import YHChatClient
    from .server.app import YHChatServer

    if bool(args.ssl_cert) != bool(args.ssl_key):
        print("--ssl-cert 与 --ssl-key 必须同时提供", file=sys.stderr)
        return 2

    session_store = None
    if not args.no_session:
        from .server.sessions import SessionStore, default_session_path

        session_store = SessionStore(args.session_file or default_session_path())

    client_kwargs: dict[str, Any] = {"http2": not args.no_http2, "trust_env": not args.no_trust_env}
    if args.base_url:
        client_kwargs["base_url"] = args.base_url
    async with YHChatClient(args.token, **client_kwargs) as client:
        server = YHChatServer(
            client,
            self_id=args.self_id,
            satori_token=args.satori_token,
            platform=args.platform,
            webhook_path=args.webhook_path,
            satori_path=args.satori_path,
            session_store=session_store,
            session_path=args.session_path,
            session_token=args.session_token,
        )
        await run_granian(
            server.build_app(),
            host=args.host,
            port=args.port,
            http2=not args.no_http2,
            ssl_cert=args.ssl_cert,
            ssl_key=args.ssl_key,
            ssl_key_password=args.ssl_key_password,
            ssl_ca=args.ssl_ca,
            ssl_client_verify=args.ssl_client_verify,
        )
    return 0


async def run_granian(
    app: object,
    *,
    host: str,
    port: int,
    http2: bool = True,
    ssl_cert: Path | None = None,
    ssl_key: Path | None = None,
    ssl_key_password: str | None = None,
    ssl_ca: Path | None = None,
    ssl_client_verify: bool = False,
) -> None:
    """用 Granian 跑 ASGI 应用（WebSocket 走 HTTP/1.1，HTTP/2 用于普通请求，可挂 TLS）。"""
    from granian.constants import HTTPModes, Interfaces
    from granian.server.embed import Server

    server = Server(
        app,
        address=host,
        port=port,
        interface=Interfaces.ASGI,
        http=HTTPModes.auto if http2 else HTTPModes.http1,
        websockets=True,
        ssl_cert=ssl_cert,
        ssl_key=ssl_key,
        ssl_key_password=ssl_key_password,
        ssl_ca=ssl_ca,
        ssl_client_verify=ssl_client_verify,
    )
    await server.serve()


if __name__ == "__main__":
    raise SystemExit(main())
