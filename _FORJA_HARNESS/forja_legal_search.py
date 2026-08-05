"""Ponte auditável entre a FORJA Harness e o Sistema de Busca Jurídica/TeiaJus."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FORJA = Path(__file__).resolve().parent
CONFIG_PATH = FORJA / "FORJA_SEARCH_CONFIG.json"


class LegalSearchError(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _canonical_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _atomic_write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def _sanitize(value: Any) -> Any:
    sensitive = ("token", "secret", "password", "passwd", "api_key", "apikey", "authorization")
    if isinstance(value, dict):
        return {
            str(key): "[REDACTED]" if any(marker in str(key).lower() for marker in sensitive) else _sanitize(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    return value


def load_config(path: Path = CONFIG_PATH) -> dict:
    try:
        config = json.loads(path.read_text(encoding="utf-8-sig"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise LegalSearchError(f"configuração da busca inválida: {path}: {exc}") from exc
    if config.get("schemaVersion") != 1 or not config.get("enabled"):
        raise LegalSearchError("integração TeiaJus desabilitada ou com schema incompatível")
    return config


class TeiaJusBridge:
    def __init__(
        self,
        *,
        config_path: Path = CONFIG_PATH,
        telemetry_root: Path | None = None,
        python_executable: str | None = None,
    ) -> None:
        self.config = load_config(config_path)
        configured_root = os.environ.get("FORJA_SEARCH_PROJECT") or self.config["projectRoot"]
        self.project_root = Path(configured_root).expanduser().resolve()
        self.default_db = Path(
            os.environ.get("FORJA_SEARCH_DB") or self.config["defaultDb"]
        ).expanduser().resolve()
        self.python = python_executable or sys.executable
        configured_telemetry = Path(self.config["telemetryRoot"])
        self.telemetry_root = telemetry_root or (
            configured_telemetry if configured_telemetry.is_absolute() else FORJA / configured_telemetry
        )
        if not (self.project_root / "src" / "teiajus" / "agent_api.py").is_file():
            raise LegalSearchError(f"API TeiaJus não encontrada em {self.project_root}")

    @property
    def read_actions(self) -> set[str]:
        return set(self.config["policy"]["readActions"])

    @property
    def mutation_actions(self) -> set[str]:
        return set(self.config["policy"]["mutationActions"])

    @property
    def denied_actions(self) -> set[str]:
        """Ações `read_paid` do TeiaJus: leem, mas consomem crédito externo.

        A allowlist já as recusaria por omissão. A lista própria existe para que
        uma inclusão distraída em `readActions` não passe a autorizar gasto sem
        que alguém tenha decidido isso.
        """
        return set(self.config["policy"].get("deniedActions") or [])

    def execute(
        self,
        action: str,
        params: dict | None = None,
        *,
        allow_mutation: bool = False,
        artifact_dir: Path | None = None,
    ) -> dict:
        if action in self.denied_actions:
            razao = self.config["policy"].get("deniedReason") or "ação vedada pela política da FORJA"
            raise LegalSearchError(f"ação negada: {action} — {razao}")
        if action not in self.read_actions | self.mutation_actions:
            raise LegalSearchError(f"ação fora da allowlist da FORJA: {action}")
        if action in self.mutation_actions and not allow_mutation:
            raise LegalSearchError(
                f"ação mutável exige autorização explícita allow_mutation=True: {action}"
            )

        request_id = f"forja-search-{uuid.uuid4().hex}"
        request_params = dict(params or {})
        if action not in {"capabilities"} and "db" not in request_params:
            request_params["db"] = str(self.default_db)
        request = {"requestId": request_id, "action": action, "params": request_params}
        env = os.environ.copy()
        src = str(self.project_root / "src")
        env["PYTHONPATH"] = src + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
        command = [self.python, "-m", self.config["module"]]
        started_at = _now()
        start = time.perf_counter()
        completed = subprocess.run(
            command,
            cwd=self.project_root,
            env=env,
            input=json.dumps(request, ensure_ascii=False),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=int(self.config.get("timeoutSeconds") or 1800),
            check=False,
        )
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        try:
            response = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            response = {
                "schemaVersion": 1,
                "requestId": request_id,
                "action": action,
                "ok": False,
                "error": {
                    "type": "InvalidGatewayResponse",
                    "message": f"stdout não contém JSON válido: {completed.stdout[-1000:]}",
                },
            }

        telemetry = {
            "schemaVersion": 1,
            "integration": "forja-teiajus",
            "requestId": request_id,
            "action": action,
            "mode": "write" if action in self.mutation_actions else "read",
            "startedAt": started_at,
            "finishedAt": _now(),
            "durationMs": duration_ms,
            "command": [self.python, "-m", self.config["module"]],
            "projectRoot": str(self.project_root),
            "request": _sanitize(request),
            "requestHash": _canonical_hash(request),
            "exitCode": completed.returncode,
            "ok": bool(response.get("ok")) and completed.returncode == 0,
            "responseHash": _canonical_hash(response),
            "responseSummary": {
                "resultKeys": sorted((response.get("result") or {}).keys()),
                "error": _sanitize(response.get("error")),
            },
            "stderrTail": completed.stderr[-2000:],
        }
        telemetry_path = self.telemetry_root / f"{request_id}.json"
        _atomic_write_json(telemetry_path, telemetry)
        response["forjaIntegration"] = {
            "telemetry": str(telemetry_path.resolve()),
            "requestHash": telemetry["requestHash"],
            "responseHash": telemetry["responseHash"],
        }

        if artifact_dir is not None:
            artifact = {
                "schemaVersion": 1,
                "artifactType": "forja_teiajus_search_evidence",
                "artifactId": request_id,
                "phase": "F5_PESQUISA_OFICIAL",
                "audience": "internal_working",
                "releasePolicy": "internal_working",
                "createdAt": _now(),
                "sourceSystem": "TeiaJus / Sistema de Busca Jurídica",
                "sourceProject": str(self.project_root),
                "request": _sanitize(request),
                "response": response,
                "legalUsePolicy": self.config["phaseIntegration"]["legalRule"],
            }
            artifact_path = Path(artifact_dir).resolve() / f"F5_TEIAJUS_SEARCH_{request_id}.json"
            _atomic_write_json(artifact_path, artifact)
            response["forjaIntegration"]["artifact"] = str(artifact_path)

        if completed.returncode != 0 or not response.get("ok"):
            error = response.get("error") or {}
            raise LegalSearchError(
                f"TeiaJus falhou em {action}: {error.get('message') or 'erro sem mensagem'} "
                f"(telemetria: {telemetry_path})"
            )
        return response


def _common_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Integração FORJA + Sistema de Busca Jurídica")
    parser.add_argument("--db", help="banco TeiaJus alternativo")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("capabilities", help="listar todos os recursos integrados")
    sub.add_parser("health", help="verificar integridade e contagens")

    search = sub.add_parser("search", help="buscar processos no acervo canônico")
    search.add_argument("query", nargs="?", default="")
    search.add_argument("--tribunal")
    search.add_argument("--phase")
    search.add_argument("--min-case-value", type=float)
    search.add_argument("--min-conviction-value", type=float)
    search.add_argument("--min-score", type=float)
    search.add_argument("--has-conviction-value", action="store_true")
    search.add_argument("--has-parties", action="store_true")
    search.add_argument("--limit", type=int, default=50)
    search.add_argument("--order", choices=["potential", "value", "score", "newest", "cnj"], default="potential")
    search.add_argument("--artifact-dir")

    case = sub.add_parser("case", help="obter dossiê por número CNJ")
    case.add_argument("numero_cnj")
    case.add_argument("--include-raw", action="store_true")
    case.add_argument("--artifact-dir")

    execute = sub.add_parser("execute", help="executar uma ação registrada do TeiaJus")
    execute.add_argument("action")
    execute.add_argument("--params", default="{}", help="objeto JSON com parâmetros")
    execute.add_argument("--allow-mutation", action="store_true")
    execute.add_argument("--artifact-dir")

    stj_health = sub.add_parser("stj-health", help="verificar fontes oficiais, cobertura e atualidade do STJ")

    stj_catalog = sub.add_parser("stj-catalog", help="listar todos os datasets e recursos oficiais STJ")
    stj_catalog.add_argument("--dataset")
    stj_catalog.add_argument("--include-resources", action="store_true")
    stj_catalog.add_argument("--artifact-dir")

    stj_search = sub.add_parser("stj-search", help="pesquisar espelhos e ementas oficiais do STJ")
    stj_search.add_argument("query")
    stj_search.add_argument("--orgao", action="append", dest="organs")
    stj_search.add_argument("--limit", type=int, default=20)
    stj_search.add_argument("--resources-per-dataset", type=int, default=1)
    stj_search.add_argument("--match-mode", choices=["all", "any", "phrase"], default="all")
    stj_search.add_argument("--artifact-dir")

    stj_daily = sub.add_parser("stj-daily", help="pesquisar decisões/acórdãos diários do STJ")
    stj_daily.add_argument("query")
    stj_daily.add_argument("--days", type=int, default=7)
    stj_daily.add_argument("--limit", type=int, default=20)
    stj_daily.add_argument("--include-text", action="store_true")
    stj_daily.add_argument("--match-mode", choices=["all", "any", "phrase"], default="all")
    stj_daily.add_argument("--artifact-dir")

    stj_datajud = sub.add_parser("stj-datajud", help="prévia processual STJ via DataJud, sem persistência")
    stj_datajud.add_argument("--limit", type=int, default=10)
    stj_datajud.add_argument("--source-timeout", type=float, default=15)
    stj_datajud.add_argument("--artifact-dir")

    stj_collect = sub.add_parser("stj-collect", help="coletar processos STJ/DataJud no banco canônico")
    stj_collect.add_argument("--max", type=int, default=None)
    stj_collect.add_argument("--allow-mutation", action="store_true")
    stj_collect.add_argument("--artifact-dir")
    return parser


def main() -> None:
    args = _common_parser().parse_args()
    bridge = TeiaJusBridge()
    common = {"db": args.db} if args.db else {}
    if args.command == "capabilities":
        action, params, allow, artifact = "capabilities", {}, False, None
    elif args.command == "health":
        action, params, allow, artifact = "health", common, False, None
    elif args.command == "search":
        params = {
            **common,
            "query": args.query,
            "tribunal": args.tribunal,
            "phase": args.phase,
            "min_case_value": args.min_case_value,
            "min_conviction_value": args.min_conviction_value,
            "min_score": args.min_score,
            "has_conviction_value": args.has_conviction_value or None,
            "has_parties": args.has_parties or None,
            "limit": args.limit,
            "order": args.order,
        }
        params = {key: value for key, value in params.items() if value is not None}
        action, allow = "search_cases", False
        artifact = Path(args.artifact_dir) if args.artifact_dir else None
    elif args.command == "case":
        params = {**common, "numero_cnj": args.numero_cnj, "include_raw": args.include_raw}
        action, allow = "get_case", False
        artifact = Path(args.artifact_dir) if args.artifact_dir else None
    elif args.command == "stj-health":
        action, params, allow, artifact = "stj_health", {}, False, None
    elif args.command == "stj-catalog":
        params = {
            "dataset": args.dataset,
            "include_resources": args.include_resources,
        }
        params = {key: value for key, value in params.items() if value is not None}
        action, allow = "stj_catalog", False
        artifact = Path(args.artifact_dir) if args.artifact_dir else None
    elif args.command == "stj-search":
        params = {
            "query": args.query,
            "organs": args.organs,
            "limit": args.limit,
            "resources_per_dataset": args.resources_per_dataset,
            "match_mode": args.match_mode,
        }
        params = {key: value for key, value in params.items() if value is not None}
        action, allow = "stj_search", False
        artifact = Path(args.artifact_dir) if args.artifact_dir else None
    elif args.command == "stj-daily":
        params = {
            "query": args.query,
            "days": args.days,
            "limit": args.limit,
            "include_text": args.include_text,
            "match_mode": args.match_mode,
        }
        action, allow = "stj_daily_decisions", False
        artifact = Path(args.artifact_dir) if args.artifact_dir else None
    elif args.command == "stj-datajud":
        action, params, allow = "stj_datajud_preview", {
            "limit": args.limit,
            "source_timeout_seconds": args.source_timeout,
        }, False
        artifact = Path(args.artifact_dir) if args.artifact_dir else None
    elif args.command == "stj-collect":
        params = {**common, "max_per_tribunal": args.max}
        params = {key: value for key, value in params.items() if value is not None}
        action, allow = "stj_collect", args.allow_mutation
        artifact = Path(args.artifact_dir) if args.artifact_dir else None
    else:
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError as exc:
            raise LegalSearchError(f"--params não é JSON válido: {exc}") from exc
        params.update(common)
        action, allow = args.action, args.allow_mutation
        artifact = Path(args.artifact_dir) if args.artifact_dir else None
    response = bridge.execute(action, params, allow_mutation=allow, artifact_dir=artifact)
    print(json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except LegalSearchError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(2)
