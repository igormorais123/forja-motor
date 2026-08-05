# -*- coding: utf-8 -*-
"""Fachada somente leitura e econômica para agentes operarem a FORJA.

O módulo não altera estado, não promove fases e não substitui os CLIs canônicos.
Ele transforma o estado local já existente em uma interface pequena, previsível
e estruturada, seguindo os princípios do Agent eXperience Interface (AXI).
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence, TextIO

FORJA = Path(__file__).resolve().parent
STATE_ROOT = FORJA / "state"
VERSION = "1.0.0"
DESCRIPTION = (
    "Orientar agentes na FORJA por estado vivo e comandos canônicos, "
    "sem alterar casos ou contornar gates humanos."
)

DEFAULT_CASE_FIELDS = ("caseId", "status", "phase", "blockers")
CASE_FIELDS = (
    "caseId",
    "demandId",
    "status",
    "phase",
    "revision",
    "updatedAt",
    "completed",
    "invalidated",
    "blockers",
    "gates",
    "packageStatus",
    "deliveryConfirmed",
    "stateHash",
)
DEFAULT_QUEUE_FIELDS = ("caseId", "deadline", "category", "reason")
QUEUE_FIELDS = (
    "caseId",
    "demandId",
    "deadline",
    "score",
    "category",
    "reason",
    "waitingDays",
    "urgent",
)
QUEUE_SECTIONS = {
    "ready": "producao",
    "blocked": "bloqueadas",
    "in_progress": "emProducao",
    "human_review": "aguardandoRevisaoHumana",
    "evidence": "aguardandoEvidencia",
}
COMMANDS = {
    "baseline": {
        "mode": "diagnostic",
        "risk": "read_only_but_expensive",
        "command": "python forja_baseline.py",
        "description": "Executa a baseline canônica isolada.",
    },
    "case-status": {
        "mode": "read",
        "risk": "read_only",
        "command": "python forja_state_machine.py <case> status",
        "description": "Lê o estado canônico detalhado de um caso.",
    },
    "release-audit": {
        "mode": "read",
        "risk": "read_only",
        "command": "python forja_release_audit.py",
        "description": "Revalida pacotes contra a política vigente.",
    },
    "start-phase": {
        "mode": "write",
        "risk": "changes_case_state",
        "command": (
            "python forja_run.py <case> start <phase> "
            "--expected-revision <revision>"
        ),
        "description": "Abre tentativa de fase sob revisão otimista.",
    },
    "promote-phase": {
        "mode": "write",
        "risk": "promotes_artifacts",
        "command": (
            "python forja_run.py <case> promote <attempt-dir> "
            "--expected-revision <revision>"
        ),
        "description": "Promove tentativa somente após os gates canônicos.",
    },
    "block-phase": {
        "mode": "write",
        "risk": "changes_case_state",
        "command": (
            "python forja_run.py <case> block <phase> "
            "--expected-revision <revision> --reason \"<reason>\""
        ),
        "description": "Registra bloqueio explícito sem apagar histórico.",
    },
}


class AxiError(RuntimeError):
    """Erro previsto que deve ser devolvido como dado estruturado."""

    def __init__(
        self,
        message: str,
        *,
        code: str = "FORJA_AXI_ERROR",
        exit_code: int = 1,
        help_commands: Sequence[str] = (),
    ) -> None:
        super().__init__(message)
        self.code = code
        self.exit_code = exit_code
        self.help_commands = list(help_commands)


class AxiArgumentParser(argparse.ArgumentParser):
    """Argparse sem erro cru em stderr nem prompt interativo."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("allow_abbrev", False)
        super().__init__(*args, **kwargs)

    def error(self, message: str) -> None:
        raise AxiError(
            message,
            code="USAGE_ERROR",
            exit_code=2,
            help_commands=(f"Run `{self.prog} --help`",),
        )


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def compact_path(path: Path) -> str:
    text = str(path.resolve())
    home = str(Path.home().resolve())
    if text.casefold().startswith(home.casefold()):
        return "~" + text[len(home) :]
    return text


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AxiError(
            f"required file not found: {path.name}",
            code="NOT_FOUND",
            help_commands=("Run `python forja_axi.py health`",),
        ) from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise AxiError(
            f"cannot read structured data from {path.name}: {exc}",
            code="INVALID_DATA",
            help_commands=("Run `python forja_axi.py health`",),
        ) from exc


