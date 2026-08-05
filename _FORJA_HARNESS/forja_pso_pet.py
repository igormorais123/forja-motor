"""PSO-Pet: problem-solving design audit for FORJA petitions.

The module is additive and shadow-only. It validates a prospective PSO_CASE.json
and audits existing N4 artifacts without changing case state or delivery gates.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from forja_n3_common import atomic_write_json, now_iso, read_json, resolve_case_dir


METHOD_VERSION = "PSO-PET-1.0"
PROFILES = {"light", "full", "intensive"}
SOURCE_ROLES = {"primary_input", "official", "secondary", "human_decision", "final_output"}
MATERIAL = {"decisive", "material"}


def issue(code: str, detail: str, *, severity: str = "p0", dimension: str | None = None) -> dict:
    value = {"code": code, "severity": severity, "detail": detail}
    if dimension:
        value["dimension"] = dimension
    return value


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _norm(value: Any) -> str:
    return re.sub(r"\W+", " ", str(value or "").casefold()).strip()


def _ids(items: list[dict], key: str, code: str, findings: list[dict]) -> set[str]:
    seen: set[str] = set()
    for item in items:
        value = str(item.get(key) or "").strip()
        if not value:
            findings.append(issue(code, f"{key} ausente"))
        elif value in seen:
            findings.append(issue(code, f"{key} duplicado: {value}"))
        seen.add(value)
    return seen


def _parse_iso(value: Any) -> datetime | None:
    if not _text(value):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def _registry(payload: dict) -> tuple[dict[str, dict], list[dict]]:
    findings: list[dict] = []
    items = payload.get("sourceRegistry") or []
    _ids(items, "sourceId", "PSO-SOURCE-ID", findings)
    result: dict[str, dict] = {}
    for item in items:
        sid = str(item.get("sourceId") or "")
        if item.get("role") not in SOURCE_ROLES:
            findings.append(issue("PSO-SOURCE-ROLE", f"{sid}: papel de fonte inválido"))
        if item.get("role") != "human_decision" and not _text(item.get("locator")):
            findings.append(issue("PSO-SOURCE-LOCATOR", f"{sid}: fonte sem localizador", severity="p1"))
        result[sid] = item
    return result, findings


def _check_refs(
    refs: list[str],
    registry: dict[str, dict],
    findings: list[dict],
    *,
    owner: str,
    allow_final: bool = False,
) -> None:
    if not refs:
        findings.append(issue("PSO-SOURCE-MISSING", f"{owner}: sem fonte"))
        return
    for ref in refs:
        if ref not in registry:
            findings.append(issue("PSO-SOURCE-DANGLING", f"{owner}: fonte inexistente {ref}"))
        elif registry[ref].get("role") == "final_output" and not allow_final:
            findings.append(issue("PSO-SOURCE-CIRCULAR", f"{owner}: usa o próprio produto final como prova de entrada"))


def validate_plan(payload: dict) -> list[dict]:
    findings: list[dict] = []
    if payload.get("methodVersion") != METHOD_VERSION:
        findings.append(issue("PSO-VERSION", f"methodVersion deve ser {METHOD_VERSION}"))
    profile = payload.get("profile")
    if profile not in PROFILES:
        findings.append(issue("PSO-PROFILE", "perfil deve ser light, full ou intensive"))
    if not _text(payload.get("caseId")):
        findings.append(issue("PSO-CASE-ID", "caseId ausente"))

    if payload.get("executionMode") == "prospective":
        frozen = _parse_iso(payload.get("frozenAt"))
        final = _parse_iso(payload.get("finalProducedAt")) if payload.get("finalProducedAt") else None
        if not frozen:
            findings.append(issue("PSO-TIME-EVIDENCE", "plano prospectivo exige frozenAt ISO 8601 com fuso"))
        if payload.get("finalProducedAt") and not final:
            findings.append(issue("PSO-TIME-EVIDENCE", "finalProducedAt deve ser ISO 8601 com fuso"))
        if frozen and final and frozen >= final:
            findings.append(issue("PSO-TIME-ORDER", "o plano deve ser congelado antes da versão final"))

    registry, source_findings = _registry(payload)
    findings.extend(source_findings)

    context = payload.get("contextPlan") or {}
    packets = context.get("issuePackets") or []
    _ids(packets, "issueId", "PSO-CONTEXT-ID", findings)
    if not _text(context.get("problemKernel")):
        findings.append(issue("PSO-CONTEXT-KERNEL", "núcleo do problema ausente", dimension="CDI"))
    if not packets:
        findings.append(issue("PSO-CONTEXT-PACKETS", "nenhum pacote de questão", dimension="CDI"))
    for packet in packets:
        pid = str(packet.get("issueId") or "?")
        if not _text(packet.get("question")):
            findings.append(issue("PSO-CONTEXT-QUESTION", f"{pid}: pergunta ausente", dimension="CDI"))
        _check_refs(packet.get("evidenceRefs") or [], registry, findings, owner=f"pacote {pid}")
        if len(str(packet.get("embeddedText") or "")) > 2000:
            findings.append(issue("PSO-CONTEXT-BLOAT", f"{pid}: texto bruto excede 2.000 caracteres; usar referência", severity="p1", dimension="CDI"))
        if not packet.get("returnConditions"):
            findings.append(issue("PSO-CONTEXT-RETURN", f"{pid}: sem condição de reabertura", severity="p1", dimension="CDI"))

    problem = payload.get("problemDefinition") or {}
    required_problem = (
        "command", "currentState", "desiredState", "gap", "interventionScope",
        "directOutcome", "ultimateOutcome", "problemStatement",
    )
    for key in required_problem:
        if not _text(problem.get(key)):
            findings.append(issue("PSO-PROBLEM-FIELD", f"problemDefinition.{key} ausente", dimension="PDI"))
    _check_refs(problem.get("currentStateEvidenceIds") or [], registry, findings, owner="situação atual")
    if _norm(problem.get("currentState")) == _norm(problem.get("desiredState")) and _text(problem.get("currentState")):
        findings.append(issue("PSO-PROBLEM-NO-GAP", "situação atual e desejada são equivalentes", dimension="PDI"))
    if _norm(problem.get("directOutcome")) == _norm(problem.get("ultimateOutcome")) and _text(problem.get("directOutcome")):
        findings.append(issue("PSO-PROBLEM-OUTCOME-CONFLATION", "resultado direto foi confundido com resultado final multicausal", dimension="PDI"))
    if not problem.get("boundaries"):
        findings.append(issue("PSO-PROBLEM-BOUNDARY", "limites de competência, cognição, prazo ou prova ausentes", dimension="PDI"))

    diagnosis = payload.get("diagnosis") or {}
    factors = diagnosis.get("factors") or []
    factor_ids = _ids(factors, "factorId", "PSO-DIAG-FACTOR-ID", findings)
    if not _text(diagnosis.get("story")):
        findings.append(issue("PSO-DIAG-STORY", "história diagnóstica ausente", dimension="DCI"))
    if not _text(diagnosis.get("interventionLever")):
        findings.append(issue("PSO-DIAG-LEVER", "elo atacável pela petição ausente", dimension="DCI"))
    for factor in factors:
        fid = str(factor.get("factorId") or "?")
        if factor.get("kind") not in {"cause", "symptom", "consequence", "obstacle", "opportunity"}:
            findings.append(issue("PSO-DIAG-KIND", f"{fid}: tipo inválido", dimension="DCI"))
        _check_refs(factor.get("evidenceIds") or [], registry, findings, owner=f"fator {fid}")
    relations = diagnosis.get("relations") or []
    for relation in relations:
        if relation.get("from") not in factor_ids or relation.get("to") not in factor_ids:
            findings.append(issue("PSO-DIAG-RELATION", "relação aponta para fator inexistente", dimension="DCI"))
        if not _text(relation.get("reason")):
            findings.append(issue("PSO-DIAG-RELATION", "relação sem justificativa", dimension="DCI"))
    rivals = diagnosis.get("rivalExplanations") or []
    if profile in {"full", "intensive"} and not rivals:
        findings.append(issue("PSO-DIAG-RIVAL", "caso completo/intensivo sem explicação rival", dimension="DCI"))
    for rival in rivals:
        if not _text(rival.get("statement")) or not _text(rival.get("discriminatingEvidence")):
            findings.append(issue("PSO-DIAG-RIVAL", "explicação rival sem enunciado ou teste discriminante", dimension="DCI"))

    requirements = payload.get("requirements") or {}
    all_requirements: list[dict] = []
    requirement_ids: set[str] = set()
    for group in ("functional", "user", "boundaries", "restrictions"):
        items = requirements.get(group) or []
        if not items:
            findings.append(issue("PSO-REQ-GROUP", f"grupo de requisitos vazio: {group}", dimension="RTI"))
        ids = _ids(items, "requirementId", "PSO-REQ-ID", findings)
        if requirement_ids.intersection(ids):
            findings.append(issue("PSO-REQ-ID", f"ID repetido entre grupos: {sorted(requirement_ids.intersection(ids))}", dimension="RTI"))
        requirement_ids.update(ids)
        all_requirements.extend(items)
        for item in items:
            rid = str(item.get("requirementId") or "?")
            if not _text(item.get("text")):
                findings.append(issue("PSO-REQ-TEXT", f"{rid}: requisito vazio", dimension="RTI"))
            if group == "boundaries" and item.get("negotiable") is not False:
                findings.append(issue("PSO-REQ-BOUNDARY", f"{rid}: condição de contorno não pode ser negociável", dimension="RTI"))
            if group == "restrictions" and item.get("negotiable") is not True:
                findings.append(issue("PSO-REQ-RESTRICTION", f"{rid}: restrição deve ser explicitamente negociável", dimension="RTI"))

    options = payload.get("options") or []
    option_ids = _ids(options, "optionId", "PSO-OPTION-ID", findings)
    viable = [item for item in options if item.get("viability") == "viable"]
    minimum = 1 if profile == "light" else 2
    if len(viable) < minimum:
        findings.append(issue("PSO-OPTION-ALTERNATIVES", f"perfil {profile} exige {minimum} alternativa(s) viável(is)", dimension="AQI"))
    signatures: set[tuple[str, str, str]] = set()
    for option in viable:
        oid = str(option.get("optionId") or "?")
        signature = (_norm(option.get("vehicle")), _norm(option.get("mechanism")), _norm(option.get("evidenceStrategy")))
        if signature in signatures:
            findings.append(issue("PSO-OPTION-DUPLICATE", f"{oid}: alternativa difere apenas no rótulo", dimension="AQI"))
        signatures.add(signature)
        for field in ("vehicle", "mechanism", "directOutcome", "bestObjection"):
            if not _text(option.get(field)):
                findings.append(issue("PSO-OPTION-FIELD", f"{oid}.{field} ausente", dimension="AQI" if field != "mechanism" else "MSI"))
        addressed = set(option.get("requirementsAddressed") or [])
        if not addressed or not addressed.issubset(requirement_ids):
            findings.append(issue("PSO-OPTION-REQUIREMENTS", f"{oid}: requisitos ausentes ou inválidos", dimension="RTI"))

    selection = payload.get("selection") or {}
    selected = selection.get("selectedOptionId")
    if selected not in option_ids:
        findings.append(issue("PSO-SELECTION-ID", "alternativa selecionada não existe", dimension="AQI"))
    if not _text(selection.get("reason")):
        findings.append(issue("PSO-SELECTION-REASON", "seleção sem comparação justificada", dimension="AQI"))
    if profile == "light" and len(viable) == 1 and not _text(selection.get("alternativeConsidered")):
        findings.append(issue("PSO-SELECTION-LIGHT", "perfil leve deve registrar a alternativa considerada e descartada", severity="p1", dimension="AQI"))

    validation = payload.get("validation") or {}
    checks = validation.get("requirementChecks") or []
    checked = {str(item.get("requirementId")) for item in checks}
    material_ids = {str(item.get("requirementId")) for item in all_requirements if item.get("materiality") in MATERIAL}
    for rid in sorted(material_ids - checked):
        findings.append(issue("PSO-TRACE-MISSING", f"requisito material sem validação: {rid}", dimension="RTI"))
    for check in checks:
        if check.get("requirementId") not in requirement_ids:
            findings.append(issue("PSO-TRACE-DANGLING", "validação aponta para requisito inexistente", dimension="RTI"))
        if check.get("status") not in {"planned", "pass", "blocked", "fail"}:
            findings.append(issue("PSO-VALIDATION-STATUS", "status de validação inválido", dimension="VSI"))
        if check.get("status") in {"pass", "fail"} and not check.get("evidenceIds"):
            findings.append(issue("PSO-VALIDATION-EVIDENCE", "resultado de validação sem evidência", dimension="VSI"))
    if not _text(validation.get("bestObjection")) or not _text(validation.get("response")):
        findings.append(issue("PSO-VALIDATION-OBJECTION", "melhor objeção ou resposta ausente", dimension="VSI"))
    if not validation.get("failureConditions"):
        findings.append(issue("PSO-VALIDATION-FALSIFIABILITY", "sem condições que fariam abandonar ou revisar a solução", dimension="VSI"))

    evaluation = payload.get("evaluationPlan") or {}
    if not evaluation.get("directOutcomes"):
        findings.append(issue("PSO-EVAL-DIRECT", "avaliação sem resultados diretos observáveis", dimension="LVI"))
    if not evaluation.get("rivalExplanations"):
        findings.append(issue("PSO-EVAL-RIVAL", "avaliação sem explicações rivais", dimension="LVI"))
    if not _text(evaluation.get("observationPlan")):
        findings.append(issue("PSO-EVAL-OBSERVE", "plano de observação ausente", dimension="LVI"))
    cimo = evaluation.get("cimo") or {}
    for key in ("context", "intervention", "mechanism", "directOutcome", "limits"):
        if not _text(cimo.get(key)):
            findings.append(issue("PSO-EVAL-CIMO", f"CIMO-Pet sem {key}", dimension="LVI"))
    return findings


def _dimension(code: str, checks: list[tuple[str, bool, str]]) -> dict:
    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    return {
        "code": code,
        "status": "measured",
        "score": round(100 * passed / total, 1) if total else None,
        "passed": passed,
        "total": total,
        "criteria": [{"criterion": name, "pass": ok, "evidence": evidence} for name, ok, evidence in checks],
    }


def measure_plan(payload: dict) -> dict:
    problem = payload.get("problemDefinition") or {}
    diagnosis = payload.get("diagnosis") or {}
    requirements = payload.get("requirements") or {}
    options = payload.get("options") or []
    selection = payload.get("selection") or {}
    validation = payload.get("validation") or {}
    context = payload.get("contextPlan") or {}
    evaluation = payload.get("evaluationPlan") or {}
    registry = {str(x.get("sourceId")): x for x in payload.get("sourceRegistry") or []}
    all_req = [x for group in ("functional", "user", "boundaries", "restrictions") for x in requirements.get(group) or []]
    material_req = {str(x.get("requirementId")) for x in all_req if x.get("materiality") in MATERIAL}
    checks = {str(x.get("requirementId")): x for x in validation.get("requirementChecks") or []}
    viable = [x for x in options if x.get("viability") == "viable"]
    source_roles = [registry.get(x, {}).get("role") for x in problem.get("currentStateEvidenceIds") or []]
    dimensions = {
        "PDI": _dimension("PDI", [
            ("estado atual explícito", _text(problem.get("currentState")), "problemDefinition.currentState"),
            ("estado atual com fonte de entrada", bool(source_roles) and "final_output" not in source_roles, str(source_roles)),
            ("estado desejado distinto", _text(problem.get("desiredState")) and _norm(problem.get("currentState")) != _norm(problem.get("desiredState")), "currentState != desiredState"),
            ("lacuna explícita", _text(problem.get("gap")), "problemDefinition.gap"),
            ("escopo de intervenção", _text(problem.get("interventionScope")), "problemDefinition.interventionScope"),
            ("limites explícitos", bool(problem.get("boundaries")), "problemDefinition.boundaries"),
            ("resultado direto separado", _text(problem.get("directOutcome")) and _norm(problem.get("directOutcome")) != _norm(problem.get("ultimateOutcome")), "directOutcome != ultimateOutcome"),
            ("problema em uma frase", _text(problem.get("problemStatement")), "problemDefinition.problemStatement"),
        ]),
        "DCI": _dimension("DCI", [
            ("história diagnóstica", _text(diagnosis.get("story")), "diagnosis.story"),
            ("fatores classificados", bool(diagnosis.get("factors")) and all(x.get("kind") for x in diagnosis.get("factors") or []), "diagnosis.factors"),
            ("fatores com evidência", bool(diagnosis.get("factors")) and all(x.get("evidenceIds") for x in diagnosis.get("factors") or []), "factor.evidenceIds"),
            ("relações justificadas", bool(diagnosis.get("relations")) and all(_text(x.get("reason")) for x in diagnosis.get("relations") or []), "diagnosis.relations"),
            ("causa, sintoma e consequência separados", {x.get("kind") for x in diagnosis.get("factors") or []}.issuperset({"cause", "symptom", "consequence"}), "factor.kind"),
            ("explicação rival", bool(diagnosis.get("rivalExplanations")), "diagnosis.rivalExplanations"),
            ("teste discriminante", bool(diagnosis.get("rivalExplanations")) and all(_text(x.get("discriminatingEvidence")) for x in diagnosis.get("rivalExplanations") or []), "rival.discriminatingEvidence"),
            ("elo atacável", _text(diagnosis.get("interventionLever")), "diagnosis.interventionLever"),
        ]),
        "AQI": _dimension("AQI", [
            ("alternativas proporcionais ao perfil", len(viable) >= (1 if payload.get("profile") == "light" else 2), f"viáveis={len(viable)}"),
            ("alternativas substantivamente distintas", len({(_norm(x.get('vehicle')), _norm(x.get('mechanism')), _norm(x.get('evidenceStrategy'))) for x in viable}) == len(viable), "assinaturas"),
            ("mecanismos explícitos", bool(viable) and all(_text(x.get("mechanism")) for x in viable), "option.mechanism"),
            ("melhor objeção por alternativa", bool(viable) and all(_text(x.get("bestObjection")) for x in viable), "option.bestObjection"),
            ("seleção válida", selection.get("selectedOptionId") in {x.get("optionId") for x in options}, "selection.selectedOptionId"),
            ("razão comparativa", _text(selection.get("reason")), "selection.reason"),
        ]),
        "RTI": _dimension("RTI", [
            ("quatro grupos de requisitos", all(requirements.get(x) for x in ("functional", "user", "boundaries", "restrictions")), "requirements.*"),
            ("IDs únicos", len({x.get("requirementId") for x in all_req}) == len(all_req), "requirementId"),
            ("condições não negociáveis", bool(requirements.get("boundaries")) and all(x.get("negotiable") is False for x in requirements.get("boundaries") or []), "requirements.boundaries"),
            ("restrições negociáveis", bool(requirements.get("restrictions")) and all(x.get("negotiable") is True for x in requirements.get("restrictions") or []), "requirements.restrictions"),
            ("alternativas ligadas a requisitos", bool(viable) and all(x.get("requirementsAddressed") for x in viable), "option.requirementsAddressed"),
            ("requisitos materiais validados", material_req.issubset(checks), f"faltantes={sorted(material_req-set(checks))}"),
            ("validação com evidência ou plano", all(x.get("status") == "planned" or x.get("evidenceIds") for x in checks.values()), "validation.requirementChecks"),
        ]),
        "MSI": _dimension("MSI", [
            ("intervenção selecionada", selection.get("selectedOptionId") in {x.get("optionId") for x in options}, "selection"),
            ("mecanismo da opção selecionada", any(x.get("optionId") == selection.get("selectedOptionId") and _text(x.get("mechanism")) for x in options), "selected.mechanism"),
            ("resultado direto da opção", any(x.get("optionId") == selection.get("selectedOptionId") and _text(x.get("directOutcome")) for x in options), "selected.directOutcome"),
            ("elo diagnóstico explícito", _text(diagnosis.get("interventionLever")), "diagnosis.interventionLever"),
            ("resposta à melhor objeção", _text(validation.get("response")), "validation.response"),
            ("gatilho de mudança", bool(selection.get("switchTriggers")), "selection.switchTriggers"),
        ]),
        "VSI": _dimension("VSI", [
            ("melhor objeção", _text(validation.get("bestObjection")), "validation.bestObjection"),
            ("resposta", _text(validation.get("response")), "validation.response"),
            ("condições de falha", bool(validation.get("failureConditions")), "validation.failureConditions"),
            ("requisitos materiais cobertos", material_req.issubset(checks), "validation.requirementChecks"),
            ("Helena localizada", _text((validation.get("council") or {}).get("helenaLocator")), "validation.council.helenaLocator"),
            ("Cícero localizado", _text((validation.get("council") or {}).get("ciceroLocator")), "validation.council.ciceroLocator"),
            ("sem autoaprovação", payload.get("producerRunId") != payload.get("reviewerRunId") and _text(payload.get("reviewerRunId")), "runIds"),
        ]),
        "CDI": _dimension("CDI", [
            ("núcleo curto", 0 < len(str(context.get("problemKernel") or "")) <= 1200, "contextPlan.problemKernel"),
            ("pacotes por questão", bool(context.get("issuePackets")), "contextPlan.issuePackets"),
            ("pacotes com fontes", bool(context.get("issuePackets")) and all(x.get("evidenceRefs") for x in context.get("issuePackets") or []), "issuePacket.evidenceRefs"),
            ("sem despejo de texto", all(len(str(x.get("embeddedText") or "")) <= 2000 for x in context.get("issuePackets") or []), "issuePacket.embeddedText"),
            ("condições de retorno", bool(context.get("issuePackets")) and all(x.get("returnConditions") for x in context.get("issuePackets") or []), "issuePacket.returnConditions"),
            ("arquivo frio separado", bool(context.get("archiveRefs")), "contextPlan.archiveRefs"),
        ]),
        "LVI": _dimension("LVI", [
            ("resultados diretos observáveis", bool(evaluation.get("directOutcomes")), "evaluationPlan.directOutcomes"),
            ("resultado final separado", bool(evaluation.get("ultimateOutcomes")), "evaluationPlan.ultimateOutcomes"),
            ("explicações rivais", bool(evaluation.get("rivalExplanations")), "evaluationPlan.rivalExplanations"),
            ("plano de observação", _text(evaluation.get("observationPlan")), "evaluationPlan.observationPlan"),
            ("CIMO-Pet completo", all(_text((evaluation.get("cimo") or {}).get(x)) for x in ("context", "intervention", "mechanism", "directOutcome", "limits")), "evaluationPlan.cimo"),
            ("sem probabilidade de vitória", not re.search(r"\b\d{1,3}\s*%\b", json.dumps(evaluation, ensure_ascii=False)), "evaluationPlan"),
        ]),
    }
    scores = [value["score"] for value in dimensions.values() if value["score"] is not None]
    critical = [dimensions[x]["score"] for x in ("PDI", "DCI", "RTI", "VSI")]
    if any(item < 70 for item in critical):
        readiness = "not_ready"
    elif any(item < 80 for item in scores):
        readiness = "human_review_required"
    else:
        readiness = "ready_for_human_review"
    bottlenecks = sorted(({"dimension": key, "score": value["score"]} for key, value in dimensions.items()), key=lambda x: x["score"])[:3]
    return {"methodVersion": METHOD_VERSION, "dimensions": dimensions, "decisionReadiness": readiness, "bottlenecks": bottlenecks, "compositeScore": None, "compositeReason": "perfil vetorial; média única ocultaria gargalos"}


def audit_n4_case(case_dir: Path) -> dict:
    n4 = case_dir / "n4_artifacts"
    plan_path = n4 / "PSO_CASE.json"
    files = {path.name: read_json(path, {}) or {} for path in n4.glob("*.json")}
    findings: list[dict] = []
    q = files.get("F2_QUESTION_TREE.json", {})
    graph = files.get("F3_REASONING_GRAPH.json", {})
    theses = files.get("F4_THESIS_MATURITY.json", {})
    suite = files.get("F4_CASE_ACCEPTANCE_TESTS.json", {})
    validation = files.get("N4_VALIDATION.json", {})
    final_nodes = {
        str(node.get("id"))
        for node in graph.get("nodes") or []
        if re.search(r"(?i)(final|canonical_text_from_final)", str(node.get("sourceArtifact") or ""))
    }
    circular = []
    for question in q.get("questions") or []:
        refs = set(question.get("supportIds") or [])
        if refs and refs.issubset(final_nodes):
            circular.append(str(question.get("questionId") or "?"))
    if circular:
        findings.append(issue("PSO-AUDIT-CIRCULAR-EVIDENCE", f"questões sustentadas somente pelo produto final: {', '.join(circular)}", severity="p1"))
    tests = suite.get("tests") or []
    semantic = [item for item in tests if item.get("method") != "deterministic" or (item.get("evaluator") or {}).get("kind") not in {"contains", "not_contains"}]
    if tests and not semantic:
        findings.append(issue("PSO-AUDIT-LITERAL-ONLY", "todos os testes observados são literais; inversão semântica continua não medida", severity="p1"))
    if suite.get("executionMode") == "retrospective_baseline":
        findings.append(issue("PSO-AUDIT-RETROSPECTIVE", "suíte criada depois do texto; não mede desenho prospectivo", severity="p1"))
    pending_council = [
        str(item.get("thesisId") or "?")
        for item in theses.get("theses") or []
        if item.get("helenaDecision") in {"review_required", "reject_current_version"}
        or item.get("ciceroDecision") in {"review_required", "reject_current_version"}
    ]
    if pending_council:
        findings.append(issue("PSO-AUDIT-COUNCIL", f"teses sem liberação conjunta: {', '.join(pending_council)}", severity="p1"))
    source_codes = [str(item.get("code")) for item in validation.get("findings") or [] if str(item.get("code")).startswith("N4-SOURCE-")]
    if source_codes:
        findings.append(issue("PSO-AUDIT-SOURCE", f"integridade de fonte bloqueada: {', '.join(sorted(set(source_codes)))}"))
    plan = read_json(plan_path, None) if plan_path.exists() else None
    if plan:
        plan_findings = validate_plan(plan)
        findings.extend(plan_findings)
        profile = measure_plan(plan)
        profile["decisionReadiness"] = "blocked" if any(x["severity"] == "p0" for x in plan_findings) else profile["decisionReadiness"]
        method_status = "measured"
    else:
        profile = {
            "methodVersion": METHOD_VERSION,
            "dimensions": {key: {"code": key, "status": "not_measured", "score": None} for key in ("PDI", "DCI", "AQI", "RTI", "MSI", "VSI", "CDI", "LVI")},
            "decisionReadiness": "not_evaluated",
            "bottlenecks": [],
            "compositeScore": None,
            "compositeReason": "PSO_CASE.json ausente; ausência não é nota zero",
        }
        method_status = "not_measured"
    return {
        "schemaVersion": 1,
        "methodVersion": METHOD_VERSION,
        "generatedAt": now_iso(),
        "caseId": case_dir.name,
        "methodStatus": method_status,
        "readOnlyAudit": True,
        "proxies": {
            "questions": len(q.get("questions") or []),
            "circularQuestionSupport": circular,
            "thesisCount": len(theses.get("theses") or []),
            "alternativeComparisonMeasured": bool(plan and len(plan.get("options") or []) > 1),
            "testCount": len(tests),
            "semanticTestCount": len(semantic),
            "executionMode": suite.get("executionMode") or "unknown",
            "councilPendingTheses": pending_council,
            "sourceIntegrityCodes": sorted(set(source_codes)),
        },
        "valueProfile": profile,
        "findings": findings,
        "counts": {
            "p0": sum(x["severity"] == "p0" for x in findings),
            "p1": sum(x["severity"] == "p1" for x in findings),
        },
    }


def _valid_fixture() -> dict:
    return {
        "schemaVersion": 1,
        "methodVersion": METHOD_VERSION,
        "caseId": "case-pso-fixture",
        "profile": "full",
        "executionMode": "prospective",
        "frozenAt": "2026-07-11T10:00:00-03:00",
        "finalProducedAt": "2026-07-11T11:00:00-03:00",
        "producerRunId": "producer-a",
        "reviewerRunId": "reviewer-b",
        "sourceRegistry": [
            {"sourceId": "DOC-1", "role": "primary_input", "locator": "evento 10, p. 3"},
            {"sourceId": "LAW-1", "role": "official", "locator": "art. 1"},
            {"sourceId": "H", "role": "human_decision", "locator": "parecer Helena, item 2"},
            {"sourceId": "C", "role": "human_decision", "locator": "parecer Cícero, conclusão"},
            {"sourceId": "FINAL", "role": "final_output", "locator": "minuta final"},
        ],
        "contextPlan": {
            "problemKernel": "Decisão deixou de enfrentar prova documental material; definir veículo e pedido adequados.",
            "issuePackets": [{"issueId": "I1", "question": "A prova foi enfrentada?", "evidenceRefs": ["DOC-1", "LAW-1"], "returnConditions": ["nova decisão", "novo documento"]}],
            "archiveRefs": ["autos integrais"],
        },
        "problemDefinition": {
            "command": "Preparar resposta",
            "currentState": "Decisão não examinou o documento material indicado.",
            "currentStateEvidenceIds": ["DOC-1"],
            "desiredState": "Órgão enfrenta expressamente a prova e sua consequência jurídica.",
            "gap": "Ausência de enfrentamento verificável.",
            "interventionScope": "Demonstrar a omissão e pedir integração, sem rejulgamento incompatível.",
            "boundaries": ["cognição do recurso", "prazo", "prova já existente"],
            "directOutcome": "Pronunciamento explícito sobre a prova material.",
            "ultimateOutcome": "Alteração do resultado do processo.",
            "problemStatement": "A decisão omitiu prova material e a peça deve obter seu enfrentamento no veículo cabível.",
        },
        "diagnosis": {
            "story": "A prova está nos autos, foi invocada e não aparece na cadeia decisória; a omissão impede verificar se sua consequência foi considerada.",
            "interventionLever": "Evidenciar a ausência na cadeia alegação-prova-decisão e pedir integração específica.",
            "factors": [
                {"factorId": "F1", "kind": "cause", "statement": "prova fora da fundamentação", "evidenceIds": ["DOC-1"]},
                {"factorId": "F2", "kind": "symptom", "statement": "silêncio decisório", "evidenceIds": ["DOC-1"]},
                {"factorId": "F3", "kind": "consequence", "statement": "incerteza sobre valoração", "evidenceIds": ["DOC-1"]},
            ],
            "relations": [
                {"from": "F1", "to": "F2", "relation": "contributes_to", "reason": "a prova não aparece na motivação"},
                {"from": "F2", "to": "F3", "relation": "produces", "reason": "o silêncio impede conhecer a valoração"},
            ],
            "rivalExplanations": [{"rivalId": "R1", "statement": "a prova foi implicitamente rejeitada", "evidenceIds": ["DOC-1"], "discriminatingEvidence": "fundamento incompatível e explícito na decisão"}],
        },
        "requirements": {
            "functional": [{"requirementId": "RF1", "text": "demonstrar omissão material", "materiality": "decisive", "negotiable": False}],
            "user": [{"requirementId": "RU1", "text": "ordem decisória visível", "materiality": "material", "negotiable": False}],
            "boundaries": [{"requirementId": "RB1", "text": "respeitar cognição", "materiality": "decisive", "negotiable": False}],
            "restrictions": [{"requirementId": "RR1", "text": "síntese em até 15 páginas", "materiality": "minor", "negotiable": True}],
        },
        "options": [
            {"optionId": "O1", "label": "integração focal", "vehicle": "embargos de declaração", "evidenceStrategy": "cotejo literal", "mechanism": "tornar visível a lacuna entre alegação, prova e decisão", "directOutcome": "enfrentamento expresso", "requirementsAddressed": ["RF1", "RU1", "RB1", "RR1"], "viability": "viable", "bestObjection": "mero inconformismo"},
            {"optionId": "O2", "label": "reserva recursal", "vehicle": "recurso subsequente", "evidenceStrategy": "prequestionamento e demonstração do prejuízo", "mechanism": "preservar a questão para controle posterior", "directOutcome": "admissibilidade da questão no recurso seguinte", "requirementsAddressed": ["RF1", "RB1"], "viability": "viable", "bestObjection": "falta de esgotamento"},
        ],
        "selection": {"selectedOptionId": "O1", "reason": "atua diretamente sobre a omissão com menor custo e maior aderência ao estado atual", "rejectedReasons": {"O2": "é contingência posterior"}, "switchTriggers": ["embargos rejeitados sem enfrentamento"]},
        "validation": {
            "requirementChecks": [
                {"requirementId": "RF1", "status": "planned", "test": "cotejo alegação-prova-decisão"},
                {"requirementId": "RU1", "status": "planned", "test": "ordem decisória na síntese"},
                {"requirementId": "RB1", "status": "planned", "test": "pedido integrativo sem rejulgamento"},
            ],
            "bestObjection": "a decisão rejeitou implicitamente a prova",
            "response": "a fundamentação não contém premissa incompatível nem análise identificável da prova",
            "failureConditions": ["localização de fundamento explícito que enfrente a prova"],
            "council": {"helenaLocator": "H", "ciceroLocator": "C"},
        },
        "interventionPlan": {"deadline": "dupla conferência", "reviewer": "responsável humano", "managementUpdate": True},
        "evaluationPlan": {
            "directOutcomes": ["decisão enfrenta a prova"],
            "ultimateOutcomes": ["eventual alteração do resultado"],
            "rivalExplanations": ["mudança decorreu de fundamento independente"],
            "observationPlan": "comparar a decisão posterior com a matriz de questões e registrar o elo enfrentado",
            "cimo": {"context": "omissão sobre prova material", "intervention": "cotejo focal", "mechanism": "visibilidade da lacuna decisória", "directOutcome": "enfrentamento expresso", "limits": "não garante mudança do resultado"},
        },
    }


def mutation_benchmark() -> dict:
    base = _valid_fixture()
    mutations: list[tuple[str, str, Callable[[dict], None]]] = [
        ("missing_input_evidence", "PSO-SOURCE-MISSING", lambda x: x["problemDefinition"].update(currentStateEvidenceIds=[])),
        ("output_as_input_evidence", "PSO-SOURCE-CIRCULAR", lambda x: x["problemDefinition"].update(currentStateEvidenceIds=["FINAL"])),
        ("no_problem_gap", "PSO-PROBLEM-NO-GAP", lambda x: x["problemDefinition"].update(desiredState=x["problemDefinition"]["currentState"])),
        ("outcome_conflation", "PSO-PROBLEM-OUTCOME-CONFLATION", lambda x: x["problemDefinition"].update(ultimateOutcome=x["problemDefinition"]["directOutcome"])),
        ("missing_diagnostic_story", "PSO-DIAG-STORY", lambda x: x["diagnosis"].update(story="")),
        ("missing_rival", "PSO-DIAG-RIVAL", lambda x: x["diagnosis"].update(rivalExplanations=[])),
        ("duplicate_option", "PSO-OPTION-DUPLICATE", lambda x: x["options"][1].update(vehicle=x["options"][0]["vehicle"], mechanism=x["options"][0]["mechanism"], evidenceStrategy=x["options"][0]["evidenceStrategy"])),
        ("single_option", "PSO-OPTION-ALTERNATIVES", lambda x: x.update(options=x["options"][:1])),
        ("missing_requirement_trace", "PSO-TRACE-MISSING", lambda x: x["validation"].update(requirementChecks=x["validation"]["requirementChecks"][:1])),
        ("invalid_selection", "PSO-SELECTION-ID", lambda x: x["selection"].update(selectedOptionId="O404")),
        ("missing_best_objection", "PSO-VALIDATION-OBJECTION", lambda x: x["validation"].update(bestObjection="")),
        ("context_dump", "PSO-CONTEXT-BLOAT", lambda x: x["contextPlan"]["issuePackets"][0].update(embeddedText="x" * 2500)),
        ("temporal_fraud", "PSO-TIME-ORDER", lambda x: x.update(frozenAt="2026-07-11T12:00:00-03:00")),
    ]
    results = []
    for name, expected, mutate in mutations:
        candidate = copy.deepcopy(base)
        mutate(candidate)
        found = {x["code"] for x in validate_plan(candidate)}
        results.append({"name": name, "expected": expected, "detected": expected in found, "codes": sorted(found)})
    benign = [
        copy.deepcopy(base),
        copy.deepcopy(base),
        copy.deepcopy(base),
        copy.deepcopy(base),
        copy.deepcopy(base),
    ]
    benign[1]["contextPlan"]["archiveRefs"].append("anexo histórico")
    benign[2]["selection"]["switchTriggers"].append("documento novo")
    benign[3]["options"].append({"optionId": "O3", "label": "não agir", "vehicle": "monitoramento", "evidenceStrategy": "aguardar ato", "mechanism": "evitar preclusão estratégica inexistente", "directOutcome": "preservar recursos", "requirementsAddressed": ["RB1"], "viability": "non_viable", "bestObjection": "inércia"})
    benign[4]["requirements"]["restrictions"][0]["text"] = "síntese preferencial, ajustável à complexidade"
    benign_results = []
    for index, candidate in enumerate(benign, 1):
        current = validate_plan(candidate)
        benign_results.append({"name": f"benign_{index}", "falseP0": any(x["severity"] == "p0" for x in current), "codes": sorted({x["code"] for x in current})})
    detected = sum(x["detected"] for x in results)
    false_p0 = sum(x["falseP0"] for x in benign_results)
    return {
        "mutations": len(results),
        "detected": detected,
        "semanticMutationRecall": round(detected / len(results), 4),
        "benignControls": len(benign_results),
        "falseBlockingRate": round(false_p0 / len(benign_results), 4),
        "specificity": round(1 - false_p0 / len(benign_results), 4),
        "mutationResults": results,
        "benignResults": benign_results,
    }


def benchmark(state_root: Path) -> dict:
    cases = []
    for case_dir in sorted(state_root.iterdir()):
        if case_dir.is_dir() and (case_dir / "n4_artifacts" / "F2_QUESTION_TREE.json").exists():
            cases.append(audit_n4_case(case_dir))
    mutation = mutation_benchmark()
    summary = {
        "casesAudited": len(cases),
        "psoPlansMeasured": sum(x["methodStatus"] == "measured" for x in cases),
        "methodDimensionsNotMeasured": sum(x["methodStatus"] != "measured" for x in cases) * 8,
        "circularEvidenceCases": sum(bool(x["proxies"]["circularQuestionSupport"]) for x in cases),
        "retrospectiveOnlyCases": sum(x["proxies"]["executionMode"] == "retrospective_baseline" for x in cases),
        "literalOnlyCases": sum(x["proxies"]["testCount"] > 0 and x["proxies"]["semanticTestCount"] == 0 for x in cases),
        "councilPendingCases": sum(bool(x["proxies"]["councilPendingTheses"]) for x in cases),
        "sourceBlockedCases": sum(bool(x["proxies"]["sourceIntegrityCodes"]) for x in cases),
        "newActionableSignals": sum(len(x["findings"]) for x in cases),
        "semanticMutationRecall": mutation["semanticMutationRecall"],
        "falseBlockingRate": mutation["falseBlockingRate"],
    }
    return {"schemaVersion": 1, "methodVersion": METHOD_VERSION, "generatedAt": now_iso(), "summary": summary, "mutationBenchmark": mutation, "cases": cases}


def main() -> None:
    parser = argparse.ArgumentParser(description="PSO-Pet shadow validator and benchmark")
    sub = parser.add_subparsers(dest="command", required=True)
    validate_cmd = sub.add_parser("validate-plan")
    validate_cmd.add_argument("plan")
    audit_cmd = sub.add_parser("audit-case")
    audit_cmd.add_argument("case")
    benchmark_cmd = sub.add_parser("benchmark")
    benchmark_cmd.add_argument("--state-root", default=str(Path(__file__).parent / "state"))
    benchmark_cmd.add_argument("--output")
    example_cmd = sub.add_parser("write-example")
    example_cmd.add_argument("--output", default=str(Path(__file__).parent / "pso_schemas" / "PSO_CASE_EXAMPLE.json"))
    args = parser.parse_args()
    if args.command == "validate-plan":
        payload = read_json(Path(args.plan), {}) or {}
        result = {"findings": validate_plan(payload), "valueProfile": measure_plan(payload)}
    elif args.command == "audit-case":
        result = audit_n4_case(resolve_case_dir(args.case))
    elif args.command == "benchmark":
        result = benchmark(Path(args.state_root))
        if args.output:
            atomic_write_json(Path(args.output), result)
    else:
        result = _valid_fixture()
        atomic_write_json(Path(args.output), result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
