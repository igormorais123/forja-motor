"""Comparador documental multicamada para o retorno humano pós-protocolo.

O JSON completo fica no vault local. O Markdown é sempre derivado dele.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
import zipfile
from collections import Counter
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

from forja_n3_common import ForjaN3Error, atomic_write_json, atomic_write_text, canonical_hash, sha256_file
from forja_post_protocol_contracts import IMPACTS, LAYERS, LAYER_CAUSES


WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{WORD_NS}}}"
SUPPORTED_EXTENSIONS = {".docx", ".pdf", ".txt", ".md"}
LAYER_CAUSE = {
    layer: sorted(causes)[0] for layer, causes in LAYER_CAUSES.items()
}
MATERIAL_LAYERS = {
    "fact",
    "procedural_identity",
    "legal_rule",
    "authority_citation",
    "reasoning",
    "request_relief",
    "evidence_annex",
    "calculation",
}
PROTOCOL_NOISE = [
    re.compile(r"^\s*(?:protocolado|protocolo)\b.*(?:\d{2}/\d{2}/\d{4}|\d{7}-\d{2}\.\d{4})", re.I),
    re.compile(r"^\s*(?:p[aá]gina|folha|fls?\.?)\s*\d+\s*(?:de\s*\d+)?\s*$", re.I),
    re.compile(r"^\s*(?:tribunal|poder judici[aá]rio)\b", re.I),
]


@dataclass(frozen=True)
class Unit:
    locator: str
    text: str
    source_part: str


@dataclass
class Extracted:
    path: str
    sha256: str
    format: str
    units: list[Unit]
    structural: dict
    extraction_confidence: float
    warnings: list[str]

    @property
    def visible_text(self) -> str:
        return "\n".join(unit.text for unit in self.units if unit.text.strip())


def _normalized_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "")
    value = value.replace("\u00a0", " ")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\s+\n", "\n", value)
    return value.strip()


def _is_protocol_noise(value: str) -> bool:
    return any(pattern.search(value) for pattern in PROTOCOL_NOISE)


def comparable_units(units: Iterable[Unit], *, cross_format: bool = False) -> list[Unit]:
    result = []
    for unit in units:
        text = _normalized_text(unit.text)
        if not text:
            continue
        if cross_format and _is_protocol_noise(text):
            continue
        if cross_format and unit.source_part.startswith("word/") and unit.source_part != "word/document.xml":
            continue
        result.append(Unit(unit.locator, text, unit.source_part))
    return result


def _paragraph_text(element: ET.Element) -> tuple[str, dict]:
    pieces: list[str] = []
    stats = {"inserted": 0, "deleted": 0}

    def visit(node: ET.Element, deleted: bool = False) -> None:
        local = node.tag.rsplit("}", 1)[-1]
        now_deleted = deleted or local == "del"
        if local == "del":
            stats["deleted"] += 1
        if local == "ins":
            stats["inserted"] += 1
        if local in {"t", "tab", "br", "cr"} and not now_deleted:
            if local == "t":
                pieces.append(node.text or "")
            elif local == "tab":
                pieces.append("\t")
            else:
                pieces.append("\n")
        for child in list(node):
            visit(child, now_deleted)

    visit(element)
    return _normalized_text("".join(pieces)), stats


def _docx_part_units(raw: bytes, part: str) -> tuple[list[Unit], dict]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise ForjaN3Error(f"XML DOCX inválido em {part}: {exc}") from exc
    units: list[Unit] = []
    inserted = deleted = tables = text_boxes = 0
    paragraphs = list(root.iter(f"{W}p"))
    for index, paragraph in enumerate(paragraphs, 1):
        text, stats = _paragraph_text(paragraph)
        inserted += stats["inserted"]
        deleted += stats["deleted"]
        if text:
            units.append(Unit(f"{part}:p{index}", text, part))
    tables = sum(1 for _ in root.iter(f"{W}tbl"))
    text_boxes = sum(1 for element in root.iter() if element.tag.rsplit("}", 1)[-1] in {"txbxContent", "textbox"})
    return units, {
        "paragraphs": len(paragraphs),
        "tables": tables,
        "textBoxes": text_boxes,
        "insertions": inserted,
        "deletions": deleted,
    }


def extract_docx(path: Path) -> Extracted:
    parts = ["word/document.xml"]
    units: list[Unit] = []
    structural_parts: dict[str, dict] = {}
    warnings: list[str] = []
    comments = 0
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        parts.extend(sorted(name for name in names if re.fullmatch(r"word/(?:header|footer)\d+\.xml", name)))
        parts.extend(name for name in ("word/footnotes.xml", "word/endnotes.xml") if name in names)
        for part in parts:
            if part not in names:
                continue
            part_units, stats = _docx_part_units(archive.read(part), part)
            units.extend(part_units)
            structural_parts[part] = stats
        if "word/comments.xml" in names:
            root = ET.fromstring(archive.read("word/comments.xml"))
            comments = sum(1 for _ in root.iter(f"{W}comment"))
        if "word/vbaProject.bin" in names:
            warnings.append("DOCX contém macro VBA")
        external_links = [
            name for name in names
            if name.endswith(".rels") and b'TargetMode="External"' in archive.read(name)
        ]
        if external_links:
            warnings.append(f"DOCX contém {len(external_links)} parte(s) com vínculo externo")
    structural = {
        "parts": structural_parts,
        "comments": comments,
        "trackChanges": {
            "insertions": sum(part["insertions"] for part in structural_parts.values()),
            "deletions": sum(part["deletions"] for part in structural_parts.values()),
            "visiblePolicy": "accepted_view",
        },
    }
    return Extracted(str(path), sha256_file(path), "docx", units, structural, 1.0, warnings)


def extract_pdf(path: Path, *, allow_ocr: bool = False) -> Extracted:
    units: list[Unit] = []
    warnings: list[str] = []
    pages = 0
    confidence = 1.0
    try:
        import fitz

        document = fitz.open(path)
        pages = len(document)
        for page_index, page in enumerate(document, 1):
            blocks = sorted(page.get_text("blocks"), key=lambda item: (round(item[1], 1), item[0]))
            for block_index, block in enumerate(blocks, 1):
                text = _normalized_text(str(block[4] or ""))
                if text:
                    units.append(Unit(f"pdf:p{page_index}:b{block_index}", text, f"page:{page_index}"))
        if not units and allow_ocr:
            try:
                import pytesseract
                from PIL import Image

                for page_index, page in enumerate(document, 1):
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, lang="por")
                    words = [
                        word for word, raw_conf in zip(data["text"], data["conf"])
                        if word.strip() and float(raw_conf) >= 0
                    ]
                    raw_confidences = [
                        float(raw_conf) for raw_conf in data["conf"] if float(raw_conf) >= 0
                    ]
                    if words:
                        units.append(Unit(f"pdf:p{page_index}:ocr", " ".join(words), f"page:{page_index}"))
                    if raw_confidences:
                        confidence = min(confidence, sum(raw_confidences) / len(raw_confidences) / 100.0)
                warnings.append("PDF extraído por OCR")
            except Exception as exc:
                warnings.append(f"OCR indisponível: {type(exc).__name__}")
        document.close()
    except ImportError:
        try:
            from pypdf import PdfReader

            reader = PdfReader(str(path))
            pages = len(reader.pages)
            for page_index, page in enumerate(reader.pages, 1):
                for block_index, text in enumerate((page.extract_text() or "").splitlines(), 1):
                    text = _normalized_text(text)
                    if text:
                        units.append(Unit(f"pdf:p{page_index}:l{block_index}", text, f"page:{page_index}"))
            warnings.append("PDF sem coordenadas: fallback pypdf")
            confidence = 0.9
        except ImportError as exc:
            raise ForjaN3Error("extração PDF exige PyMuPDF ou pypdf") from exc
    if not units:
        confidence = 0.0
        warnings.append("PDF sem texto extraível")
    return Extracted(
        str(path),
        sha256_file(path),
        "pdf",
        units,
        {"pages": pages, "ocrUsed": any("OCR" in warning for warning in warnings)},
        confidence,
        warnings,
    )


def extract_document(path: Path, *, allow_ocr: bool = False) -> Extracted:
    path = path.resolve()
    if not path.is_file():
        raise ForjaN3Error(f"documento ausente: {path}")
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ForjaN3Error(f"formato não comparável: {suffix}")
    if suffix == ".docx":
        return extract_docx(path)
    if suffix == ".pdf":
        return extract_pdf(path, allow_ocr=allow_ocr)
    units = [
        Unit(f"text:l{index}", _normalized_text(line), "text")
        for index, line in enumerate(path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), 1)
        if _normalized_text(line)
    ]
    return Extracted(str(path), sha256_file(path), suffix.lstrip("."), units, {"lines": len(units)}, 1.0, [])


def classify_change(before: str, after: str) -> tuple[str, str, str, float, list[str]]:
    joined = f"{before}\n{after}"
    reasons: list[str] = []
    compact_before = re.sub(r"\W+", "", before.casefold())
    compact_after = re.sub(r"\W+", "", after.casefold())
    if compact_before == compact_after and before != after:
        return "copy_style_voice", "style_preference", "não_material", 0.99, ["deterministic:typographic_only"]
    polarity_terms = {
        token.casefold()
        for token in re.findall(
            r"\b(?:não|nunca|jamais|sem|somente|apenas|exclusivamente|todo|toda|todos|todas|"
            r"nenhum|nenhuma|qualquer|sempre|integral(?:mente)?|parcial(?:mente)?)\b",
            joined,
            re.I,
        )
    }
    before_polarity = {term for term in polarity_terms if re.search(rf"\b{re.escape(term)}\b", before, re.I)}
    after_polarity = {term for term in polarity_terms if re.search(rf"\b{re.escape(term)}\b", after, re.I)}
    if before_polarity != after_polarity:
        return "reasoning", "reasoning", "material", 0.98, ["deterministic:polarity_or_quantifier"]
    patterns = [
        ("procedural_identity", r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b|\b(?:relator(?:a)?|[0-9]+[ªa]\s+(?:turma|c[aâ]mara)|classe\s+processual)\b"),
        ("authority_citation", r"\b(?:STF|STJ|TJ[A-Z]{2}|TRF\d|REsp|AREsp|AgInt|s[uú]mula|precedente|ac[oó]rd[aã]o)\b"),
        ("request_relief", r"\b(?:requer|pedido|provimento|improvimento|condena[cç][aã]o|efeito suspensivo|subsidiari)\w*"),
        ("calculation", r"R\$\s*\d[\d.,]*|\d[\d.,]*\s*%|\b(?:juros|corre[cç][aã]o|[ií]ndice|quantum|valor|c[aá]lculo)\b"),
        ("evidence_annex", r"\b(?:anexo|documento|prova|laudo|fls?\.|id\s*\d+)\b"),
        ("legal_rule", r"\b(?:art(?:igo)?\.?\s*\d+|lei\s*n?[ºo.]?\s*\d+|c[oó]digo|constitui[cç][aã]o|regimento)\b"),
        ("signature_protocol", r"\b(?:OAB|assinado|protocolo|protocolado|data)\b"),
        ("fact", r"\b\d{1,2}/\d{1,2}/\d{4}\b|\b(?:autor(?:a|es|as)?|r[eé](?:u|us)?|empresa|contrato|fato|evento)\b"),
        ("reasoning", r"\b(?:portanto|porque|assim|contudo|premissa|conclui|raz[aã]o|distin[cç][aã]o)\b"),
    ]
    layer = "unknown"
    for candidate, pattern in patterns:
        if re.search(pattern, joined, re.I):
            layer = candidate
            reasons.append(f"deterministic:{candidate}")
            break
    if not before.strip() or not after.strip():
        reasons.append("insertion_or_deletion")
    cause = LAYER_CAUSE.get(layer)
    if cause is None or layer not in LAYERS:
        return "unknown", "other", "incerto", 0.0, ["default_deny"]
    impact = "material" if layer in MATERIAL_LAYERS else "não_material"
    confidence = 0.92 if reasons and layer != "unknown" else 0.35
    return layer, cause, impact, confidence, reasons


TOKEN_RE = re.compile(
    r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}|"
    r"R\$|"
    r"\d+(?:[.,]\d+)*(?:%|º|ª)?|"
    r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ]+)*|"
    r"§|[^\s\w]",
    re.UNICODE,
)


def _tokens_with_locators(units: list[Unit]) -> tuple[list[str], list[str]]:
    tokens: list[str] = []
    locators: list[str] = []
    for unit in units:
        for token in TOKEN_RE.findall(unit.text):
            tokens.append(token)
            locators.append(unit.locator)
    return tokens, locators


def _unique_ordered(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _change_regions(opcodes: list[tuple[str, int, int, int, int]], *, bridge_tokens: int = 18):
    """Atribui um localizador de região sem fundir alterações semanticamente distintas."""
    region: list[tuple[int, tuple[str, int, int, int, int]]] = []
    for opcode_index, opcode in enumerate(opcodes):
        tag, i1, i2, j1, j2 = opcode
        if tag == "equal":
            gap = max(i2 - i1, j2 - j1)
            if region and gap <= bridge_tokens:
                region.append((opcode_index, opcode))
                continue
            if region:
                yield region
                region = []
            continue
        region.append((opcode_index, opcode))
    if region:
        yield region


def compare_documents(baseline_path: Path, human_path: Path, *, allow_ocr: bool = False) -> dict:
    baseline = extract_document(baseline_path, allow_ocr=allow_ocr)
    human = extract_document(human_path, allow_ocr=allow_ocr)
    cross_format = baseline.format != human.format
    before_units = comparable_units(baseline.units, cross_format=cross_format)
    after_units = comparable_units(human.units, cross_format=cross_format)
    before_tokens, before_locators = _tokens_with_locators(before_units)
    after_tokens, after_locators = _tokens_with_locators(after_units)
    matcher = SequenceMatcher(
        a=[token.casefold() for token in before_tokens],
        b=[token.casefold() for token in after_tokens],
        autojunk=False,
    )
    changes: list[dict] = []
    fingerprint_occurrences: Counter[str] = Counter()
    opcodes = matcher.get_opcodes()
    retained = sum(
        tag == "equal" and max(i2 - i1, j2 - j1) > 18
        for tag, i1, i2, j1, j2 in opcodes
    )
    # Quanto do texto os dois documentos têm em comum. Serve para responder uma
    # pergunta anterior a qualquer diff: a peça humana é REVISÃO da nossa, ou é
    # outro documento? Quando é outro documento, o alinhamento de blocos casa
    # trechos sem relação e cada par produz uma "mudança" com classificação e
    # confiança altas — ruído que se acumula e passa por padrão do escritório.
    equal_tokens = sum(i2 - i1 for tag, i1, i2, _j1, _j2 in opcodes if tag == "equal")
    shared_ratio = 2 * equal_tokens / max(1, len(before_tokens) + len(after_tokens))
    change_index = 0
    for region_index, region in enumerate(_change_regions(opcodes), 1):
        region_id = f"region-{region_index:04d}"
        for _opcode_index, (tag, i1, i2, j1, j2) in region:
            if tag == "equal":
                continue
            change_index += 1
            operation = {"insert": "added", "delete": "removed"}.get(tag, "modified")
            before = " ".join(before_tokens[i1:i2])
            after = " ".join(after_tokens[j1:j2])
            layer, cause, impact, confidence, reason_codes = classify_change(before, after)
            fingerprint_base = canonical_hash({
                "operation": operation,
                "before": before,
                "after": after,
                "baselineLocator": _unique_ordered(before_locators[i1:i2]),
                "humanLocator": _unique_ordered(after_locators[j1:j2]),
            })
            fingerprint_occurrences[fingerprint_base] += 1
            fingerprint = canonical_hash({
                "base": fingerprint_base,
                "occurrence": fingerprint_occurrences[fingerprint_base],
            })
            changes.append({
                "changeId": f"chg-{change_index:04d}",
                "changeFingerprint": fingerprint,
                "regionId": region_id,
                "operation": operation,
                "before": before,
                "after": after,
                "baselineLocator": _unique_ordered(before_locators[i1:i2]),
                "humanLocator": _unique_ordered(after_locators[j1:j2]),
                "layer": layer,
                "cause": cause,
                "impact": impact,
                "confidence": round(confidence, 2),
                "origin": "unknown",
                "scopeCeiling": "case",
                "intent": "[INFERÊNCIA] não determinada pela edição documental",
                "sourceSupport": [],
                "reasonCodes": reason_codes,
                "reviewDecision": "pending",
            })
    baseline_pages = baseline.structural.get("pages")
    human_pages = human.structural.get("pages")
    if baseline.format == human.format == "pdf" and baseline_pages != human_pages:
        change_index += 1
        page_change_fingerprint = canonical_hash({
            "operation": "modified",
            "before": f"pages={baseline_pages}",
            "after": f"pages={human_pages}",
            "baselineLocator": ["pdf:document"],
            "humanLocator": ["pdf:document"],
        })
        changes.append({
            "changeId": f"chg-{change_index:04d}",
            "changeFingerprint": page_change_fingerprint,
            "regionId": "region-structural-page-count",
            "operation": "modified",
            "before": f"pages={baseline_pages}",
            "after": f"pages={human_pages}",
            "baselineLocator": ["pdf:document"],
            "humanLocator": ["pdf:document"],
            "layer": "format_layout",
            "cause": "visual",
            "impact": "não_material",
            "confidence": 1.0,
            "origin": "unknown",
            "scopeCeiling": "case",
            "intent": "[INFERÊNCIA] não determinada pela edição documental",
            "sourceSupport": [],
            "reasonCodes": ["deterministic:page_count"],
            "reviewDecision": "pending",
        })
    material = sum(item["impact"] == "material" for item in changes)
    unknown = sum(item["layer"] == "unknown" for item in changes)
    payload = {
        "schemaVersion": 1,
        "comparisonVersion": "FORJA-POST-PROTOCOL-DIFF-v1",
        "baseline": {
            "path": baseline.path,
            "sha256": baseline.sha256,
            "format": baseline.format,
            "structural": baseline.structural,
            "warnings": baseline.warnings,
            "extractionConfidence": baseline.extraction_confidence,
        },
        "humanArtifact": {
            "path": human.path,
            "sha256": human.sha256,
            "format": human.format,
            "structural": human.structural,
            "warnings": human.warnings,
            "extractionConfidence": human.extraction_confidence,
        },
        "comparisonPolicy": {
            "visibleCanon": "accepted_view",
            "commentsLearned": False,
            "crossFormat": cross_format,
            "protocolNoiseSuppressed": cross_format,
            "layoutConclusionAllowed": not cross_format,
            "bodyComparedSeparately": cross_format and (baseline.format == "docx" or human.format == "docx"),
        },
        "structuralFlowNotes": {
            "baselineNonBodyParts": sorted(
                part for part in (baseline.structural.get("parts") or {}) if part != "word/document.xml"
            ),
            "humanNonBodyParts": sorted(
                part for part in (human.structural.get("parts") or {}) if part != "word/document.xml"
            ),
        },
        "summary": {
            "changeCount": len(changes),
            "materialCount": material,
            "nonMaterialCount": len(changes) - material,
            "unknownCount": unknown,
            "retainedBlockRuns": retained,
            "sharedTokenRatio": round(shared_ratio, 4),
            "byLayer": dict(sorted(Counter(item["layer"] for item in changes).items())),
        },
        "changes": changes,
    }
    payload["comparisonHash"] = canonical_hash(payload)
    return payload


def render_markdown(comparison: dict, *, protocol_status: str, baseline_artifact_id: str, human_artifact_id: str) -> str:
    baseline = comparison["baseline"]
    human = comparison["humanArtifact"]
    summary = comparison["summary"]
    lines = [
        "# Mudanças da última versão da IA para a peça humana retornada",
        "",
        "## Identidade dos artefatos",
        "",
        f"- Versão-base da FORJA: `{baseline_artifact_id}`",
        f"- SHA-256 da base: `{baseline['sha256']}`",
        f"- Peça humana: `{human_artifact_id}`",
        f"- SHA-256 da peça humana: `{human['sha256']}`",
        f"- Estado do protocolo: `{protocol_status}`",
        f"- Hash da comparação: `{comparison['comparisonHash']}`",
        "",
        "## Resumo executivo",
        "",
        f"- Mudanças detectadas: {summary['changeCount']}",
        f"- Materiais: {summary['materialCount']}",
        f"- Não materiais: {summary['nonMaterialCount']}",
        f"- Incertas: {summary['unknownCount']}",
        f"- Blocos preservados: {summary['retainedBlockRuns']}",
        "",
        "## Mudanças materiais",
        "",
    ]
    material_changes = [item for item in comparison["changes"] if item["impact"] == "material"]
    if not material_changes:
        lines.append("- Nenhuma mudança material detectada automaticamente.")
    for item in material_changes:
        before_summary = _normalized_text(item["before"])[:240] or "(inserção)"
        after_summary = _normalized_text(item["after"])[:240] or "(remoção)"
        lines.extend([
            f"### {item['changeId']} — {item['layer']}",
            "",
            f"- Classificação: `{item['cause']}`; confiança {item['confidence']:.2f}; revisão `{item['reviewDecision']}`.",
            f"- Antes, em `{', '.join(item['baselineLocator']) or 'sem localizador'}`: {before_summary}",
            f"- Depois, em `{', '.join(item['humanLocator']) or 'sem localizador'}`: {after_summary}",
            "- Origem intelectual: `unknown`; o sistema não atribui intenção ao advogado.",
            "",
        ])
    lines.extend(["## Estrutura, voz e visual", ""])
    soft_changes = [item for item in comparison["changes"] if item["impact"] != "material"]
    if not soft_changes:
        lines.append("- Nenhuma mudança não material detectada.")
    for item in soft_changes:
        lines.append(
            f"- `{item['changeId']}`: {item['operation']} em `{item['layer']}`; "
            f"locadores IA `{', '.join(item['baselineLocator']) or '-'}` e humano `{', '.join(item['humanLocator']) or '-'}`."
        )
    lines.extend([
        "",
        "## Itens preservados",
        "",
        f"- {summary['retainedBlockRuns']} sequência(s) de blocos foram mantidas sem alteração.",
        f"- Texto em comum entre os dois documentos: {summary.get('sharedTokenRatio', 0):.1%}.",
        "",
        "## Revisão e aprendizado",
        "",
        "- Mudanças materiais exigem conferência na fonte antes de qualquer uso jurídico.",
        "- Toda origem chega como `unknown` e fica limitada ao caso até decisão registrada.",
        "- Preferência isolada de estilo não vira regra ampla.",
        "- As decisões de promoção ou rejeição ficam no ledger F10 e nos testes associados.",
        "",
    ])
    return "\n".join(lines)


def write_comparison(
    baseline_path: Path,
    human_path: Path,
    *,
    json_path: Path,
    markdown_path: Path,
    protocol_status: str,
    baseline_artifact_id: str,
    human_artifact_id: str,
    allow_ocr: bool = False,
) -> dict:
    comparison = compare_documents(baseline_path, human_path, allow_ocr=allow_ocr)
    atomic_write_json(json_path, comparison)
    atomic_write_text(
        markdown_path,
        render_markdown(
            comparison,
            protocol_status=protocol_status,
            baseline_artifact_id=baseline_artifact_id,
            human_artifact_id=human_artifact_id,
        ),
    )
    return comparison


def main() -> None:
    parser = argparse.ArgumentParser(description="Compara a versão exata da FORJA com a peça humana retornada")
    parser.add_argument("baseline", type=Path)
    parser.add_argument("human", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument("--protocol-status", default="human_final_received")
    parser.add_argument("--baseline-artifact-id", default="forja-delivered")
    parser.add_argument("--human-artifact-id", default="human-return")
    parser.add_argument("--allow-ocr", action="store_true")
    args = parser.parse_args()
    result = write_comparison(
        args.baseline,
        args.human,
        json_path=args.json,
        markdown_path=args.markdown,
        protocol_status=args.protocol_status,
        baseline_artifact_id=args.baseline_artifact_id,
        human_artifact_id=args.human_artifact_id,
        allow_ocr=args.allow_ocr,
    )
    print(json.dumps({"comparisonHash": result["comparisonHash"], "summary": result["summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
