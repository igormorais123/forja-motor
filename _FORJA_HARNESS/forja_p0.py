# -*- coding: utf-8 -*-
"""forja_p0.py — gates computados `p0_zero` e `producer_reviewer_separation` (F7).

`p0_zero` é o gate central da esteira: nenhuma peça é declarada pronta com P0
não justificado. E era aritmética escrita à mão — o agente contava os próprios
achados e escrevia o total.

O que se computa aqui é a coerência entre o número declarado e a lista de
achados do MESMO artefato. Um artefato que diz `p0: 0` e traz achado P0 na
própria lista está se contradizendo, e nenhuma leitura posterior pega isso
porque o campo continua dizendo zero.

Calibração que evitou uma acusação errada: um `f7_gate_result` real declara
`p0: 0` e tem um achado `severity: P0` — mas o achado traz `resolution`
descrevendo a correção aplicada. Ele é registro histórico de defeito RESOLVIDO,
não pendência. Contar achado resolvido como aberto teria acusado de contradição
o caso que fez exatamente a coisa certa: achou, corrigiu e deixou a trilha.

`producer_reviewer_separation` é o caso mais barato da frente: `_validate_result`
já derruba a fase quando produtor e revisor são a mesma execução, desde antes
desta frente existir. O gate era autodeclarado porque ninguém tinha ligado o
nome à conferência que já acontecia.
"""
from __future__ import annotations

import json

_GATE_VERSAO = "FORJA-P0-v1"
GATE_P0 = "p0_zero"
GATE_SEPARACAO = "producer_reviewer_separation"

_CAMPOS_ACHADOS = ("findings", "p0Findings", "achados", "issues")
_CAMPOS_RESOLUCAO = ("resolution", "resolucao", "resolvedAt", "fixedIn", "correcao")
_LIMITE_EXEMPLOS = 4


def _payload(achado: dict) -> dict:
    """Alguns achados guardam os campos dentro de um JSON serializado em `detail`.

    Achado real em 04/08/2026: o F7 do CASO-04 declara 48 P0 e traz 49 achados
    cuja severidade vive dentro da string
    `detail = '{"severity": "P0", "code": ...}'`. Lendo só o topo, o gate via
    zero P0, chamava de contradição uma contagem correta e acusava de mentir um
    artefato honesto. É a mesma classe de erro que esta frente vinha evitando
    nos outros gates — desta vez ela passou.
    """
    bruto = achado.get("detail") or achado.get("payload") or achado.get("raw")
    if isinstance(bruto, dict):
        return bruto
    if isinstance(bruto, str) and bruto.lstrip().startswith("{"):
        try:
            dados = json.loads(bruto)
        except ValueError:
            return {}
        return dados if isinstance(dados, dict) else {}
    return {}


def _severidade(achado: dict) -> str:
    for fonte in (achado, _payload(achado)):
        for campo in ("sev", "severity", "severidade", "nivel"):
            valor = fonte.get(campo)
            if isinstance(valor, str) and valor.strip():
                return valor.strip().upper()
    return ""


def _resolvido(achado: dict) -> bool:
    for fonte in (achado, _payload(achado)):
        for campo in _CAMPOS_RESOLUCAO:
            valor = fonte.get(campo)
            if isinstance(valor, str) and valor.strip():
                return True
            if valor is True:
                return True
    return False


def _achados(resultado: dict) -> list:
    itens = []
    for campo in _CAMPOS_ACHADOS:
        valor = resultado.get(campo)
        if isinstance(valor, list):
            itens.extend(item for item in valor if isinstance(item, dict))
    return itens


def _declarado(resultado: dict):
    for campo in ("p0Count", "p0"):
        valor = resultado.get(campo)
        if isinstance(valor, bool):
            continue
        if isinstance(valor, int):
            return valor
        if isinstance(valor, list):
            return len(valor)
    contagens = resultado.get("severityCounts") or resultado.get("counts")
    if isinstance(contagens, dict):
        for chave in ("P0", "p0"):
            if isinstance(contagens.get(chave), int):
                return contagens[chave]
    return None


