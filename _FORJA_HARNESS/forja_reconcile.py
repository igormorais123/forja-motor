"""FORJA N2 - F0 Reconciliação da fila (modo leitura / sombra).

Lê painel, comandos, pastas e evidências do escritório e produz:
  - _FORJA_HARNESS/state/<caseId>/FORJA_STATE.json  (schema N2)
  - _FORJA_HARNESS/reports/RECONCILIACAO_<data>.md   (relatório humano)

NÃO altera demandas.json, intervencoes_manuais.json nem qualquer pasta de caso
(princípio N2: modo sombra nunca move, apaga ou sobrescreve artefatos do fluxo real).

Spec normativa: FORJA_SPEC_MANIFEST.json (N2.0)
Gates: planejamento/06_GATES_QUALIDADE_FORJA.md
Contrato desta fase: TDD N2 seção 7 (F0) — bloqueia demanda sem pasta, sem comando,
sem origem ou com status contraditório; Gmail sem login vira needs_login, nunca ok.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

from forja_n3_common import PHASES, now_iso, read_json

FORJA = Path(__file__).resolve().parent
RAIZ = FORJA.parent
GESTAO = RAIZ / "gestao_escritorio"
DATA = GESTAO / "data"
STATE_DIR = FORJA / "state"
REPORTS_DIR = FORJA / "reports"

SPEC_VERSION = "N2.0"
COMANDOS = [
    "COMANDO_DO_EMAIL.md",
    "COMANDO_DO_WHATSAPP.md",
    "COMANDO_HERMES.md",
    "COMANDO_MANUAL.md",
]

def classificar_integracoes(status, bridge):
    """ok | degraded | needs_login | offline — nunca promover falha a ok."""
    r = {}
    g = status.get("gmailLocal") or {}
    if g.get("authRequired"):
        r["gmail"] = "needs_login"
    elif g.get("ok"):
        r["gmail"] = "ok"
    elif g:
        r["gmail"] = "degraded"
    else:
        r["gmail"] = "offline"

    w = status.get("whatsappPersonal") or {}
    r["whatsapp"] = "ok" if w.get("ok") else ("degraded" if w else "offline")

    p = status.get("phoneAlert") or {}
    r["phoneAlert"] = "ok" if p.get("ok") else ("degraded" if p else "offline")

    r["hermesBridge"] = "ok" if (bridge or {}).get("ok") else ("degraded" if bridge else "offline")

    c = status.get("calendar") or {}
    # Calendar é lembrete humano, não executor (decisão N2); só registramos presença.
    r["calendarLembrete"] = "ok" if c.get("ok") else "degraded"
    return r


def finding(code, severity, detail):
    return {"code": code, "severity": severity, "detail": detail}


def reconciliar_gates(gates_anteriores, historico_anterior, findings, *, at):
    """Mantém somente gates ativos em ``gates`` e arquiva os encerrados.

    Estados N2 antigos não possuíam ``status`` nem ``gateHistory``. Eles são
    tratados como gates ativos para que a primeira reconciliação após a
    migração registre explicitamente qualquer encerramento, sem reabrir gates
    já resolvidos nem duplicar o histórico nas execuções seguintes.
    """
    anteriores = list(gates_anteriores or [])
    historico = list(historico_anterior or [])
    pendentes = {}
    for gate in anteriores:
        chave = (gate.get("code"), gate.get("detail"))
        pendentes.setdefault(chave, []).append(gate)

    ativos = []
    for item in findings:
        chave = (item.get("code"), item.get("detail"))
        episodios = pendentes.get(chave) or []
        anterior = episodios.pop(0) if episodios else None
        if not episodios:
            pendentes.pop(chave, None)
        ativos.append({
            "code": item["code"],
            "severity": item["severity"],
            "detail": item["detail"],
            "at": (anterior or {}).get("at") or at,
            "status": "active",
            "lastObservedAt": at,
        })

    for episodios in pendentes.values():
        for gate in episodios:
            encerrado = dict(gate)
            encerrado.update({
                "status": "resolved",
                "resolvedAt": at,
                "resolvedBy": "forja_reconcile:F0",
                "resolution": "finding_not_observed_in_current_reconciliation",
            })
            historico.append(encerrado)

    return ativos, historico


def _texto_da_evidencia(bruto):
    """Aceita a evidência como texto ou como registro estruturado.

    O campo nasceu string e passou a ser gravado também como objeto com `em`,
    `threadId` e a lista de `mensagens`. O reconciliador quebrava com
    `AttributeError: 'dict' object has no attribute 'strip'` na primeira demanda
    no formato novo — e, como ele é a porta única da reconciliação, o painel
    inteiro parava de ser conferido por causa de um registro.
    """
    if isinstance(bruto, dict):
        partes = []
        if bruto.get("em"):
            partes.append(str(bruto["em"]))
        for m in (bruto.get("mensagens") or [])[:3]:
            if isinstance(m, dict):
                partes.append(f"{m.get('id', '?')} {m.get('assunto', '')}".strip())
            else:
                partes.append(str(m))
        if not partes and bruto.get("threadId"):
            partes.append(f"thread {bruto['threadId']}")
        return " · ".join(partes).strip()
    if isinstance(bruto, (list, tuple)):
        return " · ".join(str(x) for x in bruto if x).strip()
    return (bruto or "").strip()


# O localizador é a única parte da evidência que se confere contra a fonte, e é
# onde a prosa costuma terminar ("...respondido por e-mail Gmail 19a0b1c2..."):
# cortar o texto pelo comprimento cortava justamente a prova. Medido em
# 10/08/2026: um caso da casa constava como "cumprido sem prova" e tinha DOIS
# identificadores de mensagem registrados no painel, ambos além do caractere 140.
# A acusação era falsa, e nasceu do resumo — não do trabalho.
_LOCALIZADOR = re.compile(r"\b(?:19[0-9a-f]{14}|[0-9a-f]{16}|3[A-F0-9]{15,31})\b")


def _resumo_com_localizadores(texto, limite=140):
    """Encurta a prosa e nunca encurta a prova."""
    corte = texto[:limite]
    perdidos = [x for x in dict.fromkeys(_LOCALIZADOR.findall(texto)) if x not in corte]
    if not perdidos:
        return corte
    return f"{corte} · localizadores: {', '.join(perdidos)}"


def evidencia_de_entrega(item, entregas, manual_entry):
    """Retorna (status, descricao). Evidência real exigida para cumprida (N2)."""
    ev = _texto_da_evidencia(item.get("evidenciaResposta"))
    if ev:
        return "manual_override", (
            f"Evidência registrada na demanda: {_resumo_com_localizadores(ev)}")
    if item.get("emailsResposta"):
        return "sent_confirmed", f"E-mail(s) de resposta: {', '.join(item['emailsResposta'][:3])}"
    overrides = (manual_entry or {}).get("overrides") or {}
    ev_manual = _texto_da_evidencia(overrides.get("evidenciaResposta"))
    if ev_manual:
        return "manual_override", (
            f"Evidência em intervenção manual: {_resumo_com_localizadores(ev_manual)}")
    # Cruzar com entregas arquivadas (por threadId/messageId nos assuntos arquivados)
    ids = set(item.get("emailsRecebidos") or []) | set(item.get("threadIds") or [])
    for d in (entregas or {}).get("deliveries", []):
        did = d.get("messageId") or ""
        dthread = d.get("threadId") or ""
        if did in ids or dthread in ids:
            return "sent_confirmed", f"Entrega arquivada: {d.get('subject', '(sem assunto)')[:100]}"
    return "none", "Nenhuma evidência de entrega localizada"


def auditar_demanda(item, entregas, manual_items, pastas_vistas, threads_vistos):
    findings = []
    demanda_id = item.get("id") or "(sem id)"
    manual_entry = (manual_items or {}).get(demanda_id)

    # Origem
    if not item.get("origem"):
        findings.append(finding("ORIGEM_AUSENTE", "P0", "Demanda sem origem registrada."))

    # Pasta
    pasta = item.get("pasta") or ""
    folder = (RAIZ / pasta) if pasta else None
    if not pasta:
        findings.append(finding("PASTA_AUSENTE", "P0", "Demanda sem pasta vinculada."))
    elif not folder.exists():
        findings.append(finding("PASTA_INEXISTENTE", "P0", f"Pasta não existe no disco: {pasta}"))
    else:
        if pasta in pastas_vistas:
            findings.append(finding("PASTA_DUPLICADA", "P1", f"Pasta compartilhada com a demanda {pastas_vistas[pasta]}."))
        pastas_vistas[pasta] = demanda_id

    # Comando legível por IA
    if folder and folder.exists():
        tem_comando = any((folder / c).exists() for c in COMANDOS)
        if not tem_comando:
            findings.append(finding("COMANDO_AUSENTE", "P0", "Nenhum COMANDO_*.md na pasta do caso."))

    # Duplicidade por thread
    for t in item.get("threadIds") or []:
        if t in threads_vistos and threads_vistos[t] != demanda_id:
            findings.append(finding("THREAD_DUPLICADO", "P1", f"threadId {t} também na demanda {threads_vistos[t]}."))
        threads_vistos[t] = demanda_id

    # Anexos
    anexos = item.get("anexos") or {}
    esperados = anexos.get("diretosEsperados")
    baixados = anexos.get("diretosBaixados")
    if esperados is not None and baixados is not None and baixados < esperados:
        findings.append(finding("ANEXOS_INCOMPLETOS", "P1", f"Anexos diretos: {baixados}/{esperados} baixados."))
    if item.get("status") != "cumprida" and anexos.get("externosPendentes"):
        findings.append(finding("ANEXOS_EXTERNOS_PENDENTES", "P1", "Há anexos externos (Drive/TransferNow/WhatsApp) não confirmados."))

    # Prazo (triagem)
    if item.get("status") != "cumprida" and not item.get("prazo"):
        findings.append(finding("SEM_PRAZO_TRIAGEM", "P2", "Aberta sem prazo estruturado; triagem pendente."))

    # Evidência de entrega (regra de ouro N2: cumprida exige prova)
    ev_status, ev_desc = evidencia_de_entrega(item, entregas, manual_entry)
    if item.get("status") == "cumprida" and ev_status == "none":
        findings.append(finding("CUMPRIDA_SEM_EVIDENCIA", "P0", "Marcada cumprida sem evidência de entrega arquivada."))

    # Estado N2 do caso
    tem_p0 = any(f["severity"] == "P0" for f in findings)
    if item.get("status") == "cumprida":
        case_status = "fulfilled" if ev_status != "none" else "waiting_delivery_evidence"
    elif tem_p0:
        case_status = "blocked"
    else:
        case_status = "pending"

    return findings, case_status, {"status": ev_status, "detail": ev_desc}


ESTA_FASE = "F0_RECONCILIACAO_FILA"


def _fase_preservada(anterior) -> str:
    """A reconciliação nunca puxa um caso de volta para a primeira fase.

    Até 09/08/2026 esta função não existia e `currentPhase` era reescrito como
    F0 em toda passagem. O efeito era mudo e grave: um caso que atravessou F1 a
    F10 e entregou 94 arquivos voltava a se descrever como "em reconciliação".
    Somado ao carimbo repetido abaixo, produzia o retrato de uma fábrica que
    nunca sai do lugar — e nenhum leitor do estado tinha como saber que a
    regressão fora escrita por uma varredura, e não pelo trabalho.
    """
    atual = (anterior or {}).get("currentPhase")
    if not atual or atual not in PHASES:
        return ESTA_FASE
    return atual if PHASES.index(atual) > PHASES.index(ESTA_FASE) else ESTA_FASE


def _historico_sem_repetir(anterior, fase, case_status, instante):
    """Carimbo novo só quando fase ou situação mudaram de fato.

    O mesmo caso chegou a acumular vinte e três entradas idênticas de
    `F0/fulfilled`. Cada passagem aparentava movimento e reescrevia o relógio,
    de modo que a idade de todo caso lia zero dia — inclusive a de um parado
    desde 11/07. Registro de história que grava não-eventos deixa de ser
    história.
    """
    historico = list((anterior or {}).get("phaseHistory") or [])
    ultimo = historico[-1] if historico else None
    if ultimo and ultimo.get("phase") == fase and ultimo.get("status") == case_status:
        return historico, False
    historico.append({"phase": fase, "at": instante, "status": case_status})
    return historico, True


def gravar_state(demanda, findings, case_status, evidence, integracoes):
    case_id = "case-" + (demanda.get("id") or "sem-id")
    case_dir = STATE_DIR / case_id
    case_dir.mkdir(parents=True, exist_ok=True)
    state_path = case_dir / "FORJA_STATE.json"
    anterior = read_json(state_path, None)
    exploration_path = case_dir / "n4_artifacts" / "F2_QUESTION_TREE.json"
    exploration = (anterior or {}).get("initialExploration") or {
        "protocolVersion": "FORJA-F2A-100-v1",
        "phase": "F2A_EXPLORACAO_PROBLEMA_100_PERGUNTAS",
        "status": "pending",
        "requiredArtifact": "F2_QUESTION_TREE.json",
        "rule": "100 perguntas adaptadas ao caso, 10 oticas, respostas com proveniencia e handoff F3-F7",
    }
    if exploration_path.is_file():
        exploration = {**exploration, "status": "materialized", "artifactPath": str(exploration_path)}
    instante = now_iso()
    gates, gate_history = reconciliar_gates(
        (anterior or {}).get("gates"),
        (anterior or {}).get("gateHistory"),
        findings,
        at=instante,
    )
    fase = _fase_preservada(anterior)
    historico, mudou = _historico_sem_repetir(anterior, fase, case_status, instante)
    state = {
        "caseId": case_id,
        "specVersion": SPEC_VERSION,
        "createdAt": (anterior or {}).get("createdAt") or now_iso(),
        # Só carimba o relógio quando houve mudança. `updatedAt` reescrito por
        # varredura mede a varredura, não o caso.
        "updatedAt": instante if mudou else ((anterior or {}).get("updatedAt") or instante),
        "currentPhase": fase,
        "status": case_status,
        "inputs": {
            "demandId": demanda.get("id"),
            "caseFolder": str(RAIZ / (demanda.get("pasta") or "")) if demanda.get("pasta") else None,
            "commandFile": next(
                (c for c in COMANDOS if demanda.get("pasta") and (RAIZ / demanda["pasta"] / c).exists()),
                None,
            ),
        },
        "phaseHistory": historico,
        "artifacts": (anterior or {}).get("artifacts") or [],
        "gates": gates,
        "gateHistory": gate_history,
        "sourceLedger": (anterior or {}).get("sourceLedger") or [],
        "deliveryEvidence": evidence,
        "integrations": integracoes,
        "initialExploration": exploration,
        "costLog": (anterior or {}).get("costLog") or [],
    }
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return case_id


def main():
    demandas_doc = read_json(DATA / "demandas.json", {"demandas": []})
    manual_doc = read_json(DATA / "intervencoes_manuais.json", {"items": {}})
    status_doc = read_json(DATA / "status_integracoes.json", {})
    bridge_doc = read_json(DATA / "hermes_bridge_status.json", {})
    entregas_doc = read_json(DATA / "entregas_fabio_osorio.json", {})

    integracoes = classificar_integracoes(status_doc, bridge_doc)
    itens = demandas_doc.get("demandas") or []
    pastas_vistas, threads_vistos = {}, {}
    resultados = []
    for item in itens:
        findings, case_status, evidence = auditar_demanda(
            item, entregas_doc, manual_doc.get("items") or {}, pastas_vistas, threads_vistos
        )
        case_id = gravar_state(item, findings, case_status, evidence, integracoes)
        resultados.append(
            {
                "caseId": case_id,
                "demandaId": item.get("id"),
                "titulo": item.get("titulo"),
                "statusPainel": item.get("status"),
                "statusForja": case_status,
                "findings": findings,
                "evidence": evidence,
            }
        )

    # Relatório humano
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    data_str = datetime.now().strftime("%Y-%m-%d_%H%M")
    rel = REPORTS_DIR / f"RECONCILIACAO_{data_str}.md"
    p0 = [r for r in resultados if any(f["severity"] == "P0" for f in r["findings"])]
    aguardando_ev = [r for r in resultados if r["statusForja"] == "waiting_delivery_evidence"]
    linhas = [
        "# FORJA N2 — Relatório de reconciliação da fila (F0)",
        "",
        f"Gerado em: {now_iso()} | Spec: {SPEC_VERSION} | Modo: leitura (sombra — nada foi alterado no painel)",
        "",
        "## Integrações",
        "",
    ]
    for k, v in integracoes.items():
        linhas.append(f"- {k}: **{v}**")
    linhas += [
        "",
        "## Números",
        "",
        f"- Demandas auditadas: **{len(resultados)}**",
        f"- Com bloqueio P0: **{len(p0)}**",
        f"- Cumpridas aguardando evidência de entrega: **{len(aguardando_ev)}**",
        "- Estados gravados em: `_FORJA_HARNESS/state/`",
        "",
        "## Demandas com achados",
        "",
    ]
    for r in resultados:
        if not r["findings"]:
            continue
        linhas.append(f"### {r['demandaId']} — {r['titulo']}")
        linhas.append(f"- Painel: `{r['statusPainel']}` | FORJA: `{r['statusForja']}` | Evidência: {r['evidence']['status']}")
        for f in r["findings"]:
            linhas.append(f"- [{f['severity']}] `{f['code']}`: {f['detail']}")
        linhas.append("")
    limpo = [r for r in resultados if not r["findings"]]
    linhas.append(f"## Sem achados ({len(limpo)})")
    linhas.append("")
    for r in limpo:
        linhas.append(f"- {r['demandaId']} — {r['titulo']} (FORJA: `{r['statusForja']}`)")
    rel.write_text("\n".join(linhas) + "\n", encoding="utf-8")

    resumo = {
        "ok": True,
        "auditadas": len(resultados),
        "p0": len(p0),
        "aguardandoEvidencia": len(aguardando_ev),
        "relatorio": str(rel),
        "integracoes": integracoes,
    }

    # FORJA FILA (R1.1 Helena, 12/07/2026): após reconciliar, regenerar a fila
    # priorizada sob flag. Falha da fila NUNCA derruba o F0 — a fila é derivada;
    # o F0 é autoridade (TDD planejamento/16 §5).
    try:
        from forja_n3_common import feature_enabled
        if feature_enabled("filaPriorizadaV1"):
            import forja_fila
            fila = forja_fila.gerar()
            resumo["fila"] = fila["resumo"]
    except Exception as exc:  # noqa: BLE001
        print(f"[fila] falhou sem bloquear o F0: {exc}", file=sys.stderr)

    print(json.dumps(resumo, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
