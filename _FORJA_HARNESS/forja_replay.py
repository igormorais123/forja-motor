# -*- coding: utf-8 -*-
"""forja_replay.py — gates computados `live_official_source_replayed`,
`source_excerpt_hash_match` e `citation_coverage_complete` (F7).

Fecham a família de citação, que já tinha `citations_policy_satisfied` e
`citation_identity_and_cnj_tribunal_resolved` computados. Os três respondem a
perguntas diferentes sobre a mesma citação, e confundi-las é o que produz gate
redundante ou gate cego:

    cobertura   a autoridade citada no texto existe no ledger?
    replay      a fonte oficial foi reaberta ao vivo, e respondeu?
    excerto     o trecho transcrito foi reencontrado na fonte reaberta?

O `verified_source_ledger` da CASO-04 traz um `liveReplay` por fonte com
status HTTP, hash do corpo, data de captura e casamento de excerto — dado bom o
bastante para conferência real. Medido em 04/08/2026: quatro fontes, quatro
`ok: true`, e duas com `excerptMatches` preenchido.

A ambiguidade que obriga cautela: `excerptMatches: []` pode significar "nenhum
trecho a conferir" ou "nenhum trecho encontrado". Os dois são indistinguíveis no
artefato, e um gate que escolhesse a leitura pessimista reprovaria fonte citada
sem transcrição — que é a maioria. Lista vazia é `warn`; `fail` só quando há
`matched: false` explícito, que é afirmação de que a busca foi feita e falhou.
"""
from __future__ import annotations

import json
import re
from datetime import date, datetime

_GATE_VERSAO = "FORJA-REPLAY-v1"
GATE_REPLAY = "live_official_source_replayed"
GATE_EXCERTO = "source_excerpt_hash_match"
GATE_COBERTURA = "citation_coverage_complete"

_CAMPOS_FONTES = ("entries", "officialSources", "sources", "fontes")
_LIMITE_EXEMPLOS = 4
# Fonte de ato vivo (processo, andamento, tema em julgamento) precisa de replay;
# norma compilada não muda entre a pesquisa e o protocolo.
_ATO_VIVO = re.compile(r"(?i)\b(processo|autos|andamento|tema|repetitiv|acord[ãa]o|"
                       r"agravo|recurso|aresp|resp|are\b|re\b|s[úu]mula em|portaria)\b")


def _fontes(ledger: dict) -> list:
    for campo in _CAMPOS_FONTES:
        valor = ledger.get(campo)
        if isinstance(valor, list) and valor:
            return [f for f in valor if isinstance(f, dict)]
    return []


def _replays(ledger: dict) -> dict:
    bruto = ledger.get("liveReplay") or ledger.get("live_replay") or {}
    if isinstance(bruto, dict):
        return {k: v for k, v in bruto.items() if isinstance(v, dict)}
    if isinstance(bruto, list):
        saida = {}
        for item in bruto:
            if isinstance(item, dict):
                saida[str(item.get("sourceId") or item.get("id") or len(saida))] = item
        return saida
    return {}


def _data(valor) -> date | None:
    if not isinstance(valor, str) or len(valor) < 10:
        return None
    try:
        return datetime.fromisoformat(valor[:19].replace("Z", "")).date()
    except ValueError:
        return None


