# -*- coding: utf-8 -*-
"""Ledger de citações materiais (M3.2 do plano 19 — lição 52).

A integridade FÍSICA do registro de fontes (source_registry) não é proveniência
JURÍDICA. Este módulo materializa o ledger material da peça: cada afirmação
decisiva ligada a fonte primária, localizador, trecho, alcance e ressalva.

Duas entradas alimentam o ledger:
1. Citações extraídas da minuta (forja_citations.extrair_citacoes) cruzadas com
   o cache oficial, as fontes locais do caso e o sourceLedger do estado.
2. `producao/PROPOSICOES_DECISIVAS.md` — tabela manual das 10-15 proposições
   decisivas (U6). Se não existir, o script GERA o template para o agente
   preencher e registra pendência nominada.

O que ficar sem fonte primária vira pendência P1 NOMINADA (não bloqueia — a
régua de bloqueio continua sendo citação inexistente/deturpada, modos 1-6).

Uso: python forja_ledger_material.py <case_dir|trecho-do-caseId> [--draft caminho]
Saída: state/<caso>/F5_LEDGER_MATERIAL.json. Exit 0 sempre que rodar (P1 informa).
"""
from __future__ import annotations

import io
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from forja_citations import extrair_citacoes, procurar_cache_oficial, procurar_fonte_local
from forja_mutation_semantic import _achar_caso, _achar_draft

RAIZ = Path(__file__).resolve().parent

TEMPLATE_PROPOSICOES = """# Proposições decisivas — tabela de lastro (U6 / lição 52)

Preencher com as 10-15 proposições que decidem a peça. Uma linha por proposição.
Alcance = o que a fonte REALMENTE sustenta; Ressalva = onde a fonte não chega.

| # | Proposição | Fonte primária | Localizador (fl./URL/§) | Alcance | Ressalva |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |
"""


def _parse_proposicoes(path: Path) -> list[dict]:
    """Lê a tabela markdown de proposições. Linhas com proposição vazia são ignoradas."""
    itens = []
    if not path.is_file():
        return itens
    for linha in path.read_text(encoding="utf-8").splitlines():
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(celulas) < 6 or not celulas[0].isdigit():
            continue
        num, prop, fonte, loc, alcance, ressalva = (celulas + [""] * 6)[:6]
        if not prop:
            continue
        itens.append({
            "id": f"prop-{num}",
            "origem": "tabela_proposicoes",
            "proposicao": prop,
            "fontePrimaria": fonte or None,
            "localizador": loc or None,
            "alcance": alcance or None,
            "ressalva": ressalva or None,
        })
    return itens


def _source_ledger(case_dir: Path) -> list[dict]:
    try:
        estado = json.loads((case_dir / "FORJA_STATE.json").read_text(encoding="utf-8-sig"))
        return estado.get("sourceLedger") or []
    except (OSError, json.JSONDecodeError):
        return []


def _casar_source_ledger(rotulo: str, ledger: list[dict]) -> dict | None:
    alvo = re.sub(r"[\.\s]", "", rotulo).casefold()
    for item in ledger:
        claim = re.sub(r"[\.\s]", "", str(item.get("claim") or "")).casefold()
        if alvo and alvo in claim:
            return item
    return None


def montar(case_dir: Path, draft: Path) -> dict:
    texto = draft.read_text(encoding="utf-8-sig", errors="replace")
    ledger_estado = _source_ledger(case_dir)
    pasta_caso = None
    try:
        estado = json.loads((case_dir / "FORJA_STATE.json").read_text(encoding="utf-8-sig"))
        pasta_caso = (estado.get("inputs") or {}).get("caseFolder")
    except (OSError, json.JSONDecodeError):
        pass

    entradas, pendencias = [], []

    # 1. citações da minuta -> fonte primária
    for cit in extrair_citacoes(texto):
        fonte, localizador, verificado = None, None, None
        cache = procurar_cache_oficial(cit)
        if cache:
            fonte = "cache_oficial"
            localizador = str(cache)
        elif pasta_caso:
            local = procurar_fonte_local(cit, Path(pasta_caso))
            if local:
                fonte = "fonte_local_do_caso"
                localizador = str(local)
        casado = _casar_source_ledger(cit["rotulo"], ledger_estado)
        if casado:
            fonte = fonte or casado.get("classification")
            localizador = localizador or casado.get("sourcePathOrUrl")
            verificado = casado.get("verifiedAt")
        entrada = {
            "id": f"cit-{re.sub(r'[^A-Za-z0-9]+', '-', cit['rotulo'])}",
            "origem": "citacao_extraida",
            "proposicao": cit["contexto"],
            "citacao": cit["rotulo"],
            "fontePrimaria": fonte,
            "localizador": localizador,
            "alcance": None,      # preenchido pelo agente na revisão (ratio × dictum)
            "ressalva": None,
            "verificadoEm": verificado,
        }
        entradas.append(entrada)
        if not fonte:
            pendencias.append({
                "sev": "P1", "id": entrada["id"],
                "problema": f"citação '{cit['rotulo']}' sem fonte primária "
                            "(cache oficial, fonte local ou sourceLedger)"})

    # 2. proposições decisivas manuais (U6)
    prop_path = (case_dir / "producao" / "PROPOSICOES_DECISIVAS.md")
    props = _parse_proposicoes(prop_path)
    for p in props:
        entradas.append(p)
        if not p["fontePrimaria"]:
            pendencias.append({"sev": "P1", "id": p["id"],
                               "problema": f"proposição decisiva sem fonte primária: "
                                           f"{p['proposicao'][:80]}"})
    if not props:
        if not prop_path.is_file():
            prop_path.parent.mkdir(parents=True, exist_ok=True)
            prop_path.write_text(TEMPLATE_PROPOSICOES, encoding="utf-8")
        pendencias.append({"sev": "P1", "id": "proposicoes",
                           "problema": "tabela de proposições decisivas não preenchida "
                                       f"({prop_path.name} — template gerado)"})

    return {
        "schemaVersion": 1,
        "artifactType": "F5_LEDGER_MATERIAL",
        "generatedAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "caseId": case_dir.name,
        "draft": str(draft),
        "totais": {
            "entradas": len(entradas),
            "comFontePrimaria": sum(1 for e in entradas if e.get("fontePrimaria")),
            "pendencias": len(pendencias),
        },
        "entradas": entradas,
        "pendencias": pendencias,   # P1 nominadas — nunca silenciosas
    }


def main(argv=None) -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    case_dir = _achar_caso(argv[0])
    draft = Path(argv[argv.index("--draft") + 1]) if "--draft" in argv else _achar_draft(case_dir)
    if draft is None or not draft.is_file():
        print(json.dumps({"erro": "minuta não localizada", "caso": str(case_dir)},
                         ensure_ascii=False))
        return 2
    ledger = montar(case_dir, draft)
    out = case_dir / "F5_LEDGER_MATERIAL.json"
    out.write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding="utf-8")
    t = ledger["totais"]
    print(f"caso: {case_dir.name}")
    print(f"entradas: {t['entradas']} ({t['comFontePrimaria']} com fonte primária)")
    for p in ledger["pendencias"]:
        print(f"  {p['sev']} {p['id']}: {p['problema']}")
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
