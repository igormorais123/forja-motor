from __future__ import annotations

import json
import math
import re
import zipfile
from pathlib import Path

import fitz
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
PDF = OUT / "PLANO_MESTRE_REFATORACAO_FORJA_2026-07-15.pdf"
DOCX = OUT / "PLANO_MESTRE_REFATORACAO_FORJA_2026-07-15.docx"
PAGES = OUT / "qa_word_pdf"
CONTACTS = OUT / "qa_contact_sheets"


def main() -> None:
    issues: list[str] = []
    document = fitz.open(PDF)
    pages = len(document)
    if pages < 40:
        issues.append(f"unexpectedly short report: {pages} pages")

    all_text: list[str] = []
    page_metrics: list[dict[str, object]] = []
    expected = (595.28, 841.89)
    for index, page in enumerate(document, 1):
        text = page.get_text("text")
        all_text.append(text)
        if len(text.strip()) < 12:
            issues.append(f"page {index} has too little extractable text")
        if abs(page.rect.width - expected[0]) > 2 or abs(page.rect.height - expected[1]) > 2:
            issues.append(f"page {index} is not A4 portrait: {page.rect}")
        out_of_bounds = 0
        min_font = 99.0
        for block in page.get_text("dict").get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    x0, y0, x1, y1 = span["bbox"]
                    if x0 < -1 or y0 < -1 or x1 > page.rect.width + 1 or y1 > page.rect.height + 1:
                        out_of_bounds += 1
                    if span.get("text", "").strip():
                        min_font = min(min_font, float(span.get("size", 99)))
        if out_of_bounds:
            issues.append(f"page {index} has {out_of_bounds} text spans outside the page")
        page_metrics.append(
            {
                "page": index,
                "characters": len(text.strip()),
                "minExtractableFontPt": None if min_font == 99.0 else round(min_font, 2),
                "outOfBoundsSpans": out_of_bounds,
            }
        )

    joined = "\n".join(all_text)
    forbidden = {
        "unreplaced_figure_marker": r"\{\{FIG_",
        "todo_marker": r"\[(?:TODO|TBD|FIXME|XXX)\]",
        "protocol_placeholder": r"\[(?:NOME|CRC-UF|VERIFICAR)\]",
    }
    for name, pattern in forbidden.items():
        if re.search(pattern, joined):
            issues.append(f"forbidden marker detected: {name}")
    for expected_text in (
        "Refatoração estrutural segura da FORJA",
        "Gate G9A",
        "Gate G9B",
        "Catálogo dos 18 planos executáveis",
        "Conclusão do planejamento",
    ):
        if expected_text not in joined:
            issues.append(f"expected text absent from PDF: {expected_text}")

    metadata = document.metadata
    if metadata.get("author") != "Medina Osório Advogados":
        issues.append("PDF author metadata is not institutional")
    if "Refatoração Segura" not in (metadata.get("title") or ""):
        issues.append("PDF title metadata is incomplete")
    document.close()

    with zipfile.ZipFile(DOCX) as archive:
        document_xml = archive.read("word/document.xml").decode("utf-8")
        media = [name for name in archive.namelist() if name.startswith("word/media/")]
        emf = [name for name in media if name.lower().endswith(".emf")]
        if "{{FIG_" in document_xml:
            issues.append("DOCX contains unreplaced figure marker")
        if len(emf) < 17:
            issues.append(f"DOCX contains only {len(emf)} EMF diagrams")

    pngs = sorted(PAGES.glob("p*.png"))
    if len(pngs) != pages:
        issues.append(f"rendered page count mismatch: {len(pngs)} PNG vs {pages} PDF")

    CONTACTS.mkdir(parents=True, exist_ok=True)
    contacts: list[str] = []
    for group in range(math.ceil(len(pngs) / 4)):
        subset = pngs[group * 4 : group * 4 + 4]
        if not subset:
            continue
        loaded = [Image.open(path).convert("RGB") for path in subset]
        cell_w = max(image.width for image in loaded)
        cell_h = max(image.height for image in loaded) + 42
        sheet = Image.new("RGB", (cell_w * 2, cell_h * 2), "white")
        draw = ImageDraw.Draw(sheet)
        for position, (image, path) in enumerate(zip(loaded, subset)):
            x = (position % 2) * cell_w
            y = (position // 2) * cell_h
            sheet.paste(image, (x, y + 36))
            draw.text((x + 12, y + 10), f"Página {int(path.stem[1:])}", fill="#395C60")
        target = CONTACTS / f"contact_{group + 1:02d}.png"
        sheet.save(target, optimize=True)
        contacts.append(str(target.relative_to(ROOT)))

    report = {
        "ok": not issues,
        "pages": pages,
        "pdfMetadata": metadata,
        "docxEmfCount": len(emf),
        "renderedPages": len(pngs),
        "contactSheets": contacts,
        "programmaticChecksPassed": not issues,
        "allPagesInspected": False,
        "issues": issues,
        "pageMetrics": page_metrics,
    }
    (OUT / "visual_qa_draft.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("ok", "pages", "docxEmfCount", "renderedPages", "issues")}, ensure_ascii=False))
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
