"""Inventário canônico de autoridades jurídicas citadas pela FORJA.

O módulo é deliberadamente lexical: ele não afirma que a autoridade existe.
Sua função é impedir que classes menos usuais ou referências normativas
escapem do ledger probatório. A existência, o teor e a vigência são validados
pelos gates de fonte e revisão humana.
"""

from __future__ import annotations

import re
from collections import OrderedDict


_CNJ = re.compile(
    r"\b(ADI|A[CÇ][AÃ]O\s+DIRETA\s+DE\s+INCONSTITUCIONALIDADE|"
    r"APELA[CÇ][AÃ]O|AGRAVO\s+DE\s+INSTRUMENTO)\s*"
    r"(?:n[oº.]?\s*)?(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})",
    re.I,
)
_STJ = re.compile(
    r"\b(?:AgInt|AgRg|EDcl|EAg|EREsp|EDv)?\s*(?:nos?\s+|no\s+|na\s+)?"
    r"(REsp|AREsp|EREsp|RMS|CC|SLS|SS|IAC)\s*"
    r"(?:n[oº.]?\s*)?([\d.]{3,})(?:\s*[/\-]\s*([A-Z]{2}|STJ))?",
    re.I,
)
_STF = re.compile(
    r"\b(RE|ARE|ADI|ADC|ADO|ADPF|MI|AP|INQ|EXT)\s*"
    r"(?:n[oº.]?\s*)?([\d.]{2,})(?:\s*[/\-]\s*(STF))?"
    r"\b(?!-\d{2}\.\d{4}\.)",
    re.I,
)
_AMBIGUOUS = re.compile(
    r"\b(HC|RHC|MS|RCL|RECL|PET)\s*(?:n[oº.]?\s*)?([\d.]{2,})"
    r"(?:\s*[/\-]\s*(STJ|STF))?",
    re.I,
)
_SUMULA_VINCULANTE = re.compile(
    r"S[úu]mula\s+Vinculante\s+(?:n[oº.]?\s*)?(\d{1,3})",
    re.I,
)
_SUMULA = re.compile(
    r"S[úu]mula\s+(?!Vinculante)(?:n[oº.]?\s*)?(\d{1,4})"
    r"(?:\s*(?:[/]|\s+d[oe]\s+|[-–—]\s*)\s*(STJ|STF))?",
    re.I,
)
_TEMA = re.compile(
    r"Tema\s+(?:Repetitivo\s+)?(?:n[oº.]?\s*)?"
    r"(\d{1,3}(?:\.\d{3})+|\d{1,5})\s*"
    r"(?:(?:d[oe]\s*)|(?:[-–—]\s*))?(STJ|STF)?",
    re.I,
)
_INFORMATIVO = re.compile(
    r"Informativo\s+(?:n[oº.]?\s*)?(\d{2,4})\s*"
    r"(?:(?:d[oe]\s*)|(?:[-–—]\s*))?(STJ|STF)?",
    re.I,
)
_ARTICLE = re.compile(
    r"\bart(?:igo)?s?\.?\s*(\d+[A-Z]?(?:-[A-Z])?)"
    r"(?:\s*,?\s*(?:§§?|incisos?|incs?\.?|al[ií]neas?)\s*[^.;:\n]{0,60})?"
    r"\s+(?:d[oa]\s+)?"
    r"(CPC|CPP|CC|CDC|CF(?:/88)?|CONSTITUI[CÇ][AÃ]O(?:\s+FEDERAL)?|"
    r"CTN|CLT|CP|LEF|LOMAN|RISTJ|RISTF|EOAB|ESTATUTO\s+DA\s+OAB)\b",
    re.I,
)
_LAW = re.compile(
    r"\b(Lei\s+Complementar|Lei|Decreto(?:-Lei)?|Resolu[cç][aã]o|"
    r"Emenda\s+Constitucional)\s*(?:n[oº.]?\s*)?"
    r"(\d[\d.]*)\s*(?:[/\-]\s*(\d{2,4}))?",
    re.I,
)

CNJ_TRIBUNAIS = {
    "4.01": "TRF1", "4.02": "TRF2", "4.03": "TRF3", "4.04": "TRF4",
    "4.05": "TRF5", "4.06": "TRF6", "8.07": "TJDFT", "8.26": "TJSP",
    "8.27": "TJTO", "8.21": "TJRS", "8.19": "TJRJ",
}


def normalize_number(value: str | None) -> str:
    return re.sub(r"\D", "", str(value or ""))


def tribunal_from_cnj(value: str | None) -> str | None:
    match = re.search(
        r"\d{7}-\d{2}\.\d{4}\.(\d)\.(\d{2})\.\d{4}",
        str(value or ""),
    )
    return CNJ_TRIBUNAIS.get(f"{match.group(1)}.{match.group(2)}") if match else None


def authority_key(item: dict) -> tuple[str, str, str]:
    """Identidade estável usada para cobertura do ledger."""
    identity = item.get("authorityIdentity") if isinstance(item, dict) else None
    source = identity if isinstance(identity, dict) else item
    court = str(source.get("court") or source.get("corte") or "").upper()
    kind = str(
        source.get("kind")
        or source.get("classe")
        or source.get("tipo")
        or ""
    ).upper()
    number = normalize_number(
        source.get("number")
        or source.get("numero")
        or source.get("article")
    )
    code = str(source.get("code") or "").upper()
    if kind == "SUMULA_VINCULANTE":
        court = "STF"
    if kind == "ARTICLE":
        court = code
    return court, kind, number


