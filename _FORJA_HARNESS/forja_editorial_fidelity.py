"""Gates determinísticos da revisão editorial final.

O modelo pode melhorar a forma, mas não certifica a própria fidelidade. Este
módulo recompõe hashes e invariantes diretamente dos arquivos produzidos na
tentativa F7. Qualquer divergência material reprova a promoção.

Desde 25/07/2026 também recompõe a independência entre quem escreveu e quem
revisou o texto: modelo fora da allowlist reprova, e revisão sem segunda família
identificada não passa de `unverified`, que não libera entrega em modo algum.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import forja_editorial_model as editorial_model
from forja_estilo_humano import analisar
from forja_n3_common import read_json, sha256_file


PROTOCOL_VERSION = "FORJA-FABLE5-FINAL-v1"

_NUMBER = re.compile(r"(?<![\w])(?:R\$\s*)?\d[\d.,/%\-–—]*(?![\w])", re.I)
_PROCESS_MARKER = re.compile(
    r"\b(?:e[-\s]?STJ\s+fls?\.?\s*\d[\d./-]*|evento\s+\d[\d./-]*|"
    r"ID\s+[A-Za-z0-9._/-]+|Doc\.?\s*\d[\d./-]*)\b",
    re.I,
)
_AUTHORITY = re.compile(
    r"\b(?:art(?:igo)?s?\.?\s*\d+[\wº°.,/\-]*|Lei\s+n?[º°.]?\s*\d[\d./-]*|"
    r"S[úu]mula\s+n?[º°.]?\s*\d+|Tema\s+n?[º°.]?\s*\d+|"
    r"(?:REsp|AREsp|EREsp|RMS|RHC|HC|MS|CC|Rcl|RECL|SLS|SS|"
    r"RE|ARE|ADI|ADC|ADO|ADPF|MI|PET|INQ|AP|EXT|AgInt|AgRg|EDcl|AI)"
    r"\s+n?[º°.]?\s*[\d.\-/]+)",
    re.I,
)
_SEMANTIC_POLARITY = re.compile(
    r"\b(n[ãa]o|jamais|vedad\w*|autoriz\w*|permit\w*|imped\w*|afast\w*|"
    r"aplic\w*|inaplic\w*|obrig\w*|proib\w*|admit\w*|inadmit\w*|"
    r"provimento|improvimento|prescri\w*|decad\w*)\b",
    re.I,
)
_QUOTED = re.compile(r"[\"“]([^\"”\n]{4,})[\"”]")
_AUDIT_MARKER = re.compile(
    r"\[(?:VERIFICAR|N[ÃA]O\s+VERIFICADO|FONTE:[^\]]+|DECLARA[ÇC][ÃA]O[^\]]*|INFER[ÊE]NCIA)\]",
    re.I,
)
_PEDIDOS_TITLE = re.compile(
    r"^(?:[IVXLCDM]+[.\-–—)]?\s*)?(?:DOS?\s+)?PEDIDOS?\b.*$", re.I
)
_OPERATIONAL_ORIGIN = [
    re.compile(r"\barquivo\s+(?:local|compartilhado\s+pelo\s+escrit[óo]rio)\b", re.I),
    re.compile(r"\blocalizad[oa]\s+na\s+pasta\b", re.I),
    re.compile(r"\brecebid[oa]\s+(?:por|via)\s+WhatsApp\b", re.I),
    re.compile(r"\bGoogle\s+Drive\b", re.I),
    re.compile(r"(?:[A-Za-z]:\\Users\\|/Users/|/home/)[^\s]+", re.I),
    # Lacuna achada em 04/08/2026 ao instalar o detector também na F6: a lista
    # pegava "recebido por WhatsApp" e deixava passar "enviado por WhatsApp",
    # "encaminhado por e-mail" e "compartilhado pelo cliente" — todas formas que
    # o protocolo de 11/07 proíbe expressamente no corpo da peça.
    #
    # O risco aqui é o oposto do de sempre: mencionar e-mail pode ser FATO DA
    # CAUSA legítimo ("o requerimento foi protocolado por e-mail em 2021" é o
    # eixo do caso CASO-17). Por isso os padrões exigem o verbo de recebimento
    # ou de compartilhamento colado ao canal — que é o que revela origem
    # operacional —, e não a palavra "e-mail" solta. Medido contra os treze
    # rascunhos reais do acervo: zero ocorrências.
    re.compile(r"\b(?:receb|envi|encaminh)[a-zç]*\s+(?:por|via)\s+e-?mail\b", re.I),
    re.compile(r"\b(?:envi|encaminh)[a-zç]*\s+(?:por|via)\s+WhatsApp\b", re.I),
    re.compile(r"\bcompartilhad[oa]\s+(?:por|pelo|pela)\b", re.I),
]


def _fold(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    return " ".join(value.casefold().split())


def _counter(pattern: re.Pattern, text: str) -> Counter:
    values = []
    for match in pattern.finditer(text):
        value = match.group(1) if match.lastindex else match.group(0)
        normalized = _fold(value)
        # Pontuação sintática imediatamente após número/autoridade/marcador não
        # integra o identificador e pode mudar legitimamente na reescrita.
        if pattern in {_NUMBER, _PROCESS_MARKER, _AUTHORITY}:
            normalized = normalized.rstrip(".,;:")
        values.append(normalized)
    return Counter(values)


def _is_upper_title(value: str) -> bool:
    letters = "".join(char for char in value if char.isalpha())
    return bool(letters) and letters == letters.upper()


def _heading_counter(text: str) -> Counter:
    headings = []
    for line in text.splitlines():
        stripped = line.strip()
        markdown = re.match(r"^#{1,6}\s+(.+?)\s*#*$", stripped)
        if markdown:
            headings.append(_fold(markdown.group(1)))
        elif 3 <= len(stripped) <= 180 and _is_upper_title(stripped):
            headings.append(_fold(stripped))
    return Counter(headings)


def _pedidos(text: str) -> str | None:
    offset = 0
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        markdown = re.match(r"^#{1,6}\s+(.+?)\s*#*$", stripped)
        title = markdown.group(1).strip() if markdown else stripped
        is_real_heading = bool(markdown) or _is_upper_title(stripped)
        if is_real_heading and _PEDIDOS_TITLE.match(title):
            return _fold(text[offset:])
        offset += len(line)
    return None


def _counter_delta(source: Counter, final: Counter) -> dict:
    removed = list((source - final).elements())
    added = list((final - source).elements())
    return {"removed": removed[:20], "added": added[:20]}


def _authority_semantic_counter(text: str) -> Counter:
    """Assinatura lexical de polaridade ligada a cada autoridade na frase."""
    values = []
    for sentence in re.split(r"(?<=[.!?;:])\s+|\n+", text):
        authorities = [_fold(match.group(0)).rstrip(".,;:") for match in _AUTHORITY.finditer(sentence)]
        if not authorities:
            continue
        semantics = [
            re.sub(r"(?:ando|endo|indo|ado|ida|ido|ar|er|ir|a|e|o|s)$", "", _fold(match.group(0)))
            for match in _SEMANTIC_POLARITY.finditer(sentence)
        ]
        for authority in authorities:
            values.append(authority + "|" + ",".join(semantics))
    return Counter(values)


def _finding(gate: str, detail: str, **extra) -> dict:
    return {"gate": gate, "severity": "P0", "detail": detail, **extra}


def _family_findings(report: dict, strict: bool) -> list[dict]:
    """Recompõe a independência entre produtor e revisor a partir do relatório.

    A garantia declarada não é aceita como está: é recalculada das fichas dos
    dois modelos. Bundles anteriores à emenda E14 não trazem as fichas e ficam
    em `unverified`, que bloqueia — é o comportamento correto, porque a
    independência daquelas execuções de fato não foi verificada.
    """
    declared = report.get("familyAssurance")
    producer = report.get("producerModel") or {}
    reviewer = report.get("reviewerModel") or {}
    recomputed = editorial_model.family_assurance(
        producer.get("canonicalId") if isinstance(producer, dict) else None,
        reviewer.get("canonicalId") if isinstance(reviewer, dict) else None,
        producer_session=producer.get("sessionId") if isinstance(producer, dict) else None,
        reviewer_session=reviewer.get("sessionId") if isinstance(reviewer, dict) else None,
    )
    if declared is not None and declared != recomputed:
        return [_finding(
            "cross_model_review_verified",
            "a garantia de independência declarada não coincide com a recomposta",
            declared=declared, recomputed=recomputed,
        )]
    if recomputed == editorial_model.UNVERIFIED:
        return [_finding(
            "cross_model_review_verified",
            "a revisão do texto final não identifica um segundo modelo; a independência "
            "entre produtor e revisor não foi verificada",
        )]
    if recomputed == editorial_model.SAME_FAMILY and strict:
        return [_finding(
            "cross_model_review_verified",
            "o modo estrito exige revisão por família distinta de modelo; a execução "
            "registrou apenas sessões diferentes da mesma família",
        )]
    return []


def validate_editorial_bundle(
    audited_path: Path,
    final_path: Path,
    report_path: Path,
    usage_path: Path | None = None,
    *,
    expected_model: str | None = None,
    strict_family: bool = False,
) -> dict:
    """Valida o bundle F7-B sem confiar em declarações do modelo."""
    audited_path = Path(audited_path)
    final_path = Path(final_path)
    report_path = Path(report_path)
    source = audited_path.read_text(encoding="utf-8", errors="replace")
    final = final_path.read_text(encoding="utf-8", errors="replace")
    report = read_json(report_path, None)
    source_hash = sha256_file(audited_path)
    final_hash = sha256_file(final_path)
    findings: list[dict] = []

    if not isinstance(report, dict):
        findings.append(_finding("editorial_report_valid", "relatório editorial ausente ou inválido"))
        report = {}
    if report.get("protocolVersion") != PROTOCOL_VERSION:
        findings.append(_finding("editorial_protocol_match", "versão do protocolo Fable 5 divergente"))
    if report.get("sourceSha256") != source_hash:
        findings.append(_finding(
            "editorial_source_hash_match",
            "hash do texto auditado não coincide com o relatório editorial",
            expected=source_hash,
            reported=report.get("sourceSha256"),
        ))
    if report.get("finalSha256") != final_hash:
        findings.append(_finding(
            "editorial_final_hash_match",
            "hash do texto final não coincide com o relatório editorial",
            expected=final_hash,
            reported=report.get("finalSha256"),
        ))
    reported_model = report.get("model")
    if expected_model is not None and reported_model != expected_model:
        findings.append(_finding(
            "editor_model_confirmed",
            "a execução não comprova o modelo editorial declarado no contrato do run",
            expected=expected_model,
            reported=reported_model,
        ))
    elif not editorial_model.is_authorized(reported_model):
        findings.append(_finding(
            "editor_model_confirmed",
            "o modelo que assina a reescrita não consta da allowlist editorial",
            reported=reported_model,
        ))
    if report.get("billing") != "assinatura OAuth Claude Max (sem API key)":
        findings.append(_finding(
            "editor_model_confirmed",
            "a execução não comprova uso da assinatura OAuth Claude Max",
            reported=report.get("billing"),
        ))
    findings.extend(_family_findings(report, strict_family))
    fable_report = report.get("fableReport") or {}
    if not isinstance(fable_report, dict) or fable_report.get("sourceHash") != source_hash:
        findings.append(_finding(
            "editorial_model_source_hash_match",
            "o relatório devolvido pelo Fable 5 não confirma o hash real de origem",
        ))

    if usage_path is not None:
        usage = read_json(Path(usage_path), None)
        if not isinstance(usage, dict):
            findings.append(_finding("editor_usage_valid", "evidência da sessão editorial ausente ou inválida"))
            usage = {}
        usage_checks = {
            # O modelo medido no envelope precisa ser o mesmo que assina o
            # relatório: são duas origens distintas para o mesmo fato.
            "model": reported_model,
            "authMethod": "claude.ai",
            "subscriptionType": "max",
            "sourceSha256": source_hash,
            "finalSha256": final_hash,
        }
        for key, expected in usage_checks.items():
            if usage.get(key) != expected:
                findings.append(_finding(
                    "editor_usage_valid",
                    f"evidência da sessão diverge em {key}",
                    expected=expected,
                    reported=usage.get(key),
                ))
        if not str(usage.get("sessionId") or "").strip():
            findings.append(_finding("editor_usage_valid", "sessionId do Claude Code não foi registrado"))

    invariants = {
        "numbers_preserved": (_NUMBER, "números, datas ou valores"),
        "process_markers_preserved": (_PROCESS_MARKER, "marcadores processuais"),
        "authorities_preserved": (_AUTHORITY, "autoridades normativas ou precedentes"),
        "quotes_preserved": (_QUOTED, "trechos entre aspas"),
        "audit_markers_preserved": (_AUDIT_MARKER, "marcadores de auditoria ou ressalva"),
    }
    for gate, (pattern, label) in invariants.items():
        before = _counter(pattern, source)
        after = _counter(pattern, final)
        if before != after:
            findings.append(_finding(
                gate,
                f"a reescrita alterou {label}",
                delta=_counter_delta(before, after),
            ))

    semantic_before = _authority_semantic_counter(source)
    semantic_after = _authority_semantic_counter(final)
    if semantic_before != semantic_after:
        findings.append(_finding(
            "authority_semantic_polarity_preserved",
            "a reescrita alterou negação, autorização ou efeito jurídico ligado a uma autoridade",
            delta=_counter_delta(semantic_before, semantic_after),
        ))

    source_headings = _heading_counter(source)
    final_headings = _heading_counter(final)
    if source_headings != final_headings:
        findings.append(_finding(
            "headings_preserved",
            "a reescrita alterou, suprimiu ou criou capítulos/títulos",
            delta=_counter_delta(source_headings, final_headings),
        ))
    source_compact = len(re.sub(r"\s+", "", source))
    final_compact = len(re.sub(r"\s+", "", final))
    length_ratio = final_compact / max(1, source_compact)
    if length_ratio < 0.90:
        findings.append(_finding(
            "content_retention_minimum",
            "o texto final reteve menos de 90% do tamanho não branco do texto auditado",
            ratio=round(length_ratio, 4),
        ))

    source_orders = _pedidos(source)
    final_orders = _pedidos(final)
    if source_orders != final_orders:
        findings.append(_finding(
            "pedidos_preserved",
            "o bloco de pedidos e fecho não permaneceu literalmente estável após normalização de espaços",
            sourceFound=source_orders is not None,
            finalFound=final_orders is not None,
        ))

    for pattern in _OPERATIONAL_ORIGIN:
        match = pattern.search(final)
        if match:
            findings.append(_finding(
                "operational_origin_absent",
                "o texto final expõe origem operacional proibida",
                excerpt=match.group(0)[:180],
            ))

    style_p0 = [item for item in analisar(final, "peca") if item.get("sev") == "P0"]
    for item in style_p0:
        findings.append(_finding(
            "human_style_final_pass",
            f"{item.get('gate')}: {item.get('problema')}",
            excerpt=str(item.get("trecho") or "")[:220],
        ))

    gates = {
        "editorial_source_hash_match": "pass" if not any(
            item["gate"] == "editorial_source_hash_match" for item in findings) else "blocked",
        "editorial_fidelity_pass": "pass" if not any(
            item["gate"] in {
                "numbers_preserved", "process_markers_preserved", "authorities_preserved",
                "quotes_preserved", "audit_markers_preserved", "pedidos_preserved",
                "operational_origin_absent", "editorial_final_hash_match", "editorial_report_valid",
                "editorial_protocol_match", "editorial_model_source_hash_match", "headings_preserved",
                "content_retention_minimum",
                "authority_semantic_polarity_preserved",
            } for item in findings) else "blocked",
        "human_style_final_pass": "pass" if not any(
            item["gate"] == "human_style_final_pass" for item in findings) else "blocked",
        "editor_model_confirmed": "pass" if not any(
            item["gate"] in {"editor_model_confirmed", "editor_usage_valid"}
            for item in findings
        ) else "blocked",
        "cross_model_review_verified": "pass" if not any(
            item["gate"] == "cross_model_review_verified" for item in findings
        ) else "blocked",
    }
    return {
        "protocolVersion": PROTOCOL_VERSION,
        "approved": not findings,
        "sourceSha256": source_hash,
        "finalSha256": final_hash,
        "familyAssurance": report.get("familyAssurance"),
        "gates": gates,
        "findings": findings,
        "method": "hashes, invariantes e independência recompostos pelo orquestrador; "
                  "sem autocertificação do modelo",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Gate de fidelidade editorial Fable 5")
    parser.add_argument("audited", type=Path)
    parser.add_argument("final", type=Path)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    result = validate_editorial_bundle(args.audited, args.final, args.report)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["approved"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
