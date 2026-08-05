# -*- coding: utf-8 -*-
"""forja_paragrafos.py — gate computado `paragraphs_sourced` (F6).

Até 04/08/2026 este gate era escrito pelo agente da F6: oito execuções, oito
`pass`, nenhuma reprovação. Ele responde à pergunta que decide se a peça é
protocolável — cada parágrafo afirma algo que os autos sustentam? — e um `pass`
falso é exatamente o modo de falha do incidente Vale Trading de 26/07: texto
bem escrito, lastro aparente, proposição sem âncora.

O artefato `paragraph_provenance.json` existe no acervo em CINCO dialetos,
porque cada caso inventou o seu vocabulário (`provenance` em texto corrido;
`sources`+`propositions` por faixa; `supports`; `supportIds`; `factIds`+
`propositionIds`+`sourceIds` por bloco). Como nas levas anteriores, o gate é
tolerante à forma e estrito na substância.

O que ele verifica:

  LPS1 — houve declaração? artefato ausente, vazio ou sem unidades é P0.
         Um gate calculado sobre conjunto vazio devolve `pass` sem examinar
         nada — foi a MC-15, e ela reincidiu quatro vezes num único dia.
  LPS2 — toda unidade carrega lastro, ou está declarada editorial. Medido no
         acervo: das 316 unidades reais, 23 não têm lastro e as 23 são
         cabeçalhos marcados `claimClass: editorial`. A isenção é legítima e
         precisa ser EXPLÍCITA — silêncio não isenta.
  LPS3 — a proveniência descreve ESTE rascunho. Onde o artefato declara hash
         do markdown, ele é conferido; onde declara `textPrefix`/`sample`, o
         trecho é procurado no texto. Proveniência que descreve um rascunho
         anterior é pior que proveniência ausente, porque parece conferida.
  LPS4 — cobertura, só quando computável no vocabulário do próprio artefato.
         Onde não for, o gate diz `warn` e declara o limite; não inventa
         número para parecer rigoroso.

Calibração que evitou um falso positivo: o hash do caso VerifACT (V8) diverge
do arquivo em disco por CRLF × LF, não por conteúdo. Conferir hash sem
normalizar fim de linha reprovaria uma peça correta — por isso as duas formas
são aceitas.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from forja_artefatos import nomes

_GATE_VERSAO = "FORJA-PARAGRAFOS-v1"
GATE = "paragraphs_sourced"

# Campos que, em algum dos cinco dialetos, carregam o lastro de uma unidade.
# Vocabulário vindo de `forja_artefatos.DIALETOS`, a fonte única medida no acervo.
# Até 04/08/2026 cada gate mantinha a sua própria cópia — quatorze mapas em cinco
# módulos —, e um caso novo que inventasse um nome deixava cada um deles lendo o
# vazio em silêncio, cada um numa data diferente. Derivar daqui não muda veredito
# nenhum (conferido antes da migração) e faz a catraca de vocabulário valer para
# todos de uma vez.
_CAMPOS_LASTRO = nomes("paragraph_provenance", "lastro")
# Campos que declaram, explicitamente, que a unidade não afirma fato.
_CAMPOS_EDITORIAIS = ("editorialOnly", "editorial")
_CLASSES_EDITORIAIS = {"editorial", "heading", "titulo", "título", "formatting"}
_CAMPOS_AMOSTRA = nomes("paragraph_provenance", "amostra_do_texto")
_CAMPOS_HASH = nomes("paragraph_provenance", "hash_do_texto")

_LIMITE_EXEMPLOS = 5


def _norm(texto: str) -> str:
    return re.sub(r"\s+", " ", texto or "").strip()


def _unidades(prov: dict) -> list:
    for campo in ("paragraphs", "blocks", "paragrafos", "unidades"):
        valor = prov.get(campo)
        if isinstance(valor, list) and valor:
            return [u for u in valor if isinstance(u, dict)]
    return []


def _tem_lastro(unidade: dict) -> bool:
    for campo in _CAMPOS_LASTRO:
        valor = unidade.get(campo)
        if isinstance(valor, str) and valor.strip():
            return True
        if isinstance(valor, list) and valor:
            return True
    return False


def _e_editorial(unidade: dict) -> bool:
    for campo in _CAMPOS_EDITORIAIS:
        if unidade.get(campo) is True:
            return True
    for campo in ("claimClass", "kind", "tipo", "classe"):
        if str(unidade.get(campo) or "").strip().lower() in _CLASSES_EDITORIAIS:
            return True
    return False


def _rotulo(unidade: dict) -> str:
    for campo in ("blockId", "paragraphId", "id", "range"):
        valor = unidade.get(campo)
        if valor:
            return str(valor)
    valor = unidade.get("paragraphs")
    if isinstance(valor, list) and valor:
        return str(valor[0])
    return "unidade sem identificador"


def _hashes_do_texto(texto: str) -> set:
    """Aceita as duas convenções de fim de linha; a diferença não é conteúdo."""
    variantes = {texto, texto.replace("\r\n", "\n"),
                 texto.replace("\r\n", "\n").replace("\n", "\r\n")}
    return {hashlib.sha256(v.encode("utf-8")).hexdigest() for v in variantes}


def validar_paragrafos_lastreados(prov, draft_texto=None):
    """Achados e veredito do gate `paragraphs_sourced`."""
    if not isinstance(prov, dict) or not prov:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LPS1-proveniencia-ausente", "sev": "P0",
                              "problema": ("artefato paragraph_provenance ausente ou vazio - "
                                           "nao ha declaracao de lastro por paragrafo"),
                              "acao": "a F6 deve emitir paragraph_provenance com uma unidade por bloco",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE: "fail"}}

    achados = []
    unidades = _unidades(prov)
    if not unidades:
        achados.append({
            "gate": "LPS1-sem-unidades", "sev": "P0",
            "problema": ("paragraph_provenance nao declara nenhuma unidade de texto - "
                         "o gate seria calculado sobre conjunto vazio"),
            "acao": "declare as unidades do rascunho com seu lastro",
            "versao": _GATE_VERSAO})
        return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE: "fail"}}

    # LPS2 — lastro ou isencao explicita.
    orfas = [u for u in unidades if not _tem_lastro(u) and not _e_editorial(u)]
    if orfas:
        exemplos = ", ".join(_rotulo(u) for u in orfas[:_LIMITE_EXEMPLOS])
        achados.append({
            "gate": "LPS2-paragrafo-sem-lastro", "sev": "P0",
            "problema": (f"{len(orfas)} de {len(unidades)} unidades nao declaram lastro nem "
                         f"se declaram editoriais: {exemplos}"),
            "acao": ("ligue cada unidade a fato, proposicao ou fonte, ou marque-a como "
                     "editorial quando nao afirmar fato"),
            "versao": _GATE_VERSAO})

    # LPS3 — a proveniencia descreve ESTE rascunho.
    cobertura_computavel = False
    if draft_texto:
        declarado = next((prov[c] for c in _CAMPOS_HASH if isinstance(prov.get(c), str)), None)
        if declarado:
            if declarado.strip().lower() not in _hashes_do_texto(draft_texto):
                achados.append({
                    "gate": "LPS3-proveniencia-de-outro-rascunho", "sev": "P0",
                    "problema": ("o hash do markdown declarado na proveniencia nao corresponde ao "
                                 "rascunho - o texto foi reescrito depois de registrado o lastro"),
                    "acao": "regenere paragraph_provenance sobre a versao atual do rascunho",
                    "versao": _GATE_VERSAO})

        normalizado = _norm(draft_texto)
        amostras = []
        for unidade in unidades:
            for campo in _CAMPOS_AMOSTRA:
                valor = unidade.get(campo)
                if isinstance(valor, str) and valor.strip():
                    amostras.append((_rotulo(unidade), valor))
                    break
        ausentes = [(rot, a) for rot, a in amostras if _norm(a) not in normalizado]
        if ausentes:
            achados.append({
                "gate": "LPS3-trecho-nao-encontrado", "sev": "P0",
                "problema": (f"{len(ausentes)} de {len(amostras)} trechos citados na proveniencia "
                             f"nao ocorrem no rascunho: "
                             f"{', '.join(r for r, _ in ausentes[:_LIMITE_EXEMPLOS])}"),
                "acao": "regenere a proveniencia sobre o rascunho atual",
                "versao": _GATE_VERSAO})
        if amostras:
            cobertura_computavel = True

        # LPS4 — cobertura por linha, quando o dialeto numera linhas.
        fins = [u.get("endLine") for u in unidades if isinstance(u.get("endLine"), int)]
        if fins:
            cobertura_computavel = True
            linhas = len(draft_texto.splitlines())
            if linhas and max(fins) < linhas * 0.6:
                achados.append({
                    "gate": "LPS4-cobertura-parcial", "sev": "P1",
                    "problema": (f"a proveniencia descreve ate a linha {max(fins)} de {linhas} - "
                                 "a parte final do rascunho nao foi lastreada"),
                    "acao": "estenda a proveniencia ate o fim do rascunho",
                    "versao": _GATE_VERSAO})

    if not cobertura_computavel:
        achados.append({
            "gate": "LPS4-cobertura-nao-computavel", "sev": "P2",
            "problema": ("o dialeto deste paragraph_provenance nao permite conferir cobertura "
                         "contra o rascunho: nao ha hash, trecho citado nem numeracao de linha"),
            "acao": ("declare markdownSha256 ou textPrefix por unidade para que a cobertura "
                     "deixe de ser autodeclarada"),
            "versao": _GATE_VERSAO})

    reprovado = any(a["sev"] == "P0" for a in achados)
    incerto = any(a["gate"].startswith("LPS4-cobertura-nao-computavel") for a in achados)
    veredito = "fail" if reprovado else ("warn" if incerto else "pass")
    return {"versao": _GATE_VERSAO, "findings": achados, "gates": {GATE: veredito}}


def carregar_e_validar(pasta):
    """Lê paragraph_provenance.json e draft_markdown.md de uma pasta de tentativa."""
    pasta = Path(pasta)
    arquivo = pasta / "paragraph_provenance.json"
    prov = None
    if arquivo.is_file():
        try:
            prov = json.loads(arquivo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            prov = None
    if isinstance(prov, dict) and "main" in prov and isinstance(prov["main"], dict):
        prov = prov["main"]

    texto = None
    nome = (prov or {}).get("markdownPath") or "draft_markdown.md"
    caminho = pasta / str(nome)
    if caminho.is_file():
        texto = caminho.read_text(encoding="utf-8")
    return validar_paragrafos_lastreados(prov, texto)


if __name__ == "__main__":  # pragma: no cover
    import sys
    alvo = sys.argv[1] if len(sys.argv) > 1 else "."
    print(json.dumps(carregar_e_validar(alvo), ensure_ascii=False, indent=2))
