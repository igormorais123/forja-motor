"""Cross-artifact consistency and delivery-integrity checks for FORJA N4."""

from __future__ import annotations

import argparse
import ast
import json
import operator
import re
from pathlib import Path

from forja_n3_common import resolve_case_dir, sha256_file
from forja_n4_common import ids_unique, issue, validate_file


def inspect_physical_document(
    *,
    docx_path: Path,
    pdf_path: Path,
    f8_path: Path,
    layout_profile_id: str,
    expected_docx_hash: str | None = None,
    expected_pdf_hash: str | None = None,
) -> dict:
    """Measure final-file identity and metadata after the last render."""
    from docx import Document
    import fitz

    profiles_path = Path(__file__).parent / "n4_schemas" / "N4_LAYOUT_PROFILES.json"
    profiles = json.loads(profiles_path.read_text(encoding="utf-8"))
    profile = (profiles.get("profiles") or {}).get(layout_profile_id)
    findings = []
    docx_hash = sha256_file(docx_path) if docx_path.is_file() else None
    pdf_hash = sha256_file(pdf_path) if pdf_path.is_file() else None
    if not docx_hash or not pdf_hash:
        findings.append({"code": "FINAL_FILE_MISSING", "severity": "p0", "status": "open", "detail": "DOCX ou PDF final ausente"})
    if expected_docx_hash and docx_hash != expected_docx_hash:
        findings.append({"code": "DOCX_HASH_STALE", "severity": "p0", "status": "open", "detail": "hash DOCX registrado diverge do disco"})
    if expected_pdf_hash and pdf_hash != expected_pdf_hash:
        findings.append({"code": "PDF_HASH_STALE", "severity": "p0", "status": "open", "detail": "hash PDF registrado diverge do disco"})
    metadata = {}
    if docx_path.is_file():
        props = Document(docx_path).core_properties
        metadata["docx"] = {"author": props.author, "lastModifiedBy": props.last_modified_by}
        allowed = {str(value).casefold() for value in (profile or {}).get("allowedAuthors") or []}
        for field, value in metadata["docx"].items():
            if value and allowed and str(value).casefold() not in allowed:
                findings.append({"code": f"DOCX_{field.upper()}", "severity": "p0", "status": "open", "detail": f"metadado pessoal ou não autorizado: {value}"})
    if pdf_path.is_file():
        with fitz.open(pdf_path) as pdf:
            metadata["pdf"] = dict(pdf.metadata or {})
        author = str(metadata["pdf"].get("author") or "").strip()
        allowed = {str(value).casefold() for value in (profile or {}).get("allowedAuthors") or []}
        if author and allowed and author.casefold() not in allowed:
            findings.append({"code": "PDF_AUTHOR", "severity": "p0", "status": "open", "detail": f"autor PDF não autorizado: {author}"})
    f8 = json.loads(f8_path.read_text(encoding="utf-8-sig")) if f8_path.is_file() else {}
    if not profile:
        findings.append({"code": "LAYOUT_PROFILE_UNKNOWN", "severity": "p0", "status": "open", "detail": f"perfil desconhecido: {layout_profile_id}"})
    elif profile.get("requiresIndependentVisualQa") and not (
        f8.get("approved") is True and f8.get("generatorRunId") and f8.get("reviewerRunId") and f8.get("generatorRunId") != f8.get("reviewerRunId")
    ):
        findings.append({"code": "LAYOUT_PROFILE_QA", "severity": "p0", "status": "open", "detail": "perfil visual sem QA independente aprovado"})
    return {
        "layoutProfileId": layout_profile_id,
        "files": {"docx": {"path": str(docx_path), "sha256": docx_hash}, "pdf": {"path": str(pdf_path), "sha256": pdf_hash}},
        "metadata": metadata,
        "f8": {"path": str(f8_path), "approved": f8.get("approved"), "generatorRunId": f8.get("generatorRunId"), "reviewerRunId": f8.get("reviewerRunId")},
        "findings": findings,
        "approved": not findings,
    }


COMPARISON_CLASSES = {
    "repeated_with_no_material_novelty", "repeated_with_new_basis", "new_issue_from_prior_decision",
    "legitimate_clarification", "possible_prequestioning", "not_comparable", "uncertain",
}