def _context(text: str, start: int, end: int) -> str:
    return re.sub(r"\s+", " ", text[max(0, start - 80):end + 80]).strip()[:240]


def _entry(
    *,
    tipo: str,
    classe: str,
    numero: str,
    corte: str,
    rotulo: str,
    dados: tuple,
    text: str,
    start: int,
    end: int,
    identity: dict | None = None,
) -> dict:
    identity = identity or {
        "court": corte,
        "kind": classe,
        "number": normalize_number(numero),
    }
    return {
        "tipo": tipo,
        "classe": classe,
        "numero": normalize_number(numero),
        "corte": corte,
        "rotulo": rotulo,
        "rótulo": rotulo,
        "dados": dados,
        "contexto": _context(text, start, end),
        "ocorrencias": 1,
        "authorityIdentity": identity,
    }


def extract_authorities(text: str) -> list[dict]:
    """Extrai jurisprudência e normas sem certificar existência ou teor."""
    found: OrderedDict[tuple[str, str, str], dict] = OrderedDict()

    def add(entry: dict) -> None:
        key = authority_key(entry)
        if key in found:
            found[key]["ocorrencias"] += 1
        else:
            found[key] = entry

    for match in _CNJ.finditer(text):
        label, number = match.groups()
        court = tribunal_from_cnj(number) or "TRIBUNAL_NAO_MAPEADO"
        add(_entry(
            tipo="CNJ", classe=label.upper(), numero=number, corte=court,
            rotulo=f"{court} {label.upper()} {number}", dados=match.groups(),
            text=text, start=match.start(), end=match.end(),
        ))

    for pattern, court in ((_STJ, "STJ"), (_STF, "STF")):
        for match in pattern.finditer(text):
            kind, number = match.group(1), match.group(2)
            suffix = (match.group(3) or "").upper()
            effective_court = suffix if suffix in {"STJ", "STF"} else court
            add(_entry(
                tipo=effective_court, classe=kind.upper(), numero=number,
                corte=effective_court,
                rotulo=f"{kind.upper()} {number}/{effective_court}",
                dados=(kind, number, effective_court),
                text=text, start=match.start(), end=match.end(),
            ))

    for match in _AMBIGUOUS.finditer(text):
        kind, number, suffix = match.groups()
        court = (suffix or "TRIBUNAL_AMBIGUO").upper()
        add(_entry(
            tipo=court, classe=kind.upper(), numero=number, corte=court,
            rotulo=f"{kind.upper()} {number}" + (f"/{suffix.upper()}" if suffix else " [TRIBUNAL AMBÍGUO]"),
            dados=(kind, number, suffix),
            text=text, start=match.start(), end=match.end(),
        ))

    for match in _SUMULA_VINCULANTE.finditer(text):
        number = match.group(1)
        add(_entry(
            tipo="SUMULA_VINCULANTE", classe="SUMULA_VINCULANTE",
            numero=number, corte="STF", rotulo=f"Súmula Vinculante {number}",
            dados=(number,), text=text, start=match.start(), end=match.end(),
        ))

    for pattern, tipo, label in (
        (_SUMULA, "SUMULA", "Súmula"),
        (_TEMA, "TEMA", "Tema"),
        (_INFORMATIVO, "INFORMATIVO", "Informativo"),
    ):
        for match in pattern.finditer(text):
            number, suffix = match.groups()
            court = suffix.upper() if suffix else None
            identity = {
                "court": court or "TRIBUNAL_AMBIGUO",
                "kind": tipo,
                "number": normalize_number(number),
            }
            add(_entry(
                tipo=tipo, classe=tipo, numero=number, corte=court,
                rotulo=f"{label} {number}" + (f" {suffix.upper()}" if suffix else ""),
                dados=(number, suffix), text=text,
                start=match.start(), end=match.end(),
                identity=identity,
            ))

    for match in _ARTICLE.finditer(text):
        article, code = match.groups()
        normalized_code = re.sub(r"\s+", "_", code.upper().replace("/88", ""))
        identity = {"kind": "ARTICLE", "code": normalized_code, "article": article.upper()}
        add(_entry(
            tipo="NORMA", classe="ARTICLE", numero=article,
            corte=normalized_code, rotulo=f"art. {article} {code.upper()}",
            dados=(article, normalized_code), text=text,
            start=match.start(), end=match.end(), identity=identity,
        ))

    for match in _LAW.finditer(text):
        kind, number, year = match.groups()
        normalized_kind = re.sub(r"\s+", "_", kind.upper())
        identity = {
            "court": "BR",
            "kind": normalized_kind,
            "number": normalize_number(number),
            "year": normalize_number(year),
        }
        add(_entry(
            tipo="NORMA", classe=normalized_kind, numero=number,
            corte="BR", rotulo=f"{kind} {number}" + (f"/{year}" if year else ""),
            dados=(kind, number, year), text=text,
            start=match.start(), end=match.end(), identity=identity,
        ))

    result = list(found.values())
    grouped: dict[tuple[str, str], list[dict]] = {}
    for item in result:
        if item["tipo"] in {"SUMULA", "TEMA", "INFORMATIVO"}:
            grouped.setdefault((item["tipo"], item["numero"]), []).append(item)
    dropped: set[int] = set()
    for items in grouped.values():
        qualified = [item for item in items if item.get("corte") in {"STJ", "STF"}]
        ambiguous = [item for item in items if item.get("corte") is None]
        if len(qualified) == 1 and ambiguous:
            qualified[0]["ocorrencias"] += sum(item["ocorrencias"] for item in ambiguous)
            dropped.update(id(item) for item in ambiguous)
    return [item for item in result if id(item) not in dropped]
