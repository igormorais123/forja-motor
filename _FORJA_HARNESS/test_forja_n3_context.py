from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from forja_context import (
    markdown_blocks,
    validate_context,
    validate_coverage,
    validate_fact_ledger,
)
from forja_n3_common import atomic_write_json


class ForjaN3ContextTests(unittest.TestCase):
    def test_markdown_parser_preserves_h4_and_blockquote(self) -> None:
        blocks = markdown_blocks("#### 4.1 Subtítulo\n\n> Citação importante\n\nParágrafo material com conteúdo suficiente para lastro jurídico.")
        self.assertEqual(["heading", "blockquote", "paragraph"], [item["kind"] for item in blocks])
        self.assertIn("####", blocks[0]["text"])

    def test_coverage_detects_missing_page(self) -> None:
        index = {"documents": [{"sourceId": "doc-1", "sha256": "a", "pageCount": 3, "critical": True}]}
        coverage = {"documents": [{"sourceId": "doc-1", "ranges": [{"start": 1, "end": 2, "status": "read"}]}]}
        findings = validate_coverage(index, coverage)
        self.assertEqual([3], findings[0]["pages"])
        self.assertEqual("P0", findings[0]["severity"])

    def test_unverified_fact_cannot_allow_final_use(self) -> None:
        findings = validate_fact_ledger(
            {"facts": [{"factId": "fact-1", "classification": "NAO_VERIFICADO", "finalUseAllowed": True}]},
            [],
        )
        self.assertTrue(any(item["code"] == "unsafe_final_use" for item in findings))

    def test_complete_context_is_approved(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            case = Path(temp)
            markdown = "## Mérito\n\nA contratação ocorreu em 10/01/2026 e está comprovada no documento principal.\n"
            md_path = case / "draft.md"
            md_path.write_text(markdown, encoding="utf-8")
            block = next(item for item in markdown_blocks(markdown) if item["kind"] == "paragraph")
            atomic_write_json(case / "F1_DOCUMENT_INDEX.json", {"documents": [{"sourceId": "doc-1", "sha256": "a", "pageCount": 1, "critical": True}]})
            atomic_write_json(case / "F1_COVERAGE.json", {"documents": [{"sourceId": "doc-1", "ranges": [{"start": 1, "end": 1, "status": "verified"}], "extractionStatus": "ok"}]})
            atomic_write_json(case / "F3_FACT_LEDGER.json", {"facts": [{"factId": "fact-1", "classification": "PROVADO", "finalUseAllowed": True, "sources": [{"sourceId": "doc-1", "pageOrEvent": "p. 1"}]}]})
            atomic_write_json(case / "F4_PROPOSITION_LEDGER.json", {"propositions": [{"propositionId": "prop-1"}]})
            atomic_write_json(case / "F6_PARAGRAPH_PROVENANCE.json", {"markdownPath": "draft.md", "blocks": [{"blockId": block["blockId"], "factIds": ["fact-1"], "propositionIds": ["prop-1"]}]})
            result = validate_context(case)
            self.assertTrue(result["approved"], result["findings"])
            self.assertEqual(0, result["p0"])

    def test_missing_ledgers_write_blocking_validation_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            case = Path(temp)
            result = validate_context(case)
            artifact = case / "CONTEXT_VALIDATION.json"
            self.assertFalse(result["approved"])
            self.assertEqual(5, result["p0"])
            self.assertTrue(artifact.is_file())
            self.assertIn('"missing_ledger"', artifact.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
