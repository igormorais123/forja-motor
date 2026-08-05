from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from forja_ar_architecture import (
    _cycle_count,
    _tracked_vault_leaks,
    automation_enabled,
    create_candidate,
    validate_candidate,
    validate_manifest,
)
from forja_n3_common import ForjaN3Error
from forja_post_protocol import ingest_return, promote_learning, rebuild_comparison


class ArchitectureAutoresearchTests(unittest.TestCase):
    def test_feature_off_is_real_rollback_switch(self) -> None:
        self.assertTrue(automation_enabled({"features": {"n4PostProtocolV1": True}}))
        self.assertFalse(automation_enabled({"features": {"n4PostProtocolV1": False}}))

    def test_cycle_counter_detects_relevant_scc(self) -> None:
        self.assertEqual(0, _cycle_count({"a": {"b"}, "b": set()}))
        self.assertEqual(1, _cycle_count({"a": {"b"}, "b": {"a"}}))

    def test_missing_manifest_contract_fails_closed(self) -> None:
        self.assertTrue(validate_manifest({}))

    def test_feature_off_blocks_every_mutating_entry_point(self) -> None:
        with patch("forja_post_protocol.feature_enabled", return_value=False):
            calls = [
                lambda: ingest_return(
                    Path("case"),
                    Path("missing.pdf"),
                    account_id="a",
                    thread_id="t",
                    message_id="m",
                    attachment_id="x",
                    received_at="2026-01-01T00:00:00-03:00",
                ),
                lambda: promote_learning(
                    Path("case"),
                    "missing",
                    approved_by="a",
                    fixture_id="x",
                    test_id="x",
                    evidence_runs=["r"],
                ),
                lambda: rebuild_comparison(Path("case"), "missing"),
            ]
            for call in calls:
                with self.subTest(call=call), self.assertRaisesRegex(ForjaN3Error, "desabilitado"):
                    call()

    def test_git_leak_detection_handles_accented_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            leaked = repo / "_FORJA_HARNESS" / "state" / "case" / "PEÇA PROTOCOLADA — TESTE" / "x.txt"
            leaked.parent.mkdir(parents=True)
            leaked.write_text("x", encoding="utf-8")
            subprocess.run(["git", "add", "--", str(leaked)], cwd=repo, check=True)
            leaks = _tracked_vault_leaks(repo)
        self.assertEqual(1, len(leaks))
        self.assertIn("PEÇA PROTOCOLADA — TESTE", leaks[0])

    def test_candidate_is_separate_descriptive_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with patch("forja_ar_architecture.CANDIDATE_ROOT", root):
                path = create_candidate(
                    "post-protocol-test",
                    title="Loop pós-protocolo transacional e reversível",
                    problem="Retornos humanos não produziam aprendizado arquitetural verificável.",
                    hypothesis="Eventos, contratos e canários reduzem erros sem autoeditar produção.",
                    scope=["F10", "event-store"],
                )
                candidate = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual("AR-Architecture", candidate["lineage"])
        self.assertEqual("proposed", candidate["status"])
        self.assertFalse(candidate["proposal"]["productionMutation"])
        self.assertEqual([], validate_candidate(candidate))


if __name__ == "__main__":
    unittest.main(verbosity=2)
