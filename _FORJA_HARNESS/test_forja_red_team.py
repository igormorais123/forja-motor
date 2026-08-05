# -*- coding: utf-8 -*-
"""test_forja_red_team.py — regressão de `red_team_completed` e
`adversarial_claims_rechecked`.

O achado que motivou esta leva está codificado na última verificação: das oito
execuções reais de `adversarial_recheck`, SEIS declaram `applicable: false` — e
as oito reportaram `pass`. O gate precisa devolver `not_applicable` nesses seis,
senão continua medindo o conjunto vazio e chamando isso de aprovação.

Uso: python test_forja_red_team.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_red_team import (  # noqa: E402
    GATE_RECHECK, GATE_RED_TEAM, validar_recheck_adversarial, validar_red_team)

NOVE = "\n".join(f"{i}. Objeção {i}: o adversário diria X. Resposta: Y." for i in range(1, 10))
SEIS = "\n".join(f"{i}. Objeção {i}: o adversário diria X. Resposta: Y." for i in range(1, 7))


def _red(texto):
    return validar_red_team(texto)["gates"][GATE_RED_TEAM]


def _rec(dados):
    return validar_recheck_adversarial(dados)["gates"][GATE_RECHECK]


def main() -> int:
    falhas = 0
    casos = 0

    def checar(nome, obtido, esperado):
        nonlocal falhas, casos
        casos += 1
        if obtido != esperado:
            print(f"  FALHOU: {nome} — esperado {esperado}, obtido {obtido}")
            falhas += 1

    checar("relatório ausente", _red(None), "fail")
    checar("relatório vazio", _red("   "), "fail")
    checar("prosa sem objeção enumerada",
           _red("Fizemos o red team e concluímos que está tudo certo."), "fail")
    checar("duas objeções só", _red("1. uma coisa\n2. outra coisa"), "fail")
    checar("as nove do protocolo", _red(NOVE), "pass")
    # Seis objeções densas é o relatório real da Natura: não se reprova
    # retroativamente trabalho substantivo, mas também não se diz `pass`.
    checar("seis objeções — abaixo do protocolo", _red(SEIS), "warn")

    checar("recheck ausente", _rec(None), "fail")
    checar("recheck vazio", _rec({}), "fail")
    checar("aplicável sem nenhuma alegação rechecada",
           _rec({"applicable": True, "recheckedIssues": []}), "fail")
    checar("sem declarar aplicabilidade e sem itens", _rec({"kind": "x"}), "fail")
    checar("inaplicável com motivo escrito",
           _rec({"applicable": False, "notApplicableReason": "petição inicial, sem peça adversária"}),
           "not_applicable")
    checar("inaplicável sem motivo", _rec({"applicable": False}), "warn")
    checar("aplicável com alegações e resultados",
           _rec({"applicable": True,
                 "recheckedIssues": [{"issue": "alegação A", "result": "respondida no capítulo III"}]}),
           "pass")
    checar("alegação listada sem resultado",
           _rec({"applicable": True, "recheckedIssues": [{"issue": "alegação A"}]}), "warn")

    # CONTRAPROVA — artefatos reais. Nenhum pode ser REPROVADO.
    vistos, vereditos = set(), []
    for arquivo in Path("state").rglob("adversarial_recheck.json"):
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not isinstance(dados, dict):
            continue
        chave = json.dumps(dados, sort_keys=True)
        if chave in vistos:
            continue
        vistos.add(chave)
        casos += 1
        veredito = _rec(dados)
        vereditos.append(veredito)
        if veredito == "fail":
            print(f"  TRAVOU O APROVADO: {arquivo}")
            falhas += 1

    reais_red = set()
    for arquivo in Path("state").rglob("red_team_report.md"):
        texto = arquivo.read_text(encoding="utf-8", errors="replace")
        if texto in reais_red:
            continue
        reais_red.add(texto)
        casos += 1
        if _red(texto) == "fail":
            print(f"  TRAVOU O APROVADO: {arquivo}")
            falhas += 1

    if len(vistos) < 5 or len(reais_red) < 4:
        print(f"  FALHOU: contraprova magra — {len(vistos)} rechecks e {len(reais_red)} "
              "relatórios reais examinados")
        falhas += 1

    # O achado da leva: a maioria das execuções reais não tinha o que rechecar.
    inaplicaveis = vereditos.count("not_applicable")
    if inaplicaveis < 2:
        print(f"  FALHOU: só {inaplicaveis} recheck(s) reais saíram `not_applicable` — o gate "
              "voltou a tratar conjunto vazio como aprovação")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações adversariais falharam")
        return 1
    print(f"ok: {casos} verificações — {len(vistos)} rechecks e {len(reais_red)} relatórios reais, "
          f"nenhum reprovado; {inaplicaveis} deles deixaram de mentir `pass` sobre conjunto vazio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
