# -*- coding: utf-8 -*-
"""forja_red_team.py — gates computados `red_team_completed` e
`adversarial_claims_rechecked` (F7).

Os dois eram escritos pelo agente da F7. O red team estruturado é o gate que a
casa criou depois do erro recorrente nº 2 — premissa não declarada — e ganhou
uma nona pergunta no upgrade U4 de 09/07/2026, a anti-bajulação: *a peça aceita
premissa do comando ou do e-mail que os AUTOS não sustentam?*

A medição de 04/08/2026 no acervo:

  red_team_report.md      seis relatórios reais, com 5, 6, 9, 12, 12 e 12
                          objeções enumeradas. O protocolo pede 9.
  adversarial_recheck     oito execuções; SEIS declaram `applicable: false`
                          com motivo escrito, e as oito reportaram `pass`.

Esse segundo número é a MC-15 em escala: três quartos das execuções do gate
mediram o conjunto vazio e devolveram aprovação. Quando não há peça adversária,
não há alegação a rechecar — e o veredito honesto é `not_applicable`, que
preserva a diferença entre "nada a examinar" e "examinado e aprovado".

Calibração deliberada: exigir exatamente 9 objeções reprovaria retroativamente
relatórios reais e substantivos (o da CASO-17 tem 6 objeções densas, cada uma
com resposta calibrada). Menos de 9 é `warn` com o número dito; ausência de
enumeração é que reprova.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

_GATE_VERSAO = "FORJA-RED-TEAM-v1"
GATE_RED_TEAM = "red_team_completed"
GATE_RECHECK = "adversarial_claims_rechecked"

# O protocolo U4 fixou nove perguntas; a nona é a anti-bajulação.
_PERGUNTAS_PROTOCOLO = 9
_MINIMO_ACEITAVEL = 3
_ITEM = re.compile(r"^\s*(?:[-*+]|\d{1,2}[.)])\s+\S", re.M)


def _itens_enumerados(texto: str) -> int:
    return len(_ITEM.findall(texto or ""))


def validar_red_team(relatorio):
    """Achados e veredito do gate `red_team_completed`.

    `relatorio` é o texto do red_team_report.md (ou None quando ausente).
    """
    if not isinstance(relatorio, str) or not relatorio.strip():
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LRT1-relatorio-ausente", "sev": "P0",
                              "problema": ("red_team_report ausente ou vazio - a peca nao passou "
                                           "pelo red team estruturado"),
                              "acao": ("responda por escrito as nove perguntas do protocolo U4, "
                                       "inclusive a nona, anti-bajulacao"),
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_RED_TEAM: "fail"}}

    achados = []
    itens = _itens_enumerados(relatorio)
    if itens < _MINIMO_ACEITAVEL:
        achados.append({
            "gate": "LRT2-sem-objecoes-enumeradas", "sev": "P0",
            "problema": (f"o relatorio de red team enumera {itens} objecao(oes) - nao ha exame "
                         "adversarial identificavel"),
            "acao": "enumere as objecoes do protocolo U4 e a resposta a cada uma",
            "versao": _GATE_VERSAO})
    elif itens < _PERGUNTAS_PROTOCOLO:
        achados.append({
            "gate": "LRT3-abaixo-do-protocolo", "sev": "P1",
            "problema": (f"o relatorio enumera {itens} objecoes e o protocolo U4 fixou "
                         f"{_PERGUNTAS_PROTOCOLO}, entre elas a anti-bajulacao"),
            "acao": "complete as perguntas faltantes do protocolo",
            "versao": _GATE_VERSAO})

    if any(a["sev"] == "P0" for a in achados):
        veredito = "fail"
    elif achados:
        veredito = "warn"
    else:
        veredito = "pass"
    return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_RED_TEAM: veredito}}


def _itens_rechecados(recheck: dict) -> list:
    itens = []
    for campo in ("recheckedIssues", "findingsRechecked", "citationsRechecked",
                  "externalAllegations", "alegacoesRechecadas"):
        valor = recheck.get(campo)
        if isinstance(valor, list):
            itens.extend(valor)
    return itens


def validar_recheck_adversarial(recheck):
    """Achados e veredito do gate `adversarial_claims_rechecked`."""
    if not isinstance(recheck, dict) or not recheck:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LAR1-recheck-ausente", "sev": "P0",
                              "problema": ("adversarial_recheck ausente ou vazio - nao ha registro "
                                           "de rechecagem das alegacoes adversarias"),
                              "acao": "emita adversarial_recheck, ainda que para declarar que nao se aplica",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_RECHECK: "fail"}}

    achados = []
    aplicavel = recheck.get("applicable")
    itens = _itens_rechecados(recheck)
    motivo = recheck.get("notApplicableReason") or recheck.get("reason")

    if aplicavel is False:
        if not (isinstance(motivo, str) and motivo.strip()):
            achados.append({
                "gate": "LAR2-inaplicavel-sem-motivo", "sev": "P1",
                "problema": ("o recheck se declara inaplicavel sem dizer por que - inaplicabilidade "
                             "sem motivo escrito e indistinguivel de omissao"),
                "acao": "declare por que nao ha peca adversaria a rechecar",
                "versao": _GATE_VERSAO})
            return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_RECHECK: "warn"}}
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LAR3-inaplicavel-declarado", "sev": "INFO",
                              "problema": f"nao ha peca adversaria a rechecar: {motivo[:160]}",
                              "acao": "nenhuma; o gate nao se aplica a este caso",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_RECHECK: "not_applicable"}}

    if aplicavel is True and not itens:
        achados.append({
            "gate": "LAR4-aplicavel-sem-item", "sev": "P0",
            "problema": ("o recheck se declara aplicavel e nao lista nenhuma alegacao rechecada - "
                         "o gate seria calculado sobre conjunto vazio"),
            "acao": "liste cada alegacao adversaria e o resultado da rechecagem",
            "versao": _GATE_VERSAO})

    if aplicavel is None:
        if itens:
            achados.append({
                "gate": "LAR5-aplicabilidade-nao-declarada", "sev": "P2",
                "problema": ("o recheck nao declara se ha peca adversaria, embora liste itens "
                             "rechecados"),
                "acao": "declare applicable explicitamente",
                "versao": _GATE_VERSAO})
        else:
            achados.append({
                "gate": "LAR5-aplicabilidade-nao-declarada", "sev": "P0",
                "problema": ("o recheck nao declara aplicabilidade nem lista alegacao alguma - nao "
                             "e possivel saber se houve exame"),
                "acao": "declare applicable e, sendo aplicavel, liste as alegacoes rechecadas",
                "versao": _GATE_VERSAO})

    sem_resultado = [i for i in itens
                     if isinstance(i, dict) and not (i.get("result") or i.get("resultado")
                                                     or i.get("conclusion"))]
    if sem_resultado:
        achados.append({
            "gate": "LAR6-alegacao-sem-resultado", "sev": "P1",
            "problema": (f"{len(sem_resultado)} alegacao(oes) rechecada(s) sem resultado registrado - "
                         "listar a alegacao nao e rechecar"),
            "acao": "registre a conclusao de cada rechecagem",
            "versao": _GATE_VERSAO})

    if any(a["sev"] == "P0" for a in achados):
        veredito = "fail"
    elif achados:
        veredito = "warn"
    else:
        veredito = "pass"
    return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_RECHECK: veredito}}


def validar_exame_adversarial(relatorio, recheck):
    """Junta os dois gates adversariais da F7 num laudo só."""
    red = validar_red_team(relatorio)
    rec = validar_recheck_adversarial(recheck)
    return {"versao": _GATE_VERSAO,
            "findings": red["findings"] + rec["findings"],
            "gates": {**red["gates"], **rec["gates"]}}


if __name__ == "__main__":  # pragma: no cover
    import sys
    pasta = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    relatorio = None
    alvo = pasta / "red_team_report.md"
    if alvo.is_file():
        relatorio = alvo.read_text(encoding="utf-8", errors="replace")
    recheck = {}
    alvo = pasta / "adversarial_recheck.json"
    if alvo.is_file():
        try:
            recheck = json.loads(alvo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            recheck = {}
    print(json.dumps(validar_exame_adversarial(relatorio, recheck), ensure_ascii=False, indent=2))
