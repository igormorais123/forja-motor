import json
from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "demandas.json"
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"


def ensure_manual():
    manual = read_json(MANUAL_PATH, None)
    if not isinstance(manual, dict):
        manual = {"schema": 1, "updatedAt": now_iso(), "items": {}}
    manual.setdefault("schema", 1)
    manual.setdefault("items", {})
    return manual


def comments_for(entry):
    comments = entry.get("comentarios") or []
    return sorted(comments, key=lambda x: x.get("at") or "")


def apply_manual(data, manual):
    by_id = manual.get("items") or {}
    applied = 0
    for item in data.get("demandas", []):
        entry = by_id.get(item.get("id"))
        if not entry:
            item.pop("manual", None)
            continue

        comments = comments_for(entry)
        overrides = entry.get("overrides") or {}

        status = overrides.get("status")
        if status:
            item["status"] = status
            applied += 1

        if "respondidoComConteudo" in overrides:
            item["respondidoComConteudo"] = bool(overrides.get("respondidoComConteudo"))
            applied += 1

        for src, dst in [
            ("evidenciaResposta", "evidenciaResposta"),
            ("evidenciaTipo", "evidenciaTipo"),
            ("proximaAcao", "proximaAcao"),
            ("urgenciaManual", "urgenciaManual"),
            ("prazo", "prazo"),
            ("prazoTexto", "prazoTexto"),
            ("resumo", "resumo"),
            ("titulo", "titulo"),
            ("tags", "tags"),
            ("etapaOperacional", "etapaOperacional"),
        ]:
            if src in overrides and overrides[src] not in (None, "", []):
                item[dst] = overrides[src]
                applied += 1

        item["manual"] = {
            "updatedAt": entry.get("updatedAt") or manual.get("updatedAt"),
            "commentCount": len(comments),
            "lastComment": comments[-1]["texto"] if comments else "",
            "comentarios": comments[-6:],
            "overrides": overrides,
        }
    return applied


def main():
    data = read_json(DATA_PATH, {"schema": 1, "demandas": []})
    manual = ensure_manual()
    applied = apply_manual(data, manual)
    data["updatedAt"] = now_iso()
    atomic_write_json(DATA_PATH, data)
    atomic_write_json(MANUAL_PATH, manual)
    print(json.dumps({"ok": True, "applied": applied, "items": len(manual.get("items", {}))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
