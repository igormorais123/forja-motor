# -*- coding: utf-8 -*-
"""FORJA — extração do conteúdo das figuras a partir do markdown (Onda 1B).

O gerador de mapa (forja_visual_mapa_gen) decide ONDE a figura entra. Este
módulo decide O QUE ela desenha, extraindo do próprio texto auditado. Os dois
são separados porque falham por motivos diferentes: âncora inválida derruba a
composição; figura pobre passa despercebida.

REGRA: nada de fato novo. A cronologia usa as datas que o texto já afirma; o
encadeamento usa as frases de abertura das seções, verbatim. Quando o texto não
sustenta a figura, ela NÃO é gerada — figura fabricada é pior que figura
ausente, porque parece prova.
"""
import re
import sys
from pathlib import Path

FORJA = Path(__file__).resolve().parent
RAIZ = FORJA.parent
sys.path.insert(0, str(RAIZ / "_FERRAMENTAS"))
sys.path.insert(0, str(FORJA))

_MESES = ("janeiro fevereiro março abril maio junho julho agosto setembro "
          "outubro novembro dezembro").split()
_DATA_NUM = re.compile(r"\b(\d{1,2})[/.](\d{1,2})[/.](\d{2,4})\b")
_DATA_EXT = re.compile(r"\b(\d{1,2})\s+de\s+(" + "|".join(_MESES) + r")\s+de\s+(\d{4})\b",
                       re.I)
_MD = re.compile(r"[*`_#>]")


def _limpa(t):
    return re.sub(r"\s+", " ", _MD.sub("", t)).strip()


def _chave(d, m, a):
    a = int(a)
    if a < 100:
        a += 2000 if a < 70 else 1900
    return (a, int(m), int(d))


# Números de processo no padrão CNJ contêm sequências que se parecem com data:
# em 9000006-00.2014.8.26.0000 o trecho "8.26.0100" casa com dd.mm.aaaa e vira
# um marco fantasma na linha do tempo (flagrado no CASO-02, 30/07/2026). Também
# mascaramos valores monetários e artigos com pontuação numérica.
_CNJ = re.compile(r"\b\d{6,7}-?\d{0,2}\.?\d{0,4}\.?\d?\.?\d{2}\.?\d{4}\b")
# 12+ caracteres: uma data dd/mm/aaaa tem 10 e não pode ser mascarada aqui.
_NUM_LONGO = re.compile(r"\b\d[\d.,/-]{11,}\b")


def _mascara(texto):
    texto = _CNJ.sub(lambda m: "#" * len(m.group(0)), texto)
    return _NUM_LONGO.sub(lambda m: "#" * len(m.group(0)), texto)


def _datas(texto):
    """[(chave_ordenacao, rotulo_como_escrito, posicao)] — sem reformatar.

    Só devolve datas plausíveis: dia 1-31, mês 1-12, ano 1900-2100. Sem esse
    filtro, fragmento de número de processo entra como marco.
    """
    limpo = _mascara(texto)
    achados = []
    for m in _DATA_NUM.finditer(limpo):
        d, mes, a = m.groups()
        if not (1 <= int(d) <= 31 and 1 <= int(mes) <= 12):
            continue
        chave = _chave(d, mes, a)
        if not 1900 <= chave[0] <= 2100:
            continue
        achados.append((chave, m.group(0), m.start()))
    for m in _DATA_EXT.finditer(limpo):
        dia, mes, ano = m.groups()
        if not 1 <= int(dia) <= 31:
            continue
        chave = _chave(dia, _MESES.index(mes.lower()) + 1, ano)
        if not 1900 <= chave[0] <= 2100:
            continue
        achados.append((chave, m.group(0), m.start()))
    return achados


