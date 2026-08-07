"""Generate the versioned N4 JSON Schemas and candidate phase contracts."""

from __future__ import annotations

from copy import deepcopy

from forja_n3_common import FORJA, PHASES, atomic_write_json, read_json
from forja_n4_common import ARTIFACT_SPECS, SPEC_VERSION


COMMON = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "common.schema.json",
    "type": "object",
    "required": [
        "schemaVersion", "specVersion", "caseId", "artifactType", "phase", "applicability",
        "status", "sourceHashes", "producerRunId", "createdAt", "updatedAt", "contentHash", "issues",
    ],
    "properties": {
        "schemaVersion": {"const": 1},
        "specVersion": {"const": SPEC_VERSION},
        "caseId": {"type": "string", "minLength": 1},
        "artifactType": {"type": "string", "minLength": 1},
        "phase": {"enum": list(PHASES)},
        "applicability": {"enum": ["required", "conditional", "not_applicable"]},
        "status": {"enum": ["draft", "pending_review", "approved", "blocked", "stale", "not_applicable"]},
        "sourceHashes": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        "producerRunId": {"type": "string", "minLength": 1},
        "reviewerRunId": {"type": ["string", "null"]},
        "createdAt": {"type": "string"},
        "updatedAt": {"type": "string"},
        "contentHash": {"type": "string", "minLength": 16},
        "issues": {"type": "array"},
        "justification": {"type": "string"},
    },
    "allOf": [
        {
            "if": {"properties": {"applicability": {"const": "not_applicable"}}},
            "then": {"required": ["justification"]},
        },
        {
            "if": {"properties": {"status": {"const": "approved"}}},
            "then": {"required": ["reviewerRunId"]},
        },
    ],
    "additionalProperties": True,
}


EXTENSIONS = {
    "F0": {"outputs": ["n4_run_registration"], "gates": []},
    "F1": {"outputs": ["n4_document_coverage"], "gates": ["comparison_inputs_preserved"]},
    "F2": {"outputs": ["n4_classification", "question_tree"], "gates": ["n4_modules_classified", "material_questions_open_or_routed", "exploration_100_complete", "answers_provenance_classified", "downstream_handoff_ready"]},
    "F3": {"outputs": ["event_identity", "document_comparison", "reasoning_graph", "conduct_ledger", "recipient_map"], "gates": ["event_identity_stable", "comparison_inputs_complete_or_blocked", "reasoning_references_valid"]},
    "F4": {"outputs": ["coverage_matrix", "thesis_maturity", "case_acceptance_tests", "decision_factor_map", "settlement_map", "intertemporal_map", "quantification_scenarios", "signature_brief"], "gates": ["material_coverage_complete", "thesis_roles_decided", "case_tests_frozen_before_final_draft", "conditional_modules_resolved"]},
    "F5": {"outputs": ["science_research_protocol", "science_study_ledger", "science_evidence_synthesis", "science_claim_evidence_map"], "gates": ["science_evidence_ready_or_explicitly_blocked"]},
    "F6": {"outputs": ["paragraph_evidence_map_n4"], "gates": ["only_authorized_claims_used"]},
    "F7": {"outputs": ["case_test_results", "global_consistency", "metacognitive_audit", "science_audit"], "gates": ["case_tests_passed", "global_consistency_passed", "metacognitive_audit_completed", "science_audit_passed_or_not_applicable"]},
    "F8": {"outputs": ["n4_visual_semantic_audit"], "gates": ["visual_scales_units_sources_consistent"]},
    "F9": {"outputs": ["delivery_selection"], "gates": ["delivery_selection_matches_package"]},
    "F10": {
        "outputs": [
            "delivery_integrity",
            "human_diff_classification",
            "post_protocol_return",
            "protocol_evidence",
            "post_protocol_baseline_backfill",
            "post_protocol_document_comparison",
            "learning_candidate",
        ],
        "conditionalOutputs": {
            "when": "eligible_post_protocol_return_detected",
            "outputs": [
                "post_protocol_return",
                "protocol_evidence",
                "post_protocol_baseline_backfill",
                "post_protocol_document_comparison",
                "learning_candidate",
            ],
        },
        "gates": [
            "delivery_integrity_confirmed",
            "human_diff_classified",
            "post_protocol_identity_resolved",
            "post_protocol_baseline_resolved",
            "n4_management_synced",
        ],
    },
}


