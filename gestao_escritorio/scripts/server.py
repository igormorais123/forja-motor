from __future__ import annotations

import atexit
import hashlib
import json
import os
import re
import subprocess
import sys
import threading
import time
import uuid
from datetime import date, datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

from dashboard_enrichment import enrich_snapshot
from office_io import atomic_write_json, atomic_write_text, compact_error, now_iso, read_json
from office_application import completion_blockers


VERSION = "2.0.0"
HOST = "127.0.0.1"
PORT = 8765
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
DATA_DIR = ROOT / "data"
DATA = DATA_DIR / "demandas.json"
STATUS = DATA_DIR / "status_integracoes.json"
WHATSAPP = DATA_DIR / "whatsapp_candidates.json"
DELIVERIES = DATA_DIR / "entregas_fabio_osorio.json"
MANUAL = DATA_DIR / "intervencoes_manuais.json"
HERMES_BRIDGE = DATA_DIR / "hermes_bridge_status.json"
RUNTIME = DATA_DIR / "runtime_status.json"
UPDATE_HISTORY = DATA_DIR / "update_history.json"
FORJA_STATUS = DATA_DIR / "forja_status.json"
PID_FILE = DATA_DIR / "server.pid"
HTML = ROOT / "painel_gestao_escritorio.html"
UPDATE = ROOT / "scripts" / "update_dashboard_local.ps1"
GMAIL_LOGIN = ROOT / "conectar_gmail_local.ps1"
WHATSAPP_ACCESS = Path(r"C:\Users\IgorPC\.hermes\bin\hermes-whatsapp-personal-access.ps1")
RENDER = ROOT / "scripts" / "render_dashboard.py"
APPLY_MANUAL = ROOT / "scripts" / "apply_manual_updates.py"
FORJA_STATE_ROOT = WORKSPACE / "_FORJA_HARNESS" / "state"

STARTED_AT = now_iso()
STARTED_MONOTONIC = time.monotonic()
DATA_LOCK = threading.RLock()
RUNTIME_LOCK = threading.RLock()
UPDATE_LOCK = threading.Lock()


def run_python(script: Path, *, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script)],
        cwd=str(WORKSPACE),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def apply_manual_updates() -> None:
    proc = run_python(APPLY_MANUAL, timeout=45)
    if proc.returncode != 0:
        raise RuntimeError(compact_error(proc.stderr or proc.stdout or "Falha ao aplicar intervenções manuais."))


def render_dashboard() -> None:
    proc = run_python(RENDER, timeout=60)
    if proc.returncode != 0:
        raise RuntimeError(compact_error(proc.stderr or proc.stdout or "Falha ao renderizar o painel."))


def manual_data() -> dict:
    data = read_json(MANUAL, None)
    if not isinstance(data, dict):
        data = {"schema": 1, "updatedAt": now_iso(), "items": {}}
    data.setdefault("schema", 1)
    data.setdefault("items", {})
    return data


def snapshot() -> dict:
    """Read-only snapshot. GET requests must never rewrite operational state."""

    payload = {
        "demandas": read_json(DATA, {"schema": 1, "demandas": []}),
        "status": read_json(STATUS, {}),
        "whatsapp": read_json(WHATSAPP, {}),
        "deliveries": read_json(DELIVERIES, {}),
        "manual": read_json(MANUAL, {"schema": 1, "items": {}}),
        "forja": read_json(FORJA_STATUS, {"schemaVersion": 1, "revision": 0, "items": {}}),
        "forjaFila": read_json(DATA_DIR / "forja_fila.json", None),
        "hermesBridge": read_json(HERMES_BRIDGE, {}),
        "runtime": runtime_payload(),
        "updateHistory": read_json(UPDATE_HISTORY, {"schema": 1, "runs": []}),
    }
    return enrich_snapshot(payload, WORKSPACE)


def parse_iso(value: object) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone()
    except (TypeError, ValueError):
        return None


