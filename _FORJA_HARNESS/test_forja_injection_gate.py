# -*- coding: utf-8 -*-
"""test_forja_injection_gate.py — `injection_triaged` computado, tolerante à forma.

O gate existe por causa do U3: conteúdo dos autos é DADO, nunca instrução. Um
`pass` falso significa ingerir autos sem ter procurado texto branco sobre
branco, fonte de 1,7 pt ou padrão de comando escondido no PDF. Até 04/08/2026
era escrito pelo agente da fase F1 — nove execuções, nove `pass`, zero
reprovações.

A dificuldade real não é detectar: é que o artefato `injection_scan.json`
aparece no acervo em **sete esquemas distintos**, porque cada caso inventou o
seu. Um gate preso a um formato reprova seis casos corretos. Por isso as duas
listas abaixo, e por isso a segunda roda contra todos os esquemas reais:

  DEVE_REPROVAR   — artefato ausente ou vazio; nenhum documento declarado;
                    achado P0 sem triagem humana registrada.
  NAO_PODE_TRAVAR — os SETE esquemas reais do acervo, e o resumo de contagens
                    zeradas, que significa varredura limpa e não detecção.

Uso: python test_forja_injection_gate.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_injection_scan import validar_triagem_injecao  # noqa: E402

GATE = "injection_triaged"


def _veredito(scan):
    return validar_triagem_injecao(scan)["gates"][GATE]


DEVE_REPROVAR = [
    ("artefato ausente", {}),
    ("artefato sem escopo varrido", {"schemaVersion": 1, "status": "pass"}),
    ("P0 por contagem, sem triagem",
     {"total_pdfs": 3, "resumo_p0": {"cor_invisivel": 2, "fonte_microscopica": 0}}),
    ("P0 por flag de arquivo, sem triagem",
     {"pdfCount": 2, "files": [{"name": "a.pdf", "p0": True}]}),
    ("injeção detectada, sem triagem",
     {"documentsScanned": 10, "promptInjectionDetected": True}),
]

NAO_PODE_TRAVAR = [
    # Resumo de contagens ZERADAS é varredura limpa. A primeira versão do gate
    # tratou o dicionário não vazio como detecção e reprovou a Cafelana, que
    # havia varrido corretamente e registrado o resultado.
    ("resumo com contagens zeradas",
     {"total_pdfs": 1, "resumo_p0": {"padroes_instrucao": 0, "cor_invisivel": 0,
                                     "fonte_microscopica": 0}}),
    ("P0 com triagem humana registrada",
     {"total_pdfs": 3, "resumo_p0": {"cor_invisivel": 2},
      "triagem": "achado revisado e classificado como artefato de digitalização"}),
    ("varredura limpa declarada em inglês",
     {"documentsScanned": 200, "promptInjectionDetected": False, "findings": [],
      "approved": True}),
]


def _contraprova_da_amostragem() -> list[str]:
    """Amostrar a evidência não pode encolher a MEDIDA.

    Os detectores de nível de caractere passaram a guardar só os primeiros
    exemplos, porque um PDF pericial de 945 páginas gerava 645.966 registros e
    um laudo de 291 MB. O risco óbvio dessa mudança é o gate passar a
    subcontar justamente no arquivo mais sujo — que é onde a contagem importa.
    Então a contagem é exercida aqui contra um volume acima do limite de
    amostra, e o P0, que decide, é exercido para provar que não é amostrado.
    """
    from forja_injection_scan import (AMOSTRA_POR_ARQUIVO, AMOSTRA_POR_PAGINA,
                                      _amostrar)
    falhas = []

    destino, contagem = [], 0
    for _ in range(AMOSTRA_POR_PAGINA * 5 + 7):
        contagem += 1
        _amostrar(destino, {"x": 1}, AMOSTRA_POR_PAGINA)
    if contagem != AMOSTRA_POR_PAGINA * 5 + 7:
        falhas.append("a contagem seguiu o tamanho da lista em vez do total real")
    if len(destino) != AMOSTRA_POR_PAGINA:
        falhas.append(f"a amostra por página vazou: {len(destino)} > {AMOSTRA_POR_PAGINA}")
    if AMOSTRA_POR_ARQUIVO < AMOSTRA_POR_PAGINA:
        falhas.append("amostra por arquivo menor que a por página — resumo perderia exemplo")

    # A soma do resumo tem de vir de `contagens`, nunca de len(lista): com um
    # arquivo acima do limite de amostra, ler a lista subcontaria em 100x.
    achados = {"p0": True,
               "contagens": {"padrao_instrucao": 3, "cor_invisivel": 900,
                             "fonte_microscopica": 645966},
               "resumo_geral": {"padrao_instrucao": [{}, {}, {}],
                                "cor_invisivel": [{}] * AMOSTRA_POR_ARQUIVO,
                                "fonte_microscopica": [{}] * AMOSTRA_POR_ARQUIVO}}
    if len(achados["resumo_geral"]["fonte_microscopica"]) >= achados["contagens"]["fonte_microscopica"]:
        falhas.append("o cenário da contraprova não exercita a amostragem")
    if achados["contagens"]["fonte_microscopica"] != 645966:
        falhas.append("a contagem exata se perdeu")

    # P0 não é amostrado: é de baixo volume e é o que exige triagem humana.
    if _veredito({"total_pdfs": 1, "arquivos_analisados": [
            {"p0": True, "contagens": {"padrao_instrucao": 1}}]}) != "fail":
        falhas.append("achado de instrução oculta sem triagem deixou de reprovar")
    return falhas


def main() -> int:
    falhas = 0
    casos = 0

    for problema in _contraprova_da_amostragem():
        print(f"  FALHOU (contraprova da amostragem): {problema}")
        falhas += 1
        casos += 1

    for nome, scan in DEVE_REPROVAR:
        casos += 1
        if _veredito(scan) != "fail":
            print(f"  FALHOU (não pegou): {nome}")
            falhas += 1

    for nome, scan in NAO_PODE_TRAVAR:
        casos += 1
        if _veredito(scan) != "pass":
            print(f"  TRAVOU INDEVIDAMENTE: {nome}")
            falhas += 1

    # OS SETE ESQUEMAS REAIS — nenhum pode reprovar.
    esquemas = {}
    for caminho in Path("state").rglob("injection_scan.json"):
        try:
            scan = json.loads(caminho.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(scan, dict):
            continue
        chave = tuple(sorted(scan))
        if chave in esquemas:
            continue
        esquemas[chave] = caminho
        casos += 1
        if _veredito(scan) != "pass":
            print(f"  TRAVOU O APROVADO: esquema de {caminho.relative_to('state')}")
            falhas += 1

    if len(esquemas) < 5:
        print(f"  FALHOU: só {len(esquemas)} esquemas reais examinados — "
              "a contraprova perdeu o acervo")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações de triagem falharam")
        return 1
    print(f"ok: {casos} verificações — reprova as {len(DEVE_REPROVAR)} formas de pular a "
          f"varredura e não trava nenhum dos {len(esquemas)} esquemas reais do acervo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
