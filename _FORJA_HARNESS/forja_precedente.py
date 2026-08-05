"""Trilha de pesquisa jurídica e ficha do precedente-âncora.

Dois contratos que respondem a perguntas distintas.

`FORJA-LEGAL-SEARCH-TRACE-v1` responde **como se procurou**: qual base, qual
consulta, quais filtros, o que voltou, o que foi descartado e por quê, e o que
deliberadamente não se procurou. Sem essa trilha, "não há precedente contrário"
é opinião; com ela, é resultado reproduzível de uma busca declarada.

`FORJA-PRECEDENT-ANCHOR-v1` responde **o que o precedente decide**. Ementa não
é holding: é resumo redigido por terceiro, sem valor decisório próprio. A ficha
exige a íntegra, o localizador do trecho e o hash — e, pelas emendas E7, E8 e
E13, a vigência em quatro estados, o confronto com o contrário conhecido e o
regime declarado por dispositivo, nunca por rótulo.
"""

from __future__ import annotations

import re
from pathlib import Path

from forja_n4_common import issue
from forja_official_sources import source_excerpt_sha256


RESEARCH_PROTOCOL = "FORJA-LEGAL-SEARCH-TRACE-v1"
ANCHOR_PROTOCOL = "FORJA-PRECEDENT-ANCHOR-v1"

FULL_TEXT_STATUSES = {"verified", "insufficient", "not_applicable"}
ANCHOR_OPERATIONS = {"apply", "distinguish", "limit_scope", "argue_overruling"}

# E7 — vigência em quatro estados. "Superado" e "afetado por tema posterior"
# não são sinônimos: o segundo ainda decide enquanto o tema não é julgado.
VIGENCIA_STATES = {"vigente", "modulado", "superado", "afetado_por_tema_posterior"}

# E13 — o regime é convenção interna da FORJA, inclusive na categoria
# "vinculante". A peça afirma o efeito pelo dispositivo que o cria; o rótulo
# organiza o trabalho interno e não vale como fundamento.
REGIME_FIELDS = (
    "legalBasis", "authorityType", "dutyOrEffect",
    "competentBody", "changePath", "validityStatus", "checkedAt",
)
REGIME_SCORE_FIELDS = ("authorityScore", "precedentScore", "weight", "peso")

# Decisão sancionatória administrativa decide um processo administrativo. Ela
# pode ser fato do caso, prova de conduta ou objeto de impugnação — nunca
# precedente judicial. A confusão é fácil justamente porque a linguagem se
# parece: há relator, voto, ementa e acórdão.
AUTORIDADES_ADMINISTRATIVAS = (
    "cgu", "cade", "tcu", "cvm", "bacen", "coaf", "carf", "pas",
    "controladoria-geral", "tribunal de contas", "corregedoria",
    "processo administrativo sancionador", "conselho de recursos",
)
# Fronteira de palavra: "CADE" é órgão; "academia" não é. Sigla curta sem
# âncora de palavra produz falso positivo dentro de palavra comum.
_ADMINISTRATIVA = re.compile(
    r"(?<![0-9A-Za-zÀ-ÿ])(?:" + "|".join(AUTORIDADES_ADMINISTRATIVAS) + r")(?![0-9A-Za-zÀ-ÿ])",
    re.I,
)


# ---------------------------------------------------------------------------
# Trilha de pesquisa jurídica (F5)
# ---------------------------------------------------------------------------

