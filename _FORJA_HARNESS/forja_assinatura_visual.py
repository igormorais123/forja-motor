# -*- coding: utf-8 -*-
"""FORJA — gate F8-S: assinatura visual completa (Onda 3, modo observação).

Contraparte AFIRMATIVA do QA visual. O `forja_visual_qa` procura DEFEITO
(markdown vazado, marcador literal, colisão, clipping); nada nele pergunta se
os elementos EXISTEM. Uma peça de texto corrido, sem um único destaque, passa
limpa nele — porque não há nada quebrado para achar. Foi assim que as entregas
de 10/07 a 30/07/2026 saíram pobres com sinal verde.

Este módulo verifica PRESENÇA, lendo o DOCX final (não o markdown, não o mapa:
o que vale é o que está no arquivo que vai ao destinatário).

Taxonomia (auditoria do Igor, 30/07/2026):
    VIS-02 síntese inicial ausente ou fraca
    VIS-03 argumento principal sem visualização
    VIS-04 leitura transversal insuficiente
    VIS-05 deriva de identidade visual
    VIS-06 excesso ou decoração sem função
    VIS-11 síntese de fechamento ausente

MODO. `avaliar()` só descreve. Quem decide bloquear é o chamador, e hoje
ninguém bloqueia: a ordem do Igor é não travar a produção antes de a qualidade
estar comprovada nas peças de conferência.
"""
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

FORJA = Path(__file__).resolve().parent

PETROLEO = "395C60"
TERRACOTA = "D9926A"
PAINEL = "EFF4F3"

# Densidade calibrada por extensão (auditoria do Igor, 30/07/2026): peça de 4
# páginas e de 31 não podem ter a mesma régua. (min_figuras, min_destaques).
FAIXAS = ((5, 1, 1), (12, 2, 2), (25, 3, 4), (10**6, 4, 6))

# Régua usada quando não se sabe a extensão. É a faixa de 12 páginas, e o laudo
# declara `densidadeCalibrada: false` para que ninguém leia "conforme" como
# "conferido contra o tamanho da peça".
PAGINAS_NEUTRAS = 10


def _faixa(paginas):
    for limite, figs, destaques in FAIXAS:
        if paginas <= limite:
            return figs, destaques
    return FAIXAS[-1][1], FAIXAS[-1][2]


def paginas_reais(docx):
    """Contagem FÍSICA de páginas, e só ela. Devolve None quando não há prova.

    Por que não estimar. Em 04/08/2026 a `FAIXAS` estava inerte: a única rota
    viva chamava `avaliar(destino, None, tipo)`, então toda peça — de 4 ou de 40
    páginas — era medida contra a faixa neutra. A constante existia, estava
    documentada e nunca era consultada com valor real: catraca decorativa.

    A saída óbvia seria estimar a extensão pelo tamanho do texto. Foi tentada e
    **medida contra 269 pares DOCX/PDF reais do acervo**, que é âncora externa e
    não o próprio gate. O melhor estimador (caracteres ÷ 3.800) acerta a faixa de
    densidade em **60%** dos casos. Numa régua de quatro faixas, errar 40% faria
    o gate exigir quatro figuras de uma peça de seis páginas — precisamente o
    falso positivo que travaria peça com prazo, que é o risco que adiou a
    ativação do bloqueio.

    Continuar mexendo na heurística até a taxa agradar seria a autovalidação que
    esta frente existe para quebrar. Então: usa-se o fato quando ele existe (há
    PDF ao lado do DOCX, e aí a contagem é exata) e declara-se a ignorância
    quando não existe. Régua neutra com aviso é honesta; régua estimada com
    aparência de precisão não é.
    """
    try:
        import fitz
    except ImportError:
        return None
    pdf = Path(docx).with_suffix(".pdf")
    if not pdf.is_file():
        return None
    try:
        with fitz.open(pdf) as documento:
            return documento.page_count or None
    except Exception:
        return None


