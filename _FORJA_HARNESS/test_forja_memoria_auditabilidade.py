"""Regressão da memória obrigatória de auditabilidade (sem renderização)."""

from __future__ import annotations

import json
import hashlib
import tempfile
import unittest
from pathlib import Path

from forja_memoria_auditabilidade import (
    MEMORY_HTML,
    MEMORY_JSON,
    MEMORY_MD,
    build_payload,
    build_bundle,
    validate_bundle,
)


class MemoriaAuditabilidadeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.case = Path(self.temp.name) / "case-memoria"
        self.case.mkdir()
        (self.case / "FORJA_N3_STATE.json").write_text(
            json.dumps({
                "caseId": self.case.name,
                "revision": 12,
                "currentPhase": "F9_PACOTE_REVISAO_DRAFT_OPCIONAL",
                "lifecycleStatus": "blocked",
                "completedPhases": ["F0_RECONCILIACAO_FILA", "F1_INGESTAO_COBERTURA", "F7_AUDITORIA_JURIDICA_FACTUAL"],
                "phaseHistory": [
                    {"phase": "F1_INGESTAO_COBERTURA", "status": "completed", "eventSeq": 2},
                    {"phase": "F4_PLANEJAMENTO_ESTRATEGICO", "status": "completed", "eventSeq": 3},
                ],
                "blockers": ["aprovação humana ausente"],
                "artifacts": {},
            }),
            encoding="utf-8",
        )
        (self.case / "producao").mkdir()
        (self.case / "producao" / "VISUAL_BUILD.json").write_text(
            json.dumps({
                "schemaVersion": 1,
                "route": "visual_law_canonica_svg_ooxml",
                "renderingUsed": False,
                "pdfCreated": False,
                "pngCreated": False,
            }),
            encoding="utf-8",
        )
        (self.case / "producao" / "F8_QA_ESTRUTURAL.json").write_text(
            json.dumps({"schemaVersion": 1, "mode": "static_ooxml_svg", "approved": True, "findings": []}),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_bundle_tem_memoria_sanitizada_e_no_render(self) -> None:
        result = build_bundle(self.case)
        self.assertTrue(result["approved"])
        for name in (MEMORY_MD, MEMORY_HTML, MEMORY_JSON):
            self.assertTrue((self.case / "pacote_revisao" / name).is_file())
        check = validate_bundle(Path(result["manifest"]), expected_case_dir=self.case)
        self.assertTrue(check["approved"], check["findings"])
        markdown = (self.case / "pacote_revisao" / MEMORY_MD).read_text(encoding="utf-8")
        self.assertIn("Materialização visual sem renderização", markdown)
        self.assertIn("renderingUsed", markdown)
        self.assertNotIn(str(self.case), markdown)
        self.assertNotIn("forja_render_docx.py", markdown)

    def test_tamper_no_manifesto_reprova(self) -> None:
        result = build_bundle(self.case)
        manifest = Path(result["manifest"])
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        payload["visual"]["renderingUsed"] = True
        manifest.write_text(json.dumps(payload), encoding="utf-8")
        check = validate_bundle(manifest, expected_case_dir=self.case)
        self.assertFalse(check["approved"])
        self.assertTrue(any("renderização" in item for item in check["findings"]))

    def test_inventario_distingue_ledger_canonico_de_snapshot_historico(self) -> None:
        ledger_dir = self.case / "n3_artifacts" / "F3_FONTES_REGIMENTO_LEIS"
        ledger_dir.mkdir(parents=True)
        historical = ledger_dir / "fact_ledger-old.json"
        historical.write_text(json.dumps({"facts": [{"id": "old"}]}), encoding="utf-8")
        canonical = ledger_dir / "fact_ledger.json"
        canonical.write_text(json.dumps({"facts": [{"id": "current"}]}), encoding="utf-8")
        state_path = self.case / "FORJA_N3_STATE.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["artifacts"] = {
            "fact_ledger": {
                "path": str(historical),
                "sha256": hashlib.sha256(historical.read_bytes()).hexdigest(),
            }
        }
        state_path.write_text(json.dumps(state), encoding="utf-8")

        payload = build_payload(self.case)
        old = next(item for item in payload["artifacts"] if item["id"] == "fact_ledger")
        current = next(item for item in payload["artifacts"] if item["id"] == "fact_ledger_canonical")
        self.assertEqual(old["role"], "historical_snapshot")
        self.assertEqual(current["path"], "n3_artifacts/F3_FONTES_REGIMENTO_LEIS/fact_ledger.json")
        self.assertEqual(current["role"], "source_ledger_canonical")
        self.assertTrue(current["sourceOfTruth"])
        self.assertTrue(current["hashMatches"])

    def test_fases_usam_identificadores_canonicos_e_aliases_historicos(self) -> None:
        payload = build_payload(self.case)
        phases = {item["phase"]: item["status"] for item in payload["method"]["phases"]}
        self.assertEqual(phases["F0_RECONCILIACAO_FILA"], "completed")
        self.assertEqual(phases["F1_INGESTAO_SEGURA"], "completed")
        self.assertEqual(phases["F7_AUDITORIA_JURIDICA_FACTUAL"], "completed")
        self.assertEqual(phases["F9_PACOTE_REVISAO_DRAFT_OPCIONAL"], "blocked")
        self.assertNotIn("F1_INGESTAO_COBERTURA", phases)
        self.assertEqual(payload["state"]["currentPhase"], "F9_PACOTE_REVISAO_DRAFT_OPCIONAL")
        history = payload["method"]["phaseHistory"]
        self.assertEqual([item["phase"] for item in history], ["F1_INGESTAO_SEGURA", "F4_BLUEPRINT_ESTRATEGICO"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
