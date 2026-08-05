# -*- coding: utf-8 -*-
"""forja_produto.py — gates computados de definição: `product_defined`,
`audience_defined`, `release_policy_defined` (F2), `jurisdictional_question_defined`
(F4) e `final_use_policy_recorded` (F5).

São os gates que dizem PARA QUE a esteira está trabalhando. Um `pass` falso
aqui não produz erro visível: produz uma esteira inteira sem alvo, que entrega
um produto tecnicamente correto e estrategicamente inútil — o modo de falha mais
caro e o menos denunciado, porque ninguém reclama de trabalho bem-feito na
pergunta errada.

A regra da casa que este módulo carimba é a da pergunta jurisdicional: uma
frase, antes do blueprint, dizendo o que exatamente se pede ao juízo. Ela está
no catálogo de gates desde 08/07/2026 e era atestada pelo agente.

O que se verifica é SUBSTÂNCIA contra rótulo. `product: "peça"` satisfaz
qualquer verificação de existência de campo e não define nada. Por isso há piso
de tamanho — calibrado contra os cinco artefatos reais, cujo campo `product`
mais curto tem 38 caracteres ("peticao_inicial_tjdft_revisada_v8") e o mais
longo tem 78.
"""
from __future__ import annotations

import json
import re

_GATE_VERSAO = "FORJA-PRODUTO-v1"
GATE_PRODUTO = "product_defined"
GATE_PUBLICO = "audience_defined"
GATE_LIBERACAO = "release_policy_defined"
GATE_PERGUNTA = "jurisdictional_question_defined"
GATE_USO_FINAL = "final_use_policy_recorded"

# Piso medido: o menor `product` real do acervo tem 33 caracteres. 12 é folgado
# o bastante para não travar rótulo legítimo curto e apertado o bastante para
# reprovar "peça", "parecer" e "minuta" — que nomeiam a espécie sem definir nada.
_PISO_DEFINICAO = 12
_PISO_PERGUNTA = 25

_CAMPOS_PRODUTO = ("product", "selectedProduct", "produto", "deliverable")
_CAMPOS_PUBLICO = ("audience", "primaryAudience", "audiences", "publico", "destinatario")
_CAMPOS_LIBERACAO = ("releasePolicy", "release_policy", "politicaLiberacao", "usePolicy")
_CAMPOS_PERGUNTA = ("jurisdictionalQuestion", "perguntaJurisdicional", "jurisdictional_question",
                    "questaoJurisdicional", "coreQuestion")
_CAMPOS_USO_FINAL = ("finalUsePolicy", "usePolicy", "finalUseAllowed", "politicaUsoFinal")

_GENERICOS = re.compile(
    r"^(pe[çc]a|parecer|minuta|documento|texto|manifesta[çc][ãa]o|peti[çc][ãa]o|"
    r"recurso|agravo|embargos|draft|documento jur[íi]dico|an[áa]lise|analise)$", re.I)


def _texto(fonte: dict, campos) -> str | None:
    if not isinstance(fonte, dict):
        return None
    for campo in campos:
        valor = fonte.get(campo)
        if isinstance(valor, str) and valor.strip():
            return valor.strip()
        if isinstance(valor, list) and valor:
            juntos = ", ".join(str(v).strip() for v in valor if str(v).strip())
            if juntos:
                return juntos
        if isinstance(valor, dict) and valor:
            return json.dumps(valor, ensure_ascii=False)
    return None


def _conferir(fonte, campos, gate, rotulo, piso, achados, *, obrigatorio=True):
    valor = _texto(fonte, campos)
    if not valor:
        achados.append({
            "gate": f"LPD-{gate}", "sev": "P0" if obrigatorio else "P1",
            "problema": f"{rotulo} nao esta declarado",
            "acao": f"declare {rotulo} antes de seguir para a proxima fase",
            "versao": _GATE_VERSAO})
        return "fail" if obrigatorio else "warn"
    if _GENERICOS.match(valor.strip()):
        achados.append({
            "gate": f"LPD-{gate}", "sev": "P0",
            "problema": (f"{rotulo} esta declarado como rotulo generico ('{valor[:40]}') - "
                         "nomeia a especie sem definir o alvo"),
            "acao": f"diga qual {rotulo} especificamente, e para que serve neste caso",
            "versao": _GATE_VERSAO})
        return "fail"
    if len(valor) < piso:
        achados.append({
            "gate": f"LPD-{gate}", "sev": "P1",
            "problema": (f"{rotulo} tem {len(valor)} caracteres, abaixo do piso de {piso} - "
                         "definicao curta demais para orientar a esteira"),
            "acao": f"detalhe {rotulo}",
            "versao": _GATE_VERSAO})
        return "warn"
    return "pass"


def validar_definicao_produto(classificacao):
    """Gates da F2: produto, público e política de liberação."""
    achados = []
    fonte = classificacao if isinstance(classificacao, dict) else {}
    if not fonte:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LPD-classificacao-ausente", "sev": "P0",
                              "problema": ("product_classification ausente ou vazio - a esteira "
                                           "seguiria sem saber o que esta produzindo"),
                              "acao": "emita product_classification com produto, publico e liberacao",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_PRODUTO: "fail", GATE_PUBLICO: "fail", GATE_LIBERACAO: "fail"}}

    return {"versao": _GATE_VERSAO, "findings": achados, "gates": {
        GATE_PRODUTO: _conferir(fonte, _CAMPOS_PRODUTO, GATE_PRODUTO, "o produto",
                                _PISO_DEFINICAO, achados),
        GATE_PUBLICO: _conferir(fonte, _CAMPOS_PUBLICO, GATE_PUBLICO, "o publico destinatario",
                                _PISO_DEFINICAO, achados),
        GATE_LIBERACAO: _conferir(fonte, _CAMPOS_LIBERACAO, GATE_LIBERACAO,
                                  "a politica de liberacao", 6, achados),
    }}


