"""命令行入口测试：参数解析、TLS 参数、事件循环选择、延迟导入（不真正常驻服务器）。"""

import asyncio
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from yhchat.cli import build_parser, main, run_granian


def test_serve_defaults() -> None:
    args = build_parser().parse_args(["serve", "--token", "tk", "--self-id", "bot-1"])

    assert args.host == "127.0.0.1"
    assert args.port == 5140
    assert args.webhook_path == "/webhook"
    assert args.satori_path == "/satori"
    assert args.platform == "yhchat"
    assert args.session_path == "/session"
    assert args.session_file is None
    assert args.no_session is False
    assert args.session_token is None
    assert args.http2 is True
    assert args.loop == "auto"
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


def test_serve_passes_http2_and_tls_to_granian(monkeypatch: pytest.MonkeyPatch) -> None:
    started: dict[str, object] = {}

    async def fake_granian(app: object, *, host: str, port: int, http2: bool = True, **ssl: object) -> None:
        started["granian"] = (host, port, http2)

    monkeypatch.setattr("yhchat.cli.run_granian", fake_granian)

    code = main(["serve", "--token", "tk", "--self-id", "bot-1", "--no-trust-env", "--no-session"])

    assert code == 0
    assert started["granian"] == ("127.0.0.1", 5140, True)


def test_granian_http2_can_be_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    started: dict[str, object] = {}

    async def fake_granian(app: object, *, host: str, port: int, http2: bool = True, **ssl: object) -> None:
        started["granian"] = (host, port, http2)

    monkeypatch.setattr("yhchat.cli.run_granian", fake_granian)

    code = main(["serve", "--token", "tk", "--self-id", "bot-1", "--no-http2", "--no-trust-env", "--no-session"])

    assert code == 0
    assert started["granian"] == ("127.0.0.1", 5140, False)


def test_loop_asyncio_uses_default_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: dict[str, str] = {}

    async def fake_serve(args: Any) -> int:
        seen["loop"] = type(asyncio.get_running_loop()).__name__
        return 0

    monkeypatch.setattr("yhchat.cli._serve", fake_serve)

    code = main(["serve", "--token", "tk", "--self-id", "bot-1", "--loop", "asyncio", "--no-session"])

    assert code == 0
    assert "RLoop" not in seen["loop"]


def test_loop_rloop_runs_on_rloop(monkeypatch: pytest.MonkeyPatch) -> None:
    pytest.importorskip("rloop")
    seen: dict[str, str] = {}

    async def fake_serve(args: Any) -> int:
        seen["loop"] = type(asyncio.get_running_loop()).__name__
        return 0

    monkeypatch.setattr("yhchat.cli._serve", fake_serve)

    code = main(["serve", "--token", "tk", "--self-id", "bot-1", "--loop", "rloop", "--no-session"])

    assert code == 0
    assert seen["loop"] == "RLoop"


def test_loop_rloop_reports_missing_dependency(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    import importlib.util

    real_find_spec = importlib.util.find_spec

    def fake_find_spec(name: str, package: str | None = None) -> object:
        if name == "rloop":
            return None
        return real_find_spec(name, package)

    monkeypatch.setattr(importlib.util, "find_spec", fake_find_spec)

    code = main(["serve", "--token", "tk", "--self-id", "bot-1", "--loop", "rloop", "--no-session"])

    assert code == 2
    assert "rloop" in capsys.readouterr().err


def test_loop_auto_uses_rloop_when_available(monkeypatch: pytest.MonkeyPatch) -> None:
    pytest.importorskip("rloop")
    seen: dict[str, str] = {}

    async def fake_serve(args: Any) -> int:
        seen["loop"] = type(asyncio.get_running_loop()).__name__
        return 0

    monkeypatch.setattr("yhchat.cli._serve", fake_serve)

    code = main(["serve", "--token", "tk", "--self-id", "bot-1", "--no-session"])

    assert code == 0
    assert seen["loop"] == "RLoop"
