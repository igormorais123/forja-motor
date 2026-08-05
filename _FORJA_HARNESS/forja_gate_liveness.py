# -*- coding: utf-8 -*-
"""forja_gate_liveness.py — prova que cada gate declarado realmente roda.

Motivo. A falha mais cara da esteira não é o gate frouxo: é o gate que não roda.
Em 04/08/2026 o recomputo de lastro do F7 foi encontrado inerte desde que
nasceu — procurava um artefato com um nome que nenhuma execução emite, e devolveu
`not_applicable` em 100% das rodadas (7 fases F7, zero laudos). Antes dele, o elo
4-B de fidelidade visual tinha rodado em 3 casos na história inteira. Os dois
compartilham a mesma assinatura: **a saída de "não examinei nada" é idêntica à de
"examinei e aprovei"**, e nenhum painel distingue as duas.

Esta ferramenta mede três coisas que ninguém media:

1. **Inerte** — gate declarado em contrato de fase que nunca apareceu em nenhum
   resultado do acervo. Ou o produtor usa outro nome, ou o gate não é cobrado.
2. **Complacente** — gate que aparece, sempre em `pass`, e nunca reprovou nada.
   Não é prova de defeito: há gate que de fato nunca foi violado. É prova de que
   ninguém sabe se ele sabe dizer não, e é onde a autovalidação se esconde.
3. **Órfão** — gate que os resultados relatam e nenhum contrato exige. Vive fora
   de governança: some sem que nada reprove.

O que a ferramenta NÃO faz: julgar se o limiar do gate é bom. Ela responde
"este gate já operou?" e "ele já disse não?", que são perguntas anteriores e que
estavam sem resposta.

Uso:
    python forja_gate_liveness.py
    python forja_gate_liveness.py --json LIVENESS.json
    python forja_gate_liveness.py --estrito    # sai != 0 se houver gate inerte
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from collections import defaultdict
from pathlib import Path

FORJA = Path(__file__).resolve().parent
CONTRATOS = FORJA / "phase_contracts"
ESTADO = FORJA / "state"

# Valores que contam como reprovação. `warn` não conta: é achado sem veredito
# negativo, e tratá-lo como reprovação inflaria a evidência de que o gate sabe
# dizer não.
REPROVA = {"fail", "failed", "blocked", "reproved", "reprovado", "no", "false"}
APROVA = {"pass", "passed", "ok", "aprovado", "yes", "true"}


def _nomes_declarados() -> dict[str, set[str]]:
    """gate -> fases que o exigem."""
    declarados: dict[str, set[str]] = defaultdict(set)
    for caminho in sorted(CONTRATOS.glob("*.json")):
        try:
            contrato = json.loads(caminho.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        fase = str(contrato.get("phase") or caminho.stem)
        for gate in contrato.get("requiredGates") or []:
            declarados[str(gate)].add(fase)
    return declarados


def _alias(nome: str) -> set[str]:
    """Nomes legados aceitos para o mesmo gate, quando o harness os declara."""
    try:
        from forja_n3_common import name_with_legacy
    except ImportError:
        return {nome}
    try:
        return {str(x) for x in name_with_legacy(nome)}
    except Exception:  # noqa: BLE001 - a ausência de alias não pode derrubar a medição
        return {nome}


def _observados() -> tuple[dict[str, dict], int]:
    """gate -> {pass, fail, outro, fases}. Varre todo resultado do acervo."""
    observados: dict[str, dict] = defaultdict(
        lambda: {"pass": 0, "fail": 0, "outro": 0, "fases": set()})
    resultados = 0
    for caminho in ESTADO.rglob("*.json"):
        nome = caminho.name
        if nome not in {"PHASE_RESULT.json", "f7_gate_result.json",
                        "COMPUTED_LASTRO_GATES.json", "F8S_ASSINATURA_VISUAL.json",
                        "FORJA_N3_STATE.json", "F10_DELIVERY_INTEGRITY.json"}:
            continue
        try:
            dados = json.loads(caminho.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(dados, dict):
            continue
        resultados += 1
        fase = str(dados.get("phase") or caminho.parent.name)
        blocos = [dados.get("gates"), dados.get("computed"),
                  dados.get("gatesForjaVerificador"), dados.get("computedLastroGates")]
        if nome == "FORJA_N3_STATE.json":
            blocos.append((dados.get("deliveryEvidence") or {}).get("gates"))
        for bloco in blocos:
            if not isinstance(bloco, dict):
                continue
            for gate, valor in bloco.items():
                chave = str(gate)
                texto = str(valor).strip().casefold()
                registro = observados[chave]
                registro["fases"].add(fase)
                if texto in REPROVA:
                    registro["fail"] += 1
                elif texto in APROVA:
                    registro["pass"] += 1
                else:
                    registro["outro"] += 1
    return observados, resultados


def _sem_produtor(declarados: dict[str, set[str]]) -> list[dict]:
    """Gates cujo nome só aparece no próprio contrato — nenhum código os computa.

    Isto sozinho NÃO significa inexequível: a maior parte é emitida pelo agente,
    que recebe `requiredGates` no `RUN_CONTEXT` e escreve `pass` no
    `PHASE_RESULT`. Por isso o resultado é cruzado com a observação no acervo:

    - sem produtor **e observado** => o agente atesta a si mesmo. É a superfície
      de autovalidação da esteira, e o número dela nunca tinha sido medido.
    - sem produtor **e nunca observado** => ninguém sabe emitir e ninguém emitiu.
      A fase não fecha como especificada.

    Medido em 04/08/2026: 13 dos 16 gates do F8 caíam no segundo caso, e o F8
    rodou 2 vezes na história, ambas antes de o contrato ser apertado.
    """
    corpus: list[str] = []
    for padrao in ("*.py", "templates/*.md", "prompts/*.md", "*.md"):
        for caminho in FORJA.glob(padrao):
            # Teste não é produtor, e documento não é produtor. Sem esta
            # exclusão, escrever a regressão de um gate faria o próprio gate
            # parecer implementado — a métrica passaria a medir quem fala dela
            # em vez de quem a cumpre. Medido ao vivo em 04/08/2026: criar
            # `test_forja_f8_gates_contrato.py` moveu o número de 30 para 34
            # sem que uma linha de produção tivesse mudado.
            if caminho.name == Path(__file__).name or caminho.name.startswith("test_"):
                continue
            try:
                bruto = caminho.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            # Comentário também não é produtor. Medido em 04/08/2026: o gate
            # `citation_identity_and_cnj_tribunal_resolved` contava como
            # implementado porque um comentário o mencionava para dizer que
            # NÃO era assunto daquele trecho. Falar de um gate e cumpri-lo são
            # coisas diferentes, e a métrica não pode confundi-las.
            corpus.append("\n".join(
                linha for linha in bruto.splitlines()
                if not linha.lstrip().startswith("#")))
    texto = "\n".join(corpus)
    orfaos = []
    for gate, fases in sorted(declarados.items()):
        if not any(nome in texto for nome in _alias(gate)):
            orfaos.append({"gate": gate, "fases": sorted(fases)})
    return orfaos


def medir() -> dict:
    declarados = _nomes_declarados()
    observados, resultados = _observados()
    vistos = set(observados)

    inertes, complacentes, ativos = [], [], []
    for gate, fases in sorted(declarados.items()):
        candidatos = _alias(gate) & vistos
        if not candidatos:
            inertes.append({"gate": gate, "fases": sorted(fases)})
            continue
        soma = {"pass": 0, "fail": 0, "outro": 0}
        for nome in candidatos:
            for chave in soma:
                soma[chave] += observados[nome][chave]
        registro = {"gate": gate, "fases": sorted(fases), **soma,
                    "observadoComo": sorted(candidatos)}
        (ativos if soma["fail"] else complacentes).append(registro)

    todos_declarados = set()
    for gate in declarados:
        todos_declarados |= _alias(gate)
    orfaos = [
        {"gate": gate, "pass": observados[gate]["pass"], "fail": observados[gate]["fail"],
         "fases": sorted(observados[gate]["fases"])}
        for gate in sorted(vistos - todos_declarados)
    ]

    sem_produtor = {item["gate"] for item in _sem_produtor(declarados)}
    nomes_inertes = {item["gate"] for item in inertes}
    autodeclarados = sorted(sem_produtor - nomes_inertes)
    inexequiveis = [item for item in inertes if item["gate"] in sem_produtor]
    # Inerte com produtor é diagnóstico DIFERENTE de inerte sem produtor, e
    # tratá-los como uma coisa só foi imprecisão do próprio instrumento de
    # medida. Aqui existe código que sabe emitir o gate; o que nunca aconteceu
    # foi a rota rodar. É a lição 3 do plano visual — "gate instalado na rota
    # que ninguém percorre é gate nenhum" —, e ela pede exercitar a rota, não
    # escrever produtor. Medido em 04/08/2026: os 14 gates do F8 e os 3 do F10
    # estão nesta faixa, porque empacotamento e fechamento rodam muito menos
    # que as fases N3.
    nao_exercitados = [item for item in inertes if item["gate"] not in sem_produtor]
    computados = sorted(set(declarados) - sem_produtor)

    return {
        "versao": "FORJA-GATE-LIVENESS-v2",
        "resultadosExaminados": resultados,
        "gatesDeclarados": len(declarados),
        "gatesObservados": len(vistos),
        "computados": computados,
        "autodeclarados": autodeclarados,
        "inexequiveis": inexequiveis,
        "naoExercitados": nao_exercitados,
        "inertes": inertes,
        "complacentes": sorted(complacentes, key=lambda x: -x["pass"]),
        "ativos": sorted(ativos, key=lambda x: -x["fail"]),
        "orfaos": orfaos,
    }


def relatar(laudo: dict) -> None:
    print("=" * 74)
    print("LIVENESS DOS GATES DA FORJA")
    print("=" * 74)
    print(f"  resultados examinados : {laudo['resultadosExaminados']}")
    print(f"  gates declarados      : {laudo['gatesDeclarados']}")
    print(f"  gates observados      : {laudo['gatesObservados']}")

    total = laudo["gatesDeclarados"] or 1
    n_comp, n_auto = len(laudo["computados"]), len(laudo["autodeclarados"])
    print("\n  QUEM DECIDE CADA GATE")
    print(f"    computados por código : {n_comp:3}  ({100*n_comp//total}%)")
    print(f"    atestados pelo agente : {n_auto:3}  ({100*n_auto//total}%)  <- superfície de autovalidação")

    print(f"\nINEXEQUÍVEIS — sem produtor e nunca observados ({len(laudo['inexequiveis'])})")
    print("  Ninguém sabe emitir e ninguém emitiu. A fase não fecha como especificada.")
    for item in laudo["inexequiveis"]:
        print(f"    {item['gate']:52} ({', '.join(item['fases'])})")
    if not laudo["inexequiveis"]:
        print("    nenhum")

    nao_ex = laudo.get("naoExercitados", [])
    print(f"\nNÃO EXERCITADOS — têm produtor, a rota nunca rodou ({len(nao_ex)})")
    print("  Diagnóstico diferente do anterior: o código sabe emitir, o que falta é")
    print("  a rota acontecer. Pede exercitar a rota, não escrever produtor.")
    for item in nao_ex:
        print(f"    {item['gate']:52} ({', '.join(item['fases'])})")
    if not nao_ex:
        print("    nenhum")

    print(f"\nCOMPLACENTES — observados e nunca reprovaram ({len(laudo['complacentes'])})")
    print("  Não é defeito por si: há gate legitimamente nunca violado. É onde")
    print("  ninguém sabe se o gate sabe dizer não.")
    for item in laudo["complacentes"][:25]:
        print(f"    {item['gate']:52} pass={item['pass']:3}")
    resto = len(laudo["complacentes"]) - 25
    if resto > 0:
        print(f"    ... e mais {resto}")

    print(f"\nÓRFÃOS — relatados e não exigidos por contrato ({len(laudo['orfaos'])})")
    for item in laudo["orfaos"][:20]:
        print(f"    {item['gate']:52} pass={item['pass']:3} fail={item['fail']:3}")
    resto = len(laudo["orfaos"]) - 20
    if resto > 0:
        print(f"    ... e mais {resto}")

    print(f"\nATIVOS — já reprovaram alguma coisa ({len(laudo['ativos'])})")
    for item in laudo["ativos"][:12]:
        print(f"    {item['gate']:52} fail={item['fail']:3} pass={item['pass']:3}")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Mede se cada gate declarado realmente roda.")
    ap.add_argument("--json", metavar="ARQUIVO", help="grava o laudo em JSON")
    ap.add_argument("--estrito", action="store_true",
                    help="sai com código != 0 quando houver gate inerte")
    args = ap.parse_args(argv)

    laudo = medir()
    relatar(laudo)
    if args.json:
        Path(args.json).write_text(
            json.dumps(laudo, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nlaudo: {args.json}")
    return 1 if (args.estrito and laudo["inertes"]) else 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    raise SystemExit(main(sys.argv[1:]))
