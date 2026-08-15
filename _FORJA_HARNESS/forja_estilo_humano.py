# -*- coding: utf-8 -*-
"""Gate determinístico contra vícios de redação automatizada na FORJA.

O módulo não tenta adivinhar autoria nem produzir uma falsa "probabilidade de IA".
Ele mede sinais observáveis no texto e devolve trechos, contagens e ação corretiva.
P0 bloqueia F6, F7, F9, render, pacote, rascunho e entrega; P1 exige leitura editorial.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
import unicodedata
from collections import Counter
from pathlib import Path


VERSION = "FORJA-ESTILO-HUMANO-v3"

_STOPWORDS = {
    "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "do", "dos",
    "e", "em", "entre", "era", "essa", "esse", "esta", "este", "foi", "há",
    "isso", "isto", "já", "lhe", "mais", "mas", "na", "nas", "não", "no",
    "nos", "o", "os", "ou", "para", "pela", "pelas", "pelo", "pelos", "por",
    "que", "se", "sem", "ser", "seu", "sua", "suas", "também", "um", "uma",
}

_CONTRASTES_ARTIFICIAIS = (
    (r"\bn[ãa]o\s+apenas\b[^.!?\n]{0,220}\bmas\s+tamb[ée]m\b", "não apenas... mas também"),
    (r"\b(?:a|esta|essa)\s+quest[ãa]o\s+n[ãa]o\s+(?:[ée]|consiste\s+em)\b[^.!?\n]{0,220}\bmas\b", "a questão não é X, mas Y"),
    (r"\bn[ãa]o\s+se\s+trata\s+de\b[^.!?\n]{0,220}\bmas\s+(?:de|sim)\b", "não se trata de X, mas de Y"),
)

_METADISCURSO_VAZIO = (
    (r"(?:^|[.!?]\s+)(vale\s+(?:destacar|ressaltar|observar))\b", "vale destacar/ressaltar"),
    (r"(?:^|[.!?]\s+)(cumpre\s+(?:destacar|ressaltar|observar))\b", "cumpre destacar/ressaltar"),
    (r"(?:^|[.!?]\s+)(em\s+outras\s+palavras)\b", "em outras palavras"),
    (r"(?:^|[.!?]\s+)(isso\s+significa\s+que)\b", "isso significa que"),
    (r"(?:^|[.!?]\s+)(em\s+conclus[ãa]o)\b", "em conclusão"),
    (r"(?:^|[.!?]\s+)([ée]\s+(?:cedi[çc]o|consabido|pacífico)\s+que)\b", "é cediço/consabido/pacífico que"),
    (r"(?:^|[.!?]\s+)(como\s+(?:se\s+sabe|[ée]\s+sabido|[ée]\s+de\s+conhecimento\s+geral))\b",
     "como se sabe/é de conhecimento geral"),
)

_CLICHES = (
    (r"\balicerce\s+d[oa]\s+(?:progresso|desenvolvimento|justi[çc]a)\b", "metáfora genérica de alicerce"),
    (r"\bchave\s+para\s+(?:o|a)\s+(?:progresso|desenvolvimento|compreens[ãa]o|solu[çc][ãa]o)\b", "metáfora genérica de chave"),
    (r"\b(?:pilar|papel)\s+fundamental\b", "clichê de fundamentalidade"),
    (r"\b(?:cen[áa]rio|contexto)\s+(?:complexo|desafiador|em constante evolu[çc][ãa]o)\b", "clichê contextual genérico"),
)

_CONECTORES = (
    "além disso", "contudo", "entretanto", "portanto", "dessa forma", "desse modo",
    "assim", "em síntese", "nesse sentido", "por outro lado", "ademais",
)

_DOGMATICOS_DUROS = (
    "obviamente", "claramente", "sem dúvida", "indiscutivelmente", "inquestionavelmente",
    "evidentemente", "certamente",
)

_DOGMATICOS_CONTEXTO = ("sempre", "nunca", "inequivocamente")

_LASTRO = re.compile(
    r"\b(?:art(?:s)?\.?|lei|decreto|resolu[çc][ãa]o|s[úu]mula|tema|STF|STJ|TRF\d?|"
    r"TJ[A-Z]{2}|doc\.?|evento|ID|fls?\.?|autos|ac[óo]rd[ãa]o|decis[ãa]o|laudo|"
    r"contrato|cl[áa]usula|prova|per[íi]cia)\b|\d",
    re.I,
)

_PEDIDO_CONCRETO = re.compile(
    r"\b(?:requer|pede|postula|solicita|deve\s+ser\s+(?:provido|acolhido|rejeitado)|"
    r"seja\s+(?:provido|acolhido|rejeitado|deferido|intimado|condenado))\b",
    re.I,
)

_EMAIL_FORMULAS = (
    (r"\bespero\s+que\s+(?:esta|essa|a presente)\s+(?:mensagem|e-?mail)\s+(?:o|a|os|as)?\s*encontre\s+bem\b",
     "abertura traduzida do inglês: espero que esta mensagem o encontre bem"),
    (r"\bespero\s+que\s+(?:voc[êe]|o senhor|a senhora)\s+esteja\s+bem\b",
     "abertura genérica sem relação com o assunto"),
    (r"\bvenho\s+por\s+meio\s+(?:deste|desta|do presente)\b",
     "formalidade burocrática vazia: venho por meio deste"),
    (r"\bgostaria\s+de\s+(?:informar|comunicar|compartilhar|encaminhar|aproveitar)\b",
     "verbo de intenção retarda a informação principal"),
    (r"\b[ée]\s+com\s+(?:grande\s+)?(?:satisfa[çc][ãa]o|prazer)\s+que\b",
     "cerimônia genérica incompatível com e-mail operacional"),
    (r"\bn[ãa]o\s+hesite\s+em\s+(?:entrar\s+em\s+contato|me\s+procurar)\b",
     "fecho traduzido e impessoal: não hesite em entrar em contato"),
    (r"\b(?:fico|permane[çc]o)\s+[àa]\s+disposi[çc][ãa]o\s+para\s+quaisquer\s+esclarecimentos(?:\s+adicionais|\s+que\s+se\s+fa[çc]am\s+necess[áa]rios)?\b",
     "fecho inflado; prefira 'Fico à disposição.'"),
    (r"\bagrade[çc]o\s+antecipadamente\b",
     "cortesia automática e antecipada"),
    (r"\b(?:realizei|elaborei|preparei)\s+(?:uma\s+)?(?:an[áa]lise|revis[ãa]o|avalia[çc][ãa]o)\s+(?:abrangente|detalhada|cuidadosa|minuciosa)\b",
     "autonarração de esforço; informe o resultado concreto"),
)

_EMAIL_CABECALHOS_ARTIFICIAIS = re.compile(
    r"(?im)^\s*(?:#{1,6}\s*)?(?:resumo\s+executivo|contexto|conclus[ãa]o|considera[çc][õo]es\s+finais|vis[ãa]o\s+geral)\s*:?[\s*]*$"
)


PROMPT_F6_F7 = """

