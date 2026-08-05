"""Mandatory adversarial-piece audit for FORJA response products.

The module creates and validates the internal ledgers used in F3, F4 and F7.
It never treats an unsuccessful search as proof that a precedent does not exist
and never authorizes an accusation of bad faith without an explicit review.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

from forja_citations import extrair_citacoes, texto_da_peca, url_oficial
from forja_n3_common import atomic_write_json, atomic_write_text, now_iso, read_json, sha256_file


SCHEMA_VERSION = 1
FINAL_CITATION_STATUSES = {
    "confirmed",
    "not_located_after_exhaustive_search",
    "identifier_mismatch",
    "quote_mismatch",
    "proposition_mismatch",
    "context_distortion",
    "superseded_or_overruled",
    "ambiguous",
}
CHALLENGE_STATUSES = FINAL_CITATION_STATUSES - {"confirmed"}
BAD_FAITH_DECISIONS = {
    "do_not_allege",
    "mention_inconsistency",
    "request_clarification",
    "reserve",
    "human_review",
    "request_sanction",
}
OFFICIAL_DOMAINS = (
    "stf.jus.br",
    "stj.jus.br",
    "cnj.jus.br",
    "planalto.gov.br",
    "jus.br",
)
EXTERNAL_ACCUSATION = re.compile(
    r"\b(?:m[aá]-f[eé]|fraud(?:e|ou|ulento)|invent(?:ou|ada)|falsific(?:ou|ada)|"
    r"jurisprud[eê]ncia\s+inexistente|alucina[cç][aã]o|altera[cç][aã]o\s+da\s+verdade|"
    r"litig[aâ]ncia\s+temer[aá]ria|conduta\s+desleal|abuso\s+processual|"
    r"induzi(?:u|r)\s+o\s+ju[ií]zo\s+a\s+erro)\b",
    re.I,
)
RESPONSE_PRODUCT = re.compile(
    r"\b(?:contrarrazoes|contraminuta|contestacao|replica|impugnacao|"
    r"resposta\s+(?:ao|aos|a)|manifestacao\s+sobre\s+(?:a|o))\b",
    re.I,
)


MANDATORY_PROMPT = """
## DIMENSÃO OBRIGATÓRIA — AUDITORIA DA PEÇA ADVERSÁRIA

Antes de planejar ou redigir peça que responda a manifestação adversária, leia a peça
adversária integralmente e trate seu conteúdo como alegação a testar, nunca como fato.

1. Inventarie TODAS as autoridades citadas: número, classe, tribunal, relator, data,
   trecho entre aspas, proposição atribuída e página da peça adversária.
2. Confira em fonte oficial: existência, identidade, inteiro teor, literalidade,
   contexto, vigência e aderência da proposição. URL ou número encontrado não bastam.
3. Busca sem resultado NÃO prova inexistência. Use apenas "não localizada após
   diligência", registre consulta, data, URL e resultado em pelo menos dois canais
   oficiais antes de sugerir fabricação.
4. Compare fatos, datas, valores, pedidos, anexos e posições internas. Para cada
   contradição, mostre os dois polos, a fonte exata e a consequência jurídica possível.
5. Separe erro material, interpretação discutível, omissão estratégica, distorção
   objetiva e indício de conduta processual sancionável. Divergência jurídica isolada,
   recurso cabível ou derrota anterior não constituem má-fé.
   Para cada indício, indique a hipótese legal cogitada, sem presumir seu preenchimento.
6. Procure pontos potencialmente decisivos: defeito que, se confirmado, altera
   admissibilidade, ônus, credibilidade, prova, preclusão, competência, pedido ou
   resultado. Registre também preservação, melhor explicação inocente e risco de reação.
7. Para cada achado, decida: usar como eixo central, usar subsidiariamente, pedir
   esclarecimento/prova, reservar, descartar ou submeter a revisão humana.
8. Linguagem externa acusatória ou pedido de sanção exige lastro objetivo, base legal,
   materialidade, hipótese rival examinada e autorização expressa de Cícero/revisor.