def _oracao(frase, pos_data, limite=118):
    """Trecho da frase que contém a data, verbatim, cortado em fronteira de
    oração. Se nem a menor fronteira couber, devolve None — melhor não desenhar
    o marco do que desenhá-lo truncado no meio de uma afirmação."""
    limpo = _limpa(frase)
    if len(limpo) <= limite:
        return limpo
    for sep in ("; ", ", ", " — ", " ("):
        partes = limpo.split(sep)
        acc = ""
        for p in partes:
            cand = (acc + sep + p).strip(sep) if acc else p
            if len(cand) > limite:
                break
            acc = cand
        if 30 <= len(acc) <= limite:
            return acc.strip()
    return None


# Seções e tabelas que declaram cronologia de forma explícita. Fora delas, o
# texto não sustenta uma linha do tempo.
_SEC_CRONO = re.compile(
    r"cronologi|hist[óo]rico process|linha do tempo|sequ[êe]ncia dos atos|"
    r"dos fatos e do process|marcos process", re.I)
# Origem operacional é bloqueador P0 no corpo da peça (protocolo 11/07/2026) e
# não pode entrar pela porta da figura.
_ORIGEM_OPERACIONAL = re.compile(
    r"\b(e-?mail|whats?app|drive|pasta|arquivo local|compartilhad|"
    r"planilha interna|minuta interna|prazo interno)\b", re.I)


def _fonte_cronologica(texto_md):
    """Devolve o trecho do md que DECLARA cronologia, ou None.

    Decisão de projeto (30/07/2026, após inspeção visual do CASO-02 e do CASO-07):
    varrer datas da prosa inteira mistura data do documento, prazo interno,
    data de julgado citado e ato processual numa única linha do tempo. Cada item
    sai verbatim e o conjunto ainda assim afirma uma sequência que o texto não
    estabelece. Só geramos cronologia quando o autor escreveu uma.
    """
    linhas = texto_md.splitlines()
    for k, linha in enumerate(linhas):
        titulo = re.match(r"^#{1,6}\s+(.*)$", linha.strip())
        if not titulo or not _SEC_CRONO.search(titulo.group(1)):
            continue
        bloco = []
        for seguinte in linhas[k + 1:]:
            if re.match(r"^#{1,6}\s+", seguinte.strip()):
                break
            bloco.append(seguinte)
        if bloco:
            return "\n".join(bloco)
    # tabela cujo cabeçalho tem coluna de data
    for k, linha in enumerate(linhas):
        s = linha.strip()
        if s.startswith("|") and re.search(r"\|\s*\**\s*(data|per[íi]odo|quando)",
                                           s, re.I):
            bloco = [s]
            for seguinte in linhas[k + 1:]:
                if not seguinte.strip().startswith("|"):
                    break
                bloco.append(seguinte.strip())
            if len(bloco) > 2:
                return "\n".join(bloco)
    return None


def extrair_cronologia(texto_md, minimo=3, maximo=7):
    """Marcos processuais em ordem cronológica. None se o texto não sustenta."""
    from forja_visual_mapa_gen import _varre
    fonte = _fonte_cronologica(texto_md)
    if fonte is None:
        return None
    elegiveis, _, _ = _varre(fonte)
    if not elegiveis:
        elegiveis = [{"par": ln.strip("| ")} for ln in fonte.splitlines()
                     if ln.strip()]
    marcos, vistos, descricoes = [], set(), set()
    for e in elegiveis:
        for chave, rotulo, pos in _datas(e["par"]):
            if chave in vistos:
                continue
            # a oração da frase onde a data aparece
            frase = None
            for pedaco in re.split(r"(?<=[.;])\s+", e["par"]):
                if rotulo in pedaco:
                    frase = pedaco
                    break
            if frase is None:
                continue
            desc = _oracao(frase, pos)
            # VÍNCULO OBRIGATÓRIO: a descrição do marco tem de conter a própria
            # data. Sem isso, o corte por fronteira de oração pode devolver um
            # trecho que fala de OUTRO ato — a figura afirmaria um vínculo
            # temporal que o texto não estabelece (defeito CASO-02, 30/07/2026).
            if not desc or rotulo not in desc:
                continue
            if _ORIGEM_OPERACIONAL.search(desc):
                continue   # P0: origem operacional nunca entra na peça, nem via figura
            # descrição repetida significa que várias datas caíram na mesma
            # frase: manter só a primeira, senão a linha do tempo mente por
            # repetição.
            # Dedup por descrição SEM os dígitos e sem truncar: cortar em 80
            # caracteres fazia "…de 15/07/2026" e "…de 15/07/26" gerarem chaves
            # diferentes, e o mesmo ato entrava duas vezes na linha do tempo
            # (achado A-10 da revisão cruzada Codex, 03/08/2026). Sem os
            # dígitos, as duas formas da mesma data colapsam na mesma chave.
            chave_desc = re.sub(r"[\W\d]+", "", desc.lower())
            if chave_desc in descricoes:
                continue
            vistos.add(chave)
            descricoes.add(chave_desc)
            marcos.append((chave, rotulo, desc))
    if len(marcos) < minimo:
        return None
    marcos.sort(key=lambda m: m[0])
    if len(marcos) > maximo:
        # preserva o primeiro e o último; amostra uniforme no meio
        passo = (len(marcos) - 2) / (maximo - 2)
        idx = [0] + [1 + int(k * passo) for k in range(maximo - 2)] + [len(marcos) - 1]
        marcos = [marcos[k] for k in sorted(set(idx))]
    return [(rotulo, desc) for _, rotulo, desc in marcos]


