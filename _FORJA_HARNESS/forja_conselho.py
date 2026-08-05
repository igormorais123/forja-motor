# -*- coding: utf-8 -*-
"""forja_conselho.py — computa os gates do conselho obrigatório da F4.

O protocolo da fábrica é inviolável desde 09/07/2026: toda petição passa por
Helena (estratégia) e Cícero (jurídico) antes da redação final, cada um emite
parecer escrito com recomendações numeradas, e o redator registra a decisão
sobre cada recomendação. Até 04/08/2026 os três gates que atestam isso —
`helena_present`, `cicero_present` e `council_decisions_recorded` — eram
escritos pelo próprio agente da fase no `PHASE_RESULT.json`. Nove execuções,
nove `pass`, nenhuma reprovação: ninguém sabia se o gate sabia dizer não.

Um `pass` falso aqui significa peça seguindo para redação sem o conselho que a
casa tornou obrigatório. É por isso que estes foram os primeiros a migrar da
palavra do agente para código.

**O que este módulo NÃO faz.** Não julga a qualidade do parecer nem se a decisão
tomada foi acertada — isso é trabalho humano e continua sendo. Ele verifica o
que é verificável sem opinar: o parecer existe, tem recomendações numeradas e
não é um esqueleto; as deliberações existem, e cada uma declara estado e
responsável humano. A linha entre as duas coisas é deliberada: gate que tenta
julgar mérito vira trava, e trava ensina a contornar.

**Permissivo na forma, estrito na substância.** As deliberações reais usam
tabela markdown com ID, decisão, estado, responsável e evidência; lista numerada
também é aceita. O que não se aceita é linha sem estado ou sem responsável.
Reprovar o formato aprovado pelo dono é o erro que o § 5 das lições proíbe.
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

VERSAO = "FORJA-CONSELHO-v1"

# Um parecer precisa de recomendações para ser parecer. O protocolo pede
# "recomendações numeradas", então a contagem é sobre itens numerados de
# primeiro nível, e não sobre qualquer linha do documento.
_ITEM_NUMERADO = re.compile(r"^\s{0,3}(\d{1,2})[.)]\s+\S", re.M)
_SECAO_RECOMENDACOES = re.compile(r"^#{1,4}\s*.*recomenda", re.M | re.I)

# Piso de tamanho para separar parecer de esqueleto. Medido contra os pareceres
# reais do acervo, que vão de 3.4 KB a 3.7 KB: 800 bytes é folgado o bastante
# para não reprovar um parecer curto e legítimo, e apertado o bastante para
# pegar um arquivo criado só para o gate ficar verde.
_PISO_PARECER_BYTES = 800

_ESTADO_VAZIO = {"", "-", "—", "n/a", "na", "tbd", "?"}


def _ler(caminho: Path | None) -> str | None:
    if not caminho or not caminho.is_file():
        return None
    try:
        return caminho.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _achados_parecer(persona: str, caminho: Path | None) -> list[dict]:
    """L-C1: o parecer existe, tem corpo e traz recomendações numeradas."""
    texto = _ler(caminho)
    if texto is None:
        return [{"gate": f"LC1-{persona}", "sev": "P0",
                 "problema": f"parecer de {persona} ausente — o conselho obrigatório não ocorreu",
                 "acao": f"produza o parecer de {persona} antes da redação final",
                 "versao": VERSAO}]
    achados = []
    if len(texto.encode("utf-8")) < _PISO_PARECER_BYTES:
        achados.append({
            "gate": f"LC1-{persona}", "sev": "P0",
            "problema": (f"parecer de {persona} tem {len(texto.encode('utf-8'))} bytes — "
                         "curto demais para ser parecer, parece arquivo criado para o gate"),
            "acao": "emita o parecer real, com veredito e recomendações", "versao": VERSAO})
    numeradas = _ITEM_NUMERADO.findall(texto)
    if not numeradas:
        achados.append({
            "gate": f"LC1-{persona}", "sev": "P0",
            "problema": (f"parecer de {persona} sem recomendações numeradas — "
                         "o protocolo exige recomendações que possam ser decididas uma a uma"),
            "acao": "numere as recomendações", "versao": VERSAO})
    elif not _SECAO_RECOMENDACOES.search(texto):
        achados.append({
            "gate": f"LC1-{persona}", "sev": "P1",
            "problema": f"parecer de {persona} tem itens numerados sem seção de recomendações identificável",
            "acao": "nomeie a seção de recomendações", "versao": VERSAO})
    return achados


def _linhas_de_decisao(texto: str) -> list[list[str]]:
    """Linhas de deliberação, seja em tabela markdown ou em lista numerada."""
    linhas = []
    for linha in texto.splitlines():
        crua = linha.strip()
        if not crua.startswith("|") or not crua.endswith("|"):
            continue
        celulas = [c.strip() for c in crua.strip("|").split("|")]
        if len(celulas) < 3:
            continue
        # Cabeçalho e separador da tabela não são deliberações.
        if set("".join(celulas)) <= set("-: "):
            continue
        if celulas[0].casefold() in {"id", "#", "item"}:
            continue
        linhas.append(celulas)
    return linhas


def _achados_decisoes_json(texto: str) -> list[dict] | None:
    """Lê o dialeto JSON emitido por algumas execuções da F4.

    O acervo tem dois formatos legítimos de registro: tabela Markdown e
    ``{"decisions": [...]}``. Antes deste leitor, o segundo caía no caminho
    "nenhuma decisão identificável" mesmo quando cada recomendação estava
    registrada. A compatibilidade não transforma decisão do agente em decisão
    humana: `responsible` continua sendo uma conferência P1, como na tabela.
    ``None`` significa que o texto não é JSON de deliberação e permite ao
    chamador usar o parser Markdown existente.
    """
    try:
        payload = json.loads(texto)
    except (TypeError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None

    decisoes = payload.get("decisions")
    if not isinstance(decisoes, list):
        return None
    if not decisoes:
        return [{
            "gate": "LC2-decisoes", "sev": "P0",
            "problema": "arquivo JSON de deliberações sem nenhuma decisão identificável",
            "acao": "registre uma decisão por recomendação, com estado e responsável humano",
            "versao": VERSAO,
        }]

    achados = []
    for indice, item in enumerate(decisoes, 1):
        if not isinstance(item, dict):
            achados.append({
                "gate": "LC2-decisoes", "sev": "P0", "decisao": str(indice),
                "problema": f"deliberação {indice} não é um objeto estruturado",
                "acao": "registre cada deliberação como objeto com recomendação e decisão",
                "versao": VERSAO,
            })
            continue

        identificador = str(item.get("id") or item.get("decisionId")
                            or item.get("item") or indice)
        recomendacao = (item.get("recommendation") or item.get("recommendationId")
                        or item.get("recommendation_id"))
        if not recomendacao:
            achados.append({
                "gate": "LC2-decisoes", "sev": "P0", "decisao": identificador,
                "problema": f"deliberação {identificador} não vincula recomendação",
                "acao": "ligue a decisão à recomendação numerada correspondente",
                "versao": VERSAO,
            })

        estado = (item.get("state") or item.get("status") or item.get("decision")
                  or item.get("outcome") or "")
        if isinstance(estado, str) and estado.strip().casefold() in _ESTADO_VAZIO:
            estado = ""
        if not estado:
            achados.append({
                "gate": "LC2-decisoes", "sev": "P0", "decisao": identificador,
                "problema": f"deliberação {identificador} sem estado declarado",
                "acao": "declare o estado da deliberação",
                "versao": VERSAO,
            })

        responsavel = (item.get("responsible") or item.get("responsibleHuman")
                       or item.get("responsavel") or item.get("owner")
                       or item.get("decidedBy") or "")
        if not str(responsavel).strip() or str(responsavel).strip().casefold() in _ESTADO_VAZIO:
            achados.append({
                "gate": "LC2-decisoes", "sev": "P1", "decisao": identificador,
                "problema": (f"deliberação {identificador} sem responsável humano — "
                             "decisão sem dono não é decisão"),
                "acao": "nomeie o responsável humano",
                "versao": VERSAO,
            })
    return achados


def _achados_decisoes(caminho: Path | None) -> list[dict]:
    """L-C2: cada deliberação declara estado e responsável humano."""
    texto = _ler(caminho)
    if texto is None:
        return [{"gate": "LC2-decisoes", "sev": "P0",
                 "problema": ("deliberações do conselho ausentes — não há registro de qual "
                              "recomendação foi acatada, rejeitada ou por quê"),
                 "acao": "registre a decisão sobre cada recomendação dos pareceres",
                 "versao": VERSAO}]
    json_achados = _achados_decisoes_json(texto)
    if json_achados is not None:
        return json_achados
    linhas = _linhas_de_decisao(texto)
    if not linhas:
        # Sem tabela: aceitar lista numerada, desde que tenha itens.
        if not _ITEM_NUMERADO.search(texto):
            return [{"gate": "LC2-decisoes", "sev": "P0",
                     "problema": "arquivo de deliberações sem nenhuma decisão identificável",
                     "acao": "use tabela com ID, decisão, estado e responsável, ou lista numerada",
                     "versao": VERSAO}]
        return []
    achados = []
    for celulas in linhas:
        identificador = celulas[0] or "?"
        estado = celulas[2].casefold() if len(celulas) > 2 else ""
        responsavel = celulas[3] if len(celulas) > 3 else ""
        if estado in _ESTADO_VAZIO:
            achados.append({
                "gate": "LC2-decisoes", "sev": "P0", "decisao": identificador,
                "problema": f"deliberação {identificador} sem estado declarado",
                "acao": "declare o estado da deliberação", "versao": VERSAO})
        if not responsavel.strip() or responsavel.strip().casefold() in _ESTADO_VAZIO:
            achados.append({
                "gate": "LC2-decisoes", "sev": "P1", "decisao": identificador,
                "problema": (f"deliberação {identificador} sem responsável humano — "
                             "decisão sem dono não é decisão"),
                "acao": "nomeie o responsável humano", "versao": VERSAO})
    return achados


def validar_conselho(*, helena: Path | None, cicero: Path | None,
                     decisoes: Path | None) -> dict:
    """Devolve achados e o veredito de cada gate do contrato F4."""
    ach_helena = _achados_parecer("Helena", helena)
    ach_cicero = _achados_parecer("Cícero", cicero)
    ach_decisoes = _achados_decisoes(decisoes)

    def veredito(achados: list[dict]) -> str:
        if any(a["sev"] == "P0" for a in achados):
            return "fail"
        return "pass"

    return {
        "versao": VERSAO,
        "findings": ach_helena + ach_cicero + ach_decisoes,
        "gates": {
            "helena_present": veredito(ach_helena),
            "cicero_present": veredito(ach_cicero),
            "council_decisions_recorded": veredito(ach_decisoes),
        },
    }


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("uso: python forja_conselho.py <helena.md> <cicero.md> <council_decisions.md>")
        return 2
    laudo = validar_conselho(helena=Path(argv[0]), cicero=Path(argv[1]), decisoes=Path(argv[2]))
    for nome, valor in laudo["gates"].items():
        print(f"{nome:32} {valor}")
    for achado in laudo["findings"]:
        print(f"  {achado['sev']} {achado['gate']}: {achado['problema']}")
    return 1 if any(v == "fail" for v in laudo["gates"].values()) else 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    raise SystemExit(main(sys.argv[1:]))
