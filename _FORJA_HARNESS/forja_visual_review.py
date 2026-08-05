"""Prova verificável da inspeção visual página a página da FORJA.

O render automático produz imagens e detecta alguns defeitos, mas não pode se
declarar revisor independente. Este módulo mantém as duas coisas separadas:

* ``build_pending_review`` cria apenas um roteiro PENDENTE, com hashes reais;
* ``validate_visual_review`` valida uma revisão humana ou de agente visual;
* nenhuma função preenche ``pass`` ou marca checks como verdadeiros.

O gate estrutural do DOCX é recomputado fora desta declaração. Assim, mesmo um
JSON de revisão fabricado não consegue liberar corpo desalinhado ou tipografia
fora do padrão.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from forja_n3_common import atomic_write_json, now_iso, read_json, sha256_file


REQUIRED_PAGE_CHECKS = (
    "bodyAlignment",
    "typographyConsistency",
    "clipping",
    "overlap",
    "spacing",
    "tablesAndFigures",
    "headersAndFooters",
    "pageBreaksAndOrphans",
)
ALLOWED_REVIEW_TYPES = {"human", "agent_visual"}
ATTESTATION_VERSION = "FORJA-PAGE-VISUAL-v2"


def _rendered_page_map(rendered_pages: list[dict]) -> dict[int, dict]:
    result: dict[int, dict] = {}
    for entry in rendered_pages:
        try:
            number = int(entry.get("page"))
        except (TypeError, ValueError, AttributeError):
            continue
        result[number] = entry
    return result


def build_pending_review(
    output: Path,
    *,
    pdf: Path,
    rendered_pages: list[dict],
    generator_run_id: str,
    docx: Path | None = None,
) -> dict:
    """Cria um formulário hash-bound sem aprovar nenhuma página."""
    pages = []
    for rendered in rendered_pages:
        pages.append({
            "page": int(rendered["page"]),
            "reviewedImageSha256": rendered.get("imageSha256"),
            "status": "pending",
            "checks": {name: None for name in REQUIRED_PAGE_CHECKS},
            "notes": "",
        })
    payload = {
        "schemaVersion": 2,
        "attestationVersion": ATTESTATION_VERSION,
        "createdAt": now_iso(),
        "reviewedAt": None,
        "generatorRunId": generator_run_id,
        "reviewer": {"id": None, "runId": None, "type": None},
        "reviewMethod": None,
        "autoFilled": False,
        "pdfSha256": sha256_file(pdf),
        "docxSha256": sha256_file(docx) if docx else None,
        "pageCount": len(pages),
        "requiredChecks": list(REQUIRED_PAGE_CHECKS),
        "pages": pages,
        "approved": False,
    }
    atomic_write_json(Path(output), payload)
    return payload


def validate_visual_review(
    review_path: Path,
    *,
    pdf: Path,
    rendered_pages: list[dict],
    generator_run_id: str,
    expected_reviewer_run_id: str | None = None,
    docx: Path | None = None,
) -> dict:
    """Valida autoria independente, cobertura e hashes de todas as páginas."""
    review_path = Path(review_path)
    payload = read_json(review_path, None)
    findings: list[dict[str, Any]] = []
    if not isinstance(payload, dict):
        return {
            "approved": False,
            "reviewPath": str(review_path),
            "findings": [{"severity": "P0", "code": "visual_review_invalid_json"}],
            "pages": [],
        }

    if payload.get("schemaVersion") != 2 or payload.get("attestationVersion") != ATTESTATION_VERSION:
        findings.append({"severity": "P0", "code": "visual_review_wrong_schema"})
    if payload.get("autoFilled") is not False:
        findings.append({"severity": "P0", "code": "visual_review_autofilled_or_undeclared"})
    if payload.get("reviewMethod") != "page_by_page_at_100_percent":
        findings.append({"severity": "P0", "code": "visual_review_method_not_proved"})
    if not payload.get("reviewedAt"):
        findings.append({"severity": "P0", "code": "visual_review_without_timestamp"})
    if payload.get("pdfSha256") != sha256_file(pdf):
        findings.append({"severity": "P0", "code": "visual_review_wrong_pdf"})
    if docx is not None and payload.get("docxSha256") != sha256_file(docx):
        findings.append({"severity": "P0", "code": "visual_review_wrong_docx"})
    if payload.get("generatorRunId") != generator_run_id:
        findings.append({"severity": "P0", "code": "visual_review_wrong_generator"})
    if payload.get("requiredChecks") != list(REQUIRED_PAGE_CHECKS):
        findings.append({"severity": "P0", "code": "visual_review_checks_redefined"})

    reviewer = payload.get("reviewer") or {}
    reviewer_id = str(reviewer.get("id") or "").strip()
    reviewer_run = str(reviewer.get("runId") or "").strip()
    reviewer_type = str(reviewer.get("type") or "").strip()
    if len(reviewer_id) < 3 or not reviewer_run:
        findings.append({"severity": "P0", "code": "visual_reviewer_unidentified"})
    if reviewer_type not in ALLOWED_REVIEW_TYPES:
        findings.append({"severity": "P0", "code": "visual_review_not_human_or_visual_agent"})
    if reviewer_run and reviewer_run == generator_run_id:
        findings.append({"severity": "P0", "code": "visual_review_self_certified"})
    if expected_reviewer_run_id and reviewer_run != expected_reviewer_run_id:
        findings.append({"severity": "P0", "code": "visual_review_wrong_reviewer_run"})

    rendered = _rendered_page_map(rendered_pages)
    entries = payload.get("pages") or []
    if not isinstance(entries, list):
        entries = []
    expected_numbers = list(range(1, len(rendered) + 1))
    actual_numbers = [entry.get("page") for entry in entries if isinstance(entry, dict)]
    if payload.get("pageCount") != len(rendered) or actual_numbers != expected_numbers:
        findings.append({"severity": "P0", "code": "visual_review_incomplete_page_set"})

    verified_pages = []
    for number in expected_numbers:
        entry = entries[number - 1] if number - 1 < len(entries) and isinstance(entries[number - 1], dict) else {}
        rendered_entry = rendered.get(number) or {}
        image_path = Path(str(rendered_entry.get("imagePath") or ""))
        expected_hash = rendered_entry.get("imageSha256")
        if not image_path.is_file() or sha256_file(image_path) != expected_hash:
            findings.append({"severity": "P0", "code": "rendered_page_evidence_tampered", "page": number})
        if entry.get("reviewedImageSha256") != expected_hash:
            findings.append({"severity": "P0", "code": "visual_review_wrong_page_image", "page": number})
        if entry.get("status") != "pass":
            findings.append({"severity": "P0", "code": "visual_page_not_approved", "page": number})
        checks = entry.get("checks") or {}
        if set(checks) != set(REQUIRED_PAGE_CHECKS) or any(checks.get(name) is not True for name in REQUIRED_PAGE_CHECKS):
            findings.append({"severity": "P0", "code": "visual_page_checks_incomplete", "page": number})
        verified_pages.append({
            "page": number,
            "reviewedImageSha256": entry.get("reviewedImageSha256"),
            "status": entry.get("status"),
            "checks": checks,
            "notes": str(entry.get("notes") or ""),
        })

    if payload.get("approved") is not True:
        findings.append({"severity": "P0", "code": "visual_review_not_attested"})
    return {
        "approved": not findings,
        "reviewPath": str(review_path),
        "reviewSha256": sha256_file(review_path),
        "reviewer": reviewer,
        "reviewedAt": payload.get("reviewedAt"),
        "reviewMethod": payload.get("reviewMethod"),
        "pages": verified_pages,
        "findings": findings,
    }

