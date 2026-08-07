"""Hash-bound FORJA N3 review package builder and gate validator."""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

from forja_n3_common import (
    ForjaN3Error,
    atomic_write_json,
    canonical_hash,
    now_iso,
    read_json,
    resolve_name,
    sha256_file,
)
from forja_state_machine import derive_state
from forja_adversarial_audit import (
    validate_adversarial_audit,
    validate_adversarial_recheck,
    validate_adversarial_strategy,
)
from forja_editorial_fidelity import validate_editorial_bundle
from forja_fidelity import compare_fidelity
from forja_official_sources import source_excerpt_sha256, validate_source_path
from forja_human_review import validate_claim_review_receipt
from forja_f8_contract import validate_f8 as validate_f8_contract
from forja_memoria_auditabilidade import validate_bundle as validate_audit_memory_bundle
from forja_authorities import authority_key
# Fachadas públicas previstas no contrato; a implementação vive no módulo do
# precedente, que não conhece empacotamento nem liberação.
from forja_precedente import (  # noqa: F401
    anchor_ids,
    failed_anchor_routes,
    validate_anchor_cards,
    validate_legal_research_trace,
)

RELEASE_POLICY_VERSION = "FORJA-LEGAL-RELEASE-v2"


def release_policy_hash() -> str:
    """Hash do conjunto executável que decide se uma peça pode ser liberada."""
    base = Path(__file__).resolve().parent
    files = [
        "forja_package.py",
        "forja_authorities.py",
        "forja_claim_binding.py",
        "forja_human_review.py",
        "forja_official_sources.py",
        "forja_editorial_fidelity.py",
        "forja_f8_contract.py",
        "forja_memoria_auditabilidade.py",
        "phase_contracts/F7.json",
        "phase_contracts/F8.json",
        "phase_contracts/F9.json",
    ]
    return canonical_hash({
        "version": RELEASE_POLICY_VERSION,
        "files": {
            name: sha256_file(base / name)
            for name in files
            if (base / name).is_file()
        },
    })


def _protocolable_content(item: dict, markdown: dict, files: dict | None = None) -> bool:
    tokens = " ".join([
        str(item.get("id") or ""),
        str(item.get("role") or ""),
        str(item.get("audience") or ""),
    ]).casefold()
    if any(token in tokens for token in (
        "protocol", "filing", "peti", "recurso", "contest", "manifesta",
        "agravo", "embargo",
    )):
        return True
    text = ""
    path = Path(str(markdown.get("path") or ""))
    if path.is_file():
        text = path.read_text(encoding="utf-8", errors="replace")[:20000]
    elif files:
        docx_path = Path(str((files.get("docx") or {}).get("path") or ""))
        pdf_path = Path(str((files.get("pdf") or {}).get("path") or ""))
        try:
            if docx_path.is_file():
                from docx import Document

                document = Document(str(docx_path))
                text = "\n".join(paragraph.text for paragraph in document.paragraphs)[:20000]
            elif pdf_path.is_file():
                import fitz

                with fitz.open(pdf_path) as document:
                    text = "\n".join(page.get_text("text") for page in document)[:20000]
        except Exception:
            # Falha de extração não torna conteúdo externo automaticamente seguro.
            text = ""
    head = text.casefold()
    return bool(re.search(
        r"\b(?:excelent[ií]ssim|egr[eé]gi[oa]|termos em que|pede deferimento|"
        r"dos pedidos|tribunal|ju[ií]z[oa] de direito|oab[/\s-])\b",
        head,
    ))


def _artifact(state: dict, artifact_id: str) -> dict:
    promoted = state.get("artifacts") or {}
    # Tentativas promovidas antes da renomeação de 25/07/2026 guardam o nome
    # anterior do mesmo artefato; ler o legado não é aceitar objeto diferente.
    artifact_id = resolve_name(artifact_id, promoted) or artifact_id
    entry = promoted.get(artifact_id)
    if not isinstance(entry, dict):
        raise ForjaN3Error(f"artefato não promovido: {artifact_id}")
    path = Path(str(entry.get("path") or ""))
    if not path.is_file():
        raise ForjaN3Error(f"arquivo ausente para {artifact_id}: {path}")
    actual = sha256_file(path)
    if actual != entry.get("sha256"):
        raise ForjaN3Error(f"hash divergente para {artifact_id}")
    return {**entry, "artifactId": artifact_id, "path": str(path), "sha256": actual, "size": path.stat().st_size}


def _f7_metrics(payload: dict, document_key: str | None) -> dict:
    documents = payload.get("documentos")
    if isinstance(documents, dict):
        if not document_key or document_key not in documents:
            raise ForjaN3Error(f"documento F7 não identificado no agregado: {document_key}")
        return documents[document_key]
    return payload


def _pending_citations(metrics: dict) -> list[str]:
    values = metrics.get("citacoesNaoConferidas") or []
    return sorted({str(value).strip() for value in values if str(value).strip()})


