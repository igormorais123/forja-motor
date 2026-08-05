# -*- coding: utf-8 -*-
"""test_forja_p0.py — regressão de `p0_zero` e `producer_reviewer_separation`.

A contraprova que define a calibração: um `f7_gate_result` real declara `p0: 0`
e traz um achado `severity: P0` — com campo `resolution` descrevendo a correção.
É registro de defeito RESOLVIDO, e contá-lo como aberto acusaria de contradição
justamente o caso que achou, corrigiu e deixou a trilha.

Uso: python test_forja_p0.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_p0 import GATE_P0, GATE_SEPARACAO, validar_p0  # noqa: E402

RESOLVIDO = {"severity": "P0", "gate": "L1-lastro", "detail": "misquote do critério temporal",
             "resolution": "corrigido no ledger e no § 38 da minuta"}
ABERTO = {"severity": "P0", "gate": "L1-lastro", "detail": "valor sem âncora"}


def main() -> int:
    falhas = 0
    casos = 0

    def checar(nome, obtido, esperado):
        nonlocal falhas, casos
        casos += 1
        if obtido != esperado:
            print(f"  FALHOU: {nome} — esperado {esperado}, obtido {obtido}")
            falhas += 1

    def p0(dados, **kw):
        return validar_p0(dados, **kw)["gates"][GATE_P0]

    def sep(dados, **kw):
        return validar_p0(dados, **kw)["gates"][GATE_SEPARACAO]

    checar("resultado ausente", p0(None), "fail")
    checar("resultado vazio", p0({}), "fail")
    checar("P0 aberto na lista", p0({"p0": 1, "findings": [ABERTO]}), "fail")
    checar("declara zero e tem P0 aberto", p0({"p0": 0, "findings": [ABERTO]}), "fail")
    checar("declara um e não tem nenhum aberto", p0({"p0": 1, "findings": []}), "fail")
    # A calibração que veio do acervo.
    checar("P0 já resolvido, fora da conta de abertos",
           p0({"p0": 0, "p0Count": 0, "findings": [RESOLVIDO]}), "pass")
    checar("zero limpo", p0({"p0": 0, "findings": []}), "pass")
    checar("contagem não declarada", p0({"findings": []}), "warn")
    checar("dialeto severityCounts",
           p0({"severityCounts": {"P0": 0, "P1": 6}, "findings": []}), "pass")

    # Sexto dialeto, achado no F7 do CASO-04 em 04/08/2026: a severidade mora
    # dentro de um JSON serializado no campo `detail`. Lendo só o topo, o gate
    # via zero P0 sobre 48 declarados e acusava de contraditório um artefato
    # correto — reprovar trabalho bem-feito é o defeito mais caro de um gate.
    ANINHADO = {"code": "unknown_provenance_reference",
                "detail": '{"severity": "P0", "code": "unknown_provenance_reference"}'}
    checar("severidade aninhada em detail conta como P0 aberto",
           p0({"p0": 48, "findings": [ANINHADO]}), "fail")
    checar("48 declarados com 48 aninhados não é contradição",
           p0({"p0": 2, "findings": [ANINHADO, ANINHADO]}), "fail")
    checar("aninhado já resolvido sai da conta de abertos",
           p0({"p0": 0, "findings": [{"detail": '{"severity": "P0", "resolution": "corrigido"}'}]}),
           "pass")

    checar("produtor e revisor iguais",
           sep({"p0": 0}, produtor="agente-x", revisor="agente-x"), "fail")
    checar("produtor vazio", sep({"p0": 0}, produtor="", revisor="agente-y"), "fail")
    checar("produtor e revisor distintos",
           sep({"p0": 0}, produtor="agente-x", revisor="agente-y"), "pass")
    checar("papéis não informados ao gate", sep({"p0": 0}), "warn")

    # CONTRAPROVA — os resultados reais. Só pode reprovar quem tem P0 aberto.
    dialetos, reprovados = {}, 0
    for arquivo in Path("state").rglob("f7_gate_result.json"):
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not isinstance(dados, dict):
            continue
        chave = tuple(sorted(dados))
        if chave in dialetos:
            continue
        dialetos[chave] = arquivo
        casos += 1
        veredito = p0(dados)
        if veredito == "fail":
            reprovados += 1
            # Reprovar é legítimo quando o próprio artefato declara P0 aberto.
            declarado = dados.get("p0") if isinstance(dados.get("p0"), int) else dados.get("p0Count")
            if not declarado:
                print(f"  TRAVOU O APROVADO: {arquivo}")
                for item in validar_p0(dados)["findings"]:
                    print(f"      {item['gate']}: {item['problema'][:150]}")
                falhas += 1

    if len(dialetos) < 6:
        print(f"  FALHOU: só {len(dialetos)} resultados reais examinados — a contraprova "
              "perdeu o acervo")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações de P0 falharam")
        return 1
    print(f"ok: {casos} verificações — {len(dialetos)} resultados reais, {reprovados} reprovado(s) "
          "por P0 que o próprio artefato declara aberto")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
