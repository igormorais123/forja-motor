"""Canonical, resumable phase executor for FORJA N3.

Agents work inside runs/<run>/<phase>/<attempt>. Only validated PHASE_RESULT.json
artifacts are promoted to n3_artifacts and recorded in the event store.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

from forja_n3_common import (
    FORJA,
    WORKSPACE,
    ForjaN3Error,
    atomic_write_json,
    canonical_hash,
    ensure_within,
    name_with_legacy,
    new_id,
    now_iso,
    read_json,
    resolve_case_dir,
    resolve_name,
    sha256_file,
)
from forja_phase_contracts import load_contract
from forja_state_machine import derive_state, load_events, record_event
from forja_adversarial_audit import validate_phase_artifacts
from forja_n4_common import ARTIFACT_SPECS
from forja_exploracao_100 import validate_exploration_100
from forja_editorial_fidelity import validate_editorial_bundle
from forja_severidade import blocking_findings


TEMPLATE = WORKSPACE / "_FERRAMENTAS" / "TEMPLATE_MEDINA_OSORIO_PETICAO.docx"


def _artifact_path(entry: dict) -> Path | None:
    value = entry.get("path") if isinstance(entry, dict) else None
    return Path(value) if value else None


def _read_gate_artifact(path_value: Path | str | None) -> Any:
    """Lê o artefato da forma emitida, sem transformar Markdown em ausência."""
    if not path_value:
        return {}
    path = Path(path_value)
    if not path.is_file():
        return {}
    if path.suffix.lower() in {".md", ".markdown", ".txt"}:
        return path.read_text(encoding="utf-8", errors="replace")
    return read_json(path, {})


def _resolve_input(case_dir: Path, state: dict, input_id: str) -> dict | None:
    inputs = state.get("inputs") or {}
    artifacts = state.get("artifacts") or {}
    if input_id == "demandId":
        return {"kind": "value", "value": state.get("demandId")} if state.get("demandId") else None
    if input_id == "caseFolder":
        value = inputs.get("caseFolder")
        return {"kind": "path", "path": value} if value and Path(value).exists() else None
    if input_id in {"commandFile", "command"}:
        value = inputs.get("commandFile")
        folder = Path(inputs.get("caseFolder") or "")
        path = Path(value) if value and Path(value).is_absolute() else folder / str(value or "")
        return {"kind": "path", "path": str(path), "sha256": sha256_file(path)} if path.is_file() else None
    if input_id == "case_manifest":
        path = case_dir / "FORJA_CASE_MANIFEST.json"
        return {"kind": "path", "path": str(path), "sha256": sha256_file(path)} if path.exists() else None
    if input_id == "source_documents":
        folder = Path(inputs.get("caseFolder") or "")
        files = [path for path in folder.rglob("*") if path.is_file()] if folder.is_dir() else []
        return {"kind": "collection", "root": str(folder), "count": len(files)} if files else None
    if input_id == "template":
        return {"kind": "path", "path": str(TEMPLATE), "sha256": sha256_file(TEMPLATE)} if TEMPLATE.exists() else None
    entry = artifacts.get(input_id)
    path = _artifact_path(entry or {})
    if path and path.exists():
        return {"kind": "artifact", "artifactId": input_id, **entry}
    return None


def prepare_attempt(
    case_dir: Path,
    phase: str,
    *,
    expected_revision: int,
    run_id: str | None = None,
    actor: str = "forja-runner",
) -> dict:
    contract = load_contract(phase)
    state = derive_state(case_dir)
    resolved = {}
    missing = []
    for input_id in contract["requiredInputs"]:
        value = _resolve_input(case_dir, state, input_id)
        if value is None:
            missing.append(input_id)
        else:
            resolved[input_id] = value
    if missing:
        raise ForjaN3Error(f"{phase} sem entradas obrigatórias: {', '.join(missing)}")

    phase_events = load_events(case_dir)
    last_reopen_seq = max(
        (event["eventSeq"] for event in phase_events if event.get("type") == "gate_reopened" and event.get("phase") == phase),
        default=0,
    )
    attempts = [
        event for event in phase_events
        if event["eventSeq"] > last_reopen_seq and event.get("type") == "phase_started" and event.get("phase") == phase
    ]
    max_attempts = int((contract.get("retryPolicy") or {}).get("maxAttempts") or 1)
    if len(attempts) >= max_attempts:
        raise ForjaN3Error(f"{phase} excedeu {max_attempts} tentativas; reabertura formal necessária")

    run_id = run_id or new_id("run")
    attempt_id = new_id("attempt")
    event, state, _ = record_event(
        case_dir,
        "phase_started",
        expected_revision=expected_revision,
        idempotency_key=f"{case_dir.name}:{run_id}:{phase}:{attempt_id}:started",
        phase=phase,
        actor=actor,
        run_id=run_id,
        attempt_id=attempt_id,
        demand_id=state.get("demandId"),
        payload={"contractHash": contract["contractHash"]},
    )
    attempt_dir = case_dir / "runs" / run_id / phase / attempt_id
    attempt_dir.mkdir(parents=True, exist_ok=False)
    context = {
        "schemaVersion": 1,
        "specVersion": "N3.0-r2",
        "caseId": case_dir.name,
        "demandId": state.get("demandId"),
        "runId": run_id,
        "attemptId": attempt_id,
        "phase": phase,
        "phaseStartedEventSeq": event["eventSeq"],
        "contract": contract,
        "inputs": resolved,
        "createdAt": now_iso(),
        "instructions": {
            "writeOnlyInsideAttempt": True,
            "resultFile": "PHASE_RESULT.json",
            "requiredOutputs": contract["requiredOutputs"],
            "requiredGates": contract["requiredGates"],
            "n4Candidate": contract.get("n4Candidate"),
            "n4Rule": "Em shadow, produzir quando aplicável e registrar bloqueios sem relaxar critérios; não inventar dados para preencher artefatos.",
        },
    }
    aprendidas = _regras_aprendidas_da_fase(phase)
    if aprendidas:
        context["instructions"]["regrasAprendidas"] = aprendidas
    if phase == "F2_CLASSIFICACAO_PRODUTO_RISCO":
        context["instructions"]["exploration100"] = {
            "protocolVersion": "FORJA-F2A-100-v1",
            "template": str(FORJA / "templates" / "F2A_EXPLORACAO_100_PERGUNTAS.md"),
            "validator": str(FORJA / "forja_exploracao_100.py"),
            "rule": "exactly 100 case-adapted questions; 10 lenses x 10; answer, source or block; route F3-F7",
        }
    context["contextHash"] = canonical_hash(context)
    atomic_write_json(attempt_dir / "RUN_CONTEXT.json", context)
    return {"attemptDir": str(attempt_dir), "context": context, "state": state}


REGISTRO_APRENDIZADO = FORJA / "learning_registry" / "REGRAS_APRENDIDAS.json"


def _regras_aprendidas_da_fase(phase: str) -> list[dict]:
    """As regras que a casa aprendeu com o retorno humano, entregues ao agente.

    Existe porque aplicar a regra no arquivo de destino não a faz chegar a
    ninguém. Metade das regras adotadas em 06/08/2026 foi escrita num roteiro
    que nenhuma execução lê — o mesmo modo de falha do elo 4-B e do recomputo
    inerte do F7: o trabalho foi feito, ficou registrado, e a rota de produção
    não passava por ali.

    O contrato da fase já viaja inteiro dentro do RUN_CONTEXT, então a regra de
    destino `checklist` chegava por carona. A de destino `template`, não. Aqui a
    entrega deixa de depender de qual arquivo alguém escolheu como destino.
    """
    try:
        registro = json.loads(REGISTRO_APRENDIZADO.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    curta = str(phase).split("_", 1)[0]
    return [
        {
            "regraId": r.get("regraId"),
            "texto": r.get("texto"),
            "origem": "retorno_humano_pos_protocolo",
            "destinoArquivo": r.get("destinoArquivo"),
        }
        for r in (registro.get("regras") or [])
        if str(r.get("fase") or "") == curta and str(r.get("texto") or "").strip()
    ]


def _raiz_do_caso(alguma_saida: Path) -> Path | None:
    """Sobe da tentativa até a pasta do caso (a que contém ``n3_artifacts``).

    Nenhum ``RUN_CONTEXT.json`` do acervo declara ``inputs.caseFolder`` — medido
    em 04/08/2026, 10 de 10 vazios. Enquanto o base_dir dependeu só desse campo,
    o L12 rodou sem inventário econômico e o L2 sem fonte para conferir. A raiz
    é derivável do próprio caminho da tentativa, então derivá-la é mais fiável
    que cobrar declaração de quem já esqueceu dez vezes.
    """
    for pai in alguma_saida.resolve().parents:
        if (pai / "n3_artifacts").is_dir():
            return pai
    return None


def _lastro_context_base(context: dict, referencia: Path | None = None) -> Path | None:
    """A pasta onde os documentos do caso realmente estão.

    Não é a pasta do caso no harness: `quoteSource` aponta para arquivos do
    cliente (`COMANDO_DO_CASO.md`, laudos, incidentes), que vivem em
    `<workspace>/<Caso>/...`. Ancorar em `state/<caseId>` fazia o L2 devolver
    "fonte não localizada" para transcrição correta — a acusação errada contra
    quem fez certo. O caminho verdadeiro está no manifesto do caso, que é o
    único lugar onde ele foi gravado de forma confiável.
    """
    entrada = (context.get("inputs") or {}).get("caseFolder") or {}
    valor = entrada.get("path") if isinstance(entrada, dict) else entrada
    if valor and Path(str(valor)).is_dir():
        return Path(str(valor))
    raiz = _raiz_do_caso(referencia) if referencia else None
    if raiz:
        manifesto = raiz / "FORJA_CASE_MANIFEST.json"
        if manifesto.is_file():
            try:
                dados = json.loads(manifesto.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                dados = {}
            declarado = (dados.get("inputs") or {}).get("caseFolder") or dados.get("caseFolder")
            if declarado and Path(str(declarado)).is_dir():
                return Path(str(declarado))
    return raiz


def _achar_fact_ledger(artifacts: list[dict], referencia: Path | None) -> Path | None:
    """O ledger de fatos declarado; senão, o promovido pela F3 no caso.

    ``verified_source_ledger`` NÃO serve aqui: ele audita citações e autoridades
    (``entries`` com ``claim``/``authorityIdentity``), não as proposições do
    FORJA-LASTRO. Tratá-lo como ledger de fatos faria o gate reprovar em P0 o
    padrão aprovado — o erro que o § 5 das lições manda não cometer.
    """
    for item in artifacts:
        aid = item["artifactId"]
        if aid == "fact_ledger" or aid.startswith("fact_ledger_"):
            return item["source"]
    raiz = _raiz_do_caso(referencia) if referencia else None
    if raiz:
        promovido = raiz / "n3_artifacts" / "F3_FONTES_REGIMENTO_LEIS" / "fact_ledger.json"
        if promovido.is_file():
            return promovido
    return None


_GATES_ECONOMICOS = {"L9", "L10", "L11", "L12", "L13"}


def _severidade_economica(findings: list[dict]) -> str:
    """`fail` só com P0 econômico; `warn` com P1 apenas; senão `pass`."""
    economicos = [f for f in findings if f["gate"].split("-", 1)[0] in _GATES_ECONOMICOS]
    if any(f.get("sev") == "P0" for f in economicos):
        return "fail"
    return "warn" if economicos else "pass"


def _compute_lastro_gates(phase: str, artifacts: list[dict], context: dict) -> dict:
    """Recomputa lastro contra artefatos reais, sem confiar no PHASE_RESULT.

    F7 é a primeira fase que possui simultaneamente o ledger e o texto final.
    A função devolve um relatório pequeno para ficar no diretório da tentativa;
    o resultado declarado pelo agente nunca substitui esta prova.
    """
    if phase != "F7_AUDITORIA_JURIDICA_FACTUAL":
        return {"applicable": False, "phase": phase, "findings": [], "computed": {}}
    by_id = {item["artifactId"]: item for item in artifacts}

    def _achar(nomes: tuple[str, ...]):
        for nome in nomes:
            if nome in by_id:
                return by_id[nome]
        return next((item for item in artifacts
                     if item["artifactId"].startswith(tuple(n + "_" for n in nomes))), None)

    # Algumas execuções históricas não declararam o ``fact_ledger`` no próprio
    # PHASE_RESULT, embora o contrato atual o exija. O recomputo não pode
    # transformar isso em ``not_applicable``: ele resolve o ledger promovido
    # pela F3 no caso e registra ausência como achado, não como silêncio.
    final_item = _achar(("final_markdown",))
    if not final_item:
        return {"applicable": True, "phase": phase, "computed": {"status": "fail"},
                "findings": [{
                    "gate": "L0-recomputo-sem-insumo", "sev": "P0", "factId": "-",
                    "problema": ("F7 sem texto final entre os artefatos — o recomputo de lastro "
                                 "não teve o que auditar e não pode ser lido como aprovação"),
                    "acao": "declare final_markdown no PHASE_RESULT"}]}
    ledger_path = _achar_fact_ledger(artifacts, final_item["source"])
    if ledger_path is None:
        return {"applicable": True, "phase": phase, "computed": {"status": "fail"},
                "findings": [{
                    "gate": "L0-recomputo-sem-insumo", "sev": "P1", "factId": "-",
                    "problema": ("F7 sem ledger de fatos declarado nem promovido pela F3 — "
                                 "L1/L2/L9-L13 não examinaram nada; ausência de achados aqui "
                                 "não é aprovação"),
                    "acao": "declare fact_ledger no PHASE_RESULT ou promova o da F3 no caso"}]}
    ledger_item = {"artifactId": "fact_ledger", "source": ledger_path}
    # O estado histórico pode apontar para um snapshot hash-específico,
    # enquanto a fase mantém ``fact_ledger.json`` como fonte canônica mutável.
    # Quando os dois convivem no mesmo diretório, o recomputo usa o canônico;
    # caso contrário uma correção recente fica invisível no F7. A seleção é
    # somente leitura e fica registrada no laudo da tentativa.
    ledger_source = ledger_item["source"]
    canonical_ledger = ledger_source.with_name("fact_ledger.json")
    if canonical_ledger.is_file():
        ledger_source = canonical_ledger
    try:
        ledger = json.loads(ledger_source.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {
            "applicable": True,
            "phase": phase,
            "findings": [{
                "gate": "L0-recomputo-sem-insumo",
                "sev": "P0",
                "factId": "-",
                "problema": (
                    "ledger de fontes existe, mas não pôde ser lido como JSON; "
                    "o recomputo não pode ser tratado como aprovação"
                ),
                "acao": "corrija ou substitua o fact_ledger.json antes de promover a fase",
                "erro": str(exc),
            }],
            "computed": {"status": "fail", "reason": "fact_ledger inválido"},
            "ledger": str(ledger_source),
            "ledgerDeclared": str(ledger_item["source"]),
        }
    if not isinstance(ledger, dict):
        return {
            "applicable": True,
            "phase": phase,
            "findings": [{
                "gate": "L0-recomputo-sem-insumo",
                "sev": "P0",
                "factId": "-",
                "problema": (
                    "ledger de fontes não é um objeto JSON; o recomputo "
                    "não teve insumo estruturado e não pode passar em silêncio"
                ),
                "acao": "registre um fact_ledger.json estruturado antes de promover a fase",
            }],
            "computed": {"status": "fail", "reason": "fact_ledger fora do schema"},
            "ledger": str(ledger_source),
            "ledgerDeclared": str(ledger_item["source"]),
        }
    texto = final_item["source"].read_text(encoding="utf-8", errors="replace")
    base_dir = _lastro_context_base(context, final_item["source"])
    from forja_lastro import (
        validar_gates_economicos,
        validar_lastro_fatos,
        exigir_criterio_vigente,
        material_economico,
    )
    findings = validar_lastro_fatos(ledger, base_dir=base_dir)
    contexto_textual = " ".join((texto[:4000], str(context.get("instructions") or "")))
    exige_criterio = bool(
        (context.get("lastro") or {}).get("exigirCriterioVigente")
        or re.search(r"liquida[cç][aã]o|cumprimento\s+de\s+senten[cç]a|base\s+de\s+c[aá]lculo", contexto_textual, re.I)
    )
    if exige_criterio:
        findings.extend(exigir_criterio_vigente(ledger))
    economico = material_economico(texto)
    if economico:
        findings.extend(validar_gates_economicos(texto, ledger=ledger, base_dir=base_dir))
    computed = {
        "status": "pass" if not findings else "fail",
        "fact_grounding_verbatim": "pass" if not any(
            item["gate"].startswith(("L1-", "L2-")) for item in findings
        ) else "fail",
        "criterio_vigente": "pass" if not any(item["gate"] == "L7-criterio-vigente" for item in findings) else "fail",
        "economic_material": economico,
        # Severidade importa na flag agregada. Enquanto qualquer achado L9-L13
        # virava `fail`, a flag dizia "reprovado" sem que nada bloqueante
        # tivesse acontecido — e bloquear nela seria promover o L11 a P0 pela
        # porta dos fundos, importando os ~55% de falso positivo medidos da
        # heurística de valor citado. `warn` mantém o achado visível sem mentir
        # sobre a gravidade. Parecer Helena de 04/08/2026.
        "economic_gates": _severidade_economica(findings),
    }
    return {"applicable": True, "phase": phase, "findings": findings, "computed": computed,
            "ledger": str(ledger_source), "ledgerDeclared": str(ledger_item["source"]),
            "product": str(final_item["source"])}


def _recompute_injecao(contract: dict, artifacts: list[dict], attempt_dir: Path,
                       result: dict) -> None:
    """Computa `injection_triaged` em vez de aceitar o `pass` do agente.

    Existe por causa do U3 — conteúdo dos autos é dado, nunca instrução. O gate
    é tolerante à forma porque o artefato aparece no acervo em sete esquemas
    distintos, e estrito na substância: houve varredura declarada, e achado P0
    tem triagem humana registrada.
    """
    if contract["phase"] != "F1_INGESTAO_SEGURA":
        return
    from forja_injection_scan import validar_triagem_injecao

    por_id = {item["artifactId"]: item["source"] for item in artifacts}
    scan = read_json(por_id.get("injection_scan"), {}) if por_id.get("injection_scan") else {}
    laudo = validar_triagem_injecao(scan or {})
    atomic_write_json(attempt_dir / "COMPUTED_INJECAO_GATES.json", laudo)
    result["computedInjecaoGates"] = laudo["gates"]
    if laudo["gates"]["injection_triaged"] == "fail":
        detalhes = "; ".join(item["problema"] for item in laudo["findings"][:4])
        raise ForjaN3Error("triagem de injeção reprovada na recomputação: " + detalhes)
    result.setdefault("gates", {}).update(laudo["gates"])
    atomic_write_json(attempt_dir / "PHASE_RESULT.json", result)


def _recompute_politica_citacoes(contract: dict, artifacts: list[dict], attempt_dir: Path,
                                 result: dict) -> None:
    """Computa `citations_policy_satisfied` em vez de aceitar o `pass` do agente.

    Era o gate de maior volume da esteira — onze execuções, onze `pass`, zero
    reprovações — e o mais caro se falso: "jurisprudência com atribuição errada"
    é o erro recorrente nº 1 das entregas reais. O veredito `warn` existe para o
    ledger cujo esquema não permite conferência automática: nesse caso o gate
    não bloqueia, mas também não diz que auditou.
    """
    if contract["phase"] != "F7_AUDITORIA_JURIDICA_FACTUAL":
        return
    from forja_citations import validar_politica_citacoes

    por_id = {item["artifactId"]: item["source"] for item in artifacts}
    final = por_id.get("final_markdown")
    if not final or not final.is_file():
        return
    ledger_path = por_id.get("verified_source_ledger")
    ledger = read_json(ledger_path, {}) if ledger_path else {}
    from forja_citations import validar_identidade_citacoes

    texto = final.read_text(encoding="utf-8", errors="replace")
    laudo = validar_politica_citacoes(texto, ledger or {})
    identidade = validar_identidade_citacoes(texto, ledger or {})
    laudo["findings"].extend(identidade["findings"])
    laudo["gates"].update(identidade["gates"])
    # Cobertura, reabertura ao vivo e casamento de excerto respondem perguntas
    # diferentes sobre a mesma citação; confundi-las produz gate redundante ou
    # gate cego. Os três saem do mesmo ledger verificado.
    from forja_replay import validar_replay

    replay = validar_replay(ledger or {})
    laudo["findings"].extend(replay["findings"])
    laudo["gates"].update(replay["gates"])
    atomic_write_json(attempt_dir / "COMPUTED_CITACOES_GATES.json", laudo)
    result["computedCitacoesGates"] = laudo["gates"]
    reprovados = [nome for nome, valor in laudo["gates"].items() if valor == "fail"]
    if reprovados:
        detalhes = "; ".join(item["problema"] for item in laudo["findings"][:6])
        raise ForjaN3Error(
            f"citações reprovadas na recomputação ({', '.join(reprovados)}): {detalhes}")
    result.setdefault("gates", {}).update(laudo["gates"])
    atomic_write_json(attempt_dir / "PHASE_RESULT.json", result)


def _recompute_definicao(contract: dict, artifacts: list[dict], attempt_dir: Path,
                         result: dict) -> None:
    """Computa os gates que dizem PARA QUE a esteira trabalha (F0, F2, F4, F5, F9).

    Um `pass` falso aqui não produz erro visível: produz uma esteira inteira sem
    alvo, entregando trabalho tecnicamente correto sobre a pergunta errada.
    Ninguém reclama disso, e por isso ele nunca aparecia.
    """
    fase = contract["phase"]
    por_id = {item["artifactId"]: item["source"] for item in artifacts}
    laudo = None

    if fase == "F2_CLASSIFICACAO_PRODUTO_RISCO":
        from forja_produto import validar_definicao_produto
        laudo = validar_definicao_produto(
            read_json(por_id.get("product_classification"), {})
            if por_id.get("product_classification") else {})

    elif fase == "F4_BLUEPRINT_ESTRATEGICO":
        from forja_produto import validar_pergunta_jurisdicional
        caminho = por_id.get("blueprint")
        blueprint = {}
        if caminho and caminho.is_file():
            if caminho.suffix.lower() == ".md":
                blueprint = caminho.read_text(encoding="utf-8", errors="replace")
            else:
                blueprint = read_json(caminho, {}) or {}
        laudo = validar_pergunta_jurisdicional(blueprint)

    elif fase == "F5_PESQUISA_OFICIAL":
        from forja_produto import validar_uso_final
        laudo = validar_uso_final(read_json(por_id.get("source_ledger"), {})
                                  if por_id.get("source_ledger") else {})

    elif fase == "F0_RECONCILIACAO_FILA":
        from forja_entrega import validar_reconciliacao
        manifesto = (read_json(por_id.get("case_manifest"), {})
                     if por_id.get("case_manifest") else {})
        # O contrato aceita `reconciliation_report` como artefato textual
        # (Markdown) ou estruturado (JSON). Até 04/08/2026 a recomputação lia
        # apenas o segundo e devolvia `warn` para o resto — e como
        # `forja_reconcile.py` SEMPRE emitiu markdown, `status_consistent`
        # nunca conseguiu dizer `pass` em nenhuma tentativa da história. Gate
        # preso em `warn` é ruído, e ruído ensina o operador a passar por cima.
        # O validador passou a ler a forma textual.
        relatorio = _read_gate_artifact(por_id.get("reconciliation_report"))
        laudo = validar_reconciliacao(
            manifesto,
            relatorio)

    elif fase == "F9_PACOTE_REVISAO_DRAFT_OPCIONAL":
        from forja_entrega import validar_pacote
        email = None
        caminho = por_id.get("email_response")
        if caminho and caminho.is_file():
            email = (caminho.read_text(encoding="utf-8", errors="replace")
                     if caminho.suffix.lower() in {".md", ".txt"} else read_json(caminho, {}))
        manifesto = (read_json(por_id.get("package_manifest"), {})
                     if por_id.get("package_manifest") else {})
        laudo = validar_pacote(manifesto, email, attempt_dir, set(por_id))
        from forja_adversarial_gate import validar_politica_liberacao

        politica = validar_politica_liberacao(
            manifesto,
            read_json(por_id.get("f7_gate_result_package"), {})
            if por_id.get("f7_gate_result_package") else {})
        laudo["findings"].extend(politica["findings"])
        laudo["gates"].update(politica["gates"])

    if laudo is None:
        return

    atomic_write_json(attempt_dir / "COMPUTED_DEFINICAO_GATES.json", laudo)
    result["computedDefinicaoGates"] = laudo["gates"]
    reprovados = [nome for nome, valor in laudo["gates"].items() if valor == "fail"]
    if reprovados:
        detalhes = "; ".join(item["problema"] for item in laudo["findings"][:4])
        raise ForjaN3Error(
            f"definição reprovada na recomputação ({', '.join(reprovados)}): {detalhes}")
    result.setdefault("gates", {}).update(laudo["gates"])
    atomic_write_json(attempt_dir / "PHASE_RESULT.json", result)


def _recompute_regimento(contract: dict, artifacts: list[dict], attempt_dir: Path,
                         result: dict) -> None:
    """Computa `tribunal_identified`, `regimento_available` e `critical_facts_sourced` (F3).

    A consideração do regimento do tribunal é regra inviolável da casa desde
    06/07/2026, e o gate que a atestava era escrito pelo agente. A distinção que
    a medição impôs: hash divergente de cópia arquivada é P0, mas hash
    divergente de REGIMENTO é `warn` — o protocolo manda anexar as emendas
    posteriores ao próprio arquivo antes de cada peça, então divergir com o
    tempo é o protocolo funcionando, não defeito.
    """
    if contract["phase"] != "F3_FONTES_REGIMENTO_LEIS":
        return
    from forja_regimento_gate import validar_regimento

    por_id = {item["artifactId"]: item["source"] for item in artifacts}
    mapa = _read_gate_artifact(por_id.get("sources_map"))
    ledger = _read_gate_artifact(por_id.get("fact_ledger"))

    laudo = validar_regimento(mapa or {}, ledger or {})
    # A auditoria adversarial nasce na F3 e é decidida na F4; aqui se confere o
    # escopo classificado e a substância do exame.
    from forja_adversarial_gate import validar_auditoria_adversarial

    caminho_auditoria = por_id.get("adversarial_audit")
    adversarial = validar_auditoria_adversarial(
        read_json(caminho_auditoria, {}) if caminho_auditoria else {}, {}, caminho_auditoria)
    for nome in ("adversarial_scope_classified", "adversarial_audit_complete"):
        laudo["gates"][nome] = adversarial["gates"][nome]
    laudo["findings"].extend(adversarial["findings"])

    atomic_write_json(attempt_dir / "COMPUTED_REGIMENTO_GATES.json", laudo)
    result["computedRegimentoGates"] = laudo["gates"]
    reprovados = [nome for nome, valor in laudo["gates"].items() if valor == "fail"]
    if reprovados:
        detalhes = "; ".join(item["problema"] for item in laudo["findings"][:4])
        raise ForjaN3Error(
            f"fontes e regimento reprovados na recomputação ({', '.join(reprovados)}): {detalhes}")
    result.setdefault("gates", {}).update(laudo["gates"])
    atomic_write_json(attempt_dir / "PHASE_RESULT.json", result)


def _recompute_contexto(contract: dict, artifacts: list[dict], attempt_dir: Path,
                        result: dict) -> None:
    """Computa `facts_rechecked` e `context_complete` (F7).

    Não há como recomputar de fora se cada fato foi reconferido na fonte — isso
    é leitura humana. O que se computa é a **contradição interna**: artefato que
    declara não ter reconferido enquanto a fase reporta o gate aprovado; hash do
    texto auditado que aponta para outra versão; e questão material pendente ao
    lado de liberação externa aprovada. Essa última combinação não existe no
    acervo — os três casos com pendência negam o release —, e é justamente por
    isso que ela merece um gate: nenhum revisor apressado a pega.
    """
    if contract["phase"] != "F7_AUDITORIA_JURIDICA_FACTUAL":
        return
    from forja_contexto import validar_contexto

    por_id = {item["artifactId"]: item["source"] for item in artifacts}
    validacao = read_json(por_id.get("context_validation"), {}) \
        if por_id.get("context_validation") else {}
    gate_result = read_json(por_id.get("f7_gate_result"), {}) \
        if por_id.get("f7_gate_result") else {}

    texto = None
    for chave in ("audited_markdown", "final_markdown"):
        caminho = por_id.get(chave)
        if caminho and caminho.is_file():
            texto = caminho.read_text(encoding="utf-8", errors="replace")
            break

    laudo = validar_contexto(validacao or {}, gate_result or {}, texto)
    # `p0_zero` é o gate central da F7 e era aritmética escrita à mão;
    # `producer_reviewer_separation` já era conferido por `_validate_result`
    # desde antes desta frente, só nunca tinha recebido o nome.
    from forja_p0 import validar_p0

    contagem = validar_p0(gate_result or {},
                          produtor=result.get("producer"),
                          revisor=result.get("reviewer"))
    laudo["findings"].extend(contagem["findings"])
    laudo["gates"].update(contagem["gates"])

    atomic_write_json(attempt_dir / "COMPUTED_CONTEXTO_GATES.json", laudo)
    result["computedContextoGates"] = laudo["gates"]
    reprovados = [nome for nome, valor in laudo["gates"].items() if valor == "fail"]
    if reprovados:
        detalhes = "; ".join(item["problema"] for item in laudo["findings"][:4])
        raise ForjaN3Error(
            f"contexto reprovado na recomputação ({', '.join(reprovados)}): {detalhes}")
    result.setdefault("gates", {}).update(laudo["gates"])
    atomic_write_json(attempt_dir / "PHASE_RESULT.json", result)


def _recompute_red_team(contract: dict, artifacts: list[dict], attempt_dir: Path,
                        result: dict) -> None:
    """Computa `red_team_completed` e `adversarial_claims_rechecked` (F7).

    Das oito execuções reais de `adversarial_recheck` medidas em 04/08/2026,
    seis declaram `applicable: false` — e as oito reportaram `pass`. Três
    quartos das execuções do gate mediram o conjunto vazio e chamaram isso de
    aprovação. Aqui, ausência de peça adversária vira `not_applicable`, que
    preserva a diferença entre "nada a examinar" e "examinado e aprovado".
    """
    if contract["phase"] != "F7_AUDITORIA_JURIDICA_FACTUAL":
        return
    from forja_red_team import validar_exame_adversarial

    por_id = {item["artifactId"]: item["source"] for item in artifacts}
    relatorio = None
    caminho = por_id.get("red_team_report")
    if caminho and caminho.is_file():
        relatorio = caminho.read_text(encoding="utf-8", errors="replace")
    caminho = por_id.get("adversarial_recheck")
    recheck = read_json(caminho, {}) if caminho else {}

    laudo = validar_exame_adversarial(relatorio, recheck or {})
    atomic_write_json(attempt_dir / "COMPUTED_RED_TEAM_GATES.json", laudo)
    result["computedRedTeamGates"] = laudo["gates"]
    reprovados = [nome for nome, valor in laudo["gates"].items() if valor == "fail"]
    if reprovados:
        detalhes = "; ".join(item["problema"] for item in laudo["findings"][:4])
        raise ForjaN3Error(
            f"exame adversarial reprovado na recomputação ({', '.join(reprovados)}): {detalhes}")
    result.setdefault("gates", {}).update(laudo["gates"])
    atomic_write_json(attempt_dir / "PHASE_RESULT.json", result)


def _recompute_conselho(contract: dict, artifacts: list[dict], attempt_dir: Path,
                        result: dict) -> None:
    """Computa os gates do conselho da F4 em vez de aceitar o `pass` do agente.

    O conselho Helena + Cícero é obrigatório desde 09/07/2026, e até 04/08 os
    três gates que o atestam eram escritos pelo próprio agente da fase: nove
    execuções, nove `pass`, nenhuma reprovação. Um `pass` falso aqui é peça indo
    para redação sem o conselho que a casa tornou inviolável.
    """
    if contract["phase"] != "F4_BLUEPRINT_ESTRATEGICO":
        return
    from forja_conselho import validar_conselho

    por_id = {item["artifactId"]: item["source"] for item in artifacts}
    laudo = validar_conselho(
        helena=por_id.get("helena_opinion"),
        cicero=por_id.get("cicero_opinion"),
        decisoes=por_id.get("council_decisions"),
    )
    # A estratégia adversarial decide sobre a auditoria da F3 — e declara o hash
    # dela. Se não bater, as decisões foram tomadas sobre outra versão do exame,
    # e nada no artefato denuncia isso.
    from forja_adversarial_gate import validar_auditoria_adversarial

    raiz = _raiz_do_caso(attempt_dir)
    caminho_auditoria = None
    if raiz:
        candidato = raiz / "n3_artifacts" / "F3_FONTES_REGIMENTO_LEIS" / "adversarial_audit.json"
        caminho_auditoria = candidato if candidato.is_file() else None
    adversarial = validar_auditoria_adversarial(
        read_json(caminho_auditoria, {}) if caminho_auditoria else {},
        read_json(por_id.get("adversarial_strategy"), {})
        if por_id.get("adversarial_strategy") else {},
        caminho_auditoria)
    for nome in ("adversarial_decisions_recorded", "bad_faith_language_authorized"):
        laudo["gates"][nome] = adversarial["gates"][nome]
    laudo["findings"] = list(laudo.get("findings") or []) + adversarial["findings"]
    atomic_write_json(attempt_dir / "COMPUTED_CONSELHO_GATES.json", laudo)
    result["computedConselhoGates"] = laudo["gates"]
    reprovados = [nome for nome, valor in laudo["gates"].items() if valor != "pass"]
    if reprovados:
        detalhes = "; ".join(item["problema"] for item in laudo["findings"][:6])
        raise ForjaN3Error(
            f"conselho obrigatório reprovado na recomputação ({', '.join(reprovados)}): {detalhes}")
    # A autoridade passa a ser o cálculo, não o campo escrito pelo produtor.
    result.setdefault("gates", {}).update(laudo["gates"])
    atomic_write_json(attempt_dir / "PHASE_RESULT.json", result)


def _recompute_ingestao(contract: dict, artifacts: list[dict], attempt_dir: Path,
                        result: dict) -> None:
    """Computa `critical_documents_indexed` e `coverage_declared` (F1).

    São os gates mais a montante da esteira: um `pass` falso aqui é peça
    redigida sobre leitura parcial dos autos sem que ninguém saiba. A medição
    do acervo derrubou as regras óbvias — há índice legítimo sem `documents[]`,
    e completude qualificada ao lado de lacuna declarada é honestidade, não
    contradição. O que reprova é hash que não confere e aritmética impossível.
    """
    if contract["phase"] != "F1_INGESTAO_SEGURA":
        return
    from forja_ingestao import validar_ingestao

    por_id = {item["artifactId"]: item["source"] for item in artifacts}
    indice_path = por_id.get("document_index")
    indice = read_json(indice_path, {}) if indice_path else {}
    ledger_path = por_id.get("coverage_ledger")
    ledger = read_json(ledger_path, {}) if ledger_path else {}

    laudo = validar_ingestao(indice or {}, ledger or {},
                             indice_path.parent if indice_path else attempt_dir)
    atomic_write_json(attempt_dir / "COMPUTED_INGESTAO_GATES.json", laudo)
    result["computedIngestaoGates"] = laudo["gates"]
    reprovados = [nome for nome, valor in laudo["gates"].items() if valor == "fail"]
    if reprovados:
        detalhes = "; ".join(item["problema"] for item in laudo["findings"][:4])
        raise ForjaN3Error(
            f"ingestão reprovada na recomputação ({', '.join(reprovados)}): {detalhes}")
    result.setdefault("gates", {}).update(laudo["gates"])
    atomic_write_json(attempt_dir / "PHASE_RESULT.json", result)


def _recompute_exploracao(contract: dict, artifacts: list[dict], attempt_dir: Path,
                          result: dict) -> None:
    """Nomeia como gates da F2 o que `validate_exploration_100` já computava.

    A rota já chamava o validador da exploração de 100 perguntas e derrubava a
    fase quando ele achava algo — mas os três gates que atestam a exploração
    continuavam sendo escritos pelo agente. O gate existia, a capacidade
    existia, e faltava ligar um nome ao outro. Nenhum limiar novo nasce aqui.
    """
    if contract["phase"] != "F2_CLASSIFICACAO_PRODUTO_RISCO":
        return
    from forja_exploracao_100 import gates_da_exploracao

    por_id = {item["artifactId"]: item["source"] for item in artifacts}
    arvore_path = por_id.get("question_tree")
    if not arvore_path:
        return
    arvore = read_json(arvore_path, {}) or {}

    laudo = gates_da_exploracao(arvore, require_protocol=True)
    atomic_write_json(attempt_dir / "COMPUTED_EXPLORACAO_GATES.json",
                      {"versao": laudo["versao"], "gates": laudo["gates"],
                       "codigosNaoMapeados": laudo["codigosNaoMapeados"],
                       "findings": laudo["findings"][:40]})
    result["computedExploracaoGates"] = laudo["gates"]
    reprovados = [nome for nome, valor in laudo["gates"].items() if valor == "fail"]
    if reprovados:
        detalhes = "; ".join(str(item.get("detail") or "") for item in laudo["findings"][:4])
        raise ForjaN3Error(
            f"exploração reprovada na recomputação ({', '.join(reprovados)}): {detalhes}")
    result.setdefault("gates", {}).update(laudo["gates"])
    atomic_write_json(attempt_dir / "PHASE_RESULT.json", result)


def _recompute_pesquisa_oficial(contract: dict, artifacts: list[dict], attempt_dir: Path,
                                result: dict) -> None:
    """Computa `official_sources_archived` e `quotes_compared` (F5).

    A medição do acervo em 04/08/2026 achou um `source_ledger` com dez fontes e
    nenhuma arquivada, reportando `official_sources_archived: pass` — o nome do
    gate era falso no próprio artefato que ele auditava. Só bloqueia o que é
    verificavelmente falso (caminho declarado que não existe, hash que não
    confere); a ausência de arquivamento vira `warn`, porque foi a prática
    corrente da casa e travar a F5 seria pior que registrar o limite.

    `quotes_compared` devolve `not_applicable` quando nenhuma citação textual
    foi usada: aí não há cotejo a fazer, e dizer `pass` seria medir o conjunto
    vazio — a MC-15 no seu estado mais puro.
    """
    if contract["phase"] != "F5_PESQUISA_OFICIAL":
        return
    from forja_fontes_oficiais import validar_pesquisa_oficial

    por_id = {item["artifactId"]: item["source"] for item in artifacts}
    ledger_path = por_id.get("source_ledger")
    ledger = read_json(ledger_path, {}) if ledger_path else {}
    # Sete dos nove `citation_checklist` do acervo são markdown. Passá-los pelo
    # parser JSON devolvia `{}`, o gate `quotes_compared` lia isso como
    # "checklist ausente" e a fase inteira era BLOQUEADA — reprovando uma F5
    # correta por causa da extensão do arquivo. É o modo de falha mais caro que
    # um gate tem, porque ele para trabalho bom.
    checklist = _read_gate_artifact(por_id.get("citation_checklist"))

    laudo = validar_pesquisa_oficial(ledger or {}, checklist or {},
                                     ledger_path.parent if ledger_path else attempt_dir)
    atomic_write_json(attempt_dir / "COMPUTED_FONTES_GATES.json", laudo)
    result["computedFontesGates"] = laudo["gates"]
    reprovados = [nome for nome, valor in laudo["gates"].items() if valor == "fail"]
    if reprovados:
        detalhes = "; ".join(item["problema"] for item in laudo["findings"][:4])
        raise ForjaN3Error(
            f"pesquisa oficial reprovada na recomputação ({', '.join(reprovados)}): {detalhes}")
    result.setdefault("gates", {}).update(laudo["gates"])
    atomic_write_json(attempt_dir / "PHASE_RESULT.json", result)


def _recompute_paragrafos(contract: dict, artifacts: list[dict], attempt_dir: Path,
                          result: dict) -> None:
    """Computa `paragraphs_sourced` em vez de aceitar o `pass` do agente.

    Oito execuções, oito `pass`, nenhuma reprovação até 04/08/2026. É o gate que
    responde à pergunta que decide se a peça é protocolável — cada parágrafo
    afirma algo que os autos sustentam? — e um `pass` falso é o modo de falha do
    incidente CASO-23: texto bem escrito, lastro aparente, proposição sem
    âncora. O veredito `warn` existe para o dialeto que não declara hash, trecho
    nem numeração de linha: aí a cobertura não é conferível, e o gate diz isso em
    vez de aprovar.
    """
    if contract["phase"] != "F6_REDACAO_TEMPLATE":
        return
    from forja_paragrafos import validar_paragrafos_lastreados

    por_id = {item["artifactId"]: item["source"] for item in artifacts}
    caminho = por_id.get("paragraph_provenance")
    prov = read_json(caminho, {}) if caminho else {}
    if isinstance(prov, dict) and isinstance(prov.get("main"), dict):
        prov = prov["main"]

    texto = None
    rascunho = por_id.get("draft_markdown")
    if rascunho and rascunho.is_file():
        texto = rascunho.read_text(encoding="utf-8", errors="replace")

    laudo = validar_paragrafos_lastreados(prov or {}, texto)
    # Os detectores de voz humana e de origem operacional existiam desde sempre,
    # instalados só na F7-B — onde acusar custa um ciclo inteiro de reescrita.
    # Aqui eles rodam sobre o rascunho. Medido contra os treze rascunhos reais:
    # zero achado, ou seja, antecipá-los não trava ninguém.
    from forja_redacao import validar_redacao

    redacao = validar_redacao(prov or {}, texto)
    laudo["findings"].extend(redacao["findings"])
    laudo["gates"].update(redacao["gates"])

    atomic_write_json(attempt_dir / "COMPUTED_PARAGRAFOS_GATES.json", laudo)
    result["computedParagrafosGates"] = laudo["gates"]
    reprovados = [nome for nome, valor in laudo["gates"].items() if valor == "fail"]
    if reprovados:
        detalhes = "; ".join(item["problema"] for item in laudo["findings"][:4])
        raise ForjaN3Error(
            f"redação reprovada na recomputação ({', '.join(reprovados)}): {detalhes}")
    result.setdefault("gates", {}).update(laudo["gates"])
    atomic_write_json(attempt_dir / "PHASE_RESULT.json", result)


def _validate_result(attempt_dir: Path, contract: dict) -> tuple[dict, list[dict]]:
    result_path = attempt_dir / "PHASE_RESULT.json"
    result = read_json(result_path, None)
    if not isinstance(result, dict):
        raise ForjaN3Error(f"resultado ausente ou inválido: {result_path}")
    if result.get("status") != "pass":
        raise ForjaN3Error(f"fase não aprovada: {result.get('status') or 'sem status'}")
    if result.get("producer") == result.get("reviewer"):
        raise ForjaN3Error("produtor e revisor da fase não podem ser a mesma execução")
    if result.get("producerRole") != contract["producerRole"] or result.get("reviewerRole") != contract["reviewerRole"]:
        raise ForjaN3Error("papéis do resultado divergem do contrato")
    gates = result.get("gates") or {}
    failed = [
        name for name in contract["requiredGates"]
        if not any(gates.get(alias) == "pass" for alias in name_with_legacy(name))
    ]
    if failed:
        raise ForjaN3Error(f"gates não aprovados: {', '.join(failed)}")
    artifacts = result.get("artifacts") or []
    by_id = {str(item.get("id") or ""): item for item in artifacts if isinstance(item, dict)}
    if len(by_id) != len(artifacts):
        raise ForjaN3Error("IDs de artefatos ausentes ou duplicados")
    missing = [item for item in contract["requiredOutputs"] if resolve_name(item, by_id) is None]
    if missing:
        raise ForjaN3Error(f"saídas obrigatórias ausentes: {', '.join(missing)}")
    validated = []
    for artifact_id, entry in by_id.items():
        relative = Path(str(entry.get("path") or ""))
        if relative.is_absolute():
            raise ForjaN3Error(f"artefato deve usar caminho relativo: {artifact_id}")
        source = ensure_within(attempt_dir / relative, attempt_dir)
        if not source.is_file():
            raise ForjaN3Error(f"arquivo do artefato ausente: {source}")
        if artifact_id == "question_tree":
            question_tree = read_json(source, None)
            if not isinstance(question_tree, dict):
                raise ForjaN3Error("question_tree deve ser JSON válido")
            exploration_findings = validate_exploration_100(question_tree, require_protocol=True)
            blocking = blocking_findings(exploration_findings)
            if blocking:
                details = "; ".join(item["detail"] for item in blocking[:8])
                remaining = len(blocking) - 8
                if remaining > 0:
                    details += f"; e mais {remaining} achado(s)"
                raise ForjaN3Error("exploração F2-A reprovada: " + details)
        validated.append({
            "artifactId": artifact_id,
            "source": source,
            "role": entry.get("role") or "phase_output",
            "audience": entry.get("audience") or "internal_working",
            "releasePolicy": entry.get("releasePolicy") or "internal_working",
            "sha256": sha256_file(source),
            "size": source.stat().st_size,
        })
    context = read_json(attempt_dir / "RUN_CONTEXT.json", {}) or {}
    _recompute_injecao(contract, validated, attempt_dir, result)
    _recompute_ingestao(contract, validated, attempt_dir, result)
    _recompute_exploracao(contract, validated, attempt_dir, result)
    _recompute_regimento(contract, validated, attempt_dir, result)
    _recompute_definicao(contract, validated, attempt_dir, result)
    _recompute_conselho(contract, validated, attempt_dir, result)
    _recompute_pesquisa_oficial(contract, validated, attempt_dir, result)
    _recompute_paragrafos(contract, validated, attempt_dir, result)
    _recompute_contexto(contract, validated, attempt_dir, result)
    _recompute_red_team(contract, validated, attempt_dir, result)
    _recompute_politica_citacoes(contract, validated, attempt_dir, result)
    lastro_report = _compute_lastro_gates(contract["phase"], validated, context)
    if lastro_report.get("applicable"):
        atomic_write_json(attempt_dir / "COMPUTED_LASTRO_GATES.json", lastro_report)
        result["computedLastroGates"] = lastro_report["computed"]
        # L1/L2/L7 e os gates econômicos são calculados pelo runner. Um valor
        # declarado pelo agente não pode transformá-los em verde.
        if lastro_report["findings"]:
            p0 = [item for item in lastro_report["findings"] if item.get("sev") == "P0"]
            if (p0 or lastro_report["computed"].get("fact_grounding_verbatim") != "pass"
                    or lastro_report["computed"].get("economic_gates") == "fail"):
                detalhes = "; ".join(item["problema"] for item in lastro_report["findings"][:8])
                raise ForjaN3Error("lastro documental computado reprovado: " + detalhes)
        if "fact_grounding_verbatim" in contract["requiredGates"] and result["computedLastroGates"].get("fact_grounding_verbatim") != "pass":
            raise ForjaN3Error("fact_grounding_verbatim não passou na recomputação do runner")
        if "fact_grounding_verbatim" in contract["requiredGates"]:
            # Remove a possibilidade de o agente declarar pass sem a prova
            # independente. A exigência abaixo é a mesma, mas a autoridade é
            # o resultado computado, não o campo escrito pelo produtor.
            result.setdefault("gates", {})["fact_grounding_verbatim"] = "pass"
            atomic_write_json(attempt_dir / "PHASE_RESULT.json", result)
    # A declaração do agente foi conferida no início, mas os recomputos acima
    # podem transformar um `pass` autodeclarado em `warn` ou `fail`. Gate
    # obrigatório só autoriza promoção quando a prova independente também é
    # `pass`; `warn` continua visível no laudo, mas não atravessa a fase.
    recomputed_failed = [
        name for name in contract["requiredGates"]
        if not any((result.get("gates") or {}).get(alias) == "pass"
                   for alias in name_with_legacy(name))
    ]
    if recomputed_failed:
        raise ForjaN3Error(
            "gates não aprovados após recomputação: " + ", ".join(recomputed_failed))
    adversarial_findings = validate_phase_artifacts(
        contract["phase"],
        {item["artifactId"]: item["source"] for item in validated},
        context.get("inputs") or {},
    )
    if adversarial_findings:
        raise ForjaN3Error("auditoria adversarial reprovada: " + "; ".join(adversarial_findings))
    _validate_fable5_editorial(contract["phase"], validated)
    _validate_f7_source_ledger(contract["phase"], validated)
    _validate_optional_instrumentation(contract["phase"], attempt_dir, result)
    _validate_human_style(contract["phase"], validated)
    return result, validated


def _validate_f7_source_ledger(phase: str, artifacts: list[dict]) -> None:
    """F7 não promove declarações de gate sem refazer a prova contra o texto final."""
    if phase != "F7_AUDITORIA_JURIDICA_FACTUAL":
        return
    from forja_authorities import extract_authorities
    from forja_package import validate_source_ledger

    by_id = {item["artifactId"]: item for item in artifacts}
    final_ids = sorted(
        item for item in by_id
        if item == "final_markdown" or item.startswith("final_markdown_")
    )
    for final_id in final_ids:
        suffix = final_id[len("final_markdown"):]
        ledger_id = f"verified_source_ledger{suffix}"
        if ledger_id not in by_id:
            raise ForjaN3Error(f"ledger probatório final ausente para {final_id}: {ledger_id}")
        final = by_id[final_id]
        ledger = by_id[ledger_id]
        text = final["source"].read_text(encoding="utf-8", errors="replace")
        validation = validate_source_ledger(
            {"path": str(ledger["source"])},
            release_policy="strict_protocol",
            expected_citations=extract_authorities(text),
            markdown={"path": str(final["source"]), "sha256": final["sha256"]},
        )
        if not validation["approved"]:
            raise ForjaN3Error(
                f"ledger probatório F7 reprovado em {final_id}: "
                + "; ".join(validation["blocked"][:10])
            )


def _validate_optional_instrumentation(phase: str, attempt_dir: Path, result: dict) -> None:
    """Audita sidecars do PRD 45 sem transformá-los em gate canônico no piloto."""
    if phase not in {"F5_PESQUISA_OFICIAL", "F7_AUDITORIA_JURIDICA_FACTUAL"}:
        return
    case_dir = attempt_dir.parents[3]
    map_path = case_dir / "instrumentation" / "F5_PROPOSITION_EVIDENCE_MAP.json"
    if not map_path.is_file():
        return
    from forja_proposition_evidence import validate_map

    proposition_path = case_dir / "n3_artifacts" / "F4_BLUEPRINT_ESTRATEGICO" / "proposition_ledger.json"
    source_path = case_dir / "n3_artifacts" / "F5_PESQUISA_OFICIAL" / "source_ledger.json"
    f7_path = case_dir / "n3_artifacts" / "F7_AUDITORIA_JURIDICA_FACTUAL" / "verified_source_ledger.json"
    map_payload = read_json(map_path, {}) or {}
    proposition = read_json(proposition_path, {}) if proposition_path.is_file() else None
    source = read_json(source_path, {}) if source_path.is_file() else None
    f7 = read_json(f7_path, {}) if f7_path.is_file() else None
    findings = validate_map(
        map_payload,
        proposition,
        source,
        f7_source_ledger=f7,
        source_base_dir=source_path.parent if source_path.is_file() else None,
    )
    report = {
        "schemaVersion": 1,
        "phase": phase,
        "mapPath": str(map_path),
        "findings": findings,
        "approvedForObservation": not any(item.get("severity") == "p0" for item in findings),
        "pilotPolicy": "instrumentation_findings_do_not_block_canonical_phase",
    }
    atomic_write_json(attempt_dir / "COMPUTED_EVIDENCE_BRIDGE.json", report)
    result["computedEvidenceBridge"] = report


def _validate_fable5_editorial(phase: str, artifacts: list[dict]) -> None:
    """Recomputa os gates F7-B; a declaração do modelo editorial nunca basta."""
    if phase != "F7_AUDITORIA_JURIDICA_FACTUAL":
        return
    by_id = {item["artifactId"]: item for item in artifacts}
    required = ("audited_markdown", "final_markdown", "editorial_report", "editor_usage")
    if any(resolve_name(item, by_id) is None for item in required):
        return  # o contrato relata as saídas ausentes antes deste ponto
    final_ids = sorted(item for item in by_id if item == "final_markdown" or item.startswith("final_markdown_"))
    for final_id in final_ids:
        suffix = final_id[len("final_markdown"):]
        paired = {
            "audited": resolve_name(f"audited_markdown{suffix}", by_id),
            "report": resolve_name(f"editorial_report{suffix}", by_id),
            "usage": resolve_name(f"editor_usage{suffix}", by_id),
        }
        missing = [f"{papel}{suffix}" for papel, value in paired.items() if value is None]
        if missing:
            raise ForjaN3Error(
                f"bundle editorial incompleto para {final_id}: {', '.join(missing)}"
            )
        validation = validate_editorial_bundle(
            by_id[paired["audited"]]["source"],
            by_id[final_id]["source"],
            by_id[paired["report"]]["source"],
            by_id[paired["usage"]]["source"],
        )
        if not validation["approved"]:
            details = "; ".join(item["detail"] for item in validation["findings"][:8])
            remaining = len(validation["findings"]) - 8
            if remaining > 0:
                details += f"; e mais {remaining} achado(s)"
            raise ForjaN3Error(f"gate editorial Fable 5 reprovado em {final_id}: " + details)


def _validate_human_style(phase: str, artifacts: list[dict]) -> None:
    """Recomputa o gate no texto real; o agente não pode aprová-lo por declaração."""
    alvo_por_fase = {
        "F6_REDACAO_TEMPLATE": "draft_markdown",
        "F7_AUDITORIA_JURIDICA_FACTUAL": "final_markdown",
    }
    alvo = alvo_por_fase.get(phase)
    if not alvo:
        return
    artefato = next((item for item in artifacts if item["artifactId"] == alvo), None)
    if not artefato:
        return  # a ausência já é tratada pelo contrato antes deste ponto
    from forja_estilo_humano import analisar
    texto = artefato["source"].read_text(encoding="utf-8", errors="replace")
    p0 = [item for item in analisar(texto, "peca") if item["sev"] == "P0"]
    if p0:
        detalhes = "; ".join(
            f"{item['gate']}: {item['problema']} [{item['trecho'][:120]}]" for item in p0[:6]
        )
        restante = len(p0) - 6
        if restante > 0:
            detalhes += f"; e mais {restante} achado(s)"
        raise ForjaN3Error("gate de escrita humana reprovado: " + detalhes)


def _promote_file(case_dir: Path, phase: str, artifact: dict) -> Path:
    source = artifact["source"]
    safe_id = "".join(char if char.isalnum() or char in "-_" else "_" for char in artifact["artifactId"])
    suffix = source.suffix or ".bin"
    n4_filename = next(
        (filename for filename, spec in ARTIFACT_SPECS.items() if spec["type"] == artifact["artifactId"]),
        None,
    )
    destination_dir = case_dir / "n4_artifacts" if n4_filename else case_dir / "n3_artifacts" / phase
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / n4_filename if n4_filename else destination_dir / f"{safe_id}{suffix}"
    replace_existing = False
    if destination.exists() and sha256_file(destination) != artifact["sha256"]:
        if n4_filename:
            previous_hash = sha256_file(destination)
            history = destination_dir / "history"
            history.mkdir(parents=True, exist_ok=True)
            archived = history / f"{destination.stem}-{previous_hash[:12]}{destination.suffix}"
            if not archived.exists():
                shutil.copy2(destination, archived)
            replace_existing = True
        else:
            destination = destination_dir / f"{safe_id}-{artifact['sha256'][:12]}{suffix}"
    if not destination.exists() or replace_existing:
        fd, temp_name = tempfile.mkstemp(prefix=f".{safe_id}.", suffix=".tmp", dir=destination_dir)
        os.close(fd)
        temp_path = Path(temp_name)
        try:
            shutil.copy2(source, temp_path)
            if sha256_file(temp_path) != artifact["sha256"]:
                raise ForjaN3Error(f"hash mudou durante promoção: {artifact['artifactId']}")
            os.replace(temp_path, destination)
        finally:
            temp_path.unlink(missing_ok=True)
    return destination


def promote_attempt(case_dir: Path, attempt_dir: Path, *, expected_revision: int, actor: str = "forja-runner") -> dict:
    attempt_dir = ensure_within(attempt_dir, case_dir / "runs")
    context = read_json(attempt_dir / "RUN_CONTEXT.json", None)
    if not isinstance(context, dict):
        raise ForjaN3Error("RUN_CONTEXT.json ausente")
    contract = load_contract(context["phase"])
    if context.get("contract", {}).get("contractHash") != contract["contractHash"]:
        raise ForjaN3Error("contrato mudou desde o início da tentativa")
    result, artifacts = _validate_result(attempt_dir, contract)
    state = derive_state(case_dir)
    if state["revision"] != expected_revision:
        raise ForjaN3Error(f"revisão mudou antes da promoção: {state['revision']}")
    revision = expected_revision
    promoted = {}
    for artifact in artifacts:
        destination = _promote_file(case_dir, contract["phase"], artifact)
        payload = {
            "artifactId": artifact["artifactId"],
            "artifact": {
                "path": str(destination),
                "sha256": artifact["sha256"],
                "size": artifact["size"],
                "role": artifact["role"],
                "audience": artifact["audience"],
                "releasePolicy": artifact["releasePolicy"],
                "runId": context["runId"],
                "attemptId": context["attemptId"],
            },
        }
        _, state, _ = record_event(
            case_dir,
            "artifact_promoted",
            expected_revision=revision,
            idempotency_key=f"{context['attemptId']}:{artifact['artifactId']}:promoted:{artifact['sha256']}",
            phase=contract["phase"],
            actor=actor,
            run_id=context["runId"],
            attempt_id=context["attemptId"],
            artifact_hashes={artifact["artifactId"]: artifact["sha256"]},
            payload=payload,
        )
        revision = state["revision"]
        promoted[artifact["artifactId"]] = payload["artifact"]
    from forja_n4_validate import validate_case as validate_n4

    n4 = validate_n4(case_dir, target_phase=contract["phase"])
    if n4.get("blocksCurrentFlow"):
        blockers = [item["detail"] for item in n4.get("findings") or [] if item.get("severity") == "p0"]
        _, state, _ = record_event(
            case_dir,
            "phase_blocked",
            expected_revision=revision,
            idempotency_key=f"{context['attemptId']}:{contract['phase']}:n4-blocked:{n4['validationHash']}",
            phase=contract["phase"],
            actor=actor,
            run_id=context["runId"],
            attempt_id=context["attemptId"],
            payload={"reason": "gate N4 bloqueante", "blockers": blockers},
        )
        raise ForjaN3Error("gate N4 bloqueante: " + "; ".join(blockers))
    _, state, _ = record_event(
        case_dir,
        "phase_completed",
        expected_revision=revision,
        idempotency_key=f"{context['attemptId']}:{contract['phase']}:completed",
        phase=contract["phase"],
        actor=actor,
        run_id=context["runId"],
        attempt_id=context["attemptId"],
        artifact_hashes={key: value["sha256"] for key, value in promoted.items()},
        payload={"result": "pass", "gates": result.get("gates") or {}, "contractHash": contract["contractHash"]},
    )
    return {"state": state, "promoted": promoted, "n4": n4}


def block_phase(case_dir: Path, phase: str, *, expected_revision: int, reason: str, blockers: list[str]) -> dict:
    _, state, _ = record_event(
        case_dir,
        "phase_blocked",
        expected_revision=expected_revision,
        idempotency_key=f"{case_dir.name}:{phase}:blocked:{canonical_hash([reason, blockers])}",
        phase=phase,
        payload={"reason": reason, "blockers": blockers},
    )
    return state


def main() -> None:
    parser = argparse.ArgumentParser(description="Executor canônico e retomável FORJA N3")
    parser.add_argument("case")
    sub = parser.add_subparsers(dest="command", required=True)
    start = sub.add_parser("start")
    start.add_argument("phase")
    start.add_argument("--expected-revision", type=int, required=True)
    start.add_argument("--run-id")
    promote = sub.add_parser("promote")
    promote.add_argument("attempt_dir", type=Path)
    promote.add_argument("--expected-revision", type=int, required=True)
    block = sub.add_parser("block")
    block.add_argument("phase")
    block.add_argument("--expected-revision", type=int, required=True)
    block.add_argument("--reason", required=True)
    block.add_argument("--blocker", action="append", default=[])
    args = parser.parse_args()
    case_dir = resolve_case_dir(args.case)
    if args.command == "start":
        result = prepare_attempt(case_dir, args.phase, expected_revision=args.expected_revision, run_id=args.run_id)
    elif args.command == "promote":
        result = promote_attempt(case_dir, args.attempt_dir, expected_revision=args.expected_revision)
    else:
        result = block_phase(case_dir, args.phase, expected_revision=args.expected_revision, reason=args.reason, blockers=args.blocker)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
