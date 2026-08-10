# -*- coding: utf-8 -*-
"""forja_licoes.py — o índice das lições da casa, e o que cada uma faz reprovar.

A queixa que originou este módulo é a de que o sistema esquece. Medido em
10/08/2026, o esquecimento tem forma e tamanho:

* `RETROSPECTIVAS.md` tem **321 lições** em 1.104 linhas, num arquivo que só se
  consulta lendo inteiro. Ninguém lê 1.104 linhas antes de escrever uma função.
* **43 números querem dizer duas coisas.** "Lição 87" é uma lição e é outra
  lição, porque a numeração foi reiniciada ao longo do tempo. Isso não é
  desarrumação cosmética: torna **ambígua toda citação por número**, inclusive
  as que já estão no código.
* Apenas **27 lições (8%)** têm o número citado em código, teste ou contrato de
  fase. Para as outras 294 não há como responder "isto já virou gate?" — e o que
  não se consegue responder, alguém redescobre e reescreve. Aconteceu duas vezes
  só nesta semana.

O que este módulo NÃO faz, de propósito: renumerar. Reescrever 1.104 linhas
quebraria toda citação existente e toda referência em conversa, commit e
documento — trocaria uma ambiguidade por uma invalidação geral. Em vez disso,
cada lição ganha um **identificador estável derivado do próprio título**, que
não depende de posição e não muda quando o arquivo cresce. É o mesmo desenho do
registro de regras aprendidas: a coisa recebe nome próprio, e a ligação com o
código passa a ser conferível nos dois sentidos.

O gate que sai daqui é estreito e verdadeiro: **citação ambígua reprova**. Não
se cobra que as 321 lições virem gate — muitas são julgamento humano e devem
continuar sendo. Cobra-se que, quando o código diz "Lição 87", exista uma só
Lição 87 para ele estar apontando.

Uso
    python forja_licoes.py                 # o retrato
    python forja_licoes.py --ambiguas      # só as citações que não decidem
    python forja_licoes.py --orfas         # lições sem nada que as faça valer
    python forja_licoes.py --indexar       # grava o índice legível por máquina
    python forja_licoes.py --buscar prazo  # acha a lição pelo assunto
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

FORJA = Path(__file__).resolve().parent
RETRO = FORJA / "RETROSPECTIVAS.md"
INDICE = FORJA / "learning_registry" / "LICOES_INDEX.json"

VERSAO = "FORJA-LICOES-v1"

# Os dois formatos que convivem no arquivo. Ler só um subestimaria o corpus pela
# metade — a primeira contagem que fiz devolveu 7 lições de 321 por isso.
_NOMEADA = re.compile(r"\*\*Liç(?:ão|ao)\s+(\d{1,3})\s*[—–-]\s*(.+?)\*\*")
_NUMERADA = re.compile(r"^\s*(\d{1,3})\.\s+\*\*(.+?)\*\*", re.M)

# Onde uma lição pode estar ancorada: algo que reprova se ela for violada.
_CITACAO = re.compile(r"[Ll]i[çc][ãa]o\s+(\d{1,3})")
_ONDE_ANCORAR = ("*.py", "phase_contracts/*.json", "templates/*.md")


def _ident(titulo: str) -> str:
    """Nome próprio da lição, derivado do título e independente da posição.

    Não usa o número porque é justamente ele que está duplicado, e não usa a
    linha porque ela muda a cada edição do arquivo.
    """
    base = unicodedata.normalize("NFKD", titulo.lower())
    base = "".join(c for c in base if not unicodedata.combining(c))
    base = re.sub(r"[^a-z0-9]+", " ", base).strip()
    return "licao-" + hashlib.sha256(base.encode()).hexdigest()[:12]


def ler(caminho: Path | None = None) -> list[dict]:
    """Todas as lições do arquivo, na ordem em que aparecem, com o corpo.

    O corpo vai junto porque a busca por título não serve para recuperar nada:
    medida aqui, "prazo" devolvia zero achados num acervo que tem lições sobre
    contagem de prazo — elas simplesmente não usam a palavra no título. Índice
    que só acha quem já sabe o nome do que procura não resolve esquecimento.
    """
    texto = (caminho or RETRO).read_text(encoding="utf-8", errors="ignore")
    linhas = texto.splitlines()
    achados: list[dict] = []
    for i, linha in enumerate(linhas, 1):
        for regex in (_NOMEADA, _NUMERADA):
            m = regex.search(linha)
            if not m:
                continue
            titulo = m.group(2).strip().rstrip(".")
            achados.append({"numero": int(m.group(1)), "titulo": titulo,
                            "id": _ident(titulo), "linha": i})
            break
    for atual, seguinte in zip(achados, achados[1:] + [None]):
        fim = (seguinte["linha"] - 1) if seguinte else len(linhas)
        atual["corpo"] = "\n".join(linhas[atual["linha"] - 1:fim]).strip()
    return achados


def numeros_ambiguos(licoes: list[dict]) -> dict[int, list[dict]]:
    """Números que designam mais de uma lição — e por isso não designam nenhuma."""
    por_numero = defaultdict(list)
    for lic in licoes:
        por_numero[lic["numero"]].append(lic)
    return {n: v for n, v in sorted(por_numero.items()) if len(v) > 1}


def citacoes(raiz: Path | None = None) -> dict[int, set[str]]:
    """Onde o código cita lição por número."""
    base = raiz or FORJA
    achado: dict[int, set[str]] = defaultdict(set)
    for padrao in _ONDE_ANCORAR:
        for p in base.glob(padrao):
            if p.name == Path(__file__).name:
                continue  # este módulo fala de lições por ofício
            try:
                texto = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for n in _CITACAO.findall(texto):
                achado[int(n)].add(p.name)
    return achado


def retrato(caminho: Path | None = None, raiz: Path | None = None) -> dict:
    licoes = ler(caminho)
    ambiguos = numeros_ambiguos(licoes)
    citadas = citacoes(raiz)
    numeros = {lic["numero"] for lic in licoes}

    # A citação que aponta para um número duplicado não erra o alvo: ela não
    # tem alvo. É o achado que este módulo existe para tornar impossível.
    ambiguas = {n: sorted(arqs) for n, arqs in citadas.items() if n in ambiguos}
    orfas = [lic for lic in licoes if lic["numero"] not in citadas]
    perdidas = {n: sorted(arqs) for n, arqs in citadas.items() if n not in numeros}

    return {
        "versao": VERSAO,
        "licoes": len(licoes),
        "numerosDistintos": len(numeros),
        "numerosAmbiguos": len(ambiguos),
        "citadasEmCodigo": len(set(citadas) & numeros),
        "citacoesAmbiguas": ambiguas,
        "citacoesSemLicao": perdidas,
        "orfas": len(orfas),
        "detalhe": {
            "ambiguos": {str(n): [{"titulo": x["titulo"], "linha": x["linha"],
                                   "id": x["id"]} for x in v]
                         for n, v in ambiguos.items()},
        },
        "itens": licoes,
    }


def _imprimir(r: dict) -> None:
    print(f"{r['versao']} — {r['licoes']} lições, {r['numerosDistintos']} números")
    print(f"  números que designam mais de uma lição   {r['numerosAmbiguos']:4d}")
    print(f"  lições citadas em código/teste/contrato  {r['citadasEmCodigo']:4d}"
          f"  ({r['citadasEmCodigo'] / max(1, r['licoes']):.0%})")
    print(f"  lições sem nada que as faça reprovar     {r['orfas']:4d}")
    if r["citacoesAmbiguas"]:
        print(f"\n  {len(r['citacoesAmbiguas'])} citação(ões) em código apontam para "
              f"número duplicado — não erram o alvo, ficam sem alvo:")
        for n, arqs in sorted(r["citacoesAmbiguas"].items()):
            titulos = [x["titulo"][:44] for x in r["detalhe"]["ambiguos"][str(n)]]
            print(f"    Lição {n}: citada em {', '.join(arqs)[:60]}")
            for t in titulos:
                print(f"        pode ser: {t}")
    if r["citacoesSemLicao"]:
        print(f"\n  citação a lição que não existe no arquivo:")
        for n, arqs in sorted(r["citacoesSemLicao"].items()):
            print(f"    Lição {n} em {', '.join(arqs)[:70]}")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--ambiguas", action="store_true",
                   help="só as citações em código que não decidem")
    p.add_argument("--orfas", action="store_true",
                   help="lições sem citação em código, teste ou contrato")
    p.add_argument("--buscar", metavar="TERMO", help="acha a lição pelo assunto")
    p.add_argument("--indexar", action="store_true",
                   help=f"grava {INDICE.name} para consulta por máquina")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    r = retrato()

    if a.buscar:
        alvo = a.buscar.lower()
        # Título primeiro, corpo depois: quem acerta o título quase sempre quer
        # aquela lição, e enterrá-la no meio dos achados por corpo seria pior.
        no_titulo = [x for x in r["itens"] if alvo in x["titulo"].lower()]
        no_corpo = [x for x in r["itens"]
                    if x not in no_titulo and alvo in x.get("corpo", "").lower()]
        for x in no_titulo:
            print(f"  Lição {x['numero']:3d}  linha {x['linha']:5d}  "
                  f"{x['titulo'][:86]}")
        if no_corpo:
            print(f"  — e no corpo de mais {len(no_corpo)}:")
            for x in no_corpo[:12]:
                print(f"  Lição {x['numero']:3d}  linha {x['linha']:5d}  "
                      f"{x['titulo'][:86]}")
            if len(no_corpo) > 12:
                print(f"       … e mais {len(no_corpo) - 12}")
        print(f"\n{len(no_titulo)} no título, {len(no_corpo)} no corpo, "
              f"sobre {a.buscar!r}.")
        return 0

    if a.orfas:
        citadas = citacoes()
        for x in r["itens"]:
            if x["numero"] not in citadas:
                print(f"  Lição {x['numero']:3d}  {x['titulo'][:92]}")
        print(f"\n{r['orfas']} sem âncora. Nem toda lição precisa virar gate — "
              f"muitas são julgamento humano. O que não pode é ninguém conseguir "
              f"responder quais são quais.")
        return 0

    if a.indexar:
        INDICE.parent.mkdir(parents=True, exist_ok=True)
        INDICE.write_text(json.dumps(
            {k: v for k, v in r.items() if k != "detalhe"},
            ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"gravado: {INDICE}")
        return 0

    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0

    _imprimir(r)
    if a.ambiguas:
        return 1 if r["citacoesAmbiguas"] else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
