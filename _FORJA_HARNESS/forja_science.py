"""Interdisciplinary scientific-evidence gates for FORJA N4 (F5C/F7)."""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

from forja_n3_common import resolve_case_dir
from forja_n4_common import ids_unique, issue, validate_file


SCIENCE_MODES = {"not_applicable", "rapid", "strict"}
SYNTHESIS_STATES = {"convergent", "mixed", "weak", "absent", "not_transferable"}


def _get_json(base: str, params: dict, *, timeout: int = 30) -> dict:
    url = base + "?" + urllib.parse.urlencode({key: value for key, value in params.items() if value is not None})
    request = urllib.request.Request(url, headers={"User-Agent": "FORJA-N4/1.0 academic-evidence"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def crossref_search(query: str, *, rows: int = 10) -> dict:
    try:
        payload = _get_json("https://api.crossref.org/works", {"query.bibliographic": query, "rows": rows})
        return {"status": "ok", "source": "crossref", "items": (payload.get("message") or {}).get("items") or []}
    except Exception as exc:
        return {"status": "unavailable", "source": "crossref", "error": str(exc)[:500], "items": []}


def crossref_by_doi(doi: str) -> dict:
    normalized = normalize_doi(doi)
    if not normalized:
        return {"status": "invalid", "source": "crossref", "item": None}
    try:
        request = urllib.request.Request("https://api.crossref.org/works/" + urllib.parse.quote(normalized, safe=""), headers={"User-Agent": "FORJA-N4/1.0 academic-evidence"})
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return {"status": "ok", "source": "crossref", "item": payload.get("message")}
    except Exception as exc:
        return {"status": "unavailable", "source": "crossref", "error": str(exc)[:500], "item": None}


def pubmed_search(query: str, *, rows: int = 10) -> dict:
    try:
        search = _get_json("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi", {"db": "pubmed", "term": query, "retmax": rows, "retmode": "json", "tool": "FORJA-N4"})
        ids = ((search.get("esearchresult") or {}).get("idlist") or [])
        if not ids:
            return {"status": "ok", "source": "pubmed", "items": []}
        summary = _get_json("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi", {"db": "pubmed", "id": ",".join(ids), "retmode": "json", "version": "2.0", "tool": "FORJA-N4"})
        result = summary.get("result") or {}
        return {"status": "ok", "source": "pubmed", "items": [result[item] for item in ids if isinstance(result.get(item), dict)]}
    except Exception as exc:
        return {"status": "unavailable", "source": "pubmed", "error": str(exc)[:500], "items": []}


def ncbi_fetch(identifier: str, *, database: str = "pmc") -> dict:
    try:
        params = urllib.parse.urlencode({"db": database, "id": identifier, "retmode": "xml", "tool": "FORJA-N4"})
        request = urllib.request.Request(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + params,
            headers={"User-Agent": "FORJA-N4/1.0 academic-evidence"},
        )
        with urllib.request.urlopen(request, timeout=45) as response:
            text = response.read().decode("utf-8", errors="replace")
        return {"status": "ok", "source": "ncbi_efetch", "database": database, "identifier": identifier, "text": text}
    except Exception as exc:
        return {"status": "unavailable", "source": "ncbi_efetch", "database": database, "identifier": identifier, "error": str(exc)[:500], "text": ""}


def openalex_search(query: str, *, rows: int = 10, api_key: str | None = None) -> dict:
    key = api_key or os.environ.get("OPENALEX_API_KEY")
    if not key:
        return {"status": "unavailable", "source": "openalex", "reason": "api_key_not_configured", "items": []}
    try:
        payload = _get_json("https://api.openalex.org/works", {"search": query, "per-page": rows, "api_key": key})
        return {"status": "ok", "source": "openalex", "items": payload.get("results") or []}
    except Exception as exc:
        return {"status": "unavailable", "source": "openalex", "error": str(exc)[:500], "items": []}


def discover(query: str, *, rows: int = 10) -> dict:
    """Run independent discovery routes; an unavailable route is degradation, not absence."""
    routes = [crossref_search(query, rows=rows), pubmed_search(query, rows=rows), openalex_search(query, rows=rows)]
    return {"query": query, "routes": routes, "found": sum(len(route.get("items") or []) for route in routes)}


def normalize_doi(value: object) -> str | None:
    text = str(value or "").strip().lower()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text)
    return text or None


def _bibliographic_text(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").casefold()).strip()


def validate_classification(payload: dict) -> list[dict]:
    science = payload.get("science") or {}
    findings = []
    if science.get("mode") not in SCIENCE_MODES:
        findings.append(issue("N4-SCI-MODE", "modo LCI inválido"))
    if science.get("mode") != "not_applicable":
        if not science.get("triggerPropositionIds") or not science.get("domains") or not science.get("justification"):
            findings.append(issue("N4-SCI-TRIGGER", "LCI aplicável sem proposição, domínio ou justificativa"))
    elif not science.get("justification"):
        findings.append(issue("N4-SCI-NA", "LCI não aplicável sem justificativa"))
    return findings


def validate_protocol(payload: dict) -> list[dict]:
    findings = []
    for key in ("researchQuestion", "databases", "queries", "inclusionCriteria", "exclusionCriteria", "stopRule", "searchDate"):
        if not payload.get(key):
            findings.append(issue("N4-SCI-PROTOCOL", f"protocolo sem {key}"))
    mode = payload.get("mode")
    if mode == "strict" and len(payload.get("databases") or []) < 2:
        findings.append(issue("N4-SCI-STRICT-BASES", "modo strict exige ao menos duas bases/rotas"))
    return findings


def validate_studies(payload: dict) -> list[dict]:
    studies = payload.get("studies") or []
    findings = ids_unique(studies, "studyId", "N4-SCI-ID")
    identifiers: dict[tuple[str, str], str] = {}
    for study in studies:
        sid = str(study.get("studyId") or "?")
        ids = study.get("identifiers") or {}
        doi = normalize_doi(ids.get("doi"))
        for kind, value in (("doi", doi), ("pmid", ids.get("pmid")), ("openalex", ids.get("openalex"))):
            if value:
                key = (kind, str(value).casefold())
                if key in identifiers and identifiers[key] != sid:
                    findings.append(issue("N4-SCI-DUPLICATE", f"{sid} duplica identificador de {identifiers[key]}"))
                identifiers[key] = sid
        verification = study.get("verification") or {}
        identity_check = study.get("identityCheck") or {}
        if identity_check:
            queried_title = _bibliographic_text(identity_check.get("queriedTitle"))
            returned_title = _bibliographic_text(identity_check.get("returnedTitle"))
            if queried_title and returned_title and queried_title != returned_title:
                findings.append(issue("N4-SCI-TITLE-MISMATCH", f"{sid}: DOI/identificador resolveu para outro título"))
            queried_authors = {_bibliographic_text(value) for value in identity_check.get("queriedAuthors") or []}
            returned_authors = {_bibliographic_text(value) for value in identity_check.get("returnedAuthors") or []}
            author_match = any(
                queried == returned or queried in returned or returned in queried
                for queried in queried_authors for returned in returned_authors
            )
            if queried_authors and returned_authors and not author_match:
                findings.append(issue("N4-SCI-AUTHOR-MISMATCH", f"{sid}: autoria retornada não corresponde à pesquisada"))
        if verification.get("identity") != "confirmed":
            findings.append(issue("N4-SCI-IDENTITY", f"{sid}: identidade bibliográfica não confirmada"))
        if verification.get("content") != "confirmed" and study.get("supportsClaimIds"):
            findings.append(issue("N4-SCI-CONTENT", f"{sid}: metadado/resumo não sustenta claim substantivo"))
        if verification.get("correctionRetraction") != "checked":
            findings.append(issue("N4-SCI-EDITORIAL", f"{sid}: correção/retratação não consultada"))
        if study.get("publicationStatus") in {"retracted", "expression_of_concern"} and study.get("supportsClaimIds"):
            findings.append(issue("N4-SCI-RETRACTED", f"{sid}: fonte editorialmente comprometida usada como apoio"))
        if study.get("version") == "preprint" and study.get("peerReviewStatus") == "confirmed":
            findings.append(issue("N4-SCI-PREPRINT", f"{sid}: preprint tratado como versão revisada por pares"))
        if not study.get("limitations"):
            findings.append(issue("N4-SCI-LIMITS", f"{sid}: limitações não registradas", severity="p1"))
    return findings


def validate_claims(payload: dict, study_ledger: dict | None = None) -> list[dict]:
    claims = payload.get("claims") or []
    findings = ids_unique(claims, "scienceClaimId", "N4-SCI-CLAIM-ID")
    studies = {item.get("studyId"): item for item in (study_ledger or {}).get("studies") or []}
    for claim in claims:
        cid = str(claim.get("scienceClaimId") or "?")
        if claim.get("synthesisStatus") not in SYNTHESIS_STATES:
            findings.append(issue("N4-SCI-SYNTHESIS", f"{cid}: síntese inválida"))
        support_ids = claim.get("supportingStudyIds") or []
        contrary_ids = claim.get("contraryStudyIds") or []
        for sid in support_ids + contrary_ids:
            if study_ledger is not None and sid not in studies:
                findings.append(issue("N4-SCI-DANGLING", f"{cid}: estudo inexistente {sid}"))
        text = str(claim.get("draftText") or "")
        causal = bool(re.search(r"\b(causa|provoca|determina|leva necessariamente|causes?|determines?)\b", text, re.I))
        if causal and claim.get("causalLanguageAllowed") is not True:
            findings.append(issue("N4-SCI-CAUSAL", f"{cid}: linguagem causal não autorizada"))
        individual = bool(re.search(r"\b(diagn[oó]stico|comprova que (?:o|a) paciente|prova individual)\b", text, re.I))
        if individual and claim.get("useType") == "contextual_support":
            findings.append(issue("N4-SCI-INDIVIDUAL", f"{cid}: evidência populacional usada como prova individual"))
        if claim.get("finalUseAllowed") is True and not support_ids:
            findings.append(issue("N4-SCI-NO-SUPPORT", f"{cid}: uso final sem estudo de apoio"))
        if not claim.get("transferLimits"):
            findings.append(issue("N4-SCI-TRANSFER", f"{cid}: limites de transferência ausentes"))
    return findings


def validate_synthesis(payload: dict) -> list[dict]:
    findings = []
    if payload.get("synthesisStatus") not in SYNTHESIS_STATES:
        findings.append(issue("N4-SCI-SYNTHESIS-STATUS", "estado de síntese inválido"))
    search = payload.get("contraryEvidenceSearch") or {}
    if search.get("performed") is not True or not search.get("queries"):
        findings.append(issue("N4-SCI-CONTRARY", "síntese sem busca registrada de evidência contrária"))
    if not payload.get("limitations"):
        findings.append(issue("N4-SCI-SYNTHESIS-LIMITS", "síntese sem limitações"))
    return findings


def validate_audit(payload: dict) -> list[dict]:
    if payload.get("applicability") == "not_applicable":
        return [] if payload.get("justification") else [issue("N4-SCI-AUDIT-NA", "auditoria não aplicável sem justificativa")]
    findings = []
    for item in payload.get("findings") or []:
        if item.get("severity") == "p0" and item.get("status") != "resolved":
            findings.append(issue("N4-SCI-AUDIT-P0", str(item.get("detail") or item.get("code") or "P0 científico")))
    if payload.get("approved") is not True:
        findings.append(issue("N4-SCI-AUDIT-STATUS", "auditoria científica não aprovada"))
    return findings


def validate_case(case_dir: Path) -> dict:
    findings = []
    classification, current = validate_file(case_dir, "F2_N4_CLASSIFICATION.json", validate_classification)
    findings += current
    mode = ((classification or {}).get("science") or {}).get("mode")
    if mode == "not_applicable":
        _, current = validate_file(case_dir, "F7_SCIENCE_AUDIT.json", validate_audit)
        findings += current
        return {"approved": not any(x["severity"] == "p0" for x in findings), "mode": mode, "findings": findings}
    protocol, current = validate_file(case_dir, "F5C_RESEARCH_PROTOCOL.json", validate_protocol)
    findings += current
    studies, current = validate_file(case_dir, "F5C_STUDY_LEDGER.json", validate_studies)
    findings += current
    _, current = validate_file(case_dir, "F5C_EVIDENCE_SYNTHESIS.json", validate_synthesis)
    findings += current
    _, current = validate_file(case_dir, "F5C_CLAIM_EVIDENCE_MAP.json", lambda value: validate_claims(value, studies))
    findings += current
    _, current = validate_file(case_dir, "F7_SCIENCE_AUDIT.json", validate_audit)
    findings += current
    return {"approved": not any(x["severity"] == "p0" for x in findings), "mode": mode, "findings": findings}


def main() -> None:
    parser = argparse.ArgumentParser(description="Pesquisa e valida Lastro Científico Interdisciplinar FORJA N4")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("case")
    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--rows", type=int, default=10)
    args = parser.parse_args()
    result = validate_case(resolve_case_dir(args.case)) if args.command == "validate" else discover(args.query, rows=args.rows)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
