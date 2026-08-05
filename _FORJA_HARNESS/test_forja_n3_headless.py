import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import forja_headless


def fake_process():
    return SimpleNamespace(
        returncode=0,
        stdout=json.dumps({
            "result": "resultado controlado",
            "usage": {"input_tokens": 10, "output_tokens": 4},
            "total_cost_usd": 0,
            "session_id": "session-test",
        }),
        stderr="",
    )


class HeadlessN3Tests(unittest.TestCase):
    def test_f2_prompt_always_carries_exploration_contract(self):
        with patch.object(forja_headless.subprocess, "run", return_value=fake_process()) as runner:
            forja_headless._invoke_headless("001", "F2_CLASSIFICACAO_PRODUTO_RISCO", "classifique")
        sent_prompt = runner.call_args.args[0][2]
        self.assertIn("FORJA-F2A-100-v1", sent_prompt)
        self.assertIn("exatamente 100 perguntas", sent_prompt)

    def test_n3_writes_only_inside_attempt(self):
        with tempfile.TemporaryDirectory() as temp:
            case_dir = Path(temp) / "state" / "case-001"
            attempt = case_dir / "runs" / "run-1" / "F6_REDACAO_TEMPLATE" / "attempt-1"
            attempt.mkdir(parents=True)
            (attempt / "RUN_CONTEXT.json").write_text(json.dumps({
                "caseId": case_dir.name,
                "phase": "F6_REDACAO_TEMPLATE",
                "runId": "run-1",
                "attemptId": "attempt-1",
            }), encoding="utf-8")
            with (
                patch.object(forja_headless, "feature_enabled", return_value=True),
                patch.object(forja_headless, "resolve_case_dir", return_value=case_dir),
                patch.object(forja_headless.subprocess, "run", return_value=fake_process()),
            ):
                forja_headless.run_phase(
                    "001", "F6_REDACAO_TEMPLATE", "redija", attempt_dir=attempt)
            self.assertTrue((attempt / "HEADLESS_RESULT.md").is_file())
            self.assertTrue((attempt / "HEADLESS_USAGE.json").is_file())
            self.assertFalse((case_dir / "FORJA_STATE.json").exists())
            usage = json.loads((attempt / "HEADLESS_USAGE.json").read_text(encoding="utf-8"))
            self.assertEqual(usage["attemptId"], "attempt-1")

    def test_legacy_mode_preserves_existing_contract(self):
        with tempfile.TemporaryDirectory() as temp:
            harness = Path(temp)
            case_dir = harness / "state" / "case-abc"
            case_dir.mkdir(parents=True)
            state_path = case_dir / "FORJA_STATE.json"
            state_path.write_text(json.dumps({"artifacts": [], "phaseHistory": []}), encoding="utf-8")
            with (
                patch.object(forja_headless, "FORJA", harness),
                patch.object(forja_headless, "feature_enabled", return_value=False),
                patch.object(forja_headless.subprocess, "run", return_value=fake_process()),
            ):
                forja_headless.run_phase("abc", "F6", "redija")
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["currentPhase"], "F6")
            self.assertEqual(len(state["artifacts"]), 1)
            self.assertTrue((case_dir / "F6_HEADLESS.md").is_file())


if __name__ == "__main__":
    unittest.main()