def validate_legal_research_trace(
    payload: dict,
    mode: str = "shadow",
    *,
    denied_actions: set[str] | None = None,
    case_dir: Path | None = None,
) -> list[dict]:
    """Valida o bloco `searchRuns` do source ledger.

    O bloco é aditivo e top-level: ledgers históricos existem em mais de uma
    forma (`entries`, `sources`, lista direta) e não são reformatados aqui.
    Ledger sem o bloco não é irregular — é anterior ao protocolo.
    """
    if not isinstance(payload, dict):
        return []
    runs = payload.get("searchRuns")
    if runs is None:
        return []
    findings: list[dict] = []
    if payload.get("legalResearchProtocol") != RESEARCH_PROTOCOL:
        findings.append(issue(
            "FAL-F5-QUERY-INCOMPLETE",
            f"bloco de pesquisa sem `legalResearchProtocol: {RESEARCH_PROTOCOL}`",
        ))
    if not isinstance(runs, list):
        return findings + [issue("FAL-F5-QUERY-INCOMPLETE", "`searchRuns` não é lista")]

    vistos: set[str] = set()
    for run in runs:
        if not isinstance(run, dict):
            findings.append(issue("FAL-F5-QUERY-INCOMPLETE", "entrada de busca não é objeto"))
            continue
        qid = str(run.get("queryId") or "").strip()
        rotulo = qid or "consulta sem ID"
        if not qid:
            findings.append(issue("FAL-F5-QUERY-INCOMPLETE", "consulta sem `queryId`"))
        elif qid in vistos:
            findings.append(issue(
                "FAL-F5-QUERY-DUPLICATE",
                f"{qid}: ID de consulta repetido; duas buscas distintas com o mesmo ID "
                "tornam a trilha irreproduzível",
            ))
        else:
            vistos.add(qid)

        for campo, nome in (("database", "base consultada"),
                            ("executedAt", "horário de execução"),
                            ("query", "consulta literal")):
            if not str(run.get(campo) or "").strip():
                findings.append(issue(
                    "FAL-F5-QUERY-INCOMPLETE", f"{rotulo}: {nome} ausente"))
        if not isinstance(run.get("filters"), dict):
            # Filtro ausente e filtro vazio são estados diferentes: o segundo
            # afirma que a busca foi ampla, o primeiro não afirma nada.
            findings.append(issue(
                "FAL-F5-QUERY-INCOMPLETE",
                f"{rotulo}: filtros não declarados; `{{}}` afirma busca sem filtro",
            ))

        resultados = {str(v) for v in (run.get("resultIds") or [])}
        descartes = run.get("discarded") or []
        for item in descartes:
            if not isinstance(item, dict):
                findings.append(issue(
                    "FAL-F5-QUERY-INCOMPLETE", f"{rotulo}: descarte sem estrutura"))
                continue
            rid = str(item.get("resultId") or "")
            if not str(item.get("reason") or "").strip():
                findings.append(issue(
                    "FAL-F5-QUERY-INCOMPLETE",
                    f"{rotulo}: descarte de {rid or '?'} sem motivo registrado",
                ))
            if rid and rid in resultados:
                findings.append(issue(
                    "FAL-F5-RESULT-DISCARD-OVERLAP",
                    f"{rotulo}: {rid} consta como aproveitado e descartado ao mesmo tempo",
                ))

        if run.get("negativeResult") is True:
            if not str(run.get("query") or "").strip() or not str(run.get("executedAt") or "").strip():
                findings.append(issue(
                    "FAL-F5-NEGATIVE-NO-QUERY",
                    f"{rotulo}: resultado negativo sem consulta executada; ausência só é "
                    "probatória quando a busca que não achou está descrita",
                ))
            if resultados:
                findings.append(issue(
                    "FAL-F5-NEGATIVE-NO-QUERY",
                    f"{rotulo}: declarado negativo, mas com resultados aproveitados",
                ))

        replay = str(run.get("replayRef") or "").strip()
        if replay:
            alvo = Path(replay)
            if not alvo.is_absolute() and case_dir is not None:
                alvo = case_dir / replay
            if not alvo.is_file():
                findings.append(issue(
                    "FAL-F5-REPLAY-MISSING",
                    f"{rotulo}: replay declarado em {replay}, mas o arquivo não existe",
                ))

        ferramenta = str(run.get("endpointOrTool") or "").strip()
        if ferramenta and ferramenta in (denied_actions or set()):
            findings.append(issue(
                "FAL-F5-PAID-ACTION-DENIED",
                f"{rotulo}: consulta executada por ação vedada ({ferramenta})",
            ))
    return findings


