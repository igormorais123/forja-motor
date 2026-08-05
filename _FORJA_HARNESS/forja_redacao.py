# -*- coding: utf-8 -*-
"""forja_redacao.py — gates computados da F6: voz humana, entidades estrangeiras,
origem operacional e template.

O escritório já tinha os detectores certos, instalados no lugar errado. O gate
de estilo humano (`forja_estilo_humano.analisar`) e o de origem operacional
(`_OPERATIONAL_ORIGIN`) rodam na F7-B, quando o editor reescreve o texto —
depois de a peça inteira já ter sido redigida. Na F6, onde o texto NASCE, os
gates equivalentes eram escritos pelo próprio agente: oito execuções, oito
`pass`.

É a lição 3 do plano visual noutra roupa: gate instalado na rota tarde demais
custa um ciclo inteiro de reescrita quando acusa. Aqui eles passam a rodar
sobre o rascunho, e o custo é zero — medido em 04/08/2026 contra os treze
rascunhos reais do acervo, os dois detectores produzem ZERO achado. Não é sorte:
é a prova de que o padrão da casa já é o que eles cobram, e de que instalá-los
mais cedo não trava ninguém.

O que este módulo NÃO faz: decidir quem é entidade estranha ao caso. Isso exige
saber quem pertence à causa, e um gate que adivinha isso erra contra o cliente.
O que ele exige é que a conferência tenha sido feita COM SUBSTÂNCIA — lista de
entidades esperadas e de inesperadas —, não com um booleano.
"""
from __future__ import annotations

import json
from pathlib import Path

_GATE_VERSAO = "FORJA-REDACAO-v1"
GATE_VOZ = "human_voice_protocol_applied"
GATE_ENTIDADES = "foreign_entities_clear"
GATE_TEMPLATE = "template_selected"

_CAMPOS_ENTIDADES = ("foreignEntityCheck", "unexplainedForeignEntities", "entidadesEstrangeiras")
_CAMPOS_TEMPLATE = ("template", "templateUsed", "modelo", "baseTemplate")
_LIMITE_EXEMPLOS = 3


def _origem_operacional(texto: str) -> list:
    from forja_editorial_fidelity import _OPERATIONAL_ORIGIN
    achados = []
    for padrao in _OPERATIONAL_ORIGIN:
        encontrado = padrao.search(texto)
        if encontrado:
            achados.append(encontrado.group(0)[:180])
    return achados


def _estilo_p0(texto: str) -> list:
    from forja_estilo_humano import analisar
    return [item for item in analisar(texto, "peca") if item.get("sev") == "P0"]


