"""Spot-check dos flags I6 (origem operacional) do painel AR-0."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from forja_verificador import verificar  # noqa: E402

panel = json.loads((ROOT / "autoresearch" / "AR_PANEL.json").read_text(encoding="utf-8"))
ruins = [l for l in panel["linhas"] if l["indicadores"].get("I6") == 0.0]
print("pecas com I6=0:", len(ruins))
v1 = ROOT.parent / ".autoresearch" / "fabrica-peticoes-v1"
for linha in ruins[:4]:
    path = v1 / linha["id"] if linha["fonte"] == "extensao_v1" else ROOT / linha["id"]
    if not path.is_file():
        continue
    texto = path.read_text(encoding="utf-8", errors="replace")
    achados = [x for x in verificar(texto, "peca") if x["gate"] == "G9-proveniencia"]
    print("---", linha["id"], "->", [x["trecho"][:100] for x in achados[:2]])
