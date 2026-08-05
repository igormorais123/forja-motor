"""Tests for provenance tracking in context validation.

Verifies that findings for unknown provenance references include:
1. gateCode: identifier of the gate that originated the finding
2. anchor: minimal information to reconstruct the block (blockId, lines, text excerpt)

This satisfies the auditability requirement: readers can now trace which gate
generated each finding without external documentation.
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from forja_context import (
    markdown_blocks,
    validate_context,
    validate_paragraph_provenance,
)
from forja_n3_common import atomic_write_json


class ProvenanceTraceabilityTests(unittest.TestCase):
    """Tests for gate code and anchor in unknown_provenance_reference findings."""

    def test_unknown_provenance_reference_includes_gate_code(self) -> None:
        """Achado unknown_provenance_reference deve incluir gateCode."""
        markdown = "Parágrafo com afirmação bem desenvolvida que refere fato inexistente no ledger de forma explícita e clara.\n"
        blocks = markdown_blocks(markdown)
        para_block = blocks[0]  # O parágrafo significativo

        provenance = {
            "blocks": [{
                "blockId": para_block["blockId"],
                "factIds": ["fact-unknown"],
                "propositionIds": [],
            }]
        }
        fact_payload = {"facts": []}
        proposition_payload = {"propositions": []}

        blocks_result, findings = validate_paragraph_provenance(
            markdown, provenance, fact_payload, proposition_payload
        )

        # Deve haver um achado P0 para referência desconhecida
        p0_findings = [f for f in findings if f["code"] == "unknown_provenance_reference"]
        self.assertEqual(1, len(p0_findings), f"Esperava 1 achado, obtive {len(p0_findings)}: {findings}")

        # Novo campo: gateCode rastreável
        finding = p0_findings[0]
        self.assertIn("gateCode", finding, "Finding sem gateCode — rastreabilidade perdida")
        self.assertIsInstance(finding["gateCode"], str)
        self.assertTrue(finding["gateCode"], "gateCode vazio")

    def test_unknown_provenance_reference_includes_anchor(self) -> None:
        """Achado unknown_provenance_reference deve incluir anchor minimo."""
        markdown = "## Seção\n\nParágrafo bem desenvolvido que refere fato inexistente no ledger de forma clara e objetiva.\n"
        blocks = markdown_blocks(markdown)
        para_block = next((b for b in blocks if b["kind"] == "paragraph"), None)
        self.assertIsNotNone(para_block)

        provenance = {
            "blocks": [{
                "blockId": para_block["blockId"],
                "factIds": ["fact-nao-existe"],
                "propositionIds": [],
            }]
        }
        fact_payload = {"facts": []}
        proposition_payload = {"propositions": []}

        blocks_result, findings = validate_paragraph_provenance(
            markdown, provenance, fact_payload, proposition_payload
        )

        p0_findings = [f for f in findings if f["code"] == "unknown_provenance_reference"]
        self.assertEqual(1, len(p0_findings), f"Esperava 1 P0, obtive: {findings}")

        finding = p0_findings[0]
        self.assertIn("anchor", finding, "Finding sem anchor — reconstrução impossível")
        anchor = finding["anchor"]
        self.assertIsInstance(anchor, dict)

        # Campos mínimos do anchor: blockId, linhas
        self.assertIn("blockId", anchor)
        self.assertEqual(para_block["blockId"], anchor["blockId"])
        self.assertIn("startLine", anchor)
        self.assertIn("endLine", anchor)
        self.assertIsInstance(anchor["startLine"], int)
        self.assertIsInstance(anchor["endLine"], int)

    def test_anchor_includes_text_excerpt(self) -> None:
        """Anchor deve incluir excerpt do texto para auditoria visual."""
        markdown = "Aqui vem um parágrafo bem longo com conteúdo específico que permite reconstruir o contexto de forma clara e precisa.\n"
        blocks = markdown_blocks(markdown)
        para_block = blocks[0]

        provenance = {
            "blocks": [{
                "blockId": para_block["blockId"],
                "factIds": ["unknown-fact"],
                "propositionIds": [],
            }]
        }
        fact_payload = {"facts": []}
        proposition_payload = {"propositions": []}

        blocks_result, findings = validate_paragraph_provenance(
            markdown, provenance, fact_payload, proposition_payload
        )

        p0_findings = [f for f in findings if f["code"] == "unknown_provenance_reference"]
        self.assertEqual(1, len(p0_findings), f"Esperava 1, obtive {findings}")
        finding = p0_findings[0]
        anchor = finding["anchor"]

        # Deve ter excerpt — resumo legível do bloco
        self.assertIn("text", anchor, "Anchor sem excerpt — não há pista visual")
        self.assertIsInstance(anchor["text"], str)
        self.assertGreater(len(anchor["text"]), 0)

    def test_backward_compatibility_no_keyerror_on_missing_gate_code(self) -> None:
        """Leitores antigos não podem quebrar por ausência de gateCode (compatibilidade)."""
        markdown = "Parágrafo de teste.\n"
        provenance = {
            "blocks": [{
                "blockId": "b0003-test",
                "factIds": ["x"],
                "propositionIds": [],
            }]
        }
        fact_payload = {"facts": []}
        proposition_payload = {"propositions": []}

        blocks, findings = validate_paragraph_provenance(
            markdown, provenance, fact_payload, proposition_payload
        )

        # Simula leitor antigo que usa .get("gateCode")
        for finding in findings:
            gate_code = finding.get("gateCode")  # Não deve dar KeyError
            if gate_code:
                self.assertIsInstance(gate_code, str)

    def test_complete_context_validation_with_gate_codes(self) -> None:
        """Teste de integração: validate_context produz achados rastreáveis."""
        with tempfile.TemporaryDirectory() as temp:
            case = Path(temp)
            markdown = "Parágrafo bem desenvolvido que refere fato e proposição de forma clara e significativa com conteúdo suficiente.\n"
            md_path = case / "draft.md"
            md_path.write_text(markdown, encoding="utf-8")

            blocks = markdown_blocks(markdown)
            para_block = next((b for b in blocks if b["kind"] == "paragraph"), None)
            self.assertIsNotNone(para_block, f"Nenhum parágrafo significativo encontrado. Blocos: {blocks}")

            # Setup: documento, cobertura, fatos, proposições, provenance
            atomic_write_json(case / "F1_DOCUMENT_INDEX.json", {
                "documents": [{"sourceId": "doc-1", "sha256": "a", "pageCount": 1, "critical": True}]
            })
            atomic_write_json(case / "F1_COVERAGE.json", {
                "documents": [{"sourceId": "doc-1", "ranges": [{"start": 1, "end": 1, "status": "verified"}], "extractionStatus": "ok"}]
            })
            # Fatos existentes
            atomic_write_json(case / "F3_FACT_LEDGER.json", {
                "facts": [
                    {"factId": "known-fact", "classification": "PROVADO", "finalUseAllowed": True,
                     "sources": [{"sourceId": "doc-1", "pageOrEvent": "p. 1"}]}
                ]
            })
            atomic_write_json(case / "F4_PROPOSITION_LEDGER.json", {
                "propositions": [{"propositionId": "known-prop"}]
            })
            # Provenance: bloco refere fato DESCONHECIDO
            atomic_write_json(case / "F6_PARAGRAPH_PROVENANCE.json", {
                "markdownPath": "draft.md",
                "blocks": [{
                    "blockId": para_block["blockId"],
                    "factIds": ["unknown-fact"],  # Não existe em F3_FACT_LEDGER
                    "propositionIds": ["known-prop"],
                }]
            })

            result = validate_context(case)

            # Deve haver achado P0
            self.assertFalse(result["approved"])
            self.assertGreater(result["p0"], 0)

            # Achado deve ter gateCode e anchor
            unknown_refs = [f for f in result["findings"] if f["code"] == "unknown_provenance_reference"]
            self.assertEqual(1, len(unknown_refs))

            finding = unknown_refs[0]
            self.assertIn("gateCode", finding)
            self.assertIn("anchor", finding)

            # Anchor deve ter as informações mínimas
            anchor = finding["anchor"]
            self.assertIn("blockId", anchor)
            self.assertIn("startLine", anchor)
            self.assertIn("endLine", anchor)


class BackwardCompatibilityTests(unittest.TestCase):
    """Testes para garantir que leitores antigos continuam funcionando."""

    def test_readers_using_get_method_do_not_break(self) -> None:
        """Código que usa .get('gateCode') não quebra com KeyError."""
        markdown = "Teste.\n"
        provenance = {"blocks": [{"blockId": "b0004", "factIds": ["x"], "propositionIds": []}]}

        blocks, findings = validate_paragraph_provenance(
            markdown, provenance, {"facts": []}, {"propositions": []}
        )

        # Simula consumidor que usa .get() — modo seguro
        for finding in findings:
            code = finding.get("code")
            gate = finding.get("gateCode")  # Novo campo
            severity = finding.get("severity")
            # Nenhum desses deve dar KeyError
            self.assertIsNotNone(severity)

    def test_findings_without_gate_code_still_readable(self) -> None:
        """Achados sem gateCode (legados) ainda são iteráveis."""
        # Simula um achado antigo sem o novo campo
        old_finding = {
            "severity": "P0",
            "code": "unknown_provenance_reference",
            "blockId": "b0005-old",
            "factIds": ["x"],
            "propositionIds": [],
        }

        # Consumidor que não conhece gateCode
        self.assertEqual(old_finding.get("code"), "unknown_provenance_reference")
        self.assertIsNone(old_finding.get("gateCode"))  # Campo ausente
        self.assertIsNotNone(old_finding.get("severity"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
