from __future__ import annotations

import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from forja_n3_common import PHASES, RevisionConflict, TransitionError
from forja_state_machine import derive_state, initialize_case, load_events, record_event


class ForjaN3StateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.case = Path(self.temp.name) / "case-test"
        self.case.mkdir()
        initialize_case(self.case, demand_id="demand-test")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def event(self, event_type: str, revision: int, key: str, *, phase: str | None = None, payload: dict | None = None):
        return record_event(
            self.case,
            event_type,
            expected_revision=revision,
            idempotency_key=key,
            phase=phase,
            payload=payload or {},
        )

    def complete_phase(self, phase: str, revision: int) -> int:
        self.event("phase_started", revision, f"{phase}:start", phase=phase)
        self.event("phase_completed", revision + 1, f"{phase}:done", phase=phase)
        return revision + 2

    def test_progression_and_recovery(self) -> None:
        revision = self.complete_phase(PHASES[0], 1)
        revision = self.complete_phase(PHASES[1], revision)
        state = derive_state(self.case)
        self.assertEqual(revision, state["revision"])
        self.assertEqual(PHASES[1], state["phaseCursor"])
        self.assertEqual(PHASES[:2], tuple(state["completedPhases"]))
        (self.case / "FORJA_N3_STATE.json").unlink()
        recovered = derive_state(self.case, load_events(self.case))
        self.assertEqual(state["stateHash"], recovered["stateHash"])

    def test_regression_requires_reopen(self) -> None:
        revision = self.complete_phase(PHASES[0], 1)
        revision = self.complete_phase(PHASES[1], revision)
        with self.assertRaises(TransitionError):
            self.event("phase_started", revision, "silent-regression", phase=PHASES[0])
        self.event(
            "gate_reopened",
            revision,
            "reopen-f0",
            phase=PHASES[0],
            payload={"reason": "nova inconsistência"},
        )
        _, state, _ = self.event("phase_started", revision + 1, "retry-f0", phase=PHASES[0])
        self.assertEqual("running", state["lifecycleStatus"])
        self.assertIn(PHASES[1], state["invalidatedPhases"])

    def test_idempotency(self) -> None:
        first, state, created = self.event("phase_started", 1, "same-key", phase=PHASES[0])
        self.assertTrue(created)
        second, state2, created2 = self.event("phase_started", 999, "same-key", phase=PHASES[0])
        self.assertFalse(created2)
        self.assertEqual(first["eventId"], second["eventId"])
        self.assertEqual(state["revision"], state2["revision"])

    def test_concurrent_revision_conflict(self) -> None:
        outcomes: list[str] = []
        barrier = threading.Barrier(2)

        def worker(name: str) -> None:
            barrier.wait()
            try:
                self.event("phase_started", 1, f"worker-{name}", phase=PHASES[0])
                outcomes.append("ok")
            except RevisionConflict:
                outcomes.append("conflict")

        threads = [threading.Thread(target=worker, args=(str(index),)) for index in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(["conflict", "ok"], sorted(outcomes))
        self.assertEqual(2, len(load_events(self.case)))

    def test_partial_event_is_ignored(self) -> None:
        events_dir = self.case / "events"
        (events_dir / ".evt-partial.tmp").write_text("{", encoding="utf-8")
        self.assertEqual(1, len(load_events(self.case)))

    def test_returned_state_includes_synchronous_management_ack(self) -> None:
        def acknowledge(case_dir, event):
            record_event(
                case_dir,
                "sync_succeeded",
                expected_revision=event["eventSeq"],
                idempotency_key=f"test-sync:{event['eventSeq']}",
                payload={"syncedEventSeq": event["eventSeq"]},
            )
            return {"status": "ok"}

        with patch("forja_management_bridge.sync_after_event", side_effect=acknowledge):
            _, state, _ = self.event("phase_started", 1, "phase-with-sync", phase=PHASES[0])
        self.assertEqual(3, state["revision"])
        self.assertEqual("ok", state["sync"]["status"])

    def test_legacy_highest_phase_blocks_silent_regression(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            case_dir = Path(temp) / "case-legacy-regression"
            case_dir.mkdir()
            (case_dir / "FORJA_STATE.json").write_text(json.dumps({
                "currentPhase": PHASES[5],
                "status": "draft_awaiting_review",
                "phaseHistory": [
                    {"phase": PHASES[9], "status": "ok"},
                    {"phase": PHASES[5], "status": "pendencias"},
                ],
                "inputs": {},
            }), encoding="utf-8")
            initialize_case(case_dir, from_legacy=True)
            with self.assertRaises(TransitionError):
                record_event(
                    case_dir,
                    "phase_started",
                    expected_revision=1,
                    idempotency_key="legacy-silent-f5",
                    phase=PHASES[5],
                )
            record_event(
                case_dir,
                "gate_reopened",
                expected_revision=1,
                idempotency_key="legacy-reopen-f5",
                phase=PHASES[5],
                payload={"reason": "fonte pendente"},
            )
            _, state, _ = record_event(
                case_dir,
                "phase_started",
                expected_revision=2,
                idempotency_key="legacy-retry-f5",
                phase=PHASES[5],
            )
            self.assertEqual(PHASES[5], state["phaseCursor"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
