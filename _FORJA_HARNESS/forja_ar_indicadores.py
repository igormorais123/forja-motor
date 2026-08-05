"""Painel determinístico de indicadores do FORJA AUTO-RESEARCH."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

SCHEMA = "FORJA-AR-v1"
ROOT = Path(__file__).resolve().parent
DEFAULT_CACHE = ROOT / "autoresearch" / "cache"
DEFAULT_MANIFEST = ROOT / "autoresearch" / "AR_MANIFEST.json"
FIXED_TIME = "1970-01-01T00:00:00Z"


def _canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha(value: bytes | str) -> str:
    return hashlib.sha256(value.encode("utf-8") if isinstance(value, str) else value).hexdigest()


def _null(reason: str, evidence: list | None = None) -> dict:
    return {"valor": None, "evidencia": evidence or [], "motivo_null": reason}


def _entries(context: dict, name: str) -> list[dict] | None:
    value = context.get(name)
    if not isinstance(value, list):
        return None
    return [item for item in value if isinstance(item, dict)]


def _terms(item: dict, *keys: str) -> list[str]:
    values: list[str] = []
    for key in keys:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            values.append(value.strip())
        elif isinstance(value, list):
            values.extend(str(part).strip() for part in value if str(part).strip())
    return values


def _contains(text: str, terms: list[str]) -> bool:
    folded = text.casefold()
    return any(term.casefold() in folded for term in terms if term)


def _sensor_versions() -> dict[str, str]:
    versions = {}
    for name in ("forja_verificador.py", "forja_metricas_f7.py", "forja_estilo_humano.py", "forja_human_review.py"):
        path = ROOT / name
        versions[name] = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "ausente"
    return versions


def _i1(text: str, context: dict) -> dict:
    ledger = _entries(context, "authorities_ledger")
    if ledger is None:
        return _null("ledger_ausente")
    required = [item for item in ledger if item.get("required", True)]
    if not required:
        return _null("ledger_vazio")
    try:
        from forja_metricas_f7 import extrair_citacoes_basico

        extracted = extrair_citacoes_basico(text)
    except Exception as exc:
        return _null(f"sensor_indisponivel:{type(exc).__name__}")

    def cited_by_sensor(item: dict) -> bool:
        terms = _terms(item, "rotulo", "label", "numero", "aliases")
        if _contains(text, terms):
            return True
        wanted = {term.casefold().replace(".", "") for term in terms}
        return any(
            str(citation.get("numero", "")).casefold().replace(".", "") in wanted
            or str(citation.get("rótulo", "")).casefold().replace(".", "") in wanted
            for citation in extracted
        )

    cited = [item for item in required if cited_by_sensor(item)]
    verified = [item for item in cited if item.get("verified") is True or item.get("conferida") is True]
    return {
        "valor": len(cited) / len(required),
        "cobertura": len(cited) / len(required),
        "correcao": len(verified) / len(cited) if cited else 0.0,
        "evidencia": {"obrigatorias": len(required), "citadas": len(cited), "conferidas": len(verified)},
    }


def _i3(text: str, context: dict) -> dict:
    ledger = _entries(context, "claims_ledger")
    if ledger is None:
        return _null("ledger_ausente")
    decisive = [item for item in ledger if item.get("required", True) and not item.get("issueOnly", False)]
    if not decisive:
        return _null("ledger_vazio")
    covered, grounded = [], []
    for item in decisive:
        claim_terms = _terms(item, "claim", "rotulo", "aliases")
        anchors = _terms(item, "anchor", "anchors")
        present = _contains(text, claim_terms)
        if present:
            covered.append(item)
            if anchors and _contains(text, anchors):
                grounded.append(item)
    return {
        "valor": len(grounded) / len(decisive),
        "cobertura": len(covered) / len(decisive),
        "correcao": len(grounded) / len(covered) if covered else 0.0,
        "evidencia": {"decisivas": len(decisive), "presentes": len(covered), "lastreadas": len(grounded)},
    }


def _i7(text: str, context: dict) -> dict:
    issues = _entries(context, "issue_ledger")
    if issues is None:
        claims = _entries(context, "claims_ledger")
        issues = [item for item in (claims or []) if item.get("issue") or item.get("issueOnly")]
    if not issues:
        return _null("ledger_ausente")
    entailed = []
    for item in issues:
        issue_terms = _terms(item, "issue", "claim", "rotulo")
        anchors = _terms(item, "anchor", "anchors", "requiredTerms")
        if _contains(text, issue_terms) and anchors and _contains(text, anchors):
            entailed.append(item)
    return {
        "valor": len(entailed) / len(issues),
        "cobertura": len(entailed) / len(issues),
        "evidencia": {"issues": len(issues), "vinculados": len(entailed)},
    }


def _i8(context: dict) -> dict:
    visual = context.get("visual_qa")
    if not isinstance(visual, dict):
        return _null("qa_visual_ausente")
    critical = visual.get("criticalDefects")
    if not isinstance(critical, int):
        return _null("qa_visual_incompleto")
    if visual.get("synthetic") is True:
        approved = visual.get("receiptApproved")
        if not isinstance(approved, bool):
            return _null("qa_visual_incompleto")
        receipt_evidence = "recibo_sintetico_de_teste"
    else:
        receipt_path = visual.get("receiptPath")
        expected = visual.get("receiptExpected")
        if not receipt_path or not isinstance(expected, dict):
            return _null("recibo_visual_ausente")
        try:
            from forja_human_review import validate_visual_review_receipt

            validation = validate_visual_review_receipt(
                Path(str(receipt_path)),
                expected=expected,
                trust_store_path=Path(visual["trustStorePath"]) if visual.get("trustStorePath") else None,
                trust_store_pin_path=Path(visual["trustStorePinPath"]) if visual.get("trustStorePinPath") else None,
            )
            approved = bool(validation.get("approved"))
            receipt_evidence = validation.get("receiptSha256")
        except Exception as exc:
            return _null(f"sensor_indisponivel:{type(exc).__name__}")
    return {
        "valor": 1.0 if critical == 0 and approved else 0.0,
        "aprovado": critical == 0 and approved,
        "violacoes": critical,
        "evidencia": {
            "criticalDefects": critical,
            "receiptApproved": approved,
            "receiptEvidence": receipt_evidence,
        },
    }


def computar_indicadores(md_texto: str, contexto: dict | None = None) -> dict:
    """Computa I1–I10; falha de sensor vira null motivado."""
    contexto = contexto or {}
    indicators: dict[str, dict] = {}
    try:
        from forja_verificador import verificar

        violations = verificar(md_texto, "peca")
        integrity = [v for v in violations if str(v.get("gate", "")).startswith(("G3-", "G4-", "G5-"))]
        placeholders = [v for v in violations if str(v.get("gate", "")).startswith("G2-")]
        origin = [v for v in violations if str(v.get("gate", "")).startswith("G9-")]
        indicators["I2"] = {
            "valor": 1.0 if not integrity else 0.0,
            "aprovado": not integrity,
            "violacoes": len(integrity),
            "evidencia": integrity,
        }
        indicators["I4"] = {
            "valor": 1.0 if not placeholders else 0.0,
            "aprovado": not placeholders,
            "violacoes": len(placeholders),
            "evidencia": placeholders,
        }
        indicators["I6"] = {
            "valor": 1.0 if not origin else 0.0,
            "aprovado": not origin,
            "violacoes": len(origin),
            "evidencia": origin,
        }
    except Exception as exc:
        for ident in ("I2", "I4", "I6"):
            indicators[ident] = _null(f"sensor_indisponivel:{type(exc).__name__}")
    try:
        # A assinatura viva é relatorio(texto, tipo), não um score 0–100.
        from forja_estilo_humano import relatorio

        style = relatorio(md_texto, "peca")
        indicators["I5"] = {
            "valor": 1.0 if style["aprovado"] else 0.0,
            "aprovado": style["aprovado"],
            "p0": style["p0"],
            "p1": style["p1"],
            "evidencia": style["achados"],
        }
    except Exception as exc:
        indicators["I5"] = _null(f"sensor_indisponivel:{type(exc).__name__}")
    indicators["I1"] = _i1(md_texto, contexto)
    indicators["I3"] = _i3(md_texto, contexto)
    indicators["I7"] = _i7(md_texto, contexto)
    indicators["I8"] = _i8(contexto)
    indicators["I9"] = _null("julgamento_cego_ausente")
    indicators["I10"] = _null("pos_entrega_ausente")
    return {
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": str(contexto.get("producerRunId") or "forja-ar-indicadores"),
        "artifactSha256": _sha(md_texto),
        "sensorVersions": _sensor_versions(),
        "indicadores": {key: indicators[key] for key in sorted(indicators)},
    }


def comparar(baseline: dict, variante: dict, manifest: dict | None = None) -> dict:
    """Aplica máscara pareada; novo null bloqueia e nunca renormaliza."""
    manifest = manifest or {}
    base = baseline.get("indicadores", baseline)
    var = variante.get("indicadores", variante)
    mask = [key for key in sorted(base) if isinstance(base.get(key), dict) and base[key].get("valor") is not None]
    new_null = [key for key in mask if not isinstance(var.get(key), dict) or var[key].get("valor") is None]
    margins = ((manifest.get("margens") or {}).get("ruido_por_indicador") or {})
    roles = {
        item.get("id"): item.get("papel")
        for item in (manifest.get("indicadores") or [])
        if isinstance(item, dict)
    }
    regressions = []
    vetoes = []
    deltas = {}
    for key in mask:
        if key in new_null:
            continue
        left, right = float(base[key]["valor"]), float(var[key]["valor"])
        delta = right - left
        deltas[key] = delta
        margin = float(margins.get(key, 0.0))
        if roles.get(key) == "alvo" and delta < -margin:
            regressions.append(key)
        if roles.get(key) == "veto" and right < left:
            vetoes.append(key)
    blocked = bool(new_null or regressions or vetoes)
    return {
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": "forja-ar-comparison",
        "mascara": mask,
        "novoNull": new_null,
        "regressoes": regressions,
        "vetos": vetoes,
        "deltas": deltas,
        "bloqueio": "novo_null" if new_null else ("nao_inferioridade" if regressions else ("veto" if vetoes else None)),
        "aprovado": not blocked,
    }


def cache_key(md_texto: str, contexto: dict, sensor_versions: dict | None = None) -> str:
    """Produz chave content-addressed artifact+sensor+context."""
    payload = _sha(md_texto) + _sha(_canonical(sensor_versions or _sensor_versions())) + _sha(_canonical(contexto))
    return _sha(payload)


def computar_com_cache(md_texto: str, contexto: dict, cache_dir: Path = DEFAULT_CACHE) -> tuple[dict, bool]:
    """Lê ou grava cache sem depender de relógio."""
    key = cache_key(md_texto, contexto)
    path = Path(cache_dir) / f"{key}.json"
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8", errors="replace")), True
    result = computar_indicadores(md_texto, contexto)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result, False


def _load_ledgers(directory: Path | None) -> dict:
    if not directory:
        return {}
    context = {}
    for key, names in {
        "claims_ledger": ("claims_ledger.json", "CLAIMS_LEDGER.json"),
        "authorities_ledger": ("authorities_ledger.json", "AUTHORITIES_LEDGER.json"),
        "issue_ledger": ("issue_ledger.json", "ISSUE_LEDGER.json"),
        "visual_qa": ("visual_qa.json", "VISUAL_QA.json"),
    }.items():
        for name in names:
            path = directory / name
            if path.is_file():
                context[key] = json.loads(path.read_text(encoding="utf-8", errors="replace"))
                break
    return context


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Indicadores do FORJA AUTO-RESEARCH")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--md", type=Path)
    action.add_argument("--comparar", nargs=2, type=Path)
    action.add_argument("--caso")
    action.add_argument("--painel", action="store_true")
    parser.add_argument("--ledgers", type=Path)
    parser.add_argument("--split", choices=("train", "holdout"))
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args(argv)
    try:
        if args.md:
            text = args.md.read_text(encoding="utf-8", errors="replace")
            result = computar_indicadores(text, _load_ledgers(args.ledgers))
        elif args.comparar:
            left = json.loads(args.comparar[0].read_text(encoding="utf-8", errors="replace"))
            right = json.loads(args.comparar[1].read_text(encoding="utf-8", errors="replace"))
            manifest = json.loads(args.manifest.read_text(encoding="utf-8", errors="replace"))
            result = comparar(left, right, manifest)
        else:
            raise ValueError("--caso/--painel requerem corpus materializado pelo operador")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("aprovado", True) else 1
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
