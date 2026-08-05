"""Painel descritivo do ciclo AR-0 (estudo piloto, sem alegação de eficácia).

Cobre: artefatos pontuáveis do AR_CORPUS (train+holdout) + extensão descritiva com as
peças reais do experimento fabrica-peticoes-v1 (pilotos e rodadas cegas gen-0..2).
Saída: autoresearch/AR_PANEL.json com n, média, sigma e missingness por indicador.
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from forja_ar_indicadores import computar_com_cache  # noqa: E402

V1 = ROOT.parent / ".autoresearch" / "fabrica-peticoes-v1"


def coletar() -> list[dict]:
    itens = []
    corpus = json.loads((ROOT / "autoresearch" / "AR_CORPUS.json").read_text(encoding="utf-8"))
    for case in corpus["cases"]:
        if case["scoringEligible"]:
            itens.append({
                "fonte": "corpus_state",
                "id": case["caseId"],
                "split": case["split"],
                "path": ROOT / case["artifactPath"],
            })
    for pattern in ("pilotos/T*_output.md", "gen-*/blind/*.md"):
        for path in sorted(V1.glob(pattern)):
            if path.name == "MAPA_IA.md":
                continue
            itens.append({
                "fonte": "extensao_v1",
                "id": path.relative_to(V1).as_posix(),
                "split": "descritivo",
                "path": path,
            })
    return itens


def main() -> int:
    linhas = []
    for item in coletar():
        texto = item["path"].read_text(encoding="utf-8", errors="replace")
        resultado, _ = computar_com_cache(texto, {})
        linhas.append({
            "fonte": item["fonte"],
            "id": item["id"],
            "split": item["split"],
            "indicadores": {
                chave: valor.get("valor") for chave, valor in resultado["indicadores"].items()
            },
        })
    agregado = {}
    chaves = sorted({chave for linha in linhas for chave in linha["indicadores"]})
    for chave in chaves:
        valores = [linha["indicadores"][chave] for linha in linhas if linha["indicadores"].get(chave) is not None]
        agregado[chave] = {
            "n": len(valores),
            "missing": len(linhas) - len(valores),
            "media": round(statistics.mean(valores), 4) if valores else None,
            "sigma": round(statistics.pstdev(valores), 4) if len(valores) > 1 else None,
        }
    payload = {
        "schemaVersion": "FORJA-AR-v1",
        "generatedAt": "1970-01-01T00:00:00Z",
        "producerRunId": "ar-painel-piloto-ciclo0",
        "declaracao": "estudo piloto descritivo — sem alegação de eficácia (PRD §9.8)",
        "amostra": {"total": len(linhas),
                     "corpus_state": sum(l["fonte"] == "corpus_state" for l in linhas),
                     "extensao_v1": sum(l["fonte"] == "extensao_v1" for l in linhas)},
        "porIndicador": agregado,
        "linhas": linhas,
    }
    out = ROOT / "autoresearch" / "AR_PANEL.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"amostra": payload["amostra"], "porIndicador": agregado}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
