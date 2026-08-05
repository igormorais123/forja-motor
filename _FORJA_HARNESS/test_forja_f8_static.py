"""Regressão: F8 canônico valida OOXML/SVG sem disparar renderização."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from forja_f8_contract import validate_f8
from forja_n3_common import sha256_file


class F8StaticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.docx = self.root / "peca.docx"
        self.md = self.root / "peca.md"
        self.ledger = self.root / "F8_QA_ESTRUTURAL.json"
        self.docx.write_text("OOXML sintético para o despacho estático", encoding="utf-8")
        self.md.write_text("# Peça\n\nTexto auditado suficiente.", encoding="utf-8")
        payload = {
            "schemaVersion": 1,
            "mode": "static_ooxml_svg",
            "renderingUsed": False,
            "pdfCreated": False,
            "pngCreated": False,
            "approved": True,
            "docx": {"sha256": sha256_file(self.docx)},
            "package": {"approved": True},
            "docxLint": {"approved": True},
            "layoutAudit": {"approved": True},
            "fidelity": {"approved": True},
            "svg": [],
        }
        self.ledger.write_text(json.dumps(payload), encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_rota_estatica_nao_chama_inspect_pdf(self) -> None:
        files = {
            "docx": {"path": str(self.docx), "sha256": sha256_file(self.docx)},
            "md": {"path": str(self.md), "sha256": sha256_file(self.md)},
        }
        with patch("forja_f8_contract.inspect_pdf") as inspect, \
             patch("forja_f8_contract.audit_docx_layout", return_value={"approved": True}), \
             patch("forja_f8_contract.compare_docx_fidelity", return_value={"approved": True, "blocks": {}}):
            result = validate_f8({"path": str(self.ledger)}, files=files)
        self.assertTrue(result["approved"], result["findings"])
        self.assertFalse(result["renderingUsed"])
        inspect.assert_not_called()

    def test_rota_estatica_reprova_sinal_de_render(self) -> None:
        payload = json.loads(self.ledger.read_text(encoding="utf-8"))
        payload["renderingUsed"] = True
        self.ledger.write_text(json.dumps(payload), encoding="utf-8")
        files = {"docx": {"path": str(self.docx), "sha256": sha256_file(self.docx)}, "md": {"path": str(self.md), "sha256": sha256_file(self.md)}}
        result = validate_f8({"path": str(self.ledger)}, files=files)
        self.assertFalse(result["approved"])
        self.assertTrue(any("renderingUsed" in item for item in result["findings"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
