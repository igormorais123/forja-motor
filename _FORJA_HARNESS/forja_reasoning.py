"""Structural reasoning validators for FORJA N4.

The module checks coverage and relationships. It deliberately does not decide
the legal merits or manufacture missing answers.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from forja_n4_common import ids_unique, issue, validate_file
from forja_n3_common import resolve_case_dir
from forja_exploracao_100 import PROTOCOL_VERSION, STATUSES, validate_exploration_100


QUESTION_CATEGORIES = {
    "fact", "evidence", "procedural_event", "merit", "precedent", "calculation",
    "request", "risk", "opponent_response", "science", "visual", "mandate",
    "jurisdiction", "ethics", "alternative", "execution", "communication",
}
COVERAGE_STATES = {"covered", "partially_covered", "intentionally_excluded", "blocked", "not_applicable"}
RELATIONS = {
    "supports", "contradicts", "qualifies", "depends_on", "responds_to", "ignored_by",
    "distinguishes", "quantifies", "limits", "records", "justifies", "tested_by", "resolves",
}


def validate_question_tree(payload: dict) -> list[dict]:
    questions = payload.get("questions") or []
    findings = ids_unique(questions, "questionId", "N4-Q-ID")
    ids = {str(item.get("questionId")) for item in questions}
    material = answered = blocked = 0
    for item in questions:
        qid = str(item.get("questionId") or "?")
        if item.get("category") not in QUESTION_CATEGORIES:
            findings.append(issue("N4-Q-CATEGORY", f"{qid}: categoria inválida"))
        if item.get("parentId") and item.get("parentId") not in ids:
            findings.append(issue("N4-Q-PARENT", f"{qid}: parentId inexistente"))
        # Os três estados canônicos valem para toda pergunta, material ou não.
        # Antes de 25/07/2026 o validador tolerava `retired` e `accepted_by_human`,
        # que o schema gerado nunca admitiu: um produtor podia emiti-los, passar
        # aqui e ser rejeitado adiante — ou, em pergunta não material, passar sem
        # exame algum.
        if item.get("status") not in STATUSES:
            findings.append(issue(
                "N4-Q-STATUS",
                f"{qid}: estado {item.get('status')!r} fora do contrato; "
                f"use {', '.join(sorted(STATUSES))}",
            ))
        if item.get("materiality") in {"decisive", "material"}:
            material += 1
            status = item.get("status")
            if status == "answered":
                answered += 1
                if not str(item.get("answer") or "").strip():
                    findings.append(issue("N4-Q-EMPTY-ANSWER", f"{qid}: resposta material vazia"))
                if not item.get("supportIds") and item.get("category") in {"fact", "evidence", "procedural_event", "calculation"}:
                    findings.append(issue("N4-Q-NO-SUPPORT", f"{qid}: resposta factual sem lastro"))
            elif status == "blocked":
                blocked += 1
                if not str(item.get("unansweredConsequence") or "").strip():
                    findings.append(issue("N4-Q-NO-CONSEQUENCE", f"{qid}: bloqueio sem consequência"))
            else:
                # Os estados canônicos são `answered`, `blocked` e `not_applicable`,
                # e questão material não pode ser não-aplicável: se é material,
                # incide. Os antigos `retired` e `accepted_by_human` saíram em
                # 25/07/2026 — o schema F2-A nunca os admitiu, nenhuma das treze
                # árvores reais os usa, e enquanto existiam davam rota de fuga ao
                # gate de questão material não resolvida.
                findings.append(issue("N4-Q-UNRESOLVED", f"{qid}: questão material sem resposta ou bloqueio"))
    declared = payload.get("coverage") or {}
    actual = {"total": len(questions), "material": material, "answeredMaterial": answered, "blockedMaterial": blocked}
    for key, value in actual.items():
        if declared.get(key) != value:
            findings.append(issue("N4-Q-COUNT", f"coverage.{key}={declared.get(key)!r}; calculado={value}"))
    # Compatibilidade histórica: árvores N4 anteriores continuam auditáveis pelo
    # contrato antigo. Todo artefato que declara o protocolo F2-A recebe também
    # os gates fortes de 100 perguntas, dez óticas, proveniência e handoff.
    if payload.get("protocolVersion") == PROTOCOL_VERSION:
        strict = validate_exploration_100(payload)
        existing = {(item.get("code"), item.get("detail")) for item in findings}
        findings.extend(item for item in strict if (item.get("code"), item.get("detail")) not in existing)
    return findings


def validate_coverage(payload: dict) -> list[dict]:
    items = payload.get("items") or []
    findings = ids_unique(items, "coverageId", "N4-COV-ID")
    for item in items:
        cid = str(item.get("coverageId") or "?")
        status = item.get("status")
        if status not in COVERAGE_STATES:
            findings.append(issue("N4-COV-STATUS", f"{cid}: estado inválido"))
        material = item.get("materiality") in {"decisive", "material"}
        if material and status == "covered" and not item.get("draftParagraphIds"):
            findings.append(issue("N4-COV-NO-PARAGRAPH", f"{cid}: item material sem parágrafo correspondente"))
        if material and status == "partially_covered" and not str(item.get("residualRisk") or "").strip():
            findings.append(issue("N4-COV-PARTIAL", f"{cid}: cobertura parcial sem risco residual"))
        if status == "intentionally_excluded":
            if not str(item.get("strategicReason") or "").strip():
                findings.append(issue("N4-COV-EXCLUSION", f"{cid}: exclusão sem razão estratégica"))
            if material and not all(item.get(key) for key in ("helenaDecision", "ciceroDecision")):
                findings.append(issue("N4-COV-COUNCIL", f"{cid}: exclusão material sem decisão Helena/Cícero"))
        if material and status in {"blocked", "not_applicable"} and not str(item.get("reason") or "").strip():
            findings.append(issue("N4-COV-BLOCK", f"{cid}: item material sem justificativa"))
    return findings


def _dependency_cycles(edges: list[dict]) -> list[list[str]]:
    graph: dict[str, list[str]] = {}
    for edge in edges:
        if edge.get("relation") == "depends_on":
            graph.setdefault(str(edge.get("from")), []).append(str(edge.get("to")))
    cycles: list[list[str]] = []
    visiting: list[str] = []
    visited: set[str] = set()

    def walk(node: str) -> None:
        if node in visiting:
            cycles.append(visiting[visiting.index(node):] + [node])
            return
        if node in visited:
            return
        visiting.append(node)
        for nxt in graph.get(node, []):
            walk(nxt)
        visiting.pop()
        visited.add(node)

    for node in graph:
        walk(node)
    return cycles


def validate_graph(payload: dict) -> list[dict]:
    nodes = payload.get("nodes") or []
    edges = payload.get("edges") or []
    findings = ids_unique(nodes, "id", "N4-GRAPH-NODE") + ids_unique(edges, "edgeId", "N4-GRAPH-EDGE")
    node_ids = {str(item.get("id")) for item in nodes}
    for edge in edges:
        eid = str(edge.get("edgeId") or "?")
        for key in ("from", "to"):
            if edge.get(key) not in node_ids:
                findings.append(issue("N4-GRAPH-DANGLING", f"{eid}: {key} aponta para nó inexistente"))
        relation = edge.get("relation")
        if relation not in RELATIONS:
            findings.append(issue("N4-GRAPH-RELATION", f"{eid}: relação inválida {relation!r}"))
        if relation in {"supports", "justifies"} and edge.get("scope") not in {"full", "partial"}:
            findings.append(issue("N4-GRAPH-SCOPE", f"{eid}: relação de sustentação sem escopo"))
        if not str(edge.get("reason") or "").strip():
            findings.append(issue("N4-GRAPH-REASON", f"{eid}: relação sem razão"))
    for cycle in _dependency_cycles(edges):
        findings.append(issue("N4-GRAPH-CYCLE", "dependência circular: " + " -> ".join(cycle)))
    return findings


def validate_theses(payload: dict) -> list[dict]:
    theses = payload.get("theses") or []
    findings = ids_unique(theses, "thesisId", "N4-THESIS-ID")
    allowed_decisions = {"adopt", "adopt_with_qualification", "reject_current_version", "review_required"}
    for thesis in theses:
        tid = str(thesis.get("thesisId") or "?")
        if thesis.get("role") not in {"primary", "subsidiary", "reserve", "immature"}:
            findings.append(issue("N4-THESIS-ROLE", f"{tid}: papel inválido"))
        if not str(thesis.get("bestObjection") or "").strip():
            findings.append(issue("N4-THESIS-OBJECTION", f"{tid}: falta melhor objeção"))
        if not thesis.get("helenaDecision") or not thesis.get("ciceroDecision"):
            findings.append(issue("N4-THESIS-COUNCIL", f"{tid}: falta decisão Helena/Cícero"))
            continue
        for actor in ("helena", "cicero"):
            decision = thesis.get(f"{actor}Decision")
            if decision not in allowed_decisions:
                findings.append(issue("N4-THESIS-COUNCIL-DECISION", f"{tid}: decisão {actor} inválida"))
            if not thesis.get(f"{actor}EvidenceId") or not thesis.get(f"{actor}DecisionLocator"):
                findings.append(issue("N4-THESIS-COUNCIL-EVIDENCE", f"{tid}: decisão {actor} sem parecer e localizador verificáveis"))
            if decision in {"reject_current_version", "review_required"}:
                findings.append(issue("N4-THESIS-COUNCIL-PENDING", f"{tid}: {actor} não aprovou a tese para uso final", severity="p1"))
    return findings


def validate_conducts(payload: dict) -> list[dict]:
    items = payload.get("conducts") or []
    findings = ids_unique(items, "conductId", "N4-COND-ID")
    for item in items:
        cid = str(item.get("conductId") or "?")
        status = item.get("verificationStatus")
        if status not in {"verified", "partial", "not_verified", "contradicted"}:
            findings.append(issue("N4-COND-STATUS", f"{cid}: verificação inválida"))
        if status in {"not_verified", "contradicted"} and item.get("externalPhrasingAllowed") is not None:
            findings.append(issue("N4-COND-EXTERNAL", f"{cid}: conduta não confirmada não pode ser externalizada"))
        if item.get("externalPhrasingAllowed") and item.get("ciceroApproval") != "approved":
            findings.append(issue("N4-COND-CICERO", f"{cid}: formulação externa sem aprovação de Cícero"))
    return findings


def validate_decision_factors(payload: dict) -> list[dict]:
    findings = ids_unique(payload.get("decisions") or [], "decisionId", "N4-DEC-ID")
    for decision in payload.get("decisions") or []:
        if not decision.get("decisionSourceId") or not decision.get("locator"):
            findings.append(issue("N4-DEC-SOURCE", f"{decision.get('decisionId')}: decisão sem fonte/localizador"))
        for factor in decision.get("factors") or []:
            if factor.get("kind") not in {"explicit_requirement", "evidence_assessment", "judicial_caution", "open_question"}:
                findings.append(issue("N4-DEC-KIND", f"{factor.get('factorId')}: tipo inválido"))
    return findings


FAMILIAS_DE_TESE = (
    "competencia", "admissibilidade", "prejudiciais", "prescricao_decadencia",
    "nulidades", "merito_principal", "merito_subsidiario",
    "constitucional_prequestionamento", "consequencia_institucional",
)


# Nível probatório da fonte. A distinção não é acadêmica: ela decide o que o
# mapa pode afirmar. Descoberta não é prova — princípio herdado do TeiaJus.
NIVEL_PROBATORIO = {
    # decide: o próprio ato judicial, lido na íntegra
    "decisao_integra": "decide",
    "acordao_integra": "decide",
    "ato_oficial_tribunal": "decide",
    # corrobora: publicação oficial que noticia o ato, sem substituí-lo
    "ementa": "corrobora",
    "espelho_oficial": "corrobora",
    "diario_eletronico": "corrobora",
    # orienta: metadado e dado administrativo — dizem onde procurar
    "metadado_datajud": "orienta",
    "dado_administrativo": "orienta",
    "resultado_busca": "orienta",
}
FONTES_QUE_DECIDEM = {k for k, v in NIVEL_PROBATORIO.items() if v == "decide"}
FONTES_QUE_ORIENTAM = {k for k, v in NIVEL_PROBATORIO.items() if v == "orienta"}


def nivel_probatorio(kind: str | None) -> str:
    """Classifica uma fonte; o desconhecido nunca é promovido a prova."""
    return NIVEL_PROBATORIO.get(str(kind or "").strip().casefold(), "orienta")


def _fontes_do_mapa(payload: dict) -> dict[str, str]:
    """Índice sourceId → tipo declarado, a partir do bloco `sourceCatalog`."""
    catalogo = payload.get("sourceCatalog") or []
    return {
        str(item.get("sourceId")): str(item.get("kind") or "")
        for item in catalogo if isinstance(item, dict) and item.get("sourceId")
    }


def _idade_em_horas(momento: str | None, agora: datetime | None = None) -> float | None:
    if not momento:
        return None
    try:
        instante = datetime.fromisoformat(str(momento))
    except ValueError:
        return None
    referencia = agora or datetime.now(instante.tzinfo)
    return (referencia - instante).total_seconds() / 3600.0


def validate_recipient_map(
    payload: dict,
    *,
    freshness_hours: int | None = None,
    agora: datetime | None = None,
) -> list[dict]:
    """Mapa do destinatário — o que orienta a busca não prova a distribuição.

    Metadado de processo indica onde procurar. Prevenção e composição atual do
    órgão exigem fonte própria; sem ela, o estado honesto é `unknown`, que é
    aceito. O que não se aceita é `confirmed` sem lastro.
    """
    findings: list[dict] = []
    recipient = payload.get("recipient") or {}
    if recipient.get("identityStatus") == "confirmed" and not (recipient.get("sourceIds") or []):
        findings.append(issue(
            "FAL-F3-RECIPIENT-UNSOURCED",
            "identidade do destinatário declarada confirmada sem fonte",
        ))
    for campo, codigo in (("competence", "FAL-F3-COMPETENCE-UNSOURCED"),
                          ("prevention", "FAL-F3-PREVENTION-DATAJUD-ONLY")):
        bloco = payload.get(campo) or {}
        if bloco.get("status") == "confirmed" and not (bloco.get("sourceIds") or []):
            findings.append(issue(codigo, f"{campo} confirmada sem fonte que a sustente"))
    catalogo = _fontes_do_mapa(payload)

    def so_orienta(source_ids) -> bool:
        """Verdadeiro quando toda fonte listada apenas indica onde procurar."""
        ids = [str(v) for v in (source_ids or [])]
        if not ids:
            return False
        niveis = {
            nivel_probatorio(catalogo[i]) if i in catalogo
            else ("orienta" if "datajud" in i.casefold() else "decide")
            for i in ids
        }
        return niveis == {"orienta"}

    prevention = payload.get("prevention") or {}
    if prevention.get("status") == "confirmed" and so_orienta(prevention.get("sourceIds")):
        findings.append(issue(
            "FAL-F3-PREVENTION-DATAJUD-ONLY",
            "prevenção confirmada apenas por fonte que orienta a busca; metadado processual indica "
            "onde procurar e não decide distribuição",
        ))
    composition = payload.get("composition") or {}
    if composition.get("status") == "confirmed":
        if not (composition.get("sourceIds") or []):
            findings.append(issue(
                "FAL-F3-COMPOSITION-NO-OFFICIAL-SOURCE",
                "composição do órgão confirmada sem fonte oficial",
            ))
        elif so_orienta(composition.get("sourceIds")):
            findings.append(issue(
                "FAL-F3-COMPOSITION-NO-OFFICIAL-SOURCE",
                "composição confirmada apenas por metadado; exige ato ou publicação oficial do tribunal",
            ))
        if not composition.get("checkedAt"):
            findings.append(issue(
                "FAL-F3-COMPOSITION-STALE",
                "composição confirmada sem data de conferência; composição de órgão muda",
            ))
        elif freshness_hours is not None:
            # `status=confirmed` autodeclarado não sobrevive ao relógio: quem
            # decide se a composição ainda vale é a data, não o campo.
            idade = _idade_em_horas(composition.get("checkedAt"), agora)
            if idade is not None and idade > float(freshness_hours):
                findings.append(issue(
                    "FAL-F3-COMPOSITION-STALE",
                    f"composição conferida há {idade:.0f}h, acima do limite de {freshness_hours}h; "
                    "reconferir antes de usar",
                ))
    for position in payload.get("positions") or []:
        if not (position.get("decisionIds") or []):
            findings.append(issue(
                "FAL-F3-POSITION-NO-DECISION",
                f"{position.get('positionId')}: posição sem decisão identificada é impressão, não posição",
            ))
    niveis_amplos = {"section", "special_court", "plenary"}
    usa_amplo = any(
        (position.get("level") in niveis_amplos) for position in payload.get("positions") or []
    )
    if usa_amplo and not str(payload.get("topologyScopeReason") or "").strip():
        findings.append(issue(
            "FAL-F3-TOPOLOGY-UNJUSTIFIED",
            "topologia além do órgão julgador exige justificativa registrada",
        ))
    return findings


def validate_signature_brief(payload: dict) -> list[dict]:
    """Brief de assinatura — a rota escolhida precisa de decisão humana material."""
    findings: list[dict] = []
    if not str(payload.get("decisiveQuestion") or "").strip():
        findings.append(issue("FAL-F4-NO-DECISIVE-QUESTION", "brief sem pergunta jurisdicional"))
    routes = payload.get("routes") or []
    findings.extend(ids_unique(routes, "routeId", "FAL-F4-ROUTE-ID"))
    bloqueios = payload.get("blockingIssues") or []

    # Rotas que só diferem no texto não são alternativas: são a mesma rota
    # reescrita para simular deliberação.
    assinaturas: dict[tuple, str] = {}
    for route in routes:
        assinatura = (
            tuple(sorted(str(v) for v in route.get("thesisIds") or [])),
            tuple(sorted(str(v) for v in route.get("anchorCandidateIds") or [])),
            " ".join(str(route.get("bestObjection") or "").casefold().split()),
        )
        anterior = assinaturas.get(assinatura)
        if anterior:
            findings.append(issue(
                "FAL-F4-ROUTE-DUPLICATE",
                f"{route.get('routeId')} repete teses, âncoras e objeção de {anterior}",
            ))
        else:
            assinaturas[assinatura] = str(route.get("routeId"))

    if len(routes) == 1 and not str(payload.get("singleRouteReason") or "").strip():
        findings.append(issue("FAL-F4-ROUTE-ARTIFICIAL", "rota única exige motivo registrado"))
    if len(routes) > 4 and not str(payload.get("complexityReason") or "").strip():
        findings.append(issue("FAL-F4-ROUTE-ARTIFICIAL", "mais de quatro rotas exigem justificativa de complexidade"))

    selecionadas = [r for r in routes if r.get("decision") == "selected"]
    selected_id = str(payload.get("selectedRouteId") or "")
    if not bloqueios:
        if len(selecionadas) != 1:
            findings.append(issue(
                "FAL-F4-SELECTION-MISMATCH",
                f"esperada exatamente uma rota selecionada; encontradas {len(selecionadas)}",
            ))
        elif str(selecionadas[0].get("routeId")) != selected_id:
            findings.append(issue(
                "FAL-F4-SELECTION-MISMATCH",
                "selectedRouteId não coincide com a rota marcada como selecionada",
            ))
        if selecionadas and not str(payload.get("humanDecisionId") or "").strip():
            findings.append(issue(
                "FAL-F4-SELECTION-NO-HUMAN-DECISION",
                "rota material selecionada sem decisão humana registrada",
            ))
    elif selected_id:
        findings.append(issue(
            "FAL-F4-BLOCKED-RELEASE",
            "há pendência bloqueante; nenhuma rota pode ser dada por selecionada",
        ))

    cobertura = payload.get("thesisFamilyCoverage")
    if cobertura is not None:
        vistas = {str(item.get("family")) for item in cobertura}
        for familia in FAMILIAS_DE_TESE:
            if familia not in vistas:
                findings.append(issue(
                    "FAL-F4-FAMILY-MISSING",
                    f"família de tese não examinada: {familia}",
                ))
        for item in cobertura:
            if item.get("status") != "examinada_proposta" and not str(item.get("reason") or "").strip():
                findings.append(issue(
                    "FAL-F4-FAMILY-NO-REASON",
                    f"{item.get('family')}: descarte ou inaplicabilidade exige motivo",
                ))
    return findings


def _pool_de_ids(case_dir: Path, filename: str, chave: str, bloco: str) -> set[str] | None:
    """IDs declarados num artefato irmão; `None` quando o artefato não existe.

    A distinção importa: sem o artefato, não há como afirmar que a referência
    está pendurada — a ausência de pool não é prova de ID inexistente.
    """
    caminho = case_dir / "n4_artifacts" / filename
    if not caminho.is_file():
        return None
    try:
        payload = json.loads(caminho.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None
    if isinstance(payload, dict) and isinstance(payload.get("payload"), dict):
        payload = payload["payload"]
    itens = payload.get(bloco) or [] if isinstance(payload, dict) else []
    return {str(item.get(chave)) for item in itens if isinstance(item, dict) and item.get(chave)}


def validate_brief_references(brief: dict, case_dir: Path) -> list[dict]:
    """Cross-reference do brief contra os artefatos que o sustentam.

    Âncoras são caso à parte. Em F4 nenhuma âncora está verificada — a
    verificação é trabalho de F7. O que se exige aqui é que a candidata esteja
    declarada com identidade no próprio brief: é isso que permite, depois,
    confrontar a ficha de F7 com o que F4 prometeu, e é isso que impede a
    candidata de nascer final.
    """
    findings: list[dict] = []
    pools: dict[str, set[str] | None] = {
        "thesisIds": _pool_de_ids(case_dir, "F4_THESIS_MATURITY.json", "thesisId", "theses"),
        "decisiveFactIds": None,
        "decisiveDocumentIds": _pool_de_ids(
            case_dir, "F3_MAPA_DESTINATARIO.json", "sourceId", "sourceCatalog"),
    }
    perguntas = _pool_de_ids(case_dir, "F2_QUESTION_TREE.json", "questionId", "questions")
    nos = _pool_de_ids(case_dir, "F3_REASONING_GRAPH.json", "id", "nodes")
    if perguntas is not None or nos is not None:
        pools["decisiveFactIds"] = (perguntas or set()) | (nos or set())

    def conferir(campo: str, valores, origem: str) -> None:
        pool = pools.get(campo)
        if pool is None:
            return
        for valor in valores or []:
            if str(valor) not in pool:
                findings.append(issue(
                    "FAL-F4-REFERENCE-DANGLING",
                    f"{origem}: {campo} {valor!r} não existe no artefato de origem",
                ))

    conferir("decisiveFactIds", brief.get("decisiveFactIds"), "brief")
    conferir("decisiveDocumentIds", brief.get("decisiveDocumentIds"), "brief")

    candidatas = {
        str(item.get("anchorCandidateId"))
        for item in (brief.get("anchorCandidates") or [])
        if isinstance(item, dict) and item.get("anchorCandidateId")
    }
    for item in brief.get("anchorCandidates") or []:
        if isinstance(item, dict) and not str(item.get("identity") or "").strip():
            findings.append(issue(
                "FAL-F4-ANCHOR-DANGLING",
                f"{item.get('anchorCandidateId') or '?'}: candidata sem identificação do julgado",
            ))
    for route in brief.get("routes") or []:
        rid = str(route.get("routeId") or "?")
        conferir("thesisIds", route.get("thesisIds"), rid)
        for anchor in route.get("anchorCandidateIds") or []:
            if str(anchor) not in candidatas:
                findings.append(issue(
                    "FAL-F4-ANCHOR-DANGLING",
                    f"{rid}: âncora candidata {anchor!r} não declarada em `anchorCandidates`",
                ))
        if route.get("finalAnchorIds"):
            findings.append(issue(
                "FAL-F4-ANCHOR-DANGLING",
                f"{rid}: âncora dada por final em F4; verificação de íntegra é trabalho de F7",
            ))
    return findings


VALIDATORS = {
    "F2_QUESTION_TREE.json": validate_question_tree,
    "F4_COVERAGE_MATRIX.json": validate_coverage,
    "F3_REASONING_GRAPH.json": validate_graph,
    "F4_THESIS_MATURITY.json": validate_theses,
    "F3_CONDUCT_LEDGER.json": validate_conducts,
    "F4_DECISION_FACTOR_MAP.json": validate_decision_factors,
    "F3_MAPA_DESTINATARIO.json": validate_recipient_map,
    "F4_SIGNATURE_BRIEF.json": validate_signature_brief,
}


def validate_case(case_dir: Path) -> dict:
    findings = []
    payloads: dict[str, dict | None] = {}
    for filename, validator in VALIDATORS.items():
        payloads[filename], current = validate_file(case_dir, filename, validator)
        findings.extend(current)
    # Passe cruzado: um artefato pode estar íntegro sozinho e ainda apontar
    # para IDs que não existem em lugar nenhum. Reusa o payload já lido para
    # não duplicar os achados de envelope.
    brief = payloads.get("F4_SIGNATURE_BRIEF.json")
    if isinstance(brief, dict) and brief.get("applicability") != "not_applicable":
        findings.extend(validate_brief_references(brief, case_dir))
    return {"approved": not any(x["severity"] == "p0" for x in findings), "findings": findings}


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida raciocínio estrutural FORJA N4")
    parser.add_argument("case")
    args = parser.parse_args()
    print(json.dumps(validate_case(resolve_case_dir(args.case)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
