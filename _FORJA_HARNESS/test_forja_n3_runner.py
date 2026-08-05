from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from forja_n3_common import PHASES, ForjaN3Error, atomic_write_json, read_json
from forja_phase_contracts import load_contract, validate_all
from forja_run import prepare_attempt, promote_attempt
from forja_state_machine import derive_state, initialize_case


class ForjaN3RunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.source = root / "source case"
        self.source.mkdir()
        (self.source / "COMANDO_DO_EMAIL.md").write_text("# Comando\n", encoding="utf-8")
        self.case = root / "case-runner"
        self.case.mkdir()
        atomic_write_json(
            self.case / "FORJA_STATE.json",
            {
                "specVersion": "N2.0",
                "currentPhase": "F0_RECONCILIACAO_FILA",
                "status": "pending",
                "inputs": {
                    "demandId": "demand-runner",
                    "caseFolder": str(self.source),
                    "commandFile": "COMANDO_DO_EMAIL.md",
                },
            },
        )
        initialize_case(self.case, from_legacy=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_result(self, attempt: Path, *, valid: bool = True) -> None:
        contract = load_contract(PHASES[0])
        # F0 passou a recomputar `mapping_valid`; o fixture precisa representar
        # um manifesto mínimo, mas real, em vez de testar a antiga rota que
        # promovia `{}` sem conferir o caso.
        atomic_write_json(
            attempt / "case_manifest.json",
            {
                "caseId": "case-runner",
                "demandId": "demand-runner",
                "caseFolder": str(self.source),
                "commandFile": str(self.source / "COMANDO_DO_EMAIL.md"),
            },
        )
        (attempt / "reconciliation.md").write_text(
            "# Reconciliação\n\n## Status\n\nNenhuma inconsistência detectada.\n",
            encoding="utf-8")
        gates = {gate: "pass" for gate in contract["requiredGates"]}
        if not valid:
            gates[contract["requiredGates"][0]] = "blocked"
        atomic_write_json(
            attempt / "PHASE_RESULT.json",
            {
                "status": "pass",
                "producer": "producer-run",
                "reviewer": "reviewer-run",
                "producerRole": contract["producerRole"],
                "reviewerRole": contract["reviewerRole"],
                "gates": gates,
                "artifacts": [
                    {"id": "case_manifest", "path": "case_manifest.json"},
                    {"id": "reconciliation_report", "path": "reconciliation.md"},
                ],
            },
        )

    def test_contracts_are_complete(self) -> None:
        self.assertEqual(11, len(validate_all()))

    def test_attempt_promotes_only_validated_outputs(self) -> None:
        prepared = prepare_attempt(self.case, PHASES[0], expected_revision=1, run_id="run-test")
        attempt = Path(prepared["attemptDir"])
        self.write_result(attempt)
        promoted = promote_attempt(self.case, attempt, expected_revision=2)
        state = promoted["state"]
        self.assertEqual(5, state["revision"])
        self.assertIn(PHASES[0], state["completedPhases"])
        self.assertEqual({"case_manifest", "reconciliation_report"}, set(promoted["promoted"]))
        for entry in promoted["promoted"].values():
            self.assertTrue(Path(entry["path"]).is_file())

    def test_failed_gate_does_not_promote(self) -> None:
        prepared = prepare_attempt(self.case, PHASES[0], expected_revision=1, run_id="run-fail")
        attempt = Path(prepared["attemptDir"])
        self.write_result(attempt, valid=False)
        with self.assertRaises(ForjaN3Error):
            promote_attempt(self.case, attempt, expected_revision=2)
        state = derive_state(self.case)
        self.assertEqual(2, state["revision"])
        self.assertFalse((self.case / "n3_artifacts").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
