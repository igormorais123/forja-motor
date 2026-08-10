# -*- coding: utf-8 -*-
"""forja_licoes.py — o índice das lições da casa, e o que cada uma faz reprovar.

A queixa que originou este módulo é a de que o sistema esquece. Medido em
10/08/2026, o esquecimento tem forma e tamanho:

* `RETROSPECTIVAS.md` tem **382 lições** em 1.104 linhas, num arquivo que só se
  consulta lendo inteiro. Ninguém lê 1.104 linhas antes de escrever uma função.
* **48 números querem dizer duas coisas** — até cinco, num caso. "Lição 87" é
  uma lição e é outra lição, porque a numeração foi reiniciada ao longo do
  tempo. Isso não é desarrumação cosmética: torna **ambígua toda citação por
  número**, inclusive as que já estão no código.
* Apenas **27 lições (7%)** têm o número citado em código, teste ou contrato de
  fase, e **9 dessas citações apontam para número duplicado**. Para as demais
  não há como responder "isto já virou gate?" — e o que não se consegue
  responder, alguém redescobre e reescreve. Aconteceu duas vezes só nesta
  semana.

O que este módulo NÃO faz, de propósito: renumerar. Reescrever 1.104 linhas
quebraria toda citação existente e toda referência em conversa, commit e
documento — trocaria uma ambiguidade por uma invalidação geral. Em vez disso,
cada lição ganha um **identificador estável derivado do próprio título**, que
não depende de posição e não muda quando o arquivo cresce. É o mesmo desenho do
registro de regras aprendidas: a coisa recebe nome próprio, e a ligação com o
código passa a ser conferível nos dois sentidos.

O gate que sai daqui é estreito e verdadeiro: **citação ambígua reprova**. Não
se cobra que as 382 lições virem gate — muitas são julgamento humano e devem
continuar sendo. Cobra-se que, quando o código diz "Lição 87", exista uma só
Lição 87 para ele estar apontando.

Sobre os índices por tema e por rodada: eles são **gerados**, nunca mantidos à
mão. A casa já aprendeu, com a edição visual, que recurso dependente de esforço
manual por item para de ser alimentado na primeira semana movimentada — e um
índice desatualizado é pior que índice nenhum, porque tem aparência de ordem.
Guia de consulta em `licoes/LEIA-ME.md`.

Uso
    python forja_licoes.py                 # o retrato
    python forja_licoes.py --temas         # quantas lições em cada tema
    python forja_licoes.py --tema visual   # as lições de um tema
    python forja_licoes.py --buscar prazo  # acha a lição pelo assunto
    python forja_licoes.py --ambiguas      # só as citações que não decidem
    python forja_licoes.py --orfas         # lições sem nada que as faça valer
    python forja_licoes.py --documentar    # reescreve os índices em licoes/
    python forja_licoes.py --indexar       # grava o índice legível por máquina
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
PASTA = FORJA / "licoes"
TEMATICO = PASTA / "INDICE_TEMATICO.md"
CRONOLOGICO = PASTA / "INDICE_CRONOLOGICO.md"

VERSAO = "FORJA-LICOES-v1"

# Os dois formatos que convivem no arquivo. Ler só um subestimaria o corpus pela
# metade — a primeira contagem que fiz devolveu 7 lições de 321 por isso.
_NOMEADA = re.compile(r"\*\*Liç(?:ão|ao)\s+(\d{1,3})\s*[—–-]\s*(.+?)\*\*")
_NUMERADA = re.compile(r"^\s*(\d{1,3})\.\s+\*\*(.+?)\*\*", re.M)

# Onde uma lição pode estar ancorada: algo que reprova se ela for violada.
_CITACAO = re.compile(r"[Ll]i[çc][ãa]o\s+(\d{1,3})")
_ONDE_ANCORAR = ("*.py", "phase_contracts/*.json", "templates/*.md")

# O arquivo é dividido por rodada de trabalho: um caso, uma auditoria, um ciclo.
# A seção é a única proveniência que a lição carrega — de onde ela veio e quando.
_SECAO = re.compile(r"^##\s+(.+?)\s*$", re.M)
_DATA = re.compile(r"(\d{2}/\d{2}/\d{4})")

# Vocabulário temático. É declarado, não inferido: cada tema existe porque um
# punhado de lições da casa fala dele, e o termo que o identifica foi tirado do
# texto delas. Uma lição pode ter vários temas — a maioria tem, porque um erro
# real raramente é de uma coisa só. O que não pode é o tema virar rótulo vago:
# termo que casaria em quase tudo (`lição`, `regra`, `caso`) fica de fora de
# propósito, porque tema que classifica todo mundo não classifica ninguém.
# Quanto do corpo conta como enunciado da tese, antes de passar a exigir
# repetição. Medido: 600 caracteres cobrem o título e a frase que o explica na
# esmagadora maioria das lições, sem alcançar o desenvolvimento.
ABERTURA = 600

TEMAS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("gate", "Gates: o que reprova e o que só parece reprovar",
     ("gate ", "gates ", "catraca", "teste de mutacao", "falso positivo",
      "contraprova", "reprovar o acerto", "overblocking", "teto medido")),
    ("lastro", "Lastro: afirmação conferida na fonte",
     ("lastro", "na fonte", "premissa", "verbatim", "nao conferid",
      "sem conferir", "afirmacao bem formada", "inferencia", "sem fonte",
      "fonte oficial", "alucinac", "inventad", "divergent")),
    ("citacao", "Citação, jurisprudência e dispositivo",
     ("precedente", "sumula", "acordao", "jurisprud", "misquote", "pincite",
      "ratio", "autoridade citada", "inventar autoridade", "dispositivo",
      "instituto juridico", "citac")),
    ("redacao", "Redação, estilo e cara de IA",
     ("cara de ia", "fecho", "estilo", "reescrita", "editorial", "prosa",
      "sintese executiva", "redator", "linguagem", "terminologia")),
    ("visual", "Visual law: figura, diagrama e diagramação",
     ("svg", "emf", "diagrama", "figura", "capa ", "visual law", "viewbox",
      "colisao", "tipograf", "render")),
    ("modelos", "Modelos, famílias e revisão cruzada",
     ("grok", "codex", "opus", "fable", "kimi", "glm", "familia de modelo",
      "bancada", "juiz cego", "revisao cruzada", "auto-preferencia")),
    ("processual", "Identidade processual e peça",
     ("agravo", "embargos", "cnj", "prevenc", "preclus", "sustentacao oral",
      "regimento", "orgao julgador", "identidade dos atos")),
    # Não há tema de prazo, e a ausência foi medida, não esquecida: a palavra
    # aparece na fábrica em "prazo de revalidação", "prazo interno", "prazo do
    # ciclo" — mais fora do assunto do que dentro. O tema devolvia três lições
    # e as três eram de outra coisa. Para prazo processual, `--buscar prazo`
    # acha as nove que existem; um rótulo errado seria pior que nenhum.
    ("entrega", "Entrega ao destinatário e comunicação",
     ("entrega", "e-mail", "destinatario", "protocolad", "reenvi",
      "relatorio de melhorias", "whatsapp")),
    ("aprendizado", "Retorno humano e aprendizado da casa",
     ("retorno humano", "correcao do titular", "regra adotada", "feedback",
      "quarentena", "aprendizado continuo", "recorrencia entre casos")),
    ("acoplamento", "Acoplamento: onde o código de fato passa",
     ("acopl", "chamador", "import", "rota unica", "quem grava",
      "instalado no fechamento", "rota que ninguem percorre")),
    ("estado", "Estado, artefatos e contratos de fase",
     ("phase_result", "contrato da fase", "censo", "ledger", "manifest",
      "artefato interno", "requiredgates", "idempot")),
    ("fronteira", "Fronteira, sigilo e proveniência",
     ("fronteira", "motor/acervo", "segredo", "sigilo", "dado pessoal",
      "injecao de prompt", "injecao indireta", "origem operacional",
      "proveniencia")),
    ("automacao", "Automação, agendamento e volume",
     ("agendad", "cron", "background", "esforco manual por caso",
      "varredura em massa", "backoff", "concorrenc")),
    ("evidencia", "Prova, atestado e o que conta como evidência",
     ("prova independente", "provar que", " prova ", "atestad", "recibo",
      "declarado nao e computado", "evidencia", "reproduz")),
    ("autoengano", "Autoengano e autovalidação",
     ("autoengano", "circularidade", "autovalidac", "autoatestac", "red team",
      "adversarial", "complacen", "bajulac", "quem constroi")),
)

_SEM_TEMA = "sem-tema"


def _plano(texto: str) -> str:
    """Minúscula sem acento, para o vocabulário não depender de grafia."""
    base = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in base if not unicodedata.combining(c))


def _temas(titulo: str, corpo: str) -> list[str]:
    """Os temas de que a lição TRATA, não os que ela menciona de passagem.

    A primeira versão marcava o tema à primeira ocorrência do termo, e `gate`
    caía em 49% do acervo — a palavra aparece de passagem em quase toda lição
    da casa. Rótulo que cabe em metade do corpus não ajuda ninguém a achar
    nada. Exigir repetição no corpo corrigiu isso e criou o defeito oposto:
    42% sem tema, porque a lição curta de uma linha não tem onde repetir termo
    algum — a régua punia o formato, não o assunto.

    A régua que ficou separa lição curta de lição longa, que é onde estava a
    assimetria real. O título vale sempre. No corpo, a lição de uma linha
    precisa de uma ocorrência — é tudo o que ela tem; a lição longa precisa de
    duas, porque um registro denso de rodada menciona meia dúzia de assuntos
    uma vez cada, e marcar todos põe a lição em seis temas sem ser de nenhum.
    """
    no_titulo = _plano(titulo)
    no_corpo = _plano(corpo)
    curta = len(corpo) <= ABERTURA
    achados = []
    for slug, _, termos in TEMAS:
        if any(t in no_titulo for t in termos):
            achados.append(slug)
            continue
        vezes = sum(no_corpo.count(t) for t in termos)
        if curta:
            if vezes:
                achados.append(slug)
        elif vezes >= 2 and any(t in no_corpo[:ABERTURA] for t in termos):
            achados.append(slug)
    return achados or [_SEM_TEMA]


def rotulo(slug: str) -> str:
    for s, r, _ in TEMAS:
        if s == slug:
            return r
    return "Sem tema atribuído pelo vocabulário"


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
    secao, data = "(antes da primeira seção)", ""
    for i, linha in enumerate(linhas, 1):
        cabeca = _SECAO.match(linha)
        if cabeca:
            secao = cabeca.group(1)
            achada = _DATA.search(secao)
            data = achada.group(1) if achada else data
        for regex in (_NOMEADA, _NUMERADA):
            m = regex.search(linha)
            if not m:
                continue
            titulo = m.group(2).strip().rstrip(".")
            achados.append({"numero": int(m.group(1)), "titulo": titulo,
                            "id": _ident(titulo), "linha": i,
                            "secao": secao, "data": data})
            break
    for atual, seguinte in zip(achados, achados[1:] + [None]):
        fim = (seguinte["linha"] - 1) if seguinte else len(linhas)
        atual["corpo"] = "\n".join(linhas[atual["linha"] - 1:fim]).strip()
        atual["temas"] = _temas(atual["titulo"], atual["corpo"])
    return achados


def por_tema(licoes: list[dict]) -> dict[str, list[dict]]:
    """Tema → lições, na ordem canônica do vocabulário e com o resto no fim."""
    mapa: dict[str, list[dict]] = {slug: [] for slug, _, _ in TEMAS}
    mapa[_SEM_TEMA] = []
    for lic in licoes:
        for t in lic["temas"]:
            mapa[t].append(lic)
    return {k: v for k, v in mapa.items() if v}


def por_secao(licoes: list[dict]) -> dict[str, list[dict]]:
    """Rodada de trabalho → lições, na ordem em que aconteceram."""
    mapa: dict[str, list[dict]] = {}
    for lic in licoes:
        mapa.setdefault(lic["secao"], []).append(lic)
    return mapa


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


_AVISO = (
    "> **Documento gerado.** Não edite aqui: a fonte é `RETROSPECTIVAS.md` e "
    "este arquivo é reescrito por `python forja_licoes.py --documentar`.\n")


def _linha_de_licao(lic: dict, citadas: dict, ambiguos: dict) -> str:
    n = lic["numero"]
    if n not in citadas:
        ancora = "—"
    elif n in ambiguos:
        ancora = "⚠ citada, mas o número é ambíguo"
    else:
        ancora = ", ".join(sorted(citadas[n]))
    data = lic["data"] or "—"
    return (f"| {n} | {data} | {lic['titulo']} | "
            f"[L{lic['linha']}](../RETROSPECTIVAS.md#L{lic['linha']}) | "
            f"{ancora} |")


_CABECA = ("| nº | data | lição | onde | o que a faz reprovar |\n"
           "|---:|---|---|---|---|")


def documentos(caminho: Path | None = None,
               raiz: Path | None = None) -> dict[Path, str]:
    """Os índices de consulta, em memória, a partir do arquivo de lições.

    São gerados, e não mantidos à mão, pela mesma razão que a casa já aprendeu
    com a edição visual: índice que custa trabalho manual por lição envelhece
    na primeira semana movimentada e passa a mentir com aparência de ordem.

    Devolve em vez de escrever para que o teste possa perguntar se o que está
    no disco ainda corresponde à fonte, sem reescrever nada para descobrir.
    """
    licoes = ler(caminho)
    citadas = citacoes(raiz)
    ambiguos = numeros_ambiguos(licoes)
    temas = por_tema(licoes)
    secoes = por_secao(licoes)

    # ---------- índice temático ----------
    t = [f"# Lições da FORJA — índice temático\n", _AVISO,
         f"\n{len(licoes)} lições em {len(temas)} temas. Uma lição aparece em "
         f"mais de um tema quando trata de mais de uma coisa (média de "
         f"{sum(len(x['temas']) for x in licoes) / max(1, len(licoes)):.1f} "
         f"por lição), então a soma das seções é maior que o total.\n",
         "\nO tema sai do texto da própria lição, por vocabulário declarado em "
         "`forja_licoes.py`. O termo no título vale sozinho; no corpo, a lição "
         "curta precisa de uma ocorrência e a longa de duas, uma delas na "
         "abertura — sem isso, um registro denso de rodada cai em seis temas "
         "por mencionar seis assuntos uma vez cada.\n",
         "\nÉ um mapa de navegação, não uma autoridade: leia a lição antes de "
         "citá-la. O tema diz onde procurar, não o que a lição decide.\n",
         "\n## Sumário\n\n| tema | lições |\n|---|---:|"]
    for slug, itens in temas.items():
        t.append(f"| [{rotulo(slug)}](#{slug}) | {len(itens)} |")
    for slug, itens in temas.items():
        t.append(f"\n<a id=\"{slug}\"></a>\n## {rotulo(slug)}\n")
        if slug == _SEM_TEMA:
            t.append("O vocabulário não alcançou estas. Não são lições piores "
                     "— são as que ninguém classificou ainda, e ficam "
                     "listadas para que a lacuna seja visível em vez de "
                     "silenciosa.\n")
        t.append(f"{len(itens)} lições.\n")
        t.append(_CABECA)
        for lic in sorted(itens, key=lambda x: x["linha"]):
            t.append(_linha_de_licao(lic, citadas, ambiguos))

    # ---------- índice cronológico ----------
    c = [f"# Lições da FORJA — índice por rodada de trabalho\n", _AVISO,
         f"\nCada seção do arquivo é uma rodada: um caso, uma auditoria, um "
         f"ciclo. São {len(secoes)} rodadas e {len(licoes)} lições. Este "
         f"índice responde \"o que aprendemos naquele dia\", que é a pergunta "
         f"de quem volta a um caso; o temático responde \"o que a casa já "
         f"sabe sobre isto\", que é a de quem vai escrever código novo.\n",
         "\n## Sumário\n\n| rodada | data | lições |\n|---|---|---:|"]
    for nome, itens in secoes.items():
        alvo = _ident(nome)
        c.append(f"| [{nome}](#{alvo}) | {itens[0]['data'] or '—'} | "
                 f"{len(itens)} |")
    for nome, itens in secoes.items():
        c.append(f"\n<a id=\"{_ident(nome)}\"></a>\n## {nome}\n")
        c.append(_CABECA)
        for lic in itens:
            c.append(_linha_de_licao(lic, citadas, ambiguos))

    # O índice legível por máquina entra aqui, e não num caminho próprio, para
    # ficar sob a mesma catraca: os três envelhecem juntos ou não envelhecem.
    # Sem o corpo das lições — com ele, o JSON viraria uma segunda cópia do
    # arquivo de origem, que passaria a divergir dele na edição seguinte.
    bruto = retrato(caminho, raiz)
    enxuto = {k: v for k, v in bruto.items() if k != "detalhe"}
    enxuto["itens"] = [{k: v for k, v in x.items() if k != "corpo"}
                       for x in bruto["itens"]]
    maquina = json.dumps(enxuto, ensure_ascii=False, indent=2) + "\n"

    return {TEMATICO: "\n".join(t) + "\n", CRONOLOGICO: "\n".join(c) + "\n",
            INDICE: maquina}


def documentar(caminho: Path | None = None,
               raiz: Path | None = None) -> list[Path]:
    """Escreve no disco os índices de `documentos()`."""
    escritos = []
    for arquivo, corpo in documentos(caminho, raiz).items():
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo.write_text(corpo, encoding="utf-8")
        escritos.append(arquivo)
    return escritos


def desatualizados(caminho: Path | None = None,
                   raiz: Path | None = None) -> list[Path]:
    """Índices cujo conteúdo no disco não é mais o que a fonte produz."""
    fora = []
    for arquivo, corpo in documentos(caminho, raiz).items():
        atual = (arquivo.read_text(encoding="utf-8")
                 if arquivo.exists() else None)
        if atual != corpo:
            fora.append(arquivo)
    return fora


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
    p.add_argument("--temas", action="store_true",
                   help="quantas lições há em cada tema")
    p.add_argument("--tema", metavar="SLUG", help="lista as lições de um tema")
    p.add_argument("--documentar", action="store_true",
                   help="reescreve os índices temático e cronológico")
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

    if a.temas or a.tema:
        agrupado = por_tema(r["itens"])
        if a.tema:
            itens = agrupado.get(a.tema)
            if itens is None:
                print(f"tema desconhecido: {a.tema!r}. Os que existem: "
                      f"{', '.join(agrupado)}")
                return 2
            for x in sorted(itens, key=lambda y: y["linha"]):
                print(f"  Lição {x['numero']:3d}  linha {x['linha']:5d}  "
                      f"{x['titulo'][:86]}")
            print(f"\n{len(itens)} em {rotulo(a.tema)}.")
            return 0
        for slug, itens in agrupado.items():
            print(f"  {slug:12s} {len(itens):4d}  {rotulo(slug)}")
        print(f"\n{r['licoes']} lições. Uma lição conta em mais de um tema "
              f"quando trata de mais de uma coisa.")
        return 0

    if a.documentar:
        for arquivo in documentar():
            print(f"gravado: {arquivo}")
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
        # Mesma rota do `--documentar`: um só gerador, para os três índices não
        # poderem discordar entre si sobre o que o arquivo de lições diz.
        for arquivo in documentar():
            print(f"gravado: {arquivo}")
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