BRIEF_NOME = "F7_5_BRIEF_VISUAL.json"

# A legenda afirma de onde vem o dado, então ela muda com o produto. "Conforme
# declarado nos autos" é verdade numa peça e é falso num estudo interno, que
# não tem autos: em 07/08/2026 uma nota técnica saiu com essa legenda sob uma
# cronologia montada a partir do brief do autor. Legenda é afirmação, não
# enfeite — e afirmação errada sob figura correta é pior que figura sem
# legenda, porque atribui lastro que não existe.
_LEGENDAS = {
    "peca": {
        "cronologia": "Cronologia dos atos, conforme declarado nos autos.",
        "comparacao": "Quadro comparativo dos critérios em confronto.",
        "cadeia": "Encadeamento da tese: premissas e conclusão.",
    },
    "estudo": {
        "cronologia": "Cronologia dos fatos relevantes.",
        "comparacao": "Quadro comparativo dos critérios em confronto.",
        "cadeia": "Encadeamento do raciocínio: premissas e conclusão.",
    },
}

_TOKEN_FATO = re.compile(r"\b\d[\d.,/º§-]*\b")


def carregar_brief(md_path):
    """Brief visual declarado em F7.5, ao lado do markdown. None se não existe."""
    import json
    p = Path(md_path).with_name(BRIEF_NOME)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8-sig"))


def validar_brief(brief, texto_md):
    """Devolve lista de problemas. Vazia = aprovado.

    O brief é redigido por quem escreveu a peça, então não é verbatim. O que se
    verifica é o que dá para verificar de forma barata e que pega o modo de
    falha real: número, data ou dispositivo que aparece na figura e NÃO aparece
    no texto é fato introduzido pela camada visual — proibido.
    """
    problemas = []
    alvo = _limpa(texto_md)
    alvo_num = set(_TOKEN_FATO.findall(alvo))

    def confere(texto, onde):
        if not texto or not str(texto).strip():
            problemas.append(f"{onde}: vazio")
            return
        if len(str(texto)) > 190:
            problemas.append(f"{onde}: passa de 190 caracteres ({len(str(texto))})")
        if _ORIGEM_OPERACIONAL.search(str(texto)):
            problemas.append(f"{onde}: origem operacional (P0) — {str(texto)[:50]}")
        for token in _TOKEN_FATO.findall(str(texto)):
            if len(token) > 2 and token not in alvo_num:
                problemas.append(f"{onde}: número/data ausente do texto — {token}")

    cadeia = brief.get("cadeiaArgumentativa") or []
    if cadeia and not 3 <= len(cadeia) <= 6:
        problemas.append(f"cadeiaArgumentativa: {len(cadeia)} etapas (esperado 3 a 6)")
    for k, etapa in enumerate(cadeia, 1):
        confere(etapa, f"cadeiaArgumentativa[{k}]")
    for k, item in enumerate(brief.get("cronologia") or [], 1):
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            problemas.append(f"cronologia[{k}]: esperado par [data, descrição]")
            continue
        confere(item[0], f"cronologia[{k}].data")
        confere(item[1], f"cronologia[{k}].descrição")
    return problemas