# ---------------------------------------------------------------------------
# Ficha do precedente-âncora (F7)
# ---------------------------------------------------------------------------

def _regime_findings(rotulo: str, regime: dict) -> list[dict]:
    findings: list[dict] = []
    if not isinstance(regime, dict) or not regime:
        return [issue("FAL-F7-REGIME-INCOMPLETE", f"{rotulo}: regime não declarado")]
    def preenchido(campo: str) -> bool:
        valor = regime.get(campo)
        return bool(valor) if campo == "legalBasis" else bool(str(valor or "").strip())

    faltando = [campo for campo in REGIME_FIELDS if not preenchido(campo)]
    if faltando:
        findings.append(issue(
            "FAL-F7-REGIME-INCOMPLETE",
            f"{rotulo}: regime incompleto; faltam {', '.join(faltando)}",
        ))
    # E13: o efeito vem do dispositivo. Um rótulo de vinculação sem base legal
    # é exatamente a inversão que o art. 489, §1º, não autoriza presumir.
    if str(regime.get("dutyOrEffect") or "").strip() and not (regime.get("legalBasis") or []):
        findings.append(issue(
            "FAL-F7-REGIME-INCOMPLETE",
            f"{rotulo}: efeito afirmado sem dispositivo que o crie; regime é convenção "
            "interna e não substitui base legal",
        ))
    texto = " ".join(
        str(regime.get(campo) or "") for campo in ("authorityType", "competentBody")
    )
    marca = _ADMINISTRATIVA.search(texto)
    if marca:
        findings.append(issue(
            "FAL-F7-ADMIN-NOT-PRECEDENT",
            f"{rotulo}: autoridade administrativa ({marca.group(0)}) invocada como âncora; "
            "decisão sancionatória é fato ou objeto do caso, não precedente judicial",
        ))
    presentes = [c for c in REGIME_SCORE_FIELDS if regime.get(c) is not None]
    if presentes:
        findings.append(issue(
            "FAL-F7-REGIME-UNIVERSAL-SCORE",
            f"{rotulo}: regime com nota universal ({', '.join(presentes)}); autoridade se "
            "avalia por dispositivo, órgão e via de alteração, não por escore",
        ))
    return findings


def _vigencia_findings(rotulo: str, card: dict, operation: str) -> list[dict]:
    """E7 — vigência em quatro estados, com marco temporal da modulação."""
    regime = card.get("regime") or {}
    vigencia = str(card.get("vigencia") or regime.get("vigencia") or "").strip()
    if not vigencia:
        return [issue("FAL-F7-VIGENCIA-AUSENTE", f"{rotulo}: vigência do precedente não declarada")]
    if vigencia not in VIGENCIA_STATES:
        return [issue(
            "FAL-F7-VIGENCIA-INVALIDA",
            f"{rotulo}: vigência {vigencia!r} fora do contrato; use "
            f"{', '.join(sorted(VIGENCIA_STATES))}",
        )]
    findings: list[dict] = []
    if vigencia == "modulado" and not str(
        card.get("marcoTemporalModulacao") or regime.get("marcoTemporalModulacao") or ""
    ).strip():
        findings.append(issue(
            "FAL-F7-MODULACAO-SEM-MARCO",
            f"{rotulo}: precedente modulado sem marco temporal; sem a data, não se sabe "
            "se o caso está dentro ou fora do efeito",
        ))
    if vigencia == "superado" and operation == "apply":
        findings.append(issue(
            "FAL-F7-ANCHOR-INVALIDATES-ROUTE",
            f"{rotulo}: precedente superado invocado para aplicar; cabe `argue_overruling` "
            "ou outra âncora",
        ))
    if vigencia == "afetado_por_tema_posterior" and operation == "apply" and not str(
        card.get("afetacaoReason") or ""
    ).strip():
        findings.append(issue(
            "FAL-F7-VIGENCIA-AFETADA-SEM-RAZAO",
            f"{rotulo}: precedente afetado por tema posterior aplicado sem registrar por que "
            "ainda decide",
        ))
    return findings