def validate_event_identity(payload: dict) -> list[dict]:
    events = payload.get("events") or []
    findings = ids_unique(events, "eventId", "N4-EVENT-ID")
    for event in events:
        eid = str(event.get("eventId") or "?")
        if not all(str(event.get(key) or "").strip() for key in ("canonicalLabel", "sourceId", "locator")):
            findings.append(issue("N4-EVENT-SOURCE", f"{eid}: identidade sem rótulo, fonte ou localizador"))
        overlap = set(event.get("allowedParaphrases") or []) & set(event.get("forbiddenEquivalents") or [])
        if overlap:
            findings.append(issue("N4-EVENT-OVERLAP", f"{eid}: formas simultaneamente permitidas e proibidas: {sorted(overlap)}"))
    for surface in payload.get("surfaces") or []:
        text = str(surface.get("text") or "")
        for event in events:
            for forbidden in event.get("forbiddenEquivalents") or []:
                if re.search(rf"(?<!\w){re.escape(str(forbidden))}(?!\w)", text, re.I) and not surface.get("semanticContrast"):
                    findings.append(issue("N4-EVENT-CONFLICT", f"{surface.get('surfaceId')}: {forbidden!r} conflita com {event.get('canonicalLabel')!r}"))
    return findings


def validate_comparison(payload: dict) -> list[dict]:
    findings = ids_unique(payload.get("comparisonSets") or [], "setId", "N4-CMP-SET")
    for group in payload.get("comparisonSets") or []:
        if len(group.get("documents") or []) < 2:
            findings.append(issue("N4-CMP-DOCS", f"{group.get('setId')}: comparação exige ao menos dois documentos"))
        findings += ids_unique(group.get("units") or [], "unitId", "N4-CMP-UNIT")
        for unit in group.get("units") or []:
            uid = str(unit.get("unitId") or "?")
            if unit.get("classification") not in COMPARISON_CLASSES:
                findings.append(issue("N4-CMP-CLASS", f"{uid}: classificação inválida"))
            if unit.get("classification") in {"repeated_with_no_material_novelty", "possible_prequestioning", "uncertain"} and unit.get("reviewStatus") != "confirmed":
                findings.append(issue("N4-CMP-REVIEW", f"{uid}: conclusão sensível exige revisão jurídica", severity="p1"))
            if unit.get("consequence") in {"bad_faith", "sanction", "fine"}:
                findings.append(issue("N4-CMP-AUTO-SANCTION", f"{uid}: comparação não pode gerar sanção automática"))
    return findings


def validate_intertemporal(payload: dict) -> list[dict]:
    items = payload.get("temporalIssues") if "temporalIssues" in payload else payload.get("issues") or []
    findings = ids_unique(items, "issueId", "N4-TEMP-ID")
    for item in items:
        iid = str(item.get("issueId") or "?")
        if item.get("triggeringDate") and not item.get("dateSourceId"):
            findings.append(issue("N4-TEMP-DATE-SOURCE", f"{iid}: data sem fonte"))
        if item.get("conclusion") and not item.get("transitionRuleSourceId"):
            findings.append(issue("N4-TEMP-RULE", f"{iid}: conclusão sem regra de transição"))
        if item.get("dateStatus") == "inferred" and item.get("status") == "confirmed":
            findings.append(issue("N4-TEMP-INFERENCE", f"{iid}: data inferida tratada como comprovada"))
    return findings


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def _eval_formula(formula: str, values: dict[str, float]) -> float:
    def walk(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.Name) and node.id in values:
            return float(values[node.id])
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](walk(node.left), walk(node.right))
        raise ValueError("fórmula contém operação não autorizada")
    return walk(ast.parse(formula, mode="eval"))


def validate_quantification(payload: dict) -> list[dict]:
    findings = ids_unique(payload.get("scenarios") or [], "scenarioId", "N4-QUANT-ID")
    for scenario in payload.get("scenarios") or []:
        sid = str(scenario.get("scenarioId") or "?")
        formula = str(scenario.get("formula") or "").strip()
        if not formula:
            if scenario.get("status") != "blocked" or not scenario.get("missingInputs"):
                findings.append(issue("N4-QUANT-FORMULA", f"{sid}: sem fórmula e sem bloqueio explícito"))
            continue
        known = scenario.get("knownInputs") or []
        if any(item.get("sourceId") is None for item in known):
            findings.append(issue("N4-QUANT-SOURCE", f"{sid}: entrada conhecida sem fonte"))
        values = {str(item.get("name")): float(item.get("value")) for item in known if isinstance(item.get("value"), (int, float))}
        disputed = scenario.get("disputedInputs") or []
        try:
            if disputed:
                lows = dict(values)
                highs = dict(values)
                for item in disputed:
                    bounds = item.get("range") or []
                    if len(bounds) != 2 or not item.get("basisIds"):
                        raise ValueError("intervalo sem duas extremidades fundamentadas")
                    lows[str(item.get("name"))] = float(bounds[0])
                    highs[str(item.get("name"))] = float(bounds[1])
                expected = sorted((_eval_formula(formula, lows), _eval_formula(formula, highs)))
                outputs = scenario.get("outputs") or {}
                actual = [float(outputs.get("minimum")), float(outputs.get("maximum"))]
                if any(abs(a - b) > 1e-6 for a, b in zip(actual, expected)):
                    findings.append(issue("N4-QUANT-OUTPUT", f"{sid}: faixa não corresponde à fórmula"))
            elif scenario.get("outputs", {}).get("value") is not None:
                expected = _eval_formula(formula, values)
                if abs(float(scenario["outputs"]["value"]) - expected) > 1e-6:
                    findings.append(issue("N4-QUANT-OUTPUT", f"{sid}: resultado não corresponde à fórmula"))
        except (TypeError, ValueError, ZeroDivisionError, SyntaxError) as exc:
            findings.append(issue("N4-QUANT-CALC", f"{sid}: {exc}"))
    return findings


