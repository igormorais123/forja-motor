import hashlib
from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
DEMANDS_PATH = ROOT / "data" / "demandas.json"
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"

DELTAN_DEMAND_ID = "email-auto-19f3ea400b7dec3d"
GENERIC_WHATSAPP_ID = "whatsapp-fabio-medina-osorio"
CASE_FOLDER = "Material para elaboração de parecer - interessado Deltan Dallagnol"

DOCUMENTS = [
    {
        "messageId": "3AC5E1928C9F45803E36",
        "file": "2026.07.20_RDE_DeltanDallagnol_PI - versao final.pdf",
        "pages": 142,
        "sha256": "1be414b5f44c0ab1b2534ff66b1ade3426d9a3ba9edb00be57fb500bdbeb0b62",
    },
    {
        "messageId": "3AA5B46B735305DE37C8",
        "file": "Parecer Ricardo - Deltan Dallagnol - final.pdf",
        "pages": 20,
        "sha256": "c61422d8af4d87fc8cf28892b762aceefaea34bab7cef09caf9ca90a16870901",
    },
    {
        "messageId": "3AB2ADA2478A4568AEDE",
        "file": "Parecer - Dallagnol - Adriano - versao final.pdf",
        "pages": 51,
        "sha256": "5f61e19b0b44504c9b8904fdcc2447d3031943a1b3db2e49ba67d456be684d30",
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_archive() -> None:
    annexes = WORKSPACE / CASE_FOLDER / "Anexos do email"
    for document in DOCUMENTS:
        path = annexes / document["file"]
        if not path.is_file():
            raise FileNotFoundError(f"Arquivo canônico ausente: {path}")
        actual = sha256(path)
        if actual != document["sha256"]:
            raise ValueError(f"SHA-256 divergente: {path.name}: {actual}")


def add_comment(entry: dict, comment: dict) -> None:
    comments = entry.setdefault("comentarios", [])
    existing = next(
        (item for item in comments if item.get("id") == comment["id"]), None
    )
    if existing is None:
        comments.append(comment)
    else:
        existing.update(comment)


def main() -> None:
    validate_archive()

    data = read_json(DEMANDS_PATH, {"schema": 1, "demandas": []}) or {
        "schema": 1,
        "demandas": [],
    }
    if not any(
        item.get("id") == DELTAN_DEMAND_ID for item in data.get("demandas", [])
    ):
        raise RuntimeError("Demanda Deltan não encontrada; registro não aplicado.")

    manual = read_json(MANUAL_PATH, {"schema": 1, "items": {}}) or {
        "schema": 1,
        "items": {},
    }
    items = manual.setdefault("items", {})
    event_time = now_iso()

    deltan_entry = items.setdefault(
        DELTAN_DEMAND_ID, {"comentarios": [], "overrides": {}}
    )
    add_comment(
        deltan_entry,
        {
            "id": "proveniencia-rde-pareceres-whatsapp-20260721",
            "at": event_time,
            "tipo": "ingestao-documental",
            "texto": (
                "Três PDFs recebidos de Fábio no WhatsApp às 14h03 de 21/07 foram "
                "arquivados no caso Deltan e confrontados por SHA-256 com o complemento "
                "do Gmail 19f85a802667b10c. Os pares são idênticos; mantida uma cópia "
                "canônica de cada arquivo, com 213 páginas no total."
            ),
            "autor": "Igor/Codex",
        },
    )
    add_comment(
        deltan_entry,
        {
            "id": "utilidade-rde-pareceres-whatsapp-20260721",
            "at": event_time,
            "tipo": "avaliacao-documental",
            "texto": (
                "Material classificado como altamente útil e já aproveitado criticamente "
                "na N4 entregue para revisão interna. A tabela foi indexada em 16 entradas; "
                "a divergência dos pareceres e as inconsistências da RDE foram preservadas. "
                "Continuam pendentes o áudio do advogado Leandro, o número/recibo do RDE e "
                "as fontes oficiais dos expedientes."
            ),
            "autor": "Igor/Codex",
        },
    )
    deltan_entry["updatedAt"] = event_time

    generic_entry = items.setdefault(
        GENERIC_WHATSAPP_ID, {"comentarios": [], "overrides": {}}
    )
    add_comment(
        generic_entry,
        {
            "id": "triagem-fabio-deltan-rde-pareceres-20260721",
            "at": event_time,
            "tipo": "triagem-whatsapp",
            "texto": (
                "Entrada documental de 21/07 roteada para a demanda Deltan: três PDFs "
                "arquivados, deduplicados contra o Gmail, indexados e vinculados à N4. "
                "Nenhuma mensagem foi enviada."
            ),
            "autor": "Igor/Codex",
        },
    )
    generic_entry["updatedAt"] = event_time

    manual["updatedAt"] = event_time
    atomic_write_json(MANUAL_PATH, manual)

    print(
        {
            "ok": True,
            "demandId": DELTAN_DEMAND_ID,
            "documents": len(DOCUMENTS),
            "pages": sum(item["pages"] for item in DOCUMENTS),
            "preservedOverrides": sorted(deltan_entry.get("overrides", {}).keys()),
        }
    )


if __name__ == "__main__":
    main()
