# -*- coding: utf-8 -*-
"""forja_anonimizar.py — tira nome de cliente do motor sem perder a lição.

O problema que este módulo resolve. A doutrina da FORJA é boa justamente porque
cada regra está amarrada a uma falha que aconteceu de verdade: "o modo de falha
do CASO-19, Lição 48" vale mais do que "evite gerar dois DOCX parecidos".
Só que o motor vai ser compartilhado com outros advogados e depois aberto, e
nome de cliente não pode ir junto. Apagar a âncora salvaria o sigilo e mataria a
doutrina.

A saída é substituir o nome por um pseudônimo estável e guardar a tradução no
acervo. Quem tem o acervo lê "CASO-07" e sabe qual é; quem não tem lê uma lição
com âncora concreta e rastreável, que continua sendo melhor do que uma regra
abstrata. O mapa de tradução é dado de cliente e por isso mora em
`state/FRONTEIRA_PSEUDONIMOS.json`, junto com o registro de nomes.

O que este módulo NÃO faz, e é deliberado:

  - Não renomeia arquivo. Há módulos com o nome do caso no próprio nome, e
    renomeá-los quebra import, manifesto de hash e referência em teste. Quando
    o nome do cliente está no nome do arquivo, este módulo reporta e para, para
    que a decisão fique com quem consegue conferir o que quebra.
  - Não toca em identificador de código. As chaves de âncora de
    `BASELINE_APROVADO.json` vivem presas por hash na régua; trocá-las em massa
    romperia a cadeia sem que ninguém visse. Identificadores entram na lista de
    pendências, não na substituição automática.
  - Não mexe no acervo. Lá o nome verdadeiro é o certo.

Uso:
    python forja_anonimizar.py --seco            # mostra o que faria
    python forja_anonimizar.py --gerar-mapa      # (re)cria o mapa no acervo
    python forja_anonimizar.py --aplicar         # reescreve os arquivos
    python forja_anonimizar.py --aplicar --so-texto   # só .md/.txt
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import forja_fronteira as fr

RAIZ_PADRAO = fr.RAIZ_PADRAO
MAPA = "_FORJA_HARNESS/state/FRONTEIRA_PSEUDONIMOS.json"
ESTRUTURAIS = "_FORJA_HARNESS/state/FRONTEIRA_ESTRUTURAIS.json"

# Variantes do mesmo cliente recebem o mesmo pseudônimo. Sem essa consolidação
# três grafias do mesmo nome viram três casos distintos na doutrina, e
# uma lição sobre um caso passa a parecer três lições sobre três.
#
# O agrupamento vive no acervo: escrever as variantes aqui colocaria a lista de
# clientes dentro do próprio módulo que existe para tirá-la do motor.
FAMILIAS_ORIGEM = "_FORJA_HARNESS/state/FRONTEIRA_FAMILIAS.json"


def carregar_familias(raiz: Path) -> dict[str, list[str]]:
    caminho = raiz / FAMILIAS_ORIGEM
    if not caminho.exists():
        return {}
    try:
        d = json.loads(caminho.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {k: list(v) for k, v in (d.get("familias") or {}).items()}

def _pseudonimo(indice: int) -> str:
    return f"CASO-{indice:02d}"


def gerar_mapa(raiz: Path) -> dict:
    """Atribui um pseudônimo estável por família, em ordem alfabética."""
    origem = carregar_familias(raiz)
    if not origem:
        raise SystemExit(
            f"REPROVADO — {FAMILIAS_ORIGEM} não existe. O agrupamento de "
            "variantes vive no acervo; sem ele não há como gerar o mapa.")
    entradas = {}
    for i, chave in enumerate(sorted(origem), start=1):
        pseudo = _pseudonimo(i)
        # Variantes ordenadas da mais longa para a mais curta: substituir
        # o nome curto antes do composto deixaria metade do nome no texto.
        entradas[chave] = {
            "pseudonimo": pseudo,
            "variantes": sorted(origem[chave], key=len, reverse=True),
        }
    return {
        "schema": "FORJA-FRONTEIRA-PSEUDONIMOS-v1",
        "porque": ("Tradução entre o pseudônimo usado na doutrina do motor e o "
                   "nome real do caso. É dado de cliente e por isso vive no "
                   "acervo; o motor não guarda nenhuma das duas pontas juntas."),
        "familias": entradas,
    }


def carregar_mapa(raiz: Path) -> list[tuple[re.Pattern, str, str]]:
    """Lê o mapa e devolve (padrão, pseudônimo, variante) em ordem de aplicação."""
    caminho = raiz / MAPA
    if not caminho.exists():
        return []
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    regras: list[tuple[re.Pattern, str, str]] = []
    for entrada in dados.get("familias", {}).values():
        pseudo = entrada["pseudonimo"]
        for variante in entrada["variantes"]:
            partes = [re.escape(p) for p in variante.split()]
            # A barra entra como separador porque a doutrina escreve o nome
            # composto tanto com barra quanto com espaço.
            padrao = re.compile(r"\b" + r"[\s\-/]+".join(partes) + r"\b",
                                0 if fr._e_ambiguo(variante) else re.I)
            regras.append((padrao, pseudo, variante))
    # Mais longas primeiro, globalmente: o composto antes do curto,
    # inclusive quando estão em famílias diferentes.
    regras.sort(key=lambda r: len(r[2]), reverse=True)
    return regras


def _e_ocorrencia_em_identificador(linha: str, inicio: int, fim: int) -> bool:
    """A ocorrência está colada em símbolo, caminho ou chave?

    Julgar pelo caractere vizinho não funciona, e as duas tentativas erraram em
    direções opostas: tratar todo `.` como identificador deixou o nome seguido de ponto
    intacto no fim da frase, e tratar toda `/` como caminho deixou o nome composto com barra
    intacto, que é prosa com barra no sentido de "ou".

    O que decide é o TOKEN inteiro em volta da ocorrência, delimitado por espaço
    ou aspas. Ele é identificador quando traz marca de caminho ou de símbolo:
    contrabarra, sublinhado, extensão de arquivo, ou mais de uma barra.
    """
    delim = " \t\"'`(),;:!?«»[]{}"
    i = inicio
    while i > 0 and linha[i - 1] not in delim:
        i -= 1
    j = fim
    while j < len(linha) and linha[j] not in delim:
        j += 1
    token = linha[i:j]

    if "\\" in token or "_" in token:
        return True
    if re.search(r"\.[A-Za-z0-9]", token):
        return True
    if token.count("/") >= 2:
        return True
    # Uma barra só, entre duas palavras, é prosa. Uma barra colada a algo que
    # já parece caminho foi coberta acima.
    # O pseudônimo tem hífen. Sem tirá-lo antes do teste, a segunda ocorrência
    # da mesma linha vira "identificador" só porque a primeira já foi trocada —
    # foi assim que um nome composto ficou trocado pela metade.
    token = re.sub(r"CASO-\d{2}", "", token)
    if "-" in token and " " not in token and re.search(r"[A-Za-z0-9]-[A-Za-z0-9]", token):
        return True
    return False


def mascarar_estruturais(texto: str, registro: dict) -> tuple[str, int]:
    """Troca número CNJ e inscrição na OAB por valor sintético estável.

    O número mascarado mantém o formato, porque em vários pontos a doutrina
    ensina sobre o próprio formato — a Lição 27 explica como converter a
    numeração `UF999999` da certidão do STJ na forma `OAB/UF 99.999`, e apagar
    o número mataria a lição. O que muda é só o dígito, e a tradução fica no
    acervo.
    """
    trocas = 0

    def _proximo(chave: str, moldar) -> str:
        """Valor mascarado estável para `chave`, criado na primeira vez.

        `moldar` recebe o índice e devolve o texto. É função, e não string de
        formato, porque a largura dos campos importa: o sequencial do CNJ tem
        exatamente sete dígitos, e a primeira versão, que usava um dígito livre,
        produzia números de oito a partir do décimo caso — nenhum leitor de CNJ
        reconhece isso, e cinco testes caíram de uma vez.
        """
        if chave not in registro:
            registro[chave] = moldar(len(registro) + 1)
        return registro[chave]

    def _cnj(m):
        """Mascara só o que identifica o processo.

        A primeira versão zerava o número inteiro e quebrou cinco testes de uma
        vez: `tribunal_do_cnj` lê o segmento e o tribunal de dentro do próprio
        número, e um CNJ todo zerado deixa de dizer que é TJRJ. O que identifica
        o caso é o sequencial; segmento, tribunal e ano dizem apenas qual corte
        e quando, e são exatamente o que a doutrina e os testes precisam.
        """
        nonlocal trocas
        valor = m.group(0)
        if fr.e_sintetico(valor):
            return valor
        trocas += 1
        _, resto = valor.split("-", 1)
        _dv, ano, seg, trib, _origem = resto.split(".")
        return _proximo("CNJ:" + valor,
                        lambda i: f"9{i:06d}-00.{ano}.{seg}.{trib}.0000")

    def _oab(m):
        nonlocal trocas
        valor = m.group(0)
        if fr.e_sintetico(valor):
            return valor
        uf = re.search(r"OAB[/\s-]*([A-Z]{2})", valor, re.I)
        sigla = uf.group(1).upper() if uf else "DF"
        trocas += 1
        return _proximo("OAB:" + valor,
                        lambda i: f"OAB/{sigla} {90 + i // 1000}.{i % 1000:03d}")

    texto = fr.RE_CNJ.sub(_cnj, texto)
    texto = fr.RE_OAB.sub(_oab, texto)
    return texto, trocas


def anonimizar_texto(texto: str, regras) -> tuple[str, int, list[str]]:
    """Substitui em prosa. Devolve (novo_texto, trocas, pendências)."""
    trocas = 0
    pendencias: list[str] = []
    linhas = texto.splitlines(keepends=True)
    for i, linha in enumerate(linhas):
        nova = linha
        for padrao, pseudo, variante in regras:
            saida = []
            fim_anterior = 0
            mudou = False
            for m in padrao.finditer(nova):
                if _e_ocorrencia_em_identificador(nova, m.start(), m.end()):
                    pendencias.append(f"identificador: {m.group(0)!r}")
                    continue
                saida.append(nova[fim_anterior:m.start()])
                saida.append(pseudo)
                fim_anterior = m.end()
                trocas += 1
                mudou = True
            if mudou:
                saida.append(nova[fim_anterior:])
                nova = "".join(saida)
        linhas[i] = nova
    texto_novo = "".join(linhas)
    # Duas partes do mesmo caso e viram o mesmo pseudônimo,
    # o que deixaria o pseudônimo repetido no meio da doutrina.
    texto_novo = re.sub(r"\b(CASO-\d{2})\s*[/×x]\s*\1\b", r"\1", texto_novo)
    return texto_novo, trocas, pendencias


def percorrer(raiz: Path, so_texto: bool = False, estruturais: bool = False):
    """Arquivos do MOTOR que carregam nome, na ordem em que serão tratados."""
    nomes, modo = fr.carregar_nomes(raiz)
    padroes = {n: fr._padrao_de_nome(n) for n in nomes}
    extensoes = {".md", ".txt"} if so_texto else fr.TEXTO
    for p in sorted(raiz.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(raiz).as_posix()
        if fr.classificar(rel)[0] != fr.MOTOR:
            continue
        if p.suffix.lower() not in extensoes:
            continue
        try:
            texto = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        sinais = fr.sinais_no_texto(texto, nomes, padroes)
        interessa = ("NOME:", "CNJ:", "OAB:") if estruturais else ("NOME:",)
        if not any(s.startswith(interessa) for s in sinais):
            continue
        yield p, rel, texto


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--raiz", type=Path, default=RAIZ_PADRAO)
    ap.add_argument("--gerar-mapa", action="store_true")
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--seco", action="store_true")
    ap.add_argument("--so-texto", action="store_true",
                    help="restringe a .md e .txt, para separar o risco")
    ap.add_argument("--estruturais", action="store_true",
                    help="também mascara número CNJ e inscrição na OAB")
    args = ap.parse_args(argv)

    if args.gerar_mapa:
        mapa = gerar_mapa(args.raiz)
        destino = args.raiz / MAPA
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(json.dumps(mapa, ensure_ascii=False, indent=2),
                           encoding="utf-8")
        print(f"{len(mapa['familias'])} família(s) em {MAPA}")
        for chave, e in mapa["familias"].items():
            print(f"   {e['pseudonimo']}  {chave}: {', '.join(e['variantes'])}")
        return 0

    regras = carregar_mapa(args.raiz)
    if not regras:
        print(f"REPROVADO — {MAPA} não existe. Rode --gerar-mapa primeiro.")
        return 1

    caminho_est = args.raiz / ESTRUTURAIS
    registro_est: dict = {}
    if caminho_est.exists():
        registro_est = json.loads(caminho_est.read_text(encoding="utf-8")).get("mapa", {})

    total_trocas = 0
    total_arquivos = 0
    pendentes: dict[str, list[str]] = {}
    for p, rel, texto in percorrer(args.raiz, so_texto=args.so_texto,
                                   estruturais=args.estruturais):
        novo, trocas, pend = anonimizar_texto(texto, regras)
        if args.estruturais:
            novo, extra = mascarar_estruturais(novo, registro_est)
            trocas += extra
        if pend:
            pendentes[rel] = sorted(set(pend))
        # A condição é "o texto mudou", e não "houve troca de nome": a limpeza
        # do pseudônimo repetido altera o arquivo sem contar troca, e enquanto a
        # condição olhava o contador ela nunca era gravada.
        if novo != texto:
            total_arquivos += 1
            total_trocas += trocas
            print(f"  {trocas:4d}  {rel}")
            if args.aplicar and not args.seco:
                p.write_text(novo, encoding="utf-8")

    if args.estruturais and registro_est and args.aplicar and not args.seco:
        caminho_est.parent.mkdir(parents=True, exist_ok=True)
        caminho_est.write_text(json.dumps(
            {"schema": "FORJA-FRONTEIRA-ESTRUTURAIS-v1",
             "porque": ("Tradução entre o número mascarado que aparece na "
                        "doutrina do motor e o número real do processo ou da "
                        "inscrição. É dado de cliente e vive no acervo."),
             "mapa": registro_est}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{len(registro_est)} número(s) mascarado(s) em {ESTRUTURAIS}")

    print(f"\n{total_trocas} troca(s) em {total_arquivos} arquivo(s)"
          + ("" if args.aplicar and not args.seco else "  [seco]"))
    if pendentes:
        print(f"\n{len(pendentes)} arquivo(s) com nome dentro de identificador,"
              " que este módulo não troca — decida um a um:")
        for rel, itens in list(pendentes.items())[:30]:
            print(f"  {rel}: {', '.join(sorted(set(itens))[:4])}")
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
