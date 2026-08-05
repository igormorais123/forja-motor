"""Congelamento e validação de execuções pareadas do FORJA AUTO-RESEARCH."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

SCHEMA = "FORJA-AR-v1"
FIXED_TIME = "1970-01-01T00:00:00Z"
REQUIRED = {
    "modelo",
    "familia",
    "versao",
    "parametros",
    "promptHash",
    "inputHash",
    "outputPath",
    "outputSha256",
    "tokens",
    "duracao",
    "repeticao",
}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def freeze_input(
    runpair_dir: Path,
    case_id: str,
    target: Path,
    *,
    claims_ledger: list | None = None,
    authorities_ledger: list | None = None,
    repetition: int = 0,
) -> Path:
    """Congela texto e denominadores antes da geração."""
    target = Path(target)
    text = target.read_text(encoding="utf-8", errors="replace")
    payload = {
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": f"runpair-{case_id}-{repetition}",
        "caseId": case_id,
        "repeticao": int(repetition),
        "sourcePath": str(target),
        "sourceSha256": _sha(target),
        "text": text,
        "claims_ledger": claims_ledger or [],
        "authorities_ledger": authorities_ledger or [],
    }
    payload["inputHash"] = hashlib.sha256(_canonical(payload)).hexdigest()
    runpair_dir = Path(runpair_dir)
    runpair_dir.mkdir(parents=True, exist_ok=True)
    output = runpair_dir / f"INPUT_{repetition}.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


def sanitize_instructions(text: str) -> str:
    """Remove cabeçalhos HTML iniciais (metadados de mutação) das instruções de trabalho.

    Lição L6 (ciclo AR-2): o cabeçalho `<!-- mutacao: ... -->` embutido no prompt fez o
    executor escrever metadados do experimento dentro da peça, quebrando o cegamento.
    """
    import re as _re

    return _re.sub(r"^(\s*<!--.*?-->\s*\n)+", "", text, flags=_re.DOTALL)


def register_manifest(runpair_dir: Path, side: str, manifest_path: Path) -> Path:
    """Valida e arquiva manifest de execução sem alterar o output."""
    if side not in {"vigente", "variante"}:
        raise ValueError("lado deve ser vigente ou variante")
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8", errors="replace"))
    missing = sorted(REQUIRED - set(manifest))
    if missing:
        raise ValueError(f"campos ausentes no manifest: {missing}")
    output = Path(str(manifest["outputPath"]))
    if not output.is_file() or _sha(output) != manifest["outputSha256"]:
        raise ValueError("output ausente ou hash divergente")
    if not isinstance(manifest["parametros"], dict):
        raise ValueError("parametros deve ser objeto")
    normalized = dict(manifest)
    normalized.update({
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": f"runpair-register-{side}-{int(manifest['repeticao'])}",
        "lado": side,
    })
    destination = Path(runpair_dir) / f"EXEC_{side}_R{int(manifest['repeticao'])}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return destination


def validate_pair(runpair_dir: Path) -> dict:
    """Falha fechado se os dois lados não foram produzidos sob condições pares."""
    manifests = []
    for path in sorted(Path(runpair_dir).glob("EXEC_*_R*.json")):
        item = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        item["_path"] = str(path)
        manifests.append(item)
    by_rep: dict[int, dict[str, dict]] = {}
    errors = []
    for item in manifests:
        rep = int(item.get("repeticao", -1))
        side = str(item.get("lado", ""))
        if side in by_rep.setdefault(rep, {}):
            errors.append(f"manifest duplicado: repetição {rep}, lado {side}")
        by_rep[rep][side] = item
    custo = []
    for rep, pair in sorted(by_rep.items()):
        if set(pair) != {"vigente", "variante"}:
            errors.append(f"par incompleto na repetição {rep}")
            continue
        left, right = pair["vigente"], pair["variante"]
        for field in ("inputHash", "familia", "modelo", "versao", "parametros"):
            if left.get(field) != right.get(field):
                errors.append(f"paridade violada em {field}, repetição {rep}")
        vig = int(left.get("tokens") or 0)
        var = int(right.get("tokens") or 0)
        custo.append({
            "repeticao": rep,
            "vigenteTokens": vig,
            "varianteTokens": var,
            "razaoVarianteSobreVigente": round(var / vig, 4) if vig else None,
        })
    if not by_rep:
        errors.append("nenhum par registrado")
    return {
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": "forja-ar-runpair-validate",
        "valid": not errors,
        "releasedForBlind": not errors,
        "pairs": len(by_rep),
        "errors": errors,
        # Indicador operacional de custo (lição L10, ciclo AR-2): 4-13x de diferença real
        # entre prompts não aparecia em nenhum artefato formal.
        "custoPareado": custo,
    }


def _read_ledger(path: Path | None) -> list:
    if not path:
        return []
    value = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    if not isinstance(value, list):
        raise ValueError("ledger deve ser uma lista JSON")
    return value


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Executor pareado FORJA AUTO-RESEARCH")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--freeze", action="store_true")
    action.add_argument("--register", action="store_true")
    action.add_argument("--validate", action="store_true")
    parser.add_argument("--runpair-dir", type=Path, required=True)
    parser.add_argument("--caso")
    parser.add_argument("--alvo", type=Path)
    parser.add_argument("--lado", choices=("vigente", "variante"))
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--claims-ledger", type=Path)
    parser.add_argument("--authorities-ledger", type=Path)
    parser.add_argument("--repeticao", type=int, default=0)
    args = parser.parse_args(argv)
    try:
        if args.freeze:
            if not args.caso or not args.alvo:
                raise ValueError("--freeze requer --caso e --alvo")
            output = freeze_input(
                args.runpair_dir,
                args.caso,
                args.alvo,
                claims_ledger=_read_ledger(args.claims_ledger),
                authorities_ledger=_read_ledger(args.authorities_ledger),
                repetition=args.repeticao,
            )
            result = {"schemaVersion": SCHEMA, "frozen": str(output)}
        elif args.register:
            if not args.lado or not args.manifest:
                raise ValueError("--register requer --lado e --manifest")
            output = register_manifest(args.runpair_dir, args.lado, args.manifest)
            result = {"schemaVersion": SCHEMA, "registered": str(output)}
        else:
            result = validate_pair(args.runpair_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("valid", True) else 2
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