def _case_files(state_root: Path) -> list[Path]:
    if not state_root.is_dir():
        return []
    return sorted(state_root.glob("case-*/FORJA_N3_STATE.json"))


def _blocker_text(blocker: Any) -> str:
    if isinstance(blocker, str):
        return blocker
    if not isinstance(blocker, dict):
        return str(blocker)
    parts = []
    for key in ("code", "reasonCode", "reason", "message", "description"):
        value = blocker.get(key)
        if value not in (None, "", [], {}):
            parts.append(str(value))
    return " · ".join(dict.fromkeys(parts)) or "structured blocker"


def _truncate(text: str, limit: int, *, full: bool) -> tuple[str, bool]:
    text = str(text)
    if full or len(text) <= limit:
        return text, False
    suffix = f"... (truncated, {len(text)} chars total — use --full)"
    keep = max(0, limit - len(suffix))
    return text[:keep].rstrip() + suffix, True


def _case_summary(path: Path, data: dict[str, Any]) -> dict[str, Any]:
    blockers = data.get("blockers") or []
    gate_status = data.get("gateStatus") or {}
    gates = Counter(
        str(value).casefold()
        for value in gate_status.values()
        if isinstance(value, (str, int, float, bool))
    )
    package = data.get("package") or {}
    delivery = data.get("deliveryEvidence") or {}
    return {
        "caseId": str(data.get("caseId") or path.parent.name),
        "demandId": data.get("demandId"),
        "status": str(data.get("lifecycleStatus") or "unknown"),
        "phase": data.get("phaseCursor"),
        "revision": data.get("revision"),
        "updatedAt": data.get("updatedAt"),
        "completed": len(data.get("completedPhases") or []),
        "invalidated": len(data.get("invalidatedPhases") or []),
        "blockers": len(blockers),
        "gates": dict(sorted(gates.items())),
        "packageStatus": (
            package.get("status") if isinstance(package, dict) else None
        ),
        "deliveryConfirmed": bool(
            delivery
            and (
                not isinstance(delivery, dict)
                or delivery.get("confirmed")
                or delivery.get("confirmedAt")
                or delivery.get("sentAt")
            )
        ),
        "stateHash": data.get("stateHash"),
    }