PROTOCOLO OBRIGATÓRIO DE ESCRITA HUMANA — FORJA-ESTILO-HUMANO-v2
- Escreva como advogado responsável pelo caso, com voz específica, posição definida e lastro.
- Cada parágrafo deve cumprir uma função concreta: fato/prova, regra, aplicação, refutação ou pedido.
- Elimine frases que apenas anunciam ênfase, explicam o óbvio ou repetem a frase anterior.
- Não use as fórmulas "não apenas... mas também", "a questão não é X, mas Y" ou
  "não se trata de X, mas de Y".
- Evite conectores em série, simetria de parágrafos, sequências de frases com o mesmo ritmo,
  travessões explicativos repetidos, metáforas genéricas e conclusão que apenas recapitula.
- Nunca use "claramente", "obviamente", "sem dúvida", "sempre" ou "nunca" para suprir prova.
- Não apresente todos os lados por ritual nem responda além da questão jurisdicional.
- Antes de aprovar, corte tudo cuja retirada não altere a compreensão ou a decisão pretendida.

PROTOCOLO DE GOSTO JURÍDICO AUTÔNOMO — FORJA-GOSTO-EDGE-v1
Execute o processo abaixo internamente; entregue somente a peça, sem narrar o método:
- EXACTING: produza ao menos três arquiteturas retóricas possíveis e rejeite as que apenas
  reorganizam a versão óbvia. A primeira versão fluente não é presumida boa.
