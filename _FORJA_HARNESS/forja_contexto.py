# -*- coding: utf-8 -*-
"""forja_contexto.py — gates computados `facts_rechecked` e `context_complete` (F7).

Os dois eram booleanos escritos pelo agente da fase — `factsRechecked: true`
num JSON, e nada mais. Não há como recomputar de fora se cada fato foi de novo
conferido na fonte: isso é trabalho de leitura humana e do próprio F7. O que se
pode computar, e é onde mora o risco real, são as **contradições internas** do
artefato e a sua **aderência ao texto auditado**.

Medição dos seis `context_validation` reais em 04/08/2026:

  factsRechecked   quatro `true`, um `false` (CASO-04, honesto), dois ausentes
                   porque o caso usa o dialeto do `f7_gate_result`
  pendências       três casos têm questão material pendente — e nos TRÊS o
                   release externo está negado. Ninguém do acervo declarou
                   liberação externa sobre contexto aberto, e é exatamente essa
                   combinação que o gate passa a impedir
  hashes           dez conferências de hash do markdown auditado, dez batem

O gate não decide mérito, e isso é deliberado. Ele impede que o artefato
afirme uma coisa e registre a oposta no campo ao lado — o modo de falha que
nenhum revisor apressado pega e que nenhum agente reporta contra si mesmo.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from forja_artefatos import nomes

_GATE_VERSAO = "FORJA-CONTEXTO-v1"
GATE_FATOS = "facts_rechecked"
GATE_CONTEXTO = "context_complete"

# Vocabulário vindo de `forja_artefatos.DIALETOS`, a fonte única medida no acervo.
# Até 04/08/2026 cada gate mantinha a sua própria cópia — quatorze mapas em cinco
# módulos —, e um caso novo que inventasse um nome deixava cada um deles lendo o
# vazio em silêncio, cada um numa data diferente. Derivar daqui não muda veredito
# nenhum (conferido antes da migração) e faz a catraca de vocabulário valer para
# todos de uma vez.
_CAMPOS_PENDENCIA = nomes("context_validation", "pendencias")
_CAMPOS_HASH_TEXTO = ("auditedMarkdownSha256", "auditedSha256", "finalMarkdownSha256")
_CAMPOS_IDENTIDADE = nomes("context_validation", "identidade")


def _hashes_do_texto(texto: str) -> set:
    variantes = {texto, texto.replace("\r\n", "\n"),
                 texto.replace("\r\n", "\n").replace("\n", "\r\n")}
    return {hashlib.sha256(v.encode("utf-8")).hexdigest() for v in variantes}


def _declarado_bool(*fontes, chaves):
    """Procura um booleano em qualquer um dos dialetos, incluindo `checks.X: pass`."""
    for fonte in fontes:
        if not isinstance(fonte, dict):
            continue
        for chave in chaves:
            if chave in fonte:
                valor = fonte[chave]
                if isinstance(valor, bool):
                    return valor
                if isinstance(valor, str):
                    return valor.strip().lower() in {"pass", "true", "ok", "sim"}
        checks = fonte.get("checks") or fonte.get("gates")
        if isinstance(checks, dict):
            for chave in chaves:
                if chave in checks:
                    valor = checks[chave]
                    if isinstance(valor, bool):
                        return valor
                    if isinstance(valor, str):
                        return valor.strip().lower().startswith("pass")
    return None


def _pendencias(*fontes) -> list:
    achadas = []
    for fonte in fontes:
        if not isinstance(fonte, dict):
            continue
        for campo in _CAMPOS_PENDENCIA:
            valor = fonte.get(campo)
            if isinstance(valor, list):
                achadas.extend(valor)
            elif isinstance(valor, str) and valor.strip():
                achadas.append(valor)
    return achadas


def _liberacao_externa(*fontes):
    for fonte in fontes:
        if not isinstance(fonte, dict):
            continue
        for campo in ("approvedForExternalRelease", "approvedForClientOrFiling"):
            if isinstance(fonte.get(campo), bool):
                return fonte[campo]
    return None


def validar_contexto(validacao, gate_result=None, texto_auditado=None):
    """Achados e vereditos de `facts_rechecked` e `context_complete`."""
    if not isinstance(validacao, dict) or not validacao:
        if not isinstance(gate_result, dict) or not gate_result:
            return {"versao": _GATE_VERSAO,
                    "findings": [{"gate": "LCX1-validacao-ausente", "sev": "P0",
                                  "problema": ("context_validation ausente ou vazio - a F7 nao "
                                               "registrou a validacao de contexto"),
                                  "acao": "emita context_validation com identidade e pendencias",
                                  "versao": _GATE_VERSAO}],
                    "gates": {GATE_FATOS: "fail", GATE_CONTEXTO: "fail"}}
        validacao = {}

    achados = []

    # --- facts_rechecked ---------------------------------------------------
    rechecado = _declarado_bool(validacao, gate_result,
                                chaves=("factsRechecked", "facts_rechecked"))
    if rechecado is None:
        # Ausência de declaração não é o mesmo que declaração falsa. Medido: o
        # caso CASO-17 não declara o recheque em dialeto nenhum, e a fase
        # reportou `pass` — achado real, mas o gate aqui não pode atestar nem
        # acusar. `warn` é o que ele honestamente sabe dizer. `fail` fica para
        # o verificavelmente falso: recheque negado e hash de outro texto.
        achados.append({
            "gate": "LFR1-recheque-nao-declarado", "sev": "P1",
            "problema": ("nenhum artefato da F7 declara se os fatos foram reconferidos - "
                         "silencio nao e atestado"),
            "acao": "declare factsRechecked no context_validation ou em checks do f7_gate_result",
            "versao": _GATE_VERSAO})
    elif rechecado is False:
        achados.append({
            "gate": "LFR2-recheque-negado", "sev": "P0",
            "problema": ("o proprio artefato declara que os fatos NAO foram reconferidos, e a "
                         "fase reportou o gate como aprovado"),
            "acao": "reconfira os fatos do ledger antes de fechar a F7",
            "versao": _GATE_VERSAO})

    # O artefato descreve ESTE texto? Hash divergente significa que a validação
    # de contexto examinou outra versão — e nenhuma leitura posterior detecta
    # isso, porque o JSON continua dizendo `true`.
    if texto_auditado:
        reais = _hashes_do_texto(texto_auditado)
        declarados = []
        for fonte in (validacao, gate_result or {}):
            if not isinstance(fonte, dict):
                continue
            for campo in _CAMPOS_HASH_TEXTO:
                if isinstance(fonte.get(campo), str):
                    declarados.append(fonte[campo])
            markdown = fonte.get("markdown")
            if isinstance(markdown, dict) and isinstance(markdown.get("sha256"), str):
                declarados.append(markdown["sha256"])
            origem = fonte.get("sourceHashes")
            if isinstance(origem, dict) and isinstance(origem.get("auditedMarkdown"), str):
                declarados.append(origem["auditedMarkdown"])
        if declarados and not any(d.strip().lower() in reais for d in declarados):
            achados.append({
                "gate": "LFR3-validacao-de-outro-texto", "sev": "P0",
                "problema": ("o hash do texto auditado declarado na validacao nao corresponde ao "
                             "texto - a auditoria examinou outra versao"),
                "acao": "revalide o contexto sobre a versao atual do texto",
                "versao": _GATE_VERSAO})

    fatos_p0 = any(a["gate"].startswith(("LFR", "LCX")) and a["sev"] == "P0" for a in achados)
    fatos_p1 = any(a["gate"].startswith("LFR") and a["sev"] == "P1" for a in achados)
    veredito_fatos = "fail" if fatos_p0 else ("warn" if fatos_p1 else "pass")

    # --- context_complete --------------------------------------------------
    pendentes = _pendencias(validacao, gate_result)
    externo = _liberacao_externa(validacao, gate_result)
    contexto_achados = []

    if pendentes and externo is True:
        contexto_achados.append({
            "gate": "LCC1-liberacao-externa-sobre-contexto-aberto", "sev": "P0",
            "problema": (f"{len(pendentes)} questao(oes) material(is) pendente(s) e o artefato "
                         "aprova liberacao externa - o contexto nao esta completo"),
            "acao": ("resolva as questoes materiais ou negue a liberacao externa enquanto "
                     "estiverem abertas"),
            "versao": _GATE_VERSAO})
    elif pendentes and externo is None:
        contexto_achados.append({
            "gate": "LCC2-pendencia-sem-fronteira-declarada", "sev": "P1",
            "problema": (f"ha {len(pendentes)} questao(oes) material(is) pendente(s) e o artefato "
                         "nao declara ate onde o produto pode ser usado"),
            "acao": "declare a fronteira de liberacao enquanto houver pendencia material",
            "versao": _GATE_VERSAO})

    tem_identidade = any(
        fonte.get(campo) for fonte in (validacao, gate_result or {})
        if isinstance(fonte, dict) for campo in _CAMPOS_IDENTIDADE)
    if not tem_identidade:
        contexto_achados.append({
            "gate": "LCC3-identidade-processual-ausente", "sev": "P1",
            "problema": ("a validacao de contexto nao declara tribunal nem identidade do processo "
                         "ou do ato impugnado"),
            "acao": ("declare a identidade processual - exigencia do protocolo de 11/07/2026 para "
                     "processo volumoso"),
            "versao": _GATE_VERSAO})

    achados.extend(contexto_achados)
    if any(a["sev"] == "P0" for a in contexto_achados):
        contexto = "fail"
    elif contexto_achados:
        contexto = "warn"
    else:
        contexto = "pass"

    return {"versao": _GATE_VERSAO, "findings": achados,
            "gates": {GATE_FATOS: veredito_fatos,
                      GATE_CONTEXTO: contexto}}


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

    texto = None
    for nome in ("audited_markdown.md", "final_markdown.md"):
        alvo = pasta / nome
        if alvo.is_file():
            texto = alvo.read_text(encoding="utf-8")
            break
    print(json.dumps(validar_contexto(_ler("context_validation.json"),
                                      _ler("f7_gate_result.json"), texto),
                     ensure_ascii=False, indent=2))