def _load_cases(state_root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    cases: list[dict[str, Any]] = []
    invalid: list[str] = []
    for path in _case_files(state_root):
        try:
            data = _read_json(path)
            if not isinstance(data, dict):
                raise AxiError("state root is not an object", code="INVALID_DATA")
            cases.append(_case_summary(path, data))
        except AxiError:
            invalid.append(path.parent.name)
    cases.sort(
        key=lambda item: (
            str(item.get("updatedAt") or ""),
            str(item.get("caseId") or ""),
        ),
        reverse=True,
    )
    return cases, invalid


def _select_fields(
    item: dict[str, Any], fields: Sequence[str]
) -> dict[str, Any]:
    return {field: item.get(field) for field in fields}


def _parse_fields(raw: str | None, allowed: Sequence[str], default: Sequence[str]) -> list[str]:
    if not raw:
        return list(default)
    fields = [part.strip() for part in raw.split(",") if part.strip()]
    unknown = [field for field in fields if field not in allowed]
    if unknown:
        raise AxiError(
            f"unknown field(s): {', '.join(unknown)}",
            code="USAGE_ERROR",
            exit_code=2,
            help_commands=(f"Valid fields: {', '.join(allowed)}",),
        )
    return list(dict.fromkeys(fields))


def _queue_summary(queue: dict[str, Any]) -> dict[str, Any]:
    counts = {
        public: len(queue.get(internal) or [])
        for public, internal in QUEUE_SECTIONS.items()
    }
    return {
        "available": True,
        "generatedAt": queue.get("geradoEm"),
        **counts,
        "total": sum(counts.values()),
    }


def home_payload(state_root: Path = STATE_ROOT) -> dict[str, Any]:
    cases, invalid = _load_cases(state_root)
    statuses = Counter(item["status"] for item in cases)
    queue_path = state_root / "FILA_PRIORIZADA.json"
    if queue_path.is_file():
        queue = _read_json(queue_path)
        queue_summary = (
            _queue_summary(queue) if isinstance(queue, dict)
            else {"available": False, "reason": "invalid_data"}
        )
    else:
        queue_summary = {"available": False, "reason": "not_found"}
    return {
        "bin": compact_path(Path(__file__)),
        "description": DESCRIPTION,
        "mode": "read_only",
        "generatedAt": now_iso(),
        "cases": {
            "total": len(cases),
            "invalid": len(invalid),
            "byStatus": [
                {"status": status, "count": count}
                for status, count in sorted(statuses.items())
            ],
        },
        "queue": queue_summary,
        "safety": {
            "mutationsExposed": False,
            "humanReviewGatesPreserved": True,
            "legalReleaseInferred": False,
        },
        "help": [
            "Run `python forja_axi.py cases` to list compact case state",
            "Run `python forja_axi.py queue` to inspect the live queue",
            "Run `python forja_axi.py commands` before a canonical mutation",
        ],
    }


def cases_payload(
    state_root: Path = STATE_ROOT,
    *,
    status: str | None = None,
    limit: int = 50,
    fields: str | None = None,
    full: bool = False,
) -> dict[str, Any]:
    if limit < 1 or limit > 500:
        raise AxiError(
            "--limit must be between 1 and 500",
            code="USAGE_ERROR",
            exit_code=2,
            help_commands=("Run `python forja_axi.py cases --help`",),
        )
    selected_fields = _parse_fields(fields, CASE_FIELDS, DEFAULT_CASE_FIELDS)
    cases, invalid = _load_cases(state_root)
    if status:
        cases = [item for item in cases if item["status"] == status]
    total = len(cases)
    visible = cases if full else cases[:limit]
    payload: dict[str, Any] = {
        "count": f"{len(visible)} of {total} total",
        "statusFilter": status,
        "invalidStates": len(invalid),
        "cases": [_select_fields(item, selected_fields) for item in visible],
    }
    if total == 0:
        context = f" with status {status}" if status else ""
        payload["empty"] = f"0 cases found{context}"
    help_commands = ["Run `python forja_axi.py case <case-id>` for details"]
    if len(visible) < total:
        help_commands.append(
            f"Run `python forja_axi.py cases --full` to see all {total} cases"
        )
    payload["help"] = help_commands
    return payload


def _resolve_case_path(state_root: Path, case_id: str) -> Path:
    if not case_id or case_id in {".", ".."} or any(
        separator in case_id for separator in ("/", "\\", ":")
    ):
        raise AxiError(
            "case-id must be a direct state directory name",
            code="USAGE_ERROR",
            exit_code=2,
            help_commands=("Run `python forja_axi.py cases`",),
        )
    path = state_root / case_id / "FORJA_N3_STATE.json"
    if path.is_file():
        return path
    candidates = [
        item.parent.name
        for item in _case_files(state_root)
        if case_id.casefold() in item.parent.name.casefold()
    ][:5]
    hint = (
        f" Similar case ids: {', '.join(candidates)}."
        if candidates
        else ""
    )
    raise AxiError(
        f"case not found: {case_id}.{hint}",
        code="NOT_FOUND",
        help_commands=("Run `python forja_axi.py cases`",),
    )


def case_payload(
    case_id: str,
    state_root: Path = STATE_ROOT,
    *,
    fields: str | None = None,
    full: bool = False,
) -> dict[str, Any]:
    selected_fields = _parse_fields(fields, CASE_FIELDS, CASE_FIELDS)
    path = _resolve_case_path(state_root, case_id)
    data = _read_json(path)
    if not isinstance(data, dict):
        raise AxiError("case state is not an object", code="INVALID_DATA")
    summary = _case_summary(path, data)
    blockers = []
    truncated = 0
    for blocker in data.get("blockers") or []:
        text, was_truncated = _truncate(_blocker_text(blocker), 320, full=full)
        blockers.append(text)
        truncated += int(was_truncated)
    if "blockers" in selected_fields:
        summary["blockers"] = blockers
    payload = {
        "case": _select_fields(summary, selected_fields),
        "contentPolicy": {
            "inputsIncluded": False,
            "artifactBodiesIncluded": False,
            "blockersTruncated": truncated,
        },
        "help": [
            f"Run `python forja_state_machine.py {case_id} status` "
            "for the canonical full state"
        ],
    }
    if truncated:
        payload["help"].append(
            f"Run `python forja_axi.py case {case_id} --full` "
            "to see complete blocker text"
        )
    return payload


def _queue_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "caseId": item.get("caseId"),
        "demandId": item.get("demandaId"),
        "deadline": item.get("prazo"),
        "score": item.get("score"),
        "category": item.get("categoria"),
        "reason": item.get("motivo"),
        "waitingDays": item.get("esperaDias"),
        "urgent": bool(item.get("destaque48h") or item.get("prazoVencido")),
    }


