# -*- coding: utf-8 -*-
"""forja_regimento_gate.py — gates computados da F3: `tribunal_identified`,
`regimento_available` e `critical_facts_sourced`.

A consideração do regimento do tribunal é regra INVIOLÁVEL da casa desde
06/07/2026, criada depois de peças que ignoraram peculiaridades do regimento do
tribunal específico. O gate que a atesta era escrito pelo agente da F3.

Uma distinção importante saiu da medição e vale mais que os limiares:

    **Hash de cópia arquivada e hash de regimento não significam a mesma coisa.**

Cópia arquivada de fonte oficial deve ser congelada — divergência ali é P0
(`forja_fontes_oficiais`, LFA3). O `REGIMENTO_INTERNO_<TRIBUNAL>.md`, ao
contrário, DEVE mudar com o tempo: o protocolo manda pesquisar emendas
posteriores e anexá-las à seção final do próprio arquivo antes de cada peça.

Medido em 04/08/2026: o regimento do caso CASO-17 tem hash divergente do
declarado na F3 de 15/07 — porque o arquivo foi atualizado em 26/07 com a seção
"Emendas posteriores", conferida no portal do TJSP. É o protocolo funcionando.
Tratar isso como P0 reprovaria quem cumpriu a regra. Por isso a divergência de
regimento é `warn` com a causa provável dita, e o que reprova é o regimento
declarado que NÃO EXISTE no disco — aí não há o que ler.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

_GATE_VERSAO = "FORJA-REGIMENTO-GATE-v1"
GATE_TRIBUNAL = "tribunal_identified"
GATE_REGIMENTO = "regimento_available"
GATE_FATOS = "critical_facts_sourced"

_CAMPOS_REGIMENTO = ("regimento", "regiment", "regimentoInterno")
_CAMPOS_TRIBUNAL = ("tribunal", "court", "corte", "juizo", "juízo")
_CAMPOS_LASTRO_FATO = (
    "support", "source", "sources", "supportIds", "sourceId", "sourceIds",
    "evidence", "quote", "quoteSource", "lastro", "fonte",
)
_STATUS_SEM_LASTRO = {"blocked", "bloqueado", "unverified", "not_verified", "nao_verificado",
                      "inference", "inferencia", "inferência", "declaration", "declaracao",
                      "declaração", "pending", "open"}
_LIMITE_EXEMPLOS = 4


def _bloco(dados: dict, campos) -> dict:
    for campo in campos:
        valor = dados.get(campo)
        if isinstance(valor, dict):
            return valor
        if isinstance(valor, str) and valor.strip():
            return {"name": valor}
    return {}


# Os dois artefatos da F3 também existem em MARKDOWN no acervo — o mapa de fontes
# do CASO-23 e o ledger de fatos do CASO-18 só existem nessa forma. Um leitor
# que só abre JSON não erra: ele não vê, e reporta "ledger sem fatos" sobre um
# ledger de nove fatos com localizador processual em cada linha. Foi o que este
# gate fez em 04/08/2026, e o achado chegou a entrar num laudo de triagem como
# defeito do caso antes de o censo de formas mostrar que o defeito era do gate.
_LINHA_TABELA = re.compile(r"^\s*\|(.+)\|\s*$")
# Aceita as duas maneiras reais de declarar o regimento no markdown: o nome do
# arquivo (`REGIMENTO_INTERNO_TRF4.md`) e a prosa que o mapa do CASO-23 usa
# ("Regimento Interno do TRF4, consolidação oficial até o Assento Regimental nº
# 37/2026"). A regra da casa manda considerar o regimento vigente, não escrever
# o nome de um arquivo — cobrar o formato reprovaria um mapa que cumpre a regra
# melhor do que o formato exigia, inclusive com a emenda posterior nomeada.
_REGIMENTO_NO_TEXTO = re.compile(
    r"(?i)REGIMENTO[_ ]INTERNO[_ ]?(?:d[oa]\s+)?([A-Z0-9]{2,8})|"
    r"REGIMENTO\s+d[oa]\s+([A-Z]{2,4}\s?-?\s?\d?)")
_TRIBUNAL_NO_TEXTO = re.compile(
    r"(?i)\b(TRF\s?-?\s?[1-6]|STJ|STF|TJ[A-Z]{2}|TST|TSE|JF[A-Z]{2}|CARF)\b")


def _mapa_em_texto(texto: str) -> dict:
    """Reconstrói o mínimo do sources_map a partir do markdown, sem inventar."""
    saida: dict = {}
    tribunal = _TRIBUNAL_NO_TEXTO.search(texto)
    if tribunal:
        # A base é o próprio documento: o markdown não separa "quem é o tribunal"
        # de "por que se chegou a ele", então o gate reconhece o nome e deixa a
        # falta de fundamento aparecer como P1, que é o que ela é.
        saida["tribunal"] = {"name": tribunal.group(1).upper()}
    regimento = _REGIMENTO_NO_TEXTO.search(texto)
    if regimento:
        saida["regimento"] = {"file": regimento.group(0)}
    return saida


def _fatos_em_texto(texto: str) -> list:
    """Cada linha de tabela com identificador e localizador é um fato lastreado."""
    fatos = []
    for linha in texto.splitlines():
        casado = _LINHA_TABELA.match(linha)
        if not casado:
            continue
        celulas = [c.strip() for c in casado.group(1).split("|")]
        if len(celulas) < 3 or set("".join(celulas)) <= set("- :"):
            continue
        identificador = celulas[0]
        if not re.match(r"^[A-Z][A-Z0-9]*[-_][A-Z0-9\-_.]+$", identificador):
            continue
        lastro = " ".join(celulas[2:]).strip()
        fatos.append({"id": identificador,
                      "statement": celulas[1],
                      "source": lastro or None})
    return fatos


def validar_regimento(sources_map, fact_ledger=None):
    """Achados e vereditos dos três gates da F3.

    Aceita cada artefato como dicionário (JSON) ou texto (markdown).
    """
    if isinstance(sources_map, str):
        sources_map = _mapa_em_texto(sources_map)
    if isinstance(fact_ledger, str):
        fact_ledger = {"facts": _fatos_em_texto(fact_ledger)}
    sources_map = sources_map if isinstance(sources_map, dict) else {}
    achados = []

    if not sources_map:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LRG1-mapa-ausente", "sev": "P0",
                              "problema": ("sources_map ausente ou vazio - a F3 nao registrou "
                                           "tribunal nem regimento"),
                              "acao": "emita sources_map com tribunal, base da identificacao e regimento",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_TRIBUNAL: "fail", GATE_REGIMENTO: "fail", GATE_FATOS: "fail"}}

    # --- tribunal ----------------------------------------------------------
    tribunal = _bloco(sources_map, _CAMPOS_TRIBUNAL)
    nome = tribunal.get("name") or tribunal.get("identified") or tribunal.get("nome")
    if not nome or (isinstance(nome, bool) and nome is False):
        achados.append({
            "gate": "LRG2-tribunal-nao-identificado", "sev": "P0",
            "problema": ("o mapa de fontes nao identifica o tribunal de analise - sem ele nao ha "
                         "regimento aplicavel nem endereçamento"),
            "acao": "identifique o tribunal pelo numero CNJ, endereçamento e decisoes dos autos",
            "versao": _GATE_VERSAO})
        veredito_tribunal = "fail"
    elif not (tribunal.get("basis") or tribunal.get("base") or tribunal.get("fundamento")):
        achados.append({
            "gate": "LRG3-tribunal-sem-base", "sev": "P1",
            "problema": (f"o tribunal esta declarado ({str(nome)[:60]}) sem dizer em que a "
                         "identificacao se apoia"),
            "acao": "registre a base - segmento do CNJ, endereçamento, decisao nos autos",
            "versao": _GATE_VERSAO})
        veredito_tribunal = "warn"
    else:
        veredito_tribunal = "pass"

    # --- regimento ---------------------------------------------------------
    regimento = _bloco(sources_map, _CAMPOS_REGIMENTO)
    caminho = regimento.get("path") or regimento.get("caminho")
    if not caminho and regimento.get("file"):
        # O mapa em markdown identifica o regimento pelo nome, não pelo caminho:
        # "Regimento Interno do TRF4, consolidação oficial até o Assento
        # Regimental nº 37/2026". A regra da casa manda considerar o regimento
        # vigente; o caminho é a forma de provar isso em JSON, não a regra.
        # Sem caminho não dá para reconferir a versão — e isso é P1 (`warn`),
        # não a ausência de regimento que o LRG4 acusa.
        achados.append({
            "gate": "LRG4b-regimento-sem-caminho", "sev": "P1",
            "problema": (f"o mapa declara o regimento em prosa ({str(regimento['file'])[:60]}) e "
                         "nao aponta o arquivo - a versao nao pode ser reconferida aqui"),
            "acao": ("salve a consolidacao vigente como REGIMENTO_INTERNO_<TRIBUNAL>.md na pasta "
                     "do caso e declare o caminho, mantendo a mencao em prosa"),
            "versao": _GATE_VERSAO})
        veredito_regimento = "warn"
    elif not caminho:
        achados.append({
            "gate": "LRG4-regimento-nao-declarado", "sev": "P0",
            "problema": ("a F3 nao declara o arquivo do regimento interno do tribunal - regra "
                         "inviolavel da casa desde 06/07/2026"),
            "acao": ("baixe a consolidacao oficial vigente, salve como "
                     "REGIMENTO_INTERNO_<TRIBUNAL>.md na pasta do caso e declare o caminho"),
            "versao": _GATE_VERSAO})
        veredito_regimento = "fail"
    else:
        alvo = Path(str(caminho))
        if not alvo.is_file():
            achados.append({
                "gate": "LRG5-regimento-inexistente", "sev": "P0",
                "problema": (f"o regimento declarado nao existe no disco: {str(caminho)[:120]}"),
                "acao": "restaure o arquivo do regimento ou corrija o caminho declarado",
                "versao": _GATE_VERSAO})
            veredito_regimento = "fail"
        else:
            texto = alvo.read_text(encoding="utf-8", errors="replace")
            declarado = regimento.get("sha256")
            real = hashlib.sha256(alvo.read_bytes()).hexdigest()
            veredito_regimento = "pass"
            if declarado and declarado.lower() != real.lower():
                # NÃO é P0. O protocolo manda atualizar este arquivo com as
                # emendas posteriores antes de cada peça — divergir é o esperado
                # quando o tempo passa entre a F3 e a peça seguinte.
                tem_emendas = "emendas posteriores" in texto.lower()
                achados.append({
                    "gate": "LRG6-regimento-mudou-desde-a-f3", "sev": "P1",
                    "problema": ("o regimento em disco nao tem mais o hash registrado na F3"
                                 + (" - o arquivo ja traz secao de emendas posteriores, o que "
                                    "sugere atualizacao conforme o protocolo"
                                    if tem_emendas else
                                    " e nao traz secao de emendas posteriores")),
                    "acao": ("confirme que a mudanca foi a anexacao de emendas e reregistre o "
                             "hash; a peca deve refletir o regimento vigente NA DATA DO PROTOCOLO"),
                    "versao": _GATE_VERSAO})
                veredito_regimento = "warn"
            if "emendas posteriores" not in texto.lower():
                achados.append({
                    "gate": "LRG7-sem-secao-de-emendas", "sev": "P1",
                    "problema": ("o arquivo do regimento nao tem a secao final de emendas "
                                 "posteriores exigida pelo protocolo"),
                    "acao": ("pesquise emendas e resolucoes posteriores a consolidacao e anexe-as "
                             "ao arquivo antes de redigir"),
                    "versao": _GATE_VERSAO})
                veredito_regimento = "warn" if veredito_regimento == "pass" else veredito_regimento

    # --- fatos críticos com lastro ------------------------------------------
    ledger = fact_ledger if isinstance(fact_ledger, dict) else {}
    fatos = [f for f in (ledger.get("facts") or ledger.get("fatos") or []) if isinstance(f, dict)]
    if not fatos:
        achados.append({
            "gate": "LRG8-ledger-sem-fatos", "sev": "P0",
            "problema": ("o ledger de fatos da F3 nao lista nenhum fato - o gate seria calculado "
                         "sobre conjunto vazio"),
            "acao": "registre os fatos do caso com o respectivo lastro documental",
            "versao": _GATE_VERSAO})
        veredito_fatos = "fail"
    else:
        orfaos = []
        for fato in fatos:
            status = str(fato.get("status") or fato.get("classification")
                         or fato.get("epistemicClass") or "").strip().lower()
            if status in _STATUS_SEM_LASTRO:
                continue
            if not any(fato.get(campo) for campo in _CAMPOS_LASTRO_FATO):
                orfaos.append(str(fato.get("id") or fato.get("factId") or "fato sem id")[:40])
        if orfaos:
            achados.append({
                "gate": "LRG9-fato-sem-lastro", "sev": "P0",
                "problema": (f"{len(orfaos)} de {len(fatos)} fatos nao declaram lastro nem se "
                             f"declaram bloqueados: {', '.join(orfaos[:_LIMITE_EXEMPLOS])}"),
                "acao": "ligue cada fato ao documento que o sustenta, ou marque-o como bloqueado",
                "versao": _GATE_VERSAO})
            veredito_fatos = "fail"
        else:
            veredito_fatos = "pass"

    return {"versao": _GATE_VERSAO, "findings": achados,
            "gates": {GATE_TRIBUNAL: veredito_tribunal,
                      GATE_REGIMENTO: veredito_regimento,
                      GATE_FATOS: veredito_fatos}}


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

    print(json.dumps(validar_regimento(_ler("sources_map.json"), _ler("fact_ledger.json")),
                     ensure_ascii=False, indent=2))
