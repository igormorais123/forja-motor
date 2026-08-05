"""Divide as devolutivas dos juízes por par e consolida na bancada cega."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from forja_ar_blind import consolidate  # noqa: E402

CICLO = ROOT / "autoresearch" / "ciclos" / "ciclo-1"
JUD = CICLO / "judgments"
JUD.mkdir(exist_ok=True)

# Devolutivas brutas coladas pelo orquestrador (JSON dos dois juízes)
raw = json.loads((JUD / "raw_juizes.json").read_text(encoding="utf-8"))

for judge in raw:
    for pair_id, pair_data in judge["pares"].items():
        payload = {
            "schemaVersion": judge["schemaVersion"],
            "judgeId": judge["judgeId"],
            "judgeFamily": judge["judgeFamily"],
            "declarations": judge["declarations"],
            "votes": pair_data["votes"],
        }
        dest = JUD / f"{judge['judgeId']}_{pair_id}.json"
        dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("gravado:", dest.name)

for pair_id in ("ciclo1-varA", "ciclo1-varB"):
    paths = sorted(JUD.glob(f"*_{pair_id}.json"))
    result = consolidate(CICLO / "blind", paths, pair_id)
    dest = CICLO / f"AR_JUDGMENT_{pair_id}.json"
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(pair_id, "| valid:", result["valid"], "| posicional:", result["positionalInvalidations"],
          "| kappa:", result["kappa"], "| winner:", (result["winnerArtifactSha256"] or "")[:12] or None)
    for e in result["errors"]:
        print("   erro:", e)
