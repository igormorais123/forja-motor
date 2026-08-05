# -*- coding: utf-8 -*-
"""forja_adversarial_gate.py — gates computados da auditoria adversarial.

    F3   `adversarial_scope_classified`, `adversarial_audit_complete`
    F4   `adversarial_decisions_recorded`, `bad_faith_language_authorized`
    F9   `release_policy_satisfied`

A auditoria adversarial é onde o escritório examina a peça da parte contrária —
e onde o risco de excesso é maior que o de omissão, porque imputar má-fé sem
lastro é problema de OAB, não de qualidade. Por isso o gate de linguagem de
má-fé existe desde a origem da esteira, e por isso ele era autodeclarado: o
mesmo agente que escolhia a linguagem atestava que ela estava autorizada.

Dois verificáveis de verdade saíram da medição:

  1. `adversarial_strategy` declara `auditSha256`, o hash da auditoria que ela
     decide. Se não bater com o arquivo, a estratégia decidiu sobre OUTRA
     auditoria — e nada no artefato denuncia isso.
  2. `applicable: false` com motivo escrito é a forma correta de dizer "não há
     peça adversária", e aparece em quatro dos seis artefatos reais. O veredito
     honesto ali é `not_applicable`, não `pass` — pela mesma razão de sempre.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

_GATE_VERSAO = "FORJA-ADVERSARIAL-GATE-v1"
GATE_ESCOPO = "adversarial_scope_classified"
GATE_AUDITORIA = "adversarial_audit_complete"
GATE_DECISOES = "adversarial_decisions_recorded"
GATE_MA_FE = "bad_faith_language_authorized"
GATE_LIBERACAO = "release_policy_satisfied"

_CAMPOS_MOTIVO = ("notApplicableReason", "reason", "motivo")
_CAMPOS_SUBSTANCIA = ("factualClaims", "contradictions", "citationInventory",
                      "decisivePoints", "researchLog")
_LIMITE_EXEMPLOS = 3


def _motivo(dados: dict) -> str | None:
    for campo in _CAMPOS_MOTIVO:
        valor = dados.get(campo)
        if isinstance(valor, str) and valor.strip():
            return valor.strip()
    return None


def _hashes_do_arquivo(caminho) -> set:
    alvo = Path(caminho)
    if not alvo.is_file():
        return set()
    bruto = alvo.read_bytes()
    texto = bruto.decode("utf-8", errors="replace")
    variantes = {bruto,
                 texto.replace("\r\n", "\n").encode("utf-8"),
                 texto.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8")}
    return {hashlib.sha256(v).hexdigest() for v in variantes}


def validar_auditoria_adversarial(auditoria, estrategia=None, caminho_auditoria=None):
    """Achados e vereditos dos quatro gates adversariais."""
    auditoria = auditoria if isinstance(auditoria, dict) else {}
    estrategia = estrategia if isinstance(estrategia, dict) else {}
    achados = []

    if not auditoria:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LAD1-auditoria-ausente", "sev": "P0",
                              "problema": ("adversarial_audit ausente ou vazio - a peca adversaria "
                                           "nao foi examinada nem declarada inexistente"),
                              "acao": "emita adversarial_audit, ainda que para declarar que nao se aplica",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_ESCOPO: "fail", GATE_AUDITORIA: "fail",
                          GATE_DECISOES: "fail", GATE_MA_FE: "fail"}}

    aplicavel = auditoria.get("applicable")
    motivo = _motivo(auditoria)

    # --- escopo classificado -------------------------------------------------
    if aplicavel is None:
        achados.append({
            "gate": "LAD2-escopo-nao-classificado", "sev": "P0",
            "problema": ("a auditoria nao declara se ha peca adversaria a examinar - sem isso nao "
                         "se sabe se o silencio e ausencia ou omissao"),
            "acao": "declare applicable explicitamente",
            "versao": _GATE_VERSAO})
        escopo = "fail"
    elif aplicavel is False:
        if not motivo:
            achados.append({
                "gate": "LAD3-inaplicavel-sem-motivo", "sev": "P1",
                "problema": "a auditoria se declara inaplicavel sem dizer por que",
                "acao": "escreva por que nao ha peca adversaria a examinar",
                "versao": _GATE_VERSAO})
            escopo = "warn"
        else:
            escopo = "pass"
    else:
        cobertura = auditoria.get("scope") or {}
        if not (isinstance(cobertura, dict) and
                (cobertura.get("pagesOrSectionsCovered") or cobertura.get("fullReadingConfirmed"))):
            achados.append({
                "gate": "LAD4-escopo-sem-cobertura", "sev": "P1",
                "problema": ("a auditoria se declara aplicavel e nao registra o que foi lido da "
                             "peca adversaria"),
                "acao": "registre as secoes ou paginas cobertas e se a leitura foi integral",
                "versao": _GATE_VERSAO})
            escopo = "warn"
        else:
            escopo = "pass"

    # --- auditoria completa --------------------------------------------------
    if aplicavel is False:
        auditoria_veredito = "not_applicable"
    else:
        vazios = [campo for campo in _CAMPOS_SUBSTANCIA if not auditoria.get(campo)]
        if len(vazios) == len(_CAMPOS_SUBSTANCIA):
            achados.append({
                "gate": "LAD5-auditoria-sem-substancia", "sev": "P0",
                "problema": ("a auditoria se declara aplicavel e nao registra alegacao, "
                             "contradicao nem inventario de citacao da peca adversaria"),
                "acao": "registre o que foi encontrado no exame da peca adversaria",
                "versao": _GATE_VERSAO})
            auditoria_veredito = "fail"
        elif vazios:
            auditoria_veredito = "warn"
        else:
            auditoria_veredito = "pass"

    # --- decisões registradas ------------------------------------------------
    if not estrategia:
        achados.append({
            "gate": "LAD6-estrategia-ausente", "sev": "P0",
            "problema": ("adversarial_strategy ausente - os achados da auditoria nao receberam "
                         "decisao"),
            "acao": "emita adversarial_strategy com a decisao sobre cada achado",
            "versao": _GATE_VERSAO})
        decisoes = "fail"
    else:
        # A estratégia decide sobre ESTA auditoria?
        declarado = estrategia.get("auditSha256")
        if declarado and caminho_auditoria:
            reais = _hashes_do_arquivo(caminho_auditoria)
            if reais and declarado.strip().lower() not in reais:
                achados.append({
                    "gate": "LAD7-estrategia-de-outra-auditoria", "sev": "P0",
                    "problema": ("o hash da auditoria declarado na estrategia nao corresponde ao "
                                 "arquivo - as decisoes foram tomadas sobre outra versao do exame"),
                    "acao": "refaca a estrategia sobre a auditoria vigente",
                    "versao": _GATE_VERSAO})

        if estrategia.get("applicable") is False:
            decisoes = "not_applicable" if _motivo(estrategia) else "warn"
            if not _motivo(estrategia):
                achados.append({
                    "gate": "LAD8-estrategia-inaplicavel-sem-motivo", "sev": "P1",
                    "problema": "a estrategia se declara inaplicavel sem motivo escrito",
                    "acao": "escreva por que nao ha decisao adversarial a tomar",
                    "versao": _GATE_VERSAO})
        else:
            itens = [d for d in (estrategia.get("decisions") or []) if isinstance(d, dict)]
            if not itens:
                achados.append({
                    "gate": "LAD9-sem-decisao-registrada", "sev": "P0",
                    "problema": ("a estrategia se declara aplicavel e nao registra decisao "
                                 "sobre achado algum"),
                    "acao": "registre, por achado, a decisao tomada e a razao",
                    "versao": _GATE_VERSAO})
                decisoes = "fail"
            else:
                incompletas = [d for d in itens
                               if not (d.get("decision") and (d.get("rationale") or d.get("razao")))]
                if incompletas:
                    achados.append({
                        "gate": "LAD10-decisao-sem-razao", "sev": "P1",
                        "problema": (f"{len(incompletas)} de {len(itens)} decisoes nao registram "
                                     "a razao"),
                        "acao": "escreva por que cada achado foi acatado, rejeitado ou usado em parte",
                        "versao": _GATE_VERSAO})
                    decisoes = "warn"
                else:
                    decisoes = "pass"
        if any(a["gate"].startswith("LAD7") for a in achados):
            decisoes = "fail"

    # --- linguagem de má-fé --------------------------------------------------
    decisao_ma_fe = (estrategia.get("badFaithDecision")
                     if isinstance(estrategia.get("badFaithDecision"), (dict, str)) else None)
    indicadores = auditoria.get("badFaithIndicators")
    usou = bool(indicadores) if isinstance(indicadores, list) else None

    # A ordem importa: indicador de má-fé ENCONTRADO sem decisão que o autorize
    # é P0, e precisa ser testado antes do caso geral de decisão ausente. Na
    # primeira versão o caso geral vinha primeiro e engolia o específico,
    # rebaixando para `warn` justamente a situação mais grave.
    if usou and decisao_ma_fe is None:
        achados.append({
            "gate": "LAD12-ma-fe-indicada-sem-autorizacao", "sev": "P0",
            "problema": (f"a auditoria lista {len(indicadores)} indicador(es) de ma-fe e nenhuma "
                         "decisao autoriza usa-los na peca"),
            "acao": "decida expressamente se a ma-fe sera imputada, e com que lastro",
            "versao": _GATE_VERSAO})
        ma_fe = "fail"
    elif decisao_ma_fe is None and not motivo and aplicavel is not False:
        achados.append({
            "gate": "LAD11-ma-fe-sem-decisao", "sev": "P1",
            "problema": ("nao ha decisao registrada sobre imputar ou nao ma-fe a parte contraria - "
                         "excesso aqui e problema de OAB, nao de qualidade"),
            "acao": "registre expressamente a decisao sobre linguagem de ma-fe",
            "versao": _GATE_VERSAO})
        ma_fe = "warn"
    elif aplicavel is False:
        ma_fe = "not_applicable"
    else:
        ma_fe = "pass"

    return {"versao": _GATE_VERSAO, "findings": achados,
            "gates": {GATE_ESCOPO: escopo, GATE_AUDITORIA: auditoria_veredito,
                      GATE_DECISOES: decisoes, GATE_MA_FE: ma_fe}}


def validar_politica_liberacao(manifesto, gate_result=None):
    """Gate da F9: o pacote não libera mais do que a auditoria autorizou."""
    achados = []
    manifesto = manifesto if isinstance(manifesto, dict) else {}
    gate_result = gate_result if isinstance(gate_result, dict) else {}
    entregaveis = [d for d in (manifesto.get("deliverables") or []) if isinstance(d, dict)]

    if not entregaveis:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LAD13-pacote-sem-entregavel", "sev": "P0",
                              "problema": ("o manifesto nao lista entregavel - a politica de "
                                           "liberacao seria conferida sobre conjunto vazio"),
                              "acao": "liste os entregaveis e a politica de cada um",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_LIBERACAO: "fail"}}

    externo = None
    for campo in ("approvedForExternalRelease", "approvedForClientOrFiling", "approvedForPromotion"):
        if isinstance(gate_result.get(campo), bool):
            externo = gate_result[campo]
            break

    estritos = [d for d in entregaveis
                if str(d.get("releasePolicy") or "").strip().lower() == "strict_protocol"]
    if estritos and externo is False:
        achados.append({
            "gate": "LAD14-pacote-libera-alem-da-auditoria", "sev": "P0",
            "problema": (f"{len(estritos)} entregavel(is) classificado(s) como strict_protocol "
                         "enquanto a auditoria da F7 negou a liberacao externa"),
            "acao": "rebaixe a politica do pacote ou reabra a F7",
            "versao": _GATE_VERSAO})
        return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_LIBERACAO: "fail"}}

    sem_politica = [d for d in entregaveis if not d.get("releasePolicy")]
    if sem_politica:
        achados.append({
            "gate": "LAD15-entregavel-sem-politica", "sev": "P1",
            "problema": (f"{len(sem_politica)} de {len(entregaveis)} entregaveis nao declaram "
                         "politica de liberacao"),
            "acao": "declare, por entregavel, ate onde ele pode ir",
            "versao": _GATE_VERSAO})
        return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_LIBERACAO: "warn"}}

    if externo is None:
        achados.append({
            "gate": "LAD16-auditoria-sem-decisao-de-liberacao", "sev": "P2",
            "problema": ("o resultado da F7 nao declara se a liberacao externa foi aprovada - a "
                         "politica do pacote nao tem contra o que ser conferida"),
            "acao": "declare a decisao de liberacao no f7_gate_result",
            "versao": _GATE_VERSAO})
        return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_LIBERACAO: "warn"}}

    return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_LIBERACAO: "pass"}}


if __name__ == "__main__":  # pragma: no cover
    import sys

    pasta = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

    def _ler(nome):
        alvo = pasta / nome
        if not alvo.is_file():
            return {}
        try:
            return json.loads(alvo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return {}

    print(json.dumps(validar_auditoria_adversarial(
        _ler("adversarial_audit.json"), _ler("adversarial_strategy.json"),
        pasta / "adversarial_audit.json"), ensure_ascii=False, indent=2))