def _unresolved_markers(metrics: dict) -> list[str]:
    values = metrics.get("verificarRestantes") or []
    result = []
    for value in values:
        result.append(str(value.get("marcador") if isinstance(value, dict) else value).strip())
    return [value for value in result if value]


def validate_f7(artifact: dict, *, document_key: str | None, release_policy: str, markdown: dict) -> dict:
    payload = read_json(Path(artifact["path"]), None)
    if not isinstance(payload, dict):
        raise ForjaN3Error(f"F7 inválido: {artifact['path']}")
    metrics = _f7_metrics(payload, document_key)
    p0 = int(metrics.get("p0") or 0)
    pending = _pending_citations(metrics)
    markers = _unresolved_markers(metrics)
    blockers = []
    if release_policy != "internal_working" and metrics.get("mdSha256") != markdown.get("sha256"):
        blockers.append("F7 foi calculado sobre Markdown diferente")
    if p0:
        blockers.append(f"p0={p0}")
    if release_policy == "strict_protocol":
        blockers += [f"citação não conferida: {item}" for item in pending]
        blockers += [f"marcador pendente: {item}" for item in markers]
    # Anti-autocertificação: p0=0 escrito no JSON não basta. Reexecuta todos os
    # gates sobre o Markdown hash-bound que efetivamente entrará no pacote.
    recomputed_p0 = []
    recomputed_metrics = {}
    markdown_path = Path(str(markdown.get("path") or "")) if markdown else None
    if markdown_path and markdown_path.is_file():
        from forja_verificador import verificar
        from forja_metricas_f7 import metricas_f7
        texto = markdown_path.read_text(encoding="utf-8", errors="replace")
        recomputed_p0 = [item for item in verificar(texto, "peca") if item["sev"] == "P0"]
        blockers += [
            f"gate recomputado {item['gate']}: {item['problema']}"
            for item in recomputed_p0[:12]
        ]
        recomputed_metrics = metricas_f7(texto, require_live=release_policy == "strict_protocol")
        recomputed_pending = _pending_citations(recomputed_metrics)
        if release_policy == "strict_protocol":
            blockers += [f"citação não conferida na recomputação: {item}" for item in recomputed_pending]
        if sorted(pending) != sorted(recomputed_pending):
            blockers.append("lista declarada de citações pendentes diverge da recomputação")
    elif release_policy != "internal_working":
        blockers.append("Markdown ausente para recomputar os gates F7")
    return {
        "approved": not blockers,
        "p0": p0,
        "recomputedP0": len(recomputed_p0),
        "pendingCitations": pending,
        "markers": markers,
        "citations": (recomputed_metrics or {}).get("citacoes") or [],
        "blockers": blockers,
    }


