# -*- coding: utf-8 -*-
"""test_forja_produto.py — regressão dos gates de definição.

O que estes gates protegem não é um erro visível: é uma esteira inteira sem
alvo, produzindo trabalho tecnicamente correto sobre a pergunta errada. Ninguém
reclama disso, e por isso ele nunca aparece — a não ser que algo o meça.

Medido em 04/08/2026: os treze `product_classification` reais passam nos três
gates. Já a pergunta jurisdicional, exigida pelo catálogo desde 08/07, é
declarada em apenas 4 dos 15 blueprints do acervo — e o gate reportou `pass` nos
quinze. Esse número é achado, não calibração a corrigir.

Uso: python test_forja_produto.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_produto import (  # noqa: E402
    GATE_LIBERACAO, GATE_PERGUNTA, GATE_PRODUTO, GATE_PUBLICO, GATE_USO_FINAL,
    validar_definicao_produto, validar_pergunta_jurisdicional, validar_uso_final)

BOM = {"product": "parecer técnico-jurídico sobre a liquidação por arbitramento",
       "audience": "Fábio Medina Osório e equipe interna",
       "releasePolicy": "internal_review_only"}


def main() -> int:
    falhas = 0
    casos = 0

    def checar(nome, obtido, esperado):
        nonlocal falhas, casos
        casos += 1
        if obtido != esperado:
            print(f"  FALHOU: {nome} — esperado {esperado}, obtido {obtido}")
            falhas += 1

    def g(dados, gate):
        return validar_definicao_produto(dados)["gates"][gate]

    checar("classificação ausente", g(None, GATE_PRODUTO), "fail")
    checar("produto não declarado",
           g({k: v for k, v in BOM.items() if k != "product"}, GATE_PRODUTO), "fail")
    # Rótulo genérico satisfaz "o campo existe" e não define nada.
    for generico in ("peça", "parecer", "minuta", "petição"):
        casos += 1
        if g({**BOM, "product": generico}, GATE_PRODUTO) != "fail":
            print(f"  FALHOU: rótulo genérico '{generico}' foi aceito como definição")
            falhas += 1
    checar("produto curto demais", g({**BOM, "product": "réplica"}, GATE_PRODUTO), "warn")
    checar("definição completa", g(BOM, GATE_PRODUTO), "pass")
    checar("público declarado", g(BOM, GATE_PUBLICO), "pass")
    checar("liberação declarada", g(BOM, GATE_LIBERACAO), "pass")
    checar("público em lista",
           g({**BOM, "audience": ["Fábio Medina Osório", "juízo cível do TJDFT"]},
             GATE_PUBLICO), "pass")

    # Pergunta jurisdicional: JSON e markdown.
    checar("pergunta ausente", validar_pergunta_jurisdicional({})["gates"][GATE_PERGUNTA], "fail")
    checar("pergunta rasa",
           validar_pergunta_jurisdicional({"jurisdictionalQuestion": "cabe?"})["gates"][GATE_PERGUNTA],
           "warn")
    checar("pergunta em JSON",
           validar_pergunta_jurisdicional(
               {"jurisdictionalQuestion": "A decisão do evento 228 podia manter a TIPI sem "
                                          "enfrentar o acórdão do AI 5039469?"}
           )["gates"][GATE_PERGUNTA], "pass")
    checar("pergunta em markdown",
           validar_pergunta_jurisdicional(
               "# Blueprint\n\n## Pergunta jurisdicional\n\nA decisão do evento 228 podia "
               "manter a TIPI sem enfrentar o acórdão do AI 5039469?\n"
           )["gates"][GATE_PERGUNTA], "pass")
    checar("markdown sem a pergunta",
           validar_pergunta_jurisdicional("# Blueprint\n\n## Rota escolhida\n\nEmbargos.\n"
                                          )["gates"][GATE_PERGUNTA], "fail")

    # CONTRAPROVA da segunda calibração: os rótulos reais do acervo. Exigir a
    # palavra "jurisdicional" reprovava cinco blueprints que cumprem a regra —
    # e um deles nem tem juízo a quem perguntar, porque o produto é uma reunião.
    checar("rótulo 'Pergunta central' (CASO-17)",
           validar_pergunta_jurisdicional(
               "# Blueprint\n\n## Pergunta central\n\nQuais capítulos do crédito permanecem "
               "juridicamente exigíveis em 2026, dada a negativa de 2019?\n"
           )["gates"][GATE_PERGUNTA], "pass")
    checar("rótulo numerado 'Pergunta decisória' (CASO-04)",
           validar_pergunta_jurisdicional(
               "# Blueprint\n\n## 1. Pergunta decisória\n\nComo conduzir uma reunião capaz de "
               "produzir fonte reconhecida sem converter lacuna em cifra?\n"
           )["gates"][GATE_PERGUNTA], "pass")
    # A calibração afrouxou o RÓTULO e não a substância: título sem frase embaixo
    # continua reprovado, senão bastaria escrever o cabeçalho para passar.
    checar("rótulo aceito mas sem frase embaixo",
           validar_pergunta_jurisdicional(
               "# Blueprint\n\n## Pergunta central\n\n## Arquitetura\n\nEmbargos.\n"
           )["gates"][GATE_PERGUNTA], "fail")

    checar("uso final sem fontes", validar_uso_final({"sources": []})["gates"][GATE_USO_FINAL],
           "fail")
    checar("uso final não registrado",
           validar_uso_final({"sources": [{"id": "S1", "authority": "STJ"}]}
                             )["gates"][GATE_USO_FINAL], "warn")
    checar("uso final por fonte",
           validar_uso_final({"sources": [{"id": "S1", "finalUseAllowed": True}]}
                             )["gates"][GATE_USO_FINAL], "pass")

    # CONTRAPROVA — as classificações reais não podem reprovar.
    classificacoes = 0
    for arquivo in Path("state").rglob("product_classification.json"):
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not isinstance(dados, dict):
            continue
        classificacoes += 1
        casos += 1
        laudo = validar_definicao_produto(dados)
        reprovados = [n for n, v in laudo["gates"].items() if v == "fail"]
        if reprovados:
            print(f"  TRAVOU O APROVADO: {arquivo} em {', '.join(reprovados)}")
            falhas += 1

    if classificacoes < 8:
        print(f"  FALHOU: só {classificacoes} classificações reais examinadas")
        falhas += 1

    # O blueprint em markdown precisa ser lido; se o leitor quebrar, o número
    # de aprovações cai a zero e a regressão avisa.
    aprovados_md = 0
    for arquivo in Path("state").rglob("F4_BLUEPRINT_ESTRATEGICO/**/blueprint*.md"):
        texto = arquivo.read_text(encoding="utf-8", errors="replace")
        if validar_pergunta_jurisdicional(texto)["gates"][GATE_PERGUNTA] == "pass":
            aprovados_md += 1
    casos += 1
    if aprovados_md < 2:
        print(f"  FALHOU: só {aprovados_md} blueprint(s) markdown reconhecido(s) — o leitor de "
              "markdown quebrou e o gate passaria a reprovar por formato")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações de definição falharam")
        return 1
    print(f"ok: {casos} verificações — {classificacoes} classificações reais passam; "
          f"{aprovados_md} blueprints markdown com pergunta jurisdicional reconhecida")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
