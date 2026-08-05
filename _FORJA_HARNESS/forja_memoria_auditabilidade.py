"""Memória obrigatória de auditabilidade da FORJA.

O artefato acompanha a minuta para permitir que o advogado reconstrua o que foi
feito, por qual fase, com quais gates e sobre quais versões de artefatos. Ele é
deliberadamente uma memória de processo: não copia autos, transcrições, e-mails,
segredos ou o texto integral da peça.

A implementação gera Markdown, HTML autônomo e um manifesto JSON. A conversão
para HTML é apenas serialização do relatório; não abre DOCX, não chama Word,
PDF, PNG, LibreOffice ou qualquer motor de renderização.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
MEMORY_MD = "MEMORIA_AUDITABILIDADE_FORJA.md"
MEMORY_HTML = "MEMORIA_AUDITABILIDADE_FORJA.html"
MEMORY_JSON = "MEMORIA_AUDITABILIDADE_FORJA.json"

PHASES = {
    "F0_RECONCILIACAO_FILA": "reconciliação da demanda e identidade do caso",
    "F1_INGESTAO_SEGURA": "ingestão protegida e cobertura documental",
    "F2_CLASSIFICACAO_PRODUTO_RISCO": "diagnóstico, classificação e árvore de perguntas",
    "F3_FONTES_REGIMENTO_LEIS": "ledger de fatos, fontes prevalentes e regimento",
    "F4_BLUEPRINT_ESTRATEGICO": "design da estratégia, hipóteses e plano de trabalho",
    "F5_PESQUISA_OFICIAL": "pesquisa e conferência de fontes oficiais",
    "F6_REDACAO_TEMPLATE": "redação da minuta a partir do material auditado",
    "F7_AUDITORIA_JURIDICA_FACTUAL": "auditoria jurídica, factual e de lastro",
    "F8_QA_VISUAL": "materialização estática em OOXML com SVG nativo",
    "F9_PACOTE_REVISAO_DRAFT_OPCIONAL": "pacote de revisão e memória de auditabilidade",
    "F10_ENTREGA_EVIDENCIA_APRENDIZADO": "evidência de entrega e aprendizado",
}

# Memórias antigas usavam estes rótulos antes da consolidação dos contratos F0-F10.
# Eles continuam reconhecidos como aliases de leitura, mas a saída sempre usa o
# identificador canônico do contrato atual.
PHASE_ALIASES = {
    "F1_INGESTAO_SEGURA": {"F1_INGESTAO_COBERTURA"},
    "F4_BLUEPRINT_ESTRATEGICO": {"F4_PLANEJAMENTO_ESTRATEGICO"},
    "F5_PESQUISA_OFICIAL": {"F5_PESQUISA_FONTES_OFICIAIS"},
    "F6_REDACAO_TEMPLATE": {"F6_REDACAO_MINUTA"},
}

PHASE_ALIAS_TO_CANONICAL = {
    alias: canonical
    for canonical, aliases in PHASE_ALIASES.items()
    for alias in aliases
}

CONTROL_NAMES = {
    "FORJA_N3_STATE.json",
    "FORJA_STATE.json",
    "FORJA_PACKAGE.json",
    "COMPUTED_LASTRO_GATES.json",
    "F7_VERIFICADOR_FORJA.json",
    "F8_QA_ESTRUTURAL.json",
    "F8S_ASSINATURA_VISUAL.json",
    "VISUAL_BUILD.json",
    "FIDELIDADE_VISUAL.json",
    "F10_TRILHA_EVIDENCIA.md",
    "F10_DELIVERY_INTEGRITY.json",
    "F10_PROTOCOL_EVIDENCE.json",
    "F10_HUMAN_DIFF_CLASSIFICATION.json",
    "F2_QUESTION_TREE.json",
}


def sha256_file(path: Path, block_size: int = 1024 * 1024) -> str:
    """Calcula SHA-256 em fluxo, inclusive para fontes grandes."""
    import hashlib

    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while True:
            block = handle.read(block_size)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None


def _redact(value: Any) -> str:
    """Mantém a utilidade do bloqueador sem vazar caminhos ou credenciais."""
    text = str(value or "")
    text = re.sub(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*[^\s;|]+", r"\1=<redigido>", text)
    text = re.sub(r"(?i)(?:[A-Z]:[\\/]|\\\\)[^\s;|]+", "<caminho-redigido>", text)
    return text[:600]


def _relative(path: Path, case_dir: Path) -> str:
    try:
        return path.resolve().relative_to(case_dir.resolve()).as_posix()
    except ValueError:
        return f"external:{path.name}"


def _state_path(case_dir: Path) -> Path | None:
    for name in ("FORJA_N3_STATE.json", "FORJA_STATE.json"):
        candidate = case_dir / name
        if candidate.is_file():
            return candidate
    return None


def _state(case_dir: Path) -> tuple[dict[str, Any], Path | None]:
    path = _state_path(case_dir)
    value = _read_json(path) if path else None
    return (value if isinstance(value, dict) else {}, path)


def _phase_status(phase: str, state: dict[str, Any]) -> str:
    aliases = PHASE_ALIASES.get(phase, set())
    completed = set(state.get("completedPhases") or [])
    if phase in completed or completed.intersection(aliases):
        return "completed"
    current = str(state.get("currentPhase") or state.get("phaseCursor") or "")
    if current == phase or current in aliases:
        return "blocked" if state.get("lifecycleStatus") == "blocked" else "in_progress"
    history = [item for item in state.get("phaseHistory") or [] if isinstance(item, dict)]
    if any(str(item.get("phase") or "") == phase or str(item.get("phase") or "") in aliases for item in history):
        return "observed"
    return "not_started"


def _canonical_phase(value: Any) -> str:
    phase = str(value or "")
    return PHASE_ALIAS_TO_CANONICAL.get(phase, phase)


def _artifact_inventory(case_dir: Path, state: dict[str, Any]) -> list[dict[str, Any]]:
    raw = state.get("artifacts") or {}
    items: list[tuple[str, Any]] = []
    if isinstance(raw, dict):
        items = [(str(key), value) for key, value in raw.items()]
    elif isinstance(raw, list):
        items = [(f"artifact_{index + 1}", value) for index, value in enumerate(raw)]
    result = []
    canonical_ledger = case_dir / "n3_artifacts" / "F3_FONTES_REGIMENTO_LEIS" / "fact_ledger.json"
    for artifact_id, entry in sorted(items):
        if isinstance(entry, dict):
            path = Path(str(entry.get("path") or ""))
            declared = str(entry.get("sha256") or "")
            role = _redact(entry.get("role") or "phase_output")
            audience = _redact(entry.get("audience") or "internal_working")
        else:
            path = Path(str(entry or ""))
            declared, role, audience = "", "phase_output", "internal_working"
        historical_fact_ledger = (
            artifact_id == "fact_ledger"
            and canonical_ledger.is_file()
            and path.is_file()
            and path.resolve() != canonical_ledger.resolve()
        )
        if historical_fact_ledger:
            role = "historical_snapshot"
        actual = sha256_file(path) if path.is_file() else None
        result.append({
            "id": artifact_id,
            "path": _relative(path, case_dir) if str(path) else "<ausente>",
            "exists": path.is_file(),
            "size": path.stat().st_size if path.is_file() else None,
            "sha256": actual,
            "declaredSha256": declared or None,
            "hashMatches": bool(actual and declared and actual == declared),
            "role": role,
            "audience": audience,
        })
        if historical_fact_ledger:
            canonical_sha = sha256_file(canonical_ledger)
            result.append({
                "id": "fact_ledger_canonical",
                "path": _relative(canonical_ledger, case_dir),
                "exists": True,
                "size": canonical_ledger.stat().st_size,
                "sha256": canonical_sha,
                "declaredSha256": canonical_sha,
                "hashMatches": True,
                "role": "source_ledger_canonical",
                "audience": "internal_working",
                "sourceOfTruth": True,
            })
    return result


def _control_files(case_dir: Path) -> list[Path]:
    found: list[Path] = []
    for root, dirs, files in os.walk(case_dir):
        # Fontes privadas e autos são representados apenas pelo ledger e seus
        # hashes; não são percorridos nem copiados para a memória.
        dirs[:] = [item for item in dirs if item not in {"private", "sources", "autos", "cache", "raw"}]
        for name in files:
            if name in CONTROL_NAMES:
                found.append(Path(root) / name)
    return sorted(set(found))


def _summary_for_control(path: Path, case_dir: Path) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "path": _relative(path, case_dir),
        "sha256": sha256_file(path),
        "size": path.stat().st_size,
        "kind": "json" if path.suffix.lower() == ".json" else "text",
    }
    payload = _read_json(path) if path.suffix.lower() == ".json" else None
    if isinstance(payload, dict):
        for key in ("schemaVersion", "mode", "status", "approved", "p0", "p1", "p2", "renderingUsed", "pdfCreated", "pngCreated", "currentPhase"):
            if key in payload and isinstance(payload[key], (str, int, float, bool, type(None))):
                entry[key] = payload[key]
        for key in ("findings", "violacoes", "gates", "artifacts", "pages", "facts", "items"):
            if isinstance(payload.get(key), (list, dict)):
                entry[f"{key}Count"] = len(payload[key])
        computed = payload.get("computed")
        if isinstance(computed, dict):
            entry["computed"] = {
                key: computed[key] for key in ("status", "fact_grounding_verbatim", "criterio_vigente", "economic_gates")
                if key in computed and isinstance(computed[key], (str, int, float, bool, type(None)))
            }
    return entry


def _source_summary(case_dir: Path) -> dict[str, Any]:
    candidates = list(case_dir.rglob("fact_ledger.json"))
    if not candidates:
        return {"present": False, "facts": 0, "roles": {}, "statuses": {}}
    path = sorted(candidates)[0]
    payload = _read_json(path)
    facts = payload.get("facts") if isinstance(payload, dict) else payload
    facts = facts if isinstance(facts, list) else []
    roles: dict[str, int] = {}
    statuses: dict[str, int] = {}
    for item in facts:
        if not isinstance(item, dict):
            continue
        role = str(item.get("role") or "sem_role")
        status = str(item.get("status") or item.get("reviewStatus") or "sem_status")
        roles[role] = roles.get(role, 0) + 1
        statuses[status] = statuses.get(status, 0) + 1
    return {
        "present": True,
        "path": _relative(path, case_dir),
        "sha256": sha256_file(path),
        "facts": len(facts),
        "roles": dict(sorted(roles.items())),
        "statuses": dict(sorted(statuses.items())),
        "quotesIncluded": False,
    }


def _visual_summary(controls: list[dict[str, Any]]) -> dict[str, Any]:
    visual = next((item for item in controls if item["path"].endswith("VISUAL_BUILD.json")), {})
    qa = next((item for item in controls if item["path"].endswith("F8_QA_ESTRUTURAL.json")), {})
    return {
        "canonicalRoute": "visual_law_canonica_svg_ooxml",
        "renderingUsed": visual.get("renderingUsed", False),
        "pdfCreated": visual.get("pdfCreated", False),
        "pngCreated": visual.get("pngCreated", False),
        "visualBuildSha256": visual.get("sha256"),
        "staticQaSha256": qa.get("sha256"),
        "humanPaginationReview": "required before strict release; not inferred by static OOXML QA",
    }


def build_payload(case_dir: Path, *, generated_at: str | None = None) -> dict[str, Any]:
    case_dir = Path(case_dir).resolve()
    state, state_path = _state(case_dir)
    if not state_path:
        raise ValueError(f"estado FORJA ausente em {case_dir}")
    generated_at = generated_at or datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    controls = [_summary_for_control(path, case_dir) for path in _control_files(case_dir)]
    history = []
    for item in state.get("phaseHistory") or []:
        if not isinstance(item, dict):
            continue
        phase = _canonical_phase(item.get("phase"))
        if phase in PHASES:
            history.append({
                "phase": phase,
                "label": PHASES[phase],
                "status": _redact(item.get("status") or "observed"),
                "at": _redact(item.get("at") or ""),
                "eventSeq": item.get("eventSeq"),
            })
    phases = [
        {"phase": phase, "label": label, "status": _phase_status(phase, state)}
        for phase, label in PHASES.items()
    ]
    blockers = state.get("blockers") or state.get("trilhaBloqueadores") or []
    if isinstance(blockers, dict):
        blockers = list(blockers.values())
    return {
        "schemaVersion": SCHEMA_VERSION,
        "kind": "forja_auditability_memory",
        "generatedAt": generated_at,
        "caseId": str(state.get("caseId") or case_dir.name),
        "state": {
            "sourceState": _relative(state_path, case_dir),
            "sourceStateSha256": sha256_file(state_path),
            "revision": state.get("revision"),
            "currentPhase": _canonical_phase(state.get("currentPhase") or state.get("phaseCursor")),
            "lifecycleStatus": state.get("lifecycleStatus") or state.get("status"),
            "humanReviewRequired": True,
            "externalSendAuthorized": False,
        },
        "method": {
            "name": "FORJA F0-F10 + FORJA-LASTRO-v2 + static OOXML/SVG QA",
            "principles": [
                "fonte declarada não equivale a fonte sustentadora",
                "gates são recomputados contra arquivos hash-bound",
                "solução sem mecanismo explícito não é design",
                "a aprovação humana permanece nominal e não é inferida pelo motor",
            ],
            "phases": phases,
            "phaseHistory": history,
        },
        "artifacts": _artifact_inventory(case_dir, state),
        "controls": controls,
        "sources": _source_summary(case_dir),
        "visual": _visual_summary(controls),
        "decisionsAndLimits": {
            "blockers": [_redact(item) for item in blockers if str(item).strip()],
            "deliveryEvidence": _redact(state.get("deliveryEvidence") or ""),
            "limitations": [
                "a memória não substitui leitura humana dos autos ou validação da fonte",
                "a QA estática não prova paginação física, legibilidade ou impressão",
                "não há autorização automática de protocolo, envio ou liberação jurídica",
            ],
        },
        "privacy": {
            "rawCaseContentIncluded": False,
            "quotesIncluded": False,
            "secretsIncluded": False,
            "pathsRedacted": True,
            "sourceEvidenceRepresentedBy": "identificador relativo, tamanho e SHA-256",
        },
    }


def _md(payload: dict[str, Any], manifest_sha: str) -> str:
    state = payload["state"]
    visual = payload["visual"]
    blocker_lines = [
        f"- {item}" for item in payload["decisionsAndLimits"]["blockers"]
    ] or ["- Nenhum bloqueador foi registrado no estado consultado."]
    limit_lines = [
        f"- Limite: {item}" for item in payload["decisionsAndLimits"]["limitations"]
    ]
    lines = [
        "# Memória de auditabilidade — FORJA",
        "",
        "> Documento interno enviado junto com a minuta para permitir a reconstrução do método, das decisões e dos gates. Não é peça processual nem substitui a conferência do advogado.",
        "",
        f"- Caso: `{payload['caseId']}`",
        f"- Revisão do estado: `{state.get('revision')}`",
        f"- Fase corrente: `{state.get('currentPhase') or 'não registrada'}`",
        f"- Gerado em: `{payload['generatedAt']}`",
        f"- Manifesto desta memória: `{manifest_sha}`",
        "",
        "## 1. Escopo e conclusão operacional",
        "",
        "A memória registra o caminho de F0 a F10, os artefatos hash-bound, os gates observados, as decisões e os limites. Ela não copia autos, transcrições, e-mails, credenciais nem o texto integral da minuta.",
        "",
        "## 2. Método aplicado",
        "",
        f"**{payload['method']['name']}**",
        "",
        *[f"- {item}" for item in payload["method"]["principles"]],
        "",
        "| Fase | Função | Estado |",
        "|---|---|---|",
        *[f"| `{item['phase']}` | {item['label']} | **{item['status']}** |" for item in payload["method"]["phases"]],
        "",
        "## 3. Fluxo auditado",
        "",
        "```text",
        "F0 entrada → F1 cobertura → F2 diagnóstico → F3 fontes → F4 design → F5 pesquisa → F6 redação → F7 auditoria → F8 OOXML/SVG estático → F9 pacote + memória → F10 evidência humana",
        "```",
        "",
        "A linha acima é um mapa do processo; não é uma afirmação de aprovação jurídica. A aprovação depende dos gates e da revisão humana indicados abaixo.",
        "",
        "## 4. Artefatos e integridade",
        "",
        "| ID | Caminho relativo | Existe | SHA-256 | Hash declarado confere |",
        "|---|---|---:|---|---:|",
        *[
            f"| `{item['id']}` | `{item['path']}` | {'sim' if item['exists'] else 'não'} | `{item.get('sha256') or 'ausente'}` | {'sim' if item['hashMatches'] else 'não verificado'} |"
            for item in payload["artifacts"]
        ],
        "",
        "## 5. Gates e controles",
        "",
        *[
            f"- `{item['path']}` — SHA-256 `{item['sha256']}`; aprovação declarada: `{item.get('approved', 'não registrada')}`; achados: `{item.get('findingsCount', item.get('violacoesCount', 0))}`."
            for item in payload["controls"]
        ],
        "",
        "## 6. Fonte e lastro",
        "",
        f"Ledger presente: **{'sim' if payload['sources'].get('present') else 'não'}**; fatos inventariados: `{payload['sources'].get('facts', 0)}`; citações/transcrições não são reproduzidas nesta memória.",
        "",
        "## 7. Materialização visual sem renderização",
        "",
        f"- Rota canônica: `{visual['canonicalRoute']}`.",
        f"- `renderingUsed`: `{visual['renderingUsed']}`; `pdfCreated`: `{visual['pdfCreated']}`; `pngCreated`: `{visual['pngCreated']}`.",
        "- A prova técnica é a inspeção estática do pacote OOXML, do texto armazenado no DOCX e dos SVGs nativos. A paginação e a legibilidade física continuam revisão humana.",
        "",
        "## 8. Decisões, bloqueios e limites",
        "",
        *blocker_lines,
        *limit_lines,
        "",
        "## 9. Privacidade e governança",
        "",
        "A memória é derivada e sanitizada: caminhos absolutos, segredos, autos e conteúdo bruto ficam fora. Para auditoria profunda, o advogado usa os artefatos internos hash-bound na pasta do caso, não este anexo isoladamente.",
        "",
        "**Próxima decisão humana:** validar a substância, a fonte prevalente, a legibilidade física e a autorização de envio antes de qualquer protocolo ou entrega externa.",
        "",
    ]
    return "\n".join(lines)


def _html_document(markdown: str, payload: dict[str, Any], manifest_sha: str) -> str:
    escaped = html.escape(markdown)
    payload_json = html.escape(json.dumps(payload, ensure_ascii=False, indent=2))
    return f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Memória de auditabilidade — FORJA</title>
<style>body{{font-family:Arial,sans-serif;line-height:1.45;color:#25373a;max-width:1100px;margin:2rem auto;padding:0 1rem}}pre{{white-space:pre-wrap;background:#f5f7f7;border:1px solid #d5dddd;border-radius:6px;padding:1rem}}details{{margin-top:1rem}}code{{word-break:break-all}}</style>
</head><body><h1>Memória de auditabilidade — FORJA</h1>
<p><strong>Manifesto:</strong> <code>{html.escape(manifest_sha)}</code></p>
<p>Documento interno derivado. Não substitui a conferência humana nem autoriza protocolo ou envio.</p>
<article><pre>{escaped}</pre></article>
<details><summary>Manifesto técnico sanitizado</summary><pre>{payload_json}</pre></details>
</body></html>
'''


def build_bundle(case_dir: Path, output_dir: Path | None = None) -> dict[str, Any]:
    case_dir = Path(case_dir).resolve()
    output_dir = Path(output_dir or case_dir / "pacote_revisao").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = build_payload(case_dir)
    manifest_path = output_dir / MEMORY_JSON
    # O manifesto não inclui hashes de si próprio ou dos dois derivados: assim
    # não há ciclo criptográfico e a verificação continua determinística.
    manifest = {**payload, "bundle": {"markdown": MEMORY_MD, "html": MEMORY_HTML, "manifest": MEMORY_JSON}}
    _write_text(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    manifest_sha = sha256_file(manifest_path)
    markdown = _md(payload, manifest_sha)
    html_doc = _html_document(markdown, payload, manifest_sha)
    _write_text(output_dir / MEMORY_MD, markdown)
    _write_text(output_dir / MEMORY_HTML, html_doc)
    result = {
        "approved": True,
        "schemaVersion": SCHEMA_VERSION,
        "caseId": payload["caseId"],
        "manifest": str(manifest_path),
        "manifestSha256": manifest_sha,
        "markdown": str(output_dir / MEMORY_MD),
        "html": str(output_dir / MEMORY_HTML),
        "renderingUsed": False,
    }
    return result


def validate_bundle(manifest_path: Path, *, expected_case_dir: Path | None = None) -> dict[str, Any]:
    manifest_path = Path(manifest_path)
    findings: list[str] = []
    payload = _read_json(manifest_path)
    if not isinstance(payload, dict) or payload.get("kind") != "forja_auditability_memory":
        findings.append("manifesto de memória inválido")
        payload = {}
    if payload.get("schemaVersion") != SCHEMA_VERSION:
        findings.append("versão de schema da memória não suportada")
    bundle = payload.get("bundle") if isinstance(payload.get("bundle"), dict) else {}
    manifest_sha = sha256_file(manifest_path) if manifest_path.is_file() else ""
    for key in ("markdown", "html"):
        name = str(bundle.get(key) or "")
        path = manifest_path.parent / name
        if not name or not path.is_file():
            findings.append(f"derivado ausente: {key}")
        else:
            text = path.read_text(encoding="utf-8", errors="replace")
            if manifest_sha and manifest_sha not in text:
                findings.append(f"derivado {key} não está vinculado ao hash do manifesto")
            if key == "markdown" and "## 7. Materialização visual sem renderização" not in text:
                findings.append("Markdown sem seção de materialização")
    if payload.get("visual", {}).get("renderingUsed") is not False:
        findings.append("memória declara uso de renderização")
    if payload.get("visual", {}).get("pdfCreated") is not False or payload.get("visual", {}).get("pngCreated") is not False:
        findings.append("memória declara PDF/PNG criado na rota canônica")
    if expected_case_dir:
        case_dir = Path(expected_case_dir).resolve()
        state_path = _state_path(case_dir)
        if state_path and payload.get("state", {}).get("sourceStateSha256") != sha256_file(state_path):
            findings.append("hash do estado de origem diverge")
    return {
        "approved": not findings,
        "findings": findings,
        "manifest": str(manifest_path),
        "caseId": payload.get("caseId"),
        "renderingUsed": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gera e valida a memória de auditabilidade da FORJA")
    sub = parser.add_subparsers(dest="command", required=True)
    build_parser = sub.add_parser("build")
    build_parser.add_argument("case_dir", type=Path)
    build_parser.add_argument("--output-dir", type=Path)
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("manifest", type=Path)
    validate_parser.add_argument("--case-dir", type=Path)
    args = parser.parse_args(argv)
    if args.command == "build":
        result = build_bundle(args.case_dir, args.output_dir)
    else:
        result = validate_bundle(args.manifest, expected_case_dir=args.case_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("approved") else 2


if __name__ == "__main__":
    raise SystemExit(main())
