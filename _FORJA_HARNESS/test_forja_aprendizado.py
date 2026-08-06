# -*- coding: utf-8 -*-
"""test_forja_aprendizado.py — a correção humana vira mudança verificável no sistema.

Este teste é o que torna o custo de aprender quase zero. O desenho anterior
exigia um teste NOVO por lição promovida, o que na prática significou uma lição
promovida em 1.096 candidatos. Aqui há **um** teste parametrizado pelo registro:
cada regra adotada é conferida contra o seu destino, e adotar a próxima não
custa uma linha de código a mais.

Ele guarda três coisas distintas:

  1. O mecanismo — agrupar, adotar, aplicar e conferir funcionam sobre dados
     sintéticos, sem depender do acervo.
  2. A idempotência — aplicar duas vezes produz o mesmo arquivo. Sem isso, cada
     execução acrescentaria as regras de novo e o documento de destino cresceria
     até ninguém mais o ler.
  3. O estado real — toda regra efetivamente adotada nesta máquina está presente
     no seu destino. É a diferença entre a casa ter registrado uma lição e ter
     aplicado uma lição.

Uso: python test_forja_aprendizado.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import forja_aprendizado as ap  # noqa: E402

falhas = 0
casos = 0


def checar(nome: str, condicao: bool, detalhe: str = "") -> None:
    global falhas, casos
    casos += 1
    if not condicao:
        falhas += 1
        print(f"  FALHOU: {nome}" + (f" — {detalhe}" if detalhe else ""))


# ------------------------------------------------------- agrupamento
# Dados sintéticos: o teste prova o critério de ordenação, e não precisa de
# nenhum caso real para isso.
SINTETICOS = [
    # Uma classe em três casos distintos, com poucas ocorrências em cada.
    {"_caso": "c1", "layer": "fact", "cause": "fact", "impact": "material", "confidence": 0.9},
    {"_caso": "c2", "layer": "fact", "cause": "fact", "impact": "material", "confidence": 0.8},
    {"_caso": "c3", "layer": "fact", "cause": "fact", "impact": "material", "confidence": 0.7},
    # Uma classe num caso só, com MUITAS ocorrências. Um processo longo produz
    # isto sozinho, e a contagem bruta a colocaria em primeiro lugar.
    *[{"_caso": "c9", "layer": "copy_style_voice", "cause": "style_preference",
       "impact": "não_material", "confidence": 0.5} for _ in range(50)],
]
grupos = ap.agrupar(SINTETICOS)
checar("a classe recorrente entre casos vem antes da volumosa de um caso só",
       grupos[0]["classe"] == "fact:fact",
       f"veio {grupos[0]['classe']} na frente")
checar("recorrência é contada por caso distinto", grupos[0]["casos"] == 3)
checar("volume de um caso só não vira padrão",
       next(g for g in grupos if g["camada"] == "copy_style_voice")["casos"] == 1)
checar("material é contado separado do total",
       grupos[0]["materiais"] == 3 and grupos[0]["ocorrencias"] == 3)

# Campo ausente não derruba o agrupamento: candidato antigo pode não ter camada.
checar("candidato sem camada cai em unknown sem estourar",
       any(g["camada"] == "unknown" for g in ap.agrupar([{"_caso": "x"}])))


# ------------------------------------------------------- adotar e aplicar
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    registro_real, contratos_real, templates_real, raiz_real = (
        ap.REGISTRO, ap.CONTRATOS, ap.TEMPLATES, ap.RAIZ)
    ap.REGISTRO = base / "learning_registry" / "REGRAS_APRENDIDAS.json"
    ap.CONTRATOS = base / "phase_contracts"
    ap.TEMPLATES = base / "templates"
    ap.RAIZ = base / "_FORJA_HARNESS"
    ap.CONTRATOS.mkdir(parents=True)
    (ap.CONTRATOS / "F7.json").write_text(
        json.dumps({"phase": "F7", "gates": []}), encoding="utf-8")
    try:
        regra = ap.adotar("fact:fact", destino="checklist", fase="F7",
                          regra="Conferir cada data contra a fonte primária.",
                          aprovado_por="teste", grupos=grupos)
        checar("adoção guarda a evidência de recorrência",
               regra["evidencia"]["casos"] == 3)
        checar("adoção nasce sem aplicação", regra["aplicadaEm"] is None)

        ap.aplicar()
        contrato = json.loads((ap.CONTRATOS / "F7.json").read_text(encoding="utf-8"))
        checar("a regra chega ao contrato da fase",
               contrato["checklistAprendido"][0]["texto"].startswith("Conferir cada data"))
        checar("o contrato original é preservado", contrato.get("phase") == "F7")
        checar("conferir aprova depois de aplicar", ap.conferir() == [])

        antes = (ap.CONTRATOS / "F7.json").read_text(encoding="utf-8")
        ap.aplicar()
        checar("aplicar duas vezes não muda o arquivo",
               (ap.CONTRATOS / "F7.json").read_text(encoding="utf-8") == antes)

        # Alguém reescreveu o destino por fora: o registro diz que aprendeu, o
        # arquivo diz que não. É este descompasso que o gate precisa acusar.
        (ap.CONTRATOS / "F7.json").write_text(
            json.dumps({"phase": "F7", "gates": []}), encoding="utf-8")
        checar("conferir acusa regra apagada do destino", len(ap.conferir()) == 1)

        # Destino inválido e classe não observada param antes de escrever.
        for chamada, nome in (
            (lambda: ap.adotar("fact:fact", destino="inventado", fase="F7",
                               regra="x", aprovado_por="t", grupos=grupos),
             "destino inválido é recusado"),
            (lambda: ap.adotar("nao:existe", destino="checklist", fase="F7",
                               regra="x", aprovado_por="t", grupos=grupos),
             "classe não observada é recusada"),
            (lambda: ap.adotar("fact:fact", destino="checklist", fase="F7",
                               regra="   ", aprovado_por="t", grupos=grupos),
             "regra vazia é recusada"),
        ):
            try:
                chamada()
                checar(nome, False, "não levantou erro")
            except SystemExit:
                checar(nome, True)
    finally:
        ap.REGISTRO, ap.CONTRATOS, ap.TEMPLATES, ap.RAIZ = (
            registro_real, contratos_real, templates_real, raiz_real)


# ------------------------------------------------------- estado real da máquina
# O ponto do teste: adotar a próxima regra não custa uma linha de código aqui.
problemas = ap.conferir()
checar("toda regra adotada nesta máquina está presente no seu destino",
       problemas == [], "; ".join(problemas[:3]))

registro = ap.carregar_registro()
checar("o registro não guarda trecho de peça",
       not any(len(str(r.get("texto", ""))) > 400 for r in registro["regras"]),
       "uma regra longa demais costuma ser texto colado da peça")

print(f"ok: {casos} casos — o retorno humano vira regra aplicada e conferida "
      f"({len(registro['regras'])} regra(s) ativa(s))" if not falhas
      else f"REGRESSÃO: {falhas} de {casos} casos falharam")
sys.exit(1 if falhas else 0)