def file_freshness(path: Path, *, updated_at: object = None) -> dict:
    stamp = parse_iso(updated_at)
    if stamp is None and path.exists():
        stamp = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).astimezone()
    if stamp is None:
        return {"state": "missing", "updatedAt": None, "ageMinutes": None}
    age_minutes = max(0, int((datetime.now(timezone.utc).astimezone() - stamp).total_seconds() / 60))
    state = "fresh" if age_minutes <= 26 * 60 else "attention" if age_minutes <= 48 * 60 else "stale"
    return {"state": state, "updatedAt": stamp.isoformat(timespec="seconds"), "ageMinutes": age_minutes}


def default_runtime() -> dict:
    return {
        "schema": 1,
        "version": VERSION,
        "server": {
            "state": "online",
            "pid": os.getpid(),
            "host": HOST,
            "port": PORT,
            "startedAt": STARTED_AT,
        },
        "update": {"state": "idle", "message": "Aguardando atualização."},
    }


def runtime_payload() -> dict:
    with RUNTIME_LOCK:
        payload = read_json(RUNTIME, None)
        if not isinstance(payload, dict):
            payload = default_runtime()
        payload["version"] = VERSION
        payload["server"] = {
            "state": "online",
            "pid": os.getpid(),
            "host": HOST,
            "port": PORT,
            "startedAt": STARTED_AT,
            "uptimeSeconds": int(time.monotonic() - STARTED_MONOTONIC),
        }
        payload.setdefault("update", {"state": "idle", "message": "Aguardando atualização."})
        return payload


def write_runtime(update: dict | None = None) -> dict:
    with RUNTIME_LOCK:
        payload = runtime_payload()
        if update is not None:
            payload["update"] = update
        atomic_write_json(RUNTIME, payload)
        return payload


def integration_summary() -> dict:
    status = read_json(STATUS, {}) or {}
    names = {
        "gmail": status.get("gmailLocal") or {},
        "whatsapp": status.get("whatsappPersonal") or {},
        "phone": status.get("phoneAlert") or {},
        "calendar": status.get("calendar") or {},
        "deliveries": status.get("deliveries") or {},
    }
    return {
        key: {
            "ok": bool(value.get("ok")),
            "state": value.get("state") or "nao_verificado",
            "message": value.get("message") or value.get("error") or value.get("summary") or "",
        }
        for key, value in names.items()
    }


def health_payload() -> dict:
    data = read_json(DATA, {}) or {}
    status = read_json(STATUS, {}) or {}
    items = data.get("demandas") or []
    open_items = [item for item in items if item.get("status") != "cumprida"]
    today = date.today()
    critical = 0
    for item in open_items:
        try:
            due = date.fromisoformat(str(item.get("prazo") or ""))
        except ValueError:
            continue
        if (due - today).days <= 2:
            critical += 1
    files = {
        "demandas": file_freshness(DATA, updated_at=data.get("updatedAt")),
        "integracoes": file_freshness(STATUS, updated_at=status.get("updatedAt")),
        "whatsapp": file_freshness(WHATSAPP, updated_at=(read_json(WHATSAPP, {}) or {}).get("updatedAt")),
        "hermes": file_freshness(HERMES_BRIDGE, updated_at=(read_json(HERMES_BRIDGE, {}) or {}).get("updatedAt")),
        "painel": file_freshness(HTML),
        "forja": file_freshness(FORJA_STATUS, updated_at=(read_json(FORJA_STATUS, {}) or {}).get("updatedAt")),
    }
    warnings = [name for name, value in files.items() if value["state"] in {"attention", "stale", "missing"}]
    return {
        "ok": DATA.exists() and HTML.exists(),
        "ready": DATA.exists() and HTML.exists(),
        "version": VERSION,
        "server": runtime_payload()["server"],
        "update": runtime_payload().get("update") or {},
        "files": files,
        "integrations": integration_summary(),
        "counts": {"total": len(items), "open": len(open_items), "done": len(items) - len(open_items), "critical48h": critical},
        "warnings": warnings,
    }


def parse_json_output(stdout: str) -> dict:
    text = (stdout or "").strip()
    if not text:
        return {}
    try:
        value = json.loads(text)
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        matches = list(re.finditer(r"(?m)^\s*\{", text))
        for match in reversed(matches):
            try:
                value = json.loads(text[match.start() :])
                if isinstance(value, dict):
                    return value
            except json.JSONDecodeError:
                continue
    return {}


