# -*- coding: utf-8 -*-
"""FORJA — geração automática do mapa visual declarativo (Onda 1A).

Motivação (diagnóstico 30/07/2026, plano 24): a edição visual law parou em
10/07/2026 porque `forja_visual.compor()` exige um mapa escrito à mão por caso.
Cinco mapas manuais existem; nenhum posterior. Recurso que depende de esforço
humano por caso não sobrevive ao volume — a constância exige que o mapa nasça
sozinho do markdown auditado.

REGRA DE OURO DESTE MÓDULO: nenhum texto novo é inventado. Toda pull quote,
linha-síntese e corpo de caixa é EXTRAÍDO verbatim do próprio markdown. O único
texto autoral são legendas de figura e rótulos de seção, que descrevem artefatos
nossos, não fatos do caso. Isso mantém a peça dentro da regra de que o editor
não cria fato, data, número, citação nem autoridade.

Contrato de saída: dicionário aceito por `forja_visual.compor(md, docx, mapa)`.

Uso:
    from forja_visual_mapa_gen import gerar_mapa
    mapa = gerar_mapa("peca.md")                 # dict pronto para compor()
    gravar_mapa("peca.md", "mapa.json")          # persiste na pasta do caso
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

FORJA = Path(__file__).resolve().parent
RAIZ = FORJA.parent
sys.path.insert(0, str(RAIZ / "_FERRAMENTAS"))

# ---------------------------------------------------------------- normalização
# Espelha _norm de forja_visual.py. Precisa ser idêntica: é ela que decide se a
# âncora emitida aqui sobrevive à validação de _Mapa._valida lá.


def _norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[*_#|>`“”‘’\"']", "", s.lower())
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def _e_enderecamento(linha):
    t = linha.strip().lstrip("#").strip().strip("*")
    return bool(t) and (t == t.upper() and len(t) > 25 or t.startswith("Excelent"))


# ---------------------------------------------------------------- elegibilidade
# ESTE É O CORAÇÃO DO MÓDULO. compor() só executa pos_paragrafo/como_caixa/
# figs_depois para linhas que atravessam todo o laço até a etapa de corpo.
# Âncora em linha consumida antes (tabela, título, citação >, lista, capa,
# síntese, fecho/assinatura) nunca é consumida e derruba a composição inteira
# com "MAPA NÃO CONSUMIDO". Por isso simulamos o mesmo caminho, na mesma ordem.


def _varre(texto_md):
    """Devolve (elegiveis, secoes, sintese_linhas).

    elegiveis: [{"raw", "par", "norm", "secao", "i"}] — parágrafos de corpo que
        aceitam pull/caixa/figura. "par" já vem sem a numeração de origem.
    secoes: [{"titulo", "t_sem_num", "nivel", "i"}] — títulos de nível <= 2.
    sintese_linhas: linhas cruas da seção de síntese (para rotulos_sintese).
    """
    linhas = texto_md.splitlines()
    elegiveis, secoes, sintese_linhas = [], [], []
    i, primeiro_h1, capa = 0, True, True
    em_sintese = False
    pos_deferimento = False
    secao_atual = ""

    while i < len(linhas):
        strip = linhas[i].rstrip().strip()

        if not strip or re.match(r"^\s*([-*_])\1{2,}\s*$", strip):
            i += 1
            continue

        # tabela markdown -> quadro zebrado (encerra a síntese, como em compor)
        if strip.startswith("|") and i + 1 < len(linhas) and \
                re.match(r"^\s*\|[\s:|-]+\|\s*$", linhas[i + 1]):
            em_sintese = False
            i += 2
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                i += 1
            continue

        mh = re.match(r"^(#{1,6})\s+(.*)$", strip)
        if mh:
            nivel, titulo = len(mh.group(1)), mh.group(2).strip()
            t_sem_num = re.sub(r"^[IVXL0-9]+\s*[—\-–.]\s*", "",
                               titulo.replace("**", "")).strip()
            if _norm(t_sem_num).startswith(("sintese executiva", "sintese dos pontos",
                                            "sintese")) and nivel >= 2 and not secoes:
                em_sintese = True
                capa = False
                i += 1
                continue
            em_sintese = False
            if nivel == 1 and primeiro_h1:
                # título da peça consome endereçamentos e dados do processo
                j = i + 1
                while j < len(linhas):
                    s2 = linhas[j].strip()
                    if not s2:
                        j += 1
                        continue
                    if _e_enderecamento(s2):
                        j += 1
                        continue
                    break
                while j < len(linhas) and not linhas[j].strip():
                    j += 1
                if j < len(linhas):
                    s2 = linhas[j].strip()
                    if s2.startswith("**") and re.search(r"\d[\d./\-]{3,}", s2):
                        j += 1
                while j < len(linhas):
                    s3 = linhas[j].strip()
                    if not s3:
                        j += 1
                        continue
                    if s3.startswith("**") and len(s3) < 260 and not s3.startswith("#"):
                        j += 1
                        continue
                    break
                primeiro_h1 = False
                i = j
                continue
            if capa and not secoes and _e_enderecamento(titulo) and \
                    not re.match(r"^[IVXL0-9]+\s*[—\-–.]", titulo):
                i += 1
                continue
            capa = False
            if nivel <= 2:
                secoes.append({"titulo": titulo.replace("**", ""),
                               "t_sem_num": t_sem_num, "nivel": nivel, "i": i})
                secao_atual = t_sem_num
            i += 1
            continue

        if em_sintese:
            sintese_linhas.append(strip)
            i += 1
            continue

        # citação em bloco: compor chama pv.pgf direto, sem passar por âncoras
        if re.match(r"^>\s?", strip):
            while i < len(linhas) and re.match(r"^\s*>\s?", linhas[i]):
                i += 1
            continue

        # lista: idem, consumida antes das âncoras
        if re.match(r"^[-•]\s+", strip):
            while i < len(linhas) and re.match(r"^[-•]\s+", linhas[i].strip()):
                i += 1
            continue

        par = re.sub(r"^\*{0,2}(\d{1,3})\.\*{0,2}\s+", "", strip)

        # capa: dados em negrito antes da 1ª seção
        if capa and strip.startswith("**") and len(strip) < 260:
            i += 1
            continue

        if re.search(r"pede[m]?\s+deferimento", strip, re.I):
            pos_deferimento = True
            i += 1
            continue

        t_ass = strip.strip("*").strip()
        eh_fecho_data = re.match(
            r"^(Bras[íi]lia|Porto Alegre|Rio de Janeiro|S[ãa]o Paulo).{0,40}de\s+20\d\d", t_ass)
        if eh_fecho_data:
            pos_deferimento = True
        eh_assin = pos_deferimento and (
            (t_ass == t_ass.upper() and 2 <= len(t_ass.split()) <= 6)
            or re.match(r"^OAB[/ ]", t_ass, re.I)
            or re.match(r"^(Curador|Curadora|Advogado|Advogada|Representante|Assistente)\b",
                        t_ass, re.I)
            or (strip.startswith("**") and 2 <= len(t_ass.split()) <= 6)
            or eh_fecho_data)
        if eh_assin:
            i += 1
            continue

        elegiveis.append({"raw": strip, "par": par, "norm": _norm(strip),
                          "secao": secao_atual, "i": i})
        i += 1

    return elegiveis, secoes, sintese_linhas


# ---------------------------------------------------------------- extração
_FIM_FRASE = re.compile(r"(?<=[.;:])\s+")
_MD = re.compile(r"[*`_]")


def _limpa(t):
    return _MD.sub("", t).strip()


def _ancora(par, alvo_norm=None, minimo=45, maximo=90):
    """Prefixo do parágrafo usado como âncora.

    Cresce até ficar ÚNICO no documento: âncora repetida faz compor() casar no
    parágrafo errado — a moldura visual apareceria no lugar errado sem erro
    visível. Boilerplate ("Ante o exposto, ...") repete com frequência, então o
    crescimento vai até o fim do parágrafo se necessário."""
    limpo = _limpa(par)
    if len(limpo) <= minimo:
        return limpo
    fim = minimo
    while fim < len(limpo):
        corte = limpo.rfind(" ", minimo, min(fim + maximo, len(limpo)))
        cand = limpo[:corte if corte > minimo else min(fim + maximo, len(limpo))].strip()
        if alvo_norm is None or alvo_norm.count(_norm(cand)) <= 1:
            return cand
        fim = len(cand) + 1
    return limpo


def _frase(par, minimo=55, maximo=190):
    """Primeira frase completa do parágrafo, verbatim. None se não couber —
    truncar no meio distorce sentido e é pior que não destacar."""
    limpo = _limpa(par)
    for frase in _FIM_FRASE.split(limpo):
        frase = frase.strip()
        if minimo <= len(frase) <= maximo:
            return frase
    return None


def _frase_destacavel(par, minimo=55, maximo=190, evitar=()):
    """Frase para pull quote ou linha-síntese, nunca a que abre o parágrafo.

    Pull quote e linha-síntese são impressas imediatamente ACIMA do parágrafo
    de onde saíram. Se a frase escolhida for a primeira dele, o leitor vê a
    mesma frase duas vezes seguidas, e o gate de escrita humana reprova por
    redundância consecutiva — foi o que barrou o Adendo VII do mapeamento em
    06/08/2026, com similaridade 1,00. O defeito passava despercebido porque
    parágrafo de abertura longo faz `_frase` cair na segunda frase sozinha.

    `evitar` recebe as frases já comprometidas com outro destaque. Sem isso, a
    linha-síntese da seção e a pull quote do mesmo parágrafo escolhem a mesma
    frase — que é a segunda metade do mesmo defeito.

    Devolve None quando só a frase de abertura cabe: destaque redundante é pior
    que destaque ausente, e o documento tem outros parágrafos candidatos.
    """
    limpo = _limpa(par)
    frases = [f.strip() for f in _FIM_FRASE.split(limpo)]
    # O critério é de POSIÇÃO, não de igualdade de frase. Comparar frases não
    # resolve porque o divisor quebra também em dois-pontos: em "A consequência
    # é direta: não existe fonte pública nacional que responda...", a segunda
    # metade é frase distinta da primeira e ainda assim abre o parágrafo. O que
    # produz a leitura duplicada é o destaque nascer da abertura, qualquer que
    # seja o recorte.
    ABERTURA = 80
    for frase in frases:
        if not frase or frase in evitar:
            continue
        if limpo.find(frase) < ABERTURA:
            continue
        # O divisor quebra em abreviação: "fundado nos arts. 7º e 8º da Lei" vira
        # duas "frases", e a segunda entrou como linha-síntese de uma seção
        # começando em "7º e 8º da Lei nº 9.966/2000 e vale por réu". Destaque
        # que começa no meio de uma oração parece erro de recorte, e é.
        letras = [c for c in frase if c.isalpha()]
        if letras and not letras[0].isupper():
            continue
        if minimo <= len(frase) <= maximo:
            return frase
    return None


# Marcadores de parágrafo que carrega decisão — base das pull quotes.
# Calibrado contra os 5 mapas manuais: o humano destaca (a) conclusões, (b)
# negações categóricas, (c) imputações de vício, (d) movimentos argumentativos
# ordinais ("Primeira —", "Segunda —") e (e) enunciados normativos.
_PESO = (
    (re.compile(r"\b(portanto|logo|por isso|donde|conclui-se|resulta|"
                r"em s[íi]ntese|do exposto)\b", re.I), 3),
    (re.compile(r"\b(n[ãa]o h[áa]|n[ãa]o existe|n[ãa]o subsiste|n[ãa]o prospera|"
                r"n[ãa]o resiste|n[ãa]o cabe|n[ãa]o autoriza|nenhum[ao]?\b)", re.I), 3),
    (re.compile(r"\b([ée] inequ[íi]voco|[ée] incontroverso|[ée] certo que|"
                r"basta (?:ver|notar)|precisamente)\b", re.I), 3),
    (re.compile(r"\b(viola|contraria|afronta|desconsidera|omitiu|silenciou|"
                r"incorre|desafia)\b", re.I), 2),
    (re.compile(r"\b(exige|imp[õo]e|determina|obriga|veda|assegura|garante)\b", re.I), 2),
    (re.compile(r"^\s*\*{0,2}(Primeir[ao]|Segund[ao]|Terceir[ao]|Quart[ao]|Quint[ao])\b",
                re.I), 3),
    (re.compile(r"\b(a quest[ãa]o|o ponto|a controv[ée]rsia|o cerne|a tese)\b", re.I), 2),
    (re.compile(r"\b(registre-se|note-se|observe-se|frise-se|destaque-se)\b", re.I), 2),
)
_CITACAO = re.compile(r"[“\"]")
# identificadores de precedente — base das caixas
_PRECEDENTE = re.compile(
    r"\b(S[úu]mula\s+\d+|Tema\s+(?:Repetitivo\s+)?\d+|REsp\s*n?[ºo.]?\s*[\d.]+|"
    r"AREsp\s*n?[ºo.]?\s*[\d.]+|AgInt|RE\s*n?[ºo.]?\s*[\d.]+|ADI\s*n?[ºo.]?\s*[\d.]+)\b")
_DATA = re.compile(r"\b\d{1,2}[/.]\d{1,2}[/.]\d{2,4}\b|\b\d{1,2}\s+de\s+\w+\s+de\s+\d{4}\b")


def _titulo_precedente(texto):
    """Rótulo da caixa: o identificador do precedente, quando houver um.

    O padrão anterior era rotular "PRECEDENTE INVOCADO" tudo o que virasse
    caixa. Mas a caixa também é escolhida por peso de citação — aspas bastam —,
    e no Adendo VII do mapeamento (06/08/2026) três caixas sem precedente
    nenhum saíram assim rotuladas, sendo que uma delas era uma ressalva nossa
    sobre valor. O rótulo afirmava, na cara do leitor, uma coisa que o
    parágrafo não continha. Rótulo é texto autoral e cai na mesma regra das
    figuras: melhor neutro e verdadeiro do que específico e falso.
    """
    m = _PRECEDENTE.search(texto)
    return (m.group(0).upper() if m else "DESTAQUE")


# ---------------------------------------------------------------- geração
def _rotulo_curto(texto, limite=34):
    """Rótulo da linha de síntese: caixa alta, curto, sem pontuação final.
    A coluna do rótulo tem 3,1cm — texto longo quebra em quatro linhas e
    desmonta o alinhamento da tabela."""
    limpo = re.sub(r"\s+", " ", _MD.sub("", str(texto))).strip(" .:;—-")
    if len(limpo) <= limite:
        return limpo.upper().strip(" .:;—-")
    # Lead-in longo costuma terminar no núcleo ("Se, excepcionalmente, admitido
    # o agravo, no mérito subsidiário" -> "MÉRITO SUBSIDIÁRIO"). Truncar pela
    # frente produz rótulo sem sentido, que foi o que saiu no CASO-16.
    cauda = re.split(r",\s*", limpo)[-1].strip()
    cauda = re.sub(r"^(no|na|em|de|do|da|ao|à|para|com)\s+", "", cauda, flags=re.I)
    if 8 <= len(cauda) <= limite:
        return cauda.upper().strip(" .:;—-")
    corte = limpo.rfind(" ", 0, limite)
    return limpo[:corte if corte > 12 else limite].upper().strip(" .:;—-")


def _rotulos_sintese(sintese_linhas, maximo=6):
    """Divide a síntese em linhas rotuladas a partir dos lead-ins em negrito.

    Sem isto, compor() cai no fallback de uma única linha "SÍNTESE" com o texto
    inteiro num bloco — foi o que saiu no CASO-16 em 30/07/2026, e é
    exatamente a leitura rápida transversal que se perde.

    CUIDADO: compor() localiza as âncoras por busca LITERAL no texto da síntese
    e fatia entre elas. O trecho anterior à primeira âncora é DESCARTADO — se a
    primeira âncora não estiver na posição zero, a abertura some do DOCX e o
    gate de fidelidade reprova a peça inteira.
    """
    texto = "\n".join(sintese_linhas)
    if len(texto) < 200:
        return []
    # A PRIMEIRA fatia precisa conter sozinha os 150 primeiros caracteres da
    # linha da síntese. O gate de fidelidade de compor() procura esse trecho
    # como bloco contíguo no DOCX, e o rótulo da linha seguinte se intercala
    # entre a abertura e o próximo lead-in, partindo o bloco ao meio
    # (reprovação real no CASO-16, 30/07/2026). 170 dá margem para a
    # diferença de comprimento introduzida pela normalização.
    marcas = [(m.start(), m.group(0), m.group(1))
              for m in re.finditer(r"\*\*([^*\n]{3,80})\*\*", texto)
              if m.start() >= 170]
    if len(marcas) < 2:
        return []
    marcas = marcas[:maximo - 1]

    # abertura: âncora obrigatória na posição zero
    corte = texto.find(" ", 40)
    abertura = texto[:corte if 40 < corte < 90 else 60]
    rotulos = [("SÍNTESE", abertura)]
    for _, literal, interno in marcas:
        rotulo = _rotulo_curto(interno)
        if not rotulo:
            continue
        if texto.count(literal) != 1:
            continue                       # âncora ambígua: fatiaria errado
        rotulos.append((rotulo, literal))
    return rotulos if len(rotulos) >= 3 else []


def gerar_mapa(md_path, tipo=None, com_figuras=True, max_pulls=6, max_caixas=3):
    """Deriva o mapa visual declarativo do markdown auditado."""
    texto_md = Path(md_path).read_text(encoding="utf-8")
    elegiveis, secoes, sintese_linhas = _varre(texto_md)

    if tipo is None:
        abertura = texto_md[:1800].upper()
        tipo = "estudo" if re.search(
            r"\b(ESTUDO|DIAGN[ÓO]STICO|RELAT[ÓO]RIO|PARECER|MATRIZ|CHECKLIST)\b",
            abertura) else "peca"

    usados = set()          # índices já comprometidos com caixa (substituem o pgf)
    alvo = _norm(texto_md)   # base de unicidade das âncoras
    mapa = {"tipo": tipo}

    # --- linhas-síntese: uma frase do 1º parágrafo de cada seção ---
    linhas_sintese = {}
    comprometidas = set()   # frases já usadas: nenhum outro destaque as repete
    for sec in secoes:
        corpo = [e for e in elegiveis if e["secao"] == sec["t_sem_num"]]
        if not corpo:
            continue
        frase = _frase_destacavel(corpo[0]["par"], minimo=40, maximo=150)
        if frase:
            linhas_sintese[sec["t_sem_num"]] = frase
            comprometidas.add(frase)
    if linhas_sintese:
        mapa["linhas_sintese"] = linhas_sintese

    # --- síntese de abertura dividida em linhas rotuladas ---
    rotulos = _rotulos_sintese(sintese_linhas)
    if rotulos:
        mapa["rotulos_sintese"] = rotulos

    # --- caixas: o parágrafo VIRA a caixa, então tem de ser autossuficiente ---
    # Prioriza citação de precedente com corpo longo; empata pelo tamanho.
    cand_caixa = []
    for e in elegiveis:
        corpo = _limpa(e["par"])
        if len(corpo) < 140:
            continue
        peso = 0
        if _PRECEDENTE.search(corpo):
            peso += 4
        if _CITACAO.search(e["par"]):
            peso += 2
        if peso:
            cand_caixa.append((peso, len(corpo), e))
    caixas, secoes_com_caixa = [], set()
    for _, _, e in sorted(cand_caixa, key=lambda x: (-x[0], -x[1])):
        if len(caixas) >= max_caixas or e["secao"] in secoes_com_caixa:
            continue
        caixas.append((_ancora(e["par"], alvo), "precedente", _titulo_precedente(e["par"])))
        secoes_com_caixa.add(e["secao"])
        usados.add(e["i"])
    if caixas:
        mapa["caixas"] = sorted(caixas, key=lambda c: _norm(texto_md).find(_norm(c[0])))

    # --- pull quotes: frase verbatim de peso ---
    # Densidade calibrada pelos mapas manuais (4 a 7 por peça). Uma pull por
    # seção deixava recall preso em ~15%: o humano destaca várias vezes dentro
    # da mesma seção. O limite real é a densidade do documento, não a seção.
    alvo_pulls = max(4, min(max_pulls, len(elegiveis) // 8))
    candidatos = []
    for e in elegiveis:
        if e["i"] in usados:
            continue
        peso = sum(p for rx, p in _PESO if rx.search(e["par"]))
        if not peso:
            continue
        if _frase_destacavel(e["par"], evitar=comprometidas) is None:
            continue
        candidatos.append((peso, e))
    # Fallback de densidade: documento de registro técnico (diagnóstico,
    # matriz, checklist) não usa o vocabulário argumentativo dos marcadores —
    # no CASO-07 nenhum dos 208 parágrafos elegíveis dispara peso. Sem isto, o
    # produto interno sairia sem nenhum destaque, violando o piso do padrão.
    # Critério do fallback: parágrafo substancial, bem distribuído no texto.
    if len(candidatos) < alvo_pulls:
        ja = {id(e) for _, e in candidatos}
        reserva = [e for e in elegiveis
                   if e["i"] not in usados and id(e) not in ja
                   and len(_limpa(e["par"])) >= 140 and _frase_destacavel(e["par"], evitar=comprometidas)]
        if reserva:
            passo = max(1, len(reserva) // max(1, alvo_pulls - len(candidatos)))
            candidatos += [(1, e) for e in reserva[::passo]]

    pulls, por_secao = [], {}
    for _, e in sorted(candidatos, key=lambda x: (-x[0], x[1]["i"])):
        if len(pulls) >= alvo_pulls:
            break
        # no máximo 2 por seção: mais que isso vira ruído na margem
        if por_secao.get(e["secao"], 0) >= 2:
            continue
        frase_pull = _frase_destacavel(e["par"], evitar=comprometidas)
        pulls.append((_ancora(e["par"], alvo), frase_pull))
        comprometidas.add(frase_pull)
        por_secao[e["secao"]] = por_secao.get(e["secao"], 0) + 1
        usados.add(e["i"])
    if pulls:
        mapa["pulls"] = sorted(pulls, key=lambda p: _norm(texto_md).find(_norm(p[0])))

    # --- figuras: cronologia onde há mais datas; tese na seção de maior corpo ---
    if com_figuras:
        figs = []
        por_datas = sorted(
            (e for e in elegiveis if e["i"] not in usados),
            key=lambda e: (-len(_DATA.findall(e["par"])), e["i"]))
        if por_datas and _DATA.findall(por_datas[0]["par"]):
            figs.append((_ancora(por_datas[0]["par"], alvo), "{{FIG1}}",
                         "Cronologia dos atos relevantes."))
            usados.add(por_datas[0]["i"])
        restantes = [e for e in elegiveis if e["i"] not in usados
                     and len(_limpa(e["par"])) > 200]
        if restantes:
            alvo_fig = restantes[len(restantes) // 2]
            figs.append((_ancora(alvo_fig["par"], alvo), "{{FIG2}}",
                         "Encadeamento da tese: premissas e conclusão."))
            usados.add(alvo_fig["i"])
        # Peça longa comporta — e a faixa de densidade exige — um terceiro
        # elemento gráfico. Sem este espaço o teto do gerador era de três
        # imagens (cards + duas figuras) e documento acima de 25 páginas nunca
        # fechava o piso, acusando VIS-03 por limitação nossa, não da peça.
        # O slot só vira figura se houver conteúdo que o sustente: quem decide
        # é forja_visual_figuras, que descarta o que não tem lastro.
        if len(elegiveis) > 90:
            sobra = [e for e in elegiveis if e["i"] not in usados
                     and len(_limpa(e["par"])) > 200]
            if sobra:
                alvo3 = sobra[int(len(sobra) * 0.75)]
                figs.append((_ancora(alvo3["par"], alvo), "{{FIG3}}",
                             "Quadro comparativo dos critérios em confronto."))
                usados.add(alvo3["i"])
        if figs:
            mapa["figs"] = figs
        if tipo == "peca" and len(secoes) >= 3:
            mapa["cards_apos_titulo"] = True
            # Capa cheia (parecer Helena, 31/07/2026, delegado pelo Igor): sem a
            # quebra de página o texto sobe para a capa e ocupa o branco da
            # metade inferior. O julgador do STJ recebe centenas de peças e
            # página em branco custa tempo dele. Verificado no render: a capa
            # passa a trazer qualificação e início da síntese 343-A, e a peça
            # encurta uma página. Os mapas manuais históricos não recebem esta
            # chave e seguem com capa autônoma, como aprovado em 09/07/2026.
            mapa["capa_com_sintese"] = True

    _autovalidar(mapa, texto_md)
    return mapa


def _autovalidar(mapa, texto_md):
    """Falha aqui é melhor que falha dentro de compor(): mesma regra, mensagem
    que aponta o gerador em vez do caso."""
    alvo = _norm(texto_md)
    vistos = set()
    for chave in ("pulls", "laterais"):
        for anc, _ in mapa.get(chave) or []:
            _checa(anc, alvo, vistos, chave)
    for anc, _, _ in mapa.get("caixas") or []:
        _checa(anc, alvo, vistos, "caixas")
    for anc, _, _ in mapa.get("figs") or []:
        _checa(anc, alvo, vistos, "figs")


def _checa(anc, alvo, vistos, origem):
    n = _norm(anc)
    if not n or n not in alvo:
        raise ValueError(f"GERADOR PRODUZIU ÂNCORA INVÁLIDA ({origem}): {anc[:70]!r}")
    if alvo.count(n) > 1:
        raise ValueError(f"ÂNCORA AMBÍGUA ({origem}, {alvo.count(n)} ocorrências): {anc[:70]!r}")
    if n in vistos:
        raise ValueError(f"ÂNCORA REPETIDA ({origem}): {anc[:70]!r}")
    vistos.add(n)


def gravar_mapa(md_path, destino=None, **kw):
    md_path = Path(md_path)
    destino = Path(destino) if destino else md_path.with_name("mapa.json")
    mapa = gerar_mapa(md_path, **kw)
    destino.write_text(json.dumps(mapa, ensure_ascii=False, indent=2), encoding="utf-8")
    return destino, mapa


if __name__ == "__main__":
    caminho, m = gravar_mapa(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print(json.dumps({"mapa": str(caminho), "pulls": len(m.get("pulls") or []),
                      "caixas": len(m.get("caixas") or []),
                      "figs": len(m.get("figs") or []),
                      "linhasSintese": len(m.get("linhas_sintese") or {}),
                      "tipo": m["tipo"]}, ensure_ascii=False, indent=2))