QUESTION_TREE_SCHEMA = {
    "properties": {
        "protocolVersion": {"const": "FORJA-F2A-100-v1"},
    },
    "strictProperties": {
        "problemDefinition": {"type": "string", "minLength": 40},
        "diagnosticSynthesis": {"type": "string", "minLength": 80},
        "questions": {
            "type": "array", "minItems": 100, "maxItems": 100,
            "items": {
                "type": "object",
                "required": ["questionId", "lens", "category", "text", "caseAnchor", "whyItMatters", "materiality", "status", "answer", "epistemicStatus", "supportIds", "downstreamTargets"],
                "properties": {
                    "questionId": {"type": "string", "pattern": "^Q[0-9]{3}$"},
                    "lens": {"enum": ["mandato_resultado", "fatos_cronologia", "prova_fontes", "processo_competencia", "direito_precedentes", "adversario_julgador", "riscos_etica_impactos", "alternativas_solucoes", "quantificacao_execucao", "comunicacao_visual_validacao"]},
                    "text": {"type": "string", "minLength": 12},
                    "caseAnchor": {"type": "string", "minLength": 12},
                    "whyItMatters": {"type": "string", "minLength": 12},
                    "status": {"enum": ["answered", "blocked", "not_applicable"]},
                    "answer": {"type": "string", "minLength": 12},
                    "epistemicStatus": {"enum": ["confirmed_document", "confirmed_official_source", "office_declaration", "legal_inference", "strategic_hypothesis", "not_verified", "not_applicable"]},
                    "supportIds": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
                    "downstreamTargets": {"type": "array", "minItems": 1, "items": {"enum": ["F3", "F4", "F5", "F6", "F7"]}, "uniqueItems": True},
                },
            },
        },
        "coverage": {"type": "object", "required": ["total", "material", "answeredMaterial", "blockedMaterial", "perLens"]},
        "solutionHypotheses": {"type": "array", "minItems": 2},
        "downstreamHandoff": {"type": "object", "required": ["F3", "F4", "F5", "F6", "F7"]},
        "openDecisiveQuestions": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        "draftRelease": {"enum": ["blocked", "ready_for_drafting"]},
    },
    "allOf": [{
        "if": {"required": ["protocolVersion"]},
        "then": {
            "required": ["problemDefinition", "diagnosticSynthesis", "solutionHypotheses", "downstreamHandoff", "openDecisiveQuestions", "draftRelease"],
            "properties": {},
        },
    }],
}
QUESTION_TREE_SCHEMA["allOf"][0]["then"]["properties"] = QUESTION_TREE_SCHEMA["strictProperties"]

# Emenda E5. A cobertura é por família examinada, nunca por contagem mínima de
# teses: o dever do brief é ter olhado para cada frente, e uma frente examinada
# e descartada com motivo cobre tão bem quanto uma proposta.
NOVE_FAMILIAS = [
    "competencia",
    "admissibilidade",
    "prejudiciais",
    "prescricao_decadencia",
    "nulidades",
    "merito_principal",
    "merito_subsidiario",
    "constitucional_prequestionamento",
    "consequencia_institucional",
]