def record_update_run(run: dict) -> None:
    with RUNTIME_LOCK:
        history = read_json(UPDATE_HISTORY, None)
        if not isinstance(history, dict):
            history = {"schema": 1, "runs": []}
        runs = [entry for entry in history.get("runs") or [] if entry.get("id") != run.get("id")]
        runs.insert(0, run)
        history["runs"] = runs[:30]
        history["updatedAt"] = now_iso()
        atomic_write_json(UPDATE_HISTORY, history)


class UpdateManager:
    def start(self, mode: str = "Manual") -> tuple[bool, dict]:
        if not UPDATE_LOCK.acquire(blocking=False):
            return False, runtime_payload().get("update") or {}
        run_id = uuid.uuid4().hex[:12]
        state = {
            "id": run_id,
            "state": "running",
            "mode": mode,
            "startedAt": now_iso(),
            "message": "Atualizando Gmail, WhatsApp sanitizado, Hermes, entregas e painel.",
        }
        write_runtime(state)
        thread = threading.Thread(target=self._run, args=(state,), name=f"office-update-{run_id}", daemon=True)
        thread.start()
        return True, state

    def _run(self, state: dict) -> None:
        started = time.monotonic()
        final = dict(state)
        try:
            env = os.environ.copy()
            env["PYTHONUTF8"] = "1"
            proc = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(UPDATE),
                    "-Mode",
                    state["mode"],
                ],
                cwd=str(WORKSPACE),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=900,
                env=env,
            )
            result = parse_json_output(proc.stdout)
            success = proc.returncode == 0 and result.get("ok") is not False
            final.update(
                {
                    "state": "success" if success else "error",
                    "finishedAt": now_iso(),
                    "durationSeconds": round(time.monotonic() - started, 1),
                    "message": "Atualização concluída." if success else "A atualização terminou com falha.",
                    "summary": {
                        "demands": result.get("demands"),
                        "whatsapp": result.get("whatsapp"),
                        "phoneAlert": result.get("phoneAlert"),
                        "updatedAt": result.get("updatedAt"),
                    },
                }
            )
            if not success:
                final["error"] = compact_error(proc.stderr or proc.stdout or f"exit {proc.returncode}")
        except subprocess.TimeoutExpired:
            final.update(
                {
                    "state": "error",
                    "finishedAt": now_iso(),
                    "durationSeconds": round(time.monotonic() - started, 1),
                    "message": "A atualização excedeu o limite de 15 minutos.",
                    "error": "timeout",
                }
            )
        except Exception as exc:
            final.update(
                {
                    "state": "error",
                    "finishedAt": now_iso(),
                    "durationSeconds": round(time.monotonic() - started, 1),
                    "message": "Falha inesperada durante a atualização.",
                    "error": compact_error(exc),
                }
            )
        finally:
            write_runtime(final)
            record_update_run(final)
            UPDATE_LOCK.release()


UPDATES = UpdateManager()


def safe_folder_name(value: object, fallback: str) -> str:
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", str(value or fallback))
    text = re.sub(r"\s+", " ", text).strip(" .")
    return (text[:110] or fallback).strip()


def demand_by_id(item_id: str) -> dict | None:
    data = read_json(DATA, {}) or {}
    return next((item for item in data.get("demandas") or [] if item.get("id") == item_id), None)


