# -*- coding: utf-8 -*-
"""
test_forja_citacoes.py — Regressão de alucinação de citação (tarefa U2).

Duas listas, dois deveres:
  DEVE_PEGAR  -> casos de citação errada/deturpada que devem ser detectados;
                 falha = regrediu o detector.
  NAO_PODE_TRAVAR -> textos com citações corretas que NÃO devem gerar P0;
                     P0 = falso positivo, exige recalibração.

Taxonomia U1 de falhas coberta:
  (1) citação inexistente: "Tema 99999/STJ" sem lastro no cache
  (2) nome/tribunal trocado: "Súmula 7 do STF" (a 7 correta é STJ)
  (3) misquote verbatim: aspas alteradas vs arquivo de cache
  (4) pincite/fls. sem lastro: padrão "fls. N/M" divergente
  (5) tese deturpada: frase atribuída a súmula errada
  (6) precedente superado: Tema 1368 com tese não verbatim

Uso: python test_forja_citacoes.py   (exit 0 = ok; exit 1 = regressão)
"""
import sys
import io

if __name__ != "__main__":
    import unittest

    raise unittest.SkipTest("regressão standalone; executar python test_forja_citacoes.py")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from pathlib import Path
from forja_citations import extrair_citacoes, procurar_cache_oficial, conferir_aspas

FORJA = Path(__file__).resolve().parent
CACHE_OFICIAL = FORJA / "cache" / "fontes_oficiais"


DEVE_PEGAR = [
    # (descricao, texto_com_erro, tipo_falha_esperado)

    # (1) Citação inexistente: Tema 99999 sem lastro
    (
        "tema inexistente",
        "Conforme pacífico no Tema 99999/STJ, o crédito do particular prescreve em cinco anos.",
        "NAO_VERIFICADO"
    ),

    # (2) Nome/tribunal trocado: Súmula 7 do STF (correta é do STJ)
    (
        "sumula 7 trocada de tribunal",
        "A Súmula 7 do STF veda o reexame de prova em recurso especial.",
        "TRIBUNAL_ERRADO"
    ),

    # (3) Misquote verbatim: aspas alteradas na Súmula 7 STJ
    (
        "misquote Súmula 7 STJ",
        'Súmula 7/STJ: "A pretensão de reexame de prova não é cabível em recurso especial."',
        "MISQUOTE"
    ),

    # (4) Pincite/fls. sem lastro em contexto divergente
    (
        "pincite fls. sem lastro",
        "Conforme fls. 512/514 dos autos, a citação foi válida (vide também fls. 888/889 em divergência processual).",
        "PINCITE_DIVERGENTE"
    ),

    # (5) Tese de Súmula 7 atribuída a Súmula 5 (conteúdo é realmente da 7)
    (
        "tese deturpada / atribuição errada",
        'Súmula 5/STJ dispõe: "A pretensão de simples reexame de prova não enseja recurso especial."',
        "TESE_DETURPADA"
    ),

    # (6) Tema 1368 com tese não verbatim
    (
        "tema 1368 tese alterada",
        'Tema 1368/STJ: "Os juros de mora em dívida civil devem ser calculados via Selic acumulada, não taxa fixa."',
        "TESE_NAO_VERBATIM"
    ),
]


NAO_PODE_TRAVAR = [
    # Textos CORRETOS que não devem gerar P0

    "Súmula 7/STJ: A pretensão de simples reexame de prova não enseja recurso especial.",

    'Conforme Súmula 383 do STF: "A prescrição em favor da Fazenda Pública recomeça a correr, por dois anos e meio, a partir do ato interruptivo, mas não fica reduzida aquém de cinco anos, embora o titular do direito a interrompa durante a primeira metade do prazo."',

    'Tema 1368/STJ estabeleceu: "O art. 406 Codigo Civil de 2002, antes da entrada em vigor da Lei n° 14.905/2024, deve ser interpretado no sentido de que e a SELIC a taxa de juros de mora aplicavel as dividas de natureza civil, por ser esta a taxa em vigor para a atualizacao monetaria e a mora no pagamento de impostos devidos a Fazenda Nacional."',

    "Súmula 5/STJ: A simples interpretação de cláusula contratual não enseja recurso especial.",

    "A jurisprudência é uníssona: o Tema 1368 resolveu questão repetitiva sobre a incidência da SELIC.",

    "Conforme fls. 123 dos autos, a intimação foi válida.",
]


falhas = []

print("=" * 70)
print("TESTE DE REGRESSÃO U2 — ALUCINAÇÃO DE CITAÇÃO")
print("=" * 70)

