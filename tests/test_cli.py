"""命令行入口测试：参数翻译、环境变量、子进程启动（不真正常驻服务器）。"""

import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from yhchat.cli import build_parser, granian_command, main, server_env


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
    assert args.reload is False
    assert args.no_trust_env is False


def test_token_and_self_id_are_required() -> None:
    with pytest.raises(SystemExit) as excinfo:
        build_parser().parse_args(["serve"])

    assert excinfo.value.code == 2


def test_no_command_prints_help(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 2
    assert "serve" in capsys.readouterr().out


def test_granian_is_not_imported_by_cli() -> None:
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


def test_granian_command_defaults() -> None:
    args = build_parser().parse_args(["serve", "--token", "tk", "--self-id", "bot-1"])

    command = granian_command(args)

    assert command[:3] == [sys.executable, "-m", "granian"]
    assert "--factory" in command
    assert command[command.index("--factory") + 1] == "yhchat.server.app:create_app"
    assert command[command.index("--http") + 1] == "auto"
    assert command[command.index("--loop") + 1] == "auto"
    assert "--reload" not in command


def test_granian_command_maps_flags() -> None:
    args = build_parser().parse_args(
        [
            "serve",
            "--token",
            "tk",
            "--self-id",
            "bot-1",
            "--no-http2",
            "--loop",
            "asyncio",
            "--reload",
            "--ssl-cert",
            "cert.pem",
            "--ssl-key",
            "key.pem",
            "--ssl-key-password",
            "pw",
            "--ssl-ca",
            "ca.pem",
            "--ssl-client-verify",
        ]
    )

    command = granian_command(args)

    assert command[command.index("--http") + 1] == "1"
    assert command[command.index("--loop") + 1] == "asyncio"
    assert "--reload" in command
    assert command[command.index("--ssl-certificate") + 1] == "cert.pem"
    assert command[command.index("--ssl-keyfile") + 1] == "key.pem"
    assert command[command.index("--ssl-keyfile-password") + 1] == "pw"
    assert command[command.index("--ssl-ca") + 1] == "ca.pem"
    assert "--ssl-client-verify" in command


def test_server_env_sets_config() -> None:
    args = build_parser().parse_args(
        [
            "serve",
            "--token",
            "tk",
            "--self-id",
            "bot-1",
            "--satori-token",
            "satori-tk",
            "--base-url",
            "http://127.0.0.1:9",
            "--no-trust-env",
            "--no-session",
        ]
    )

    env = server_env(args)

    assert env["YHCHAT_TOKEN"] == "tk"
    assert env["YHCHAT_SELF_ID"] == "bot-1"
    assert env["YHCHAT_SATORI_TOKEN"] == "satori-tk"
    assert env["YHCHAT_BASE_URL"] == "http://127.0.0.1:9"
    assert env["YHCHAT_TRUST_ENV"] == "0"
    assert "YHCHAT_SESSION_FILE" not in env


def test_server_env_enables_session_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("YHCHAT_SESSION_FILE", raising=False)
    args = build_parser().parse_args(["serve", "--token", "tk", "--self-id", "bot-1"])

    env = server_env(args)

    assert env["YHCHAT_SESSION_FILE"].endswith("session.json")


def test_serve_spawns_granian_subprocess(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    class FakePopen:
        def __init__(self, command: list[str], env: dict[str, str]) -> None:
            captured["command"] = command
            captured["env"] = env

        def poll(self) -> int:
            return 0

        def wait(self) -> int:
            return 0

        def send_signal(self, signum: int) -> None:
            captured["signal"] = signum

    monkeypatch.setattr("yhchat.cli.subprocess.Popen", FakePopen)

    code = main(
        [
            "serve",
            "--token",
            "tk",
            "--self-id",
            "bot-1",
            "--port",
            "5299",
            "--no-session",
            "--no-trust-env",
        ]
    )

    assert code == 0
    command = captured["command"]
    assert command[command.index("--port") + 1] == "5299"
    assert captured["env"]["YHCHAT_TOKEN"] == "tk"
    assert captured["env"]["YHCHAT_TRUST_ENV"] == "0"


def test_reload_requires_watchfiles(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    import importlib.util

    real_find_spec = importlib.util.find_spec

    def fake_find_spec(name: str, package: str | None = None) -> object:
        if name == "watchfiles":
            return None
        return real_find_spec(name, package)

    monkeypatch.setattr(importlib.util, "find_spec", fake_find_spec)

    code = main(["serve", "--token", "tk", "--self-id", "bot-1", "--reload", "--no-session"])

    assert code == 2
    assert "watchfiles" in capsys.readouterr().err


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


def test_loop_winloop_reports_missing_dependency(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    import importlib.util

    real_find_spec = importlib.util.find_spec

    def fake_find_spec(name: str, package: str | None = None) -> object:
        if name == "winloop":
            return None
        return real_find_spec(name, package)

    monkeypatch.setattr(importlib.util, "find_spec", fake_find_spec)

    code = main(["serve", "--token", "tk", "--self-id", "bot-1", "--loop", "winloop", "--no-session"])

    assert code == 2
    assert "winloop" in capsys.readouterr().err