def validar_replay(ledger, *, hoje=None, limite_dias=90):
    """Achados e vereditos dos três gates da família de citação."""
    fonte = ledger if isinstance(ledger, dict) else {}
    if not fonte:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LRP1-ledger-ausente", "sev": "P0",
                              "problema": ("verified_source_ledger ausente ou vazio - nao ha "
                                           "registro de conferencia de fonte"),
                              "acao": "emita o ledger de fontes verificadas na F7",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_REPLAY: "fail", GATE_EXCERTO: "fail", GATE_COBERTURA: "fail"}}

    achados = []
    fontes = _fontes(fonte)
    if not fontes:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LRP1-ledger-sem-fontes", "sev": "P0",
                              "problema": ("o ledger nao lista nenhuma fonte - os tres gates "
                                           "seriam calculados sobre conjunto vazio"),
                              "acao": "registre as fontes conferidas",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_REPLAY: "fail", GATE_EXCERTO: "fail", GATE_COBERTURA: "fail"}}

    # --- cobertura: toda fonte tem identidade e decisão de uso ---------------
    sem_identidade = [f for f in fontes
                      if not (f.get("authorityIdentity") or f.get("identifier")
                              or f.get("claim") or f.get("title"))]
    sem_decisao = [f for f in fontes
                   if f.get("finalUseAllowed") is None
                   and not (f.get("status") or f.get("verificationStatus"))]
    if sem_identidade:
        achados.append({
            "gate": "LRP2-fonte-sem-identidade", "sev": "P0",
            "problema": (f"{len(sem_identidade)} de {len(fontes)} entradas do ledger nao "
                         "identificam a autoridade que representam"),
            "acao": "identifique cada fonte pela autoridade e pelo numero do ato",
            "versao": _GATE_VERSAO})
    if sem_decisao:
        achados.append({
            "gate": "LRP3-fonte-sem-decisao-de-uso", "sev": "P1",
            "problema": (f"{len(sem_decisao)} de {len(fontes)} fontes nao dizem se podem ser "
                         "usadas na peca"),
            "acao": "declare finalUseAllowed ou status de verificacao por fonte",
            "versao": _GATE_VERSAO})
    if sem_identidade:
        cobertura = "fail"
    elif sem_decisao:
        cobertura = "warn"
    else:
        cobertura = "pass"

    # --- replay ao vivo ------------------------------------------------------
    replays = _replays(fonte)
    vivas = [f for f in fontes if _ATO_VIVO.search(
        " ".join(str(f.get(c) or "") for c in ("claim", "title", "identifier", "kind")))]
    if not replays:
        achados.append({
            "gate": "LRP4-sem-replay", "sev": "P1",
            "problema": ("o ledger nao registra reabertura ao vivo de fonte alguma"
                         + (f" - {len(vivas)} fonte(s) tratam de ato vivo, que muda"
                            if vivas else "")),
            "acao": ("reabra as fontes de ato vivo e registre status, hash do corpo e data "
                     "de captura"),
            "versao": _GATE_VERSAO})
        replay = "warn"
    else:
        falhos = [chave for chave, item in replays.items()
                  if item.get("ok") is False
                  or (isinstance(item.get("status"), int) and item["status"] >= 400)]
        if falhos:
            achados.append({
                "gate": "LRP5-replay-falhou", "sev": "P0",
                "problema": (f"{len(falhos)} fonte(s) nao responderam na reabertura: "
                             f"{', '.join(list(falhos)[:_LIMITE_EXEMPLOS])}"),
                "acao": "reabra a fonte ou registre a impossibilidade como bloqueio",
                "versao": _GATE_VERSAO})
            replay = "fail"
        else:
            replay = "pass"
            referencia = hoje or date.today()
            velhas = []
            for chave, item in replays.items():
                capturado = _data(item.get("capturedAt") or item.get("checkedAt"))
                if capturado and (referencia - capturado).days > limite_dias:
                    velhas.append(f"{chave} ({(referencia - capturado).days} dias)")
            if velhas:
                achados.append({
                    "gate": "LRP6-replay-envelhecido", "sev": "P1",
                    "problema": (f"{len(velhas)} reabertura(s) com mais de {limite_dias} dias: "
                                 f"{', '.join(velhas[:_LIMITE_EXEMPLOS])}"),
                    "acao": "reabra as fontes de ato vivo antes do protocolo",
                    "versao": _GATE_VERSAO})
                replay = "warn"

    # --- excerto -------------------------------------------------------------
    conferidos, discordantes = 0, []
    for chave, item in replays.items():
        for casamento in (item.get("excerptMatches") or []):
            if not isinstance(casamento, dict):
                continue
            conferidos += 1
            if casamento.get("matched") is False:
                discordantes.append(f"{chave}/{casamento.get('factId') or '?'}")
    if discordantes:
        achados.append({
            "gate": "LRP7-excerto-nao-encontrado", "sev": "P0",
            "problema": (f"{len(discordantes)} trecho(s) transcrito(s) nao foram reencontrados na "
                         f"fonte reaberta: {', '.join(discordantes[:_LIMITE_EXEMPLOS])}"),
            "acao": "corrija a transcricao ou remova a afirmacao que ela sustenta",
            "versao": _GATE_VERSAO})
        excerto = "fail"
    elif conferidos:
        excerto = "pass"
    else:
        # Lista vazia é ambígua: "nada a conferir" ou "nada encontrado". O
        # artefato não distingue, e escolher a leitura pessimista reprovaria a
        # maioria das fontes, que são citadas sem transcrição.
        achados.append({
            "gate": "LRP8-excerto-nao-conferido", "sev": "P2",
            "problema": ("nenhum casamento de trecho foi registrado - nao e possivel saber se "
                         "havia transcricao a conferir ou se ela nao foi encontrada"),
            "acao": "registre, por transcricao, se ela foi reencontrada na fonte",
            "versao": _GATE_VERSAO})
        excerto = "warn"

    return {"versao": _GATE_VERSAO, "findings": achados,
            "gates": {GATE_REPLAY: replay, GATE_EXCERTO: excerto, GATE_COBERTURA: cobertura}}


if __name__ == "__main__":  # pragma: no cover
    import sys
    from pathlib import Path

    alvo = Path(sys.argv[1] if len(sys.argv) > 1 else "verified_source_ledger.json")
    dados = {}
    if alvo.is_file():
        try:
            dados = json.loads(alvo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            dados = {}
    print(json.dumps(validar_replay(dados), ensure_ascii=False, indent=2))
