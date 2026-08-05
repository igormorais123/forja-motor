# -*- coding: utf-8 -*-
"""forja_ingestao.py — gates computados `critical_documents_indexed` e
`coverage_declared` (F1).

São os dois gates mais a montante da esteira, e um `pass` falso neles é peça
redigida sobre leitura parcial dos autos sem que ninguém saiba. Nove execuções,
nove `pass`, nenhuma reprovação até 04/08/2026.

Medição do acervo antes de qualquer limiar — e ela derrubou duas regras que
pareciam óbvias:

  1. "o índice tem que listar documentos" — um dos seis índices reais tem
     `documents: []` e registra o acervo em `keyDocuments` no topo, com 200
     arquivos e 3.035 páginas validadas. Exigir a lista teria reprovado o caso
     mais bem documentado do acervo.
  2. "confira o hash de cada documento" — só DOIS dos seis índices têm caminhos
     que resolvem a partir daqui; os demais são relativos à pasta do cliente.
     Caminho que não resolve é impossibilidade de conferir, não reprovação.

  3. "cobertura completa com lacuna aberta é contradição" — os cinco ledgers
     reais declaram completude QUALIFICADA (`complete_for_f2a_internal_working`,
     "integral sobre o acervo disponível; lacunas externas explicitadas") e
     listam as lacunas ao lado. Isso é honestidade, não contradição. O que o
     gate persegue é a completude NUA declarada sobre lacuna conhecida.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from forja_artefatos import nomes

_GATE_VERSAO = "FORJA-INGESTAO-v1"
GATE_INDICE = "critical_documents_indexed"
GATE_COBERTURA = "coverage_declared"

# Vocabulário vindo de `forja_artefatos.DIALETOS`, a fonte única medida no acervo.
# Até 04/08/2026 cada gate mantinha a sua própria cópia — quatorze mapas em cinco
# módulos —, e um caso novo que inventasse um nome deixava cada um deles lendo o
# vazio em silêncio, cada um numa data diferente. Derivar daqui não muda veredito
# nenhum (conferido antes da migração) e faz a catraca de vocabulário valer para
# todos de uma vez.
_CAMPOS_CRITICOS_TOPO = nomes("document_index", "criticos_no_topo")
_CAMPOS_LACUNA = nomes("coverage_ledger", "lacunas")
_CAMPOS_COBERTURA = nomes("coverage_ledger", "declaracao")
# Completude NUA: a palavra sozinha, sem o "para quê" ao lado.
_COMPLETUDE_NUA = re.compile(r"^(complete|completa|integral|total|full)$", re.I)

_LIMITE_EXEMPLOS = 4


def _lista(valor) -> list:
    if isinstance(valor, list):
        return valor
    if isinstance(valor, dict):
        return list(valor.values())
    return []


def _tem_conteudo(valor) -> bool:
    if isinstance(valor, str):
        return bool(valor.strip())
    if isinstance(valor, (list, dict)):
        return len(valor) > 0
    return valor is not None and valor is not False


def validar_indice_documentos(indice, base_dir=None):
    """Achados e veredito do gate `critical_documents_indexed`."""
    if not isinstance(indice, dict) or not indice:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LDI1-indice-ausente", "sev": "P0",
                              "problema": ("document_index ausente ou vazio - os autos foram "
                                           "ingeridos sem indice"),
                              "acao": "a F1 deve emitir document_index com o acervo recebido",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_INDICE: "fail"}}

    achados = []
    documentos = [d for d in _lista(indice.get("documents") or indice.get("documentos"))
                  if isinstance(d, dict)]
    criticos_topo = {campo: indice[campo] for campo in _CAMPOS_CRITICOS_TOPO
                     if _tem_conteudo(indice.get(campo))}
    totais = indice.get("totals") or indice.get("aggregateValidation") or {}

    if not documentos and not criticos_topo and not totais:
        achados.append({
            "gate": "LDI2-indice-sem-acervo", "sev": "P0",
            "problema": ("o indice nao lista documento, ato critico nem totais do acervo - "
                         "o gate seria calculado sobre conjunto vazio"),
            "acao": "registre o acervo recebido e os atos criticos localizados",
            "versao": _GATE_VERSAO})
        return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_INDICE: "fail"}}

    # Documento crítico identificado — no item ou no topo. Um acervo processual
    # sem nenhum ato crítico apontado não é impossível, mas é improvável o
    # bastante para merecer aviso: sem isso, "documentos críticos indexados"
    # aprova um índice que não distinguiu nada.
    criticos_item = [d for d in documentos
                     if d.get("critical") is True or _tem_conteudo(d.get("criticalAct"))]
    if not criticos_item and not criticos_topo:
        achados.append({
            "gate": "LDI3-nenhum-ato-critico-apontado", "sev": "P1",
            "problema": (f"o indice registra {len(documentos)} documento(s) e nao aponta nenhum "
                         "como critico - o gate aprovaria sem ter distinguido nada"),
            "acao": "marque os atos decisivos (decisao impugnada, laudo, intimacao) no indice",
            "versao": _GATE_VERSAO})

    # Hash declarado que não confere é afirmação verificável e falsa.
    conferidos, divergentes, nao_resolvidos = 0, [], 0
    for documento in documentos:
        digest = documento.get("sha256") or documento.get("hash")
        caminho = documento.get("path") or documento.get("file") or documento.get("name")
        if not digest or not caminho:
            continue
        alvo = Path(str(caminho))
        if not alvo.is_absolute() and base_dir:
            alvo = Path(base_dir) / alvo
        if not alvo.is_file():
            nao_resolvidos += 1
            continue
        try:
            real = hashlib.sha256(alvo.read_bytes()).hexdigest()
        except OSError:
            nao_resolvidos += 1
            continue
        conferidos += 1
        if real.lower() != str(digest).lower():
            divergentes.append(str(documento.get("id") or caminho)[:60])

    if divergentes:
        achados.append({
            "gate": "LDI4-hash-divergente", "sev": "P0",
            "problema": (f"{len(divergentes)} documento(s) do indice tem hash que nao confere com "
                         f"o arquivo: {', '.join(divergentes[:_LIMITE_EXEMPLOS])}"),
            "acao": "reindexe o acervo; o arquivo mudou depois de indexado ou o hash esta errado",
            "versao": _GATE_VERSAO})

    if not conferidos and nao_resolvidos:
        achados.append({
            "gate": "LDI5-hash-nao-conferivel", "sev": "P2",
            "problema": (f"nenhum dos {nao_resolvidos} caminhos declarados resolve a partir desta "
                         "execucao - a integridade do indice nao pode ser reconferida aqui"),
            "acao": "registre caminhos relativos a pasta do caso para permitir a reconferencia",
            "versao": _GATE_VERSAO})

    if any(a["sev"] == "P0" for a in achados):
        veredito = "fail"
    elif any(a["sev"] == "P1" for a in achados):
        veredito = "warn"
    else:
        veredito = "pass"
    return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_INDICE: veredito}}


def validar_cobertura(ledger):
    """Achados e veredito do gate `coverage_declared`."""
    if not isinstance(ledger, dict) or not ledger:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LCD1-ledger-ausente", "sev": "P0",
                              "problema": ("coverage_ledger ausente ou vazio - nao ha declaracao "
                                           "de quanto dos autos foi lido"),
                              "acao": "a F1 deve declarar a cobertura da leitura e as lacunas",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_COBERTURA: "fail"}}

    achados = []
    declaracoes = {campo: ledger[campo] for campo in _CAMPOS_COBERTURA
                   if _tem_conteudo(ledger.get(campo))}
    if not declaracoes:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LCD2-sem-declaracao", "sev": "P0",
                              "problema": ("o ledger existe e nao declara cobertura alguma - "
                                           "nenhum campo diz quanto do acervo foi lido"),
                              "acao": "declare o escopo coberto e o metodo de leitura",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_COBERTURA: "fail"}}

    # Aritmética que o próprio ledger permite conferir.
    recebidos = ledger.get("sourcePdfsReceived")
    validados = ledger.get("sourcePdfsValidated")
    if isinstance(recebidos, int) and isinstance(validados, int):
        if validados > recebidos:
            achados.append({
                "gate": "LCD3-aritmetica-impossivel", "sev": "P0",
                "problema": (f"o ledger declara {validados} documento(s) validado(s) sobre "
                             f"{recebidos} recebido(s)"),
                "acao": "corrija a contagem da ingestao",
                "versao": _GATE_VERSAO})
        elif validados < recebidos:
            achados.append({
                "gate": "LCD4-validacao-parcial", "sev": "P1",
                "problema": (f"{recebidos - validados} de {recebidos} documento(s) recebidos nao "
                             "foram validados, e a cobertura nao qualifica essa falta"),
                "acao": "valide os documentos restantes ou registre a falta como lacuna",
                "versao": _GATE_VERSAO})

    # Completude NUA sobre lacuna conhecida. Os cinco ledgers reais qualificam a
    # completude ("complete_for_f2a_internal_working", "integral sobre o acervo
    # disponível") e listam as lacunas ao lado — isso é honestidade. O defeito é
    # dizer "completo" seco tendo lacuna registrada no próprio artefato.
    lacunas = [campo for campo in _CAMPOS_LACUNA if _tem_conteudo(ledger.get(campo))]
    status = str(ledger.get("coverageStatus") or ledger.get("status") or "").strip()
    if lacunas and _COMPLETUDE_NUA.match(status):
        achados.append({
            "gate": "LCD5-completude-nua-sobre-lacuna", "sev": "P1",
            "problema": (f"a cobertura se declara '{status}' enquanto o proprio ledger registra "
                         f"lacuna em {', '.join(lacunas)}"),
            "acao": ("qualifique a completude - completo PARA QUE, e com que lacuna conhecida - "
                     "como fazem os demais casos do acervo"),
            "versao": _GATE_VERSAO})

    if any(a["sev"] == "P0" for a in achados):
        veredito = "fail"
    elif any(a["sev"] == "P1" for a in achados):
        veredito = "warn"
    else:
        veredito = "pass"
    return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE_COBERTURA: veredito}}


def validar_ingestao(indice, ledger, base_dir=None):
    """Junta os dois gates da F1 num laudo só."""
    a = validar_indice_documentos(indice, base_dir)
    b = validar_cobertura(ledger)
    return {"versao": _GATE_VERSAO,
            "findings": a["findings"] + b["findings"],
            "gates": {**a["gates"], **b["gates"]}}


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

    print(json.dumps(validar_ingestao(_ler("document_index.json"),
                                      _ler("coverage_ledger.json"), pasta),
                     ensure_ascii=False, indent=2))