# sz=24 exato: é o valor que `PecaVisual._caixa` e a faixa de síntese usam. A
# faixa 2[0-9] admitia bordas de outros contextos (achado da rodada 2 do Codex).
# Medido no acervo: os únicos sz de borda esquerda presentes são 6 e 24.
_BARRA_CAIXA = re.compile(r'<w:left[^>]*w:val="single"[^>]*w:sz="24"')
# O timbre do escritório é ARTE VETORIAL desenhada no cabeçalho, não imagem
# embutida: nenhum header*.xml referencia `a:blip` ou `r:embed`. Procurar imagem
# em `word/media/` media outra coisa — um diagrama no corpo satisfazia o teste
# (achado da rodada 2 do Codex).
#
# Detectar por COR também não serve: a arte usa 3a5c61 e d9936a, um dígito fora
# dos tokens da paleta (395C60 e D9926A). A diferença é da própria arte, não
# defeito da peça — e um gate calibrado por ela quebraria na primeira revisão da
# marca. Por isso a prova é a presença de DESENHO no cabeçalho, que é o que
# distingue a peça nascida do template daquela nascida de Document() vazio.
_ARTE_TIMBRE = re.compile(r"(a:blip|r:embed|<v:shape|<v:group|<w:drawing|a:prstGeom)")


def _tabelas(doc, todos_os_niveis=False):
    """Blocos <w:tbl>…</w:tbl>.

    Fatiamento por profundidade em vez de regex: `<w:tbl>.*?</w:tbl>` casa o
    primeiro fechamento e, em tabela aninhada, devolve um bloco truncado —
    deixando o miolo da tabela interna no texto (achado A-7, rodada 1).

    Por padrão devolve só o primeiro nível, que é o correto para EXCLUIR
    tabelas do cálculo de negrito (o bloco de nível 1 já contém as internas).
    Para CONTAR caixas é preciso `todos_os_niveis=True`, senão uma caixa
    aninhada fica invisível (achado da rodada 2). No acervo medido não há
    aninhamento, mas a assimetria era real."""
    blocos, pilha = [], []
    for m in re.finditer(r"<w:tbl>|</w:tbl>", doc):
        if m.group(0) == "<w:tbl>":
            pilha.append(m.start())
        elif pilha:
            ini = pilha.pop()
            if todos_os_niveis or not pilha:
                blocos.append(doc[ini:m.end()])
    return blocos


def _caixas(doc):
    """Tabelas cuja assinatura é a barra lateral grossa das caixas de destaque
    (acórdão, precedente, chave) e da faixa de síntese."""
    return sum(1 for t in _tabelas(doc, todos_os_niveis=True)
               if _BARRA_CAIXA.search(t))


_REL = re.compile(r'<Relationship\b[^>]*Id="([^"]+)"[^>]*Target="([^"]+)"', re.I)
_REL_ALT = re.compile(r'<Relationship\b[^>]*Target="([^"]+)"[^>]*Id="([^"]+)"', re.I)
_REF_NO_CORPO = re.compile(r'r:(?:embed|link|id)="([^"]+)"')


def _figuras_exibidas(z, doc, nomes):
    """Figuras vetoriais REFERENCIADAS pelo documento — não arquivos no pacote.

    Contar `word/media/*.emf` era falso negativo demonstrado: em 04/08/2026,
    copiar quatro EMF órfãos para dentro do pacote de uma peça reprovada, sem
    referenciá-los em lugar nenhum e sem que aparecessem na página, virou o
    veredito de reprovada para CONFORME. O gate contava arquivo presente, não
    figura exibida — e essas duas coisas se separam com um comando de cópia.

    A prova correta é a cadeia de relacionamento: o corpo cita um `r:embed`, o
    `document.xml.rels` resolve aquele id para um alvo em `media/`, e só então a
    figura existe para o leitor.
    """
    rels_nome = "word/_rels/document.xml.rels"
    if rels_nome not in nomes:
        return []
    rels_xml = z.read(rels_nome).decode("utf-8", "replace")
    alvo_por_id = {rid: alvo for rid, alvo in _REL.findall(rels_xml)}
    for alvo, rid in _REL_ALT.findall(rels_xml):   # ordem dos atributos varia
        alvo_por_id.setdefault(rid, alvo)

    presentes = set(nomes)
    exibidas = set()
    for rid in _REF_NO_CORPO.findall(doc):
        alvo = alvo_por_id.get(rid, "")
        if not alvo.lower().endswith((".emf", ".wmf")):
            continue
        # O alvo é relativo a `word/`. Referência sem arquivo é figura quebrada:
        # o Word mostra o quadro vazio com o X. Contá-la seria dar por presente
        # uma figura que o julgador não vê — foi o segundo falso negativo que o
        # canário anti-moldagem pegou, minutos depois de corrigido o primeiro.
        caminho = alvo.replace("\\", "/").lstrip("./")
        completo = caminho if caminho.startswith("word/") else f"word/{caminho}"
        if completo in presentes:
            exibidas.add(completo)
    return sorted(exibidas)