def _contrario_findings(rotulo: str, card: dict) -> list[dict]:
    """E8 — o contrário conhecido é examinado, não silenciado."""
    if "precedenteContrarioConhecido" not in card:
        return [issue(
            "FAL-F7-CONTRARY-NOT-EXAMINED",
            f"{rotulo}: campo `precedenteContrarioConhecido` ausente; lista vazia declara "
            "exame sem achado, ausência não declara nada",
        )]
    contrarios = card.get("precedenteContrarioConhecido") or []
    findings: list[dict] = []
    if not str(card.get("contraryCheckedAt") or "").strip():
        findings.append(issue(
            "FAL-F7-CONTRARY-NOT-EXAMINED",
            f"{rotulo}: exame do contrário sem data; jurisprudência muda e o exame envelhece",
        ))
    for item in contrarios:
        if not isinstance(item, dict):
            findings.append(issue("FAL-F7-CONTRARY-NOT-EXAMINED", f"{rotulo}: contrário sem estrutura"))
            continue
        identidade = str(item.get("identity") or item.get("citation") or "").strip()
        if not identidade:
            findings.append(issue(
                "FAL-F7-CONTRARY-NOT-EXAMINED", f"{rotulo}: contrário sem identificação"))
        operacao = str(item.get("operation") or "").strip()
        if operacao not in ANCHOR_OPERATIONS:
            findings.append(issue(
                "FAL-F7-CONTRARY-NO-OPERATION",
                f"{rotulo}: contrário {identidade or '?'} sem operação declarada; citar o que "
                "pesa contra sem dizer como se opõe a ele é registro, não resposta",
            ))
    return findings


