"""命令行入口测试：参数解析、TLS 参数、延迟导入（不真正常驻服务器）。"""

import asyncio
import subprocess
import sys
from pathlib import Path

import pytest

from yhchat.cli import build_parser, main, run_granian


def test_serve_defaults() -> None:
    args = build_parser().parse_args(["serve", "--token", "tk", "--self-id", "bot-1"])

    assert args.host == "127.0.0.1"
    assert args.port == 5140
    assert args.webhook_path == "/webhook"
    assert args.satori_path == "/satori"
    assert args.platform == "yhchat"
    assert args.grpc_port is None
    assert args.no_http2 is False
    assert args.no_trust_env is False


def test_token_and_self_id_are_required() -> None:
    with pytest.raises(SystemExit) as excinfo:
        build_parser().parse_args(["serve"])

    assert excinfo.value.code == 2


def test_no_command_prints_help(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 2
    assert "serve" in capsys.readouterr().out


def test_granian_is_imported_lazily() -> None:
    code = "import sys, yhchat.cli; sys.exit(0 if 'granian' not in sys.modules else 1)"
    result = subprocess.run([sys.executable, "-c", code], check=False, capture_output=True)

    assert result.returncode == 0, result.stderr


def test_grpc_port_starts_and_stops_grpc_server(monkeypatch: pytest.MonkeyPatch) -> None:
    started: dict[str, object] = {}

    class FakeGrpcServer:
        async def stop(self, grace: int = 0) -> None:
            started["stopped"] = grace

    async def fake_serve(client: object, *, host: str, port: int) -> tuple[FakeGrpcServer, int]:
        started["grpc"] = (host, port)
        return FakeGrpcServer(), port

    async def fake_granian(app: object, *, host: str, port: int, http2: bool = True, **ssl: object) -> None:
        started["granian"] = (host, port)

    monkeypatch.setattr("yhchat.grpc.server.serve", fake_serve)
    monkeypatch.setattr("yhchat.cli.run_granian", fake_granian)

    # --no-trust-env：测试环境的 NO_PROXY=[::1] 会让 httpx 建 client 时就报 InvalidURL
    code = main(
        [
            "serve",
            "--token",
            "tk",
            "--self-id",
            "bot-1",
            "--grpc-port",
            "50999",
            "--port",
            "5150",
            "--no-trust-env",
        ]
    )

    assert code == 0
    assert started == {"grpc": ("127.0.0.1", 50999), "granian": ("127.0.0.1", 5150), "stopped": 0}


def test_ssl_flags_parse() -> None:
    args = build_parser().parse_args(
        [
            "serve",
            "--token",
            "tk",
            "--self-id",
            "bot-1",
            "--ssl-cert",
            "cert.pem",
            "--ssl-key",
            "key.pem",
            "--ssl-key-password",
            "pw",
            "--ssl-client-verify",
        ]
    )

    assert args.ssl_cert == Path("cert.pem")
    assert args.ssl_key == Path("key.pem")
    assert args.ssl_key_password == "pw"
    assert args.ssl_ca is None
    assert args.ssl_client_verify is True


def test_ssl_cert_without_key_is_rejected(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["serve", "--token", "tk", "--self-id", "bot-1", "--ssl-cert", "cert.pem"])

    assert code == 2
    assert "同时提供" in capsys.readouterr().err


def test_run_granian_passes_tls_options(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    class FakeServer:
        def __init__(self, app: object, **kwargs: object) -> None:
            captured["app"] = app
            captured.update(kwargs)

        async def serve(self) -> None:
            captured["served"] = True

    monkeypatch.setattr("granian.server.embed.Server", FakeServer)

    asyncio.run(
        run_granian(
            "app",
            host="0.0.0.0",
            port=8443,
            ssl_cert=Path("cert.pem"),
            ssl_key=Path("key.pem"),
            ssl_client_verify=True,
        )
    )

    assert captured["served"] is True
    assert captured["ssl_cert"] == Path("cert.pem")
    assert captured["ssl_key"] == Path("key.pem")
    assert captured["ssl_client_verify"] is True
    assert captured["port"] == 8443
