# -*- coding: utf-8 -*-
from __future__ import annotations

import io
import json
from pathlib import Path

import forja_axi


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _state(case_id: str, *, status: str, blockers: list | None = None) -> dict:
    return {
        "schemaVersion": 1,
        "specVersion": "test",
        "caseId": case_id,
        "demandId": f"demand-{case_id}",
        "revision": 7,
        "updatedAt": "2026-07-29T12:00:00-03:00",
        "phaseCursor": "F7_AUDITORIA_JURIDICA_FACTUAL",
        "lifecycleStatus": status,
        "completedPhases": ["F1", "F2"],
        "invalidatedPhases": [],
        "gateStatus": {"F1": "PASS", "F2": "PASS"},
        "blockers": blockers or [],
        "package": None,
        "deliveryEvidence": None,
        "stateHash": "abc123",
    }


def _queue() -> dict:
    return {
        "schemaVersion": 1,
        "producao": [],
        "bloqueadas": [
            {
                "demandaId": "demand-case-a",
                "caseId": "case-a",
                "prazo": "2026-08-01",
                "score": 90,
                "categoria": "legal",
                "motivo": "missing source",
                "esperaDias": 2,
                "destaque48h": True,
            }
        ],
        "emProducao": [],
        "aguardandoRevisaoHumana": [],
        "aguardandoEvidencia": [],
        "geradoEm": "2026-07-29T12:00:00-03:00",
    }


def _fixture(tmp_path: Path) -> Path:
    state_root = tmp_path / "state"
    _write_json(
        state_root / "case-a" / "FORJA_N3_STATE.json",
        _state(
            "case-a",
            status="blocked",
            blockers=[{"code": "P0", "reason": "x" * 600}],
        ),
    )
    _write_json(
        state_root / "case-b" / "FORJA_N3_STATE.json",
        _state("case-b", status="ready"),
    )
    _write_json(state_root / "FILA_PRIORIZADA.json", _queue())
    return state_root


def test_toon_tabular_and_quoting() -> None:
    encoded = forja_axi.encode_toon(
        {
            "items": [
                {"id": "01", "title": "hello, world", "ok": True},
                {"id": "02", "title": "plain", "ok": False},
            ]
        }
    )
    assert 'items[2]{id,title,ok}:' in encoded
    assert '"01","hello, world",true' in encoded
    assert '"02",plain,false' in encoded


def test_home_is_live_aggregate_without_case_names(tmp_path: Path) -> None:
    state_root = _fixture(tmp_path)
    payload = forja_axi.home_payload(state_root)
    assert payload["mode"] == "read_only"
    assert payload["cases"]["total"] == 2
    assert payload["queue"]["blocked"] == 1
    rendered = forja_axi.render(payload, "toon")
    assert "case-a" not in rendered
    assert "case-b" not in rendered


def test_cases_default_schema_and_definitive_empty_state(tmp_path: Path) -> None:
    state_root = _fixture(tmp_path)
    payload = forja_axi.cases_payload(state_root)
    assert payload["count"] == "2 of 2 total"
    assert tuple(payload["cases"][0]) == forja_axi.DEFAULT_CASE_FIELDS

    empty = forja_axi.cases_payload(state_root, status="missing")
    assert empty["count"] == "0 of 0 total"
    assert empty["empty"] == "0 cases found with status missing"


def test_case_truncates_blocker_and_full_is_escape_hatch(tmp_path: Path) -> None:
    state_root = _fixture(tmp_path)
    compact = forja_axi.case_payload("case-a", state_root)
    blocker = compact["case"]["blockers"][0]
    assert "truncated" in blocker
    assert compact["contentPolicy"]["blockersTruncated"] == 1

    full = forja_axi.case_payload("case-a", state_root, full=True)
    assert len(full["case"]["blockers"][0]) > len(blocker)
    assert full["contentPolicy"]["blockersTruncated"] == 0


def test_queue_uses_minimal_default_schema(tmp_path: Path) -> None:
    payload = forja_axi.queue_payload(_fixture(tmp_path), section="blocked")
    assert payload["count"] == "1 of 1 total"
    assert tuple(payload["items"][0]) == forja_axi.DEFAULT_QUEUE_FIELDS
    assert payload["summary"]["total"] == 1


def test_unknown_flag_is_structured_stdout_and_exit_2(tmp_path: Path) -> None:
    output = io.StringIO()
    code = forja_axi.main(
        ["cases", "--stat", "blocked", "--json"],
        state_root=_fixture(tmp_path),
        stdout=output,
    )
    payload = json.loads(output.getvalue())
    assert code == 2
    assert payload["error"]["code"] == "USAGE_ERROR"
    assert "unrecognized arguments" in payload["error"]["message"]
    assert payload["help"] == ["Run `python forja_axi.py cases --help`"]


def test_case_id_cannot_escape_state_root(tmp_path: Path) -> None:
    try:
        forja_axi.case_payload("../outside", _fixture(tmp_path))
    except forja_axi.AxiError as exc:
        assert exc.exit_code == 2
        assert exc.code == "USAGE_ERROR"
    else:
        raise AssertionError("path traversal should be rejected")
