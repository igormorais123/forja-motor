"""FORJA N2 - F3 Fontes, regimento e leis gerais (modo leitura / sombra).

Para cada caso (ou os casos-piloto indicados):
  - identifica o tribunal (número CNJ, sigla de recurso, mapa da fábrica);
  - verifica REGIMENTO_INTERNO_<TRIBUNAL>.md na pasta do caso (metadados + emendas);
  - se ausente na pasta mas existente em outra pasta da fábrica, aponta a origem;
  - verifica _LEIS_GERAIS (Estatuto OAB + LOMAN);
  - grava F3_MAPA_FONTES_E_REGIMENTO.md em _FORJA_HARNESS/state/<caseId>/ (sombra:
    NÃO escreve na pasta do caso) e atualiza FORJA_STATE.json (fase, gates, ledger).

Gate P0 (spec N2, TDD seção 7 F3): regimento ausente/incompleto/sem metadados
bloqueia F4/F6 até correção.
"""

import json
import re
import sys
from pathlib import Path

from forja_n3_common import now_iso, read_json

FORJA = Path(__file__).resolve().parent
RAIZ = FORJA.parent
STATE_DIR = FORJA / "state"
LEIS_GERAIS = RAIZ / "_LEIS_GERAIS"

CNJ_RE = re.compile(r"(\d{7})-?(\d{2})\.(\d{4})\.(\d)\.(\d{2})\.(\d{4})")

TJ_POR_TR = {"27": "TJTO", "19": "TJRJ", "21": "TJRS", "26": "TJSP", "07": "TJDFT"}


def classificar_produto(texto):
    """F2 mínima: tipo de produto define se regimento é obrigatório."""
    t = (texto or "").lower()
    judicial = ["memoriais", "memorial", "embargos", "contrarraz", "agravo", "apela",
                "impugna", "recurso", "manifesta", "peti", "sustenta"]
    consultivo = ["parecer", "quesitos", "consultoria", "proposta de servi", "análise de risco", "due diligence"]
    if any(k in t for k in consultivo) and not CNJ_RE.search(texto or ""):
        return "parecer_consultivo", False
    if any(k in t for k in judicial) or CNJ_RE.search(texto or ""):
        return "peca_judicial", True
    return "indefinido", True


def detectar_tribunal(texto):
    """Retorna (tribunal, criterio) ou (None, None). Ordem: sigla superior > CNJ."""
    t = texto or ""
    if re.search(r"\b(AREsp|REsp|EREsp|AgInt no AREsp|EDcl no AgInt)\b", t, re.I):
        return "STJ", "sigla de recurso ao STJ no título/pasta"
    if re.search(r"\b(RE|ARE)\s*\d{6,}", t):
        return "STF", "sigla de recurso extraordinário"
    m = CNJ_RE.search(t)
    if m:
        segmento, tr = m.group(4), m.group(5)
        if segmento == "4":
            return f"TRF{int(tr)}", f"CNJ segmento J=4, TR={tr} (Justiça Federal)"
        if segmento == "8":
            trib = TJ_POR_TR.get(tr)
            if trib:
                return trib, f"CNJ segmento J=8, TR={tr} (Justiça Estadual)"
            return f"TJ-{tr}", f"CNJ segmento J=8, TR={tr} (Justiça Estadual, sigla não mapeada)"
    return None, None


def validar_regimento(path):
    """Confere texto integral com metadados e seção de emendas. Retorna (ok, avisos)."""
    avisos = []
    texto = path.read_text(encoding="utf-8", errors="replace")
    cabecalho = texto[:2000].lower()
    if not any(k in cabecalho for k in ("fonte", "orig", "http")):
        avisos.append("Cabeçalho sem indicação de fonte oficial.")
    if not any(k in cabecalho for k in ("emenda", "versão", "versao", "consolida", "atualiza")):
        avisos.append("Cabeçalho sem versão/última emenda declarada.")
    if not re.search(r"emendas?\s+posteriores", texto, re.I):
        avisos.append("Sem seção 'Emendas posteriores' — atualização até a data do protocolo não comprovada.")
    if len(texto) < 30000:
        avisos.append(f"Arquivo curto ({len(texto)} chars) — conferir se é texto integral, não resumo.")
    return (len(avisos) == 0), avisos