- DIFFERENTIATED: identifique a formulação genérica que qualquer IA produziria e escolha
  um fio decisivo específico deste processo, sustentado por fatos, provas e limites reais.
- GROUNDED: toda afirmação que precise ser verdadeira deve estar ligada à fonte já fornecida.
  Se o lastro faltar, preserve a lacuna; nunca compense com segurança verbal.
- EMOTIONAL: torne perceptível a consequência humana, institucional ou processual que já
  decorre dos autos. Não invente drama, intenção, sofrimento nem adjetivação persuasiva.
- SELEÇÃO: compare as alternativas por poder de decisão, especificidade, lastro e economia.
  Escolha uma, faça uma revisão adversarial e elimine tudo que sobreviva apenas por soar bem.
O gate determinístico será recomputado; autodeclarar aprovação não o contorna.
"""

PROMPT_F9_EMAIL = """

PROTOCOLO OBRIGATÓRIO DE E-MAIL HUMANO — FORJA-ESTILO-HUMANO-v3
- Escreva para a pessoa e para a conversa concreta; use o nome quando conhecido.
- Abra com o que foi feito ou com a decisão que precisa ser tomada. Não use frases de aquecimento.
- Não use "espero que este e-mail o encontre bem", "venho por meio deste", "gostaria de informar",
  "não hesite em entrar em contato" ou fechos cerimoniosos equivalentes.
