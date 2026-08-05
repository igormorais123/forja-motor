from __future__ import annotations

import tempfile
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import forja_reconcile
from forja_n3_common import atomic_write_json, read_json
from validate_forja_n3 import SCRIPT_TESTS


class ForjaReconcileGateHistoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.state_root = Path(self.temp.name) / "state"
        self.demanda = {"id": "d1"}
        self.integracoes = {"gmail": "offline"}
        self.evidence = {"status": "none", "detail": "sem evidência"}

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _gravar(self, findings):
        with patch.object(forja_reconcile, "STATE_DIR", self.state_root):
            case_id = forja_reconcile.gravar_state(
                self.demanda,
                findings,
                "pending",
                self.evidence,
                self.integracoes,
            )
        return read_json(self.state_root / case_id / "FORJA_STATE.json")

    def test_gate_que_deixa_de_ser_atual_e_resolvido_sem_sumir(self) -> None:
        case_dir = self.state_root / "case-d1"
        case_dir.mkdir(parents=True)
        atomic_write_json(case_dir / "FORJA_STATE.json", {
            "caseId": "case-d1",
            "createdAt": "2026-07-15T10:00:00-03:00",
            "phaseHistory": [],
            "gates": [
                {
                    "code": "COMANDO_AUSENTE",
                    "severity": "P0",
                    "detail": "Nenhum COMANDO_*.md na pasta do caso.",
                    "at": "2026-07-15T10:01:00-03:00",
                },
                {
                    "code": "SEM_PRAZO_TRIAGEM",
                    "severity": "P2",
                    "detail": "Aberta sem prazo estruturado; triagem pendente.",
                    "at": "2026-07-15T10:02:00-03:00",
                },
            ],
        })

        state = self._gravar([
            forja_reconcile.finding(
                "SEM_PRAZO_TRIAGEM",
                "P2",
                "Aberta sem prazo estruturado; triagem pendente.",
            )
        ])

        self.assertEqual(["SEM_PRAZO_TRIAGEM"], [gate["code"] for gate in state["gates"]])
        self.assertEqual("active", state["gates"][0]["status"])
        self.assertEqual("2026-07-15T10:02:00-03:00", state["gates"][0]["at"])
        self.assertEqual(1, len(state["gateHistory"]))
        resolvido = state["gateHistory"][0]
        self.assertEqual("COMANDO_AUSENTE", resolvido["code"])
        self.assertEqual("resolved", resolvido["status"])
        self.assertEqual("forja_reconcile:F0", resolvido["resolvedBy"])
        self.assertTrue(resolvido["resolvedAt"])
        self.assertEqual(
            "finding_not_observed_in_current_reconciliation",
            resolvido["resolution"],
        )

        repetido = self._gravar([
            forja_reconcile.finding(
                "SEM_PRAZO_TRIAGEM",
                "P2",
                "Aberta sem prazo estruturado; triagem pendente.",
            )
        ])
        self.assertEqual(1, len(repetido["gateHistory"]))

    def test_runner_referencia_o_script_f7_no_destino_atual(self) -> None:
        caminho = "_scripts_oneoff/validate_f7_integration.py"
        self.assertIn(caminho, SCRIPT_TESTS)
        raiz = Path(__file__).resolve().parent
        self.assertTrue((raiz / caminho).is_file())
        processo = subprocess.run(
            [sys.executable, caminho],
            cwd=raiz,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            check=False,
        )
        self.assertEqual(0, processo.returncode, processo.stdout + processo.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