def localizar_regimento(tribunal, case_folder):
    """Procura primeiro na pasta do caso, depois em qualquer pasta da fábrica."""
    nome = f"REGIMENTO_INTERNO_{tribunal}.md"
    local = case_folder / nome if case_folder else None
    if local and local.exists():
        return local, "pasta do caso"
    for candidato in RAIZ.rglob(nome):
        if "_FORJA_HARNESS" in str(candidato):
            continue
        return candidato, "outra pasta da fábrica"
    return None, None


def merge_by_id(existing, new_items):
    merged = {}
    for item in existing or []:
        item_id = item.get("id")
        if item_id:
            merged[item_id] = item
    for item in new_items or []:
        item_id = item.get("id")
        if item_id:
            merged[item_id] = item
    return list(merged.values())


def merge_gates(existing, new_items):
    seen = set()
    merged = []
    for item in (existing or []) + (new_items or []):
        key = (item.get("code"), item.get("severity"), item.get("detail"))
        if key in seen:
            continue
        seen.add(key)
        merged.append(item)
    return merged


def append_unique(existing, value):
    items = list(existing or [])
    if value not in items:
        items.append(value)
    return items


def processar_caso(state_path):
    state = read_json(state_path, None)
    if not state:
        return None
    demanda_id = (state.get("inputs") or {}).get("demandId") or state["caseId"]
    case_folder = (state.get("inputs") or {}).get("caseFolder")
    case_folder = Path(case_folder) if case_folder else None

    # Texto-base para detecção: título vem do relatório do painel; usamos pasta + comando
    partes = [str(case_folder.name) if case_folder else "", demanda_id]
    cmd_file = (state.get("inputs") or {}).get("commandFile")
    if case_folder and cmd_file and (case_folder / cmd_file).exists():
        partes.append((case_folder / cmd_file).read_text(encoding="utf-8", errors="replace")[:4000])
    texto = "\n".join(partes)

    produto, regimento_obrigatorio = classificar_produto(texto)
    tribunal, criterio = detectar_tribunal(texto)
    gates, ledger, linhas = [], [], []

    linhas += [
        "# F3 — Mapa de fontes, regimento e leis gerais",
        "",
        f"Caso: `{state['caseId']}` | Gerado: {now_iso()} | Modo sombra (arquivo fora da pasta do caso)",
        "",
        f"## Produto (F2): {produto}" ,
        "",
        "## Tribunal",
        "",
    ]
    if tribunal:
        linhas.append(f"- Tribunal identificado: **{tribunal}** ({criterio})")
        ledger.append({
            "id": f"src-trib-{demanda_id[:24]}",
            "claim": f"Tribunal de análise: {tribunal}",
            "classification": "INFERENCIA",
            "sourcePathOrUrl": criterio,
            "pageOrEvent": None,
            "verifiedAt": now_iso(),
            "finalUseAllowed": True,
        })
    elif regimento_obrigatorio:
        linhas.append("- Tribunal NÃO identificado automaticamente — exige classificação humana ou leitura da decisão.")
        gates.append({"code": "TRIBUNAL_NAO_IDENTIFICADO", "severity": "P0",
                      "detail": "Sem tribunal não há regimento aplicável; classificar antes de redigir.", "at": now_iso()})
    else:
        linhas.append("- Produto consultivo (parecer/quesitos): regimento de tribunal NÃO é bloqueador; jurisprudência de fonte oficial continua obrigatória (comando expresso do cliente).")

    linhas += ["", "## Regimento interno", ""]
    if tribunal:
        reg_path, onde = localizar_regimento(tribunal, case_folder)
        if reg_path is None:
            gates.append({"code": "REGIMENTO_AUSENTE", "severity": "P0",
                          "detail": f"REGIMENTO_INTERNO_{tribunal}.md não existe em nenhuma pasta da fábrica; baixar versão oficial consolidada antes de redigir.", "at": now_iso()})
            linhas.append(f"- **AUSENTE**: `REGIMENTO_INTERNO_{tribunal}.md` não localizado na fábrica. Bloqueia F4/F6.")
        else:
            ok, avisos = validar_regimento(reg_path)
            linhas.append(f"- Localizado em: `{reg_path.relative_to(RAIZ)}` ({onde})")
            if onde != "pasta do caso":
                gates.append({"code": "REGIMENTO_FORA_DA_PASTA", "severity": "P1",
                              "detail": f"Regimento existe em '{reg_path.parent.name}' mas não na pasta do caso; copiar antes da redação (regra do protocolo).", "at": now_iso()})
            for a in avisos:
                gates.append({"code": "REGIMENTO_INCOMPLETO", "severity": "P1", "detail": a, "at": now_iso()})
                linhas.append(f"- Aviso: {a}")
            if ok:
                linhas.append("- Metadados e seção de emendas: OK.")
            ledger.append({
                "id": f"src-reg-{tribunal}",
                "claim": f"Regimento interno {tribunal} disponível para consulta",
                "classification": "FONTE_ARQUIVO",
                "sourcePathOrUrl": str(reg_path),
                "pageOrEvent": None,
                "verifiedAt": now_iso(),
                "finalUseAllowed": ok,
            })

    linhas += ["", "## Leis gerais (_LEIS_GERAIS)", ""]
    if LEIS_GERAIS.exists():
        arquivos = sorted(p.name for p in LEIS_GERAIS.glob("*.md"))
        linhas.append(f"- Pasta presente com {len(arquivos)} arquivo(s): {', '.join(arquivos[:6])}")
        ledger.append({
            "id": "src-leis-gerais",
            "claim": "Estatuto da OAB e LOMAN disponíveis",
            "classification": "FONTE_ARQUIVO",
            "sourcePathOrUrl": str(LEIS_GERAIS),
            "pageOrEvent": None,
            "verifiedAt": now_iso(),
            "finalUseAllowed": True,
        })
    else:
        gates.append({"code": "LEIS_GERAIS_AUSENTES", "severity": "P0",
                      "detail": "Pasta _LEIS_GERAIS não encontrada.", "at": now_iso()})
        linhas.append("- **AUSENTE**: pasta _LEIS_GERAIS não encontrada.")

    linhas += ["", "## Lacunas bloqueantes", ""]
    p0s = [g for g in gates if g["severity"] == "P0"]
    if p0s:
        for g in p0s:
            linhas.append(f"- [P0] `{g['code']}`: {g['detail']}")
    else:
        linhas.append("- Nenhuma. Caso liberado para F4 (blueprint).")

    # Persistência (sombra): mapa no state dir + atualização do estado
    mapa_path = state_path.parent / "F3_MAPA_FONTES_E_REGIMENTO.md"
    mapa_path.write_text("\n".join(linhas) + "\n", encoding="utf-8")

    tem_p0 = bool(p0s)
    state["currentPhase"] = "F3_FONTES_REGIMENTO_LEIS"
    state["status"] = "blocked" if tem_p0 else state.get("status", "pending")
    state["updatedAt"] = now_iso()
    state.setdefault("phaseHistory", []).append(
        {"phase": "F3_FONTES_REGIMENTO_LEIS", "at": now_iso(), "status": "blocked" if tem_p0 else "ok"})
    state["gates"] = merge_gates(state.get("gates") or [], gates)
    state["sourceLedger"] = merge_by_id(state.get("sourceLedger") or [], ledger)
    state["artifacts"] = append_unique(state.get("artifacts") or [], str(mapa_path))
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    return {"caseId": state["caseId"], "tribunal": tribunal, "p0": len(p0s),
            "p1": len([g for g in gates if g["severity"] == "P1"]), "mapa": str(mapa_path)}


def main():
    alvos = sys.argv[1:]
    resultados = []
    for state_path in sorted(STATE_DIR.glob("case-*/FORJA_STATE.json")):
        if alvos and not any(a in str(state_path.parent.name) for a in alvos):
            continue
        r = processar_caso(state_path)
        if r:
            resultados.append(r)
    print(json.dumps({"processados": len(resultados), "casos": resultados}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
