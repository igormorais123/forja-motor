# -*- coding: utf-8 -*-
"""forja_tpu_diff.py — o que mudou entre duas versões das TPU do CNJ.

O procedimento de manutenção pedido em 07/08/2026 exige, no item 5, identificar
e classificar **códigos acrescentados, descrições ou glossários alterados,
mudanças de hierarquia, códigos inativados, códigos reativados, diferenças por
segmento e mudanças de estrutura do arquivo** — e produzir dois relatórios: um
legível para o jurídico e outro estruturado para os sistemas.

Sem isso o vigia de versão avisa que mudou e ninguém sabe o quê. Numa taxonomia
de 62 mil linhas, "mudou" sem o diff obriga a reler tudo, que é o mesmo que não
reler nada.

Duas decisões de desenho que vêm de erro já cometido nesta casa:

**A comparação é por (tabela, segmento, código), nunca por descrição.** Código é
a identidade que o CNJ mantém; descrição é o rótulo que ele reescreve. Comparar
por texto transformaria cada correção de acentuação em "item novo" e enterraria
a mudança real no ruído.

**Reativação não se infere da ausência de data de inativação.** Um código que
some da coluna de inativação pode ter sido reativado ou pode ter tido a data
corrigida. O CNJ tem coluna própria de reativação, e é ela que decide; quando as
duas discordam, o item entra em `divergencias` em vez de virar veredito.

O que ele NÃO faz: não julga se a mudança é juridicamente relevante. O e-mail é
expresso — "alterações semânticas relevantes deverão ser revisadas por Igor antes
de qualquer propagação" —, e essa é exatamente a linha entre o que a máquina
apura e o que a pessoa decide.

Uso:
    python forja_tpu_diff.py --antes <a.sqlite> --depois <b.sqlite> \
                             --json DIFF.json --relatorio DIFF.md
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

VERSAO = "FORJA-TPU-DIFF-v1"

# Os campos cuja alteração interessa. `descricao` e `glossario` são o texto que
# o jurídico lê; `cod_pai` é a hierarquia; as datas são o ciclo de vida.
COMPARADOS = ("descricao", "cod_pai", "glossario",
              "dt_inativacao", "dt_reativacao")


def carregar(banco: Path) -> dict[tuple, dict]:
    """Itens de uma versão, indexados por (tabela, segmento, código).

    Quando o mesmo código aparece duas vezes no arquivo — o CNJ redeclara nós de
    topo como cabeçalho de seção, 55 vezes na versão de 26/05/2026 — conserva-se
    a primeira ocorrência. As repetições são idênticas nesta versão; se deixarem
    de ser, `divergencias` acusa, porque a segunda passa a discordar da primeira.
    """
    con = sqlite3.connect(banco)
    con.row_factory = sqlite3.Row
    itens: dict[tuple, dict] = {}
    repetidos_diferentes = []
    for linha in con.execute(
            "SELECT tabela, segmento, codigo, descricao, cod_pai, glossario, "
            "dt_inativacao, dt_reativacao FROM itens"):
        chave = (linha["tabela"], linha["segmento"], linha["codigo"])
        atual = {c: linha[c] for c in COMPARADOS}
        anterior = itens.get(chave)
        if anterior is None:
            itens[chave] = atual
        elif anterior != atual:
            repetidos_diferentes.append(chave)
    con.close()
    if repetidos_diferentes:
        itens["__repetidos_diferentes__"] = repetidos_diferentes  # type: ignore
    return itens


def comparar(antes: dict, depois: dict) -> dict:
    """O diff. Toda categoria é apurada por comparação, nenhuma por inferência."""
    rep_antes = antes.pop("__repetidos_diferentes__", [])
    rep_depois = depois.pop("__repetidos_diferentes__", [])

    chaves_antes, chaves_depois = set(antes), set(depois)
    resultado: dict = {
        "geradoPor": VERSAO,
        "totais": {"antes": len(chaves_antes), "depois": len(chaves_depois)},
        "acrescentados": [], "removidos": [], "inativados": [], "reativados": [],
        "hierarquia": [], "descricao": [], "glossario": [], "divergencias": [],
    }

    for chave in sorted(chaves_depois - chaves_antes):
        t, s, c = chave
        resultado["acrescentados"].append(
            {"tabela": t, "segmento": s, "codigo": c,
             "descricao": depois[chave]["descricao"]})

    # Remoção é diferente de inativação, e confundi-las é erro caro: o código
    # inativado continua existindo e ainda aparece em processos antigos; o
    # removido do export não tem mais linha nenhuma.
    for chave in sorted(chaves_antes - chaves_depois):
        t, s, c = chave
        resultado["removidos"].append(
            {"tabela": t, "segmento": s, "codigo": c,
             "descricao": antes[chave]["descricao"]})

    for chave in sorted(chaves_antes & chaves_depois):
        t, s, c = chave
        a, d = antes[chave], depois[chave]
        base = {"tabela": t, "segmento": s, "codigo": c,
                "descricao": d["descricao"]}

        if not a["dt_inativacao"] and d["dt_inativacao"]:
            resultado["inativados"].append({**base, "em": d["dt_inativacao"]})
        if a["dt_inativacao"] and not d["dt_inativacao"]:
            # A ausência sozinha não prova reativação — ver o cabeçalho.
            if d["dt_reativacao"] and d["dt_reativacao"] != a["dt_reativacao"]:
                resultado["reativados"].append(
                    {**base, "em": d["dt_reativacao"]})
            else:
                resultado["divergencias"].append({
                    **base,
                    "problema": ("a data de inativação sumiu sem data de "
                                 "reativação correspondente: pode ser "
                                 "reativação sem registro ou correção da data "
                                 "anterior. Exige conferência humana"),
                    "antes": a["dt_inativacao"], "depois": None})
        if a["cod_pai"] != d["cod_pai"]:
            resultado["hierarquia"].append(
                {**base, "paiAntes": a["cod_pai"], "paiDepois": d["cod_pai"]})
        if a["descricao"] != d["descricao"]:
            resultado["descricao"].append(
                {**base, "antes": a["descricao"], "depois": d["descricao"]})
        if (a["glossario"] or "") != (d["glossario"] or ""):
            resultado["glossario"].append(
                {**base,
                 "tinhaGlossario": bool(a["glossario"]),
                 "temGlossario": bool(d["glossario"])})

    for chave in rep_antes + rep_depois:
        resultado["divergencias"].append({
            "tabela": chave[0], "segmento": chave[1], "codigo": chave[2],
            "problema": ("o mesmo código aparece duas vezes no arquivo com "
                         "conteúdo diferente; a comparação usou a primeira "
                         "ocorrência")})

    resultado["resumo"] = {k: len(v) for k, v in resultado.items()
                           if isinstance(v, list)}
    resultado["houveMudanca"] = any(resultado["resumo"].values())
    return resultado


TITULOS = {
    "acrescentados": "Códigos novos",
    "removidos": "Códigos que saíram do export",
    "inativados": "Códigos inativados",
    "reativados": "Códigos reativados",
    "hierarquia": "Mudanças de hierarquia (mudou o código do pai)",
    "descricao": "Descrições alteradas",
    "glossario": "Glossários alterados",
    "divergencias": "Precisam de conferência humana",
}


def relatorio(diff: dict, antes: str, depois: str, limite: int = 40) -> str:
    """O relatório legível. O outro produto, o JSON, é o mesmo dado sem corte.

    O corte por categoria é declarado no texto, e não silencioso: uma versão do
    CNJ pode mexer em milhares de assuntos, e um relatório de mil páginas não é
    lido — mas um relatório que esconde o tamanho do que omitiu é pior.
    """
    linhas = [f"# TPU/CNJ — o que mudou entre {antes} e {depois}", ""]
    if not diff["houveMudanca"]:
        linhas += ["Nenhuma diferença entre as duas versões: mesmos códigos, "
                   "mesma hierarquia, mesmas descrições, mesmos glossários e "
                   "mesmo ciclo de vida.", ""]
        return "\n".join(linhas)

    linhas += [f"Itens: **{diff['totais']['antes']}** antes, "
               f"**{diff['totais']['depois']}** depois.", "",
               "| o que mudou | quantos |", "|---|---:|"]
    for chave, titulo in TITULOS.items():
        linhas.append(f"| {titulo} | {diff['resumo'][chave]} |")
    linhas.append("")

    if diff["resumo"]["divergencias"]:
        linhas += ["> **Leia primeiro as divergências.** Elas são o que a "
                   "comparação não conseguiu decidir sozinha, e nenhuma "
                   "propagação deve ocorrer antes de resolvê-las.", ""]

    for chave, titulo in TITULOS.items():
        itens = diff[chave]
        if not itens:
            continue
        linhas += [f"## {titulo} ({len(itens)})", ""]
        for it in itens[:limite]:
            onde = f"{it['tabela']}/{it['segmento'] or 'único'}"
            if chave == "descricao":
                linhas.append(f"- `{it['codigo']}` em {onde}: "
                              f"**{it['antes']}** → **{it['depois']}**")
            elif chave == "hierarquia":
                linhas.append(f"- `{it['codigo']}` {it['descricao']} em {onde}: "
                              f"pai {it['paiAntes']} → {it['paiDepois']}")
            elif chave == "divergencias":
                linhas.append(f"- `{it['codigo']}` em {onde}: {it['problema']}")
            else:
                linhas.append(f"- `{it['codigo']}` {it['descricao']} em {onde}")
        if len(itens) > limite:
            linhas.append(f"- … e mais **{len(itens) - limite}**, todos no JSON "
                          f"que acompanha este relatório")
        linhas.append("")

    linhas += ["---", "",
               "Apurado por comparação de código a código; nenhuma categoria "
               "foi inferida. Este relatório não julga se a mudança é "
               "juridicamente relevante — essa leitura é humana e precede "
               "qualquer propagação para o sistema de gestão, para a taxonomia "
               "de pesquisa ou para os agentes."]
    return "\n".join(linhas)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--antes", required=True, help="banco da versão anterior")
    p.add_argument("--depois", required=True, help="banco da versão nova")
    p.add_argument("--json", help="onde gravar o diff estruturado")
    p.add_argument("--relatorio", help="onde gravar o relatório legível")
    p.add_argument("--limite", type=int, default=40,
                   help="itens por categoria no relatório legível")
    a = p.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    diff = comparar(carregar(Path(a.antes)), carregar(Path(a.depois)))
    for chave, titulo in TITULOS.items():
        print(f"{titulo:<48} {diff['resumo'][chave]:>6}")

    if a.json:
        Path(a.json).write_text(json.dumps(diff, ensure_ascii=False, indent=2),
                                encoding="utf-8")
        print(f"gravado: {a.json}")
    if a.relatorio:
        Path(a.relatorio).write_text(
            relatorio(diff, Path(a.antes).stem, Path(a.depois).stem, a.limite),
            encoding="utf-8")
        print(f"gravado: {a.relatorio}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
