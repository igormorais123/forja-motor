"""Monta os canários reais de falha única do ciclo AR (camadas pública e secreta).

Uso interno (internal_working). Base: peça real ENTREGUE do caso Cafelana (Impugnação ao
AgInt, V4 de 15/07/2026) — fora de `state/` e portanto fora de qualquer split do corpus
(desentrelaçamento canário×avaliação, limitação do ciclo AR-2; a base anterior, Azimut,
era artefato do split train e foi usada como tarefa de avaliação no mesmo ciclo).
Cada classe injeta UMA falha real minerada; o controle benigno é paráfrase neutra.
Reexecutável: sobrescreve as classes e recalcula hashes no manifest.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_PIECE = (
    ROOT.parent / "Cafelana" / "contrarrazões ao AgInt no AREsp nº 2.698.443D"
    / "_entrega_fabio_2026-07-15" / "IMPUGNACAO_AGINT_CAFELANA_V4_15-07-2026_FONTE.md"
)
ANCHOR = "Súmula 7"
PUBLIC_DIR = ROOT / "autoresearch" / "canarios"
SECRETS = Path(os.environ.get("FORJA_AR_SECRETS_DIR") or Path.home() / ".forja_ar_secrets")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_class(root: Path, class_id: str, base: str, mutation: str, control: str,
                target: str, licao: str, context: dict | None = None) -> dict:
    folder = root / class_id
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "base.md").write_text(base, encoding="utf-8")
    (folder / "mutacao.md").write_text(mutation, encoding="utf-8")
    (folder / "controle_benigno.md").write_text(control, encoding="utf-8")
    (folder / "README.md").write_text(
        f"# Canário {class_id} (internal_working — nunca protocolar)\n\n"
        f"Sensor-alvo: {target}. Lição-âncora: {licao}.\n"
        "Base real (Impugnação AgInt Cafelana V4, entregue; fora do corpus AR) com UMA falha injetada em mutacao.md.\n",
        encoding="utf-8",
    )
    entry = {
        "id": class_id,
        "path": class_id,
        "base": "base.md",
        "mutation": "mutacao.md",
        "control": "controle_benigno.md",
        "targetSensor": target,
        "licaoAncora": licao,
        "hashes": {
            "base": sha(folder / "base.md"),
            "mutation": sha(folder / "mutacao.md"),
            "control": sha(folder / "controle_benigno.md"),
        },
    }
    if context:
        entry["context"] = context
    return entry


def main() -> int:
    base = BASE_PIECE.read_text(encoding="utf-8", errors="replace")
    control = base + "\nTermos em que aguarda deferimento.\n"

    authorities_context = {
        "authorities_ledger": [
            {"rotulo": ANCHOR, "aliases": [ANCHOR], "required": True, "verified": True},
            {"rotulo": "AREsp", "aliases": ["AREsp"], "required": True, "verified": True},
        ]
    }
    if ANCHOR not in base:
        print(f"base não contém '{ANCHOR}' — revisar classe citacao_removida_real", file=sys.stderr)
        return 2

    public_entries = [
        build_class(
            PUBLIC_DIR, "placeholder_real", base,
            base + "\nProtocolado em [DIA] de julho de 2026.\n", control,
            "I4", "Erro recorrente #3 (placeholder no PDF final; lições 12 e 18)",
        ),
        build_class(
            PUBLIC_DIR, "origem_operacional_real", base,
            base.replace(
                ANCHOR,
                ANCHOR + " (conforme documento recebido por WhatsApp)",
                1,
            ), control,
            "I6", "Feedback Fábio 11/07/2026 (origem operacional nunca aparece na peça)",
        ),
        build_class(
            PUBLIC_DIR, "estilo_ia_real", base,
            base + "\nNão se trata de mera irregularidade, mas de vício estrutural do julgado.\n", control,
            "I5", "Lições 5, 12 e 38 (cara de IA; protocolo de escrita humana)",
        ),
        build_class(
            PUBLIC_DIR, "sumula_trocada_real", base,
            base + "\nAplica-se, ainda, o óbice da Súmula 182 do STF.\n", control,
            "I2", "Erro recorrente #1 e lição 41 (par súmula×tribunal trocado)",
        ),
        build_class(
            PUBLIC_DIR, "citacao_removida_real", base,
            base.replace(ANCHOR, "óbice aplicável"), control,
            "I1", "Erro recorrente #1 (autoridade obrigatória ausente; diretriz 8 — suficiência)",
            context=authorities_context,
        ),
    ]

    manifest_path = PUBLIC_DIR / "CANARIOS_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["classes"] = public_entries
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    secret_root = SECRETS / "canarios_secretos"
    secret_entries = [
        build_class(
            secret_root, "origem_parafraseada", base,
            base.replace(
                ANCHOR,
                ANCHOR + " — cuja cópia consta do Google Drive compartilhado —",
                1,
            ), control,
            "I6", "Feedback Fábio 11/07/2026 (paráfrase de repositório operacional)",
        ),
        build_class(
            secret_root, "placeholder_sutil", base,
            base.replace(ANCHOR, ANCHOR + " (acórdão de [DATA])", 1), control,
            "I4", "Erro recorrente #3 (placeholder no meio do texto, não no fecho)",
        ),
    ]
    secret_manifest = {
        "schemaVersion": "FORJA-AR-v1",
        "generatedAt": "1970-01-01T00:00:00Z",
        "producerRunId": "ar-build-canarios-reais",
        "classes": secret_entries,
    }
    (secret_root / "CANARIOS_MANIFEST.json").write_text(
        json.dumps(secret_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"publicas: {len(public_entries)} | secretas: {len(secret_entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
