"""Ciclo, promoção e log encadeado do FORJA AUTO-RESEARCH."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import statistics
import sys
from pathlib import Path

from forja_ar_corpus import ROOT, secrets_dir

SCHEMA = "FORJA-AR-v1"
FIXED_TIME = "1970-01-01T00:00:00Z"
MODULES = (
    "forja_ar_corpus.py",
    "forja_ar_indicadores.py",
    "forja_ar_canarios.py",
    "forja_ar_runpair.py",
    "forja_ar_blind.py",
    "forja_ar_ciclo.py",
)
SENSORS = (
    "forja_verificador.py",
    "forja_metricas_f7.py",
    "forja_estilo_humano.py",
    "forja_mutation_semantic.py",
    "forja_human_review.py",
)


def _canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha_file(path: Path) -> str:
    return _sha_bytes(path.read_bytes())


def append_log(log_path: Path, ciclo: str, acao: str, inputs, resultado) -> dict:
    """Acrescenta evento hash-linked sem usar relógio em decisão."""
    events = []
    if Path(log_path).is_file():
        events = [
            json.loads(line)
            for line in Path(log_path).read_text(encoding="utf-8", errors="replace").splitlines()
            if line.strip()
        ]
    event = {
        "seq": len(events) + 1,
        "prevHash": events[-1]["eventHash"] if events else "0" * 64,
        "ts": FIXED_TIME,
        "ciclo": ciclo,
        "acao": acao,
        "inputsHash": _sha_bytes(_canonical(inputs)),
        "resultado": resultado,
    }
    event["eventHash"] = _sha_bytes(_canonical(event))
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    with Path(log_path).open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    return event


def verify_log(log_path: Path) -> list[str]:
    """Reconstrói sequência, prevHash e hash de cada evento."""
    errors = []
    previous = "0" * 64
    for index, line in enumerate(Path(log_path).read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"linha inválida: {index}")
            continue
        if event.get("seq") != index:
            errors.append(f"sequência inválida: {index}")
        if event.get("prevHash") != previous:
            errors.append(f"prevHash inválido: {index}")
        claimed = event.get("eventHash")
        unsigned = {key: value for key, value in event.items() if key != "eventHash"}
        actual = _sha_bytes(_canonical(unsigned))
        if claimed != actual:
            errors.append(f"eventHash inválido: {index}")
        previous = str(claimed)
    return errors


def snapshot(
    cycle_dir: Path,
    manifest_path: Path,
    *,
    corpus_path: Path | None = None,
    log_path: Path | None = None,
) -> Path:
    """Congela pré-registro, código, sensores e corpus antes da medição."""
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8", errors="replace"))
    if manifest.get("schemaVersion") != SCHEMA:
        raise ValueError("AR_MANIFEST usa schema desconhecido")
    for required in ("indicadores", "margens", "orcamentos"):
        if required not in manifest:
            raise ValueError(f"pré-registro incompleto: {required}")
    frozen = {
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": f"snapshot-{Path(cycle_dir).name}",
        "preregister": manifest,
        "preregisterHash": _sha_file(Path(manifest_path)),
        "codeHashes": {name: _sha_file(ROOT / name) for name in MODULES},
        "sensorVersions": {name: _sha_file(ROOT / name) for name in SENSORS},
        "corpusHash": _sha_file(corpus_path) if corpus_path and corpus_path.is_file() else None,
    }
    cycle_dir = Path(cycle_dir)
    cycle_dir.mkdir(parents=True, exist_ok=True)
    output = cycle_dir / "AR_CICLO_MANIFEST.json"
    output.write_text(json.dumps(frozen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if log_path:
        append_log(log_path, cycle_dir.name, "snapshot", frozen, {"status": "snapshot_created"})
    return output


def _load_required(path: Path | None, name: str, errors: list[str]) -> dict:
    if not path or not Path(path).is_file():
        errors.append(f"artefato_ausente:{name}")
        return {}
    try:
        return json.loads(Path(path).read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        errors.append(f"artefato_invalido:{name}")
        return {}


def consume_sealed(version: str, limit: int, evaluation: dict | None = None) -> tuple[bool, str]:
    """Debita orçamento vitalício externo, nunca por ciclo.

    Débito exige avaliação REAL do caso elegível (gap v1 nº 1, ciclo AR-1): sem um
    resultado de avaliação vinculado ao próprio caso que será aposentado, nada é debitado.
    """
    path = secrets_dir(create=True) / "sealed_registry.json"
    if not path.is_file():
        return False, "sealed_registry_ausente"
    registry = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    versions = registry.setdefault("versions", {})
    entry = versions.setdefault(version, {"used": 0, "eligible": []})
    if int(entry.get("used", 0)) >= int(limit):
        return False, "sealed_orcamento_vitalicio_esgotado"
    if not entry.get("eligible"):
        return False, "sealed_sem_caso_elegivel"
    if not isinstance(evaluation, dict) or not evaluation.get("caseId") or not isinstance(evaluation.get("aprovado"), bool):
        return False, "sealed_sem_avaliacao"
    next_case = entry["eligible"][0]
    if str(evaluation["caseId"]) != str(next_case):
        return False, "sealed_avaliacao_caso_divergente"
    entry["used"] = int(entry.get("used", 0)) + 1
    entry["retired"] = list(entry.get("retired") or []) + [entry["eligible"].pop(0)]
    entry.setdefault("evaluations", {})[str(next_case)] = _sha_bytes(_canonical(evaluation))
    registry.update({"schemaVersion": SCHEMA, "generatedAt": FIXED_TIME})
    path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True, "sealed_debitado"


def promotion(
    cycle_dir: Path,
    manifest_path: Path,
    *,
    comparison_path: Path | None,
    canary_path: Path | None,
    judgment_path: Path | None,
    use_sealed: bool = True,
    variant_sha: str | None = None,
    sealed_eval_path: Path | None = None,
) -> dict:
    """Avalia gates e nunca emite acima de technical_candidate_passed.

    Sem sealed consultado o teto é `estudo_descritivo` (gap v1 nº 1); o vencedor do
    julgamento por hash tem de ser a VARIANTE (gap v1 nº 2, ciclo AR-2).
    """
    errors: list[str] = []
    frozen_path = Path(cycle_dir) / "AR_CICLO_MANIFEST.json"
    frozen = _load_required(frozen_path, "snapshot", errors)
    if frozen and frozen.get("preregisterHash") != _sha_file(Path(manifest_path)):
        errors.append("manifest_editado_pos_resultado")
    comparison = _load_required(comparison_path, "comparacao", errors)
    canary = _load_required(canary_path, "canarios", errors)
    judgment = _load_required(judgment_path, "julgamento", errors)
    if comparison and not comparison.get("aprovado"):
        errors.append("nao_inferioridade_reprovada")
    if canary and not canary.get("allPass"):
        errors.append("canarios_reprovados")
    prereg = frozen.get("preregister") or {}
    if canary and not isinstance(canary.get("secret"), dict):
        errors.append("canarios_secretos_ausentes")
    elif canary and not canary["secret"].get("allPass"):
        errors.append("canarios_secretos_reprovados")
    budgets = prereg.get("orcamentos") or {}
    candidates_used = int(comparison.get("candidatesUsed", 0)) if comparison else 0
    holdout_used = int(comparison.get("holdoutQueriesUsed", 0)) if comparison else 0
    judgments_used = len(judgment.get("votes") or []) if judgment else 0
    if candidates_used > int(budgets.get("candidatos_por_holdout", 0)):
        errors.append("orcamento_candidatos_excedido")
    if holdout_used > int(budgets.get("consultas_holdout", 0)):
        errors.append("orcamento_holdout_excedido")
    if judgments_used > int(budgets.get("julgamentos_llm_max", 0)):
        errors.append("orcamento_julgamentos_excedido")
    min_kappa = float((prereg.get("blind") or {}).get("kappaMin", 0.0))
    max_positional = int((prereg.get("blind") or {}).get("positionalInvalidationsMax", 0))
    if judgment:
        if not judgment.get("valid"):
            errors.append("julgamento_invalido")
        if judgment.get("kappa") is None or float(judgment["kappa"]) < min_kappa:
            errors.append("kappa_abaixo_minimo")
        if int(judgment.get("positionalInvalidations", 0)) > max_positional:
            errors.append("vies_posicional_acima_limite")
        winner = judgment.get("winnerArtifactSha256")
        if not variant_sha:
            errors.append("variante_sha_ausente")
        elif not winner or str(winner) != str(variant_sha):
            errors.append("vencedor_nao_e_variante")
    sealed_status = "nao_consultado"
    if not errors and use_sealed:
        budget = int((prereg.get("orcamentos") or {}).get("consultas_sealed_vitalicio", 0))
        version = str(prereg.get("holdoutVersion") or "v0")
        evaluation = None
        if sealed_eval_path and Path(sealed_eval_path).is_file():
            try:
                evaluation = json.loads(Path(sealed_eval_path).read_text(encoding="utf-8", errors="replace"))
            except json.JSONDecodeError:
                evaluation = None
        ok, sealed_status = consume_sealed(version, budget, evaluation)
        if not ok:
            errors.append(sealed_status)
    if errors:
        status = (
            "estudo_descritivo"
            if errors == ["sealed_registry_ausente"] or "sealed_sem_caso_elegivel" in errors
            else "blocked"
        )
    elif not use_sealed:
        status = "estudo_descritivo"
    else:
        status = "technical_candidate_passed"
    return {
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": f"promotion-{Path(cycle_dir).name}",
        "status": status,
        "errors": errors,
        "sealed": sealed_status,
        "budgetUse": {
            "candidates": candidates_used,
            "holdoutQueries": holdout_used,
            "judgments": judgments_used,
        },
    }


def independent_review(decision_path: Path, opinion_path: Path, family: str, generator_family: str) -> dict:
    """Registra revisão independente somente entre famílias distintas."""
    if family == generator_family:
        raise ValueError("revisor pertence à família geradora")
    decision = json.loads(Path(decision_path).read_text(encoding="utf-8", errors="replace"))
    if decision.get("status") != "technical_candidate_passed":
        raise ValueError("candidato técnico ainda não aprovado")
    if not Path(opinion_path).read_text(encoding="utf-8", errors="replace").strip():
        raise ValueError("parecer independente vazio")
    return {
        "schemaVersion": SCHEMA,
        "status": "independent_review_passed",
        "decisionSha256": _sha_file(Path(decision_path)),
        "opinionSha256": _sha_file(Path(opinion_path)),
        "reviewFamily": family,
    }


def human_approve(decision_path: Path, receipt_path: Path) -> dict:
    """Valida recibo Ed25519 vivo, vinculado ao hash da decisão AR."""
    decision_hash = _sha_file(Path(decision_path))
    receipt = json.loads(Path(receipt_path).read_text(encoding="utf-8", errors="replace"))
    expected = {"arPromotionHash": decision_hash}
    # Divergência viva: o sensor possui recibos claim/visual, não tipo promotion.
    # A extensão assinada arPromotionHash preserva a trilha existente sem forjar API.
    if receipt.get("reviewPurpose") == "all_pages_visual_layout_review":
        from forja_human_review import validate_visual_review_receipt

        validated = validate_visual_review_receipt(Path(receipt_path), expected=expected)
    elif receipt.get("reviewPurpose") == "jurisprudence_claim_entailment":
        from forja_human_review import validate_claim_review_receipt

        validated = validate_claim_review_receipt(Path(receipt_path), expected=expected)
    else:
        raise ValueError("recibo não pertence a contrato Ed25519 conhecido")
    if not validated.get("approved"):
        raise ValueError("recibo humano inválido: " + "; ".join(validated.get("findings") or []))
    return {
        "schemaVersion": SCHEMA,
        "status": "human_promotion_approved",
        "decisionSha256": decision_hash,
        "receiptSha256": validated["receiptSha256"],
    }


def cluster_interval(values_by_lineage: dict[str, list[float]], corpus_hash: str, samples: int = 400) -> dict:
    """Bootstrap simples por linhagem com seed derivada do corpus."""
    lineages = sorted(values_by_lineage)
    flat = [v for lineage in lineages for v in values_by_lineage[lineage]]
    if not flat:
        return {"mean": None, "low": None, "high": None, "lineages": 0, "warning": "sem_dados"}
    rng = random.Random(int((corpus_hash or "0" * 64)[:16], 16))
    means = []
    for _ in range(samples):
        selected = [lineages[rng.randrange(len(lineages))] for _ in lineages]
        sample = [v for lineage in selected for v in values_by_lineage[lineage]]
        means.append(statistics.fmean(sample))
    means.sort()
    return {
        "mean": statistics.fmean(flat),
        "low": means[int(0.025 * (len(means) - 1))],
        "high": means[int(0.975 * (len(means) - 1))],
        "lineages": len(lineages),
        "warning": "n_menor_10_intervalo_indicativo" if len(lineages) < 10 else None,
    }


def relatorio(cycle_dir: Path, panel_path: Path, output_path: Path | None = None) -> Path:
    """Publica relatório descritivo com missingness, sigma e intervalo por linhagem."""
    cycle_dir = Path(cycle_dir)
    frozen = json.loads(
        (cycle_dir / "AR_CICLO_MANIFEST.json").read_text(encoding="utf-8", errors="replace")
    )
    panel = json.loads(Path(panel_path).read_text(encoding="utf-8", errors="replace"))
    rows = panel.get("cases") or panel.get("rows") or []
    identifiers = [str(item.get("id")) for item in (frozen.get("preregister", {}).get("indicadores") or [])]
    lines = [
        "# Relatório FORJA AUTO-RESEARCH — estudo descritivo",
        "",
        "**Declaração obrigatória:** este piloto não demonstra eficácia e não autoriza promoção.",
        "",
        "| Indicador | N | Missingness | Sigma | Média | IC cluster 95% |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for ident in identifiers:
        values_by_lineage: dict[str, list[float]] = {}
        total = len(rows)
        observed = []
        for row in rows:
            indicator = (row.get("indicadores") or {}).get(ident) or {}
            value = indicator.get("valor")
            if isinstance(value, (int, float)):
                lineage = str(row.get("lineageId") or row.get("caseId") or "sem-linhagem")
                values_by_lineage.setdefault(lineage, []).append(float(value))
                observed.append(float(value))
        interval = cluster_interval(values_by_lineage, str(frozen.get("corpusHash") or "0" * 64))
        missing = (total - len(observed)) / total if total else 1.0
        sigma = statistics.pstdev(observed) if len(observed) > 1 else 0.0 if observed else None
        mean = statistics.fmean(observed) if observed else None
        sigma_text = f"{sigma:.4f}" if sigma is not None else "n/d"
        mean_text = f"{mean:.4f}" if mean is not None else "n/d"
        ci = (
            f"{interval['low']:.4f}–{interval['high']:.4f}"
            if interval["low"] is not None
            else "n/d"
        )
        lines.append(
            f"| {ident} | {len(observed)} | {missing:.2%} | "
            f"{sigma_text} | {mean_text} | {ci} |"
        )
    lines += [
        "",
        "## Efeito mínimo detectável",
        "",
        "Não estimado inferencialmente nesta coorte inicial; requer número prospectivo de linhagens e variância estável.",
        "",
        "## Orçamentos",
        "",
        "Os consumos devem ser lidos dos manifests e do registro sealed externo; ausência bloqueia promoção.",
    ]
    output = output_path or cycle_dir / f"AR_{cycle_dir.name.upper().replace('-', '_')}_RELATORIO.md"
    Path(output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return Path(output)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Ciclo FORJA AUTO-RESEARCH")
    sub = parser.add_subparsers(dest="command", required=True)
    verify = sub.add_parser("verify-log")
    verify.add_argument("--log", type=Path, required=True)
    snap = sub.add_parser("snapshot")
    snap.add_argument("--cycle-dir", type=Path, required=True)
    snap.add_argument("--manifest", type=Path, required=True)
    snap.add_argument("--corpus", type=Path)
    snap.add_argument("--log", type=Path)
    promote = sub.add_parser("promotion")
    promote.add_argument("--cycle-dir", type=Path, required=True)
    promote.add_argument("--manifest", type=Path, required=True)
    promote.add_argument("--comparison", type=Path)
    promote.add_argument("--canary", type=Path)
    promote.add_argument("--judgment", type=Path)
    promote.add_argument("--no-sealed", action="store_true")
    promote.add_argument("--variant-sha", help="sha256 canônico do output da VARIANTE (obrigatório com --judgment)")
    promote.add_argument("--sealed-eval", type=Path, help="JSON com avaliação real do caso sealed elegível ({caseId, aprovado, ...})")
    review = sub.add_parser("independent-review")
    review.add_argument("--decision", type=Path, required=True)
    review.add_argument("--parecer", type=Path, required=True)
    review.add_argument("--familia", required=True)
    review.add_argument("--familia-geradora", required=True)
    approve = sub.add_parser("human-approve")
    approve.add_argument("--decision", type=Path, required=True)
    approve.add_argument("--receipt", type=Path, required=True)
    report_cmd = sub.add_parser("relatorio")
    report_cmd.add_argument("--cycle-dir", type=Path, required=True)
    report_cmd.add_argument("--panel", type=Path, required=True)
    report_cmd.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "verify-log":
            errors = verify_log(args.log)
            result = {"schemaVersion": SCHEMA, "valid": not errors, "errors": errors}
        elif args.command == "snapshot":
            output = snapshot(args.cycle_dir, args.manifest, corpus_path=args.corpus, log_path=args.log)
            result = {"schemaVersion": SCHEMA, "snapshot": str(output)}
        elif args.command == "promotion":
            result = promotion(
                args.cycle_dir,
                args.manifest,
                comparison_path=args.comparison,
                canary_path=args.canary,
                judgment_path=args.judgment,
                use_sealed=not args.no_sealed,
                variant_sha=args.variant_sha,
                sealed_eval_path=args.sealed_eval,
            )
        elif args.command == "independent-review":
            result = independent_review(args.decision, args.parecer, args.familia, args.familia_geradora)
        elif args.command == "human-approve":
            result = human_approve(args.decision, args.receipt)
        else:
            output = relatorio(args.cycle_dir, args.panel, args.output)
            result = {"schemaVersion": SCHEMA, "report": str(output)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("valid", True) and result.get("status") != "blocked" else 2
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
