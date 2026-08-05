import tempfile
import unittest
from pathlib import Path

from forja_n3_common import PHASES
from forja_run_metrics import build_metrics, write_metrics
from forja_state_machine import initialize_case, record_event


class RunMetricsTests(unittest.TestCase):
    def test_metrics_follow_events_and_are_materialized(self):
        with tempfile.TemporaryDirectory() as temp:
            case_dir = Path(temp) / "case-metrics"
            case_dir.mkdir()
            initialize_case(case_dir, demand_id="d-1")
            record_event(
                case_dir,
                "phase_started",
                expected_revision=1,
                idempotency_key="start",
                phase=PHASES[0],
            )
            record_event(
                case_dir,
                "phase_blocked",
                expected_revision=2,
                idempotency_key="blocked",
                phase=PHASES[0],
                payload={"reason": "fonte ausente", "blockers": ["fonte ausente"]},
            )
            metrics = build_metrics(case_dir)
            self.assertEqual(metrics["attemptsByPhase"][PHASES[0]], 1)
            self.assertEqual(metrics["blockedByPhase"][PHASES[0]], 1)
            self.assertEqual(metrics["context"]["status"], "not_run")
            write_metrics(case_dir)
            self.assertTrue((case_dir / "FORJA_RUN_METRICS.json").is_file())


if __name__ == "__main__":
    unittest.main()
