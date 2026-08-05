# -*- coding: utf-8 -*-
"""forja_fontes_oficiais.py — gates computados `official_sources_archived` e
`quotes_compared` (F5).

Ambos eram escritos pelo agente da fase: nove execuções, nove `pass`, nenhuma
reprovação. A medição do acervo em 04/08/2026 mostrou por que isso importa —
um dos `source_ledger` reais tem DEZ fontes e NENHUMA arquivada, e mesmo assim
a fase reportou `official_sources_archived: pass`. O nome do gate era falso no
próprio artefato que ele deveria auditar.

Os seis dialetos de `source_ledger` medidos:

  CASO-23  5 fontes, 5 arquivadas, 5 hashes conferem
  VerifACT      5 fontes, 4 arquivadas com hash conferindo, 1 sem nada
  Nylton        5 fontes, 5 arquivadas, nenhuma com hash
  CASO-17       10 fontes, nenhuma arquivada
  CASO-04      9 fontes, nenhuma arquivada, 3 com hash sem caminho

O que o gate garante: que a fonte possa ser RECOTEJADA depois, de forma
idêntica. URL viva conferida numa data não permite isso — a página muda, o
link morre. Daí a escala de veredito:

  P0    caminho de arquivo declarado que não existe, ou hash declarado que não
        confere com o arquivo. É afirmação verificável sobre um arquivo, e ela
        é falsa — a forma mais pura de lastro aparente.
  P1    arquivamento parcial: a casa arquiva neste caso, e algumas fontes
        ficaram de fora.
  warn  nenhuma fonte arquivada, só verificação ao vivo. Não bloqueia — foi a
        prática corrente da casa por um mês, e travar a F5 na véspera do prazo
        seria pior que registrar o limite. Mas o gate deixa de dizer `pass`.

`quotes_compared` tem uma peculiaridade que é justamente a MC-15: quando a peça
não usa nenhuma citação textual, não há o que cotejar. Nove execuções
reportaram `pass`; o correto é `not_applicable`. "Nada examinado" e "examinado
e aprovado" precisam ser distinguíveis, senão o gate mede o conjunto vazio.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from forja_artefatos import nomes

_GATE_VERSAO = "FORJA-FONTES-OFICIAIS-v1"
GATE_ARQUIVO = "official_sources_archived"
GATE_COTEJO = "quotes_compared"

# Vocabulário vindo de `forja_artefatos.DIALETOS`, a fonte única medida no acervo.
# Até 04/08/2026 cada gate mantinha a sua própria cópia — quatorze mapas em cinco
# módulos —, e um caso novo que inventasse um nome deixava cada um deles lendo o
# vazio em silêncio, cada um numa data diferente. Derivar daqui não muda veredito
# nenhum (conferido antes da migração) e faz a catraca de vocabulário valer para
# todos de uma vez.
_CAMPOS_CAMINHO = nomes("source_ledger", "caminho_arquivado")
_CAMPOS_HASH = nomes("source_ledger", "hash_arquivado")
_CAMPOS_URL = nomes("source_ledger", "url_oficial")
_CAMPOS_AUTORIDADE = nomes("source_ledger", "autoridade")

_LIMITE_EXEMPLOS = 4


def _fontes(ledger: dict) -> list:
    for campo in ("sources", "entries", "fontes", "officialSources"):
        valor = ledger.get(campo)
        if isinstance(valor, list) and valor:
            return [f for f in valor if isinstance(f, dict)]
    return []


def _rotulo(fonte: dict) -> str:
    for campo in ("sourceId", "id", "identifier", "title", "claim"):
        valor = fonte.get(campo)
        if valor:
            return str(valor)[:60]
    return "fonte sem identificador"


def _primeiro(fonte: dict, campos) -> str | None:
    for campo in campos:
        valor = fonte.get(campo)
        if isinstance(valor, str) and valor.strip():
            return valor.strip()
    return None


def _resolver(caminho: str, base_dir) -> Path:
    alvo = Path(caminho)
    if not alvo.is_absolute() and base_dir:
        alvo = Path(base_dir) / alvo
    return alvo


def validar_fontes_arquivadas(ledger, base_dir=None):
    """Achados e veredito do gate `official_sources_archived`."""
    if not isinstance(ledger, dict) or not ledger:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LFA1-ledger-ausente", "sev": "P0",
                              "problema": ("source_ledger ausente ou vazio - a fase de pesquisa "
                                           "oficial nao registrou nenhuma fonte"),
                              "acao": "a F5 deve emitir source_ledger com as fontes conferidas",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_ARQUIVO: "fail"}}

    achados = []
    fontes = _fontes(ledger)
    if not fontes:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LFA1-sem-fontes", "sev": "P0",
                              "problema": ("source_ledger nao lista nenhuma fonte - o gate seria "
                                           "calculado sobre conjunto vazio"),
                              "acao": "registre as fontes oficiais conferidas",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_ARQUIVO: "fail"}}

    sem_identidade = [f for f in fontes
                      if not _primeiro(f, _CAMPOS_URL) and not _primeiro(f, _CAMPOS_AUTORIDADE)]
    if sem_identidade:
        achados.append({
            "gate": "LFA2-fonte-sem-origem-oficial", "sev": "P0",
            "problema": (f"{len(sem_identidade)} fonte(s) sem URL oficial nem autoridade: "
                         f"{', '.join(_rotulo(f) for f in sem_identidade[:_LIMITE_EXEMPLOS])}"),
            "acao": "declare a autoridade e o endereco oficial de cada fonte",
            "versao": _GATE_VERSAO})

    arquivadas, quebradas, sem_hash = [], [], []
    for fonte in fontes:
        caminho = _primeiro(fonte, _CAMPOS_CAMINHO)
        digest = _primeiro(fonte, _CAMPOS_HASH)
        if not caminho:
            continue
        arquivadas.append(fonte)
        alvo = _resolver(caminho, base_dir)
        if not alvo.is_file():
            quebradas.append((fonte, "o arquivo declarado nao existe"))
            continue
        if not digest:
            sem_hash.append(fonte)
            continue
        try:
            real = hashlib.sha256(alvo.read_bytes()).hexdigest()
        except OSError:
            quebradas.append((fonte, "o arquivo declarado nao pode ser lido"))
            continue
        if real.lower() != digest.lower():
            quebradas.append((fonte, "o hash declarado nao confere com o arquivo"))

    if quebradas:
        detalhe = "; ".join(f"{_rotulo(f)}: {motivo}" for f, motivo in quebradas[:_LIMITE_EXEMPLOS])
        achados.append({
            "gate": "LFA3-arquivo-declarado-invalido", "sev": "P0",
            "problema": (f"{len(quebradas)} fonte(s) afirmam copia arquivada que nao se sustenta - "
                         f"{detalhe}"),
            "acao": "rearquive a fonte e regrave o hash, ou remova a afirmacao de arquivamento",
            "versao": _GATE_VERSAO})

    if sem_hash:
        achados.append({
            "gate": "LFA4-arquivo-sem-hash", "sev": "P2",
            "problema": (f"{len(sem_hash)} fonte(s) arquivadas sem hash - a copia existe mas nao "
                         "ha ancora de integridade para detectar troca posterior"),
            "acao": "grave o sha256 da copia arquivada",
            "versao": _GATE_VERSAO})

    if not arquivadas:
        achados.append({
            "gate": "LFA5-nenhuma-fonte-arquivada", "sev": "P1",
            "problema": (f"nenhuma das {len(fontes)} fontes tem copia arquivada - a conferencia foi "
                         "ao vivo e nao podera ser refeita de forma identica"),
            "acao": ("arquive a fonte em cache/fontes_oficiais com data de conferencia, "
                     "conforme o protocolo da casa"),
            "versao": _GATE_VERSAO})
    elif len(arquivadas) < len(fontes):
        faltam = len(fontes) - len(arquivadas)
        achados.append({
            "gate": "LFA6-arquivamento-parcial", "sev": "P1",
            "problema": (f"{faltam} de {len(fontes)} fontes ficaram sem copia arquivada num caso "
                         "que arquiva as demais"),
            "acao": "arquive tambem as fontes restantes",
            "versao": _GATE_VERSAO})

    if any(a["sev"] == "P0" for a in achados):
        veredito = "fail"
    elif any(a["sev"] == "P1" for a in achados):
        veredito = "warn"
    else:
        veredito = "pass"
    return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_ARQUIVO: veredito}}


def _itens_checklist(checklist: dict) -> list:
    for campo in ("items", "citations", "entries", "itens"):
        valor = checklist.get(campo)
        if isinstance(valor, list) and valor:
            return [i for i in valor if isinstance(i, dict)]
    return []


def _usou_citacao_textual(item: dict) -> bool:
    for campo in ("quoteUsed", "citacaoTextual", "verbatim", "hasQuote"):
        if item.get(campo) is True:
            return True
    for campo in ("quote", "citacao", "excerpt", "trecho"):
        valor = item.get(campo)
        if isinstance(valor, str) and valor.strip():
            return True
    return False


def _cotejo_registrado(item: dict) -> bool:
    for campo in ("comparedTo", "quoteComparedTo", "cotejo", "sourceExcerptSha256",
                  "excerptHash", "locator", "pincite"):
        valor = item.get(campo)
        if isinstance(valor, str) and valor.strip():
            return True
    for campo in ("quoteCompared", "compared", "cotejado"):
        if item.get(campo) is True:
            return True
    return False


# Sete dos nove `citation_checklist` do acervo são MARKDOWN, e o gate só lia os
# dois JSON — por isso `quotes_compared` respondeu `not_applicable` nas duas
# tentativas que alcançava e nunca produziu veredito sobre as outras sete. A
# forma markdown é uma lista de caixas marcadas, não uma tabela de citações; o
# que dá para aferir nela é honesto e limitado, e o gate diz qual é o limite em
# vez de fingir precisão que o artefato não tem.
_CAIXA_ABERTA = re.compile(r"(?m)^\s*[-*]\s*\[\s\]\s+(.{10,})")
_CAIXA_MARCADA = re.compile(r"(?m)^\s*[-*]\s*\[[xX]\]\s+(.{10,})")
_NEGA_TRANSCRICAO = re.compile(
    r"(?i)(?:n[ãa]o\s+haver[áa]|sem|nenhuma)\s+transcri[çc][ãa]o\s+literal|"
    r"par[áa]frases?\s+fi[ée]is|sem\s+cita[çc][ãa]o\s+textual")
_AFIRMA_TRANSCRICAO = re.compile(
    r"(?i)transcri[çc][ãa]o\s+literal\s+(?:conferida|cotejada|comparada)|"
    r"cita[çc][ãa]o\s+textual\s+(?:conferida|cotejada|comparada)|verbatim\s+conferid")


def _cotejo_em_texto(texto: str) -> dict:
    marcadas = _CAIXA_MARCADA.findall(texto)
    abertas = _CAIXA_ABERTA.findall(texto)
    if not marcadas and not abertas:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LQC5-checklist-sem-item-conferivel", "sev": "P1",
                              "problema": ("o checklist em markdown nao traz item marcavel - nao ha "
                                           "como distinguir o que foi conferido do que falta"),
                              "acao": "liste as conferencias como caixas, uma por citacao",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_COTEJO: "warn"}}
    if abertas:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LQC6-conferencia-pendente", "sev": "P0",
                              "problema": (f"{len(abertas)} item(ns) do checklist continuam sem "
                                           f"conferir: {abertas[0][:90]}"),
                              "acao": "conclua a conferencia ou registre por que ela nao se aplica",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_COTEJO: "fail"}}
    if _NEGA_TRANSCRICAO.search(texto):
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LQC2-sem-citacao-textual", "sev": "INFO",
                              "problema": ("o checklist declara por escrito que a peca usa parafrase "
                                           "e nao transcricao literal - nao ha cotejo a fazer"),
                              "acao": "nenhuma; o gate nao se aplica a este caso",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_COTEJO: "not_applicable"}}
    if _AFIRMA_TRANSCRICAO.search(texto):
        return {"versao": _GATE_VERSAO, "findings": [], "gates": {GATE_COTEJO: "pass"}}
    return {"versao": _GATE_VERSAO,
            "findings": [{"gate": "LQC7-uso-textual-nao-declarado", "sev": "P2",
                          "problema": (f"os {len(marcadas)} itens do checklist estao conferidos e o "
                                       "artefato nao diz se houve transcricao literal - o cotejo "
                                       "nao pode ser afirmado nem descartado"),
                          "acao": ("declare, em uma linha, se a peca transcreve literalmente e se a "
                                   "transcricao foi cotejada com a fonte"),
                          "versao": _GATE_VERSAO}],
            "gates": {GATE_COTEJO: "warn"}}


def validar_cotejo_citacoes(checklist, ledger=None):
    """Achados e veredito do gate `quotes_compared`.

    Devolve `not_applicable` quando nenhuma citação textual foi usada: nesse
    caso não há cotejo a fazer, e dizer `pass` seria medir o conjunto vazio.
    """
    if isinstance(checklist, str):
        return _cotejo_em_texto(checklist)
    if not isinstance(checklist, dict) or not checklist:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LQC1-checklist-ausente", "sev": "P0",
                              "problema": ("citation_checklist ausente ou vazio - nao ha registro "
                                           "de conferencia de citacao"),
                              "acao": "a F5 deve emitir citation_checklist",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_COTEJO: "fail"}}

    achados = []
    itens = _itens_checklist(checklist)
    if not itens:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LQC1-checklist-sem-itens", "sev": "P0",
                              "problema": ("citation_checklist nao lista nenhuma citacao - o gate "
                                           "seria calculado sobre conjunto vazio"),
                              "acao": "liste as citacoes usadas e o resultado da conferencia",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_COTEJO: "fail"}}

    com_citacao = [i for i in itens if _usou_citacao_textual(i)]
    if not com_citacao:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LQC2-sem-citacao-textual", "sev": "INFO",
                              "problema": (f"nenhuma das {len(itens)} citacoes usa transcricao "
                                           "textual - nao ha cotejo a fazer"),
                              "acao": "nenhuma; o gate nao se aplica a este caso",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_COTEJO: "not_applicable"}}

    sem_cotejo = [i for i in com_citacao if not _cotejo_registrado(i)]
    if sem_cotejo:
        rotulos = [str(i.get("citation") or i.get("citacao") or "citacao sem rotulo")[:50]
                   for i in sem_cotejo[:_LIMITE_EXEMPLOS]]
        achados.append({
            "gate": "LQC3-citacao-textual-sem-cotejo", "sev": "P0",
            "problema": (f"{len(sem_cotejo)} de {len(com_citacao)} citacoes textuais nao registram "
                         f"cotejo contra a fonte: {', '.join(rotulos)}"),
            "acao": ("registre o localizador e o trecho conferido na fonte oficial para cada "
                     "transcricao"),
            "versao": _GATE_VERSAO})

    declarado = isinstance(ledger, dict) and ledger.get("quotesCompared") is True
    if declarado and sem_cotejo:
        achados.append({
            "gate": "LQC4-atestado-sem-lastro", "sev": "P1",
            "problema": ("o ledger declara quotesCompared=true enquanto ha citacao textual sem "
                         "registro de cotejo - a afirmacao nao se sustenta no proprio artefato"),
            "acao": "registre o cotejo por citacao em vez de um booleano global",
            "versao": _GATE_VERSAO})

    if any(a["sev"] == "P0" for a in achados):
        veredito = "fail"
    elif achados:
        veredito = "warn"
    else:
        veredito = "pass"
    return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_COTEJO: veredito}}


def validar_pesquisa_oficial(ledger, checklist, base_dir=None):
    """Junta os dois gates da F5 num laudo só."""
    arquivo = validar_fontes_arquivadas(ledger, base_dir)
    cotejo = validar_cotejo_citacoes(checklist, ledger if isinstance(ledger, dict) else None)
    return {"versao": _GATE_VERSAO,
            "findings": arquivo["findings"] + cotejo["findings"],
            "gates": {**arquivo["gates"], **cotejo["gates"]}}


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

    print(json.dumps(validar_pesquisa_oficial(_ler("source_ledger.json"),
                                              _ler("citation_checklist.json"), pasta),
                     ensure_ascii=False, indent=2))