def _inventario(docx):
    """Conta os elementos no DOCX final, direto do pacote."""
    docx = Path(docx)
    with zipfile.ZipFile(docx) as z:
        nomes = z.namelist()
        doc = z.read("word/document.xml").decode("utf-8", "replace")
        headers = "".join(z.read(n).decode("utf-8", "replace")
                          for n in nomes if re.match(r"word/header\d*\.xml$", n))
        vetoriais = _figuras_exibidas(z, doc, nomes)
    media = [n for n in nomes if n.startswith("word/media/")]
    orfas = len([n for n in media if n.lower().endswith((".emf", ".wmf"))]) - len(vetoriais)

    # Negrito medido em CARACTERES do corpo, não em contagem de runs. Duas
    # razões: um run pode ter uma palavra ou um parágrafo inteiro, e o filtro
    # por tamanho de fonte selecionava um subconjunto minúsculo como
    # denominador, produzindo razões absurdas (27.500% no Libra recomposto).
    # Também se excluem os runs de tabela e de moldura, onde o negrito é
    # estrutural (cabeçalho, rótulo) e não ênfase — foi a correção que prometi
    # ao rejeitar a proposta de tirar o negrito do padrão.
    corpo_xml = doc
    for bloco in _tabelas(doc):          # remoção por profundidade (ver _tabelas)
        corpo_xml = corpo_xml.replace(bloco, "")
    runs = re.findall(r"<w:r\b.*?</w:r>", corpo_xml, re.S)

    def _chars(run):
        return sum(len(t) for t in re.findall(r"<w:t[^>]*>(.*?)</w:t>", run, re.S))

    total_chars = sum(_chars(r) for r in runs)
    negrito_chars = sum(_chars(r) for r in runs
                        if re.search(r"<w:b\s*/>|<w:b\s+[^>]*w:val=\"(?:1|true)\"", r))
    negrito = sum(1 for r in runs
                  if re.search(r"<w:b\s*/>|<w:b\s+[^>]*w:val=\"(?:1|true)\"", r))

    return {
        "paginas_estimadas": None,
        # Figuras que o leitor VÊ (referenciadas pelo corpo), não arquivos no zip.
        "imagensVetoriais": len(vetoriais),
        # Vetoriais presentes no pacote e não referenciadas por ninguém. Zero é o
        # normal; número alto é sinal de lixo de montagem — ou de alguém tentando
        # satisfazer o gate por cópia de arquivo.
        "vetoriaisOrfas": max(0, orfas),
        "imagensRaster": len([n for n in media
                              if not n.lower().endswith((".emf", ".wmf"))]),
        "tabelas": doc.count("<w:tbl>"),
        "shading": len(re.findall(r'w:shd\s[^>]*w:fill="(?!auto)', doc)),
        # Caixas de destaque, contadas por TABELA e pela assinatura correta.
        #
        # A versão anterior casava `<w:tcBorders><w:top w:val="nil"`, que é o
        # padrão de QUALQUER célula sem borda superior — inclusive as do quadro
        # zebrado. Na peça de referência isso contava 13 onde havia 3 caixas
        # reais, e em documento cheio de tabela chegava a 672. A métrica não
        # media o que dizia medir (achado A-1 da revisão cruzada Codex,
        # 03/08/2026, confirmado por inspeção do XML).
        #
        # A assinatura real de uma caixa (`PecaVisual._caixa`) e da faixa de
        # síntese é a borda ESQUERDA grossa: `<w:left w:val="single" w:sz="24">`.
        # Conta-se por tabela, não por célula: a síntese tem uma barra por
        # linha e contá-las inflaria o total.
        "caixas": _caixas(doc),
        "bordas": doc.count("<w:pBdr>"),
        "frames": doc.count("<w:framePr"),
        "runs": len(runs),
        "runsNegrito": negrito,
        "caracteresCorpo": total_chars,
        "razaoNegrito": round(negrito_chars / max(1, total_chars), 4),
        "petroleo": doc.count(PETROLEO) + headers.count(PETROLEO),
        "terracota": doc.count(TERRACOTA) + headers.count(TERRACOTA),
        # Timbre: arte institucional NO CABEÇALHO. Antes bastava haver qualquer
        # imagem no pacote e cabeçalho não-vazio — um diagrama no corpo já
        # satisfazia. Agora exige que o próprio header traga imagem ou a paleta
        # da casa, que é como o timbre vetorial é desenhado. Na prática, prova
        # que a peça nasceu do template do escritório, e não de Document() vazio.
        "timbre": bool(_ARTE_TIMBRE.search(headers)),
        "primeiroBlocoTabela": doc.find("<w:tbl>") >= 0
                               and doc.find("<w:tbl>") < len(doc) * 0.35,
    }