# O blueprint aparece no acervo em JSON e em markdown — medido: 3 JSON e 12
# markdown. Um gate que só lesse JSON reprovaria doze artefatos reais por
# formato, que é o erro que esta frente inteira existe para não cometer.
#
# Segunda calibração, 04/08/2026: exigir a palavra "jurisdicional" reprovou
# CINCO blueprints reais que cumprem a regra com outro rótulo — "Pergunta
# central" na Natura Cabreúva, "Pergunta decisória" no Cafelana. E o Cafelana
# nem tem juízo a quem perguntar: o produto ali é uma reunião com a AGU. A regra
# da casa não é a palavra; é a obrigação de escrever em UMA frase o que se pede
# a quem decide, antes de arquitetar a peça. Cobrar o rótulo em vez da
# substância é o erro que esta frente inteira existe para não cometer, e o gate
# o cometeu em cinco de nove blueprints.
_PERGUNTA_NO_TEXTO = re.compile(
    r"(?im)^#{0,6}\s*(?:\d+[.)]\s*)?(?:pergunta|quest[ãa]o)\s+"
    r"(?:jurisdicional|decis[óo]ria|central|principal|do\s+caso)[^\n]*\n+(?!#)(.{25,})")


def validar_pergunta_jurisdicional(blueprint):
    """Gate da F4: a pergunta que se faz ao juízo, em uma frase.

    Aceita o blueprint como dicionário (JSON) ou como texto (markdown).
    """
    achados = []
    if isinstance(blueprint, str):
        encontrado = _PERGUNTA_NO_TEXTO.search(blueprint)
        valor = encontrado.group(1).strip() if encontrado else None
        fonte = {}
    else:
        fonte = blueprint if isinstance(blueprint, dict) else {}
        valor = _texto(fonte, _CAMPOS_PERGUNTA)
    if not valor:
        achados.append({
            "gate": "LPD-pergunta-jurisdicional-ausente", "sev": "P0",
            "problema": ("o blueprint nao declara a pergunta jurisdicional - regra da casa desde "
                         "08/07/2026: uma frase, antes do blueprint, dizendo o que se pede ao juizo"),
            "acao": "escreva a pergunta jurisdicional em uma frase",
            "versao": _GATE_VERSAO})
        return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_PERGUNTA: "fail"}}
    if len(valor) < _PISO_PERGUNTA:
        achados.append({
            "gate": "LPD-pergunta-jurisdicional-rasa", "sev": "P1",
            "problema": (f"a pergunta jurisdicional tem {len(valor)} caracteres - curta demais "
                         "para dizer o que se pede e sobre o que"),
            "acao": "reescreva a pergunta de forma que ela sozinha oriente a peca",
            "versao": _GATE_VERSAO})
        return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_PERGUNTA: "warn"}}
    return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_PERGUNTA: "pass"}}


def validar_uso_final(ledger):
    """Gate da F5: a política de uso final de cada fonte está registrada."""
    achados = []
    fonte = ledger if isinstance(ledger, dict) else {}
    fontes = []
    for campo in ("sources", "entries", "fontes", "officialSources"):
        valor = fonte.get(campo)
        if isinstance(valor, list) and valor:
            fontes = [f for f in valor if isinstance(f, dict)]
            break
    if not fontes:
        achados.append({
            "gate": "LPD-uso-final-sem-fontes", "sev": "P0",
            "problema": ("nao ha fonte alguma para registrar politica de uso final - o gate seria "
                         "calculado sobre conjunto vazio"),
            "acao": "registre as fontes e o que cada uma autoriza afirmar",
            "versao": _GATE_VERSAO})
        return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_USO_FINAL: "fail"}}

    global_ = _texto(fonte, _CAMPOS_USO_FINAL)
    sem_politica = [f for f in fontes if not _texto(f, _CAMPOS_USO_FINAL)
                    and f.get("finalUseAllowed") is None]
    if sem_politica and not global_:
        achados.append({
            "gate": "LPD-uso-final-nao-registrado", "sev": "P1",
            "problema": (f"{len(sem_politica)} de {len(fontes)} fontes nao registram o que "
                         "autorizam afirmar, e nao ha politica global declarada"),
            "acao": "registre, por fonte, o que ela sustenta e o que nao sustenta",
            "versao": _GATE_VERSAO})
        return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_USO_FINAL: "warn"}}
    return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_USO_FINAL: "pass"}}


if __name__ == "__main__":  # pragma: no cover
    import sys
    from pathlib import Path

    pasta = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

    def _ler(nome):
        alvo = pasta / nome
        if not alvo.is_file():
            return {}
        try:
            return json.loads(alvo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return {}

    saida = validar_definicao_produto(_ler("product_classification.json"))
    saida["gates"].update(validar_pergunta_jurisdicional(_ler("blueprint.json"))["gates"])
    saida["gates"].update(validar_uso_final(_ler("source_ledger.json"))["gates"])
    print(json.dumps(saida, ensure_ascii=False, indent=2))