SCHEMA_OVERRIDES = {
    # Extensão compatível produzida por `forja_learning.py`. Estava aplicada à
    # mão no schema gerado desde 22/07/2026 e foi apagada na primeira execução
    # do gerador — que é exatamente o que a DA-04 previne. Vive aqui agora.
    "F10_HUMAN_DIFF_CLASSIFICATION.json": {
        "comparisonId": {"type": "string", "minLength": 1},
        "protocolStatus": {
            "enum": [
                "human_final_received",
                "protocol_claimed",
                "protocol_verified",
                "identity_ambiguous",
                "not_a_petition",
            ]
        },
        "baselineHash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "humanArtifactHash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "feedbackAssimilation": {
            "type": "object",
            "description": "Ledger sanitizado de unidades conversacionais, sinais de feedback, origem intelectual das teses e mudanças de fluxo.",
            "properties": {
                "conversationUnits": {"type": "array", "items": {"type": "object"}},
                "signals": {"type": "array", "items": {"type": "object"}},
                "contributions": {"type": "array", "items": {"type": "object"}},
                "workflowChanges": {"type": "array", "items": {"type": "object"}},
            },
            "required": ["conversationUnits", "signals", "contributions", "workflowChanges"],
            "additionalProperties": False,
        },
    },
    "F10_POST_PROTOCOL_RETURN.json": {
        "contentKey": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "evidenceKeys": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        },
        "caseResolution": {
            "type": "object",
            "required": ["status", "caseId", "method", "confidence", "reasonCodes"],
            "properties": {
                "status": {"enum": ["resolved", "identity_ambiguous"]},
                "caseId": {"type": ["string", "null"]},
                "demandId": {"type": ["string", "null"]},
                "method": {"enum": ["existing_thread", "cnj", "delivery_evidence", "manual", "unresolved"]},
                "confidence": {"enum": ["high", "medium", "low"]},
                "reasonCodes": {"type": "array", "items": {"type": "string"}},
            },
            "additionalProperties": True,
        },
        "humanArtifact": {
            "type": "object",
            "required": ["artifactId", "sha256", "originalName", "originalPath", "canonicalPath", "receivedAt"],
            "properties": {
                "artifactId": {"type": "string", "minLength": 1},
                "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                "originalName": {"type": "string", "minLength": 1},
                "originalPath": {"type": "string", "minLength": 1},
                "canonicalPath": {"type": "string", "minLength": 1},
                "receivedAt": {"type": "string", "minLength": 1},
            },
            "additionalProperties": True,
        },
    },
    "F10_PROTOCOL_EVIDENCE.json": {
        "protocolStatus": {
            "enum": [
                "human_final_received",
                "protocol_claimed",
                "protocol_verified",
                "identity_ambiguous",
                "not_a_petition",
            ]
        },
        "humanArtifactHash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "evidenceLinks": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["evidenceId", "kind", "strength"],
                "properties": {
                    "evidenceId": {"type": "string", "minLength": 1},
                    "kind": {"enum": ["filing_receipt", "stamped_document", "lawyer_declaration", "none", "conflict"]},
                    "strength": {"enum": ["verified_file_link", "corroborating", "declaration_only", "none", "conflicting"]},
                },
                "additionalProperties": True,
            },
        },
    },
    "F10_POST_PROTOCOL_BASELINE_BACKFILL.json": {
        "selectedArtifactId": {"type": "string", "minLength": 1},
        "selectedHash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "selectedPath": {"type": "string", "minLength": 1},
        "deliveredAt": {"type": "string", "minLength": 1},
        "deliveryEvidenceId": {"type": "string", "minLength": 1},
        "provenance": {"const": "gmail_sent_attachment"},
        "preSendMatch": {"const": False},
        "assurance": {"const": "gmail_exact_attachment_pending_review"},
    },
    "F10_POST_PROTOCOL_DOCUMENT_COMPARISON.json": {
        "contentKey": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "baseline": {
            "type": "object",
            "required": ["artifactId", "sha256", "path"],
            "properties": {
                "artifactId": {"type": "string", "minLength": 1},
                "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                "path": {"type": "string", "minLength": 1},
            },
            "additionalProperties": True,
        },
        "humanArtifact": {
            "type": "object",
            "required": ["artifactId", "sha256", "path"],
            "properties": {
                "artifactId": {"type": "string", "minLength": 1},
                "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                "path": {"type": "string", "minLength": 1},
            },
            "additionalProperties": True,
        },
        "summary": {"type": "object"},
        "changes": {"type": "array", "items": {"type": "object"}},
        "privateComparisonHash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    },
    "F10_LEARNING_CANDIDATE.json": {
        "contentKey": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "candidates": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "candidateId",
                    "sourceChangeId",
                    "status",
                    "decision",
                    "scope",
                    "promotionStage",
                    "origin",
                ],
                "properties": {
                    "candidateId": {"type": "string", "minLength": 1},
                    "sourceChangeId": {"type": "string", "minLength": 1},
                    "status": {"enum": ["observed", "proposed", "promoted", "rejected"]},
                    "decision": {"enum": ["pending", "pending_revalidation", "approved", "rejected"]},
                    "scope": {"enum": ["case", "product_type", "tribunal", "office", "global"]},
                    "promotionStage": {
                        "enum": [
                            "case_only",
                            "evidence_repeated",
                            "fixture_added",
                            "test_passed",
                            "independently_reviewed",
                            "human_approved",
                            "monitored",
                            "retained",
                            "rolled_back",
                        ]
                    },
                    "origin": {
                        "enum": [
                            "human_original",
                            "human_selected",
                            "forja_generated",
                            "external_model_import",
                            "source_derived",
                            "mixed",
                            "unknown",
                        ]
                    },
                },
                "additionalProperties": True,
            },
        },
    },
    "F3_MAPA_DESTINATARIO.json": {
        "protocolVersion": {"const": "FORJA-RECIPIENT-MAP-v1"},
        "recipient": {
            "type": "object",
            "required": ["court", "identityStatus"],
            "properties": {
                "court": {"type": "string", "minLength": 2},
                "organ": {"type": ["string", "null"]},
                "rapporteur": {"type": ["string", "null"]},
                "identityStatus": {"enum": ["confirmed", "unknown"]},
                "sourceIds": {"type": "array", "items": {"type": "string"}},
            },
        },
        "competence": {
            "type": "object",
            "required": ["status"],
            "properties": {
                "status": {"enum": ["confirmed", "unknown", "not_applicable"]},
                "basis": {"type": ["string", "null"]},
                "sourceIds": {"type": "array", "items": {"type": "string"}},
            },
        },
        # Prevenção não se prova por metadado de DataJud: `orgaoJulgador` orienta
        # a busca e não decide distribuição. Sem fonte adequada, fica `unknown`.
        "prevention": {
            "type": "object",
            "required": ["status"],
            "properties": {
                "status": {"enum": ["confirmed", "unknown", "not_applicable"]},
                "originCaseId": {"type": ["string", "null"]},
                "basis": {"type": ["string", "null"]},
                "sourceIds": {"type": "array", "items": {"type": "string"}},
            },
        },
        "composition": {
            "type": "object",
            "required": ["status"],
            "properties": {
                "status": {"enum": ["confirmed", "stale", "unknown", "not_applicable"]},
                "members": {"type": "array", "items": {"type": "object"}},
                "checkedAt": {"type": ["string", "null"], "format": "date-time"},
                "validUntil": {"type": ["string", "null"], "format": "date-time"},
                "sourceIds": {"type": "array", "items": {"type": "string"}},
            },
        },
        "positions": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["positionId", "level", "issueId", "decisionIds", "status", "sourceIds"],
                "properties": {
                    "positionId": {"type": "string", "minLength": 1},
                    "level": {"enum": [
                        "rapporteur", "organ", "same_section_other_organ",
                        "section", "special_court", "plenary", "other",
                    ]},
                    "issueId": {"type": "string", "minLength": 1},
                    # Toda posição aponta para decisão: sem decisão identificada,
                    # o que existe é impressão, não posição.
                    "decisionIds": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                    "status": {"type": "string", "minLength": 1},
                    "asOf": {"type": ["string", "null"]},
                    "summary": {"type": ["string", "null"]},
                    "sourceIds": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "divergences": {"type": "array"},
        "appellateRoute": {"type": "object"},
        "limitations": {"type": "array", "items": {"type": "string"}},
        "topologyScopeReason": {"type": ["string", "null"]},
        # Cada fonte declara o que é. O nível probatório decorre do tipo, não da
        # confiança de quem cita: ementa corrobora, íntegra decide, metadado orienta.
        "sourceCatalog": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["sourceId", "kind"],
                "properties": {
                    "sourceId": {"type": "string", "minLength": 1},
                    "kind": {"enum": [
                        "decisao_integra", "acordao_integra", "ato_oficial_tribunal",
                        "ementa", "espelho_oficial", "diario_eletronico",
                        "metadado_datajud", "dado_administrativo", "resultado_busca",
                    ]},
                    "locator": {"type": ["string", "null"]},
                    "retrievedAt": {"type": ["string", "null"]},
                    "sha256": {"type": ["string", "null"]},
                },
            },
        },
        # Trilha de replay das consultas ao TeiaJus. Consulta sem registro não é
        # pesquisa reproduzível — é lembrança.
        "searchRuns": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["queryId", "action", "executedAt"],
                "properties": {
                    "queryId": {"type": "string", "minLength": 1},
                    "action": {"type": "string", "minLength": 1},
                    "database": {"type": ["string", "null"]},
                    "executedAt": {"type": "string"},
                    "params": {"type": "object"},
                    "resultIds": {"type": "array", "items": {"type": "string"}},
                    "negativeResult": {"type": "boolean"},
                    "notSearched": {"type": "array", "items": {"type": "string"}},
                    "replayRef": {"type": ["string", "null"]},
                    "limitations": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
    },
    "F4_SIGNATURE_BRIEF.json": {
        "protocolVersion": {"const": "FORJA-SIGNATURE-BRIEF-v1"},
        "decisiveQuestion": {"type": "string", "minLength": 20},
        "demonstratedConsequence": {"type": "string", "minLength": 10},
        "routes": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["routeId", "thesisIds", "description", "bestObjection", "response", "decision"],
                "properties": {
                    "routeId": {"type": "string", "pattern": "^R[0-9]+$"},
                    "thesisIds": {"type": "array", "items": {"type": "string"}},
                    "description": {"type": "string", "minLength": 20},
                    "anchorCandidateIds": {"type": "array", "items": {"type": "string"}},
                    "bestObjection": {"type": "string", "minLength": 10},
                    "response": {"type": "string", "minLength": 10},
                    "decision": {"enum": ["selected", "rejected", "open"]},
                    "decisionReason": {"type": "string", "minLength": 5},
                },
            },
        },
        "selectedRouteId": {"type": ["string", "null"]},
        "humanDecisionId": {"type": ["string", "null"]},
        "singleRouteReason": {"type": ["string", "null"]},
        "complexityReason": {"type": ["string", "null"]},
        "motherSentence": {"type": ["string", "null"]},
        "decisiveFactIds": {"type": "array", "items": {"type": "string"}},
        "decisiveDocumentIds": {"type": "array", "items": {"type": "string"}},
        # Candidatas a âncora, declaradas com identidade em F4. A verificação da
        # íntegra é trabalho de F7; aqui só se registra o que se pretende usar,
        # para que a ficha de F7 possa ser confrontada com a promessa de F4.
        "anchorCandidates": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["anchorCandidateId", "identity", "expectedOperation"],
                "properties": {
                    "anchorCandidateId": {"type": "string", "pattern": "^ANC-[A-Za-z0-9._-]+$"},
                    "identity": {"type": "string", "minLength": 6},
                    "expectedOperation": {"enum": ["apply", "distinguish", "limit_scope", "argue_overruling"]},
                    "fullTextObtained": {"type": "boolean"},
                    "note": {"type": ["string", "null"]},
                },
            },
        },
        "mandatoryContent": {"type": "array", "items": {"type": "string"}},
        "blockingIssues": {"type": "array"},
        # E5 — cobertura por família de tese. Nove famílias, cada uma examinada.
        # É proibido mínimo numérico de teses: o dever é examinar, não produzir.
        "thesisFamilyCoverage": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["family", "status"],
                "properties": {
                    "family": {"enum": NOVE_FAMILIAS},
                    "status": {"enum": ["examinada_proposta", "examinada_descartada", "nao_aplicavel"]},
                    "reason": {"type": ["string", "null"]},
                    "routeIds": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
    },
    "F4_CASE_ACCEPTANCE_TESTS.json": {
        "executionMode": {"enum": ["legacy", "prospective", "retrospective_baseline"]},
        "draftedBeforeFinalText": {"type": "boolean"},
        "frozenAt": {"type": "string", "format": "date-time"},
        "finalProducedAt": {"type": "string", "format": "date-time"},
        "retrospectiveReason": {"type": "string", "minLength": 1},
    },
    "F4_THESIS_MATURITY.json": {
        "theses": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "helenaDecision": {"enum": ["adopt", "adopt_with_qualification", "reject_current_version", "review_required"]},
                    "ciceroDecision": {"enum": ["adopt", "adopt_with_qualification", "reject_current_version", "review_required"]},
                    "helenaEvidenceId": {"type": "string", "minLength": 1},
                    "ciceroEvidenceId": {"type": "string", "minLength": 1},
                    "helenaDecisionLocator": {"type": "string", "minLength": 1},
                    "ciceroDecisionLocator": {"type": "string", "minLength": 1},
                },
            },
        },
    },
    "F7_CASE_TEST_RESULTS.json": {
        "antiFraud": {
            "type": "object",
            "required": ["mutationScore", "killed", "total", "mutations"],
            "properties": {
                "mutationScore": {"type": "number", "minimum": 0, "maximum": 1},
                "semanticMutationScore": {"type": "number", "minimum": 0, "maximum": 1},
                "killed": {"type": "integer", "minimum": 0},
                "total": {"type": "integer", "minimum": 0},
                "mutations": {"type": "array"},
                "survivors": {"type": "array"},
            },
            "additionalProperties": True,
        },
    },
}


