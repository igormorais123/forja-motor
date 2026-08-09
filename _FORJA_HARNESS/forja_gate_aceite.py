# -*- coding: utf-8 -*-
"""forja_gate_aceite.py — o gate do checklist que o cliente escreveu.

Existe uma classe de exigência que nenhum gate da casa alcançava: a lista de
critérios de aceitação que o titular manda por e-mail, item por item, dizendo
que só marca concluído o que tiver artefato verificável. Até aqui essa lista
virava prosa num relatório, alguém respondia "feito" ao lado de cada linha, e
não havia nada entre a afirmação e a verdade.

O que este módulo faz é simples e é a única coisa que ele faz: **confere que o
artefato prometido existe, é do tipo prometido e tem tamanho de arquivo real**,
e recusa a marcação de concluído quando não existe. Ele não lê o conteúdo e não
julga qualidade — quem diz que o texto presta é o F7, o conselho e a revisão
humana. Confundir as duas coisas produziria o defeito que a Lição 278 registra:
gate que mede a qualidade da declaração em vez do estado do mundo.

O registro fica no ACERVO, na pasta do caso, porque cada item cita evento,
documento e página de processo real. O motor traz a mecânica; o caso traz a
lista. Assim o próximo checklist do próximo titular não custa código novo.

Formato do registro (`CHECKLIST_ACEITE.json`):

    {
      "schemaVersion": 1,
      "origem": {"fonte": "...", "data": "AAAA-MM-DD"},
      "regrasDeEncerramento": ["nenhuma conclusão sem fonte", ...],
      "itens": [
        {"id": 1,
         "titulo": "...",
         "exige": ["artefato"],            # ver EXIGENCIAS
         "artefatos": ["caminho/rel.md"],  # relativo à pasta do caso
         "estado": "concluido|parcial|aberto",
         "observacao": "..."}
      ]
    }

Uso:
    python forja_gate_aceite.py --caso "<pasta do caso>"
    python forja_gate_aceite.py --caso "<pasta>" --json SAIDA.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

VERSAO = "FORJA-GATE-ACEITE-v1"
REGISTRO = "CHECKLIST_ACEITE.json"
RESULTADO = "CHECKLIST_ACEITE_RESULT.json"

ESTADOS = ("concluido", "parcial", "aberto")

# Exigências que o gate sabe conferir. Cada uma responde a uma das regras de
# encerramento escritas pelo titular, e nenhuma delas olha o conteúdo.
EXIGENCIAS = {
    # "nenhuma conclusão sem fonte" / "nenhuma fonte sem localização"
    "artefato": "pelo menos um arquivo declarado, existente e não vazio",
    # "nenhum número sem reprodução": resultado em PDF não se reproduz
    "nativo": "pelo menos um arquivo em formato reprocessável (.json/.csv/.xlsx/.py)",
    # "nenhum precedente sem inteiro teor"
    "inteiro_teor": "artefato cujo nome declara teor integral, não ementa",
    # o corpo da peça, que é o produto final
    "peca": "artefato .md ou .docx que seja a minuta, não relatório interno",
}

_NATIVO = {".json", ".csv", ".xlsx", ".xls", ".py", ".sql", ".parquet"}
_PECA = {".md", ".docx"}
_MIN_BYTES = 512


def _falta(item, codigo, problema, acao) -> dict:
    return {"item": item.get("id"), "gate": codigo, "sev": "P0",
            "titulo": item.get("titulo", "")[:80],
            "problema": problema, "acao": acao, "versao": VERSAO}


def _resolver(base: Path, rel: str) -> Path | None:
    alvo = base / rel
    if alvo.is_file():
        return alvo
    # o titular cita por nome; a pasta do caso é grande e reorganiza
    achado = next(base.rglob(Path(rel).name), None)
    return achado if achado and achado.is_file() else None


def avaliar(registro: dict, base: Path) -> dict:
    itens = [i for i in (registro.get("itens") or []) if isinstance(i, dict)]
    achados: list[dict] = []
    linhas: list[dict] = []

    for item in itens:
        estado = str(item.get("estado") or "aberto").lower()
        if estado not in ESTADOS:
            achados.append(_falta(item, "ACE0-estado-invalido",
                                  f"estado {estado!r} fora do vocabulário {ESTADOS}",
                                  "use concluido, parcial ou aberto"))
            estado = "aberto"

        existentes, ausentes = [], []
        for rel in (item.get("artefatos") or []):
            alvo = _resolver(base, str(rel))
            if alvo is None:
                ausentes.append(str(rel))
            else:
                existentes.append(alvo)

        exige = [e for e in (item.get("exige") or ["artefato"]) if e in EXIGENCIAS]

        # A regra que dá sentido ao gate: só se cobra prova de quem afirma ter
        # concluído. Item aberto declarado como aberto é informação, não falha.
        if estado == "concluido":
            if ausentes:
                achados.append(_falta(
                    item, "ACE1-artefato-inexistente",
                    f"declarado concluído, mas {len(ausentes)} artefato(s) não existem no disco: "
                    + ", ".join(ausentes[:3]),
                    "produza o artefato ou reclassifique o item como parcial ou aberto"))
            if "artefato" in exige and not existentes:
                achados.append(_falta(
                    item, "ACE2-sem-artefato",
                    "declarado concluído sem artefato algum — é afirmação, não entrega",
                    "aponte o arquivo que prova a conclusão"))
            vazios = [p.name for p in existentes if p.stat().st_size < _MIN_BYTES]
            if vazios:
                achados.append(_falta(
                    item, "ACE3-artefato-vazio",
                    f"artefato com menos de {_MIN_BYTES} bytes: " + ", ".join(vazios[:3]),
                    "o arquivo existe e não tem conteúdo; confira a geração"))
            if "nativo" in exige and not any(p.suffix.lower() in _NATIVO for p in existentes):
                achados.append(_falta(
                    item, "ACE4-sem-formato-nativo",
                    "item quantitativo sem arquivo reprocessável — PDF permite ler o "
                    "resultado, não reproduzir o cálculo",
                    "entregue a base ou a planilha em formato nativo"))
            if "inteiro_teor" in exige and not any(
                    "inteiro_teor" in p.name.lower() or "teor" in p.name.lower()
                    for p in existentes):
                achados.append(_falta(
                    item, "ACE5-sem-inteiro-teor",
                    "precedente sem artefato de teor integral declarado",
                    "junte o inteiro teor obtido em fonte oficial"))
            if "peca" in exige and not any(p.suffix.lower() in _PECA for p in existentes):
                achados.append(_falta(
                    item, "ACE6-sem-peca",
                    "item do produto final sem minuta em .md ou .docx",
                    "a minuta é o produto; relatório interno não a substitui"))

        linhas.append({
            "id": item.get("id"),
            "titulo": item.get("titulo", ""),
            "estado": estado,
            "exige": exige,
            "artefatosDeclarados": len(item.get("artefatos") or []),
            "artefatosNoDisco": len(existentes),
            "arquivos": [{"caminho": p.name, "bytes": p.stat().st_size,
                          "sha256": hashlib.sha256(p.read_bytes()).hexdigest()[:16]}
                         for p in existentes],
            "ausentes": ausentes,
            "observacao": item.get("observacao", ""),
        })

    concluidos = [l for l in linhas if l["estado"] == "concluido"]
    parciais = [l for l in linhas if l["estado"] == "parcial"]
    abertos = [l for l in linhas if l["estado"] == "aberto"]

    # "nenhuma nova entrega fragmentária": a saída só libera com a lista inteira
    # fechada. É o único gate da casa em que item aberto DECLARADO também barra —
    # porque aqui o que se autoriza não é a fase, é a remessa ao titular.
    if parciais or abertos:
        achados.append({
            "item": None, "gate": "ACE7-entrega-fragmentaria", "sev": "P0",
            "titulo": "regra de encerramento",
            "problema": (f"{len(parciais)} item(ns) parciais e {len(abertos)} abertos — "
                         "a remessa foi contratada como única e conclusiva"),
            "acao": ("feche os itens ou individualize a limitação externa, com prova e "
                     "a melhor conclusão juridicamente possível"),
            "versao": VERSAO})

    p0 = [a for a in achados if a["sev"] == "P0"]
    return {
        "schemaVersion": 1,
        "artifactType": "CHECKLIST_ACEITE_RESULT",
        "versao": VERSAO,
        "origem": registro.get("origem") or {},
        "regrasDeEncerramento": registro.get("regrasDeEncerramento") or [],
        "resumo": {"itens": len(linhas), "concluidos": len(concluidos),
                   "parciais": len(parciais), "abertos": len(abertos),
                   "p0": len(p0)},
        "liberado": not p0,
        "itens": linhas,
        "findings": achados,
    }


def _imprimir(r: dict) -> None:
    res = r["resumo"]
    print("=" * 74)
    print(f"GATE DE ACEITE — {res['itens']} itens declarados pelo titular")
    print("=" * 74)
    for l in r["itens"]:
        marca = {"concluido": "[x]", "parcial": "[~]", "aberto": "[ ]"}[l["estado"]]
        prova = (f"{l['artefatosNoDisco']}/{l['artefatosDeclarados']} arq"
                 if l["artefatosDeclarados"] else "sem artefato")
        print(f"  {marca} {str(l['id']):>2}. {l['titulo'][:52]:<52} {prova}")
    print("-" * 74)
    print(f"  concluídos {res['concluidos']} · parciais {res['parciais']} · "
          f"abertos {res['abertos']} · P0 {res['p0']}")
    for a in r["findings"]:
        onde = f"item {a['item']}" if a["item"] else "regra"
        print(f"  [{a['sev']}] {a['gate']} ({onde}): {a['problema']}")
    print("  LIBERADO" if r["liberado"] else "  BLOQUEADO — a remessa não sai assim")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--caso", required=True, help="pasta do caso, onde vive o registro")
    ap.add_argument("--json", help="grava o resultado neste caminho")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)

    base = Path(a.caso).resolve()
    reg = base / REGISTRO
    if not reg.is_file():
        print(f"registro ausente: {reg}", file=sys.stderr)
        print("o gate não inventa checklist; ele confere o que o titular escreveu",
              file=sys.stderr)
        return 2
    try:
        registro = json.loads(reg.read_text(encoding="utf-8"))
    except ValueError as e:
        print(f"registro ilegível: {e}", file=sys.stderr)
        return 2

    r = avaliar(registro, base)
    if not a.quiet:
        _imprimir(r)
    destino = Path(a.json) if a.json else base / RESULTADO
    destino.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if r["liberado"] else 1


if __name__ == "__main__":
    sys.exit(main())