def queue_payload(
    state_root: Path = STATE_ROOT,
    *,
    section: str = "all",
    limit: int = 50,
    fields: str | None = None,
    full: bool = False,
) -> dict[str, Any]:
    if limit < 1 or limit > 500:
        raise AxiError(
            "--limit must be between 1 and 500",
            code="USAGE_ERROR",
            exit_code=2,
            help_commands=("Run `python forja_axi.py queue --help`",),
        )
    selected_fields = _parse_fields(fields, QUEUE_FIELDS, DEFAULT_QUEUE_FIELDS)
    queue = _read_json(state_root / "FILA_PRIORIZADA.json")
    if not isinstance(queue, dict):
        raise AxiError("queue root is not an object", code="INVALID_DATA")
    if section != "all" and section not in QUEUE_SECTIONS:
        raise AxiError(
            f"unknown queue section: {section}",
            code="USAGE_ERROR",
            exit_code=2,
            help_commands=(
                "Valid sections: all, " + ", ".join(QUEUE_SECTIONS),
            ),
        )
    sections = (
        [section] if section != "all" else list(QUEUE_SECTIONS)
    )
    rows = []
    for public in sections:
        for raw in queue.get(QUEUE_SECTIONS[public]) or []:
            if isinstance(raw, dict):
                row = _queue_item(raw)
                row["queue"] = public
                rows.append(row)
    total = len(rows)
    visible = rows if full else rows[:limit]
    payload: dict[str, Any] = {
        "generatedAt": queue.get("geradoEm"),
        "summary": _queue_summary(queue),
        "count": f"{len(visible)} of {total} total",
        "section": section,
        "items": [_select_fields(item, selected_fields) for item in visible],
    }
    if total == 0:
        payload["empty"] = f"0 queue items found in {section}"
    help_commands = [
        "Run `python forja_axi.py case <case-id>` to inspect a queue item"
    ]
    if len(visible) < total:
        help_commands.append(
            f"Run `python forja_axi.py queue --section {section} --full` "
            f"to see all {total} items"
        )
    payload["help"] = help_commands
    return payload


def commands_payload(name: str | None = None) -> dict[str, Any]:
    if name:
        command = COMMANDS.get(name)
        if not command:
            raise AxiError(
                f"unknown command: {name}",
                code="NOT_FOUND",
                help_commands=("Run `python forja_axi.py commands`",),
            )
        return {
            "command": {"name": name, **command},
            "safety": (
                "This interface does not execute mutations. Run the canonical "
                "command only after checking the live case revision and gates."
            ),
        }
    rows = [
        {
            "name": command_name,
            "mode": command["mode"],
            "risk": command["risk"],
            "description": command["description"],
        }
        for command_name, command in sorted(COMMANDS.items())
    ]
    return {
        "count": f"{len(rows)} of {len(rows)} total",
        "commands": rows,
        "help": [
            "Run `python forja_axi.py commands <name>` "
            "for the exact command template"
        ],
    }


def health_payload(state_root: Path = STATE_ROOT) -> dict[str, Any]:
    checks = []
    targets = (
        ("stateRoot", state_root, "directory"),
        ("specManifest", FORJA / "state" / "FORJA_SPEC_MANIFEST.json", "json"),
        ("queue", state_root / "FILA_PRIORIZADA.json", "json"),
        ("architectureMap", FORJA / "00_MAPA_ARQUITETURA_IA" / "LEIA_PRIMEIRO.md", "file"),
        ("agentSkill", FORJA / ".agents" / "skills" / "forja" / "SKILL.md", "file"),
    )
    for name, path, kind in targets:
        status = "ok"
        detail = None
        try:
            if kind == "directory":
                if not path.is_dir():
                    status = "missing"
            elif not path.is_file():
                status = "missing"
            elif kind == "json":
                _read_json(path)
        except AxiError as exc:
            status = "invalid"
            detail = str(exc)
        checks.append(
            {
                "check": name,
                "status": status,
                "detail": detail,
            }
        )
    failing = [item for item in checks if item["status"] != "ok"]
    return {
        "status": "ok" if not failing else "degraded",
        "count": f"{len(checks) - len(failing)} of {len(checks)} checks passed",
        "checks": checks,
        "baseline": "not_run",
        "help": [
            "Run `python forja_baseline.py` for the canonical regression gate"
        ],
    }