9. Execute Red Team final: tente provar que o precedente existe, que a citação é apenas
   imprecisa e que a contradição é explicável. Se essa hipótese sobreviver, rebaixe o achado.

Saídas internas obrigatórias: `adversarial_audit`, `adversarial_strategy` e
`adversarial_recheck`. Nenhum rótulo interno aparece na peça protocolável.
""".strip()


def mandatory_prompt_for_phase(phase: str) -> str:
    if str(phase).startswith(("F3_", "F4_", "F7_")):
        return MANDATORY_PROMPT + "\n\n"
    return ""


def response_product_required(text: str) -> bool:
    folded = unicodedata.normalize("NFKD", str(text or ""))
    folded = "".join(char for char in folded if not unicodedata.combining(char))
    return bool(RESPONSE_PRODUCT.search(folded))


def _official_url(value: object) -> bool:
    try:
        host = (urlparse(str(value or "")).hostname or "").lower()
    except ValueError:
        return False
    return any(host == domain or host.endswith("." + domain) for domain in OFFICIAL_DOMAINS)


def _citation_id(index: int) -> str:
    return f"CIT-ADV-{index:03d}"


def initialize_audit(source: Path, *, applicable: bool = True, reason: str = "") -> dict:
    source = source.resolve()
    text = texto_da_peca(source) if source.is_file() else ""
    citations = extrair_citacoes(text) if applicable else []
    inventory = []
    for index, citation in enumerate(citations, 1):
        inventory.append({
            "id": _citation_id(index),
            "label": citation["rotulo"],
            "type": citation["tipo"],
            "contextInAdversarialPiece": citation["contexto"],
            "occurrences": citation["ocorrencias"],
            "pageOrParagraph": None,
            "propositionClaimed": None,
            "quotedText": None,
            "officialSearchUrl": url_oficial(citation["tipo"], citation["dados"]),
            "verificationStatus": "pending",
            "officialSourceUrl": None,
            "officialHolding": None,
            "identityMatch": "pending",
            "quoteMatch": "pending",
            "contextMatch": "pending",
            "currentStatus": "pending",
            "recommendedTreatment": "pending",
            "notes": "",
        })
    return {
        "schemaVersion": SCHEMA_VERSION,
        "kind": "forja_adversarial_audit",
        "generatedAt": now_iso(),
        "applicable": applicable,
        "notApplicableReason": reason if not applicable else "",
        "sourceDocument": {
            "path": str(source),
            "sha256": sha256_file(source) if source.is_file() else None,
        },
        "scope": {
            "fullReadingConfirmed": False if applicable else True,
            "pagesOrSectionsCovered": [],
            "adversarialRequestsMapped": False if applicable else True,
        },
        "citationInventory": inventory,
        "researchLog": [],
        "factualClaims": [],
        "contradictions": [],
        "badFaithIndicators": [],
        "decisivePoints": [],
        "conclusion": {
            "citationAuditComplete": False if applicable else True,
            "contradictionAuditComplete": False if applicable else True,
            "redTeamCompleted": False if applicable else True,
            "badFaithAssessment": "not_supported",
            "summary": reason if not applicable else "",
        },
        "humanReview": {
            "required": False,
            "approved": False,
            "reviewer": None,
            "reviewedAt": None,
            "authorizedIndicatorIds": [],
        },
    }


def _validate_source(payload: dict, source_path: Path | None, p0: list[str]) -> None:
    recorded = payload.get("sourceDocument") or {}
    path = source_path or Path(str(recorded.get("path") or ""))
    if not path.is_file():
        p0.append("peça adversária de origem não localizada")
        return
    if recorded.get("sha256") != sha256_file(path):
        p0.append("ledger foi produzido sobre versão diferente da peça adversária")


def _validate_inventory_completeness(payload: dict, source_path: Path | None, p0: list[str]) -> None:
    recorded = payload.get("sourceDocument") or {}
    path = source_path or Path(str(recorded.get("path") or ""))
    if not path.is_file():
        return
    expected = {item["rotulo"] for item in extrair_citacoes(texto_da_peca(path))}
    inventoried = {str(item.get("label") or "") for item in payload.get("citationInventory") or []}
    missing = sorted(expected - inventoried)
    if missing:
        p0.append("autoridades detectadas fora do inventário: " + ", ".join(missing))


def validate_adversarial_audit(payload: dict, *, source_path: Path | None = None) -> dict:
    p0: list[str] = []
    p1: list[str] = []
    if not isinstance(payload, dict) or payload.get("kind") != "forja_adversarial_audit":
        return {"approved": False, "p0": ["ledger adversarial ausente ou com tipo inválido"], "p1": []}
    if payload.get("schemaVersion") != SCHEMA_VERSION:
        p0.append("schema adversarial incompatível")
    applicable = payload.get("applicable") is True
    if not applicable:
        if len(str(payload.get("notApplicableReason") or "").strip()) < 20:
            p0.append("não aplicabilidade sem justificativa concreta")
        return {"approved": not p0, "p0": p0, "p1": p1, "applicable": False}

    _validate_source(payload, source_path, p0)
    _validate_inventory_completeness(payload, source_path, p0)
    scope = payload.get("scope") or {}
    if scope.get("fullReadingConfirmed") is not True:
        p0.append("leitura integral da peça adversária não confirmada")
    if not scope.get("pagesOrSectionsCovered"):
        p0.append("cobertura da peça adversária não registrada")
    if scope.get("adversarialRequestsMapped") is not True:
        p0.append("pedidos adversários não foram mapeados")

    citation_ids = set()
    logs = payload.get("researchLog") or []
    for citation in payload.get("citationInventory") or []:
        citation_id = str(citation.get("id") or "")
        if not citation_id or citation_id in citation_ids:
            p0.append("citação adversária sem ID único")
            continue
        citation_ids.add(citation_id)
        status = str(citation.get("verificationStatus") or "")
        if status not in FINAL_CITATION_STATUSES:
            p0.append(f"{citation_id}: verificação jurisprudencial pendente")
            continue
        if not citation.get("pageOrParagraph") or not citation.get("propositionClaimed"):
            p0.append(f"{citation_id}: localização ou proposição atribuída ausente")
        verification_fields = ("identityMatch", "quoteMatch", "contextMatch", "currentStatus")
        if any(citation.get(field) in {None, "", "pending"} for field in verification_fields):
            p0.append(f"{citation_id}: dimensões de identidade, aspas, contexto ou vigência pendentes")
        if status == "confirmed" and not _official_url(citation.get("officialSourceUrl")):
            p0.append(f"{citation_id}: confirmação sem fonte oficial")
        if status == "confirmed" and not (
            citation.get("identityMatch") == "match"
            and citation.get("quoteMatch") in {"match", "not_applicable"}
            and citation.get("contextMatch") in {"match", "not_applicable"}
            and citation.get("currentStatus") in {"current", "not_applicable"}
        ):
            p0.append(f"{citation_id}: confirmação incompatível com identidade, aspas, contexto ou vigência")
        if status in CHALLENGE_STATUSES:
            related = [entry for entry in logs if entry.get("citationId") == citation_id]
            official_hosts = {
                (urlparse(str(entry.get("url") or "")).hostname or "").lower()
                for entry in related if _official_url(entry.get("url")) and entry.get("query") and entry.get("checkedAt")
            }
            if status == "not_located_after_exhaustive_search" and len(official_hosts) < 2:
                p0.append(f"{citation_id}: não localização exige dois canais oficiais documentados")
            if status != "not_located_after_exhaustive_search" and not (
                _official_url(citation.get("officialSourceUrl")) or official_hosts
            ):
                p0.append(f"{citation_id}: divergência sem lastro oficial")
        if status != "confirmed" and citation.get("recommendedTreatment") in {None, "", "pending"}:
            p1.append(f"{citation_id}: tratamento processual ainda não decidido")

    finding_ids = citation_ids.copy()
    for group_name in ("factualClaims", "contradictions", "badFaithIndicators"):
        for entry in payload.get(group_name) or []:
            entry_id = str(entry.get("id") or "")
            if not entry_id or entry_id in finding_ids:
                p0.append(f"{group_name}: achado sem ID único")
            else:
                finding_ids.add(entry_id)

    review = payload.get("humanReview") or {}
    authorized = set(review.get("authorizedIndicatorIds") or [])
    for indicator in payload.get("badFaithIndicators") or []:
        indicator_id = str(indicator.get("id") or "")
        if not indicator.get("conduct") or not indicator.get("materiality"):
            p0.append(f"{indicator_id}: indício sem conduta objetiva ou materialidade")
        if not indicator.get("legalHypothesis"):
            p0.append(f"{indicator_id}: indício sem hipótese jurídica expressa")
        if not indicator.get("recordReferences") or not indicator.get("counterHypothesis"):
            p0.append(f"{indicator_id}: indício sem fonte ou hipótese inocente rival")
        external = str(indicator.get("externalLanguage") or "")
        alleges = bool(EXTERNAL_ACCUSATION.search(external))
        authorized_here = (
            indicator.get("status") == "human_authorized_allegation"
            and indicator_id in authorized
            and review.get("approved") is True
            and review.get("reviewer")
            and review.get("reviewedAt")
            and indicator.get("legalBasis")
        )
        if alleges and not authorized_here:
            p0.append(f"{indicator_id}: linguagem acusatória sem autorização jurídica expressa")

    decisive_ids = set()
    for point in payload.get("decisivePoints") or []:
        point_id = str(point.get("id") or "")
        decisive_ids.add(point_id)
        refs = set(point.get("findingRefs") or [])
        if not point_id or not refs or not refs.issubset(finding_ids):
            p0.append(f"{point_id or 'ponto decisivo'}: referências ausentes ou inválidas")
        for field in (
            "decisiveWhy",
            "proceduralConsequence",
            "recommendedAction",
            "preservationCheck",
            "bestInnocentExplanation",
            "backfireRisk",
        ):
            if not str(point.get(field) or "").strip():
                p0.append(f"{point_id}: campo decisivo ausente: {field}")
        if point.get("status") == "actionable" and point.get("confidence") not in {"high", "medium"}:
            p0.append(f"{point_id}: ação decisiva sem confiança calibrada")

    conclusion = payload.get("conclusion") or {}
    for field in ("citationAuditComplete", "contradictionAuditComplete", "redTeamCompleted"):
        if conclusion.get(field) is not True:
            p0.append(f"conclusão adversarial incompleta: {field}")
    if conclusion.get("badFaithAssessment") not in {"not_supported", "indicator_only", "human_authorized"}:
        p0.append("classificação de má-fé inválida")
    if conclusion.get("badFaithAssessment") == "indicator_only" and not payload.get("badFaithIndicators"):
        p0.append("conclusão registra indício de má-fé sem achado correspondente")
    if conclusion.get("badFaithAssessment") == "human_authorized" and not (
        review.get("approved") is True and authorized
    ):
        p0.append("conclusão de má-fé autorizada sem aprovação humana vinculada")
    return {
        "approved": not p0,
        "p0": sorted(set(p0)),
        "p1": sorted(set(p1)),
        "applicable": True,
        "citations": len(citation_ids),
        "decisivePoints": len(decisive_ids),
    }


def validate_adversarial_strategy(payload: dict, audit_path: Path) -> dict:
    p0: list[str] = []
    audit = read_json(audit_path, None)
    audit_result = validate_adversarial_audit(audit or {})
    if not audit_result["approved"]:
        p0.append("estratégia usa auditoria adversarial não aprovada")
    if payload.get("kind") != "forja_adversarial_strategy":
        p0.append("matriz estratégica adversarial inválida")
    if payload.get("auditSha256") != sha256_file(audit_path):
        p0.append("matriz estratégica usa auditoria diferente")
    applicable = bool((audit or {}).get("applicable"))
    if payload.get("applicable") is not applicable:
        p0.append("aplicabilidade diverge entre auditoria e estratégia")
    if applicable:
        expected = {
            str(item.get("id")) for item in (audit or {}).get("citationInventory") or []
            if item.get("verificationStatus") in CHALLENGE_STATUSES
        }
        for group_name in ("contradictions", "badFaithIndicators", "decisivePoints"):
            expected.update(str(item.get("id")) for item in (audit or {}).get(group_name) or [])
        expected.discard("")
        decisions = payload.get("decisions") or []
        decided = {str(item.get("findingId") or item.get("decisivePointId") or "") for item in decisions}
        decided.discard("")
        if expected != decided:
            p0.append("nem todos os achados adversariais receberam decisão estratégica")
        for item in decisions:
            finding_id = item.get("findingId") or item.get("decisivePointId")
            if item.get("decision") not in {
                "central", "subsidiary", "request_evidence", "reserve", "discard", "human_review"
            }:
                p0.append(f"decisão estratégica inválida: {finding_id}")
            if not item.get("rationale") or not item.get("backfireControl"):
                p0.append(f"decisão sem fundamento ou controle de reação: {finding_id}")
        for reviewer in ("helenaReview", "ciceroReview"):
            review = payload.get(reviewer) or {}
            if review.get("present") is not True or not review.get("recommendations"):
                p0.append(f"{reviewer} ausente na estratégia adversarial")
        bad_faith = payload.get("badFaithDecision") or {}
        mode = bad_faith.get("mode")
        if mode not in BAD_FAITH_DECISIONS:
            p0.append("decisão de má-fé ausente ou inválida")
        elif mode != "do_not_allege" and not bad_faith.get("rationale"):
            p0.append("decisão de má-fé sem fundamento registrado")
        if mode == "request_sanction":
            authorized = (
                bad_faith.get("humanAuthorized") is True
                and bad_faith.get("reviewer")
                and bad_faith.get("reviewedAt")
                and (payload.get("ciceroReview") or {}).get("approved") is True
            )
            complete_request = all(bad_faith.get(field) for field in (
                "legalBasis", "evidenceRefs", "proportionality", "requestedRelief"
            ))
            if not authorized or not complete_request:
                p0.append("pedido de sanção sem autorização, lastro ou proporcionalidade completos")
    return {"approved": not p0, "p0": sorted(set(p0)), "applicable": applicable}


def validate_adversarial_recheck(payload: dict, audit_path: Path, strategy_path: Path) -> dict:
    p0: list[str] = []
    audit = read_json(audit_path, None) or {}
    strategy = read_json(strategy_path, None) or {}
    if payload.get("kind") != "forja_adversarial_recheck":
        p0.append("red team adversarial inválido")
    if payload.get("auditSha256") != sha256_file(audit_path):
        p0.append("red team usa auditoria diferente")
    if payload.get("strategySha256") != sha256_file(strategy_path):
        p0.append("red team usa estratégia diferente")
    if payload.get("applicable") is not bool(audit.get("applicable")):
        p0.append("aplicabilidade diverge no red team")
    if audit.get("applicable"):
        all_finding_ids = {
            str(item.get("id")) for item in audit.get("citationInventory") or []
        }
        for group_name in ("contradictions", "badFaithIndicators", "decisivePoints"):
            all_finding_ids.update(str(item.get("id")) for item in audit.get(group_name) or [])
        all_finding_ids.discard("")
        challenge_ids = {
            str(item.get("id")) for item in audit.get("citationInventory") or []
            if item.get("verificationStatus") in CHALLENGE_STATUSES
        }
        if not challenge_ids.issubset(set(payload.get("citationsRechecked") or [])):
            p0.append("citações adversárias contestadas não foram rechecadas em F7")
        other_findings = set()
        for group_name in ("contradictions", "badFaithIndicators", "decisivePoints"):
            other_findings.update(str(item.get("id")) for item in audit.get(group_name) or [])
        other_findings.discard("")
        if not other_findings.issubset(set(payload.get("findingsRechecked") or [])):
            p0.append("contradições, indícios ou pontos decisivos não foram rechecados em F7")
        if (payload.get("falsePositiveReview") or {}).get("completed") is not True:
            p0.append("revisão de falsos positivos não concluída")
        if (payload.get("bestInnocentExplanation") or {}).get("tested") is not True:
            p0.append("melhor explicação inocente não foi testada")
        for allegation in payload.get("externalAllegations") or []:
            finding_id = str(allegation.get("findingId") or "")
            complete = (
                finding_id in all_finding_ids
                and allegation.get("authorized") is True
                and allegation.get("reviewer")
                and allegation.get("reviewedAt")
                and allegation.get("legalBasis")
                and allegation.get("evidenceRefs")
                and allegation.get("wording")
            )
            if not complete:
                p0.append("alegação externa sem achado, autorização, lastro ou redação final no red team")
    if payload.get("approved") is not True or int(payload.get("p0") or 0):
        p0.append("red team adversarial não aprovado")
    return {"approved": not p0, "p0": sorted(set(p0)), "applicable": bool(audit.get("applicable"))}


def validate_phase_artifacts(phase: str, artifacts: dict[str, Path], inputs: dict[str, dict]) -> list[str]:
    def input_path(name: str) -> Path | None:
        value = inputs.get(name) or {}
        path = value.get("path")
        return Path(path) if path else None

    if phase.startswith("F3_"):
        path = artifacts.get("adversarial_audit")
        result = validate_adversarial_audit(read_json(path, None) or {}) if path else {"p0": ["auditoria adversarial ausente"]}
        return list(result.get("p0") or [])
    if phase.startswith("F4_"):
        path = artifacts.get("adversarial_strategy")
        audit_path = input_path("adversarial_audit")
        if not path or not audit_path or not audit_path.is_file():
            return ["matriz ou auditoria adversarial ausente em F4"]
        return list(validate_adversarial_strategy(read_json(path, None) or {}, audit_path).get("p0") or [])
    if phase.startswith("F7_"):
        path = artifacts.get("adversarial_recheck")
        audit_path = input_path("adversarial_audit")
        strategy_path = input_path("adversarial_strategy")
        if not path or not audit_path or not strategy_path or not audit_path.is_file() or not strategy_path.is_file():
            return ["artefatos adversariais ausentes em F7"]
        return list(validate_adversarial_recheck(read_json(path, None) or {}, audit_path, strategy_path).get("p0") or [])
    return []


def main() -> None:
    parser = argparse.ArgumentParser(description="Auditoria obrigatória de peça adversária da FORJA")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("source", type=Path)
    init.add_argument("output", type=Path)
    na = sub.add_parser("not-applicable")
    na.add_argument("output", type=Path)
    na.add_argument("--reason", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("ledger", type=Path)
    validate.add_argument("--source", type=Path)
    validate.add_argument("--output", type=Path)
    prompt = sub.add_parser("prompt")
    prompt.add_argument("phase")
    args = parser.parse_args()
    if args.command == "init":
        payload = initialize_audit(args.source, applicable=True)
        atomic_write_json(args.output, payload)
        atomic_write_text(args.output.with_suffix(".prompt.md"), MANDATORY_PROMPT + "\n")
        result = {"ok": True, "ledger": str(args.output), "citations": len(payload["citationInventory"])}
    elif args.command == "not-applicable":
        payload = initialize_audit(Path("."), applicable=False, reason=args.reason)
        atomic_write_json(args.output, payload)
        result = {"ok": True, "ledger": str(args.output), "applicable": False}
    elif args.command == "validate":
        payload = read_json(args.ledger, None) or {}
        result = validate_adversarial_audit(payload, source_path=args.source)
        if args.output:
            atomic_write_json(args.output, {"generatedAt": now_iso(), **result})
    else:
        print(mandatory_prompt_for_phase(args.phase), end="")
        return
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.command == "validate" and not result.get("approved"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