def validate_delivery(payload: dict) -> list[dict]:
    findings = []
    if payload.get("packageHash") != payload.get("selectedHash") or payload.get("preSendMatch") is not True:
        findings.append(issue("N4-DELIVERY-PRESEND", "arquivo selecionado diverge do pacote auditado"))
    selected_path = Path(str(payload.get("selectedPath") or ""))
    if payload.get("selectedPath") and (not selected_path.is_file() or sha256_file(selected_path) != payload.get("selectedHash")):
        findings.append(issue("N4-DELIVERY-DISK", "hash selecionado diverge do arquivo em disco"))
    post = payload.get("postDeliveryVerification")
    if isinstance(post, dict):
        mode = post.get("mode")
        if mode == "channel_hash":
            if not post.get("deliveredHash") or post.get("deliveredHash") != payload.get("selectedHash"):
                findings.append(issue("N4-DELIVERY-CHANNEL-HASH", "hash entregue ausente ou divergente"))
        elif mode == "artifact_evidence":
            if not post.get("deliveryEvidenceId") or post.get("status") != "confirmed":
                findings.append(issue("N4-DELIVERY-EVIDENCE", "cadeia alternativa de entrega incompleta"))
        else:
            findings.append(issue("N4-DELIVERY-MODE", "modo de confirmação pós-entrega inválido"))
    return findings


def validate_global(payload: dict) -> list[dict]:
    findings = []
    for finding in payload.get("findings") or []:
        if finding.get("severity") == "p0" and finding.get("status") != "resolved":
            findings.append(issue("N4-GLOBAL-P0", str(finding.get("detail") or finding.get("code") or "P0 global")))
    layers = payload.get("layers") or {}
    evidence = payload.get("layerEvidence") or {}
    for layer in ("C1", "C2", "C3", "C4", "C5"):
        if layers.get(layer) not in {"pass", "not_applicable"}:
            findings.append(issue("N4-GLOBAL-LAYER", f"camada {layer} não aprovada"))
        elif layers.get(layer) == "pass" and payload.get("measurementContract") == "N4-MEASURED-v1":
            layer_evidence = evidence.get(layer) or {}
            checks = layer_evidence.get("checks") or []
            if not layer_evidence.get("measuredAt") or not checks:
                findings.append(issue("N4-GLOBAL-EVIDENCE", f"camada {layer} marcada como pass sem medição"))
            elif any(check.get("passed") is not True or not check.get("evidence") for check in checks):
                findings.append(issue("N4-GLOBAL-EVIDENCE-FAIL", f"camada {layer} possui verificação ausente ou reprovada"))
            elif any(not isinstance(check.get("evidenceData"), dict) or not check.get("evidenceData") for check in checks):
                findings.append(issue("N4-GLOBAL-EVIDENCE-DATA", f"camada {layer} sem dados estruturados reproduzíveis"))
    physical = payload.get("physicalIntegrity")
    if isinstance(physical, dict):
        for finding in physical.get("findings") or []:
            if finding.get("severity") == "p0" and finding.get("status") != "resolved":
                findings.append(issue("N4-GLOBAL-PHYSICAL", str(finding.get("detail") or finding.get("code") or "integridade física")))
    return findings


VALIDATORS = {
    "F3_EVENT_IDENTITY.json": validate_event_identity,
    "F3_DOCUMENT_COMPARISON.json": validate_comparison,
    "F4_INTERTEMPORAL_MAP.json": validate_intertemporal,
    "F4_QUANTIFICATION_SCENARIOS.json": validate_quantification,
    "F7_GLOBAL_CONSISTENCY.json": validate_global,
    "F9_DELIVERY_SELECTION.json": validate_delivery,
    "F10_DELIVERY_INTEGRITY.json": validate_delivery,
}


def validate_case(case_dir: Path) -> dict:
    findings = []
    for filename, validator in VALIDATORS.items():
        _, current = validate_file(case_dir, filename, validator)
        findings.extend(current)
    return {"approved": not any(x["severity"] == "p0" for x in findings), "findings": findings}


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida consistência global FORJA N4")
    parser.add_argument("case")
    args = parser.parse_args()
    print(json.dumps(validate_case(resolve_case_dir(args.case)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
