"""Shared, dependency-free primitives for the additive FORJA N3 layer."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FORJA = Path(__file__).resolve().parent
WORKSPACE = FORJA.parent
CONFIG_PATH = FORJA / "state" / "FORJA_N3_CONFIG.json"

PHASES = (
    "F0_RECONCILIACAO_FILA",
    "F1_INGESTAO_SEGURA",
    "F2_CLASSIFICACAO_PRODUTO_RISCO",
    "F3_FONTES_REGIMENTO_LEIS",
    "F4_BLUEPRINT_ESTRATEGICO",
    "F5_PESQUISA_OFICIAL",
    "F6_REDACAO_TEMPLATE",
    "F7_AUDITORIA_JURIDICA_FACTUAL",
    "F8_QA_VISUAL",
    "F9_PACOTE_REVISAO_DRAFT_OPCIONAL",
    "F10_ENTREGA_EVIDENCIA_APRENDIZADO",
)

# Nomes de artefato e de gate que mudaram sem que o objeto mudasse. Escritores
# emitem apenas o nome corrente; leitores aceitam o legado, para que tentativas
# promovidas antes da renomeação continuem validando (emenda E14, passo M7).
LEGACY_NAMES: dict[str, tuple[str, ...]] = {
    "editor_usage": ("fable5_usage",),
    "editor_model_confirmed": ("fable5_oauth_confirmed",),
}


def name_with_legacy(name: str) -> tuple[str, ...]:
    """Nome corrente seguido de seus nomes anteriores, se houver."""
    return (name, *LEGACY_NAMES.get(name, ()))


def resolve_name(name: str, available) -> str | None:
    """Primeiro nome — corrente ou legado — presente na coleção informada."""
    for candidate in name_with_legacy(name):
        if candidate in available:
            return candidate
    return None


class ForjaN3Error(RuntimeError):
    pass


class RevisionConflict(ForjaN3Error):
    pass


class TransitionError(ForjaN3Error):
    pass


class LockTimeout(ForjaN3Error):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex}"


def read_json(path: Path, fallback: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return fallback


def atomic_write_text(path: Path, text: str, *, encoding: str = "utf-8") -> None:
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


def atomic_write_json(path: Path, payload: Any) -> None:
    atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(payload: Any) -> str:
    value = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(value.encode("utf-8"))


def load_config() -> dict:
    data = read_json(CONFIG_PATH, {})
    if not isinstance(data, dict):
        raise ForjaN3Error(f"configuração N3 inválida: {CONFIG_PATH}")
    return data


def feature_enabled(name: str) -> bool:
    return bool((load_config().get("features") or {}).get(name))


def resolve_case_dir(case_key: str | Path, *, state_root: Path | None = None) -> Path:
    root = (state_root or (FORJA / "state")).resolve()
    candidate = Path(case_key)
    if candidate.exists():
        resolved = candidate.resolve()
        if resolved == root or root not in resolved.parents:
            raise ForjaN3Error(f"caso fora da pasta de estados: {resolved}")
        return resolved
    exact = root / str(case_key)
    if exact.is_dir():
        return exact
    matches = sorted(path for path in root.glob(f"case-*{case_key}*") if path.is_dir())
    if len(matches) != 1:
        raise ForjaN3Error(f"chave de caso ambígua ou ausente: {case_key} ({len(matches)} ocorrências)")
    return matches[0]


def ensure_within(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    base = root.resolve()
    if resolved != base and base not in resolved.parents:
        raise ForjaN3Error(f"caminho fora da raiz permitida: {resolved}")
    return resolved


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except PermissionError:
        return True
    except OSError:
        return False


class InterProcessLock:
    """Small lock-file lease used only around short atomic promotions."""

    def __init__(self, path: Path, *, timeout: float = 15, stale_after: float = 900):
        self.path = path
        self.timeout = timeout
        self.stale_after = stale_after
        self.token = new_id("lock")

    def _can_reclaim(self) -> bool:
        try:
            payload = read_json(self.path, {}) or {}
            age = time.time() - self.path.stat().st_mtime
            return age > self.stale_after and not _pid_alive(int(payload.get("pid") or 0))
        except (OSError, TypeError, ValueError, json.JSONDecodeError):
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
                if self._can_reclaim():
                    try:
                        self.path.unlink()
                    except FileNotFoundError:
                        pass
                    continue
                if time.monotonic() >= deadline:
                    raise LockTimeout(f"tempo esgotado aguardando lock: {self.path}")
                time.sleep(0.05)

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        try:
            payload = read_json(self.path, {}) or {}
            if payload.get("token") == self.token:
                self.path.unlink(missing_ok=True)
        except (OSError, json.JSONDecodeError):
            pass
