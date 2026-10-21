"""命令行入口：``yhchat serve``。

不再用 Granian 的嵌入模式：把配置写成 ``YHCHAT_*`` 环境变量，直接拉起
``python -m granian --factory yhchat.server.app:create_app`` 子进程，父进程只做信号转发
和退出码透传。这样 ``--reload`` / ``--loop rloop`` / ``--pname`` 等 Granian CLI 功能都能用。
"""

import argparse
import importlib.util
import os
import signal
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from types import FrameType
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
    serve.add_argument(
        "--http2",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="服务端 HTTP/2（默认开启；--no-http2 只留 HTTP/1.1）",
    )
    serve.add_argument(
        "--loop",
        choices=("auto", "asyncio", "rloop"),
        default="auto",
        help="事件循环（默认 auto；直接传给 Granian CLI）",
    )
    serve.add_argument("--reload", action="store_true", help="文件变更自动重启（Granian CLI 功能）")
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
        return _serve(args)
    except KeyboardInterrupt:
        return 130


def _serve(args: argparse.Namespace) -> int:
    """校验参数后拉起 Granian 子进程，转发信号并等待退出。"""
    if bool(args.ssl_cert) != bool(args.ssl_key):
        print("--ssl-cert 与 --ssl-key 必须同时提供", file=sys.stderr)
        return 2
    if args.reload and importlib.util.find_spec("watchfiles") is None:
        print("--reload 需要 watchfiles：uv sync --extra server", file=sys.stderr)
        return 2
    if args.loop == "rloop" and importlib.util.find_spec("rloop") is None:
        print("--loop rloop 需要 rloop：uv sync --extra server", file=sys.stderr)
        return 2

    try:
        process = subprocess.Popen(granian_command(args), env=server_env(args))
    except OSError as exc:
        print(f"启动 Granian 失败：{exc}", file=sys.stderr)
        return 2
    previous: dict[int, Any] = {}

    def forward(signum: int, frame: FrameType | None) -> None:
        if process.poll() is None:
            process.send_signal(signum)

    for name in ("SIGINT", "SIGTERM", "SIGHUP"):
        if hasattr(signal, name):
            previous[getattr(signal, name)] = signal.signal(getattr(signal, name), forward)
    try:
        return process.wait()
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)


def granian_command(args: argparse.Namespace) -> list[str]:
    """把 CLI 参数翻译成 Granian CLI 命令行。"""
    command = [
        sys.executable,
        "-m",
        "granian",
        "--interface",
        "asgi",
        "--factory",
        "yhchat.server.app:create_app",
        "--host",
        args.host,
        "--port",
        str(args.port),
        "--http",
        "auto" if args.http2 else "1",
        "--loop",
        args.loop,
    ]
    if args.reload:
        command.append("--reload")
    if args.ssl_cert:
        command += ["--ssl-certificate", str(args.ssl_cert)]
    if args.ssl_key:
        command += ["--ssl-keyfile", str(args.ssl_key)]
    if args.ssl_key_password:
        command += ["--ssl-keyfile-password", args.ssl_key_password]
    if args.ssl_ca:
        command += ["--ssl-ca", str(args.ssl_ca)]
    if args.ssl_client_verify:
        command.append("--ssl-client-verify")
    return command


def server_env(args: argparse.Namespace) -> dict[str, str]:
    """把 CLI 参数翻译成子进程的 ``YHCHAT_*`` 环境变量。"""
    env = dict(os.environ)
    env["YHCHAT_TOKEN"] = args.token
    env["YHCHAT_SELF_ID"] = args.self_id
    env["YHCHAT_PLATFORM"] = args.platform
    env["YHCHAT_WEBHOOK_PATH"] = args.webhook_path
    env["YHCHAT_SATORI_PATH"] = args.satori_path
    env["YHCHAT_SESSION_PATH"] = args.session_path
    env["YHCHAT_TRUST_ENV"] = "0" if args.no_trust_env else "1"
    _set_or_clear(env, "YHCHAT_BASE_URL", args.base_url)
    _set_or_clear(env, "YHCHAT_SATORI_TOKEN", args.satori_token)
    _set_or_clear(env, "YHCHAT_SESSION_TOKEN", args.session_token)
    if args.no_session:
        env.pop("YHCHAT_SESSION_FILE", None)
    else:
        from .server.sessions import default_session_path

        env["YHCHAT_SESSION_FILE"] = str(args.session_file or default_session_path())
    return env


def _set_or_clear(env: dict[str, str], key: str, value: str | None) -> None:
    if value:
        env[key] = value
    else:
        env.pop(key, None)


if __name__ == "__main__":
    raise SystemExit(main())