- Não narre o próprio esforço ("análise abrangente", "revisão cuidadosa"). Diga o resultado.
- Use verbos concretos e poucos parágrafos. Ajuste a cadência à conversa; não transforme o e-mail em relatório.
- Mantenha apenas o contexto necessário para o destinatário compreender anexos, decisão e próximo passo.
- Preserve o bloco "Pontos que exigem o seu olho" quando aplicável, com alertas concretos e páginas.
- Feche de forma simples: "Fico à disposição." ou outro fecho natural adequado à conversa.
O corpo será validado e terá o hash conferido antes do registro do rascunho.
"""


def mandatory_prompt_for_phase(phase: str) -> str:
    """Injeta o protocolo na redação/auditoria da peça e no e-mail de F9."""
    if phase in {"F6_REDACAO_TEMPLATE", "F7_AUDITORIA_JURIDICA_FACTUAL"}:
        return PROMPT_F6_F7
    if phase == "F9_PACOTE_REVISAO_DRAFT_OPCIONAL":
        return PROMPT_F9_EMAIL + mandatory_prompt_for_channel("email")
    return ""


def mandatory_prompt_for_channel(tipo: str) -> str:
    """Entrega o perfil positivo configurado para e-mail ou mensagem.

    O motor permanece genérico: o conteúdo concreto é resolvido pelo acervo da
    instalação e nunca é incorporado neste arquivo publicável.
    """
    if tipo not in {"email", "mensagem"}:
        return ""
    from forja_estilo_casa import prompt

    return prompt(tipo)


def _sem_acentos(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.lower())
    return "".join(char for char in value if not unicodedata.combining(char))


def _limpar_markdown(texto: str) -> str:
    texto = re.sub(r"```.*?```", " ", texto, flags=re.S)
    linhas = []
    for linha in texto.splitlines():
        s = linha.strip()
        if s.startswith(">") or s.startswith("|") or re.match(r"^\s*#{1,6}\s", linha):
            continue
        if re.match(r"^\s*[-*_]{3,}\s*$", linha):
            continue
        linhas.append(linha)
    return "\n".join(linhas)


def _limpar_email(texto: str) -> str:
    """Remove histórico citado sem apagar cabeçalhos artificiais da mensagem nova."""
    texto = re.sub(r"```.*?```", " ", texto, flags=re.S)
    linhas = []
    em_historico = False
    for linha in texto.splitlines():
        s = linha.strip()
        if s.startswith(">"):
            continue
        if re.match(
            r"^-{2,}\s*(?:mensagem\s+(?:encaminhada|original)|forwarded message|original message)\s*-{2,}$",
            s,
            re.I,
        ):
            em_historico = True
            continue
        if em_historico:
            continue
        linhas.append(linha)
    return "\n".join(linhas)


def _contexto(texto: str, inicio: int, fim: int, alcance: int = 85) -> str:
    return " ".join(texto[max(0, inicio - alcance): min(len(texto), fim + alcance)].split())


def _achado(regra: str, severidade: str, trecho: str, problema: str, acao: str, **extra) -> dict:
    item = {
        "gate": f"G10-escrita-humana/{regra}",
        "sev": severidade,
        "trecho": trecho[:320],
        "problema": problema,
        "acao": acao,
        "versao": VERSION,
    }
    item.update(extra)
    return item


def _paragrafos(texto: str) -> list[str]:
    saida = []
    for bloco in re.split(r"\n\s*\n+", texto):
        bloco = " ".join(linha.strip() for linha in bloco.splitlines() if linha.strip())
        bloco = re.sub(r"^\*{0,2}\d{1,3}[.)]\*{0,2}\s+", "", bloco)
        bloco = bloco.strip(" *_")
        if len(re.findall(r"\b[\wÀ-ÿ]+\b", bloco)) < 7:
            continue
        if (bloco.startswith(('"', '“')) and bloco.endswith(('"', '”'))) or bloco.startswith("Fonte:"):
            continue
        saida.append(bloco)
    return saida


def _sentencas(paragrafo: str) -> list[str]:
    partes = re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9])", paragrafo)
    return [p.strip() for p in partes if len(re.findall(r"\b[\wÀ-ÿ]+\b", p)) >= 4]


def _tokens(texto: str) -> list[str]:
    normal = _sem_acentos(texto)
    return [t for t in re.findall(r"\b[a-z]{3,}\b", normal) if t not in _STOPWORDS]


def _cv(valores: list[int]) -> float:
    media = statistics.mean(valores) if valores else 0
    return statistics.pstdev(valores) / media if media else 0.0


def _padroes_fixos(texto: str) -> list[dict]:
    achados = []
    for padrao, nome in _CONTRASTES_ARTIFICIAIS:
        for match in re.finditer(padrao, texto, re.I):
            achados.append(_achado(
                "contraste-formular", "P0", _contexto(texto, match.start(), match.end()),
                f"estrutura contrastiva formulaica: {nome}",
                "afirme diretamente a tese e apresente, na frase seguinte, o fundamento específico",
            ))
    for padrao, nome in _METADISCURSO_VAZIO:
        for match in re.finditer(padrao, texto, re.I):
            achados.append(_achado(
                "metadiscurso-vazio", "P0", _contexto(texto, match.start(), match.end()),
                f"conector anuncia importância sem acrescentar conteúdo: {nome}",
                "apague a expressão e comece pelo fato, norma ou inferência que importa",
            ))
    for padrao, nome in _CLICHES:
        for match in re.finditer(padrao, texto, re.I):
            achados.append(_achado(
                "cliche-generico", "P0", _contexto(texto, match.start(), match.end()),
                nome,
                "substitua a metáfora por consequência jurídica verificável e específica do caso",
            ))
    return achados


def _conectores(texto: str, paragrafos: list[str]) -> list[dict]:
    ocorrencias = []
    alternancia = "|".join(re.escape(item) for item in sorted(_CONECTORES, key=len, reverse=True))
    padrao = re.compile(rf"(?:^|[.!?]\s+|\n\s*\n+)({alternancia})\b", re.I)
    for match in padrao.finditer(texto):
        ocorrencias.append((match.group(1).lower(), match.start(1), match.end(1)))
    if not ocorrencias:
        return []
    contagem = Counter(_sem_acentos(item[0]) for item in ocorrencias)
    repetido = max(contagem.values())
    limite = max(4, math.ceil(max(1, len(paragrafos)) * 0.45))
    if repetido >= 3 or len(ocorrencias) > limite:
        inicio, fim = ocorrencias[0][1], ocorrencias[-1][2]
        return [_achado(
            "conectores-em-serie", "P0", _contexto(texto, inicio, fim, 140),
            f"conectores automáticos em densidade alta ({len(ocorrencias)}; máximo repetido={repetido})",
            "retire conectores de abertura e faça a relação lógica decorrer da ordem dos fatos e fundamentos",
            contagem=dict(contagem), limite=limite,
        )]
    if len(ocorrencias) >= 3:
        return [_achado(
            "conectores-em-serie", "P1", _contexto(texto, ocorrencias[0][1], ocorrencias[-1][2], 120),
            f"densidade de conectores merece revisão editorial ({len(ocorrencias)})",
            "confirme que cada conector é indispensável e varie a construção sintática",
            contagem=dict(contagem), limite=limite,
        )]
    return []


# Numeração de seção que o COMPOSITOR injeta ("I — CABIMENTO E TEMPESTIVIDADE"),
# não aparte explicativo do autor. Sem esta exceção o gate cobra do texto um vício
# que não está nele: o Agravo do CASO-18 tem 3 travessões em 3.504 palavras no
# markdown auditado e chegava a 10 no DOCX, todos títulos numerados por
# `PecaVisual.abre()`. O efeito era perverso: quanto MAIS o autor seccionasse a
# peça, mais "aparte" o gate enxergava.
#
# A exceção precisa ser ESTREITA, sob pena de virar escape. A primeira versão
# exigia só "romano + travessão + maiúscula", e a revisão cruzada (Codex,
# 05/08/2026) a quebrou em duas linhas: `[IVXLCDM]+` aceita "XXXXXXXXXXXXXX", que
# não é algarismo romano nenhum, e olhar apenas o token anterior deixava passar
# "Precedente VIII — Sem Fundamento", que é prosa, não título. Duas condições
# fecham isso:
#   1. o algarismo tem de ser bem formado e estar na tabela de I a XXX;
#   2. ele tem de ABRIR a linha — que é a posição de um título, e não a de um
#      aparte no meio do período.
_ROMANOS_SECAO = frozenset({
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
    "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX",
})


def _e_titulo_numerado(texto: str, pos: int) -> bool:
    """O travessão em `pos` separa o número de seção do título que abre a linha?"""
    inicio = texto.rfind("\n", 0, pos) + 1
    prefixo = texto[inicio:pos].strip()
    if prefixo not in _ROMANOS_SECAO:
        return False
    resto = texto[pos + 1:].lstrip()
    return bool(resto) and resto[0].isupper()


def _travessoes(texto: str) -> list[dict]:
    ocorrencias = [m for m in re.finditer(r"(?<=\s)—(?=\s)", texto)
                   if not _e_titulo_numerado(texto, m.start())]
    palavras = len(re.findall(r"\b[\wÀ-ÿ]+\b", texto))
    limite = max(3, math.ceil(palavras / 450))
    if len(ocorrencias) > limite:
        return [_achado(
            "travessao-repetido", "P0", _contexto(texto, ocorrencias[0].start(), ocorrencias[-1].end(), 150),
            f"travessão explicativo repetido ({len(ocorrencias)} em {palavras} palavras; limite={limite})",
            "converta apartes em frases autônomas ou integre a explicação ao período principal",
            contagem=len(ocorrencias), limite=limite,
        )]
    limite_editorial = max(2, math.ceil(palavras / 700))
    if len(ocorrencias) > limite_editorial:
        return [_achado(
            "travessao-repetido", "P1", _contexto(texto, ocorrencias[0].start(), ocorrencias[-1].end(), 130),
            f"frequência de travessões pede revisão ({len(ocorrencias)} em {palavras} palavras)",
            "confirme cada aparte; prefira frase autônoma quando a explicação for substantiva",
            contagem=len(ocorrencias), limite=limite,
        )]
    return []


def _dogmatismo(texto: str, paragrafos: list[str]) -> list[dict]:
    achados = []
    for termo in _DOGMATICOS_DUROS:
        for match in re.finditer(rf"\b{re.escape(termo)}\b", texto, re.I):
            achados.append(_achado(
                "dogmatismo-retorico", "P0", _contexto(texto, match.start(), match.end()),
                f"intensificador categórico substitui demonstração: {match.group(0)}",
                "apague o intensificador e mostre a prova, a norma e a inferência",
            ))
    for paragrafo in paragrafos:
        for termo in _DOGMATICOS_CONTEXTO:
            match = re.search(rf"\b{re.escape(termo)}\b", paragrafo, re.I)
            if not match:
                continue
            tem_lastro = bool(_LASTRO.search(paragrafo))
            achados.append(_achado(
                "absolutismo-sem-lastro", "P1" if tem_lastro else "P0", paragrafo,
                f"afirmação categórica {'com lastro aparente a conferir' if tem_lastro else 'sem lastro no parágrafo'}: {match.group(0)}",
                "delimite a proposição; mantenha o absoluto somente se a fonte realmente o sustentar",
                lastroAparente=tem_lastro,
            ))
    return achados


def _redundancia(paragrafos: list[str]) -> list[dict]:
    achados = []
    for paragrafo in paragrafos:
        sentencas = _sentencas(paragrafo)
        for anterior, atual in zip(sentencas, sentencas[1:]):
            a, b = set(_tokens(anterior)), set(_tokens(atual))
            if min(len(a), len(b)) < 5:
                continue
            inter = a & b
            similaridade = len(inter) / len(a | b)
            cobertura = len(inter) / min(len(a), len(b))
            if len(inter) >= 5 and (similaridade >= 0.58 or cobertura >= 0.78):
                tem_nova_ancora = bool(_LASTRO.search(atual))
                achados.append(_achado(
                    "redundancia-consecutiva", "P1" if tem_nova_ancora else "P0", anterior + " " + atual,
                    f"duas frases consecutivas reformulam a mesma proposição (similaridade={similaridade:.2f})",
                    "confirme se a segunda autoridade/dado acrescenta peso próprio; se não, funda as frases",
                    similaridade=round(similaridade, 3), novaAncoraAparente=tem_nova_ancora,
                ))
        if len(sentencas) >= 3:
            s2 = _sem_acentos(sentencas[1])
            s3 = _sem_acentos(sentencas[2])
            cadeia = re.match(r"^(?:esse|essa|isso|isto|o mesmo|a mesma)\b", s2) and re.match(
                r"^(?:trata-se|em outras palavras|isso significa)\b", s3
            )
            if cadeia and not _LASTRO.search(paragrafo):
                achados.append(_achado(
                    "repeticao-disfarcada", "P0", paragrafo,
                    "cadeia demonstrativa reformula a mesma definição sem dado novo",
                    "substitua as três frases por uma proposição precisa ou acrescente aplicação concreta ao caso",
                ))
    return achados


def _ritmo_robotico(paragrafos: list[str]) -> list[dict]:
    sentencas = [s for p in paragrafos for s in _sentencas(p)]
    achados = []
    inicio_rigido = re.compile(r"^(?:o|a|os|as|ele|ela|eles|elas|este|esta|esse|essa)\s+[a-záéíóúâêôãõç]+\b", re.I)
    for indice in range(0, max(0, len(sentencas) - 3)):
        janela = sentencas[indice: indice + 4]
        tamanhos = [len(re.findall(r"\b[\wÀ-ÿ]+\b", s)) for s in janela]
        if all(inicio_rigido.search(s) for s in janela) and max(tamanhos) <= 24 and _cv(tamanhos) <= 0.22 \
                and not any(_LASTRO.search(s) for s in janela):
            achados.append(_achado(
                "ritmo-robotico", "P0", " ".join(janela),
                "quatro frases seguidas repetem estrutura curta e ritmo quase uniforme",
                "combine relações causais, varie a extensão e dê prioridade à frase que move o argumento",
                tamanhos=tamanhos,
            ))
            break
    return achados


def _simetria(paragrafos: list[str]) -> list[dict]:
    if len(paragrafos) < 6:
        return []
    tamanhos = [len(re.findall(r"\b[\wÀ-ÿ]+\b", p)) for p in paragrafos]
    tamanhos = [n for n in tamanhos if n >= 12]
    if len(tamanhos) < 6:
        return []
    variacao = _cv(tamanhos)
    sent_por_par = [len(_sentencas(p)) for p in paragrafos]
    dominante = Counter(sent_por_par).most_common(1)[0][1] / len(sent_por_par)
    if len(tamanhos) >= 8 and variacao < 0.10 and dominante >= 0.80:
        sev = "P0"
    elif variacao < 0.18 and dominante >= 0.65:
        sev = "P1"
    else:
        return []
    return [_achado(
        "simetria-estrutural", sev, " | ".join(str(n) for n in tamanhos[:12]),
        f"parágrafos excessivamente simétricos (CV={variacao:.2f}; padrão de sentenças={dominante:.0%})",
        "revise a arquitetura pelo peso real de cada argumento, sem igualar artificialmente os blocos",
        coeficienteVariacao=round(variacao, 3), padraoSentencas=round(dominante, 3),
    )]


def _conclusao_tautologica(paragrafos: list[str]) -> list[dict]:
    if len(paragrafos) < 4:
        return []
    ultimo = paragrafos[-1]
    marcador = re.match(r"^(?:dessa forma|desse modo|assim|portanto|em síntese|em conclusão)\b", ultimo, re.I)
    if not marcador or _PEDIDO_CONCRETO.search(ultimo):
        return []
    tokens_fim = set(_tokens(ultimo))
    tokens_corpo = set(_tokens(" ".join(paragrafos[:-1])))
    cobertura = len(tokens_fim & tokens_corpo) / max(1, len(tokens_fim))
    # Menção genérica a "contrato", "prova" ou "decisão" não é novidade. Aqui
    # só conta âncora identificável: número, dispositivo, evento/ID/doc ou tribunal.
    tem_novo_ancoravel = bool(re.search(
        r"\d|\b(?:art(?:s)?\.?|lei|decreto|resolu[çc][ãa]o|s[úu]mula|tema|STF|STJ|TRF\d?|"
        r"TJ[A-Z]{2}|doc\.?|evento|ID|fls?\.?)\b",
        ultimo,
        re.I,
    ))
    if cobertura >= 0.55 or not tem_novo_ancoravel:
        return [_achado(
            "conclusao-tautologica", "P0", ultimo,
            f"parágrafo final recapitula sem pedido, fonte ou consequência nova (cobertura lexical={cobertura:.2f})",
            "apague o parágrafo ou converta-o em pedido/consequência processual concreta",
            coberturaLexical=round(cobertura, 3),
        )]
    return []


def _email_especifico(texto: str, paragrafos: list[str]) -> list[dict]:
    achados = []
    for padrao, problema in _EMAIL_FORMULAS:
        for match in re.finditer(padrao, texto, re.I):
            achados.append(_achado(
                "email-formula-automatica",
                "P0",
                _contexto(texto, match.start(), match.end()),
                problema,
                "reescreva de forma direta, situada na conversa e orientada ao próximo passo",
            ))

    for match in _EMAIL_CABECALHOS_ARTIFICIAIS.finditer(texto):
        achados.append(_achado(
            "email-cara-de-relatorio",
            "P0",
            _contexto(texto, match.start(), match.end()),
            f"cabeçalho artificial em corpo de e-mail: {match.group(0).strip()}",
            "remova o cabeçalho e transforme o conteúdo necessário em uma frase curta",
        ))

    palavras = len(re.findall(r"\b[\wÀ-ÿ]+\b", texto))
    sentencas = [sentenca for paragrafo in paragrafos for sentenca in _sentencas(paragrafo)]
    tamanhos = [len(re.findall(r"\b[\wÀ-ÿ]+\b", sentenca)) for sentenca in sentencas]
    if palavras > 450:
        achados.append(_achado(
            "email-extenso",
            "P1",
            " ".join(texto.split())[:300],
            f"e-mail com {palavras} palavras tende a funcionar como relatório",
            "mova fundamentos e histórico para anexo; deixe no corpo apenas entrega, alertas e próximo passo",
            palavras=palavras,
        ))
    if tamanhos and max(tamanhos) > 55:
        maior = sentencas[tamanhos.index(max(tamanhos))]
        achados.append(_achado(
            "email-periodo-longo",
            "P1",
            maior,
            f"período com {max(tamanhos)} palavras dificulta leitura rápida do e-mail",
            "divida o período e antecipe a informação principal",
            palavrasNoPeriodo=max(tamanhos),
        ))
    if len(paragrafos) > 10:
        achados.append(_achado(
            "email-fragmentado",
            "P1",
            f"{len(paragrafos)} parágrafos",
            "corpo de e-mail excessivamente fragmentado",
            "agrupe informações relacionadas e remova explicações que pertencem aos anexos",
            paragrafos=len(paragrafos),
        ))
    return achados


def analisar(texto: str, tipo: str = "peca") -> list[dict]:
    """Retorna achados auditáveis. A presença isolada de estilo comum não basta para P0."""
    fonte = _limpar_email(texto) if tipo == "email" else texto
    limpo = _limpar_markdown(fonte)
    paragrafos = _paragrafos(limpo)
    achados = []
    achados.extend(_padroes_fixos(limpo))
    achados.extend(_conectores(limpo, paragrafos))
    achados.extend(_travessoes("\n\n".join(paragrafos)))
    achados.extend(_dogmatismo(limpo, paragrafos))
    achados.extend(_redundancia(paragrafos))
    achados.extend(_ritmo_robotico(paragrafos))
    if tipo in {"peca", "estudo"}:
        achados.extend(_simetria(paragrafos))
        achados.extend(_conclusao_tautologica(paragrafos))
    elif tipo == "email":
        achados.extend(_email_especifico(fonte, paragrafos))
    if tipo in {"email", "mensagem"}:
        from forja_estilo_casa import analisar as _analisar_casa

        achados.extend(_analisar_casa(fonte, tipo)["findings"])
    # Deduplica achados equivalentes sem esconder ocorrências distintas relevantes.
    unicos = []
    vistos = set()
    for item in achados:
        chave = (item["gate"], item["sev"], item["trecho"])
        if chave not in vistos:
            vistos.add(chave)
            unicos.append(item)
    return unicos


def relatorio(texto: str, tipo: str = "peca") -> dict:
    achados = analisar(texto, tipo)
    saida = {
        "protocolVersion": VERSION,
        "tipo": tipo,
        "aprovado": not any(item["sev"] == "P0" for item in achados),
        "p0": sum(item["sev"] == "P0" for item in achados),
        "p1": sum(item["sev"] == "P1" for item in achados),
        "achados": achados,
        "metodo": (
            "sinais determinísticos observáveis e método positivo configurado da casa; "
            "não estima autoria nem probabilidade de IA"
        ),
    }
    if tipo in {"email", "mensagem"}:
        from forja_estilo_casa import analisar as _analisar_casa

        saida["houseStyle"] = _analisar_casa(
            _limpar_email(texto) if tipo == "email" else texto,
            tipo,
        )
    return saida


def main() -> int:
    parser = argparse.ArgumentParser(description="Gate FORJA de escrita humana")
    parser.add_argument("arquivo", type=Path)
    parser.add_argument("--tipo", choices=("peca", "estudo", "email"), default="peca")
    args = parser.parse_args()
    payload = relatorio(args.arquivo.read_text(encoding="utf-8"), args.tipo)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["aprovado"] else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
