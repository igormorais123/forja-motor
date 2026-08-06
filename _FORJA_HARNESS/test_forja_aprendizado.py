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


# ------------------------------------------------------- comparabilidade
# O filtro que separa correção de ruído. Sem ele, três retornos que não eram
# revisão da nossa peça responderam por 496 das mudanças observadas em 2026 e,
# agregados por classe, tinham a forma exata de um padrão do escritório.
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    state_real = ap.STATE
    ap.STATE = base / "state"
    try:
        def montar(caso: str, resumo: dict | None, quantos: int, sub: str = "n4_artifacts") -> None:
            pasta = ap.STATE / caso / sub
            pasta.mkdir(parents=True, exist_ok=True)
            if resumo is not None:
                (pasta / "F10_POST_PROTOCOL_DOCUMENT_COMPARISON.json").write_text(
                    json.dumps({"summary": resumo}), encoding="utf-8")
            (pasta / "F10_LEARNING_CANDIDATE.json").write_text(json.dumps({
                "caseId": caso,
                "candidates": [{"layer": "fact", "cause": "fact", "impact": "material",
                                "confidence": 0.9} for _ in range(quantos)],
            }), encoding="utf-8")

        montar("caso-revisao", {"sharedTokenRatio": 0.5, "retainedBlockRuns": 35}, 3)
        montar("caso-outro-documento", {"sharedTokenRatio": 0.03, "retainedBlockRuns": 0}, 76)
        montar("caso-sem-medida", {"retainedBlockRuns": 40}, 20)
        montar("caso-revisao", {"sharedTokenRatio": 0.5, "retainedBlockRuns": 35}, 9,
               sub="n4_artifacts/post_protocol_history/abc")

        vivos, descartados = ap.levantar_candidatos()
        checar("candidato de comparação incomparável não entra", len(vivos) == 3,
               f"vieram {len(vivos)}")
        checar("o descarte é devolvido com o motivo, não some", len(descartados) == 2)
        checar("comparação sem medida não é aprovada por omissão",
               any(d["caso"] == "caso-sem-medida" for d in descartados))
        checar("versão superada do mesmo retorno não conta duas vezes",
               all(v["_caso"] == "caso-revisao" for v in vivos) and len(vivos) == 3)
        # Reabre os incomparáveis, mas nunca a versão arquivada: contá-la seria
        # contar duas vezes a mesma correção do titular.
        checar("incluir_incomparaveis reabre os incomparáveis, não o histórico",
               len(ap.levantar_candidatos(incluir_incomparaveis=True)[0]) == 99)
    finally:
        ap.STATE = state_real


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

        # A regra guardou "3 casos"; se a recontagem der menos, quem decide é
        # gente. Foi o que aconteceu de verdade em 06/08/2026: a primeira regra
        # da casa nasceu de um lastro que o gate de comparabilidade dissolveu.
        magros = [{"classe": "fact:fact", "camada": "fact", "causa": "fact",
                   "casos": 1, "ocorrencias": 1, "materiais": 1, "confiancaMedia": 0.9}]
        agrupar_real = ap.agrupar
        levantar_real = ap.levantar_candidatos
        ap.agrupar = lambda _c: magros
        ap.levantar_candidatos = lambda **_k: ([], [])
        try:
            divs = ap.revalidar()
            checar("revalidar acusa lastro que encolheu", len(divs) == 1)
            checar("revalidar mostra o antes e o depois",
                   divs and divs[0]["antes"]["casos"] == 3 and divs[0]["agora"]["casos"] == 1)
        finally:
            ap.agrupar, ap.levantar_candidatos = agrupar_real, levantar_real

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

# O que precisa ficar fora do registro é dado de cliente, e quem sabe reconhecer
# isso é o detector da fronteira — o mesmo que guarda a publicação. O critério
# anterior era o comprimento do texto, proxy fraco que reprovou uma regra
# legítima de nove níveis de hierarquia jurisprudencial: comprimento não é
# vazamento, e a regra da casa pode ser longa quando o procedimento é longo.
import forja_fronteira  # noqa: E402
_nomes, _modo = forja_fronteira.carregar_nomes(ap.RAIZ.parent)
_vazamentos = [
    (r["regraId"], forja_fronteira.sinais_no_texto(str(r.get("texto", "")), _nomes))
    for r in registro["regras"]
]
_vazamentos = [(rid, sinais) for rid, sinais in _vazamentos if sinais]
checar("nenhuma regra carrega dado de cliente", not _vazamentos,
       "; ".join(f"{rid}: {sinais}" for rid, sinais in _vazamentos[:2]))

# Teto generoso, mas existente: regra que ninguém consegue reter não muda peça
# nenhuma, e um texto muito acima disso costuma ser trecho colado.
_longas = [r["regraId"] for r in registro["regras"] if len(str(r.get("texto", ""))) > 900]
checar("nenhuma regra tem tamanho de trecho colado", not _longas, ", ".join(_longas[:3]))

print(f"ok: {casos} casos — o retorno humano vira regra aplicada e conferida "
      f"({len(registro['regras'])} regra(s) ativa(s))" if not falhas
      else f"REGRESSÃO: {falhas} de {casos} casos falharam")
sys.exit(1 if falhas else 0)