def generate() -> None:
    schema_dir = FORJA / "n4_schemas"
    contract_dir = FORJA / "phase_contracts_n4"
    schema_dir.mkdir(parents=True, exist_ok=True)
    contract_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(schema_dir / "common.schema.json", COMMON)
    catalog = {"schemaVersion": 1, "specVersion": SPEC_VERSION, "artifacts": {}}
    for filename, spec in ARTIFACT_SPECS.items():
        schema_name = spec.get("schema") or filename.removesuffix(".json").lower() + ".schema.json"
        common = deepcopy(COMMON)
        common.pop("$schema", None)
        common.pop("$id", None)
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": schema_name,
            "allOf": [
                common,
                {
                    "type": "object",
                    "properties": {
                        "artifactType": {"const": spec["type"]},
                        "phase": {"const": spec["phase"]},
                    },
                    "allOf": [
                        {
                            "if": {"properties": {"applicability": {"not": {"const": "not_applicable"}}}},
                            "then": {"required": spec["keys"]},
                        }
                    ],
                },
            ],
        }
        if filename == "F2_QUESTION_TREE.json":
            schema["allOf"][1].setdefault("properties", {}).update(deepcopy(QUESTION_TREE_SCHEMA["properties"]))
            schema["allOf"][1].setdefault("allOf", []).extend(deepcopy(QUESTION_TREE_SCHEMA["allOf"]))
        schema["allOf"][1].setdefault("properties", {}).update(deepcopy(SCHEMA_OVERRIDES.get(filename, {})))
        atomic_write_json(schema_dir / schema_name, schema)
        catalog["artifacts"][filename] = {**spec, "schema": schema_name}
    atomic_write_json(schema_dir / "ARTIFACT_CATALOG.json", catalog)
    for index, phase in enumerate(PHASES):
        base = read_json(FORJA / "phase_contracts" / f"F{index}.json", {})
        extension = EXTENSIONS[f"F{index}"]
        candidate = {
            **base,
            "schemaVersion": 2,
            "specVersion": SPEC_VERSION,
            "mode": "candidate_shadow",
            "n4RequiredOutputs": extension["outputs"],
            "n4RequiredGates": extension["gates"],
            "baseContract": f"../phase_contracts/F{index}.json",
        }
        atomic_write_json(contract_dir / f"F{index}.json", candidate)
    atomic_write_json(contract_dir / "EXTENSIONS.json", {"schemaVersion": 1, "specVersion": SPEC_VERSION, "phases": EXTENSIONS})


if __name__ == "__main__":
    generate()
