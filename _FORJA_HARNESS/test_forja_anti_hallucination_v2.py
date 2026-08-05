from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from forja_authorities import authority_key, extract_authorities
from forja_claim_binding import bind_claims
from forja_delivery import f7_com_lastro
from forja_editorial_fidelity import PROTOCOL_VERSION, validate_editorial_bundle
from forja_n3_common import ForjaN3Error, atomic_write_json, canonical_hash, read_json, sha256_file
from forja_official_sources import source_excerpt_sha256
from forja_package import (
    _protocolable_content,
    revalidate_package_manifest,
    validate_source_ledger,
)


class AntiHallucinationV2Tests(unittest.TestCase):
    def test_inventory_covers_less_common_classes_and_norms(self) -> None:
        text = (
            "O HC 9.999.999/STJ, o RMS 8.888.888/STJ e a Rcl 12.345/STF "
            "aplicariam o art. 999 do CPC e a Lei 99.999/2099."
        )
        keys = {authority_key(item) for item in extract_authorities(text)}
        self.assertIn(("STJ", "HC", "9999999"), keys)
        self.assertIn(("STJ", "RMS", "8888888"), keys)
        self.assertIn(("STF", "RCL", "12345"), keys)
        self.assertIn(("CPC", "ARTICLE", "999"), keys)
        self.assertIn(("BR", "LEI", "99999"), keys)

    def test_ambiguous_high_court_reference_is_explicit(self) -> None:
        item = extract_authorities("O HC 7777777 resolveria a causa.")[0]
        self.assertEqual("TRIBUNAL_AMBIGUO", item["corte"])

    def test_legacy_f7_recomputes_fake_hc_and_law(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            markdown = Path(temp) / "piece.md"
            markdown.write_text(
                "O HC 9999999/STJ e o art. 999 do CPC autorizariam o pedido.",
                encoding="utf-8",
            )
            ok, reason = f7_com_lastro({
                "p0": 0,
                "arquivo": str(markdown),
                "mdSha256": sha256_file(markdown),
            })
            self.assertFalse(ok)
            self.assertIn("sem lastro", reason)

    def test_generic_claim_cannot_cover_false_final_proposition(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            markdown = root / "final.md"
            markdown.write_text(
                "O REsp 1234567/STJ não autoriza a medida excepcional.",
                encoding="utf-8",
            )
            source = root / "source.txt"
            source.write_text("STJ REsp 1234567\nTexto oficial suficiente.", encoding="utf-8")
            receipt = root / "receipt.json"
            atomic_write_json(receipt, {"signatureBase64": "stub"})
            identity = {"court": "STJ", "kind": "RESP", "number": "1234567"}
            false_proposition = "O REsp 1234567/STJ autoriza a medida excepcional."
            entry = {
                "id": "resp-1234567",
                "claim": "O precedente existe.",
                "generatorRunId": "writer-1",
                "finalUseAllowed": True,
                "sourcePathOrUrl": str(source),
                "sourceSha256": sha256_file(source),
                "sourceUrl": "https://processo.stj.jus.br/",
                "sourceIdentity": identity,
                "sourceExcerpt": "Texto oficial suficiente.",
                "sourceExcerptSha256": source_excerpt_sha256("Texto oficial suficiente."),
                "documentSha256": sha256_file(markdown),
                "documentProposition": false_proposition,
                "documentPropositionSha256": canonical_hash({"proposition": false_proposition}),
                "documentParagraphIndex": 1,
                "documentParagraphSha256": canonical_hash({
                    "paragraph": markdown.read_text(encoding="utf-8").strip()
                }),
                "authorityIdentity": identity,
                "authorityIdentitySha256": canonical_hash(identity),
                "claimReview": {
                    "status": "pass",
                    "receiptPath": str(receipt),
                    "receiptSha256": sha256_file(receipt),
                },
            }
            ledger = root / "ledger.json"
            atomic_write_json(ledger, {"entries": [entry]})
            source_validation = {
                "approved": True,
                "findings": [],
                "record": {"sourceUrl": entry["sourceUrl"], "identity": identity},
            }
            with patch("forja_package.validate_source_path", return_value=source_validation), patch(
                "forja_package.validate_claim_review_receipt",
                return_value={"approved": True, "findings": []},
            ):
                result = validate_source_ledger(
                    {"path": str(ledger)},
                    release_policy="strict_protocol",
                    expected_citations=extract_authorities(markdown.read_text(encoding="utf-8")),
                    markdown={"path": str(markdown), "sha256": sha256_file(markdown)},
                )
            self.assertFalse(result["approved"])
            self.assertTrue(
                any("não consta literalmente" in item for item in result["blocked"]),
                result["blocked"],
            )

    def test_editorial_semantic_inversion_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "audited.md"
            final = root / "final.md"
            report = root / "report.json"
            source.write_text(
                "# FUNDAMENTO\n\nO REsp 1.234.567/STJ não autoriza a medida excepcional.\n",
                encoding="utf-8",
            )
            final.write_text(
                "# FUNDAMENTO\n\nO REsp 1.234.567/STJ autoriza a medida excepcional.\n",
                encoding="utf-8",
            )
            atomic_write_json(report, {
                "protocolVersion": PROTOCOL_VERSION,
                "model": "claude-fable-5",
                "billing": "assinatura OAuth Claude Max (sem API key)",
                "sourceSha256": sha256_file(source),
                "finalSha256": sha256_file(final),
                "fableReport": {"sourceHash": sha256_file(source)},
            })
            result = validate_editorial_bundle(source, final, report)
            self.assertFalse(result["approved"])
            self.assertTrue(any(
                item["gate"] == "authority_semantic_polarity_preserved"
                for item in result["findings"]
            ))

    def test_protocolable_content_cannot_be_downgraded_and_old_package_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            markdown = root / "piece.md"
            markdown.write_text(
                "Excelentíssimo Senhor Juiz de Direito\n\nTermos em que, pede deferimento.",
                encoding="utf-8",
            )
            self.assertTrue(_protocolable_content(
                {"id": "nota", "role": "interno", "audience": "office_review"},
                {"path": str(markdown)},
            ))
            result = revalidate_package_manifest(root, {"schemaVersion": 1})
            self.assertFalse(result["approved"])
            self.assertTrue(result["stale"])

    def test_binding_tool_covers_inventory_and_resets_signature(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            markdown = root / "final.md"
            paragraph = "O HC 9999999/STJ não autoriza a medida excepcional."
            markdown.write_text(paragraph + "\n", encoding="utf-8")
            identity = {"court": "STJ", "kind": "HC", "number": "9999999"}
            draft = root / "draft.json"
            output = root / "verified.json"
            atomic_write_json(draft, {"entries": [{
                "id": "hc-9999999",
                "claim": "Efeito do HC sobre a medida.",
                "documentProposition": paragraph,
                "documentParagraphIndex": 1,
                "authorityIdentity": identity,
                "claimReview": {"status": "pass", "receiptPath": "recibo-antigo.json"},
            }]})
            result = bind_claims(markdown, draft, output)
            self.assertEqual(1, len(result["entries"]))
            self.assertEqual(
                "pending_new_signature",
                result["entries"][0]["claimReview"]["status"],
            )
            self.assertEqual(sha256_file(markdown), result["entries"][0]["documentSha256"])

            changed = read_json(output)
            changed["entries"][0]["documentProposition"] = paragraph.replace("não ", "")
            atomic_write_json(draft, changed)
            with self.assertRaises(ForjaN3Error):
                bind_claims(markdown, draft, output)


if __name__ == "__main__":
    unittest.main()
