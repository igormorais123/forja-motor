# -*- coding: utf-8 -*-
"""test_forja_paragrafos.py — regressão do gate computado `paragraphs_sourced`.

DEVE_REPROVAR   — as formas de declarar lastro sem ter lastro.
NAO_PODE_TRAVAR — o que é legítimo e um gate ingênuo reprovaria: cabeçalho
                  editorial sem fonte, e hash gravado com CRLF sobre arquivo
                  em LF (o caso VerifACT V8 — divergência de fim de linha, não
                  de conteúdo; conferir sem normalizar reprovaria peça correta).
CONTRAPROVA     — os CINCO dialetos reais do acervo, cada um com o seu
                  rascunho. Nenhum pode ser reprovado.

Uso: python test_forja_paragrafos.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_paragrafos import GATE, carregar_e_validar, validar_paragrafos_lastreados  # noqa: E402

RASCUNHO = ("# Peça\n\nO primeiro parágrafo afirma um fato do processo.\n\n"
            "O segundo parágrafo afirma outro fato.\n\nPede deferimento.\n")

DEVE_REPROVAR = [
    ("proveniência ausente", None, RASCUNHO),
    ("proveniência vazia", {}, RASCUNHO),
    ("declarada sem nenhuma unidade",
     {"schemaVersion": 1, "paragraphs": []}, RASCUNHO),
    ("parágrafo factual sem lastro e sem isenção",
     {"paragraphs": [{"id": "P1", "supports": ["F1"]}, {"id": "P2"}]}, RASCUNHO),
    ("lastro declarado como lista vazia",
     {"paragraphs": [{"id": "P1", "factIds": [], "sourceIds": []}]}, RASCUNHO),
    ("proveniência de rascunho anterior (hash não bate)",
     {"markdownSha256": "0" * 64,
      "paragraphs": [{"id": "P1", "supports": ["F1"]}]}, RASCUNHO),
    ("trecho citado que não existe no rascunho",
     {"paragraphs": [{"id": "P1", "supports": ["F1"],
                      "textPrefix": "O terceiro parágrafo afirma coisa nenhuma"}]}, RASCUNHO),
]

NAO_PODE_TRAVAR = [
    ("cabeçalho editorial sem fonte é isenção legítima",
     {"blocks": [{"blockId": "b1", "kind": "heading", "claimClass": "editorial",
                  "factIds": [], "startLine": 1, "endLine": 1},
                 {"blockId": "b2", "kind": "paragraph", "factIds": ["F1"],
                  "startLine": 3, "endLine": 3}]},
     "# Peça\n\nO primeiro parágrafo afirma um fato do processo.\n"),
    ("hash gravado em CRLF sobre arquivo em LF",
     {"markdownSha256": __import__("hashlib").sha256(
         RASCUNHO.replace("\n", "\r\n").encode("utf-8")).hexdigest(),
      "paragraphs": [{"id": "P1", "supports": ["F1"]}]}, RASCUNHO),
    ("lastro em texto corrido, dialeto CASO-17",
     {"paragraphs": [{"id": "P1", "provenance": "fact_ledger/source_ledger",
                      "textPrefix": "O primeiro parágrafo afirma um fato"}]}, RASCUNHO),
]


def main() -> int:
    falhas = 0
    casos = 0

    for nome, prov, draft in DEVE_REPROVAR:
        casos += 1
        if validar_paragrafos_lastreados(prov, draft)["gates"][GATE] != "fail":
            print(f"  FALHOU (não pegou): {nome}")
            falhas += 1

    for nome, prov, draft in NAO_PODE_TRAVAR:
        casos += 1
        if validar_paragrafos_lastreados(prov, draft)["gates"][GATE] == "fail":
            print(f"  TRAVOU INDEVIDAMENTE: {nome}")
            falhas += 1

    # Um gate cego devolve `pass` sobre conjunto vazio; este precisa dizer não.
    casos += 1
    if validar_paragrafos_lastreados({"paragraphs": []}, RASCUNHO)["gates"][GATE] != "fail":
        print("  FALHOU: conjunto vazio devolveu aprovação (MC-15)")
        falhas += 1

    # Onde a cobertura não é computável, o gate não pode mentir `pass`.
    casos += 1
    if validar_paragrafos_lastreados(
            {"paragraphs": [{"id": "P1", "supports": ["F1"]}]}, None)["gates"][GATE] != "warn":
        print("  FALHOU: cobertura não computável deveria ser `warn`, não aprovação")
        falhas += 1

    # CONTRAPROVA — os dialetos reais do acervo.
    dialetos = {}
    for arquivo in Path("state").rglob("paragraph_provenance.json"):
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if isinstance(dados, dict) and isinstance(dados.get("main"), dict):
            dados = dados["main"]
        if not isinstance(dados, dict):
            continue
        chave = tuple(sorted(dados))
        if chave in dialetos:
            continue
        dialetos[chave] = arquivo
        casos += 1
        if carregar_e_validar(arquivo.parent)["gates"][GATE] == "fail":
            print(f"  TRAVOU O APROVADO: {arquivo.parent}")
            falhas += 1

    if len(dialetos) < 4:
        print(f"  FALHOU: só {len(dialetos)} dialetos reais examinados — "
              "a contraprova perdeu o acervo")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações de lastro por parágrafo falharam")
        return 1
    print(f"ok: {casos} verificações — reprova as {len(DEVE_REPROVAR)} formas de declarar "
          f"lastro sem lastro e não trava nenhum dos {len(dialetos)} dialetos reais")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
