from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from forja_adversarial_audit import (
    initialize_audit,
    mandatory_prompt_for_phase,
    response_product_required,
    validate_adversarial_audit,
    validate_adversarial_recheck,
    validate_adversarial_strategy,
)
from forja_n3_common import atomic_write_json, sha256_file


class ForjaAdversarialAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "contestacao.md"
        self.source.write_text(
            "# Contestação\n\nA parte invoca o REsp 1.234.567/SP para afirmar tese decisiva.\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def complete_audit(self) -> dict:
        payload = initialize_audit(self.source)
        payload["scope"] = {
            "fullReadingConfirmed": True,
            "pagesOrSectionsCovered": ["p. 1"],
            "adversarialRequestsMapped": True,
        }
        citation = payload["citationInventory"][0]
        citation.update({
            "pageOrParagraph": "p. 1, parágrafo 2",
            "propositionClaimed": "Tese decisiva atribuída ao precedente.",
            "verificationStatus": "not_located_after_exhaustive_search",
            "identityMatch": "not_confirmed",
            "quoteMatch": "not_confirmed",
            "contextMatch": "not_confirmed",
            "currentStatus": "not_confirmed",
            "recommendedTreatment": "challenge_with_cautious_language",
        })
        payload["researchLog"] = [
            {"citationId": citation["id"], "query": "REsp 1234567", "url": "https://scon.stj.jus.br/SCON/", "checkedAt": "2026-07-10T10:00:00-03:00", "result": "não localizado"},
            {"citationId": citation["id"], "query": "REsp 1234567", "url": "https://processo.stj.jus.br/processo/pesquisa/", "checkedAt": "2026-07-10T10:05:00-03:00", "result": "não localizado"},
        ]
        payload["conclusion"] = {
            "citationAuditComplete": True,
            "contradictionAuditComplete": True,
            "redTeamCompleted": True,
            "badFaithAssessment": "not_supported",
            "summary": "Citação não localizada após duas diligências; não afirmar inexistência.",
        }
        return payload

    def test_initial_inventory_is_blocked_until_verified(self) -> None:
        payload = initialize_audit(self.source)
        self.assertEqual(1, len(payload["citationInventory"]))
        result = validate_adversarial_audit(payload)
        self.assertFalse(result["approved"])
        self.assertTrue(any("pendente" in item for item in result["p0"]))

    def test_not_located_requires_two_official_channels(self) -> None:
        payload = self.complete_audit()
        payload["researchLog"] = payload["researchLog"][:1]
        result = validate_adversarial_audit(payload)
        self.assertFalse(result["approved"])
        self.assertTrue(any("dois canais oficiais" in item for item in result["p0"]))

    def test_complete_cautious_audit_passes(self) -> None:
        result = validate_adversarial_audit(self.complete_audit())
        self.assertTrue(result["approved"], result)

    def test_detected_citation_cannot_be_removed_from_inventory(self) -> None:
        payload = self.complete_audit()
        payload["citationInventory"] = []
        result = validate_adversarial_audit(payload)
        self.assertFalse(result["approved"])
        self.assertTrue(any("fora do inventário" in item for item in result["p0"]))

    def test_confirmed_citation_requires_all_verification_dimensions(self) -> None:
        payload = self.complete_audit()
        citation = payload["citationInventory"][0]
        citation.update({
            "verificationStatus": "confirmed",
            "officialSourceUrl": "https://processo.stj.jus.br/processo/pesquisa/",
            "identityMatch": "pending",
            "quoteMatch": "pending",
            "contextMatch": "pending",
            "currentStatus": "pending",
            "recommendedTreatment": "use",
        })
        result = validate_adversarial_audit(payload)
        self.assertFalse(result["approved"])
        self.assertTrue(any("dimensões" in item for item in result["p0"]))

    def test_bad_faith_language_requires_human_authorization(self) -> None:
        payload = self.complete_audit()
        payload["badFaithIndicators"] = [{
            "id": "BF-001",
            "status": "objective_indicator",
            "conduct": "Atribuição de tese não confirmada.",
            "materiality": "A tese sustenta o pedido principal.",
            "recordReferences": ["p. 1"],
            "counterHypothesis": "Erro de numeração ou citação secundária imprecisa.",
            "legalHypothesis": "Possível alteração da verdade dos fatos, CPC, art. 80, II.",
            "legalBasis": "CPC, arts. 79 a 81, sujeito a conferência no caso concreto.",
            "externalLanguage": "A parte agiu de má-fé e inventou jurisprudência.",
        }]
        result = validate_adversarial_audit(payload)
        self.assertFalse(result["approved"])
        self.assertTrue(any("sem autorização" in item for item in result["p0"]))

    def test_decisive_point_requires_traceable_finding(self) -> None:
        payload = self.complete_audit()
        payload["decisivePoints"] = [{
            "id": "PD-001",
            "status": "actionable",
            "confidence": "high",
            "findingRefs": ["INEXISTENTE"],
            "decisiveWhy": "Pode retirar o suporte central.",
            "proceduralConsequence": "Impugnação específica.",
            "recommendedAction": "Confrontar com a fonte oficial.",
            "preservationCheck": "Questão devolvida.",
            "bestInnocentExplanation": "Erro de numeração sanável.",
            "backfireRisk": "A referência pode conter erro material sanável.",
        }]
        result = validate_adversarial_audit(payload)
        self.assertFalse(result["approved"])
        self.assertTrue(any("referências" in item for item in result["p0"]))

    def test_not_applicable_still_requires_reason(self) -> None:
        payload = initialize_audit(Path("."), applicable=False, reason="Petição inicial sem manifestação adversária anterior identificada.")
        self.assertTrue(validate_adversarial_audit(payload)["approved"])

    def test_strategy_and_recheck_are_hash_bound(self) -> None:
        audit = self.complete_audit()
        audit_path = self.root / "audit.json"
        atomic_write_json(audit_path, audit)
        strategy = {
            "kind": "forja_adversarial_strategy",
            "applicable": True,
            "auditSha256": sha256_file(audit_path),
            "decisions": [{
                "findingId": audit["citationInventory"][0]["id"],
                "decision": "subsidiary",
                "rationale": "A não localização enfraquece o argumento, mas não prova fabricação.",
                "backfireControl": "Usar linguagem cautelosa e indicar as consultas oficiais.",
            }],
            "badFaithDecision": {"mode": "do_not_allege", "humanAuthorized": False},
            "helenaReview": {"present": True, "recommendations": ["Usar linguagem cautelosa."]},
            "ciceroReview": {"present": True, "approved": True, "recommendations": ["Não afirmar inexistência."]},
        }
        self.assertTrue(validate_adversarial_strategy(strategy, audit_path)["approved"])
        strategy_path = self.root / "strategy.json"
        atomic_write_json(strategy_path, strategy)
        recheck = {
            "kind": "forja_adversarial_recheck",
            "applicable": True,
            "auditSha256": sha256_file(audit_path),
            "strategySha256": sha256_file(strategy_path),
            "citationsRechecked": [audit["citationInventory"][0]["id"]],
            "findingsRechecked": [],
            "falsePositiveReview": {"completed": True},
            "bestInnocentExplanation": {"tested": True},
            "externalAllegations": [],
            "approved": True,
            "p0": 0,
        }
        self.assertTrue(validate_adversarial_recheck(recheck, audit_path, strategy_path)["approved"])

    def test_every_material_finding_requires_strategy_decision(self) -> None:
        audit = self.complete_audit()
        audit_path = self.root / "audit-without-decision.json"
        atomic_write_json(audit_path, audit)
        strategy = {
            "kind": "forja_adversarial_strategy",
            "applicable": True,
            "auditSha256": sha256_file(audit_path),
            "decisions": [],
            "badFaithDecision": {"mode": "do_not_allege", "humanAuthorized": False},
            "helenaReview": {"present": True, "recommendations": ["Usar linguagem cautelosa."]},
            "ciceroReview": {"present": True, "approved": True, "recommendations": ["Não afirmar inexistência."]},
        }
        result = validate_adversarial_strategy(strategy, audit_path)
        self.assertFalse(result["approved"])
        self.assertTrue(any("todos os achados" in item for item in result["p0"]))

    def test_bad_faith_decision_rejects_unknown_mode(self) -> None:
        audit = self.complete_audit()
        audit_path = self.root / "audit-bad-mode.json"
        atomic_write_json(audit_path, audit)
        citation_id = audit["citationInventory"][0]["id"]
        strategy = {
            "kind": "forja_adversarial_strategy",
            "applicable": True,
            "auditSha256": sha256_file(audit_path),
            "decisions": [{
                "findingId": citation_id,
                "decision": "subsidiary",
                "rationale": "Inconsistência ainda inconclusiva.",
                "backfireControl": "Não afirmar inexistência.",
            }],
            "badFaithDecision": {"mode": "automatic_accusation"},
            "helenaReview": {"present": True, "recommendations": ["Manter proporcionalidade."]},
            "ciceroReview": {"present": True, "approved": True, "recommendations": ["Não acusar."]},
        }
        result = validate_adversarial_strategy(strategy, audit_path)
        self.assertFalse(result["approved"])
        self.assertTrue(any("má-fé" in item for item in result["p0"]))

    def test_prompt_and_response_classifier_are_mandatory(self) -> None:
        prompt = mandatory_prompt_for_phase("F3_FONTES_REGIMENTO_LEIS")
        self.assertIn("Busca sem resultado NÃO prova inexistência", prompt)
        self.assertTrue(response_product_required("Contrarrazões ao agravo interno"))
        self.assertFalse(response_product_required("Petição inicial de obrigação de fazer"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
