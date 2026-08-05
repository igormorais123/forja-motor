from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import pytest

from forja_legal_search import LegalSearchError, TeiaJusBridge, load_config

TEIAJUS_SRC = Path(load_config()["projectRoot"]) / "src"
sys.path.insert(0, str(TEIAJUS_SRC))

from teiajus.models import NormalizedCase, Proveniencia
from teiajus.storage import CaseStore


def _fixture_db(tmp_path: Path) -> Path:
    db = tmp_path / "teiajus-fixture.db"
    case = NormalizedCase(
        numero_cnj="00000010220208260100",
        tribunal="TJSP",
        classe_codigo=64,
        classe_nome="Improbidade",
        valor_causa=9_000_000,
        valor_condenacao=7_000_000,
        valor_condenacao_fonte="fixture/sentenca",
        valor_condenacao_ancora="condeno em R$ 7.000.000,00",
        resumo="Caso integrado FORJA TeiaJus",
        data_ajuizamento="2020-01-02",
        proveniencia=Proveniencia(
            fonte="fixture",
            coletado_em=datetime.fromisoformat("2026-07-12T10:00:00-03:00"),
            versao_extrator="forja-fixture/1",
        ),
        raw={},
    )
    with CaseStore(db) as store:
        store.upsert_case(case, fase="em_execucao", porta=3)
        store.conn.execute(
            "UPDATE cases SET resumo=? WHERE numero_cnj=?",
            ("Caso integrado FORJA TeiaJus", case.numero_cnj),
        )
        store.conn.commit()
        store.upsert_score(
            case.numero_cnj,
            {
                "score_reversibilidade": 0.95,
                "presenca_culpa": True,
                "tem_dolo_tambem": False,
                "trecho_ancora": "âncora",
                "sinais": [],
                "metodo": "heuristico",
                "avaliado_em": "2026-07-12T10:01:00-03:00",
            },
        )
    return db


def _bridge(tmp_path: Path) -> TeiaJusBridge:
    return TeiaJusBridge(telemetry_root=tmp_path / "telemetry", python_executable=sys.executable)


def test_capabilities_and_health_use_real_gateway(tmp_path):
    db = _fixture_db(tmp_path)
    bridge = _bridge(tmp_path)
    capabilities = bridge.execute("capabilities")
    names = {item["name"] for item in capabilities["result"]["actions"]}
    assert "search_cases" in names
    assert {"stj_health", "stj_catalog", "stj_search", "stj_daily_decisions", "stj_datajud_preview", "stj_collect"} <= names
    health = bridge.execute("health", {"db": str(db)})
    assert health["result"]["status"] == "ready"
    assert Path(health["forjaIntegration"]["telemetry"]).is_file()


def test_search_writes_f5_evidence_and_telemetry(tmp_path):
    db = _fixture_db(tmp_path)
    bridge = _bridge(tmp_path)
    artifact_dir = tmp_path / "attempt"
    response = bridge.execute(
        "search_cases",
        {"db": str(db), "query": "integrado", "limit": 10},
        artifact_dir=artifact_dir,
    )
    assert response["result"]["count"] == 1
    artifact = Path(response["forjaIntegration"]["artifact"])
    assert artifact.is_file()
    payload = json.loads(artifact.read_text(encoding="utf-8"))
    assert payload["phase"] == "F5_PESQUISA_OFICIAL"
    assert payload["releasePolicy"] == "internal_working"
    assert "gates" in payload["legalUsePolicy"]


def test_mutation_and_unknown_actions_fail_closed(tmp_path):
    bridge = _bridge(tmp_path)
    with pytest.raises(LegalSearchError, match="autorização explícita"):
        bridge.execute("classify", {})
    with pytest.raises(LegalSearchError, match="autorização explícita"):
        bridge.execute("stj_collect", {})
    with pytest.raises(LegalSearchError, match="allowlist"):
        bridge.execute("shell", {})
