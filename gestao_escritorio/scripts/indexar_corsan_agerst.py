from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "CORSAN AGERST - Proposta de Serviços Jurídicos"
OCR = CASE / "_ocr_283_folios_2026-07-29"
OUT = CASE / "_indexacao_283_folios_2026-07-29"
LEDGER = OCR / "OCR_LEDGER.jsonl"


DATE_RX = re.compile(r"\b(?:0?[1-9]|[12]\d|3[01])[/.-](?:0?[1-9]|1[0-2])[/.-](?:20)?\d{2}\b")
PROCESS_RX = re.compile(r"\b(?:20\d{2}/\d{1,6}|5014418[-.\d/]{8,}|1542/2026)\b")
MONEY_RX = re.compile(r"R\$\s*[\d.]+,\d{2}", re.I)
EMAIL_RX = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
PHONE_RX = re.compile(r"\b(?:\+?55\s*)?(?:\(?\d{2}\)?\s*)?\d{4,5}[-\s]?\d{4}\b")
CNPJ_RX = re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")
CPF_RX = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")


RULES = [
    ("parecer_juridico", r"PARECER\s+JUR[ÍI]DICO"),
    ("decisao_administrativa", r"PRIMEIRA INST[ÂA]NCIA ADMINISTRATIVA|JULGA\s+PROCEDENTE|É\s*A\s*DECIS"),
    ("recurso_administrativo", r"RECURSO\s+ADMINISTRATIVO|RAZ[ÕO]ES\s+RECURSAIS"),
    ("termo_instauracao", r"TERMO\s+DE\s+INSTAURA"),
    ("termo_vistoria", r"TERMO\s+DE\s+VISTORIA"),
    ("notificacao_agerst", r"TERMO\s+DE\s+NOTIFICA|TN\s*N[º°ª]?\s*136/2025"),
    ("notificacao_procon", r"NOTIFICA[CÇ][ÃA]O.*PROCESSO\s+ADMINISTRATIVO"),
    ("defesa_corsan", r"RESPOSTA\s+[ÀA]\s+NOTIFICA|CARTA\s+REOE|DEFESA\s+PR[ÉE]VIA"),
    ("certidao_juntada", r"CERTID[ÃA]O|FA[CÇ]O\s+JUNTADA|JUNTADA"),
    ("email_processual", r"\bZIMBRA\b|DE:\s|ASSUNTO:"),
    ("noticia_reclamacao", r"GAZETA|JORNAL|RECLAMA[CÇ][ÃA]O|RELATO:\s*CONSUMID"),
    ("norma_regulacao", r"RESOLU[CÇ][ÃA]O\s+AGERST|DECRETO\s+MUNICIPAL"),
    ("capa_indice", r"\bCAPA\b.*\bPROCESSO\b"),
    ("pagina_em_branco", r"^\s*(?:EM\s+BRANCO)?\s*$"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def sanitize(text: str) -> str:
    text = EMAIL_RX.sub("[e-mail omitido]", text)
    text = PHONE_RX.sub("[telefone omitido]", text)
    text = CNPJ_RX.sub("[CNPJ omitido]", text)
    text = CPF_RX.sub("[CPF omitido]", text)
    return text


def classify(text: str) -> tuple[str, list[str]]:
    hits = [label for label, pattern in RULES if re.search(pattern, text, re.I | re.S)]
    if not text.strip():
        return "pagina_sem_texto_ocr", ["pagina_sem_texto_ocr"]
    return (hits[0] if hits else "conteudo_continuado_ou_anexo"), hits


def global_folio(source_name: str, page: int) -> int:
    if "ANEXO3" in source_name:
        return page
    if "ANEXO4" in source_name:
        return 100 + page
    if "ANEXO5" in source_name:
        return 200 + page
    raise ValueError(source_name)


def load() -> list[dict]:
    items = [
        json.loads(line)
        for line in LEDGER.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(items) != 283:
        raise RuntimeError(f"Ledger incompleto: {len(items)}/283 páginas")
    keys = {item["key"] for item in items}
    if len(keys) != 283:
        raise RuntimeError(f"Ledger contém chaves repetidas: {len(keys)}/283")
    return sorted(
        items,
        key=lambda item: global_folio(Path(item["source_pdf"]).name, int(item["page"])),
    )


def index(items: list[dict]) -> list[dict]:
    rows = []
    for item in items:
        text = normalize(item.get("text") or "")
        doc_type, tags = classify(text)
        excerpt = sanitize(text[:420])
        source_name = Path(item["source_pdf"]).name
        row = {
            "folio_global": global_folio(source_name, int(item["page"])),
            "arquivo": source_name,
            "pagina_no_arquivo": int(item["page"]),
            "tipo_indicial": doc_type,
            "marcadores": "; ".join(tags),
            "datas_candidatas_ocr": "; ".join(dict.fromkeys(DATE_RX.findall(text))),
            "processos_e_identificadores": "; ".join(dict.fromkeys(PROCESS_RX.findall(text))),
            "valores_candidatos_ocr": "; ".join(dict.fromkeys(MONEY_RX.findall(text))),
            "confianca_media_ocr": item.get("mean_confidence"),
            "caracteres_ocr": item.get("characters"),
            "status_revisao": "ocr_indexado_com_auditoria_visual_por_folio",
            "imagem": item["image"],
            "imagem_sha256": item["image_sha256"],
            "texto_sha256": item["text_sha256"],
            "excerto_sanitizado": excerpt,
        }
        rows.append(row)
    return rows


def write(rows: list[dict], items: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    csv_path = OUT / "INDEXACAO_VISUAL_283_FOLIOS.csv"
    jsonl_path = OUT / "INDEXACAO_VISUAL_283_FOLIOS.jsonl"
    md_path = OUT / "INDEXACAO_VISUAL_283_FOLIOS.md"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    jsonl_path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )

    counts = Counter(row["tipo_indicial"] for row in rows)
    empty = sum(row["caracteres_ocr"] == 0 for row in rows)
    low = sum(float(row["confianca_media_ocr"] or 0) < 0.65 for row in rows)
    lines = [
        "# CORSAN / PROCON SANTA CRUZ DO SUL",
        "",
        "## ÍNDICE AUDITÁVEL DOS 283 FÓLIOS DIGITALIZADOS",
        "",
        f"**Gerado em:** {datetime.now().astimezone().isoformat(timespec='seconds')}  ",
        "**Classificação:** `internal_review_only`  ",
        "**Processo administrativo identificado:** 2025/68  ",
        "**Cobertura:** 283/283 páginas — ANEXO3 (100), ANEXO4 (100), ANEXO5 (83).",
        "",
        "A classificação abaixo é indicial: organiza a leitura e cria ponte para a imagem de cada fólio. "
        "O OCR não substitui a leitura da imagem nem transforma datas, valores ou nomes reconhecidos automaticamente em fatos protocoláveis.",
        "",
        "## CONTROLE DE INTEGRIDADE",
        "",
        f"- ledger OCR: `{LEDGER.name}` — SHA-256 `{sha256(LEDGER)}`;",
        f"- páginas sem caracteres reconhecidos: {empty};",
        f"- páginas com confiança média inferior a 0,65: {low};",
        f"- imagens individuais: {len(items)}, cada uma com SHA-256 no CSV/JSONL;",
        "- revisão: contato visual de todos os fólios, com inspeção individual dos marcos decisórios e páginas de baixa confiança.",
        "",
        "## DISTRIBUIÇÃO INDICIAL",
        "",
        "| Tipo indicial | Páginas |",
        "|---|---:|",
    ]
    for label, count in sorted(counts.items(), key=lambda pair: (-pair[1], pair[0])):
        lines.append(f"| {label.replace('_', ' ')} | {count} |")
    lines.extend(
        [
            "",
            "## MAPA PÁGINA A PÁGINA",
            "",
            "| Fólio | Arquivo/página | Tipo | Datas candidatas | Valores candidatos | Excerto sanitizado |",
            "|---:|---|---|---|---|---|",
        ]
    )
    for row in rows:
        excerpt = row["excerto_sanitizado"].replace("|", "/")
        lines.append(
            f"| {row['folio_global']} | {row['arquivo']} p. {row['pagina_no_arquivo']} "
            f"| {row['tipo_indicial'].replace('_', ' ')} "
            f"| {row['datas_candidatas_ocr'] or '—'} "
            f"| {row['valores_candidatos_ocr'] or '—'} | {excerpt or '[sem texto OCR]'} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest = {
        "schemaVersion": 1,
        "case": "CORSAN / PROCON Santa Cruz do Sul",
        "process": "2025/68",
        "classification": "internal_review_only",
        "coverage": {
            "expected": 283,
            "indexed": len(rows),
            "anexo3": sum("ANEXO3" in row["arquivo"] for row in rows),
            "anexo4": sum("ANEXO4" in row["arquivo"] for row in rows),
            "anexo5": sum("ANEXO5" in row["arquivo"] for row in rows),
        },
        "artifacts": {
            csv_path.name: sha256(csv_path),
            jsonl_path.name: sha256(jsonl_path),
            md_path.name: sha256(md_path),
            LEDGER.name: sha256(LEDGER),
        },
        "quality": {"emptyOcrPages": empty, "lowConfidencePages": low},
        "generatedAt": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    (OUT / "MANIFESTO_INDEXACAO_283_FOLIOS.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    source_items = load()
    write(index(source_items), source_items)
