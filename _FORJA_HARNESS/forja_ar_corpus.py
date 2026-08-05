"""Registro determinístico do corpus do FORJA AUTO-RESEARCH."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

SCHEMA = "FORJA-AR-v1"
ROOT = Path(__file__).resolve().parent
DEFAULT_STATE = ROOT / "state"
DEFAULT_MANIFEST = ROOT / "autoresearch" / "AR_MANIFEST.json"
FIXED_TIME = "1970-01-01T00:00:00Z"


def _read_json(path: Path, fallback=None):
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return fallback


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def secrets_dir(*, create: bool = False) -> Path:
    """Resolve o diretório externo; cria somente quando uma operação o exige."""
    configured = os.environ.get("FORJA_AR_SECRETS_DIR")
    path = Path(configured).expanduser() if configured else Path.home() / ".forja_ar_secrets"
    if create and not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(
            f"Diretório de segredos AR criado sob demanda em {path}. "
            "Mantenha ar_hmac.key e sealed_registry.json fora do workspace.",
            file=sys.stderr,
        )
    return path


def load_hmac_key(*, create_dir: bool = True) -> bytes:
    """Lê a chave HMAC externa sem jamais imprimir seu conteúdo."""
    directory = secrets_dir(create=create_dir)
    key_path = directory / "ar_hmac.key"
    if not key_path.is_file():
        raise FileNotFoundError(
            f"chave HMAC ausente em {key_path}; crie um segredo de alta entropia nesse arquivo"
        )
    key = key_path.read_bytes().strip()
    if len(key) < 32:
        raise ValueError("ar_hmac.key deve conter ao menos 32 bytes")
    return key


def _fold(value: str) -> str:
    text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def derivar_linhagem(
    case_id: str,
    case_folder: str = "",
    equivalencias: dict | None = None,
) -> str:
    """Deriva linhagem estável, priorizando equivalência e identidade material."""
    equivalencias = equivalencias or {}
    if case_id in equivalencias:
        return str(equivalencias[case_id])
    if case_folder:
        normalized = _fold(str(case_folder).replace("\\", "/").rstrip("/").split("/")[-1])
        if normalized:
            return "folder-" + hashlib.sha256(normalized.encode()).hexdigest()[:20]
    base = re.sub(r"-(?:19)?[0-9a-f]{12,16}$", "", case_id.lower())
    return _fold(base)


def atribuir_split(lineage_id: str, key: bytes, split_config: dict | None = None) -> str:
    """Atribui split por HMAC; nenhum caseId isolado participa da decisão."""
    config = split_config or {}
    train_max = int(config.get("trainMax", 69))
    holdout_max = int(config.get("holdoutMax", 89))
    bucket = int.from_bytes(hmac.new(key, lineage_id.encode(), hashlib.sha256).digest()[:8], "big") % 100
    if bucket <= train_max:
        return "train"
    if bucket <= holdout_max:
        return "holdout"
    return "sealed"


def _case_metadata(case_dir: Path) -> dict:
    state = _read_json(case_dir / "FORJA_STATE.json", {}) or {}
    manifest = _read_json(case_dir / "FORJA_CASE_MANIFEST.json", {}) or {}
    inputs = state.get("inputs") if isinstance(state.get("inputs"), dict) else {}
    product = (
        manifest.get("produto")
        or manifest.get("product")
        or state.get("produto")
        or "nao_classificado"
    )
    tribunal = (
        manifest.get("tribunal")
        or state.get("tribunal")
        or next(
            (
                str(item.get("claim", "")).split(":", 1)[-1].strip()
                for item in (state.get("sourceLedger") or [])
                if isinstance(item, dict) and str(item.get("id", "")).startswith("src-trib-")
            ),
            "nao_classificado",
        )
    )
    return {
        "caseFolder": str(inputs.get("caseFolder") or ""),
        "produto": str(product),
        "tribunal": str(tribunal),
    }


def _artifact_candidates(case_dir: Path) -> list[tuple[int, Path, str]]:
    candidates: list[tuple[int, Path, str]] = []
    for path in case_dir.rglob("*.md"):
        rel = path.relative_to(case_dir)
        low = str(rel).replace("\\", "/").lower()
        if path.name.lower().startswith("final_markdown"):
            rank, kind = (0 if "n3_artifacts/" in low else 1), "final_markdown"
        elif path.name.lower() in {"audited_markdown.md", "draft_markdown.md"}:
            rank, kind = 2, path.stem
        elif re.search(r"(peticao|memoriais|minuta|parecer|impugnacao|contrarrazoes)", _fold(path.stem)):
            rank, kind = 3, "produto_markdown"
        elif path.name == "MAPA_IA.md" and path.parent == case_dir:
            # Divergência v1.1: o glob literal cobre 3/49. O mapa-raiz mantém
            # o inventário amplo, mas fica marcado metadata_only e não pontua.
            rank, kind = 9, "metadata_only"
        else:
            continue
        candidates.append((rank, path, kind))
    return sorted(candidates, key=lambda item: (item[0], str(item[1]).lower()))


def scan_corpus(
    state_dir: Path = DEFAULT_STATE,
    *,
    manifest: dict | None = None,
    key: bytes | None = None,
    sealed_sink: list[dict] | None = None,
) -> dict:
    """Escaneia o estado sem escrever nele e retorna inventário auditável."""
    manifest = manifest or _read_json(DEFAULT_MANIFEST, {}) or {}
    key = key or b"forja-ar-scan-only-key-not-for-production"
    equivalencias = manifest.get("linhagens") if isinstance(manifest.get("linhagens"), dict) else {}
    split_config = manifest.get("splits") if isinstance(manifest.get("splits"), dict) else {}
    raw_items = []
    for case_dir in sorted((p for p in Path(state_dir).iterdir() if p.is_dir()), key=lambda p: p.name):
        candidates = _artifact_candidates(case_dir)
        if not candidates:
            continue
        rank, artifact, kind = candidates[0]
        meta = _case_metadata(case_dir)
        lineage = derivar_linhagem(case_dir.name, meta["caseFolder"], equivalencias)
        stratum = f"{meta['produto']}×{meta['tribunal']}"
        item = {
            "caseId": case_dir.name,
            "lineageId": lineage,
            "produto": meta["produto"],
            "tribunal": meta["tribunal"],
            "stratum": stratum,
            "artifactPath": artifact.relative_to(ROOT).as_posix(),
            "artifactSha256": _sha256_file(artifact),
            "artifactKind": kind,
            "scoringEligible": kind != "metadata_only",
            "_proposedSplit": atribuir_split(lineage, key, split_config),
        }
        raw_items.append(item)

    # Mínimos são aplicados por linhagem e estrato, nunca por caseId.
    lineage_stratum = {}
    proposed = {}
    for item in raw_items:
        lineage = item["lineageId"]
        lineage_stratum.setdefault(lineage, item["stratum"])
        proposed.setdefault(lineage, item["_proposedSplit"])
    by_stratum: defaultdict[str, list[str]] = defaultdict(list)
    for lineage, stratum in lineage_stratum.items():
        by_stratum[stratum].append(lineage)
    assignments = dict(proposed)
    sealed_min = max(0, int(split_config.get("sealedMinPerStratum", 0)))
    holdout_min = max(0, int(split_config.get("holdoutMinPerStratum", 0)))
    for stratum, lineages in sorted(by_stratum.items()):
        ordered = sorted(
            set(lineages),
            key=lambda lineage: hmac.new(
                key,
                f"minimum:{stratum}:{lineage}".encode(),
                hashlib.sha256,
            ).digest(),
        )
        sealed_n = min(sealed_min, len(ordered))
        holdout_n = min(holdout_min, max(0, len(ordered) - sealed_n))
        for lineage in ordered[:sealed_n]:
            assignments[lineage] = "sealed"
        for lineage in ordered[sealed_n:sealed_n + holdout_n]:
            assignments[lineage] = "holdout"

    cases = []
    sealed_by_stratum: Counter[str] = Counter()
    for item in raw_items:
        split = assignments[item["lineageId"]]
        item.pop("_proposedSplit", None)
        if split == "sealed":
            sealed_by_stratum[item["stratum"]] += 1
            if sealed_sink is not None:
                sealed_sink.append({
                    "caseId": item["caseId"],
                    "lineageId": item["lineageId"],
                    "stratum": item["stratum"],
                    "artifactSha256": item["artifactSha256"],
                })
        else:
            item["split"] = split
            cases.append(item)
    cases.sort(key=lambda item: (item["lineageId"], item["caseId"]))
    return {
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": "forja-ar-corpus-scan",
        "eligibilityRule": (
            "final_markdown*; fallback auditado/produto; MAPA_IA raiz apenas metadata_only "
            "para cobrir o inventário real sem fabricar score"
        ),
        "cases": cases,
        "sealed": {
            "count": sum(sealed_by_stratum.values()),
            "byStratum": dict(sorted(sealed_by_stratum.items())),
        },
        "summary": {
            "eligible": len(cases) + sum(sealed_by_stratum.values()),
            "scoringEligible": sum(bool(item["scoringEligible"]) for item in raw_items),
            "train": sum(item.get("split") == "train" for item in cases),
            "holdout": sum(item.get("split") == "holdout" for item in cases),
            "sealed": sum(sealed_by_stratum.values()),
        },
    }


def register_sealed_inventory(items: list[dict], manifest: dict) -> Path:
    """Atualiza somente o inventário sealed externo, preservando consumo vitalício."""
    path = secrets_dir(create=True) / "sealed_registry.json"
    registry = _read_json(path, {}) or {}
    versions = registry.setdefault("versions", {})
    version = str(manifest.get("holdoutVersion") or "v0")
    entry = versions.setdefault(version, {"used": 0, "eligible": [], "retired": []})
    retired = set(entry.get("retired") or [])
    entry["eligible"] = sorted(
        item["artifactSha256"] for item in items if item["artifactSha256"] not in retired
    )
    entry["inventoryCommitment"] = hashlib.sha256(_canonical(items)).hexdigest()
    registry.update({
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": "forja-ar-corpus-sealed-registry",
    })
    path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def check_corpus(corpus: dict, root: Path = ROOT) -> list[str]:
    """Confere hashes e impede uma linhagem em splits distintos."""
    errors: list[str] = []
    by_lineage: defaultdict[str, set[str]] = defaultdict(set)
    for item in corpus.get("cases") or []:
        path = root / str(item.get("artifactPath") or "")
        if not path.is_file():
            errors.append(f"artefato ausente: {path}")
        elif _sha256_file(path) != item.get("artifactSha256"):
            errors.append(f"hash divergente: {path}")
        by_lineage[str(item.get("lineageId"))].add(str(item.get("split")))
    for lineage, splits in sorted(by_lineage.items()):
        if len(splits) > 1:
            errors.append(f"linhagem separada entre splits: {lineage} -> {sorted(splits)}")
    return errors


def report(corpus: dict) -> dict:
    """Resume distribuição sem expor identidades sealed."""
    strata: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for item in corpus.get("cases") or []:
        strata[str(item.get("stratum"))][str(item.get("split"))] += 1
    return {
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": "forja-ar-corpus-report",
        "summary": corpus.get("summary", {}),
        "byStratum": {key: dict(value) for key, value in sorted(strata.items())},
        "sealedAggregated": corpus.get("sealed", {}),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Corpus do FORJA AUTO-RESEARCH")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--scan", action="store_true")
    action.add_argument("--check", type=Path)
    action.add_argument("--report", type=Path)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args(argv)
    try:
        if args.scan:
            manifest = _read_json(args.manifest, {}) or {}
            key = load_hmac_key()
            sealed_items: list[dict] = []
            payload = scan_corpus(
                args.state_dir,
                manifest=manifest,
                key=key,
                sealed_sink=sealed_items,
            )
            register_sealed_inventory(sealed_items, manifest)
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0 if payload["summary"]["eligible"] >= 20 else 1
        corpus = _read_json(args.check or args.report, None)
        if not isinstance(corpus, dict):
            raise ValueError("arquivo de corpus ausente ou inválido")
        if args.check:
            errors = check_corpus(corpus)
            print(json.dumps({
                "schemaVersion": SCHEMA,
                "generatedAt": FIXED_TIME,
                "producerRunId": "forja-ar-corpus-check",
                "ok": not errors,
                "errors": errors,
            }, ensure_ascii=False, indent=2))
            return 0 if not errors else 2
        print(json.dumps(report(corpus), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, FileNotFoundError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
