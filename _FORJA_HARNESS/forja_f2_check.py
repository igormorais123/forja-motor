# -*- coding: utf-8 -*-
"""Coerência da classificação F2 (M4.3 do plano 19).

Valida o enquadramento contra regras determinísticas do protocolo da fábrica:
1. Tribunal inferido do número CNJ (NNNNNNN-DD.AAAA.J.TR.OOOO): segmento J=4 →
   Justiça Federal (TRF<TR>); J=8 → Justiça Estadual (TR 27=TJTO, 19=TJRJ,
   21=TJRS, 26=TJSP...); classe recursal AREsp/REsp/AgInt→STJ, RE/ARE→STF.
2. Perfil PSO-Pet ∈ {leve, completo, intensivo} quando presente.
3. Complexidade ∈ {low, medium, high} e produto não vazio.

Uso programático:
    from forja_f2_check import tribunal_do_cnj, validar_classificacao
Uso CLI: python forja_f2_check.py <trecho-do-caseId>
Achado vira P1 nominado (classificação incoerente não segue para F3 sem revisão).
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

CNJ = re.compile(r"\b(\d{7})-?(\d{2})\.(\d{4})\.(\d)\.(\d{2})\.(\d{4})\b")

TJ_POR_TR = {
    "01": "TJAC", "02": "TJAL", "03": "TJAP", "04": "TJAM", "05": "TJBA",
    "06": "TJCE", "07": "TJDFT", "08": "TJES", "09": "TJGO", "10": "TJMA",
    "11": "TJMT", "12": "TJMS", "13": "TJMG", "14": "TJPA", "15": "TJPB",
    "16": "TJPR", "17": "TJPE", "18": "TJPI", "19": "TJRJ", "20": "TJRN",
    "21": "TJRS", "22": "TJRO", "23": "TJRR", "24": "TJSC", "25": "TJSE",
    "26": "TJSP", "27": "TJTO",
}
PERFIS_PSO = {"leve", "completo", "intensivo"}
COMPLEXIDADES = {"low", "medium", "high"}
CLASSES_STJ = re.compile(r"\b(AREsp|AgInt no AREsp|REsp|AgRg no REsp|EDcl no AgInt)\b", re.I)
CLASSES_STF = re.compile(r"\b(RE|ARE)\s*(?:n[ºo.]?\s*)?[\d\.]+", re.I)


def tribunal_do_cnj(numero: str) -> str | None:
    """Tribunal do 2º grau inferido do número CNJ. None se não reconhecido."""
    m = CNJ.search(numero or "")
    if not m:
        return None
    segmento, tr = m.group(4), m.group(5)
    if segmento == "4":
        return f"TRF{int(tr)}"
    if segmento == "8":
        return TJ_POR_TR.get(tr)
    if segmento == "5":
        return f"TRT{int(tr)}"
    if segmento == "6":
        return f"TRE-{tr}"
    return None


def tribunais_do_texto(texto: str) -> set[str]:
    """Todos os tribunais inferíveis de um texto (CNJ + classes recursais)."""
    achados = set()
    for m in CNJ.finditer(texto or ""):
        t = tribunal_do_cnj(m.group(0))
        if t:
            achados.add(t)
    if CLASSES_STJ.search(texto or ""):
        achados.add("STJ")
    if CLASSES_STF.search(texto or ""):
        achados.add("STF")
    return achados


def validar_classificacao(classificacao: dict, textos_do_caso: str = "") -> list[dict]:
    """Achados P1 nominados. Lista vazia = coerente."""
    achados = []
    if not str(classificacao.get("product") or "").strip():
        achados.append({"sev": "P1", "campo": "product",
                        "problema": "tipo de peça vazio na classificação F2"})
    cx = classificacao.get("complexity")
    if cx is not None and cx not in COMPLEXIDADES:
        achados.append({"sev": "P1", "campo": "complexity",
                        "problema": f"complexidade '{cx}' fora do enum {sorted(COMPLEXIDADES)}"})
    perfil = classificacao.get("psoProfile") or classificacao.get("perfilPso")
    if perfil is not None and perfil not in PERFIS_PSO:
        achados.append({"sev": "P1", "campo": "psoProfile",
                        "problema": f"perfil PSO-Pet '{perfil}' fora de {sorted(PERFIS_PSO)}"})
    tribunal = str(classificacao.get("tribunal") or "").upper().replace(" ", "")
    if tribunal and textos_do_caso:
        inferidos = tribunais_do_texto(textos_do_caso)
        if inferidos and tribunal not in inferidos:
            achados.append({
                "sev": "P1", "campo": "tribunal",
                "problema": f"tribunal declarado '{tribunal}' não bate com o inferido "
                            f"dos autos ({', '.join(sorted(inferidos))}) — conferir "
                            "endereçamento e regimento (protocolo da fábrica)"})
    return achados


def main(argv=None) -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    matches = sorted((RAIZ / "state").glob(f"case-*{argv[0]}*"))
    if not matches:
        print(f"caso não encontrado: {argv[0]}")
        return 2
    case_dir = matches[0]
    cls_path = case_dir / "n4_artifacts" / "F2_N4_CLASSIFICATION.json"
    classificacao = {}
    if cls_path.is_file():
        classificacao = json.loads(cls_path.read_text(encoding="utf-8"))
    textos = case_dir.name
    try:
        estado = json.loads((case_dir / "FORJA_STATE.json").read_text(encoding="utf-8-sig"))
        pasta = Path((estado.get("inputs") or {}).get("caseFolder") or "")
        cmd = pasta / str((estado.get("inputs") or {}).get("commandFile") or "")
        if cmd.is_file():
            textos += "\n" + cmd.read_text(encoding="utf-8", errors="replace")[:20000]
    except (OSError, json.JSONDecodeError):
        pass
    achados = validar_classificacao(classificacao, textos)
    print(json.dumps({"caseId": case_dir.name, "achados": achados,
                      "coerente": not achados}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