def extrair_encadeamento(texto_md, brief=None, minimo=3, maximo=6):
    """Cadeia argumentativa. EXIGE brief declarado em F7.5.

    Decisão de projeto (30/07/2026): a versão anterior inferia a cadeia das
    frases de abertura de cada seção. A inspeção visual do CASO-02 mostrou o
    resultado — o diagrama colocou a TESE DA PARTE ADVERSÁRIA como elo do
    raciocínio da cliente, além de dois conectivos terminados em dois-pontos e
    um fragmento de item de lista. Toda frase era verbatim e a cadeia era falsa.
    Nenhum filtro separa "nossa tese" de "tese deles" numa abertura de seção;
    o problema é de premissa, não de heurística. Sem brief, não há figura.
    """
    if not brief:
        return None
    etapas = [str(e).strip() for e in (brief.get("cadeiaArgumentativa") or [])
              if str(e).strip()]
    if len(etapas) < minimo:
        return None
    return etapas[:maximo]


def extrair_comparacao(texto_md, min_linhas=2, max_linhas=6):
    """Matriz comparativa a partir de tabela JÁ existente no markdown.

    **Desligada em 09/08/2026, e a razão importa.** A ideia era que a figura só
    trocasse o meio de apresentação de dados que o autor já tabulou. Mas
    `compor()` preserva 100% do texto — é o gate de fidelidade —, então a tabela
    original continua impressa. O resultado é o mesmo conteúdo duas vezes, uma
    como "Figura 1" e outra como tabela, o que saiu num memorial entregue em
    08/08/2026 e passou pelo QA página a página sem ser visto.
    Densidade gráfica obtida por repetição é densidade falsa: não reduz esforço
    do julgador, e a régua da casa manda tirar da peça o que não reduz.

    A função fica aqui, e não foi apagada, porque o caminho certo existe e é
    outro: substituir a tabela pela figura na composição. Isso exige mexer no
    contrato de fidelidade e não se faz de passagem.
    """
    linhas = texto_md.splitlines()
    for k, linha in enumerate(linhas):
        s = linha.strip()
        if not (s.startswith("|") and k + 1 < len(linhas)
                and re.match(r"^\s*\|[\s:|-]+\|\s*$", linhas[k + 1])):
            continue
        cab = [_limpa(c) for c in s.strip("|").split("|")]
        if not 2 <= len(cab) <= 4:
            continue
        corpo = []
        for seguinte in linhas[k + 2:]:
            if not seguinte.strip().startswith("|"):
                break
            corpo.append([_limpa(c) for c in seguinte.strip().strip("|").split("|")])
        if min_linhas <= len(corpo) <= max_linhas:
            return cab, corpo[:max_linhas]
    return None


