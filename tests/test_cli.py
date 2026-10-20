"""命令行入口测试：参数解析与延迟导入（不真正常驻服务器）。"""

import subprocess
import sys

import pytest

from yhchat.cli import build_parser, main


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