def validar_redacao(prov, draft_texto=None):
    """Achados e vereditos dos três gates da F6."""
    prov = prov if isinstance(prov, dict) else {}
    if isinstance(prov.get("main"), dict):
        prov = prov["main"]
    achados = []

    # --- voz humana e origem operacional -----------------------------------
    if not draft_texto:
        achados.append({
            "gate": "LRD1-rascunho-ausente", "sev": "P0",
            "problema": ("o rascunho da F6 nao esta disponivel para conferencia - os gates de "
                         "voz e de origem operacional seriam calculados sobre nada"),
            "acao": "declare draft_markdown entre as saidas da fase",
            "versao": _GATE_VERSAO})
        voz = "fail"
    else:
        vazamentos = _origem_operacional(draft_texto)
        if vazamentos:
            achados.append({
                "gate": "LRD2-origem-operacional-no-texto", "sev": "P0",
                "problema": (f"o rascunho expoe origem operacional proibida: "
                             f"{'; '.join(vazamentos[:_LIMITE_EXEMPLOS])}"),
                "acao": ("substitua por referencia processual verdadeira - documento juntado aos "
                         "autos, evento/ID, e-STJ fl. X"),
                "versao": _GATE_VERSAO})
        estilo = _estilo_p0(draft_texto)
        for item in estilo[:_LIMITE_EXEMPLOS]:
            achados.append({
                "gate": "LRD3-cara-de-ia", "sev": "P0",
                "problema": f"{item.get('gate')}: {item.get('problema')}",
                "acao": "reescreva o trecho na voz do escritorio",
                "versao": _GATE_VERSAO})
        voz = "fail" if (vazamentos or estilo) else "pass"

    # --- entidades estrangeiras --------------------------------------------
    declaracao = None
    for campo in _CAMPOS_ENTIDADES:
        if campo in prov:
            declaracao = prov[campo]
            break
    controles = prov.get("qualityControls")
    if declaracao is None and isinstance(controles, dict):
        for campo in _CAMPOS_ENTIDADES:
            if campo in controles:
                declaracao = controles[campo]
                break

    if declaracao is None:
        achados.append({
            "gate": "LRD4-entidades-nao-conferidas", "sev": "P1",
            "problema": ("a proveniencia nao registra conferencia de entidades estranhas ao caso - "
                         "silencio nao e conferencia"),
            "acao": "declare as entidades esperadas e as inesperadas encontradas no texto",
            "versao": _GATE_VERSAO})
        entidades = "warn"
    elif isinstance(declaracao, dict):
        inesperadas = declaracao.get("unexpectedEntities") or declaracao.get("inesperadas") or []
        status = str(declaracao.get("status") or "").lower()
        if inesperadas:
            achados.append({
                "gate": "LRD5-entidade-estranha-no-texto", "sev": "P0",
                "problema": (f"a propria conferencia lista {len(inesperadas)} entidade(s) estranha(s) "
                             f"ao caso: {', '.join(str(e)[:40] for e in inesperadas[:_LIMITE_EXEMPLOS])}"),
                "acao": "remova ou justifique cada entidade estranha antes de fechar a F6",
                "versao": _GATE_VERSAO})
            entidades = "fail"
        elif status and not status.startswith("pass"):
            achados.append({
                "gate": "LRD5-entidade-estranha-no-texto", "sev": "P0",
                "problema": f"a conferencia de entidades foi encerrada com status '{status}'",
                "acao": "resolva a conferencia de entidades antes de fechar a F6",
                "versao": _GATE_VERSAO})
            entidades = "fail"
        else:
            entidades = "pass"
    elif declaracao is True:
        # `unexplainedForeignEntities: true` é a afirmação de que HÁ entidade
        # não explicada; o mesmo campo em outro dialeto é `false` para dizer que
        # não há. O booleano nu é ambíguo por natureza, e aqui a leitura segue
        # o nome do campo em que ele apareceu.
        achados.append({
            "gate": "LRD5-entidade-estranha-no-texto", "sev": "P0",
            "problema": "a proveniencia declara entidade estranha nao explicada no texto",
            "acao": "explique ou remova a entidade",
            "versao": _GATE_VERSAO})
        entidades = "fail"
    else:
        entidades = "pass"

    # --- template ----------------------------------------------------------
    template = None
    for campo in _CAMPOS_TEMPLATE:
        valor = prov.get(campo)
        if isinstance(valor, str) and valor.strip():
            template = valor
            break
    if template is None:
        achados.append({
            "gate": "LRD6-template-nao-declarado", "sev": "P1",
            "problema": ("a proveniencia nao declara de qual modelo a peca partiu - o padrao da "
                         "casa proibe documento vazio e exige o template timbrado"),
            "acao": "declare o template de origem em paragraph_provenance",
            "versao": _GATE_VERSAO})
        modelo = "warn"
    else:
        modelo = "pass"

    return {"versao": _GATE_VERSAO, "findings": achados,
            "gates": {GATE_VOZ: voz, GATE_ENTIDADES: entidades, GATE_TEMPLATE: modelo}}


if __name__ == "__main__":  # pragma: no cover
    import sys
    pasta = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    prov = {}
    alvo = pasta / "paragraph_provenance.json"
    if alvo.is_file():
        try:
            prov = json.loads(alvo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            prov = {}
    texto = None
    alvo = pasta / "draft_markdown.md"
    if alvo.is_file():
        texto = alvo.read_text(encoding="utf-8")
    print(json.dumps(validar_redacao(prov, texto), ensure_ascii=False, indent=2))