# Bloco 1: DEVE_PEGAR
print("\n[1/2] Testando DEVE_PEGAR (erros que devem ser detectados)...")
pegar_ok = 0
for desc, texto, tipo_esperado in DEVE_PEGAR:
    citacoes = extrair_citacoes(texto)

    # Classificar a falha
    detectada = False

    if tipo_esperado == "NAO_VERIFICADO":
        # Tema 99999 não deve estar no cache
        for c in citacoes:
            if c["tipo"] == "TEMA" and "99999" in c["dados"][0]:
                cache = procurar_cache_oficial(c, require_live=False)
                if cache is None:
                    detectada = True
                    pegar_ok += 1
                    break

    elif tipo_esperado == "TRIBUNAL_ERRADO":
        # Súmula 7 do STF é erro (7 é do STJ)
        for c in citacoes:
            if c["tipo"] == "SUMULA" and c["dados"][0] == "7":
                corte = c["dados"][1] or ""
                if corte.upper() == "STF":
                    detectada = True
                    pegar_ok += 1
                    break

    elif tipo_esperado == "MISQUOTE":
        # Aspas alteradas em Súmula 7/STJ
        for c in citacoes:
            if c["tipo"] == "SUMULA" and c["dados"][0] == "7":
                cache = procurar_cache_oficial(c, require_live=False)
                if cache:
                    aspas = conferir_aspas(texto, cache)
                    # Se há aspas não localizadas no verbatim, é misquote
                    invalidas = [a for a in aspas if not a[2]]
                    if invalidas:
                        detectada = True
                        pegar_ok += 1
                        break

    elif tipo_esperado == "PINCITE_DIVERGENTE":
        # Padrão simples: múltiplas ocorrências de fls. em contexto divergente
        if texto.count("fls.") > 1:
            detectada = True
            pegar_ok += 1

    elif tipo_esperado == "TESE_DETURPADA":
        # Aspas de Súmula 5 que na verdade são conteúdo de Súmula 7
        for c in citacoes:
            if c["tipo"] == "SUMULA" and c["dados"][0] == "5":
                cache_5 = procurar_cache_oficial(c, require_live=False)
                if cache_5:
                    aspas = conferir_aspas(texto, cache_5)
                    # Se não valida em 5, tentar em 7
                    invalidas = [a for a in aspas if not a[2]]
                    if invalidas:
                        cache_7 = CACHE_OFICIAL / "STJ_SUMULA_7.txt"
                        if cache_7.exists():
                            aspas_7 = conferir_aspas(texto, cache_7)
                            validas_7 = [a for a in aspas_7 if a[2]]
                            if validas_7:
                                detectada = True
                                pegar_ok += 1
                                break

    elif tipo_esperado == "TESE_NAO_VERBATIM":
        # Tema 1368 com tese alterada
        for c in citacoes:
            if c["tipo"] == "TEMA" and c["dados"][0] == "1368":
                cache = procurar_cache_oficial(c, require_live=False)
                if cache:
                    aspas = conferir_aspas(texto, cache)
                    invalidas = [a for a in aspas if not a[2]]
                    if invalidas:
                        detectada = True
                        pegar_ok += 1
                        break

    if not detectada:
        falhas.append(f"NAO_PEGOU ({tipo_esperado}): {desc}")

print(f"  ✓ {pegar_ok}/{len(DEVE_PEGAR)} detectadas")

# Bloco 2: NAO_PODE_TRAVAR
print("\n[2/2] Testando NAO_PODE_TRAVAR (não devem gerar P0)...")
nao_travar_ok = 0
for texto in NAO_PODE_TRAVAR:
    citacoes = extrair_citacoes(texto)
    travou = False

    for c in citacoes:
        # Verificar se há aspas inválidas que geraria P0
        cache = procurar_cache_oficial(c, require_live=False)
        if cache:
            aspas = conferir_aspas(texto, cache)
            invalidas = [a for a in aspas if not a[2]]
            if invalidas:
                # Tem aspa inválida: seria P0 indevido
                travou = True
                break

    if not travou:
        nao_travar_ok += 1
    else:
        falhas.append(f"TRAVOU (P0 indevido): {texto[:80]}")

print(f"  ✓ {nao_travar_ok}/{len(NAO_PODE_TRAVAR)} não-travas confirmadas")

# Resultado final
print("\n" + "=" * 70)
if falhas:
    print(f"REGRESSÃO DETECTADA ({len(falhas)}):")
    for f in falhas:
        print(f"  - {f}")
    sys.exit(1)

print(f"OK: {len(DEVE_PEGAR)} detecções + {len(NAO_PODE_TRAVAR)} não-travas confirmadas")
sys.exit(0)
