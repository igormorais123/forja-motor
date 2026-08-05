"""Bancada cega com swap e mapping HMAC externo."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import re
import sys
from pathlib import Path

from forja_ar_corpus import ROOT, load_hmac_key, secrets_dir
from forja_ar_runpair import validate_pair

SCHEMA = "FORJA-AR-v1"
FIXED_TIME = "1970-01-01T00:00:00Z"


def canonicalize(text: str) -> str:
    """Remove marcadores de variante sem alterar o conteúdo argumentativo."""
    text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, flags=re.S)
    lines = []
    for line in text.splitlines():
        if re.match(r"^\s*#{1,6}\s+.*\b(vigente|variante|vers[aã]o\s*[ab12])\b", line, re.I):
            continue
        line = re.sub(r"\b(?:VIGENTE|VARIANTE)\s*:\s*", "", line, flags=re.I)
        lines.append(line.rstrip())
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines).strip()) + "\n"


# Lição L6 (ciclo AR-2): o vazamento de cegamento veio do orquestrador — executor ecoou
# o nome do arquivo de saída ("OUT_T2_VIGENTE") e o cabeçalho de mutação ("parecer AR-1")
# dentro do produto. A varredura roda no prepare e recusa o par inteiro (fail-closed).
LEAK_PATTERNS = (
    r"OUT_[A-Za-z0-9_]+",
    r"parecer\s+AR-\d",
    r"mutac[aã]o\s*:",
    r"\bvar[A-Z]\b",
    r"\bEXECPROMPT\b",
)


def leak_scan(text: str) -> list[str]:
    """Retorna padrões identificadores de lado/experimento presentes no texto canonicalizado."""
    return [pattern for pattern in LEAK_PATTERNS if re.search(pattern, text)]


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha_file(path: Path) -> str:
    return _sha_bytes(path.read_bytes())


def _canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _mapping_path(pair_id: str) -> Path:
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "-", pair_id)
    directory = secrets_dir(create=True) / "mappings"
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{safe}.mapping.json"


def prepare(runpair_dir: Path, blind_dir: Path, pair_id: str, *, key: bytes | None = None) -> dict:
    """Canonicaliza dois outputs e grava o mapping somente fora do workspace."""
    parity = validate_pair(runpair_dir)
    if not parity["valid"]:
        raise ValueError("runpair sem paridade: " + "; ".join(parity["errors"]))
    manifests = {}
    for side in ("vigente", "variante"):
        paths = sorted(Path(runpair_dir).glob(f"EXEC_{side}_R*.json"))
        if len(paths) != 1:
            raise ValueError("v1 prepara exatamente uma repetição por par")
        manifests[side] = json.loads(paths[0].read_text(encoding="utf-8", errors="replace"))
    texts, hashes = {}, {}
    for side, manifest in manifests.items():
        output = Path(str(manifest["outputPath"]))
        texts[side] = canonicalize(output.read_text(encoding="utf-8", errors="replace"))
        leaks = leak_scan(texts[side])
        if leaks:
            raise ValueError(f"cegamento_comprometido:{side}:" + ",".join(leaks))
        hashes[side] = _sha_bytes(texts[side].encode("utf-8"))
    blind_dir = Path(blind_dir)
    blind_dir.mkdir(parents=True, exist_ok=True)
    layout = {
        1: {"L": "vigente", "R": "variante"},
        2: {"L": "variante", "R": "vigente"},
    }
    bundles = {}
    for order, positions in layout.items():
        for position, side in positions.items():
            name = f"PAR_{pair_id}_ORD{order}_{position}.md"
            (blind_dir / name).write_text(texts[side], encoding="utf-8")
            bundles[f"{order}:{position}"] = {
                "file": name,
                "artifactSha256": hashes[side],
                "bundleSha256": _sha_file(blind_dir / name),
            }
    mapping = {
        "schemaVersion": SCHEMA,
        "pair": pair_id,
        "variantFamily": manifests["variante"]["familia"],
        "bundles": bundles,
    }
    key = key or load_hmac_key()
    mapping["hmacSha256"] = hmac.new(key, _canonical(mapping), hashlib.sha256).hexdigest()
    path = _mapping_path(pair_id)
    path.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": f"blind-prepare-{pair_id}",
        "prepared": True,
        "mappingPath": str(path),
        "mappingSha256": _sha_file(path),
        "mappingCommitment": _sha_bytes(_canonical(mapping)),
        "bundles": sorted(item["file"] for item in bundles.values()),
    }


def _verify_mapping(mapping: dict, key: bytes) -> bool:
    signature = str(mapping.get("hmacSha256") or "")
    unsigned = {k: v for k, v in mapping.items() if k != "hmacSha256"}
    expected = hmac.new(key, _canonical(unsigned), hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


def _mapping_leaked(workspace: Path, mapping_sha: str, external_path: Path) -> bool:
    excluded = {".git", ".claude", "state", "__pycache__"}
    for path in Path(workspace).rglob("*.json"):
        if any(part in excluded for part in path.parts):
            continue
        try:
            if path.resolve() == external_path.resolve() or path.stat().st_size > 1024 * 1024:
                continue
            if _sha_file(path) == mapping_sha:
                return True
        except OSError:
            continue
    return False


def _cohen_kappa(votes_a: list[str], votes_b: list[str]) -> float | None:
    if not votes_a or len(votes_a) != len(votes_b):
        return None
    labels = sorted(set(votes_a) | set(votes_b))
    observed = sum(a == b for a, b in zip(votes_a, votes_b)) / len(votes_a)
    expected = sum(
        (votes_a.count(label) / len(votes_a)) * (votes_b.count(label) / len(votes_b))
        for label in labels
    )
    return 1.0 if expected == 1.0 and observed == 1.0 else ((observed - expected) / (1 - expected) if expected != 1 else 0.0)


def consolidate(
    blind_dir: Path,
    judgment_paths: list[Path],
    pair_id: str,
    *,
    key: bytes | None = None,
    workspace: Path = ROOT,
) -> dict:
    """Valida âncoras, isolamento declarado, família e regra posicional correta."""
    mapping_path = _mapping_path(pair_id)
    if not mapping_path.is_file():
        raise ValueError("mapping externo ausente")
    mapping = json.loads(mapping_path.read_text(encoding="utf-8", errors="replace"))
    key = key or load_hmac_key()
    errors = []
    if not _verify_mapping(mapping, key):
        errors.append("mapping_adulterado")
    if _mapping_leaked(workspace, _sha_file(mapping_path), mapping_path):
        errors.append("mapping_vazado_no_workspace")
    votes_by_judge: dict[str, list[dict]] = {}
    for path in judgment_paths:
        judgment = json.loads(Path(path).read_text(encoding="utf-8", errors="replace"))
        judge = str(judgment.get("judgeId") or "")
        if not judge or judgment.get("schemaVersion") != SCHEMA:
            errors.append("devolutiva_schema_invalido")
            continue
        if judgment.get("judgeFamily") == mapping.get("variantFamily"):
            errors.append(f"familia_geradora_julgou:{judge}")
        declarations = judgment.get("declarations") or {}
        if declarations.get("externalAccess") or declarations.get("workspaceAccess"):
            errors.append(f"acesso_externo_detectado:{judge}")
        declared = set(declarations.get("filesRead") or [])
        judge_votes = []
        for vote in judgment.get("votes") or []:
            order, position = int(vote.get("order", 0)), str(vote.get("winnerPosition") or "")
            entry = mapping.get("bundles", {}).get(f"{order}:{position}")
            if not entry:
                errors.append(f"voto_invalido:{judge}:{order}")
                continue
            bundle = Path(blind_dir) / entry["file"]
            if entry["file"] not in declared:
                errors.append(f"arquivo_nao_declarado:{judge}:{entry['file']}")
            if not bundle.is_file() or _sha_file(bundle) != entry["bundleSha256"]:
                errors.append(f"bundle_adulterado:{entry['file']}")
                continue
            anchor = str(vote.get("anchor") or "").strip()
            text = bundle.read_text(encoding="utf-8", errors="replace")
            if not anchor or anchor not in text:
                errors.append(f"ancora_invalida:{judge}:{order}")
                continue
            judge_votes.append(
                {
                    "judgeId": judge,
                    "order": order,
                    "position": position,
                    "artifactSha256": entry["artifactSha256"],
                }
            )
        votes_by_judge[judge] = sorted(judge_votes, key=lambda item: item["order"])
    positional_invalid = 0
    consistent = []
    for judge, votes in votes_by_judge.items():
        if len(votes) != 2:
            errors.append(f"ordens_incompletas:{judge}")
            continue
        if votes[0]["position"] == votes[1]["position"]:
            positional_invalid += 1
            errors.append(f"vies_posicional:{judge}")
        elif votes[0]["artifactSha256"] != votes[1]["artifactSha256"]:
            errors.append(f"vencedor_inconsistente_por_hash:{judge}")
        else:
            consistent.append(votes[0]["artifactSha256"])
    judges = sorted(votes_by_judge)
    kappa = None
    if len(judges) >= 2:
        a = [item["artifactSha256"] for item in votes_by_judge[judges[0]]]
        b = [item["artifactSha256"] for item in votes_by_judge[judges[1]]]
        kappa = _cohen_kappa(a, b)
    return {
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": f"blind-{pair_id}",
        "valid": not errors,
        "errors": errors,
        "positionalInvalidations": positional_invalid,
        "votes": [vote for votes in votes_by_judge.values() for vote in votes],
        "winnerArtifactSha256": consistent[0] if consistent and len(set(consistent)) == 1 else None,
        "kappa": kappa,
        "smallNWarning": len(judges) < 2,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Bancada cega FORJA AUTO-RESEARCH")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--prepare", action="store_true")
    action.add_argument("--consolidate", action="store_true")
    parser.add_argument("--pair-id", required=True)
    parser.add_argument("--runpair-dir", type=Path)
    parser.add_argument("--blind-dir", type=Path, required=True)
    parser.add_argument("--judgment", type=Path, action="append", default=[])
    args = parser.parse_args(argv)
    try:
        result = (
            prepare(args.runpair_dir, args.blind_dir, args.pair_id)
            if args.prepare
            else consolidate(args.blind_dir, args.judgment, args.pair_id)
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("valid", True) else 2
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
