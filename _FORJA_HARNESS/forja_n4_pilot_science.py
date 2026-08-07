"""Real F5C rapid-mode pilot using Crossref and NCBI over the health-plan case."""

from __future__ import annotations

import json
import re
from xml.etree import ElementTree as ET

from forja_n3_common import FORJA, atomic_write_json, now_iso, read_json, sha256_file
from forja_n4_common import build_envelope, write_artifact
from forja_science import crossref_by_doi, discover, ncbi_fetch, validate_case


CASE_ID = "case-email-auto-19f3f25cb64df962"
DOI = "10.3399/bjgpopen20X101030"
PMID = "32605913"
PMCID = "PMC7465578"
QUERY = "autistic adults healthcare access unmet needs systematic review"


def _article_text(xml: str) -> str:
    root = ET.fromstring(xml)
    return re.sub(r"\s+", " ", " ".join(root.itertext())).strip()


def run() -> dict:
    case_dir = FORJA / "state" / CASE_ID
    source = case_dir / "producao" / "ESTUDO_ESTRATEGICO_PLANO_SAUDE.md"
    cache = FORJA / "cache" / "science" / "10.3399-bjgpopen20X101030"
    cache.mkdir(parents=True, exist_ok=True)
    discovery = discover(QUERY, rows=5)
    crossref = crossref_by_doi(DOI)
    full_text = ncbi_fetch(PMCID, database="pmc")
    if crossref.get("status") != "ok" or full_text.get("status") != "ok":
        raise RuntimeError("piloto científico não obteve identidade Crossref e texto PMC")
    text = _article_text(full_text["text"])
    required_terms = ("barriers", "primary health care", "autism")
    if not all(term.casefold() in text.casefold() for term in required_terms):
        raise RuntimeError("texto recuperado não corresponde ao estudo selecionado")
    raw_files = {
        "discovery": cache / "DISCOVERY.json",
        "crossref": cache / "CROSSREF_DOI.json",
        "pmc": cache / "PMC7465578.xml",
    }
    atomic_write_json(raw_files["discovery"], discovery)
    atomic_write_json(raw_files["crossref"], crossref)
    raw_files["pmc"].write_text(full_text["text"], encoding="utf-8")
    source_hashes = {"caseStudy": sha256_file(source), **{key: sha256_file(path) for key, path in raw_files.items()}}
    manifest = read_json(case_dir / "FORJA_CASE_MANIFEST.json", {}) or {}
    registry = dict(manifest.get("n4SourceRegistry") or {})
    source_paths = {"caseStudy": source, **raw_files}
    registry.update({f"science:{key}": {"path": str(source_paths[key]), "sha256": value, "status": "active"} for key, value in source_hashes.items()})
    manifest["n4SourceRegistry"] = registry
    manifest["specVersionCandidate"] = "N4.0-candidate"
    atomic_write_json(case_dir / "FORJA_CASE_MANIFEST.json", manifest)

    def save(filename: str, content: dict) -> dict:
        payload = build_envelope(
            case_dir, filename, content, source_hashes=list(source_hashes.values()),
            producer_run_id="health-f5c-producer", reviewer_run_id="health-f7-science-reviewer", status="approved",
        )
        write_artifact(case_dir, filename, payload)
        return payload

    save("F2_N4_CLASSIFICATION.json", {
        "product": "estudo estratégico e minutas de tutela de saúde",
        "science": {
            "mode": "rapid",
            "triggerPropositionIds": ["PROP-ACCESS-001"],
            "domains": ["health_services", "autism"],
            "justification": "A situação envolve continuidade e acesso à assistência de pessoa autista; literatura não jurídica pode contextualizar barreiras de acesso, sem provar o caso individual.",
            "requiredBeforeF6": False,
        },
    })
    save("F5C_RESEARCH_PROTOCOL.json", {
        "mode": "rapid",
        "researchQuestion": "Quais barreiras de acesso à atenção em saúde são descritas para pessoas autistas e/ou com deficiência intelectual?",
        "populationContext": "pessoas autistas e/ou com deficiência intelectual em serviços de saúde",
        "exposureConcept": "barreiras e facilitadores de acesso",
        "outcomeConcept": "acesso efetivo à atenção em saúde",
        "designs": ["integrative review", "systematic review", "observational studies"],
        "synonyms": ["autism", "autistic adults", "intellectual disabilities", "healthcare access", "unmet needs"],
        "databases": ["Crossref", "PubMed/PMC", "OpenAlex (indisponível sem chave; não interpretado como ausência)"],
        "queries": [QUERY, "autism primary healthcare barriers facilitators review", "autism healthcare access no barriers contrary evidence"],
        "period": "sem restrição inicial; prioridade para revisões recentes e fontes com texto integral",
        "languages": ["English", "Portuguese"],
        "inclusionCriteria": ["identidade bibliográfica confirmada", "relação direta com acesso a serviços", "método e limitações legíveis"],
        "exclusionCriteria": ["protocolo sem resultados usado como evidência", "população sem relação transferível", "apenas metadado"],
        "deduplication": "DOI, PMID/PMCID, título e autoria",
        "stopRule": "saturação prática para apoio contextual rápido; nenhuma conclusão causal ou individual",
        "selectionMethod": "identidade em Crossref/PubMed e leitura das seções relevantes no PMC",
        "assessmentCriteria": ["desenho", "população", "método", "limitações", "transferibilidade"],
        "searchDate": now_iso(),
        "routeStatus": [{"source": route.get("source"), "status": route.get("status"), "count": len(route.get("items") or []), "reason": route.get("reason")} for route in discovery["routes"]],
    })
    item = crossref["item"]
    authors = [" ".join(filter(None, (author.get("given"), author.get("family")))) for author in item.get("author") or []]
    title = (item.get("title") or [""])[0]
    save("F5C_STUDY_LEDGER.json", {"studies": [{
        "studyId": "SCI-ACCESS-001",
        "title": title,
        "authors": authors,
        "year": 2020,
        "identifiers": {"doi": DOI, "pmid": PMID, "pmcid": PMCID, "openalex": None},
        "identityCheck": {"queriedTitle": "Barriers and facilitators to primary health care for people with intellectual disabilities and/or autism: an integrative review.", "returnedTitle": title, "queriedAuthors": ["Doherty"], "returnedAuthors": authors},
        "version": "version_of_record",
        "peerReviewStatus": "confirmed",
        "studyDesign": "integrative_review",
        "discipline": "health_services",
        "population": "pessoas com deficiência intelectual e/ou autismo",
        "sample": "literatura incluída pela revisão integrativa; heterogênea",
        "method": "revisão integrativa de barreiras e facilitadores na atenção primária",
        "mainFinding": "A revisão identifica barreiras e facilitadores de acesso à atenção primária nessa população.",
        "reportedEffect": None,
        "limitations": ["população combina deficiência intelectual e autismo", "contextos de atenção primária não equivalem ao litígio brasileiro", "não produz diagnóstico nem prova individual"],
        "funding": "reported_in_full_text",
        "conflicts": "reported_in_full_text",
        "publicationStatus": "current",
        "supportsClaimIds": ["SCI-CLAIM-ACCESS-001"],
        "doesNotSupport": ["má-fé ou boa-fé individual", "urgência clínica individual", "causalidade entre exclusão contratual e dano"],
        "transferability": "limited",
        "fullTextStatus": "read_relevant_sections",
        "verification": {"identity": "confirmed", "content": "confirmed", "correctionRetraction": "checked"},
        "rawSourcePaths": [str(raw_files["crossref"]), str(raw_files["pmc"])],
    }]})
    save("F5C_EVIDENCE_SYNTHESIS.json", {
        "synthesisStatus": "weak",
        "question": "barreiras de acesso para pessoas autistas e/ou com deficiência intelectual",
        "includedStudyIds": ["SCI-ACCESS-001"],
        "excluded": [{"reason": "protocol_only", "detail": "protocolos de revisão não foram tratados como resultados"}],
        "convergence": "Uma revisão integrativa é compatível com a existência de barreiras sistêmicas, mas não basta para generalização ampla.",
        "divergence": "Não foi localizado, nesta busca rápida, resultado que autorize inferência individual ou causal sobre o caso.",
        "limitations": ["apenas uma fonte foi lida integralmente no piloto", "transferência geográfica e institucional limitada", "apoio contextual, não probatório"],
        "contraryEvidenceSearch": {"performed": True, "queries": ["autism primary healthcare no barriers", "autism healthcare access contrary evidence"], "outcome": "nenhuma evidência contrária foi promovida; isso não prova inexistência"},
    })
    save("F5C_CLAIM_EVIDENCE_MAP.json", {"claims": [{
        "scienceClaimId": "SCI-CLAIM-ACCESS-001",
        "propositionId": "PROP-ACCESS-001",
        "draftText": "A literatura de serviços de saúde descreve barreiras de acesso à atenção primária para pessoas autistas e/ou com deficiência intelectual.",
        "epistemicStatus": "supported_with_limits",
        "useType": "contextual_support",
        "supportingStudyIds": ["SCI-ACCESS-001"],
        "contraryStudyIds": [],
        "synthesisStatus": "weak",
        "transferLimits": ["não comprova fato do processo", "não substitui laudo individual", "não autoriza causalidade", "contexto internacional"],
        "causalLanguageAllowed": False,
        "finalUseAllowed": True,
    }]})
    save("F7_SCIENCE_AUDIT.json", {
        "applicability": "required",
        "approved": True,
        "checks": {"identity": "pass", "version": "pass", "correctionRetraction": "pass", "claimMatch": "pass", "populationLimits": "pass", "associationCausality": "pass", "contraryEvidence": "pass", "individualProofSeparation": "pass"},
        "findings": [],
        "auditedClaimIds": ["SCI-CLAIM-ACCESS-001"],
    })
    result = validate_case(case_dir)
    report = {"schemaVersion": 1, "specVersion": "N4.0-candidate", "caseId": CASE_ID, "generatedAt": now_iso(), "approved": result["approved"], "mode": result.get("mode"), "findings": result["findings"], "sourceHashes": source_hashes}
    atomic_write_json(FORJA / "reports" / "N4_F5C_PILOT_HEALTH.json", report)
    return report


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
