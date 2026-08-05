from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from forja_pso_pet import (
    _valid_fixture,
    audit_n4_case,
    measure_plan,
    mutation_benchmark,
    validate_plan,
)


def codes(findings: list[dict]) -> set[str]:
    return {item["code"] for item in findings}


class PsoPetTests(unittest.TestCase):
    def test_valid_fixture_has_no_findings_and_no_hidden_composite(self):
        fixture = _valid_fixture()
        self.assertEqual([], validate_plan(fixture))
        profile = measure_plan(fixture)
        self.assertIsNone(profile["compositeScore"])
        self.assertEqual("ready_for_human_review", profile["decisionReadiness"])
        self.assertTrue(all(value["score"] >= 80 for value in profile["dimensions"].values()))

    def test_output_cannot_prove_input_state(self):
        fixture = _valid_fixture()
        fixture["problemDefinition"]["currentStateEvidenceIds"] = ["FINAL"]
        self.assertIn("PSO-SOURCE-CIRCULAR", codes(validate_plan(fixture)))

    def test_direct_and_ultimate_outcome_must_be_separate(self):
        fixture = _valid_fixture()
        fixture["problemDefinition"]["ultimateOutcome"] = fixture["problemDefinition"]["directOutcome"]
        self.assertIn("PSO-PROBLEM-OUTCOME-CONFLATION", codes(validate_plan(fixture)))

    def test_full_profile_requires_distinct_viable_alternative(self):
        fixture = _valid_fixture()
        fixture["options"] = fixture["options"][:1]
        self.assertIn("PSO-OPTION-ALTERNATIVES", codes(validate_plan(fixture)))

    def test_duplicate_labelled_option_does_not_count(self):
        fixture = _valid_fixture()
        fixture["options"][1].update({
            "vehicle": fixture["options"][0]["vehicle"],
            "mechanism": fixture["options"][0]["mechanism"],
            "evidenceStrategy": fixture["options"][0]["evidenceStrategy"],
        })
        self.assertIn("PSO-OPTION-DUPLICATE", codes(validate_plan(fixture)))

    def test_material_requirement_needs_validation_trace(self):
        fixture = _valid_fixture()
        fixture["validation"]["requirementChecks"] = fixture["validation"]["requirementChecks"][:1]
        self.assertIn("PSO-TRACE-MISSING", codes(validate_plan(fixture)))

    def test_context_dump_is_detected_without_becoming_silent(self):
        fixture = _valid_fixture()
        fixture["contextPlan"]["issuePackets"][0]["embeddedText"] = "x" * 2501
        findings = validate_plan(fixture)
        self.assertIn("PSO-CONTEXT-BLOAT", codes(findings))
        self.assertTrue(any(x["code"] == "PSO-CONTEXT-BLOAT" and x["severity"] == "p1" for x in findings))

    def test_prospective_timing_is_interpreted(self):
        fixture = _valid_fixture()
        fixture["frozenAt"] = "2026-07-11T12:00:00-03:00"
        self.assertIn("PSO-TIME-ORDER", codes(validate_plan(fixture)))

    def test_mutation_benchmark_has_full_recall_and_no_false_blocking(self):
        result = mutation_benchmark()
        self.assertEqual(1.0, result["semanticMutationRecall"])
        self.assertEqual(0.0, result["falseBlockingRate"])

    def test_missing_plan_is_not_scored_as_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp) / "case-empty"
            (case / "n4_artifacts").mkdir(parents=True)
            report = audit_n4_case(case)
            self.assertEqual("not_measured", report["methodStatus"])
            self.assertEqual("not_evaluated", report["valueProfile"]["decisionReadiness"])
            self.assertTrue(all(x["score"] is None for x in report["valueProfile"]["dimensions"].values()))

    def test_audit_finds_final_output_circularity_and_literal_only_suite(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp) / "case-audit"
            n4 = case / "n4_artifacts"
            n4.mkdir(parents=True)
            (n4 / "F2_QUESTION_TREE.json").write_text(json.dumps({"questions": [{"questionId": "Q1", "supportIds": ["FINAL"]}]}), encoding="utf-8")
            (n4 / "F3_REASONING_GRAPH.json").write_text(json.dumps({"nodes": [{"id": "FINAL", "sourceArtifact": "CANONICAL_TEXT_FROM_FINAL_DOCX.txt"}]}), encoding="utf-8")
            (n4 / "F4_THESIS_MATURITY.json").write_text(json.dumps({"theses": []}), encoding="utf-8")
            (n4 / "F4_CASE_ACCEPTANCE_TESTS.json").write_text(json.dumps({"executionMode": "retrospective_baseline", "tests": [{"method": "deterministic", "evaluator": {"kind": "contains"}}]}), encoding="utf-8")
            report = audit_n4_case(case)
            found = codes(report["findings"])
            self.assertIn("PSO-AUDIT-CIRCULAR-EVIDENCE", found)
            self.assertIn("PSO-AUDIT-LITERAL-ONLY", found)
            self.assertIn("PSO-AUDIT-RETROSPECTIVE", found)


if __name__ == "__main__":
    unittest.main()
