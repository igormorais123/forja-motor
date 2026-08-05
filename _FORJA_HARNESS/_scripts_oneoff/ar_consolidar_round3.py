"""Consolida o round 3 (arquivos de voto por par) e computa comparações de indicadores."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from forja_ar_blind import canonicalize, consolidate  # noqa: E402
from forja_ar_indicadores import computar_indicadores, comparar  # noqa: E402

CICLO = ROOT / "autoresearch" / "ciclos" / "ciclo-1"
JUD = CICLO / "judgments"
EXEC = CICLO / "exec"

votes = json.loads((JUD / "raw_round3.json").read_text(encoding="utf-8"))
for item in votes:
    dest = JUD / f"{item['judgeId']}_{item['pairId']}.json"
    payload = {k: v for k, v in item.items() if k != "pairId"}
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

manifest = json.loads((ROOT / "autoresearch" / "AR_MANIFEST.json").read_text(encoding="utf-8"))

for pair_id in ("ciclo1-varA", "ciclo1-varB"):
    paths = sorted(JUD.glob(f"juiz?r3-claude_{pair_id}.json"))
    result = consolidate(CICLO / "blind", paths, pair_id)
    (CICLO / f"AR_JUDGMENT_{pair_id}.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(pair_id, "| valid:", result["valid"], "| posicional:", result["positionalInvalidations"],
          "| kappa:", result["kappa"], "| winner:", (result["winnerArtifactSha256"] or "")[:12] or None,
          "| erros:", result["errors"])

import hashlib

def canon_sha(side):
    text = canonicalize((EXEC / f"OUT_{side}.md").read_text(encoding="utf-8", errors="replace"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

print("canonical sha vigente:", canon_sha("vigente")[:12])
print("canonical sha varA:   ", canon_sha("varA")[:12])
print("canonical sha varB:   ", canon_sha("varB")[:12])

panels = {}
for side in ("vigente", "varA", "varB"):
    text = (EXEC / f"OUT_{side}.md").read_text(encoding="utf-8", errors="replace")
    panels[side] = computar_indicadores(text, {})
    (CICLO / f"AR_INDICATORS_{side}.json").write_text(
        json.dumps(panels[side], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for var in ("varA", "varB"):
    comp = comparar(panels["vigente"], panels[var], manifest)
    (CICLO / f"AR_COMPARISON_{var}.json").write_text(
        json.dumps(comp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(var, "| não-inferioridade aprovado:", comp["aprovado"], "| bloqueio:", comp["bloqueio"],
          "| deltas:", {k: round(v, 3) for k, v in comp["deltas"].items()})