class Handler(BaseHTTPRequestHandler):
    server_version = f"MedinaOffice/{VERSION}"

    def send_bytes(self, body: bytes, status: int = 200, content_type: str = "application/json; charset=utf-8") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def write_json(self, obj: object, status: int = 200) -> None:
        self.send_bytes(json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8"), status)

    def read_body_json(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        if length > 256_000:
            raise ValueError("Requisição acima do limite permitido.")
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        value = json.loads(raw or "{}")
        if not isinstance(value, dict):
            raise ValueError("Corpo JSON inválido.")
        return value

    def do_OPTIONS(self) -> None:
        self.send_bytes(b"", 204, "text/plain; charset=utf-8")

    def do_HEAD(self) -> None:
        self.do_GET()

    def do_GET(self) -> None:
        path = unquote(self.path.split("?", 1)[0])
        try:
            if path in ("/", "/painel_gestao_escritorio.html"):
                self.send_bytes(HTML.read_bytes(), 200, "text/html; charset=utf-8")
                return
            if path == "/api/health":
                self.write_json(health_payload())
                return
            if path == "/api/status":
                self.write_json({"ok": True, "root": str(ROOT), "health": health_payload()})
                return
            if path == "/api/data":
                self.write_json(snapshot())
                return
            if path == "/api/update-status":
                self.write_json({"ok": True, "runtime": runtime_payload(), "history": read_json(UPDATE_HISTORY, {"schema": 1, "runs": []})})
                return
            self.write_json({"ok": False, "error": "Rota não encontrada."}, 404)
        except Exception as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 500)

    def do_POST(self) -> None:
        path = unquote(self.path.split("?", 1)[0])
        routes = {
            "/api/update": self.run_update,
            "/api/gmail-login": self.gmail_login,
            "/api/whatsapp-pair": self.whatsapp_pair,
            "/api/comment": self.save_comment,
            "/api/item-status": self.change_item_status,
            "/api/manual-task": self.create_manual_task,
            "/api/open-folder": self.open_folder,
            "/api/forja/open-artifact": self.open_forja_artifact,
            "/api/forja/open-package": self.open_forja_package,
        }
        handler = routes.get(path)
        if handler is None:
            self.write_json({"ok": False, "error": "Rota não encontrada."}, 404)
            return
        handler()

    def save_comment(self) -> None:
        try:
            payload = self.read_body_json()
            item_id = str(payload.get("id") or "").strip()
            text = str(payload.get("text") or "").strip()
            item = demand_by_id(item_id)
            if item is None:
                self.write_json({"ok": False, "error": "Demanda não encontrada."}, 404)
                return
            if not text:
                self.write_json({"ok": False, "error": "Escreva o comentário antes de salvar."}, 400)
                return
            if len(text) > 5_000:
                self.write_json({"ok": False, "error": "Comentário acima de 5.000 caracteres."}, 400)
                return
            with DATA_LOCK:
                manual = manual_data()
                entry = manual["items"].setdefault(item_id, {"comentarios": [], "overrides": {}})
                entry.setdefault("comentarios", []).append(
                    {
                        "id": f"comment-{uuid.uuid4().hex[:12]}",
                        "at": now_iso(),
                        "tipo": str(payload.get("tipo") or "comentario")[:60],
                        "texto": text,
                        "autor": str(payload.get("autor") or "Igor/Codex")[:80],
                    }
                )
                entry["updatedAt"] = now_iso()
                manual["updatedAt"] = entry["updatedAt"]
                atomic_write_json(MANUAL, manual)
                apply_manual_updates()
                render_dashboard()
            self.write_json({"ok": True, "snapshot": snapshot()})
        except (ValueError, json.JSONDecodeError) as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 400)
        except Exception as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 500)

    def change_item_status(self) -> None:
        try:
            payload = self.read_body_json()
            item_id = str(payload.get("id") or "").strip()
            status = str(payload.get("status") or "").strip()
            note = str(payload.get("note") or "").strip()
            evidence_type = str(payload.get("evidenceType") or "").strip().lower()
            if status not in ("aberta", "cumprida"):
                self.write_json({"ok": False, "error": "Status inválido."}, 400)
                return
            item = demand_by_id(item_id)
            if item is None:
                self.write_json({"ok": False, "error": "Demanda não encontrada."}, 404)
                return
            if status == "cumprida" and (len(note) < 8 or evidence_type not in {"email", "whatsapp", "protocolo", "arquivo", "manual"}):
                self.write_json(
                    {
                        "ok": False,
                        "error": "Para concluir, informe o tipo e a evidência concreta da entrega.",
                    },
                    400,
                )
                return
            if status == "cumprida":
                blockers = completion_blockers(item)
                if blockers:
                    self.write_json(
                        {
                            "ok": False,
                            "error": "Conclusão bloqueada: " + "; ".join(blockers) + ". Resolva ou reclassifique o insumo com justificativa auditável.",
                            "blockers": blockers,
                        },
                        409,
                    )
                    return
            with DATA_LOCK:
                manual = manual_data()
                entry = manual["items"].setdefault(item_id, {"comentarios": [], "overrides": {}})
                overrides = entry.setdefault("overrides", {})
                overrides["status"] = status
                overrides["respondidoComConteudo"] = status == "cumprida"
                if status == "cumprida":
                    overrides["evidenciaResposta"] = note
                    overrides["evidenciaTipo"] = evidence_type
                else:
                    overrides.pop("evidenciaResposta", None)
                    overrides.pop("evidenciaTipo", None)
                entry.setdefault("comentarios", []).append(
                    {
                        "id": f"status-{uuid.uuid4().hex[:12]}",
                        "at": now_iso(),
                        "tipo": "status",
                        "texto": note or "Demanda reaberta manualmente.",
                        "autor": "Igor/Codex",
                    }
                )
                entry["updatedAt"] = now_iso()
                manual["updatedAt"] = entry["updatedAt"]
                atomic_write_json(MANUAL, manual)
                apply_manual_updates()
                render_dashboard()
            self.write_json({"ok": True, "snapshot": snapshot()})
        except (ValueError, json.JSONDecodeError) as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 400)
        except Exception as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 500)

    def create_manual_task(self) -> None:
        try:
            payload = self.read_body_json()
            title = str(payload.get("titulo") or "").strip()
            summary = str(payload.get("resumo") or "").strip()
            deadline = str(payload.get("prazo") or "").strip() or None
            if not title:
                self.write_json({"ok": False, "error": "Título obrigatório."}, 400)
                return
            if len(title) > 220 or len(summary) > 8_000:
                self.write_json({"ok": False, "error": "Título ou resumo acima do limite permitido."}, 400)
                return
            if deadline:
                date.fromisoformat(deadline)
            with DATA_LOCK:
                data = read_json(DATA, {"schema": 1, "demandas": []})
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                item_id = f"manual-{timestamp}-{uuid.uuid4().hex[:6]}"
                folder_name = safe_folder_name(payload.get("pasta") or title, f"Tarefa manual {timestamp}")
                folder = WORKSPACE / folder_name
                folder.mkdir(parents=True, exist_ok=True)
                atomic_write_text(
                    folder / "COMANDO_MANUAL.md",
                    "# Tarefa manual\n\n"
                    f"- ID: `{item_id}`\n"
                    f"- Origem: {payload.get('origem') or 'manual'}\n"
                    f"- Criada em: {now_iso()}\n"
                    f"- Prazo: {deadline or 'sem prazo'}\n\n"
                    "## Resumo\n\n"
                    f"{summary or title}\n\n"
                    "## Observações\n\n"
                    f"{str(payload.get('observacao') or '').strip()}\n",
                )
                data.setdefault("demandas", []).append(
                    {
                        "id": item_id,
                        "titulo": title,
                        "clienteOuCaso": payload.get("clienteOuCaso") or title,
                        "origem": payload.get("origem") or "manual",
                        "emailsRecebidos": [],
                        "emailsResposta": [],
                        "pasta": folder_name,
                        "recebidoEm": payload.get("recebidoEm") or now_iso(),
                        "prazo": deadline,
                        "prazoTexto": payload.get("prazoTexto") or ("prazo manual informado" if deadline else "sem prazo definido"),
                        "resumo": summary or title,
                        "proximaAcao": payload.get("proximaAcao") or "Revisar a tarefa e executar a próxima ação.",
                        "status": "aberta",
                        "respondidoComConteudo": False,
                        "evidenciaResposta": "",
                        "urgenciaManual": payload.get("urgenciaManual") or "media",
                        "anexos": {
                            "diretosBaixados": None,
                            "diretosEsperados": None,
                            "externosPendentes": True,
                            "observacao": payload.get("anexosObservacao") or "Conferir anexos no canal de origem.",
                        },
                        "tags": payload.get("tags") or ["manual"],
                        "manualSource": payload.get("manualSource") or {},
                    }
                )
                data["updatedAt"] = now_iso()
                atomic_write_json(DATA, data)
                manual = manual_data()
                manual["items"][item_id] = {
                    "updatedAt": now_iso(),
                    "overrides": {},
                    "comentarios": [
                        {
                            "id": f"created-{uuid.uuid4().hex[:12]}",
                            "at": now_iso(),
                            "tipo": "criacao",
                            "texto": str(payload.get("observacao") or "Criada manualmente no painel."),
                            "autor": "Igor/Codex",
                        }
                    ],
                }
                manual["updatedAt"] = now_iso()
                atomic_write_json(MANUAL, manual)
                apply_manual_updates()
                render_dashboard()
            self.write_json({"ok": True, "id": item_id, "snapshot": snapshot()})
        except (ValueError, json.JSONDecodeError) as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 400)
        except Exception as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 500)

    def run_update(self) -> None:
        accepted, state = UPDATES.start("Manual")
        if not accepted:
            self.write_json({"ok": False, "error": "Já existe uma atualização em andamento.", "update": state}, 409)
            return
        self.write_json({"ok": True, "accepted": True, "update": state}, 202)

    def gmail_login(self) -> None:
        try:
            subprocess.Popen(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(GMAIL_LOGIN)],
                cwd=str(ROOT),
                creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
            )
            self.write_json({"ok": True, "message": "Login do Gmail iniciado. Conclua no navegador e atualize o painel."})
        except Exception as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 500)

    def whatsapp_pair(self) -> None:
        try:
            if not WHATSAPP_ACCESS.exists():
                self.write_json({"ok": False, "error": "Inicializador de pareamento não encontrado."}, 404)
                return
            creation_flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(subprocess, "CREATE_NO_WINDOW", 0)
            subprocess.Popen(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(WHATSAPP_ACCESS),
                    "-Action",
                    "pair",
                ],
                cwd=str(WHATSAPP_ACCESS.parent),
                creationflags=creation_flags,
            )
            self.write_json({"ok": True, "message": "Tela segura de pareamento iniciada. Leia o QR com o WhatsApp do celular."})
        except Exception as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 500)

    def open_folder(self) -> None:
        try:
            payload = self.read_body_json()
            item = demand_by_id(str(payload.get("id") or "").strip())
            if item is None or not item.get("pasta"):
                self.write_json({"ok": False, "error": "Pasta da demanda não encontrada."}, 404)
                return
            folder = (WORKSPACE / str(item["pasta"])).resolve()
            if WORKSPACE.resolve() not in folder.parents or not folder.exists():
                self.write_json({"ok": False, "error": "A pasta vinculada não existe no workspace."}, 404)
                return
            os.startfile(folder)  # type: ignore[attr-defined]
            self.write_json({"ok": True})
        except (ValueError, json.JSONDecodeError) as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 400)
        except Exception as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 500)

    @staticmethod
    def _forja_package(case_id: str) -> tuple[Path, dict]:
        if not re.fullmatch(r"case-[A-Za-z0-9._-]+", case_id):
            raise ValueError("caseId inválido.")
        case_dir = (FORJA_STATE_ROOT / case_id).resolve()
        if FORJA_STATE_ROOT.resolve() not in case_dir.parents or not case_dir.is_dir():
            raise FileNotFoundError("Caso FORJA não encontrado.")
        manifest_path = case_dir / "FORJA_PACKAGE.json"
        manifest = read_json(manifest_path, None)
        if not isinstance(manifest, dict):
            raise FileNotFoundError("Pacote FORJA não encontrado.")
        return case_dir, manifest

    @staticmethod
    def _artifact_entry(manifest: dict, artifact_id: str) -> dict | None:
        for item in manifest.get("attachments") or []:
            if item.get("artifactId") == artifact_id:
                return item
        email = manifest.get("email") or {}
        if email.get("artifactId") == artifact_id:
            return email
        for deliverable in manifest.get("deliverables") or []:
            for item in (deliverable.get("files") or {}).values():
                if isinstance(item, dict) and item.get("artifactId") == artifact_id:
                    return item
        return None

    @staticmethod
    def _sidecar_artifact(case_id: str, artifact_id: str) -> dict | None:
        if not re.fullmatch(r"case-[A-Za-z0-9._-]+", case_id):
            raise ValueError("caseId inválido.")
        sidecar = read_json(FORJA_STATUS, {})
        if not isinstance(sidecar, dict):
            return None
        for item in (sidecar.get("items") or {}).values():
            if not isinstance(item, dict) or item.get("caseId") != case_id:
                continue
            for artifact in item.get("artifacts") or []:
                if isinstance(artifact, dict) and artifact.get("artifactId") == artifact_id:
                    return artifact
        return None

    @staticmethod
    def _n4_artifact(case_id: str, artifact_id: str) -> dict | None:
        if not re.fullmatch(r"case-[A-Za-z0-9._-]+", case_id):
            raise ValueError("caseId inválido.")
        catalog = read_json(WORKSPACE / "_FORJA_HARNESS" / "n4_schemas" / "ARTIFACT_CATALOG.json", {}) or {}
        allowed = set((catalog.get("artifacts") or {}).keys()) | {"N4_VALIDATION.json", "N4_EXECUTION_TRACE.jsonl"}
        if artifact_id not in allowed:
            return None
        path = (FORJA_STATE_ROOT / case_id / "n4_artifacts" / artifact_id).resolve()
        case_dir = (FORJA_STATE_ROOT / case_id).resolve()
        if case_dir not in path.parents or not path.is_file():
            return None
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return {"artifactId": artifact_id, "path": str(path), "sha256": digest}

    @staticmethod
    def _verified_artifact_path(entry: dict) -> Path:
        value = entry.get("packagePath") or entry.get("path")
        path = Path(str(value or "")).resolve()
        if WORKSPACE.resolve() not in path.parents or not path.is_file():
            raise FileNotFoundError("Arquivo do pacote não encontrado no workspace.")
        expected = str(entry.get("sha256") or "")
        if expected:
            digest = hashlib.sha256()
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            if digest.hexdigest() != expected:
                raise ValueError("Arquivo diverge do hash registrado no pacote.")
        return path

    def open_forja_artifact(self) -> None:
        try:
            payload = self.read_body_json()
            case_id = str(payload.get("caseId") or "").strip()
            artifact_id = str(payload.get("artifactId") or "").strip()
            entry = None
            try:
                _, manifest = self._forja_package(case_id)
                entry = self._artifact_entry(manifest, artifact_id)
            except FileNotFoundError:
                pass
            if entry is None:
                entry = self._sidecar_artifact(case_id, artifact_id)
            if entry is None:
                entry = self._n4_artifact(case_id, artifact_id)
            if entry is None:
                self.write_json({"ok": False, "error": "Artefato não consta do estado auditado da FORJA."}, 404)
                return
            path = self._verified_artifact_path(entry)
            os.startfile(path)  # type: ignore[attr-defined]
            self.write_json({"ok": True, "name": path.name})
        except (ValueError, json.JSONDecodeError) as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 400)
        except FileNotFoundError as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 404)
        except Exception as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 500)

    def open_forja_package(self) -> None:
        try:
            payload = self.read_body_json()
            case_dir, manifest = self._forja_package(str(payload.get("caseId") or "").strip())
            package_id = str(manifest.get("packageId") or "").strip()
            package_dir = (case_dir / "packages" / package_id).resolve()
            if case_dir.resolve() not in package_dir.parents or not package_dir.is_dir():
                self.write_json({"ok": False, "error": "Pasta do pacote não encontrada."}, 404)
                return
            os.startfile(package_dir)  # type: ignore[attr-defined]
            self.write_json({"ok": True, "packageId": package_id})
        except (ValueError, json.JSONDecodeError) as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 400)
        except FileNotFoundError as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 404)
        except Exception as exc:
            self.write_json({"ok": False, "error": compact_error(exc)}, 500)

    def log_message(self, fmt: str, *args: object) -> None:
        return


class OfficeHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def cleanup() -> None:
    try:
        if PID_FILE.exists() and PID_FILE.read_text(encoding="ascii").strip() == str(os.getpid()):
            PID_FILE.unlink(missing_ok=True)
    except OSError:
        pass


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write_text(PID_FILE, str(os.getpid()) + "\n", encoding="ascii")
    write_runtime(runtime_payload().get("update"))
    atexit.register(cleanup)
    server = OfficeHTTPServer((HOST, PORT), Handler)
    print(f"http://{HOST}:{PORT}/", flush=True)
    try:
        server.serve_forever(poll_interval=0.25)
    finally:
        server.server_close()
        cleanup()


if __name__ == "__main__":
    main()