def validate_anchor_cards(
    entries: list[dict],
    *,
    selected_route_id: str | None = None,
    compared_route_ids: set[str] | None = None,
) -> list[dict]:
    """Valida as fichas de âncora do verified_source_ledger.

    Só examina entradas marcadas `anchor: true`. Entrada comum de ledger
    continua regida pelas regras de lastro já existentes.
    """
    findings: list[dict] = []
    vistos: set[str] = set()
    rotas_validas = set(compared_route_ids or set())
    if selected_route_id:
        rotas_validas.add(str(selected_route_id))

    for card in entries:
        if not isinstance(card, dict) or card.get("anchor") is not True:
            continue
        anchor_id = str(card.get("anchorId") or "").strip()
        rotulo = anchor_id or str(card.get("claim") or "âncora sem ID")
        if not anchor_id:
            findings.append(issue("FAL-F7-ANCHOR-NO-ID", f"{rotulo}: âncora sem `anchorId`"))
        elif anchor_id in vistos:
            findings.append(issue("FAL-F7-ANCHOR-NO-ID", f"{anchor_id}: `anchorId` repetido"))
        else:
            vistos.add(anchor_id)

        if card.get("anchorProtocol") != ANCHOR_PROTOCOL:
            findings.append(issue(
                "FAL-F7-ANCHOR-NO-PROTOCOL",
                f"{rotulo}: ficha sem `anchorProtocol: {ANCHOR_PROTOCOL}`",
            ))

        route_id = str(card.get("routeId") or "").strip()
        if not route_id:
            findings.append(issue(
                "FAL-F7-ANCHOR-INVALIDATES-ROUTE", f"{rotulo}: âncora sem rota vinculada"))
        elif rotas_validas and route_id not in rotas_validas:
            findings.append(issue(
                "FAL-F7-ANCHOR-INVALIDATES-ROUTE",
                f"{rotulo}: vinculada à rota {route_id}, que não é a selecionada nem consta "
                "das rotas comparadas",
            ))

        status = str(card.get("fullTextStatus") or "").strip()
        if status not in FULL_TEXT_STATUSES:
            findings.append(issue(
                "FAL-F7-ANCHOR-NO-FULL-TEXT",
                f"{rotulo}: `fullTextStatus` {status or 'ausente'!r} fora do contrato",
            ))
        elif status == "insufficient":
            # Ementa é resumo redigido por terceiro. Serve para localizar o
            # acórdão; não serve para afirmar o que ele decidiu.
            findings.append(issue(
                "FAL-F7-ANCHOR-NO-FULL-TEXT",
                f"{rotulo}: íntegra insuficiente; a ficha permanece candidata e não sustenta "
                "holding na peça",
            ))

        holding = card.get("holding") or {}
        texto = str(holding.get("text") or "").strip()
        if not texto:
            findings.append(issue(
                "FAL-F7-ANCHOR-NO-FULL-TEXT", f"{rotulo}: holding sem texto"))
        if not str(holding.get("locator") or "").strip():
            findings.append(issue(
                "FAL-F7-HOLDING-NO-LOCATOR",
                f"{rotulo}: holding sem localizador; trecho sem página ou item não é conferível",
            ))
        if texto and holding.get("excerptSha256") != source_excerpt_sha256(texto):
            findings.append(issue(
                "FAL-F7-HOLDING-HASH-MISMATCH",
                f"{rotulo}: hash do trecho do holding diverge do texto registrado",
            ))

        operation = str(card.get("operation") or "").strip()
        if operation not in ANCHOR_OPERATIONS:
            findings.append(issue(
                "FAL-F7-ANCHOR-NO-OPERATION",
                f"{rotulo}: operação {operation or 'ausente'!r} fora de "
                f"{', '.join(sorted(ANCHOR_OPERATIONS))}",
            ))

        # O confronto tem de cobrir os fatos que a própria ficha declarou
        # determinantes. Declarar o fato e não confrontá-lo é escolher o que
        # comparar depois de saber o resultado.
        determinantes = [str(v) for v in (card.get("decisiveFacts") or [])]
        comparados = {
            str(item.get("element") or item.get("fact") or "")
            for item in (card.get("elementComparison") or [])
            if isinstance(item, dict)
        }
        ausentes = [f for f in determinantes if f not in comparados]
        if ausentes:
            findings.append(issue(
                "FAL-F7-FACT-FRAME-INCOMPLETE",
                f"{rotulo}: fatos determinantes sem confronto: {', '.join(ausentes)}",
            ))
        for item in card.get("elementComparison") or []:
            if isinstance(item, dict) and not str(item.get("verdict") or "").strip():
                findings.append(issue(
                    "FAL-F7-FACT-FRAME-INCOMPLETE",
                    f"{rotulo}: confronto de {item.get('element') or '?'} sem conclusão",
                ))

        findings.extend(_vigencia_findings(rotulo, card, operation))
        findings.extend(_contrario_findings(rotulo, card))
        findings.extend(_regime_findings(rotulo, card.get("regime") or {}))
    return findings


def anchor_ids(entries: list[dict]) -> set[str]:
    """IDs de âncora efetivamente presentes no ledger."""
    return {
        str(item.get("anchorId"))
        for item in entries
        if isinstance(item, dict) and item.get("anchor") is True and item.get("anchorId")
    }


def failed_anchor_routes(findings: list[dict], entries: list[dict]) -> set[str]:
    """Rotas atingidas por âncora reprovada — entrada da reabertura de F4."""
    if not findings:
        return set()
    por_id = {
        str(item.get("anchorId")): str(item.get("routeId") or "")
        for item in entries
        if isinstance(item, dict) and item.get("anchor") is True
    }
    rotas: set[str] = set()
    for finding in findings:
        rotulo = str(finding.get("detail") or "").split(":", 1)[0].strip()
        rota = por_id.get(rotulo)
        if rota:
            rotas.add(rota)
    return rotas
