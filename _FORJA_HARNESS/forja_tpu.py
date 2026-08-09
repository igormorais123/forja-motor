# -*- coding: utf-8 -*-
"""forja_tpu.py — as Tabelas Processuais Unificadas do CNJ viram dado consultável.

Por que existe. O titular encaminhou, em 08/08/2026, o acervo oficial das TPUs
(Resolução CNJ nº 46/2007) e abriu quatro frentes ao Desenvolvimento:
armazenamento versionado, integração com o sistema de gestão do escritório,
taxonomia de pesquisa e agentes de IA. As quatro pedem, como primeiro produto,
a mesma coisa — "esquema normalizado e dicionário de dados" —, e nenhuma delas
pode começar enquanto a taxonomia estiver presa em 79 arquivos que o Excel abre
e nenhum programa consulta.

O formato engana duas vezes. O CNJ serve os arquivos com extensão `.xls`, mas o
conteúdo é **tabela HTML**: abrir com leitor de planilha funciona, abrir com
`xlrd` ou `openpyxl` falha, e o LEIA-ME oficial avisa que isso é característica
do arquivo e não corrupção. E a codificação é `cp1252`, não UTF-8 — ler como
UTF-8 devolve texto que parece certo até a primeira palavra acentuada.

A hierarquia aparece duas vezes em cada linha, e só uma delas presta. A primeira
é visual: colunas vazias à esquerda desenham a indentação da árvore. A segunda é
`Código`/`Cód. Pai`. **Só a segunda é lida aqui.** A indentação é apresentação e
diverge da árvore real — o item raiz de Documentos aparece indentado um nível à
frente do filho dele.

O que este módulo NÃO faz, e é deliberado: não interpreta juridicamente nenhum
código, não propõe equivalência com sistema nenhum e não infere sinônimo. Ele
entrega o dado fiel à fonte, com a proveniência de cada linha, para que as
decisões jurídicas sejam tomadas por quem responde por elas.

Uso:
    python forja_tpu.py --pacote <dir> --saida <arquivo.sqlite>
    python forja_tpu.py --pacote <dir> --dicionario   # descreve os campos lidos
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sqlite3
import sys
from pathlib import Path

VERSAO = "FORJA-TPU-v1"

# O CNJ divide o acervo em quatro tabelas; a pasta do pacote diz qual é qual.
TABELAS = {
    "01_Documentos_Processuais": "documentos",
    "02_Classes_Processuais": "classes",
    "03_Assuntos_Processuais": "assuntos",
    "04_Movimentos_Processuais": "movimentos",
}

# Colunas que existem em toda tabela e são o esqueleto do dado. As demais
# variam por tabela (Movimentos traz complemento, dispositivo legal e artigo) e
# são preservadas em `extras`, sem inventar coluna nem descartar informação.
CANONICAS = {
    "código": "codigo",
    "cód. pai": "cod_pai",
    "glossário": "glossario",
    "data de publicação": "dt_publicacao",
    "data de alteração": "dt_alteracao",
    "data de inativação": "dt_inativacao",
    "data de reativação": "dt_reativacao",
}

_TR = re.compile(r"(?i)<tr[^>]*>")
_TD = re.compile(r"(?i)<t[dh][^>]*>")
_TAG = re.compile(r"<[^>]+>")


def _texto(celula: str) -> str:
    """Conteúdo textual de uma célula, com entidades resolvidas.

    O glossário do CNJ vem com entidade HTML dentro (`&agrave;`, `&ccedil;`),
    porque o arquivo é HTML de verdade. Sem `unescape`, o dicionário de dados
    sairia com `deve ser utilizado quando o aditamento &agrave; inicial`.
    """
    return html.unescape(_TAG.sub("", celula)).replace("\xa0", " ").strip()


def _linhas(bruto: bytes) -> list[list[str]]:
    """As linhas do arquivo, cada uma como lista de células de texto."""
    texto = bruto.decode("cp1252", "replace")
    saida = []
    for bloco in _TR.split(texto)[1:]:
        celulas = [_texto(c) for c in _TD.split(bloco)[1:]]
        if celulas:
            saida.append(celulas)
    return saida


def _segmento(nome: str) -> str | None:
    """O ramo da Justiça, que o CNJ codifica no nome do arquivo.

    `79_Tabela_Movimentos_CJF.xls` é do Conselho da Justiça Federal;
    `79_Tabela_Documentos_Processuais.xls` é único e não tem segmento.
    """
    m = re.match(r"(?i)^\d+_Tabela_(Classes|Assuntos|Movimentos)_(.+)\.xls$", nome)
    return m.group(2) if m else None


def _registros(celulas: list[str], n_colunas: int):
    """Os itens contidos numa linha do arquivo. Normalmente um; às vezes dois.

    O CNJ fecha mal algumas linhas e emite **dois itens dentro do mesmo `<tr>`**.
    Recortar as últimas `n_colunas` células, que é o caminho óbvio, desalinha
    essas linhas inteiras: a primeira tentativa aqui produziu 1.154 itens
    apontando para 29 pais inexistentes e um item cujo código era a palavra
    "Originário". Os pais não faltavam no acervo do CNJ — estavam no segundo
    registro da linha emendada, que o recorte pelo fim descartava. Se eu tivesse
    parado no "rodou e leu 60 mil itens", teria publicado uma árvore quebrada
    com aparência de completa.

    O alinhamento correto vem da frente e usa a forma do dado: cada item é
    **descrição, recuo vazio, código, e as demais colunas em ordem**. O recuo é
    desenho da árvore e varia por profundidade; o código é o primeiro valor não
    vazio depois da descrição, e é sempre numérico — é isso que permite
    ressincronizar quando a linha traz sobra.
    """
    i, n = 0, len(celulas)
    while i < n:
        if not celulas[i]:
            i += 1
            continue
        descricao = celulas[i]
        j = i + 1
        while j < n and not celulas[j]:
            j += 1
        if j >= n or not celulas[j].isdigit():
            # não é item: legenda, título de seção ou sobra. Avança um e
            # tenta de novo, em vez de desistir da linha inteira.
            i += 1
            continue
        dados = celulas[j:j + n_colunas]
        dados += [""] * (n_colunas - len(dados))   # cauda vazia o CNJ omite
        yield descricao, dados
        i = j + n_colunas


def ler_arquivo(caminho: Path, tabela: str) -> tuple[list[dict], list[str]]:
    """Itens de um arquivo oficial. Devolve (itens, cabeçalho lido).

    O cabeçalho vem na mesma linha do título da tabela: a primeira célula é o
    título ("Movimentos processuais do CJF") e as seguintes são as colunas. O
    número de colunas varia por tabela, e é ele que separa, em cada linha, as
    células de indentação das células de dado.
    """
    linhas = _linhas(caminho.read_bytes())
    if not linhas:
        return [], []
    cabecalho = linhas[0][1:]          # a célula 0 é o título, não uma coluna
    n_colunas = len(cabecalho)
    chaves = [c.strip().lower() for c in cabecalho]
    segmento = _segmento(caminho.name)

    itens = []
    for celulas in linhas[1:]:
        for descricao, dados in _registros(celulas, n_colunas):
            registro = {"tabela": tabela, "segmento": segmento,
                        "descricao": descricao, "arquivo": caminho.name}
            extras = {}
            for chave, valor in zip(chaves, dados):
                destino = CANONICAS.get(chave)
                if destino:
                    registro[destino] = valor or None
                elif valor:
                    extras[chave] = valor
            registro["extras"] = (json.dumps(extras, ensure_ascii=False)
                                  if extras else None)
            itens.append(registro)
    return itens, cabecalho


def ler_pacote(raiz: Path) -> tuple[list[dict], list[dict]]:
    """Percorre as quatro pastas do pacote. Devolve (itens, arquivos lidos)."""
    itens, arquivos = [], []
    for pasta, tabela in TABELAS.items():
        for caminho in sorted((raiz / pasta).glob("*.xls")):
            lidos, cabecalho = ler_arquivo(caminho, tabela)
            itens.extend(lidos)
            arquivos.append({
                "arquivo": caminho.name, "tabela": tabela,
                "segmento": _segmento(caminho.name), "itens": len(lidos),
                "colunas": cabecalho,
                "sha256": hashlib.sha256(caminho.read_bytes()).hexdigest(),
                "bytes": caminho.stat().st_size,
            })
    return itens, arquivos


ESQUEMA = """
CREATE TABLE itens (
  tabela        TEXT NOT NULL,   -- documentos | classes | assuntos | movimentos
  segmento      TEXT,            -- ramo da Justiça; nulo em Documentos
  codigo        TEXT NOT NULL,   -- código oficial do CNJ
  cod_pai       TEXT,            -- pai na árvore oficial; a hierarquia REAL
  descricao     TEXT NOT NULL,
  glossario     TEXT,
  dt_publicacao TEXT,
  dt_alteracao  TEXT,
  dt_inativacao TEXT,            -- preenchido = código inativo nesta versão
  dt_reativacao TEXT,
  extras        TEXT,            -- JSON com as colunas próprias da tabela
  arquivo       TEXT NOT NULL    -- proveniência: o arquivo oficial de origem
);
CREATE INDEX ix_itens_codigo  ON itens (tabela, segmento, codigo);
CREATE INDEX ix_itens_pai     ON itens (tabela, segmento, cod_pai);
CREATE INDEX ix_itens_desc    ON itens (descricao);
CREATE TABLE arquivos (
  arquivo TEXT PRIMARY KEY, tabela TEXT, segmento TEXT,
  itens INTEGER, colunas TEXT, sha256 TEXT, bytes INTEGER
);
CREATE TABLE proveniencia (chave TEXT PRIMARY KEY, valor TEXT);
"""

COLUNAS = ("tabela", "segmento", "codigo", "cod_pai", "descricao", "glossario",
           "dt_publicacao", "dt_alteracao", "dt_inativacao", "dt_reativacao",
           "extras", "arquivo")


def gravar(itens: list[dict], arquivos: list[dict], destino: Path,
           versao_cnj: str, pacote: str) -> None:
    """Grava o banco do zero. Versão do CNJ é imutável: nunca se acrescenta."""
    if destino.exists():
        destino.unlink()
    con = sqlite3.connect(destino)
    con.executescript(ESQUEMA)
    con.executemany(
        f"INSERT INTO itens ({','.join(COLUNAS)}) "
        f"VALUES ({','.join('?' * len(COLUNAS))})",
        [tuple(i.get(c) for c in COLUNAS) for i in itens])
    con.executemany(
        "INSERT INTO arquivos VALUES (?,?,?,?,?,?,?)",
        [(a["arquivo"], a["tabela"], a["segmento"], a["itens"],
          json.dumps(a["colunas"], ensure_ascii=False), a["sha256"], a["bytes"])
         for a in arquivos])
    con.executemany("INSERT INTO proveniencia VALUES (?,?)", [
        ("geradoPor", VERSAO),
        ("versaoCNJ", versao_cnj),
        ("pacote", pacote),
        ("fonte", "https://www.cnj.jus.br/sgt/versoes.php"),
        ("observacao", "dado fiel à fonte; nenhuma equivalência ou sinônimo "
                       "foi inferido por este programa"),
    ])
    con.commit()
    con.close()


def conferir_hashes(raiz: Path) -> tuple[int, list[str]]:
    """Confere os 79 arquivos contra o SHA256SUMS.txt do próprio pacote."""
    somas = raiz / "SHA256SUMS.txt"
    if not somas.is_file():
        return 0, ["SHA256SUMS.txt ausente: a integridade não pôde ser conferida"]
    ok, problemas = 0, []
    for linha in somas.read_text(encoding="utf-8", errors="replace").splitlines():
        linha = linha.strip()
        if not linha:
            continue
        esperado, _, nome = linha.partition(" ")
        alvo = raiz / nome.strip().lstrip("*")
        if not alvo.is_file():
            problemas.append(f"ausente: {nome.strip()}")
            continue
        if hashlib.sha256(alvo.read_bytes()).hexdigest() != esperado:
            problemas.append(f"hash divergente: {nome.strip()}")
        else:
            ok += 1
    return ok, problemas


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--pacote", required=True, help="raiz da árvore descompactada")
    p.add_argument("--saida", help="banco SQLite a gravar")
    p.add_argument("--versao-cnj", default="2026-05-26")
    p.add_argument("--dicionario", action="store_true",
                   help="imprime as colunas encontradas em cada tabela")
    a = p.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    raiz = Path(a.pacote)
    ok, problemas = conferir_hashes(raiz)
    print(f"integridade: {ok} arquivo(s) conferidos contra o SHA256SUMS do pacote")
    for x in problemas[:10]:
        print(f"  {x}")
    if problemas:
        print("REPROVADO: o pacote não bate com os próprios hashes")
        return 1

    itens, arquivos = ler_pacote(raiz)
    por_tabela: dict[str, int] = {}
    for i in itens:
        por_tabela[i["tabela"]] = por_tabela.get(i["tabela"], 0) + 1
    print(f"lidos {len(arquivos)} arquivo(s) · {len(itens)} item(ns)")
    for t in TABELAS.values():
        print(f"  {t:<12} {por_tabela.get(t, 0):>7}")

    if a.dicionario:
        vistas: dict[str, list[str]] = {}
        for arq in arquivos:
            vistas.setdefault(arq["tabela"], arq["colunas"])
        for tabela, colunas in vistas.items():
            print(f"\n{tabela}:")
            for c in colunas:
                marca = "canônica" if c.strip().lower() in CANONICAS else "extras"
                print(f"  [{marca}] {c}")

    if a.saida:
        gravar(itens, arquivos, Path(a.saida), a.versao_cnj, raiz.name)
        print(f"gravado: {a.saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
