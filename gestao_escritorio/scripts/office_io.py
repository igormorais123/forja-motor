"""Small, dependency-free persistence helpers for the office management app."""

from __future__ import annotations

import json
import os
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class InterProcessLock:
    """Short file lease for writers running in different local processes."""

    def __init__(self, path: Path, *, timeout: float = 15, stale_after: float = 900):
        self.path = path
        self.timeout = timeout
        self.stale_after = stale_after
        self.token = uuid.uuid4().hex

    @staticmethod
    def _pid_alive(pid: int) -> bool:
        try:
            os.kill(pid, 0)
            return True
        except PermissionError:
            return True
        except OSError:
            return False

    def __enter__(self) -> "InterProcessLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    json.dump({"token": self.token, "pid": os.getpid(), "at": now_iso()}, handle)
                    handle.flush()
                    os.fsync(handle.fileno())
                return self
            except FileExistsError:
                try:
                    payload = read_json(self.path, {}) or {}
                    age = time.time() - self.path.stat().st_mtime
                    stale = age > self.stale_after and not self._pid_alive(int(payload.get("pid") or 0))
                except (OSError, TypeError, ValueError, json.JSONDecodeError):
                    stale = False
                if stale:
                    self.path.unlink(missing_ok=True)
                    continue
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"tempo esgotado aguardando lock: {self.path}")
                time.sleep(0.05)

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        try:
            payload = read_json(self.path, {}) or {}
            if payload.get("token") == self.token:
                self.path.unlink(missing_ok=True)
        except (OSError, json.JSONDecodeError):
            pass


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def read_json(path: Path, fallback: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return fallback


def atomic_write_text(path: Path, text: str, *, encoding: str = "utf-8") -> None:
    """Replace a text file atomically so interrupted refreshes keep the last good file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding=encoding, newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)


def atomic_write_json(path: Path, data: Any) -> None:
    atomic_write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def compact_error(value: object, limit: int = 900) -> str:
    """Keep diagnostics useful without persisting long command payloads or credentials."""

    text = " ".join(str(value or "").split())
    for marker in ("refresh_token", "access_token", "authorization", "ya29."):
        index = text.lower().find(marker)
        if index >= 0:
            text = text[:index] + marker + "=***"
    return text[:limit]
