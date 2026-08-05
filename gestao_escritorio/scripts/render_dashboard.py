import base64
import json
from pathlib import Path

from dashboard_enrichment import enrich_snapshot
from office_io import atomic_write_text, read_json


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
DATA_DIR = ROOT / "data"
HTML_PATH = ROOT / "painel_gestao_escritorio.html"
REMOTE_HTML_PATH = ROOT / "PAINEL_ESCRITORIO_MEDINA_OSORIO.html"
TEMPLATE_PATH = ROOT / "templates" / "dashboard.html"
LOGO_PATH = ROOT / "assets" / "logo_medina_transp.png"
FAVICON_PATH = ROOT / "assets" / "logo_coluna_64.png"


def data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def build_snapshot() -> dict:
    payload = {
        "demandas": read_json(DATA_DIR / "demandas.json", {"schema": 1, "demandas": []}),
        "status": read_json(DATA_DIR / "status_integracoes.json", {}),
        "whatsapp": read_json(DATA_DIR / "whatsapp_candidates.json", {}),
        "deliveries": read_json(DATA_DIR / "entregas_fabio_osorio.json", {}),
        "manual": read_json(DATA_DIR / "intervencoes_manuais.json", {"schema": 1, "items": {}}),
        "forja": read_json(DATA_DIR / "forja_status.json", {"schemaVersion": 1, "revision": 0, "items": {}}),
        "forjaFila": read_json(DATA_DIR / "forja_fila.json", None),
        "hermesBridge": read_json(DATA_DIR / "hermes_bridge_status.json", {}),
        "runtime": read_json(DATA_DIR / "runtime_status.json", {}),
        "updateHistory": read_json(DATA_DIR / "update_history.json", {"schema": 1, "runs": []}),
    }
    return enrich_snapshot(payload, WORKSPACE)


def render(remote: bool) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    snapshot_json = json.dumps(build_snapshot(), ensure_ascii=False).replace("</", "<\\/")
    return (
        template.replace("__SNAPSHOT_JSON__", snapshot_json)
        .replace("__REMOTE_MODE__", "true" if remote else "false")
        .replace("__LOGO_URI__", data_uri(LOGO_PATH))
        .replace("__FAVICON_URI__", data_uri(FAVICON_PATH))
    )


def main() -> None:
    atomic_write_text(HTML_PATH, render(False))
    atomic_write_text(REMOTE_HTML_PATH, render(True))
    print(str(HTML_PATH))
    print(str(REMOTE_HTML_PATH))


if __name__ == "__main__":
    main()
