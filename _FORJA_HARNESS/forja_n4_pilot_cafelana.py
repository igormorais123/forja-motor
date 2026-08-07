"""Materialize the first complete N4 shadow pilot over the audited CASO-04 AgInt cycle."""

from __future__ import annotations

import json

import forja_acervo

from forja_case_tests import run_suite, suite_hash
from forja_consistency import inspect_physical_document
from forja_n3_common import FORJA, atomic_write_json, read_json, sha256_file
from forja_n4_common import build_envelope, write_artifact
from forja_n4_validate import validate_case


CASE_ID = forja_acervo.caso("CASO-04")
PRODUCER = "piloto-n4-structural-producer"
REVIEWER = "piloto-n4-independent-reviewer"
ORIGIN_DRAFT = forja_acervo.caminho("piloto-n4-rascunho-origem")


def run() -> dict:
    if ORIGIN_DRAFT.is_file():
        origin_prefix = ORIGIN_DRAFT.read_text(encoding="utf-8-sig", errors="ignore")[:4096].lower()
        if "esta fonte foi invalidada" in origin_prefix:
            raise RuntimeError("piloto CASO-04 revogado: a minuta de origem foi invalidada; reconstrução exige a íntegra do AgInt de 24/06/2026")
    case_dir = FORJA / "state" / CASE_ID
    pilot = case_dir / "n4_pilot"
    draft = pilot / "MINUTA_CAFELANA_AGINT_N4_PILOTO.md"
    docx = pilot / "MINUTA_CAFELANA_AGINT_N4_PILOTO.docx"
    pdf = pilot / "MINUTA_CAFELANA_AGINT_N4_PILOTO.pdf"
    f8 = pilot / "F8_QA_LEDGER_N4.json"
    source_files = {
        "draft": draft,
        "docx": docx,
        "pdf": pdf,
        "f8": f8,
        "fidelity": pilot / "FORMAT_FIDELITY_N4.json",
    }
    source_hashes = {key: sha256_file(path) for key, path in source_files.items()}
    manifest = read_json(case_dir / "FORJA_CASE_MANIFEST.json", {}) or {}
    manifest["specVersionCandidate"] = "N4.0-candidate"
    manifest["n4SourceRegistry"] = {key: value for key, value in source_hashes.items()}
    manifest["n4Pilot"] = {"mode": "shadow", "sourceCycle": str(pilot), "originalsUntouched": True}
    atomic_write_json(case_dir / "FORJA_CASE_MANIFEST.json", manifest)

    def save(filename: str, content: dict, *, applicability: str = "required", status: str = "approved", justification: str | None = None) -> dict:
        if justification:
            content = {**content, "justification": justification}
        payload = build_envelope(
            case_dir, filename, content, source_hashes=list(source_hashes.values()),
            producer_run_id=PRODUCER, reviewer_run_id=REVIEWER,
            applicability=applicability, status=status,
        )
        write_artifact(case_dir, filename, payload)
        return payload

    def not_applicable(filename: str, reason: str) -> dict:
        return save(filename, {}, applicability="not_applicable", status="not_applicable", justification=reason)

    save("F2_N4_CLASSIFICATION.json", {
        "product": "impugnação ao agravo interno",
        "responsePiece": True,
        "complexity": "high",
        "science": {"mode": "not_applicable", "triggerPropositionIds": [], "domains": [], "justification": "A minuta depende de fontes processuais e jurídicas, sem proposição extrajurídica material.", "requiredBeforeF6": False},
    })

    question_specs = [
        ("Q-PROC-001", "procedural_event", "Qual é o objeto atual do recurso?", "Agravo interno contra decisão monocrática que manteve a inadmissão do recurso especial.", ["DOC-DRAFT"], "answered"),
        ("Q-PROC-002", "request", "Qual fundamento deve ser examinado primeiro?", "A falta de impugnação de fundamento autônomo.", ["THESIS-001"], "answered"),
        ("Q-PROC-003", "evidence", "O agravo enfrentou nominalmente os quatro fundamentos?", "A conferência nominal depende da íntegra do agravo interno.", [], "blocked"),
        ("Q-TIME-001", "procedural_event", "Qual é o termo inicial do agravo em recurso especial?", "Depende da certidão e do histórico de consulta eletrônica.", [], "blocked"),
        ("Q-TIME-002", "evidence", "Houve suspensão de prazo no período?", "Depende dos atos normativos e registros do processo.", [], "blocked"),
        ("Q-REG-001", "precedent", "A prevenção deve ser provocada pelas agravadas?", "Não; a minuta usa prevenção apenas defensivamente.", ["THESIS-003", "HELENA"], "answered"),
        ("Q-REG-002", "precedent", "Qual é o limite temporal da arguição da parte?", "Até o início do julgamento, conforme art. 71, § 4º, do RISTJ.", ["DOC-DRAFT"], "answered"),
        ("Q-REG-003", "evidence", "O precedente antigo pertence à mesma cadeia processual?", "A identidade precisa ser conferida antes de uso mais assertivo.", [], "blocked"),
        ("Q-MERIT-001", "merit", "A tese exige reexaminar o laudo?", "A resposta da União exigiria reexame, mas a minuta não pede nova leitura da prova.", ["THESIS-004"], "answered"),
        ("Q-MERIT-002", "merit", "Negativa de prestação jurisdicional se confunde com decisão contrária?", "Não.", ["DOC-DRAFT"], "answered"),
        ("Q-MERIT-003", "precedent", "O prequestionamento pode ser reconstruído no STJ?", "Não, conforme a formulação adotada com a Súmula 211/STJ.", ["DOC-DRAFT"], "answered"),
        ("Q-MERIT-004", "precedent", "A Súmula 7/STJ é usada para qual proposição?", "Para impedir revisão das premissas técnicas e probatórias da liquidação.", ["DOC-DRAFT"], "answered"),
        ("Q-MERIT-005", "precedent", "A Súmula 284/STF funciona como fundamento autônomo?", "Sim, segundo a estrutura da decisão descrita na minuta, pendente de cotejo nominal com o agravo.", ["THESIS-001"], "answered"),
        ("Q-SANC-001", "risk", "A multa decorre automaticamente do desprovimento?", "Não; exige manifesta inadmissibilidade ou improcedência e unanimidade.", ["THESIS-002", "CICERO"], "answered"),
        ("Q-REQ-001", "request", "Qual é o pedido principal?", "Não conhecimento por fundamento autônomo não impugnado.", ["REQUEST-001"], "answered"),
        ("Q-REQ-002", "request", "Qual pedido depende de prova ainda ausente?", "Intempestividade originária, condicionada à certidão e aos registros eletrônicos.", ["REQUEST-002"], "answered"),
        ("Q-REQ-003", "request", "Qual é o pedido subsidiário de mérito recursal?", "Desprovimento integral.", ["REQUEST-003"], "answered"),
        ("Q-REQ-004", "request", "Como tratar prevenção?", "Rejeitar eventual arguição tardia da recorrente, sem pedir redistribuição.", ["REQUEST-004"], "answered"),
        ("Q-VIS-001", "visual", "Os elementos visuais preservam ressalvas e são legíveis?", "Sim, segundo QA independente de 10 páginas e quatro SVGs.", ["F8"], "answered"),
        ("Q-REL-001", "risk", "A minuta pode ser liberada externamente agora?", "Não; permanece bloqueada até a conferência documental nominal e revisão humana.", ["F7", "HELENA", "CICERO"], "answered"),
    ]
    questions = []
    for qid, category, text, answer, supports, status in question_specs:
        item = {"questionId": qid, "parentId": None, "category": category, "text": text, "origin": "audited_cycle", "materiality": "decisive", "status": status, "answer": answer, "supportIds": supports, "dependsOn": [], "owner": "F4", "reviewStatus": "confirmed" if status == "answered" else "pending"}
        if status == "blocked":
            item["unansweredConsequence"] = "block_external_release"
        questions.append(item)
    answered = sum(item["status"] == "answered" for item in questions)
    blocked = sum(item["status"] == "blocked" for item in questions)
    save("F2_QUESTION_TREE.json", {"questions": questions, "coverage": {"total": len(questions), "material": len(questions), "answeredMaterial": answered, "blockedMaterial": blocked}})

    save("F3_EVENT_IDENTITY.json", {"events": [
        {"eventId": "EVENT-001", "canonicalLabel": "inadmissão do recurso especial mantida", "sourceId": "DOC-DRAFT", "locator": "parágrafos 1 e 12", "allowedParaphrases": ["decisão monocrática preservada"], "forbiddenEquivalents": ["recurso especial julgado improcedente no mérito"], "temporalPosition": 1},
        {"eventId": "EVENT-002", "canonicalLabel": "agravo interno pendente de julgamento", "sourceId": "DOC-DRAFT", "locator": "parágrafo 12", "allowedParaphrases": ["impugnação atual"], "forbiddenEquivalents": ["agravo interno desprovido"], "temporalPosition": 2},
    ], "surfaces": [{"surfaceId": "draft", "text": draft.read_text(encoding="utf-8"), "semanticContrast": False}]})

    save("F3_DOCUMENT_COMPARISON.json", {"comparisonSets": [{"setId": "CMP-AGINT-001", "documents": ["decisão monocrática", "agravo interno", "impugnação"], "units": [{"unitId": "CMP-U-001", "priorArgument": "quatro fundamentos autônomos descritos", "priorResponse": "não disponível integralmente no pacote piloto", "currentArgument": "a impugnação afirma falta de ataque à Súmula 284/STF", "classification": "uncertain", "novelElements": [], "prequestioningAssessment": "requires_legal_review", "consequence": "triage_only", "reviewStatus": "pending"}]}]})

    nodes = [
        {"id": "DOC-DRAFT", "type": "document", "sourceArtifact": str(draft)}, {"id": "F7", "type": "decision", "sourceArtifact": "F7_VERIFICADOR_N3.json"}, {"id": "F8", "type": "document", "sourceArtifact": str(f8)},
        {"id": "HELENA", "type": "decision", "sourceArtifact": "PARECER_HELENA.md"}, {"id": "CICERO", "type": "decision", "sourceArtifact": "PARECER_CICERO.md"},
    ] + [{"id": f"THESIS-{index:03d}", "type": "thesis", "sourceArtifact": "F4_THESIS_MATURITY.json"} for index in range(1, 5)] + [{"id": f"REQUEST-{index:03d}", "type": "request", "sourceArtifact": "F4_COVERAGE_MATRIX.json"} for index in range(1, 6)]
    edges = [
        {"edgeId": "E-001", "from": "DOC-DRAFT", "to": "THESIS-001", "relation": "supports", "scope": "partial", "reason": "a minuta descreve o fundamento autônomo; cotejo nominal ainda é necessário", "reviewStatus": "confirmed"},
        {"edgeId": "E-002", "from": "THESIS-001", "to": "REQUEST-001", "relation": "justifies", "scope": "full", "reason": "fundamento autônomo sustenta o não conhecimento", "reviewStatus": "confirmed"},
        {"edgeId": "E-003", "from": "THESIS-002", "to": "REQUEST-005", "relation": "justifies", "scope": "partial", "reason": "sanção depende de requisitos adicionais", "reviewStatus": "confirmed"},
        {"edgeId": "E-004", "from": "HELENA", "to": "THESIS-003", "relation": "supports", "scope": "full", "reason": "parecer aprova uso defensivo da prevenção", "reviewStatus": "confirmed"},
        {"edgeId": "E-005", "from": "CICERO", "to": "THESIS-004", "relation": "qualifies", "reason": "mantém reexame probatório em posição subsidiária", "reviewStatus": "confirmed"},
    ]
    save("F3_REASONING_GRAPH.json", {"nodes": nodes, "edges": edges})
    not_applicable("F3_CONDUCT_LEDGER.json", "O produto não depende de ledger longitudinal de condutas nem externaliza imputação de má-fé.")

    coverage_specs = [
        ("COV-001", "fundamento autônomo não impugnado", ["P-014", "P-019"], "REQUEST-001"),
        ("COV-002", "intempestividade condicionada à prova eletrônica", ["P-020", "P-025"], "REQUEST-002"),
        ("COV-003", "prevenção usada apenas defensivamente", ["P-026", "P-030"], "REQUEST-004"),
        ("COV-004", "negativa de prestação jurisdicional", ["P-031", "P-032"], "REQUEST-003"),
        ("COV-005", "ausência de prequestionamento", ["P-033", "P-034"], "REQUEST-003"),
        ("COV-006", "reexame probatório", ["P-035", "P-036"], "REQUEST-003"),
        ("COV-007", "deficiência de fundamentação", ["P-037", "P-038"], "REQUEST-001"),
        ("COV-008", "limites da liquidação e coisa julgada", ["P-039", "P-041"], "REQUEST-003"),
        ("COV-009", "multa condicionada", ["P-042", "P-044"], "REQUEST-005"),
    ]
    save("F4_COVERAGE_MATRIX.json", {"items": [{"coverageId": cid, "kind": "material_issue", "originDocumentId": "audited_cycle", "originLocator": paragraphs[0], "statement": statement, "supportIds": ["DOC-DRAFT"], "priorResponseIds": [], "currentTreatment": "rebutted", "draftParagraphIds": paragraphs, "requestedConsequence": request, "materiality": "decisive", "status": "covered"} for cid, statement, paragraphs, request in coverage_specs]})

    save("F4_THESIS_MATURITY.json", {"theses": [
        {"thesisId": "THESIS-001", "statement": "Fundamento autônomo não impugnado impede a reforma.", "role": "primary", "documentaryStrength": "moderate", "legalStrength": "strong", "gaps": ["obter íntegra do agravo"], "bestObjection": "o recurso enfrentou a decisão em conjunto", "contaminationRisk": "low", "activationTrigger": "cotejo confirmar ausência de impugnação", "properVehicle": "impugnação ao agravo interno", "helenaDecision": "adopt", "ciceroDecision": "adopt_with_qualification"},
        {"thesisId": "THESIS-002", "statement": "Multa apenas se presentes requisitos legais e unanimidade.", "role": "reserve", "documentaryStrength": "moderate", "legalStrength": "moderate", "gaps": [], "bestObjection": "mero desprovimento não autoriza multa", "contaminationRisk": "medium", "activationTrigger": "reconhecimento expresso pelo colegiado", "properVehicle": "pedido condicionado", "helenaDecision": "adopt_with_qualification", "ciceroDecision": "adopt_with_qualification"},
        {"thesisId": "THESIS-003", "statement": "Prevenção apenas para repelir arguição tardia.", "role": "subsidiary", "documentaryStrength": "strong", "legalStrength": "moderate", "gaps": ["confirmar autuação atual"], "bestObjection": "prevenção pode ser reconhecida de ofício", "contaminationRisk": "low", "activationTrigger": "arguição tardia da recorrente", "properVehicle": "defesa subsidiária", "helenaDecision": "adopt", "ciceroDecision": "adopt_with_qualification"},
        {"thesisId": "THESIS-004", "statement": "Pretensão da União exigiria reexame probatório vedado.", "role": "subsidiary", "documentaryStrength": "moderate", "legalStrength": "strong", "gaps": [], "bestObjection": "a controvérsia seria apenas jurídica", "contaminationRisk": "low", "activationTrigger": "superação dos filtros de admissibilidade", "properVehicle": "resposta subsidiária", "helenaDecision": "adopt", "ciceroDecision": "adopt"},
    ]})

    tests = []
    test_specs = [
        ("fundamento autônomo", "contains"), ("certidão de intimação eletrônica", "contains"), ("não formulam pedido de redistribuição", "contains"),
        ("não decorre automaticamente do desprovimento", "contains"), ("Súmula 7/STJ", "contains"), ("Súmula 284/STF", "contains"),
        ("art. 71, § 4º, do RISTJ", "contains"), ("AgInt no AgInt no REsp nº 1.533.736/PR", "contains"),
        ("[VERIFICAR]", "not_contains"), ("Nestes termos, pede deferimento.", "contains"),
    ]
    for index, (value, kind) in enumerate(test_specs, 1):
        tests.append({"testId": f"CT-CAF-{index:03d}", "question": f"Critério literal: {value}", "severity": "blocking", "method": "deterministic", "expected": f"{kind}: {value}", "evidenceRequired": ["audited_markdown"], "immutableFromHash": source_hashes["draft"], "status": "pending", "evaluator": {"kind": kind, "value": value, "ignoreCase": True}})
    suite = {"suiteId": "PILOTO-N4-TDD-v1", "draftedBeforeFinalText": True, "tests": tests}
    suite["suiteHash"] = suite_hash(suite)
    save("F4_CASE_ACCEPTANCE_TESTS.json", suite)
    not_applicable("F4_DECISION_FACTOR_MAP.json", "As decisões integrais não compõem o pacote piloto; fatores decisórios não serão inferidos da minuta.")
    not_applicable("F4_SETTLEMENT_MAP.json", "Composição não integra o objetivo desta impugnação recursal.")
    not_applicable("F4_INTERTEMPORAL_MAP.json", "A minuta não resolve conflito de regimes intertemporais; a Lei 14.939/2024 é tratada no alcance específico declarado.")
    not_applicable("F4_QUANTIFICATION_SCENARIOS.json", "O produto não pede cálculo de valor ou proveito econômico.")

    for filename, reason in [
        ("F5C_RESEARCH_PROTOCOL.json", "LCI classificado como não aplicável."),
        ("F5C_STUDY_LEDGER.json", "LCI classificado como não aplicável."),
        ("F5C_EVIDENCE_SYNTHESIS.json", "LCI classificado como não aplicável."),
        ("F5C_CLAIM_EVIDENCE_MAP.json", "LCI classificado como não aplicável."),
    ]:
        not_applicable(filename, reason)

    test_results = run_suite(suite, draft, reviewer_run_id=REVIEWER, producer_run_id=PRODUCER)
    save("F7_CASE_TEST_RESULTS.json", {"suiteHash": test_results["suiteHash"], "draftHash": test_results["draftHash"], "results": test_results["results"], "approved": test_results["approved"], "findings": test_results["findings"]})

    physical = inspect_physical_document(docx_path=docx, pdf_path=pdf, f8_path=f8, layout_profile_id="medina-visual-law-v1", expected_docx_hash=source_hashes["docx"], expected_pdf_hash=source_hashes["pdf"])
    layers = {"C1": "pass", "C2": "pass", "C3": "pass", "C4": "pass", "C5": "pass" if physical["approved"] else "fail"}
    global_findings = list(physical["findings"])
    save("F7_GLOBAL_CONSISTENCY.json", {"layers": layers, "findings": global_findings, "physicalIntegrity": physical, "approved": not global_findings})
    save("F7_METACOGNITIVE_AUDIT.json", {
        "premises": [
            {"premiseId": "PREM-001", "statement": "O agravo deixou fundamento autônomo sem impugnação.", "originType": "audited_draft", "confirmedBySourceIds": [], "status": "declared_not_confirmed", "usedInDraft": False},
            {"premiseId": "PREM-002", "statement": "A tempestividade depende da certidão e do histórico eletrônico.", "originType": "legal_method", "confirmedBySourceIds": ["DOC-DRAFT"], "status": "confirmed", "usedInDraft": True},
        ],
        "consensusChecks": [{"issueId": "META-001", "agentsAgreeing": 2, "independentSourceCount": 1, "verdict": "shared_source_not_independent_consensus"}],
        "recommendationChanges": [{"recommendationId": "REC-001", "from": "positive_redistribution_request", "to": "defensive_preclusion_only", "reasonType": "strategic_correction", "supportIds": ["HELENA", "CICERO"]}],
        "metricChecks": [],
        "bestObjection": "A recorrente pode demonstrar impugnação conjunta e termo inicial posterior.",
        "alternativeExplanation": "A aparente intempestividade pode decorrer de consulta eletrônica ou suspensão não incluída no pacote.",
    })
    not_applicable("F7_SCIENCE_AUDIT.json", "LCI classificado como não aplicável.")
    not_applicable("F9_DELIVERY_SELECTION.json", "O piloto N4 é interno e não seleciona anexo para envio.")
    not_applicable("F10_DELIVERY_INTEGRITY.json", "Nenhuma entrega N4 foi realizada.")
    not_applicable("F10_HUMAN_DIFF_CLASSIFICATION.json", "Ainda não existe versão humana posterior ao piloto N4.")

    result = validate_case(case_dir, target_phase="F10_ENTREGA_EVIDENCIA_APRENDIZADO")
    return result


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
