"""服务端登录会话持久化：token 存在服务端，SDK 保持无状态。

SDK 只负责发请求、校验响应（``client.auth`` 返回 :class:`LoginSession`，不落盘）；
``yhchat serve`` 负责把会话写到 ``--session-file``（默认 ``~/.config/yhchat/session.json``，
权限 0600），重启后由 :meth:`YHChatServer.restore_session` 重新注入给 ``YHChatClient``。
"""

import asyncio
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast


@dataclass(frozen=True, slots=True)
class StoredSession:
    """落盘的会话；``token`` 是敏感字段，只在服务端内存/0600 文件里出现。"""

    user_id: str
    token: str
    device_id: str
    platform: str
    created_at: float

    def public(self) -> dict[str, Any]:
        """可返回给调用方的字段（**不含 token**）。"""
        return {
            "user_id": self.user_id,
            "device_id": self.device_id,
            "platform": self.platform,
            "created_at": self.created_at,
        }


def default_session_path() -> Path:
    """默认会话文件：``$XDG_CONFIG_HOME/yhchat/session.json``。"""
    config_home = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return config_home / "yhchat" / "session.json"


class SessionStore:
    """单账号会话文件：原子写、0600 权限、损坏时报错而不是静默丢会话。"""

    def __init__(self, path: Path) -> None:
        self._path = Path(path)
        self._lock = asyncio.Lock()

    @property
    def path(self) -> Path:
        """会话文件路径。"""
        return self._path

    async def save(self, session: StoredSession) -> None:
        """写盘（先写临时文件再 ``os.replace``，避免半个文件）。"""
        async with self._lock:
            await asyncio.to_thread(self._write, session)

    async def load(self) -> StoredSession | None:
        """读盘；文件不存在返回 ``None``，内容损坏抛 :class:`ValueError`。"""
        async with self._lock:
            return await asyncio.to_thread(self._read)

    async def clear(self) -> None:
        """删除会话文件（不存在也当成功）。"""
        async with self._lock:
            await asyncio.to_thread(self._path.unlink, True)

    def _write(self, session: StoredSession) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        os.chmod(self._path.parent, 0o700)
        payload = json.dumps(
            {
                "user_id": session.user_id,
                "token": session.token,
                "device_id": session.device_id,
                "platform": session.platform,
                "created_at": session.created_at,
            },
            ensure_ascii=False,
            indent=2,
        )
        fd, tmp_name = tempfile.mkstemp(dir=self._path.parent, prefix=".session-", suffix=".tmp")
        tmp = Path(tmp_name)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(tmp, 0o600)
            os.replace(tmp, self._path)
        except BaseException:
            tmp.unlink(missing_ok=True)
            raise

    def _read(self) -> StoredSession | None:
        if not self._path.exists():
            return None
        try:
            raw: object = json.loads(self._path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"会话文件不是合法 JSON: {self._path}") from exc
        if not isinstance(raw, dict):
            raise ValueError(f"会话文件结构不对（应为对象）: {self._path}")
        data = cast("dict[str, Any]", raw)
        try:
            return StoredSession(
                user_id=str(data["user_id"]),
                token=str(data["token"]),
                device_id=str(data["device_id"]),
                platform=str(data["platform"]),
                created_at=float(data["created_at"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"会话文件缺字段或类型不对: {self._path}") from exc