def _ledger_entries(payload: Any) -> list[dict]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("citations", "citationLedger", "sources", "entries"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def _citation_key(item: dict) -> tuple[str, str, str]:
    return authority_key(item)


def _markdown_paragraphs(markdown_path: Path) -> list[str]:
    text = markdown_path.read_text(encoding="utf-8", errors="replace")
    return [item.strip() for item in re.split(r"\n\s*\n", text) if item.strip()]


def _document_binding(item: dict, markdown: dict) -> tuple[dict, list[str]]:
    """Recompõe o vínculo entre recibo, proposição e Markdown final."""
    claim = str(item.get("claim") or item.get("id") or "fonte sem claim").strip()
    findings: list[str] = []
    markdown_path = Path(str(markdown.get("path") or ""))
    if not markdown_path.is_file():
        return {}, [f"{claim}: Markdown final ausente para vínculo da proposição"]
    actual_document_hash = sha256_file(markdown_path)
    if item.get("documentSha256") != actual_document_hash:
        findings.append(f"{claim}: hash do documento final diverge")
    proposition = str(item.get("documentProposition") or "").strip()
    if not proposition:
        findings.append(f"{claim}: proposição exata do documento ausente")
    if item.get("documentPropositionSha256") != canonical_hash({"proposition": proposition}):
        findings.append(f"{claim}: hash da proposição do documento diverge")
    try:
        paragraph_index = int(item.get("documentParagraphIndex"))
    except (TypeError, ValueError):
        paragraph_index = 0
    paragraphs = _markdown_paragraphs(markdown_path)
    paragraph = paragraphs[paragraph_index - 1] if 1 <= paragraph_index <= len(paragraphs) else ""
    if not paragraph:
        findings.append(f"{claim}: índice do parágrafo final inválido")
    elif proposition not in paragraph:
        findings.append(f"{claim}: proposição não consta literalmente do parágrafo indicado")
    if item.get("documentParagraphSha256") != canonical_hash({"paragraph": paragraph}):
        findings.append(f"{claim}: hash do parágrafo final diverge")
    authority_identity = item.get("authorityIdentity")
    if not isinstance(authority_identity, dict) or _citation_key(authority_identity) == ("", "", ""):
        findings.append(f"{claim}: identidade da autoridade ausente")
        authority_identity = {}
    if item.get("authorityIdentitySha256") != canonical_hash(authority_identity):
        findings.append(f"{claim}: hash da identidade da autoridade diverge")
    expected = {
        "documentSha256": actual_document_hash,
        "documentProposition": proposition,
        "documentPropositionSha256": canonical_hash({"proposition": proposition}),
        "documentParagraphIndex": paragraph_index,
        "documentParagraphSha256": canonical_hash({"paragraph": paragraph}),
        "authorityIdentity": authority_identity,
        "authorityIdentitySha256": canonical_hash(authority_identity),
    }
    return expected, findings


def _denied_search_actions() -> set[str]:
    """Ações vedadas pela política de busca, lidas sem acionar o TeiaJus."""
    config = read_json(Path(__file__).resolve().parent / "FORJA_SEARCH_CONFIG.json", None)
    if not isinstance(config, dict):
        return set()
    return {str(v) for v in ((config.get("policy") or {}).get("deniedActions") or [])}


def _brief_routes(case_dir: Path | None) -> tuple[str | None, set[str]]:
    """Rota selecionada e rotas comparadas no brief, quando houver brief."""
    if case_dir is None:
        return None, set()
    brief = read_json(case_dir / "n4_artifacts" / "F4_SIGNATURE_BRIEF.json", None)
    if not isinstance(brief, dict):
        return None, set()
    payload = brief.get("payload") if isinstance(brief.get("payload"), dict) else brief
    rotas = {
        str(route.get("routeId"))
        for route in (payload.get("routes") or [])
        if isinstance(route, dict) and route.get("routeId")
    }
    return (str(payload.get("selectedRouteId") or "") or None), rotas


def validate_source_ledger(
    artifact: dict,
    *,
    release_policy: str,
    expected_citations: list[dict] | None = None,
    markdown: dict | None = None,
    case_dir: Path | None = None,
) -> dict:
    payload = read_json(Path(artifact["path"]), None)
    entries = _ledger_entries(payload)
    blocked = []
    # Trilha de pesquisa e fichas de âncora: blocos aditivos. Ledger que não os
    # traz é anterior ao protocolo e continua liberando normalmente.
    research_findings = validate_legal_research_trace(
        payload if isinstance(payload, dict) else {},
        release_policy,
        denied_actions=_denied_search_actions(),
        case_dir=case_dir,
    )
    selected_route, compared_routes = _brief_routes(case_dir)
    anchor_findings = validate_anchor_cards(
        entries, selected_route_id=selected_route, compared_route_ids=compared_routes
    )
    blocked += [f"{item['code']}: {item['detail']}" for item in research_findings + anchor_findings]
    covered: set[tuple[str, str, str]] = set()
    for item in entries:
        claim = str(item.get("claim") or item.get("id") or "fonte sem claim").strip()
        if item.get("finalUseAllowed") is False:
            blocked.append(claim)
            continue
        if item.get("finalUseAllowed") is not True:
            blocked.append(claim)
            continue
        source_value = str(item.get("sourcePathOrUrl") or "").strip()
        if not source_value or re.match(r"^https?://", source_value, re.I):
            blocked.append(f"{claim}: URL sem captura hash-bound")
            continue
        source_path = Path(source_value)
        excerpt = str(item.get("sourceExcerpt") or "").strip()
        strict = release_policy == "strict_protocol"
        binding_expected = {}
        if strict:
            if not str(item.get("generatorRunId") or "").strip():
                blocked.append(f"{claim}: produtor da proposição não identificado")
            if not excerpt:
                blocked.append(f"{claim}: trecho oficial probatório ausente")
            elif item.get("sourceExcerptSha256") != source_excerpt_sha256(excerpt):
                blocked.append(f"{claim}: hash do trecho oficial diverge")
            binding_expected, binding_findings = _document_binding(item, markdown or {})
            blocked += binding_findings
            review = item.get("claimReview") or {}
            receipt_path = Path(str(review.get("receiptPath") or ""))
            if review.get("status") != "pass" or not receipt_path.is_file():
                blocked.append(f"{claim}: proposição jurisprudencial sem recibo humano assinado")
            elif review.get("receiptSha256") != sha256_file(receipt_path):
                blocked.append(f"{claim}: hash do recibo humano diverge")
            else:
                receipt_result = validate_claim_review_receipt(
                    receipt_path,
                    expected={
                        "generatorRunId": str(item.get("generatorRunId") or ""),
                        "claim": claim,
                        "claimSha256": canonical_hash({"claim": claim}),
                        "sourceExcerpt": excerpt,
                        "sourceExcerptSha256": source_excerpt_sha256(excerpt),
                        "sourceSha256": sha256_file(source_path) if source_path.is_file() else None,
                        "sourceUrl": str(item.get("sourceUrl") or ""),
                        "sourceIdentity": item.get("sourceIdentity") or {},
                        "sourceIdentitySha256": canonical_hash(item.get("sourceIdentity") or {}),
                        **binding_expected,
                    },
                )
                if not receipt_result["approved"]:
                    blocked.append(
                        f"{claim}: recibo humano reprovado: "
                        + ", ".join(receipt_result["findings"])
                    )
        validation = validate_source_path(
            source_path,
            require_live=strict,
            required_excerpt=excerpt if strict and excerpt else None,
        )
        if not validation["approved"]:
            blocked.append(
                f"{claim}: "
                + ", ".join(validation["findings"])
            )
            continue
        record = validation.get("record") or {}
        if item.get("sourceSha256") != sha256_file(source_path):
            blocked.append(f"{claim}: hash da fonte não confere")
        if item.get("sourceUrl") != record.get("sourceUrl"):
            blocked.append(f"{claim}: URL oficial diverge do lastro")
        if item.get("sourceIdentity") != record.get("identity"):
            blocked.append(f"{claim}: identidade do precedente diverge do lastro")
        authority_identity = item.get("authorityIdentity") or {}
        if not strict or not any(value.startswith(f"{claim}:") for value in blocked):
            covered.add(_citation_key(authority_identity or record.get("identity") or {}))

    if release_policy == "strict_protocol":
        expected = {_citation_key(item) for item in expected_citations or []}
        expected.discard(("", "", ""))
        ambiguous = sorted(
            key for key in expected
            if key[0] in {"TRIBUNAL_AMBIGUO", "TRIBUNAL_NAO_MAPEADO", ""}
        )
        for court, kind, number in ambiguous:
            blocked.append(f"autoridade ambígua sem tribunal resolvido: {court or '?'} {kind} {number}")
        missing = sorted(expected - covered)
        for court, kind, number in missing:
            blocked.append(f"citação sem entrada probatória no source ledger: {court or '?'} {kind} {number}")
    return {
        "approved": release_policy != "strict_protocol" or not blocked,
        "blocked": blocked,
        "entries": len(entries),
        "expectedCitations": len(expected_citations or []),
        "coveredCitations": len(covered),
        "researchRuns": len((payload or {}).get("searchRuns") or []) if isinstance(payload, dict) else 0,
        "anchors": sorted(anchor_ids(entries)),
        "anchorFindings": anchor_findings,
        "failedAnchorRoutes": sorted(failed_anchor_routes(anchor_findings, entries)),
    }


# Fachada pública preservada; a implementação canônica vive no contrato neutro.
validate_f8 = validate_f8_contract


def validate_context_artifact(artifact: dict, *, markdown: dict, release_policy: str) -> dict:
    payload = read_json(Path(artifact["path"]), None)
    if not isinstance(payload, dict):
        raise ForjaN3Error(f"validação de contexto inválida: {artifact['path']}")
    findings = []
    if payload.get("approved") is not True or int(payload.get("p0") or 0):
        findings.append("contexto contém bloqueio P0")
    if release_policy == "strict_protocol" and int(payload.get("p1") or 0):
        findings.append("contexto protocolável contém pendência P1")
    recorded_hash = ((payload.get("markdown") or {}).get("sha256"))
    if recorded_hash != markdown.get("sha256"):
        findings.append("contexto foi validado contra Markdown diferente")
    return {"approved": not findings, "findings": findings, "p0": payload.get("p0"), "p1": payload.get("p1")}


def validate_fidelity(artifact: dict, *, files: dict) -> dict:
    payload = read_json(Path(artifact["path"]), None)
    if not isinstance(payload, dict):
        raise ForjaN3Error(f"fidelidade inválida: {artifact['path']}")
    findings = []
    static_mode = payload.get("mode") == "markdown_docx_ooxml" or "pdf" not in files
    if payload.get("approved") is not True:
        findings.append("fidelidade Markdown/OOXML não aprovada" if static_mode else "fidelidade Markdown/Word/PDF não aprovada")
    if static_mode:
        expected_md = (files.get("md") or {}).get("sha256")
        expected_docx = (files.get("docx") or {}).get("sha256")
        if not expected_md or (payload.get("markdown") or {}).get("sha256") != expected_md:
            findings.append("fidelidade usa Markdown diferente do pacote")
        if not expected_docx or (payload.get("docx") or {}).get("sha256") != expected_docx:
            findings.append("fidelidade usa DOCX diferente do pacote")
        blocks = payload.get("blocks") or {}
        if blocks.get("docxCoverage") != 1.0:
            findings.append("fidelidade OOXML sem cobertura integral de blocos")
        recomputed = None
        try:
            recomputed = compare_docx_fidelity(
                Path(files["md"]["path"]), Path(files["docx"]["path"])
            )
            if not recomputed["approved"]:
                codes = ", ".join(item["code"] for item in recomputed["findings"][:8])
                findings.append(f"fidelidade OOXML reprovada na recomputação: {codes}")
            if payload.get("blocks") != recomputed.get("blocks"):
                findings.append("métricas de fidelidade OOXML divergem da recomputação")
        except Exception as exc:
            findings.append(f"não foi possível recomputar a fidelidade OOXML: {exc}")
        return {"approved": not findings, "findings": findings, "recomputed": recomputed}
    for kind in ("markdown", "docx", "pdf"):
        file_key = "md" if kind == "markdown" else kind
        expected = (files.get(file_key) or {}).get("sha256")
        actual = ((payload.get(kind) or {}).get("sha256"))
        if not expected or actual != expected:
            findings.append(f"fidelidade usa {kind} diferente do pacote")
    blocks = payload.get("blocks") or {}
    if blocks.get("docxCoverage") != 1.0 or blocks.get("pdfCoverage") != 1.0:
        findings.append("fidelidade sem cobertura integral de blocos")
    # Anti-trapaça: cobertura 1.0 escrita pelo produtor não vale sem reproduzir
    # a comparação diretamente nos três arquivos do pacote.
    recomputed = None
    try:
        recomputed = compare_fidelity(
            Path(files["md"]["path"]),
            Path(files["docx"]["path"]),
            Path(files["pdf"]["path"]),
        )
        if not recomputed["approved"]:
            codes = ", ".join(item["code"] for item in recomputed["findings"][:8])
            findings.append(f"fidelidade reprovada na recomputação: {codes}")
        if payload.get("blocks") != recomputed.get("blocks"):
            findings.append("métricas de fidelidade declaradas divergem da recomputação")
    except Exception as exc:
        findings.append(f"não foi possível recomputar a fidelidade: {exc}")
    return {"approved": not findings, "findings": findings, "recomputed": recomputed}


def _email_claims(email_text: str, pending: list[str]) -> list[str]:
    findings = []
    claims_all_verified = re.search(r"tod[ao]s?\s+(?:as\s+)?(?:fontes|cita[cç][oõ]es).{0,35}(?:conferid|verificad)", email_text, re.I)
    if pending and claims_all_verified:
        findings.append("e-mail afirma conferência total apesar de pendências")
    normalized = email_text.casefold()
    for item in pending:
        if item.casefold() not in normalized:
            findings.append(f"pendência não informada no e-mail: {item}")
    return findings


def validate_adversarial_bundle(state: dict, item: dict) -> dict:
    findings = []
    artifacts = {}
    requested = item.get("adversarialResponse") is True
    audit_id = str(item.get("adversarialAuditArtifactId") or "adversarial_audit")
    audit_entry = (state.get("artifacts") or {}).get(audit_id)
    if not isinstance(audit_entry, dict):
        if requested:
            findings.append("peça de resposta sem auditoria da manifestação adversária")
        return {"approved": not findings, "findings": findings, "applicable": requested, "artifacts": artifacts}
    audit = _artifact(state, audit_id)
    artifacts[audit_id] = audit
    audit_payload = read_json(Path(audit["path"]), None) or {}
    applicable = audit_payload.get("applicable") is True
    if requested and not applicable:
        findings.append("pacote declara resposta adversarial, mas o ledger marcou não aplicável")
    if not applicable and not requested:
        audit_result = validate_adversarial_audit(audit_payload)
        findings += list(audit_result.get("p0") or [])
        return {"approved": not findings, "findings": findings, "applicable": False, "artifacts": artifacts}
    audit_result = validate_adversarial_audit(audit_payload)
    findings += list(audit_result.get("p0") or [])

    strategy_id = str(item.get("adversarialStrategyArtifactId") or "adversarial_strategy")
    recheck_id = str(item.get("adversarialRecheckArtifactId") or "adversarial_recheck")
    try:
        strategy = _artifact(state, strategy_id)
        artifacts[strategy_id] = strategy
        strategy_result = validate_adversarial_strategy(read_json(Path(strategy["path"]), None) or {}, Path(audit["path"]))
        findings += list(strategy_result.get("p0") or [])
    except ForjaN3Error as exc:
        findings.append(str(exc))
        strategy = None
    try:
        recheck = _artifact(state, recheck_id)
        artifacts[recheck_id] = recheck
        if strategy is not None:
            recheck_result = validate_adversarial_recheck(
                read_json(Path(recheck["path"]), None) or {},
                Path(audit["path"]),
                Path(strategy["path"]),
            )
            findings += list(recheck_result.get("p0") or [])
    except ForjaN3Error as exc:
        findings.append(str(exc))
    return {"approved": not findings, "findings": findings, "applicable": True, "artifacts": artifacts}


def validate_definition(case_dir: Path, definition: dict) -> dict:
    state = derive_state(case_dir)
    if definition.get("caseId") != case_dir.name:
        raise ForjaN3Error("caseId da definição diverge da pasta")
    deliverables = definition.get("deliverables") or []
    if not deliverables:
        raise ForjaN3Error("pacote sem entregáveis")
    email = _artifact(state, str(definition.get("emailArtifactId") or ""))
    email_text = Path(email["path"]).read_text(encoding="utf-8", errors="replace")
    package_findings = []
    output = []
    attachments = []
    all_pending = []
    adversarial_artifacts = {}
    seen_deliverables = set()
    for item in deliverables:
        deliverable_id = str(item.get("id") or "").strip()
        if not deliverable_id or deliverable_id in seen_deliverables:
            raise ForjaN3Error(f"ID de entregável ausente ou duplicado: {deliverable_id}")
        seen_deliverables.add(deliverable_id)
        policy = item.get("releasePolicy") or "internal_working"
        if policy not in {"strict_protocol", "decision_support", "internal_working"}:
            raise ForjaN3Error(f"política inválida em {deliverable_id}: {policy}")
        files = {}
        artifact_fields = {
            "md": "mdArtifactId",
            "docx": "docxArtifactId",
            "pdf": "pdfArtifactId",
            "visual_qa_ledger": "visualQaArtifactId",
            "visual_build_manifest": "visualBuildArtifactId",
            "visual_review_attestation": "visualReviewAttestationArtifactId",
            "audit_memory_manifest": "auditMemoryManifestArtifactId",
            "audit_memory_markdown": "auditMemoryMarkdownArtifactId",
            "audit_memory_html": "auditMemoryHtmlArtifactId",
        }
        for kind, field in artifact_fields.items():
            artifact_id = item.get(field)
            if artifact_id:
                files[kind] = _artifact(state, str(artifact_id))
        static_route = item.get("visualRoute") == "visual_law_canonica_svg_ooxml" or (
            item.get("noRender") is True and "pdf" not in files
        )
        if static_route and "pdf" in files:
            package_findings.append(
                f"{deliverable_id}: rota visual canônica não aceita PDF/rerender como anexo"
            )
        if _protocolable_content(item, files.get("md") or {}, files) and policy != "strict_protocol":
            package_findings.append(
                f"{deliverable_id}: conteúdo protocolável não pode rebaixar a política {policy}"
            )
        if (
            policy != "internal_working"
            and "final_markdown" in (state.get("artifacts") or {})
            and not str(item.get("mdArtifactId") or "").startswith("final_markdown")
        ):
            package_findings.append(
                f"{deliverable_id}: pacote usa Markdown anterior ao passe editorial final"
            )
        editorial_result = None
        md_artifact_id = str(item.get("mdArtifactId") or "")
        if policy != "internal_working" and md_artifact_id.startswith("final_markdown"):
            suffix = md_artifact_id[len("final_markdown"):]
            try:
                audited = _artifact(state, f"audited_markdown{suffix}")
                editorial_report = _artifact(state, f"editorial_report{suffix}")
                editor_usage = _artifact(state, f"editor_usage{suffix}")
                editorial_result = validate_editorial_bundle(
                    Path(audited["path"]), Path(files["md"]["path"]),
                    Path(editorial_report["path"]), Path(editor_usage["path"]),
                    strict_family=policy == "strict_protocol",
                )
                if not editorial_result["approved"]:
                    package_findings += [
                        f"{deliverable_id}: passe editorial: {value['detail']}"
                        for value in editorial_result["findings"]
                    ]
            except ForjaN3Error as exc:
                package_findings.append(f"{deliverable_id}: bundle editorial incompleto: {exc}")
        if policy != "internal_working":
            required_files = (
                (("md", "Markdown"), ("docx", "Word"),
                 ("visual_qa_ledger", "QA visual OOXML"),
                 ("visual_build_manifest", "manifesto de materialização"),
                 ("audit_memory_manifest", "manifesto da memória"),
                 ("audit_memory_markdown", "memória Markdown"),
                 ("audit_memory_html", "memória HTML"))
                if static_route else
                (("md", "Markdown"), ("docx", "Word"), ("pdf", "PDF"))
            )
            for kind, label in required_files:
                if kind not in files:
                    package_findings.append(f"{deliverable_id}: {label} ausente")
        f7 = _artifact(state, str(item.get("f7ArtifactId") or ""))
        f7_result = validate_f7(
            f7,
            document_key=item.get("f7DocumentKey"),
            release_policy=policy,
            markdown=files.get("md") or {},
        )
        all_pending += f7_result["pendingCitations"] + f7_result["markers"]
        if not f7_result["approved"]:
            package_findings += [f"{deliverable_id}: {value}" for value in f7_result["blockers"]]
        source_result = None
        if item.get("sourceLedgerArtifactId"):
            source_ledger_id = str(item["sourceLedgerArtifactId"])
            if policy == "strict_protocol" and not source_ledger_id.startswith("verified_source_ledger"):
                package_findings.append(
                    f"{deliverable_id}: strict_protocol exige verified_source_ledger promovido no F7"
                )
            source = _artifact(state, source_ledger_id)
            source_result = validate_source_ledger(
                source,
                release_policy=policy,
                expected_citations=f7_result.get("citations") or [],
                markdown=files.get("md") or {},
                case_dir=case_dir,
            )
            if not source_result["approved"]:
                package_findings += [f"{deliverable_id}: fonte não autorizada: {value}" for value in source_result["blocked"]]
            # Âncora reprovada não é defeito de fonte: é a rota estratégica que
            # deixou de se sustentar. F4 reabre antes de qualquer nova redação.
            for rota in source_result.get("failedAnchorRoutes") or []:
                package_findings.append(
                    f"{deliverable_id}: FAL-F7-ANCHOR-INVALIDATES-ROUTE: âncora reprovada atinge "
                    f"a rota {rota}; reabrir F4 antes de redigir"
                )
        elif policy == "strict_protocol":
            package_findings.append(f"{deliverable_id}: source ledger ausente")
        f8_result = None
        context_result = None
        fidelity_result = None
        adversarial_result = validate_adversarial_bundle(state, item)
        if not adversarial_result["approved"]:
            package_findings += [f"{deliverable_id}: auditoria adversarial: {value}" for value in adversarial_result["findings"]]
        adversarial_artifacts.update(adversarial_result["artifacts"])
        if policy != "internal_working":
            context = _artifact(state, str(item.get("contextArtifactId") or ""))
            context_result = validate_context_artifact(context, markdown=files.get("md") or {}, release_policy=policy)
            if not context_result["approved"]:
                package_findings += [f"{deliverable_id}: {value}" for value in context_result["findings"]]
            f8 = _artifact(state, str(item.get("f8ArtifactId") or ""))
            if static_route:
                files.setdefault("md", files.get("md") or {})
                files.setdefault("visual_review_attestation", files.get("visual_review_attestation") or {})
                visual_build = read_json(Path(files["visual_build_manifest"]["path"]), None) if files.get("visual_build_manifest") else None
                if not isinstance(visual_build, dict):
                    package_findings.append(f"{deliverable_id}: manifesto de materialização inválido")
                else:
                    if visual_build.get("rota") != "visual_law_canonica_svg_ooxml":
                        package_findings.append(f"{deliverable_id}: rota visual não é SVG/OOXML canônica")
                    for key in ("renderingUsed", "pdfCreated", "pngCreated"):
                        if visual_build.get(key) is not False:
                            package_findings.append(f"{deliverable_id}: manifesto visual declara {key} diferente de false")
                f8_result = validate_f8(f8, files=files, release_policy=policy)
                if not f8_result["approved"]:
                    package_findings += [f"{deliverable_id}: {value}" for value in f8_result["findings"]]
                memory_manifest = files.get("audit_memory_manifest")
                if memory_manifest:
                    memory_result = validate_audit_memory_bundle(
                        Path(memory_manifest["path"]), expected_case_dir=case_dir
                    )
                    if not memory_result["approved"]:
                        package_findings += [
                            f"{deliverable_id}: memória de auditabilidade: {value}"
                            for value in memory_result["findings"]
                        ]
            elif "pdf" in files:
                f8_result = validate_f8(f8, files=files, release_policy=policy)
                if not f8_result["approved"]:
                    package_findings += [f"{deliverable_id}: {value}" for value in f8_result["findings"]]
            fidelity = _artifact(state, str(item.get("fidelityArtifactId") or ""))
            fidelity_result = validate_fidelity(fidelity, files=files)
            if not fidelity_result["approved"]:
                package_findings += [f"{deliverable_id}: {value}" for value in fidelity_result["findings"]]
        for kind in item.get("attachKinds") or (["docx", "audit_memory_html"] if static_route else ["docx", "pdf"]):
            if kind in files:
                attachments.append({"deliverableId": deliverable_id, "kind": kind, **files[kind]})
        output.append({
            "id": deliverable_id,
            "role": item.get("role"),
            "audience": item.get("audience"),
            "releasePolicy": policy,
            "files": files,
            "f7": {"artifact": f7, "result": f7_result},
            "sourceLedger": source_result,
            "context": context_result,
            "f8": f8_result,
            "fidelity": fidelity_result,
            "editorial": editorial_result,
            "adversarial": {key: value for key, value in adversarial_result.items() if key != "artifacts"},
        })
    email_findings = _email_claims(email_text, sorted(set(all_pending)))
    package_findings += email_findings
    from forja_estilo_humano import relatorio as relatorio_estilo_humano
    email_style = relatorio_estilo_humano(email_text, "email")
    package_findings += [
        f"e-mail reprovado por {item['gate']}: {item['problema']}"
        for item in email_style["achados"]
        if item["sev"] == "P0"
    ]
    return {
        "approved": not package_findings,
        "findings": package_findings,
        "deliverables": output,
        "email": email,
        "emailStyle": email_style,
        "attachments": attachments,
        "adversarialArtifacts": list(adversarial_artifacts.values()),
        "pending": sorted(set(all_pending)),
        "stateRevision": state["revision"],
    }


def build_package(case_dir: Path, definition_path: Path, *, publish_pointer: bool = True) -> dict:
    definition = read_json(definition_path, None)
    if not isinstance(definition, dict):
        raise ForjaN3Error(f"definição de pacote inválida: {definition_path}")
    validation = validate_definition(case_dir, definition)
    if not validation["approved"]:
        raise ForjaN3Error("pacote reprovado: " + "; ".join(validation["findings"]))
    from forja_n4_validate import validate_case as validate_n4

    n4_validation = validate_n4(case_dir, target_phase="F9_PACOTE_REVISAO_DRAFT_OPCIONAL")
    if n4_validation.get("blocksCurrentFlow"):
        raise ForjaN3Error("pacote bloqueado pela N4: " + "; ".join(item["detail"] for item in n4_validation.get("findings") or [] if item.get("severity") == "p0"))
    identity = {
        "policyVersion": RELEASE_POLICY_VERSION,
        "policyHash": release_policy_hash(),
        "definition": definition,
        "attachments": [{"artifactId": item["artifactId"], "sha256": item["sha256"]} for item in validation["attachments"]],
        "emailSha256": validation["email"]["sha256"],
        "adversarial": [
            {"artifactId": item["artifactId"], "sha256": item["sha256"]}
            for item in validation.get("adversarialArtifacts") or []
        ],
        "stateRevision": validation["stateRevision"],
        "n4ValidationHash": n4_validation.get("validationHash"),
    }
    package_hash = canonical_hash(identity)
    package_id = f"pkg-{package_hash[:16]}"
    packages = case_dir / "packages"
    final_dir = packages / package_id
    if not final_dir.exists():
        packages.mkdir(parents=True, exist_ok=True)
        temp_dir = Path(tempfile.mkdtemp(prefix=f".{package_id}.", dir=packages))
        try:
            copied = []
            for item in validation["attachments"]:
                source = Path(item["path"])
                destination = temp_dir / source.name
                if destination.exists():
                    destination = temp_dir / f"{item['artifactId']}-{source.name}"
                shutil.copy2(source, destination)
                if sha256_file(destination) != item["sha256"]:
                    raise ForjaN3Error(f"hash mudou ao montar pacote: {item['artifactId']}")
                copied.append({**item, "packagePath": str(final_dir / destination.name)})
            manifest = {
                "schemaVersion": 2,
                "specVersion": "N3.0-r3",
                "policyVersion": RELEASE_POLICY_VERSION,
                "policyHash": identity["policyHash"],
                "packageId": package_id,
                "packageHash": package_hash,
                "caseId": case_dir.name,
                "runId": definition.get("runId"),
                "createdAt": now_iso(),
                "status": "ready_for_review",
                "stateRevision": validation["stateRevision"],
                "definitionHash": canonical_hash(definition),
                "definition": definition,
                "identity": identity,
                "deliverables": validation["deliverables"],
                "email": validation["email"],
                "emailStyle": validation["emailStyle"],
                "attachments": copied,
                "adversarialChecks": identity["adversarial"],
                "pending": validation["pending"],
                "n4": {
                    "specVersion": n4_validation.get("specVersion"),
                    "mode": n4_validation.get("mode"),
                    "approved": n4_validation.get("approved"),
                    "blocksCurrentFlow": n4_validation.get("blocksCurrentFlow"),
                    "validationHash": n4_validation.get("validationHash"),
                    "materialBlocks": n4_validation.get("materialBlocks"),
                },
            }
            atomic_write_json(temp_dir / "FORJA_PACKAGE.json", manifest)
            os.replace(temp_dir, final_dir)
        finally:
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
    manifest = read_json(final_dir / "FORJA_PACKAGE.json", None)
    if publish_pointer:
        atomic_write_json(case_dir / "FORJA_PACKAGE.json", manifest)
    return manifest


def revalidate_package_manifest(case_dir: Path, manifest: dict) -> dict:
    """Revalida um pacote no estado e na política atuais, sem mutar o caso."""
    findings: list[str] = []
    if not isinstance(manifest, dict) or manifest.get("schemaVersion") != 2:
        return {
            "approved": False,
            "stale": True,
            "findings": ["manifesto anterior à política de liberação v2"],
        }
    if manifest.get("policyVersion") != RELEASE_POLICY_VERSION:
        findings.append("versão da política de liberação está obsoleta")
    current_policy_hash = release_policy_hash()
    if manifest.get("policyHash") != current_policy_hash:
        findings.append("hash da política de liberação mudou; pacote deve ser refeito")
    definition = manifest.get("definition")
    if not isinstance(definition, dict):
        findings.append("snapshot da definição do pacote ausente")
    elif manifest.get("definitionHash") != canonical_hash(definition):
        findings.append("hash da definição do pacote diverge")
    else:
        try:
            current = validate_definition(case_dir, definition)
            if not current["approved"]:
                findings += [f"revalidação: {item}" for item in current["findings"]]
        except Exception as exc:
            findings.append(f"revalidação da definição falhou: {exc}")
    identity = manifest.get("identity")
    if not isinstance(identity, dict) or canonical_hash(identity) != manifest.get("packageHash"):
        findings.append("identidade criptográfica do pacote diverge")
    for attachment in manifest.get("attachments") or []:
        path = Path(str(attachment.get("packagePath") or ""))
        if not path.is_file() or sha256_file(path) != attachment.get("sha256"):
            findings.append(f"anexo empacotado divergente: {attachment.get('artifactId') or path.name}")
    return {
        "approved": not findings,
        "stale": bool(findings),
        "findings": findings,
        "policyVersion": RELEASE_POLICY_VERSION,
        "policyHash": current_policy_hash,
    }
