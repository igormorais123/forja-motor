# -*- coding: utf-8 -*-
"""forja_recomputo_censo.py — os recomputos disparam em caso real?

A lição 3 do plano visual diz que gate instalado na rota que ninguém percorre é
gate nenhum — e o elo 4-B rodou três vezes na história inteira. Esta frente
construiu treze recomputos em um dia, e seria ingênuo supor que estão imunes à
mesma doença só porque têm regressão verde. Regressão prova que a função
funciona; não prova que ela é chamada sobre material real.

Este censo executa cada produtor contra as tentativas REAIS do acervo e conta
quantos vereditos cada gate produziu, por fase. Um gate com zero vereditos aqui
está numa das duas situações:

  - o artefato de que ele depende nunca existiu com aquele nome (MC-15 do lado
    do produtor: o gate procura o que ninguém emite);
  - a fase nunca rodou no acervo, e então o número é honesto e diz só isso.

A diferença entre as duas está no relatório: o censo mostra quantas tentativas
daquela fase existem. Zero veredito com dez tentativas é defeito. Zero veredito
com zero tentativas é aritmética.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

VERSAO = "FORJA-RECOMPUTO-CENSO-v1"
RAIZ = Path(__file__).resolve().parent


def _ler(caminho) -> dict:
    alvo = Path(caminho)
    if not alvo.is_file():
        return {}
    try:
        dados = json.loads(alvo.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}
    if isinstance(dados, dict) and isinstance(dados.get("main"), dict):
        return dados["main"]
    return dados if isinstance(dados, dict) else {}


def _texto(caminho) -> str | None:
    alvo = Path(caminho)
    if not alvo.is_file():
        return None
    return alvo.read_text(encoding="utf-8", errors="replace")


def _artefatos_da_tentativa(pasta: Path, resultado: dict) -> list[dict]:
    """Resolve os artefatos declarados no PHASE_RESULT para a forma do runner."""
    saida = []
    for item in resultado.get("artifacts") or []:
        if not isinstance(item, dict):
            continue
        artifact_id = item.get("id") or item.get("artifactId")
        valor = item.get("path") or item.get("source")
        if not artifact_id or not valor:
            continue
        caminho = Path(str(valor))
        if not caminho.is_absolute():
            caminho = pasta / caminho
        if caminho.is_file():
            saida.append({"artifactId": str(artifact_id), "source": caminho})
    return saida


def _raiz_do_caso(pasta: Path) -> Path | None:
    for pai in pasta.resolve().parents:
        if (pai / "n3_artifacts").is_dir():
            return pai
    return None


def _irmao_promovido(pasta: Path, fase: str, nome: str) -> Path | None:
    """Artefato de OUTRA fase, no material promovido do mesmo caso.

    Existe porque o censo repetiu, contra si mesmo, o erro que esta frente já
    tinha documentado: parear a auditoria adversarial (F3) com uma estratégia
    (F4) achada por varredura produz `fail` de hash que não existe. Artefato de
    fase diferente se busca pelo caso, nunca pela pasta ao lado.
    """
    raiz = _raiz_do_caso(pasta)
    if not raiz:
        return None
    candidato = raiz / "n3_artifacts" / fase / nome
    return candidato if candidato.is_file() else None


def _produtores(pasta: Path, resultado: dict | None = None) -> list:
    """Cada produtor, aplicado ao material que existir na pasta da tentativa."""
    saida = []
    resultado = resultado or {}

    from forja_injection_scan import validar_triagem_injecao
    from forja_ingestao import validar_ingestao
    from forja_exploracao_100 import gates_da_exploracao
    from forja_produto import (validar_definicao_produto, validar_pergunta_jurisdicional,
                               validar_uso_final)
    from forja_regimento_gate import validar_regimento
    from forja_adversarial_gate import validar_auditoria_adversarial, validar_politica_liberacao
    from forja_conselho import validar_conselho
    from forja_fontes_oficiais import validar_pesquisa_oficial
    from forja_paragrafos import validar_paragrafos_lastreados
    from forja_redacao import validar_redacao
    from forja_contexto import validar_contexto
    from forja_red_team import validar_exame_adversarial
    from forja_p0 import validar_p0
    from forja_replay import validar_replay
    from forja_entrega import validar_reconciliacao, validar_pacote

    if (pasta / "injection_scan.json").is_file():
        saida.append(validar_triagem_injecao(_ler(pasta / "injection_scan.json")))
    if (pasta / "document_index.json").is_file() or (pasta / "coverage_ledger.json").is_file():
        saida.append(validar_ingestao(_ler(pasta / "document_index.json"),
                                      _ler(pasta / "coverage_ledger.json"), pasta))
    if (pasta / "question_tree.json").is_file():
        saida.append(gates_da_exploracao(_ler(pasta / "question_tree.json")))
    if (pasta / "product_classification.json").is_file():
        saida.append(validar_definicao_produto(_ler(pasta / "product_classification.json")))
    for nome in ("blueprint.json", "blueprint.md"):
        if (pasta / nome).is_file():
            conteudo = _texto(pasta / nome) if nome.endswith(".md") else _ler(pasta / nome)
            saida.append(validar_pergunta_jurisdicional(conteudo))
            break
    # Os dois artefatos da F3 existem em JSON e em markdown; o Vale Trading só
    # tem o mapa em markdown e o Nylton só tem o ledger assim.
    mapa = (_ler(pasta / "sources_map.json") if (pasta / "sources_map.json").is_file()
            else _texto(pasta / "sources_map.md"))
    ledger_fatos = (_ler(pasta / "fact_ledger.json") if (pasta / "fact_ledger.json").is_file()
                    else _texto(pasta / "fact_ledger.md"))
    if mapa:
        saida.append(validar_regimento(mapa, ledger_fatos))
    if (pasta / "adversarial_audit.json").is_file():
        estrategia = pasta / "adversarial_strategy.json"
        if not estrategia.is_file():
            estrategia = _irmao_promovido(pasta, "F4_BLUEPRINT_ESTRATEGICO",
                                          "adversarial_strategy.json")
        # Sem a estratégia do caso não há o que conferir: medir aqui produziria
        # `fail` de artefato ausente, não de defeito.
        #
        # E só vale confrontar a estratégia PROMOVIDA com a auditoria que foi
        # promovida junto. Uma tentativa descartada tem hash diferente por
        # definição — foi descartada —, e pareá-la com a estratégia vigente
        # acusa de "decisões tomadas sobre outra versão do exame" um caso onde
        # o par promovido confere. Aconteceu com o Cafelana em 04/08/2026: era
        # a segunda vez que este censo inventava um `fail` de hash por parear
        # errado, e a primeira já estava documentada em `_irmao_promovido`.
        if estrategia and not (pasta / "adversarial_strategy.json").is_file():
            promovida = _irmao_promovido(pasta, "F3_FONTES_REGIMENTO_LEIS",
                                         "adversarial_audit.json")
            if promovida and promovida.read_bytes() != (pasta / "adversarial_audit.json").read_bytes():
                estrategia = None
        if estrategia:
            saida.append(validar_auditoria_adversarial(
                _ler(pasta / "adversarial_audit.json"), _ler(estrategia),
                pasta / "adversarial_audit.json"))
    if (pasta / "helena_opinion.md").is_file() or (pasta / "cicero_opinion.md").is_file():
        saida.append(validar_conselho(
            helena=pasta / "helena_opinion.md" if (pasta / "helena_opinion.md").is_file() else None,
            cicero=pasta / "cicero_opinion.md" if (pasta / "cicero_opinion.md").is_file() else None,
            decisoes=next((pasta / n for n in ("council_decisions.md", "council_decisions.json")
                           if (pasta / n).is_file()), None)))
    if (pasta / "source_ledger.json").is_file():
        # `quotes_compared` só é aferível onde a F5 emitiu o checklist. Rodá-lo
        # sobre pasta que só tem o ledger mede a ausência do artefato, não o
        # cotejo — e foi o que produziu sete `fail` no primeiro censo.
        # Sete dos nove checklists do acervo são markdown; ler só o JSON deixava
        # `quotes_compared` sem veredito na maioria das tentativas.
        checklist = (_texto(pasta / "citation_checklist.md")
                     or (_ler(pasta / "citation_checklist.json")
                         if (pasta / "citation_checklist.json").is_file() else None))
        if checklist:
            saida.append(validar_pesquisa_oficial(_ler(pasta / "source_ledger.json"),
                                                  checklist, pasta))
        else:
            from forja_fontes_oficiais import validar_fontes_arquivadas
            saida.append(validar_fontes_arquivadas(_ler(pasta / "source_ledger.json"), pasta))
        saida.append(validar_uso_final(_ler(pasta / "source_ledger.json")))
    if (pasta / "paragraph_provenance.json").is_file():
        prov = _ler(pasta / "paragraph_provenance.json")
        rascunho = _texto(pasta / "draft_markdown.md")
        saida.append(validar_paragrafos_lastreados(prov, rascunho))
        saida.append(validar_redacao(prov, rascunho))
    if (pasta / "context_validation.json").is_file():
        auditado = _texto(pasta / "audited_markdown.md") or _texto(pasta / "final_markdown.md")
        saida.append(validar_contexto(_ler(pasta / "context_validation.json"),
                                      _ler(pasta / "f7_gate_result.json"), auditado))
    if (pasta / "red_team_report.md").is_file() or (pasta / "adversarial_recheck.json").is_file():
        saida.append(validar_exame_adversarial(_texto(pasta / "red_team_report.md"),
                                               _ler(pasta / "adversarial_recheck.json")))
    if (pasta / "f7_gate_result.json").is_file():
        saida.append(validar_p0(_ler(pasta / "f7_gate_result.json"),
                                produtor=resultado.get("producer"),
                                revisor=resultado.get("reviewer")))
    # A F7 não copia necessariamente o fact_ledger para sua tentativa: o
    # runner resolve o ledger promovido pela F3. O censo precisa exercitar a
    # mesma rota de produção, ou a ausência de arquivo local vira silêncio e
    # `fact_grounding_verbatim` parece não existir no acervo. Reutilizar o
    # recomputo canônico também evita que o medidor desenvolva uma segunda
    # interpretação do lastro.
    if resultado.get("phase") == "F7_AUDITORIA_JURIDICA_FACTUAL":
        from forja_run import _compute_lastro_gates
        contexto = _ler(pasta / "RUN_CONTEXT.json")
        lastro = _compute_lastro_gates(
            resultado.get("phase"), _artefatos_da_tentativa(pasta, resultado), contexto)
        computed = lastro.get("computed") or {}
        gates = {nome: computed[nome] for nome in (
            "fact_grounding_verbatim", "criterio_vigente", "economic_gates")
            if nome in computed}
        if gates:
            saida.append({"gates": gates, "findings": lastro.get("findings") or []})

    if (pasta / "verified_source_ledger.json").is_file():
        saida.append(validar_replay(_ler(pasta / "verified_source_ledger.json")))
    # F8 fica DELIBERADAMENTE fora do censo, e o motivo é um achado, não uma
    # omissão. Os dezesseis gates da fase são produzidos por `forja_f8_contract`,
    # que despacha entre a rota estática (regime vigente desde 30/07/2026) e a
    # rota legada por PDF. Nenhum dos quatro ledgers visuais do acervo declara
    # `mode: static_ooxml_svg`: são todos anteriores ao regime. Forçar a rota
    # estática sobre eles produziria vereditos sobre uma premissa que o artefato
    # não sustenta — número inventado com cara de medição.
    #
    # A consequência precisa ser dita em voz alta: os dezesseis gates da F8
    # nunca produziram veredito sobre material real. Isso importa diretamente
    # para a decisão de tornar o F8-S bloqueante, porque é a lição 3 do plano
    # visual — gate instalado na rota que ninguém percorre é gate nenhum — a
    # respeito justamente da fase que se pretende tornar bloqueante.

    if (pasta / "case_manifest.json").is_file():
        # O relatório é markdown no acervo inteiro; passar só o JSON inexistente
        # deixava `status_consistent` preso em `warn` para sempre.
        relatorio = (_texto(pasta / "reconciliation_report.md")
                     or _ler(pasta / "reconciliation_report.json"))
        saida.append(validar_reconciliacao(_ler(pasta / "case_manifest.json"), relatorio))
    # O manifesto do pacote quase nunca se chama `package_manifest.json`. A única
    # execução real de F9 do acervo registra o id `package_manifest` apontando
    # para `PACKAGE_DEFINITION_NYLTON_V1.json`, e procurar pelo nome literal fazia
    # os cinco gates da F9 nunca produzirem veredito — lidos como "sem material"
    # quando o material existia. É a mesma MC-15 pela porta dos fundos que o
    # `reconciliation_report` e o `citation_checklist` já tinham exibido: o gate
    # abre a FORMA errada do artefato e o silêncio é lido como conferência.
    por_id = {a["artifactId"]: a["source"]
              for a in _artefatos_da_tentativa(pasta, resultado or {})}
    manifesto_path = por_id.get("package_manifest")
    if manifesto_path is None and (pasta / "package_manifest.json").is_file():
        manifesto_path = pasta / "package_manifest.json"
    if manifesto_path is not None:
        manifesto = _ler(manifesto_path)
        email = por_id.get("email_response")
        corpo = (_texto(email) if email else None) or _texto(pasta / "email_response.md")
        saida.append(validar_pacote(manifesto, corpo, pasta))
        gate_f7 = por_id.get("f7_gate_result") or (pasta / "f7_gate_result.json")
        saida.append(validar_politica_liberacao(manifesto, _ler(gate_f7)))
    return saida


def censo(raiz=None) -> dict:
    base = Path(raiz) if raiz else (RAIZ / "state")
    vereditos: dict = defaultdict(lambda: defaultdict(int))
    tentativas_por_fase: dict = defaultdict(int)
    pastas = 0
    erros = []

    vistas = set()
    for resultado in base.rglob("PHASE_RESULT.json"):
        pasta = resultado.parent
        if pasta in vistas:
            continue
        vistas.add(pasta)
        dados = _ler(resultado)
        fase = str(dados.get("phase") or pasta.parent.name)
        tentativas_por_fase[fase] += 1
        pastas += 1
        try:
            for laudo in _produtores(pasta, dados):
                for gate, veredito in (laudo.get("gates") or {}).items():
                    vereditos[gate][veredito] += 1
        except Exception as erro:  # noqa: BLE001
            erros.append(f"{pasta}: {type(erro).__name__}: {erro}")

    return {
        "versao": VERSAO,
        "tentativasExaminadas": pastas,
        "tentativasPorFase": dict(sorted(tentativas_por_fase.items())),
        "vereditosPorGate": {g: dict(sorted(v.items())) for g, v in sorted(vereditos.items())},
        "gatesQueProduziramVeredito": len(vereditos),
        "erros": erros,
    }


def _relatar(laudo: dict) -> None:
    print("=" * 74)
    print("CENSO DE DISPARO DOS RECOMPUTOS — sobre tentativas reais do acervo")
    print("=" * 74)
    print(f"  tentativas examinadas    : {laudo['tentativasExaminadas']}")
    print(f"  gates com veredito real  : {laudo['gatesQueProduziramVeredito']}")
    if laudo["erros"]:
        print(f"\n  ERROS ({len(laudo['erros'])})")
        for erro in laudo["erros"][:8]:
            print(f"    {erro[:150]}")

    print("\n  VEREDITOS POR GATE")
    for gate, contagem in laudo["vereditosPorGate"].items():
        resumo = " ".join(f"{k}={v}" for k, v in contagem.items())
        marca = "  " if contagem.get("fail") or contagem.get("warn") else "· "
        print(f"    {marca}{gate:52} {resumo}")

    complacentes = [g for g, c in laudo["vereditosPorGate"].items()
                    if set(c) == {"pass"}]
    print(f"\n  Só disseram `pass` no acervo inteiro ({len(complacentes)})")
    print("  Não é defeito por si — é onde ninguém sabe se o gate sabe dizer não.")
    for gate in complacentes[:20]:
        print(f"    {gate}")


if __name__ == "__main__":  # pragma: no cover
    import argparse

    ap = argparse.ArgumentParser(description="Mede se os recomputos disparam em caso real.")
    ap.add_argument("--json", metavar="ARQUIVO", help="grava o censo em JSON")
    args = ap.parse_args()

    laudo = censo()
    _relatar(laudo)
    if args.json:
        Path(args.json).write_text(json.dumps(laudo, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
        print(f"\ncenso: {args.json}")