def avaliar(docx, paginas=None, tipo="peca"):
    """Devolve o laudo de assinatura visual. Não bloqueia — só descreve."""
    inv = _inventario(docx)
    origem_paginas = "parametro_do_chamador" if paginas is not None else "desconhecida"
    if paginas is None:
        paginas = paginas_reais(docx)
        if paginas is not None:
            # O módulo apenas lê um PDF já existente ao lado do DOCX para obter
            # a contagem física. A FORJA não cria PDF nem chama renderizador.
            origem_paginas = "pdf_existente_ao_lado"
    inv["paginas_estimadas"] = paginas
    min_figs, min_destaques = _faixa(paginas or PAGINAS_NEUTRAS)
    # Só conta o que é destaque ARGUMENTATIVO: moldura de margem (pull quote e
    # nota lateral) e caixa. Borda de parágrafo isolada é filete de seção e
    # fólio — decoração estrutural, presente até em peça de texto corrido.
    destaques = inv["frames"] + inv["caixas"]
    achados = []

    def falta(codigo, o_que, encontrado, esperado):
        achados.append({"codigo": codigo, "elemento": o_que,
                        "encontrado": encontrado, "esperado": esperado})

    if not inv["timbre"]:
        falta("VIS-05", "timbre institucional no cabeçalho", 0, 1)
    if not inv["primeiroBlocoTabela"]:
        falta("VIS-02", "síntese de abertura em tabela (no primeiro terço)", 0, 1)
    if inv["imagensVetoriais"] < min_figs:
        falta("VIS-03", "elemento gráfico vetorial", inv["imagensVetoriais"], min_figs)
    if destaques < min_destaques:
        falta("VIS-04", "destaques de varredura (pull quote e caixa)",
              destaques, min_destaques)
    if inv["tabelas"] < 2:
        falta("VIS-11", "quadros estruturados (abertura e fechamento)",
              inv["tabelas"], 2)
    if not (0.02 <= inv["razaoNegrito"] <= 0.20):
        falta("VIS-04", "negrito estratégico fora da banda (2% a 20% do corpo)",
              f"{inv['razaoNegrito']:.1%}", "2% a 20%")
    if inv["petroleo"] == 0 or inv["terracota"] == 0:
        falta("VIS-05", "paleta institucional (petróleo e terracota)",
              f"pet={inv['petroleo']}/ter={inv['terracota']}", "ambas")
    # excesso: figura a cada menos de 2 páginas é decoração
    if paginas and inv["imagensVetoriais"] > max(4, paginas // 2):
        falta("VIS-06", "excesso de elementos gráficos",
              inv["imagensVetoriais"], f"<= {max(4, paginas // 2)}")

    return {
        "docx": str(docx),
        "tipoProduto": tipo,
        "paginas": paginas,
        # Sem isto, "conforme" com régua neutra é indistinguível de "conforme"
        # medido contra a extensão real — e a `FAIXAS` volta a ser decorativa
        # sem que ninguém perceba.
        "densidadeCalibrada": paginas is not None,
        "origemPaginas": origem_paginas,
        "faixaDensidade": {"minFiguras": min_figs, "minDestaques": min_destaques},
        "inventario": inv,
        "conforme": not achados,
        "achados": achados,
        "modo": "observacao",
        "observacao": ("Gate F8-S em modo observação por ordem do Igor "
                       "(30/07/2026): registra o que reprovaria, não bloqueia. "
                       "A ativação bloqueante depende de conferência humana das "
                       "peças de calibração."),
    }


def main():
    ap = argparse.ArgumentParser(description="Gate F8-S — assinatura visual (observação)")
    ap.add_argument("docx")
    ap.add_argument("--paginas", type=int, default=None)
    ap.add_argument("--tipo", default="peca")
    ap.add_argument("--saida", default=None)
    args = ap.parse_args()
    laudo = avaliar(args.docx, args.paginas, args.tipo)
    if args.saida:
        Path(args.saida).write_text(json.dumps(laudo, ensure_ascii=False, indent=2),
                                    encoding="utf-8")
    print(json.dumps(laudo, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
