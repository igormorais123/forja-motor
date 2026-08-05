"""Debug: em quais bundles cada âncora do round 2 realmente existe."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CICLO = ROOT / "autoresearch" / "ciclos" / "ciclo-1"
BLIND = CICLO / "blind"

bundles = {p.name: p.read_text(encoding="utf-8", errors="replace") for p in sorted(BLIND.glob("PAR_*.md"))}
raw = json.loads((CICLO / "judgments" / "raw_juizes.json").read_text(encoding="utf-8"))
for judge in raw:
    for pair_id, pair in judge["pares"].items():
        for vote in pair["votes"]:
            anchor = vote["anchor"]
            hits = [name for name, text in bundles.items() if anchor in text]
            expected = f"PAR_{pair_id}_ORD{vote['order']}_{vote['winnerPosition']}.md"
            print(f"{judge['judgeId']} {pair_id} ORD{vote['order']} vencedor={vote['winnerPosition']}")
            print(f"  esperado em: {expected} | encontrado em: {hits if hits else 'NENHUM'}")