def validar_p0(resultado, *, produtor=None, revisor=None):
    """Achados e vereditos de `p0_zero` e `producer_reviewer_separation`."""
    if not isinstance(resultado, dict) or not resultado:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LP01-resultado-ausente", "sev": "P0",
                              "problema": ("f7_gate_result ausente ou vazio - nao ha contagem de "
                                           "P0 nem lista de achados"),
                              "acao": "emita f7_gate_result com a contagem e os achados da auditoria",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_P0: "fail", GATE_SEPARACAO: "fail"}}

    achados = []
    lista = _achados(resultado)
    abertos = [item for item in lista if _severidade(item).startswith("P0") and not _resolvido(item)]
    resolvidos = [item for item in lista if _severidade(item).startswith("P0") and _resolvido(item)]
    declarado = _declarado(resultado)

    if abertos:
        rotulos = [str(item.get("gate") or item.get("detail") or "achado")[:60]
                   for item in abertos[:_LIMITE_EXEMPLOS]]
        achados.append({
            "gate": "LP02-p0-aberto", "sev": "P0",
            "problema": (f"{len(abertos)} achado(s) P0 sem resolucao registrada: "
                         f"{'; '.join(rotulos)}"),
            "acao": "resolva o P0 ou registre a justificativa antes de declarar a peca pronta",
            "versao": _GATE_VERSAO})

    if declarado is None:
        achados.append({
            "gate": "LP03-contagem-nao-declarada", "sev": "P1",
            "problema": "o resultado da F7 nao declara a contagem de P0",
            "acao": "declare p0 ou p0Count no f7_gate_result",
            "versao": _GATE_VERSAO})
    elif declarado != len(abertos):
        achados.append({
            "gate": "LP04-contagem-contradiz-achados", "sev": "P0",
            "problema": (f"o resultado declara {declarado} P0 e a propria lista traz "
                         f"{len(abertos)} aberto(s)"
                         + (f" ({len(resolvidos)} ja resolvido(s), corretamente fora da conta)"
                            if resolvidos else "")),
            "acao": "reconcilie a contagem com a lista de achados do mesmo artefato",
            "versao": _GATE_VERSAO})

    # producer_reviewer_separation — nomeia a conferência que o runner já fazia.
    separacao = "pass"
    if produtor is not None and revisor is not None:
        if not str(produtor).strip() or not str(revisor).strip():
            achados.append({
                "gate": "LP05-papel-nao-identificado", "sev": "P0",
                "problema": "produtor ou revisor da fase nao esta identificado",
                "acao": "identifique as duas execucoes no PHASE_RESULT",
                "versao": _GATE_VERSAO})
            separacao = "fail"
        elif str(produtor).strip() == str(revisor).strip():
            achados.append({
                "gate": "LP06-produtor-revisor-iguais", "sev": "P0",
                "problema": ("produtor e revisor da fase sao a mesma execucao - a revisao nao e "
                             "independente"),
                "acao": "execute a revisao numa sessao distinta da que produziu",
                "versao": _GATE_VERSAO})
            separacao = "fail"
    else:
        separacao = "warn"

    p0_reprovado = any(a["gate"].startswith(("LP01", "LP02", "LP04")) and a["sev"] == "P0"
                       for a in achados)
    p0_incerto = any(a["gate"].startswith("LP03") for a in achados)
    return {"versao": _GATE_VERSAO, "findings": achados,
            "gates": {GATE_P0: "fail" if p0_reprovado else ("warn" if p0_incerto else "pass"),
                      GATE_SEPARACAO: separacao}}


if __name__ == "__main__":  # pragma: no cover
    import sys
    from pathlib import Path

    alvo = Path(sys.argv[1] if len(sys.argv) > 1 else "f7_gate_result.json")
    dados = {}
    if alvo.is_file():
        try:
            dados = json.loads(alvo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            dados = {}
    print(json.dumps(validar_p0(dados), ensure_ascii=False, indent=2))