def gerar_figuras(texto_md, out_dir, mapa, largura_cm=13.1, brief=None, tipo=None):
    """Desenha os SVGs que o mapa declarou. Devolve {tag: (svg, largura_cm)}.

    `tipo` é o produto declarado ("peca" ou "estudo") e decide a legenda, que
    afirma a procedência do dado. Omitir mantém o texto de peça, que é o
    comportamento anterior.

    Se uma figura declarada não puder ser desenhada com lastro no texto, ela é
    REMOVIDA do mapa — o marcador ficaria literal no DOCX e o gate de marcadores
    de compor() abortaria a composição inteira.
    """
    from medina_svg_kit import cronologia, encadeamento, matriz
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    figs_saida, mantidas = {}, []

    # Cada slot tenta as fontes na ordem de confiabilidade e para na primeira
    # que o texto sustenta. Nada de inferência semântica sem brief.
    def desenha(svg, tag):
        if tag == "{{FIG1}}":
            eventos = (brief.get("cronologia") if brief else None) \
                or extrair_cronologia(texto_md)
            if eventos:
                cronologia(str(svg), [(str(d), str(t)) for d, t in eventos],
                           largura_cm=largura_cm)
                return "cronologia"
            return None
        if tag == "{{FIG2}}":
            etapas = extrair_encadeamento(texto_md, brief)
            if etapas:
                encadeamento(str(svg), etapas, largura_cm=largura_cm)
                return "cadeia"
            return None
        if tag == "{{FIG3}}":
            return None
        return None

    usados_tipo = set()
    for anc, tag, legenda in (mapa.get("figs") or []):
        svg = out_dir / f"fig_{tag.strip('{}').lower()}.svg"
        try:
            tipo_fig = desenha(svg, tag)
        except ValueError as exc:
            # gate de legibilidade/overflow reprovou: não insere figura ruim
            print(f"FIGURA DESCARTADA ({tag}): {exc}", file=sys.stderr)
            continue
        if not tipo_fig or tipo_fig in usados_tipo:
            continue
        usados_tipo.add(tipo_fig)
        legenda = _LEGENDAS.get(tipo or "peca", _LEGENDAS["peca"]).get(tipo_fig, legenda)
        figs_saida[tag] = (str(svg), largura_cm)
        mantidas.append((anc, tag, legenda))

    if mantidas:
        mapa["figs"] = mantidas
    else:
        mapa.pop("figs", None)

    # Cards da capa. O padrão aprovado em 09/07/2026 (CASO-16) usa ÂNCORAS
    # FACTUAIS — "4 / óbices processuais cumulativos", "09/04/2008 / ato
    # alegado", "13 anos / decurso sem materialização": quatro dados na cara do
    # julgador. Índice de seções ("01 RESUMO") é bem mais fraco e foi o que a
    # versão automática produzia. O dado é semântico, então vem do brief F7.5;
    # sem brief, cai no índice de seções, que ao menos orienta a varredura.
    if mapa.get("cards_apos_titulo"):
        from medina_svg_kit import cards_ancora
        from forja_visual_mapa_gen import _varre
        cores = [("395C60", "EFF4F3"), ("9C5B38", "FBF2EC"), ("2A4548", "EFF4F3"),
                 ("D9926A", "FBF2EC")]
        dados = []
        ancoras = (brief or {}).get("ancoras") or []
        if ancoras:
            for k, item in enumerate(ancoras[:4]):
                destaque, descricao = (list(item) + ["", ""])[:2]
                cor, fundo = cores[k % len(cores)]
                dados.append((str(destaque)[:12], f"#{cor}", f"#{fundo}",
                              str(descricao)[:70]))
        else:
            _, secoes, _ = _varre(texto_md)
            for k, sec in enumerate(secoes[:4]):
                cor, fundo = cores[k % len(cores)]
                dados.append((f"{k + 1:02d}", f"#{cor}", f"#{fundo}",
                              sec["t_sem_num"][:70]))
        svg = out_dir / "fig_cards.svg"
        try:
            cards_ancora(str(svg), dados, largura_cm=largura_cm)
            figs_saida["{{CARDS}}"] = (str(svg), largura_cm)
        except ValueError as exc:
            print(f"CARDS DESCARTADOS: {exc}", file=sys.stderr)
            mapa.pop("cards_apos_titulo", None)

    return figs_saida


if __name__ == "__main__":
    from forja_visual_mapa_gen import gerar_mapa
    md = Path(sys.argv[1])
    destino = Path(sys.argv[2]) if len(sys.argv) > 2 else md.parent / "_figuras"
    texto = md.read_text(encoding="utf-8")
    mapa = gerar_mapa(md)
    figs = gerar_figuras(texto, destino, mapa)
    print(f"figuras: {list(figs)}")