def _needs_quote(value: str, delimiter: str = ",") -> bool:
    if value == "" or value != value.strip():
        return True
    if value in {"true", "false", "null", "-"}:
        return True
    if re.fullmatch(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", value):
        return True
    if value.startswith("-"):
        return True
    if any(char in value for char in (delimiter, ":", '"', "\\", "[", "]", "{", "}")):
        return True
    return any(ord(char) < 32 for char in value)


def _toon_string(value: str, delimiter: str = ",") -> str:
    if not _needs_quote(value, delimiter):
        return value
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    escaped = "".join(
        f"\\u{ord(char):04x}" if ord(char) < 32 and char not in "\n\r\t" else char
        for char in escaped
    )
    return f'"{escaped}"'


def _toon_primitive(value: Any, delimiter: str = ",") -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            return "null"
        if value == 0:
            return "0"
        return format(value, ".15g")
    return _toon_string(str(value), delimiter)


def _is_primitive(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def _uniform_primitive_rows(items: list[Any]) -> tuple[bool, list[str]]:
    if not items or not all(isinstance(item, dict) for item in items):
        return False, []
    fields = list(items[0])
    if not fields:
        return False, []
    for item in items:
        if list(item) != fields or not all(_is_primitive(item[key]) for key in fields):
            return False, []
    return True, fields


def _encode_toon_value(
    key: str | None,
    value: Any,
    *,
    depth: int,
    lines: list[str],
) -> None:
    indent = "  " * depth
    prefix = f"{_toon_string(key)}: " if key is not None else ""
    if _is_primitive(value):
        lines.append(indent + prefix + _toon_primitive(value))
        return
    if isinstance(value, dict):
        if key is not None:
            lines.append(indent + f"{_toon_string(key)}:")
        for child_key, child_value in value.items():
            _encode_toon_value(
                str(child_key),
                child_value,
                depth=depth + (1 if key is not None else 0),
                lines=lines,
            )
        return
    if isinstance(value, list):
        if not value:
            lines.append(indent + prefix + "[]")
            return
        uniform, fields = _uniform_primitive_rows(value)
        label = _toon_string(key) if key is not None else ""
        if uniform:
            header = ",".join(_toon_string(field) for field in fields)
            lines.append(indent + f"{label}[{len(value)}]{{{header}}}:")
            for row in value:
                lines.append(
                    "  " * (depth + 1)
                    + ",".join(_toon_primitive(row[field]) for field in fields)
                )
            return
        if all(_is_primitive(item) for item in value):
            body = ",".join(_toon_primitive(item) for item in value)
            lines.append(indent + f"{label}[{len(value)}]: {body}")
            return
        lines.append(indent + f"{label}[{len(value)}]:")
        for item in value:
            if _is_primitive(item):
                lines.append("  " * (depth + 1) + "- " + _toon_primitive(item))
            elif isinstance(item, dict) and item:
                first_key = next(iter(item))
                first_value = item[first_key]
                if _is_primitive(first_value):
                    lines.append(
                        "  " * (depth + 1)
                        + f"- {_toon_string(first_key)}: "
                        + _toon_primitive(first_value)
                    )
                    for child_key, child_value in list(item.items())[1:]:
                        _encode_toon_value(
                            str(child_key),
                            child_value,
                            depth=depth + 2,
                            lines=lines,
                        )
                else:
                    lines.append("  " * (depth + 1) + "-")
                    for child_key, child_value in item.items():
                        _encode_toon_value(
                            str(child_key),
                            child_value,
                            depth=depth + 2,
                            lines=lines,
                        )
            else:
                lines.append(
                    "  " * (depth + 1)
                    + "- "
                    + _toon_string(json.dumps(item, ensure_ascii=False))
                )
        return
    lines.append(indent + prefix + _toon_string(str(value)))


def encode_toon(value: Any) -> str:
    """Codifica o subconjunto JSON usado pela fachada no TOON v4.1."""

    lines: list[str] = []
    _encode_toon_value(None, value, depth=0, lines=lines)
    return "\n".join(lines)


def render(payload: dict[str, Any], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(payload, ensure_ascii=False, indent=2)
    return encode_toon(payload)


def _extract_output_format(argv: list[str]) -> tuple[list[str], str]:
    output_format = "toon"
    clean: list[str] = []
    index = 0
    while index < len(argv):
        token = argv[index]
        if token == "--json":
            output_format = "json"
        elif token == "--toon":
            output_format = "toon"
        elif token == "--format":
            if index + 1 >= len(argv):
                raise AxiError(
                    "--format requires toon or json",
                    code="USAGE_ERROR",
                    exit_code=2,
                )
            index += 1
            output_format = argv[index]
            if output_format not in {"toon", "json"}:
                raise AxiError(
                    "--format must be toon or json",
                    code="USAGE_ERROR",
                    exit_code=2,
                )
        else:
            clean.append(token)
        index += 1
    return clean, output_format


def build_parser() -> AxiArgumentParser:
    parser = AxiArgumentParser(
        prog="python forja_axi.py",
        description=DESCRIPTION,
        epilog=(
            "Output defaults to TOON. Use --json anywhere for JSON. "
            "This facade never mutates FORJA state."
        ),
    )
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("home", help="show compact live workspace state")

    cases = sub.add_parser("cases", help="list case state with a minimal schema")
    cases.add_argument("--status")
    cases.add_argument("--limit", type=int, default=50)
    cases.add_argument("--fields", help="comma-separated fields")
    cases.add_argument("--full", action="store_true")

    case = sub.add_parser("case", help="inspect one case without artifact bodies")
    case.add_argument("case_id")
    case.add_argument("--fields", help="comma-separated fields")
    case.add_argument("--full", action="store_true")

    queue = sub.add_parser("queue", help="inspect the live prioritized queue")
    queue.add_argument(
        "--section",
        default="all",
        choices=("all", *QUEUE_SECTIONS),
    )
    queue.add_argument("--limit", type=int, default=50)
    queue.add_argument("--fields", help="comma-separated fields")
    queue.add_argument("--full", action="store_true")

    commands = sub.add_parser(
        "commands", help="discover canonical read and write commands"
    )
    commands.add_argument("name", nargs="?")

    sub.add_parser("health", help="check local interface prerequisites")
    return parser


def _dispatch(args: argparse.Namespace, state_root: Path) -> dict[str, Any]:
    command = args.command or "home"
    if command == "home":
        return home_payload(state_root)
    if command == "cases":
        return cases_payload(
            state_root,
            status=args.status,
            limit=args.limit,
            fields=args.fields,
            full=args.full,
        )
    if command == "case":
        return case_payload(
            args.case_id,
            state_root,
            fields=args.fields,
            full=args.full,
        )
    if command == "queue":
        return queue_payload(
            state_root,
            section=args.section,
            limit=args.limit,
            fields=args.fields,
            full=args.full,
        )
    if command == "commands":
        return commands_payload(args.name)
    if command == "health":
        return health_payload(state_root)
    raise AxiError(
        f"unknown command: {command}",
        code="USAGE_ERROR",
        exit_code=2,
    )


def main(
    argv: Sequence[str] | None = None,
    *,
    state_root: Path = STATE_ROOT,
    stdout: TextIO | None = None,
) -> int:
    out = stdout or sys.stdout
    raw = list(sys.argv[1:] if argv is None else argv)
    try:
        clean, output_format = _extract_output_format(raw)
        args = build_parser().parse_args(clean)
        payload = _dispatch(args, Path(state_root))
        print(render(payload, output_format), file=out)
        return 0
    except AxiError as exc:
        help_commands = list(exc.help_commands)
        clean_args = locals().get("clean", [])
        if (
            exc.code == "USAGE_ERROR"
            and clean_args
            and clean_args[0] in {"home", "cases", "case", "queue", "commands", "health"}
        ):
            help_commands = [
                f"Run `python forja_axi.py {clean_args[0]} --help`"
            ]
        payload = {
            "error": {
                "code": exc.code,
                "message": str(exc),
                "exitCode": exc.exit_code,
            },
            "help": help_commands,
        }
        output_format = locals().get("output_format", "toon")
        print(render(payload, output_format), file=out)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
