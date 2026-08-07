# -*- coding: utf-8 -*-
"""
forja_verificador.py — Auditoria automática de peças do FORJA.
Codifica a parte determinística das lições de RETROSPECTIVAS.md (casos 1-5,
08/07/2026) em gates objetivos. Lições que exigem fonte externa/autos continuam
dependendo de auditoria dedicada.

Uso: python forja_verificador.py <arquivo.md> [--tipo peca|estudo|email]
Saída: JSON com violações por gate; exit code 1 se houver violação P0.

Gates:
  G1 personas internas e jargão de processo (lições 17, 24)
  G2 placeholders proibidos × marcadores deliberados (lições 18, 23; erro recorrente 3)
  G3 contagens agregadas sem fonte/método declarado (lição 15)
  G4 pares súmula-tribunal e dispositivos legais notórios (lição 20)
  G5 institutos jurídicos na direção errada (lição 21)
  G6 cara de IA: emojis, símbolos decorativos (lições do caso 1 e 24)
  G7 aritmética de intervalos entre datas (lição 16)
  G8 formato protocolável de peça (lição 24)
  G9 vazamento de proveniência operacional na peça (feedback Fábio, 11/07/2026)
  G10 escrita humana: fórmulas, repetição, ritmo, dogmatismo e conclusão tautológica
  G11 citação a regimento interno sem trecho literal arquivado (emenda E9, 25/07/2026)
"""
import sys, re, json, io
from pathlib import Path

PERSONAS = ["Helena", "Efesto", "Cícero", "Cicero", "Efesto", "Hermes", "Midas", "Íris"]
PERSONAS_CONTEXTO = ["Diana"]  # nome comum: só alerta se perto de "(comunicação)" etc.
JARGAO = [r"n[ií]vel 2", r"\bP[0-4]\b(?!:)", r"\bF\d(?:_|\b)", r"workflow", r"red team",
          r"ultracode", r"subagente", r"fábrica de peti", r"\bprompt\b", r"\bharness\b"]

MARCADORES_LACUNA = re.compile(
    r"\[(?:VERIFICAR(?: EM FONTE OFICIAL)?|DOCUMENTA[ÇC][ÃA]O NECESS[ÁA]RIA|ALERTA|"
    r"DATA A DETERMINAR|DEPENDENTE DE|Texto integral n[ãa]o foi acessado|"
    r"VERIFICA[ÇC][ÃA]O PENDENTE|ESTRAT[ÉE]GICA?|NECESS[ÁA]RIO)[^\]]*\]",
    re.I,
)

# ampliado em 12/07/2026 (M3.1): a mutação semântica S6 provou que Súmula 362
# trocada de tribunal sobrevivia por ausência na tabela — pares acrescidos são
# todos de atribuição notória e inequívoca.
SUMULAS_STJ = {5, 7, 43, 54, 83, 182, 211, 227, 297, 326, 339, 362, 385, 523, 568}
SUMULAS_STF = {150, 269, 271, 279, 282, 283, 284, 356, 383, 473, 735}

DISPOSITIVOS_ERRADOS = [
    (r"[Mm]andado de [Ss]eguran[çc]a\s*\(?\s*CPC",
     "Mandado de segurança é regido pela Lei 12.016/2009, não pelo CPC"),
    (r"art\.?\s*205\s*(?:do\s*)?(?:C[óo]digo Civil|CC)\b(?![\d.])",
     "Conferir: art. 205 CC é o prazo decenal geral; prazos especiais (3 anos etc.) estão no art. 206"),
    (r"(?:trienal|3 anos|tr[êe]s anos)[^.\n]{0,60}art\.?\s*205",
     "Prazo trienal é do art. 206, § 3º, do CC; art. 205 é o decenal"),
    (r"C[óo]digo Civil,?\s*art\.?\s*37\b",
     "O art. 37, § 6º (responsabilidade do Estado) é da CF, não do Código Civil"),
    (r"[Aa]gravo de instrumento\s*\(?\s*CPC,?\s*arts?\.?\s*1\.?042",
     "Agravo de instrumento contra interlocutória é o art. 1.015 do CPC; o art. 1.042 é o agravo em REsp/RE"),
    # art. 343-A do RISTJ EXISTE desde a ER 53/2026 (DJe 01/07/2026): resumo
    # obrigatório de fatos, pedidos e decisões nas petições ao STJ. Regra
    # anterior negava a existência — corrigida em 10/07/2026 (fonte:
    # cache/fontes_oficiais/STJ_ER_53_2026_art_343A.md). Só flagrar uso do
    # dispositivo fora do STJ (o resumo em outros tribunais é padrão editorial
    # do escritório, não exigência regimental deles).
    (r"art\.?\s*343\s*[-–—]?\s*A\s*(?:,|\s+do)?\s+(?:RITJ\w+|RITRF\w*|Regimento Interno do (?:TJ|TRF)\w*)",
     "O art. 343-A (resumo obrigatório) é do RISTJ (ER 53/2026); regimentos de TJ/TRF não têm esse dispositivo — em outros tribunais o resumo é padrão editorial do escritório"),
    (r"art\.?\s*202,?\s*(?:inc\.?|inciso)?\s*I\b[^IVX][^.\n]{0,60}reconhecimento",
     "Interrupção da prescrição por reconhecimento do devedor é o art. 202, VI, do CC (o inciso I é o despacho que ordena a citação)"),
    (r"S[úu]mula\s*(?:n?[ºo°.]?\s*)?7\s*/?\s*(?:do\s*)?STF[^0-9]",
     "A Súmula 7 (reexame de prova) é do STJ; no STF o correlato é a Súmula 279"),
]

INSTITUTOS_DIRECIONAIS = [
    (r"(?:credora?|empresa|particular|autora?|fornecedor)[^.]{0,140}(?:promov|protocol|ajuiz|requer)[^.]{0,80}execu[çc][ãa]o fiscal",
     "Execução fiscal (Lei 6.830/1980) é instrumento DA Fazenda contra seus devedores — não do particular contra ente público"),
    (r"execu[çc][ãa]o fiscal[^.]{0,120}contra\s+(?:o\s+)?(?:munic[íi]pio|prefeitura|Fazenda|ente p[úu]blico)",
     "Execução fiscal contra o município é inversão do instituto; a via é cumprimento de sentença (CPC 534-535) + precatório"),
    (r"inscri[çc][ãa]o[^.]{0,80}d[íi]vida ativa[^.]{0,140}(?:credora?|em favor d|da empresa|do particular|do fornecedor)",
     "Dívida ativa é crédito DA Fazenda; credor privado não inscreve crédito contra o município"),
    (r"penhora[^.]{0,100}(?:receitas?|contas?|bens|FPM)[^.]{0,80}(?:municipal|do munic[íi]pio|da prefeitura|da Fazenda|p[úu]blic)",
     "Bens e receitas públicos são impenhoráveis; execução contra a Fazenda segue CPC 534-535 e precatórios (CF art. 100)"),
    (r"bloqueio de caixa[^.]{0,60}(?:municipal|do munic[íi]pio|da prefeitura)",
     "Não há bloqueio de caixa de ente público como regra; exceção estreita é o sequestro por preterição (CF art. 100, § 6º)"),
]

EMOJIS = re.compile("[\U0001F300-\U0001FAFF✅❌⚠⭐✔❗❤➡⚙]")
SEPARADOR_MD = re.compile(r"(?m)^\s*-{3,}\s*$")
FECHO_IA = re.compile(r"(?m)^\s*(?:\*\*)?FIM\s+D[EAO]S?\s+(?:DOCUMENTO|PE[ÇC]A|MEMORIAL|RELAT[ÓO]RIO|ESTUDO|PARECER|MINUTA)\b")

ROTULOS_PRODUCAO = [
    (r"(?im)^\s*#{0,6}\s*ENDERE[ÇC]AMENTO\s*$",
     "rótulo estrutural 'ENDEREÇAMENTO' não existe em peça real"),
    (r"(?im)^\s*#{0,6}\s*IDENTIFICA[ÇC][ÃA]O DO PROCESSO\s*$",
     "rótulo estrutural 'IDENTIFICAÇÃO DO PROCESSO' não existe em peça real"),
]

ARTEFATOS_INTERNOS = [
    (r"matriz de seguran[çc]a factual", "matriz interna vazou para a peça"),
    (r"ap[êe]ndice interno", "apêndice interno vazou para a peça"),
    (r"notas de produ[çc][ãa]o", "nota de produção vazou para a peça"),
    (r"marcadores do harness", "marcador do harness vazou para a peça"),
]

PROVENIENCIA_OPERACIONAL = [
    (r"compartilhad[oa]s?\s+(?:pela?|com\s+o)\s+escrit[óo]rio", "origem operacional do documento vazou para a peça"),
    (r"recebid[oa]s?\s+(?:por|via)\s+e-?mail", "canal interno de recebimento vazou para a peça"),
    (r"recebid[oa]s?\s+(?:por|via)\s+WhatsApp", "canal interno de recebimento vazou para a peça"),
    (r"(?:localizad[oa]|encontrad[oa])s?\s+(?:na|em uma?)\s+pasta\s+(?:interna|local|do escrit[óo]rio)", "localização interna vazou para a peça"),
    (r"(?:arquivo|caminho)\s+(?:local|interno)", "referência a arquivo/caminho interno vazou para a peça"),
    (r"(?:Google\s+)?Drive\s+(?:do|da|interno|compartilhado)", "repositório operacional vazou para a peça"),
    (r"\[FONTE\s*:\s*arquivo[^\]]*\]", "marcador interno de fonte vazou para a peça"),
    (r"[A-Za-z]:\\(?:Users|Documentos|Projetos|\.claude|\.hermes)\\", "caminho de computador vazou para a peça"),
    # A paginação do PDF que recebemos é localizador do NOSSO arquivo, não dos
    # autos: ela muda conforme quem exportou e como. Entrou aqui em 06/08/2026,
    # depois que os memoriais do EDcl no AI 0006526 saíram com sete referências
    # a "p. PDF" e quem as trocou por e-fl. foi o revisor humano, não o gate —
    # que já existia e simplesmente não conhecia essa forma. Fl./e-fl., evento,
    # ID e Doc. continuam livres, porque são localizadores processuais reais.
    (r"\b(?:pp?\.|p[áa]ginas?)\s*(?:do\s+)?PDF\s*\d", "paginação do arquivo PDF usada como localizador dos autos"),
    (r"\bPDF\s*(?:pp?\.|p[áa]ginas?)\s*\d", "paginação do arquivo PDF usada como localizador dos autos"),
]


def _ctx(texto, ini, fim, alcance=60):
    return " ".join(texto[max(0, ini - alcance):min(len(texto), fim + alcance)].split())


# G11 — citação regimental sem lastro conferido (emenda E9 do plano de 25/07/2026).
#
# O falso alarme de 25/07/2026 sobre o art. 343-A do RISTJ nasceu de regimentos
# arquivados que listam as emendas ao final sem incorporá-las ao corpo: a busca
# local não achava um dispositivo que existia. Um gate que exige lastro conferido
# resolve o problema nos dois sentidos — bloqueia a citação inventada e obriga a
# arquivar a fonte da citação verdadeira.
CITACAO_REGIMENTAL = re.compile(
    r"art(?:igo)?s?\.?\s*(?P<artigo>\d+(?:\s*[-–—]\s*[A-Z])?)(?![\d.])"
    r"[^.;\n]{0,40}?\b(?:do\s+|da\s+)?"
    r"(?:RI(?P<sigla>STJ|STF|TJ[A-Z]{2}|TRF\d)\b"
    r"|Regimento\s+Interno\s+(?:do|da)\s+(?P<tribunal>TJ[A-Z]{2}|TRF\d|STJ|STF|"
    r"Superior\s+Tribunal\s+de\s+Justi[çc]a|Supremo\s+Tribunal\s+Federal))",
    re.I,
)
_TRIBUNAL_CANONICO = {
    "SUPERIOR TRIBUNAL DE JUSTIÇA": "STJ",
    "SUPERIOR TRIBUNAL DE JUSTICA": "STJ",
    "SUPREMO TRIBUNAL FEDERAL": "STF",
}
_DATA_CONFERENCIA = re.compile(
    r"conferid[oa]\s+em\W{0,4}\s*(?:\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})", re.I
)


def _indice_fontes_oficiais():
    """Verbatins arquivados no cache, por nome de arquivo.

    Só texto legível entra: o PDF fica ao lado como prova primária, mas quem
    responde por 'o trecho está no ledger' é o verbatim transcrito.
    """
    raiz = Path(__file__).resolve().parent / "cache" / "fontes_oficiais"
    indice = {}
    if not raiz.is_dir():
        return indice
    for caminho in sorted(raiz.iterdir()):
        if caminho.suffix.casefold() in {".txt", ".md"} and caminho.is_file():
            try:
                indice[caminho.name] = caminho.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
    return indice


def gate_g11(texto, fontes=None):
    """Toda citação a regimento interno precisa de trecho literal arquivado."""
    v = []
    if fontes is None:
        fontes = _indice_fontes_oficiais()
    for m in CITACAO_REGIMENTAL.finditer(texto):
        artigo = re.sub(r"\s+", "", m.group("artigo")).upper().replace("—", "-").replace("–", "-")
        bruto = (m.group("sigla") or m.group("tribunal") or "").upper()
        sigla = _TRIBUNAL_CANONICO.get(bruto, bruto)
        # Duas exigências independentes: o artigo tem de aparecer no verbatim, e
        # o verbatim tem de ser do mesmo tribunal. O tribunal é reconhecido pelo
        # nome do arquivo, nunca por menção no corpo — um arquivo do RISTJ que
        # cite o TJTO de passagem não faz lastro de dispositivo do TJTO.
        # Lastro é a linha que DEFINE o dispositivo — "Art. 343-A. Nos termos…" —
        # e não qualquer menção a ele. Sem isso, a prosa de um comentário sobre o
        # artigo passaria por transcrição dele. O ponto após o número é o que
        # separa a definição da referência; o lookahead de letra impede que
        # "art. 343" se dê por lastreado pelo verbatim do "art. 343-A".
        alvo = re.compile(
            r"(?:^|[\s*_>])Art(?:igo)?\.?\s*"
            + re.escape(artigo).replace(r"\-", r"\s*[-–—]?\s*")
            + r"(?![\d]|\s*[-–—]\s*[A-Za-z])\s*[.º°]",
        )
        lastro = [
            nome for nome, conteudo in fontes.items()
            if re.search(r"(?:^|[_\-])RI?" + re.escape(sigla) + r"(?:[_\-.]|$)", nome.upper())
            and alvo.search(conteudo)
        ]
        if not lastro:
            v.append({
                "gate": "G11-regimento", "sev": "P0",
                "trecho": _ctx(texto, m.start(), m.end(), 40),
                "problema": (
                    f"citação regimental '{m.group(0).strip()}' sem trecho literal arquivado em "
                    "cache/fontes_oficiais — conferir na fonte oficial vigente e arquivar antes de citar"
                ),
            })
        elif not any(_DATA_CONFERENCIA.search(fontes[nome][:1200]) for nome in lastro):
            v.append({
                "gate": "G11-regimento", "sev": "P1",
                "trecho": _ctx(texto, m.start(), m.end(), 40),
                "problema": (
                    f"lastro de '{m.group(0).strip()}' existe em {lastro[0]}, mas sem data de "
                    "conferência declarada — regimento é norma mutável e o lastro precisa de data"
                ),
            })
    return v


def gate_g1(texto):
    v = []
    for p in set(PERSONAS):
        for m in re.finditer(r"\b" + p + r"\b", texto):
            if p == "Helena":
                contexto = texto[max(0, m.start() - 20):m.end() + 20]
                if re.search(r"\bRegina\s+Helena\s+Costa\b", contexto, re.I):
                    continue
            v.append({"gate": "G1-personas", "sev": "P0", "trecho": _ctx(texto, m.start(), m.end()),
                      "problema": "persona interna '" + p + "' no produto"})
    for p in PERSONAS_CONTEXTO:
        for m in re.finditer(r"\b" + p + r"\b\s*\((?:comunica|decis|estrat|execu)", texto):
            v.append({"gate": "G1-personas", "sev": "P0", "trecho": _ctx(texto, m.start(), m.end()),
                      "problema": "persona interna '" + p + "' com papel atribuído"})
    for j in JARGAO:
        for m in re.finditer(j, texto, re.I):
            v.append({"gate": "G1-jargao", "sev": "P1", "trecho": _ctx(texto, m.start(), m.end()),
                      "problema": "jargão interno '" + m.group(0) + "'"})
    return v


def gate_g2(texto, tipo="peca"):
    v = []
    for m in MARCADORES_LACUNA.finditer(texto):
        v.append({
            "gate": "G2-placeholder",
            "sev": "P0" if tipo == "peca" else "P1",
            "trecho": m.group(0),
            "problema": "marcador de lacuna no produto externo — resolver ou mover para o relatório interno",
        })
    limpo = MARCADORES_LACUNA.sub("", texto)
    # links markdown [texto](url) são sintaxe legítima, não placeholder
    # (falso positivo flagrado na auditoria de 10/07/2026 — dossiê Roraima)
    limpo = re.sub(r"\[[^\]\n]{1,120}\]\((?:https?://|#|\./|\.\./|mailto:)[^)\s]+\)", "", limpo)
    for m in re.finditer(r"\[[^\]\n]{1,70}\]", limpo):
        t = m.group(0)
        if re.match(r"\[\^?\d+\]", t) or re.match(r"\[[a-z]\)\]", t):
            continue
        if t.upper().startswith("[BLOQUEADOR"):
            sev, prob = "P0", "marcador interno de bloqueador dentro da peça — mover para o relatório"
        elif re.match(r"\[(DIA|DATA|M[ÊE]S|ANO|NOME|CRC|VALOR|CPF|CNPJ|OAB|ENDERE[ÇC]O)", t, re.I):
            sev, prob = "P0", "placeholder de dado esquecido na peça"
        else:
            sev, prob = "P1", "placeholder/marcador fora da lista aprovada — confirmar se é deliberado"
        v.append({"gate": "G2-placeholder", "sev": sev, "trecho": t, "problema": prob})
    return v


def gate_g3(texto):
    v = []
    for m in re.finditer(r"\b(\d{2,4})\s+(cl[áa]usulas|documentos|precedentes|julgados|inqu[ée]ritos|processos|dispositivos)\b", texto, re.I):
        ctx = texto[max(0, m.start() - 220):min(len(texto), m.end() + 220)]
        if not re.search(r"(refer[êe]nc|contagem|rela[çc][ãa]o|conforme|nominad|Anexo|listad|constam?|mais de|cerca de|aproximadamente|dezenas|mencion|-Chave|matriz|informad[oa]s?\s+no|e-mail do escrit[óo]rio|quantitativo informado|item\s+\d+|segundo o comando)", ctx, re.I):
            v.append({"gate": "G3-contagem", "sev": "P1", "trecho": " ".join(ctx.split())[:180],
                      "problema": "contagem agregada '" + m.group(0) + "' sem fonte/método declarado no entorno"})
    return v


def gate_g4(texto):
    v = []
    for m in re.finditer(r"S[úu]mula\s*(?:[Vv]inculante\s*)?(?:n?[ºo°.]?\s*)?(\d{1,4})\s*(?:d[oe]\s*|/)\s*(STF|STJ)", texto, re.I):
        num, trib = int(m.group(1)), m.group(2).upper()
        if "inculante" in m.group(0):
            continue
        if trib == "STF" and num in SUMULAS_STJ and num not in SUMULAS_STF:
            v.append({"gate": "G4-sumula", "sev": "P0", "trecho": m.group(0),
                      "problema": "Súmula " + str(num) + " é do STJ, não do STF"})
        if trib == "STJ" and num in SUMULAS_STF and num not in SUMULAS_STJ:
            v.append({"gate": "G4-sumula", "sev": "P0", "trecho": m.group(0),
                      "problema": "Súmula " + str(num) + " é do STF, não do STJ"})
    for pat, msg in DISPOSITIVOS_ERRADOS:
        for m in re.finditer(pat, texto):
            v.append({"gate": "G4-dispositivo", "sev": "P0", "trecho": _ctx(texto, m.start(), m.end(), 40),
                      "problema": msg})
    return v


NEGACOES_G5 = re.compile(r"n[ãa]o (?:existe|h[áa]|cabe|se admite|prometa?)|impenhor[áa]|invi[áa]vel|vedad|inaplic[áa]vel|n[ãa]o \S+ como regra", re.I)


def gate_g5(texto):
    v = []
    for pat, msg in INSTITUTOS_DIRECIONAIS:
        for m in re.finditer(pat, texto, re.I | re.S):
            entorno = texto[max(0, m.start() - 160):min(len(texto), m.end() + 160)]
            if NEGACOES_G5.search(entorno):
                continue  # o texto está NEGANDO o instituto — uso correto
            v.append({"gate": "G5-instituto", "sev": "P0",
                      "trecho": " ".join(m.group(0).split())[:200], "problema": msg})
    return v


def gate_g6(texto, tipo="peca"):
    v = []
    for m in EMOJIS.finditer(texto):
        v.append({"gate": "G6-emoji", "sev": "P0", "trecho": _ctx(texto, m.start(), m.end(), 40),
                  "problema": "emoji/símbolo decorativo em documento jurídico"})
    # Anti-trava: a composição OOXML ignora '---' (não vaza para o Word); fica como aviso.
    for m in SEPARADOR_MD.finditer(texto):
        v.append({"gate": "G6-cara-ia", "sev": "P1", "trecho": m.group(0),
                  "problema": "separador markdown '---' no fonte (a composição o ignora; preferir texto sem separadores)"})
    for m in FECHO_IA.finditer(texto):
        v.append({"gate": "G6-cara-ia", "sev": "P0", "trecho": _ctx(texto, m.start(), m.end(), 40),
                  "problema": "fecho com cara de artefato de IA"})
    return v


def gate_g7(texto):
    v = []
    pat = (r"(\d{1,2})/(\d{1,2})/(\d{4})[^.;\n]{0,120}?(\d{1,3})\s*(mes(?:es)?|anos?)\s*"
           r"(?:depois|antes|ap[óo]s)[^(;.\n]{0,50}\((\d{1,2})/(\d{1,2})/(\d{4})\)")
    for m in re.finditer(pat, texto):
        a1, m1 = int(m.group(3)), int(m.group(2))
        a2, m2 = int(m.group(8)), int(m.group(7))
        n, unidade = int(m.group(4)), m.group(5)
        meses_reais = abs((a2 - a1) * 12 + (m2 - m1))
        alvo = n * 12 if unidade.startswith("ano") else n
        if abs(meses_reais - alvo) > 1:
            v.append({"gate": "G7-datas", "sev": "P0", "trecho": " ".join(m.group(0).split())[:170],
                      "problema": "intervalo declarado de " + str(n) + " " + unidade +
                                  " difere do real (~" + str(meses_reais) + " meses)"})
    return v


def gate_g8(texto, tipo):
    v = []
    if tipo == "peca":
        for pat, msg in ROTULOS_PRODUCAO:
            for m in re.finditer(pat, texto):
                v.append({"gate": "G8-formato", "sev": "P0", "trecho": _ctx(texto, m.start(), m.end(), 40),
                          "problema": msg})
        for pat, msg in ARTEFATOS_INTERNOS:
            for m in re.finditer(pat, texto, re.I):
                v.append({"gate": "G8-formato", "sev": "P0", "trecho": _ctx(texto, m.start(), m.end(), 50),
                          "problema": msg})
        if not re.search(r"EXCELENT[ÍI]SSIM|EGR[ÉE]GI|COLENDA?|MEMORIAL", texto[:3000], re.I):
            v.append({"gate": "G8-formato", "sev": "P1", "trecho": "(início do documento)",
                      "problema": "peça sem endereçamento/abertura formal"})
        if not re.search(r"OAB", texto[-3500:]):
            v.append({"gate": "G8-formato", "sev": "P1", "trecho": "(fim do documento)",
                      "problema": "peça sem bloco de assinatura com OAB"})
    return v


def gate_g9(texto, tipo):
    v = []
    if tipo != "peca":
        return v
    for pat, msg in PROVENIENCIA_OPERACIONAL:
        for m in re.finditer(pat, texto, re.I):
            v.append({"gate": "G9-proveniencia", "sev": "P0",
                      "trecho": _ctx(texto, m.start(), m.end(), 55), "problema": msg})
    return v


def gate_s5_sobreabstracao(texto):
    """S5: Afirmação de jurisprudência/entendimento consolidado sem citação nominal.

    Taxonomia de falha de citação (modo 6): "afirma autoridade que não se pode
    conferir". Detecta padrões genéricos de jurisprudência (ex: "jurisprudência
    pacífica", "as Cortes superiores firmaram") que não possuem citação nominal
    conferível (REsp/AREsp/RE/ARE/HC/Súmula com número) na mesma frase ou
    parágrafo imediatamente seguinte.

    Critério de proximidade: mesma frase ou até 2 frases de distância.
    Calibrado contra baseline aprovado para evitar falso positivo (ex: síntese
    executiva que remete a seção posterior).
    """
    v = []

    # Padrões de afirmação genérica de jurisprudência consolidada.
    # Sensibilidade: prefiro recall alto (detect mais casos) porque o falso positivo
    # é aceitável como P1 (aviso) — precision vem da validação de proximidade.
    AFIRMACOES_GENERICAS = [
        (r"jurisprud[êe]ncia\s+(?:pacífica|s[ó0]lida|uníssona|firm[ea]|consolidada|pacíf(?:ic)?[ao])", "jurisprudência sem número"),
        (r"entendimento\s+(?:consolidado|pacífico|uníssono|firm[ea]|s[ó0]lido|consagrado|assent[ea]do)", "entendimento sem número"),
        (r"(?:é|foi)\s+(?:entendimento\s+)?pacífico\b", "afirmação vaga de consenso jurídico"),
        (r"as\s+(?:Cortes\s+)?(?:Cortes\s+)?[Ss]uperiores\s+firmaram", "Cortes superiores genérico"),
        (r"(?:este\s+)?Tribunal\s+(?:tem\s+)?entendimento\s+(?:consolidado|pacífico|assentado|firme)", "Tribunal genérico sem número"),
        (r"é\s+(?:assent|consagr)[aã]do\s+(?:que|na\s+jurisprud)", "assento genérico"),
        (r"reconhec[ie]do\s+(?:pela|nas)\s+Cortes\s+(?:Superiores|de\s+Justi[çc]a)", "Cortes genérico"),
    ]

    # Padrões de citação nominal conferível. Uma citação válida "mata" a suspeita
    # de falta de lastro porque torna a autoridade verificável.
    CITACAO_NOMINAL = re.compile(
        r"(?:"
        r"(?:REsp|RESP)\s*\.?\s*n?[ºo°]?\.?\s*\d+[/\-]?\d*"
        r"|(?:AREsp|ARESP)\s*\.?\s*n?[ºo°]?\.?\s*\d+[/\-]?\d*"
        r"|(?:RE|are)\s*\.?\s*n?[ºo°]?\.?\s*\d+[/\-]?\d*"
        r"|(?:ARE)\s*\.?\s*n?[ºo°]?\.?\s*\d+[/\-]?\d*"
        r"|(?:HC|RHC)\s*\.?\s*n?[ºo°]?\.?\s*\d+[/\-]?\d*"
        r"|[Ss]úmula\s*(?:Vinculante)?\s*n?[ºo°]?\s*\d+"
        r"|[Tt]ema\s*n?[ºo°]?\s*\d+(?:/STJ)?"
        r")",
        re.I
    )

    # Dividir em parágrafos para análise de proximidade
    paragrafos = re.split(r'\n\s*\n', texto)
    deslocamento_paragrafo = 0

    for para_idx, paragrafo in enumerate(paragrafos):
        inicio_paragrafo = texto.find(paragrafo, deslocamento_paragrafo)
        if inicio_paragrafo < 0:  # pragma: no cover - proteção contra texto mutável
            inicio_paragrafo = deslocamento_paragrafo
        deslocamento_paragrafo = inicio_paragrafo + len(paragrafo)
        for pat, msg_generica in AFIRMACOES_GENERICAS:
            for m in re.finditer(pat, paragrafo, re.I):
                # Procurar citação nominal em três zonas:
                # 1. Na mesma frase (antes do ponto seguinte)
                # 2. Na próxima frase do mesmo parágrafo
                # 3. No parágrafo seguinte (remissão para depois)

                frase_inicio = paragrafo[:m.start()].rfind('.') + 1
                frase_fim = paragrafo.find('.', m.end())
                if frase_fim == -1:
                    frase_fim = len(paragrafo)

                # Mesma frase e frase seguinte no parágrafo
                zona_proximo = paragrafo[m.start():frase_fim]
                if frase_fim < len(paragrafo):
                    proxima_frase_fim = paragrafo.find('.', frase_fim + 1)
                    if proxima_frase_fim == -1:
                        proxima_frase_fim = len(paragrafo)
                    zona_proximo = paragrafo[m.start():proxima_frase_fim]

                # Parágrafo seguinte (para remissão)
                zona_seguinte = ""
                if para_idx + 1 < len(paragrafos):
                    zona_seguinte = paragrafos[para_idx + 1][:500]  # Primeiras 500 chars

                # Validar presença de citação nominal em qualquer zona
                has_citation = (
                    CITACAO_NOMINAL.search(zona_proximo)
                    or CITACAO_NOMINAL.search(zona_seguinte)
                )

                if not has_citation:
                    v.append({
                        "gate": "S5-sobreabstracao",
                        "sev": "P1",
                        "trecho": _ctx(
                            texto,
                            inicio_paragrafo + m.start(),
                            inicio_paragrafo + m.end(),
                            50,
                        ),
                        "problema": (
                            f"afirmação genérica de jurisprudência '{m.group(0).strip()}' "
                            f"sem citação nominal verificável (REsp/AREsp/RE/Súmula) na vizinhança — "
                            f"{msg_generica}"
                        ),
                    })

    return v


def _carregar_contexto_lastro(case_dir=None, ledger=None, base_dir=None):
    """Descobre contexto documental sem tornar o verificador dependente de um caso.

    A descoberta é somente leitura. Quando a rota fornece ``case_dir``, o
    ledger canônico é procurado nos artefatos F3 e na produção; quando não há
    contexto, o verificador continua cobrindo os gates lexicais v1.
    """
    from pathlib import Path

    caso = Path(case_dir) if case_dir else None
    if ledger is None and caso and caso.is_dir():
        candidatos = [
            caso / "producao" / "fact_ledger.json",
            caso / "n3_artifacts" / "F3_FONTES_REGIMENTO_LEIS" / "fact_ledger.json",
        ]
        candidatos += sorted(caso.glob("n3_artifacts/F3_FONTES_REGIMENTO_LEIS/fact_ledger*.json"))
        for candidato in candidatos:
            if candidato.is_file():
                try:
                    ledger = json.loads(candidato.read_text(encoding="utf-8"))
                    if not isinstance(ledger, dict):
                        # Um ledger canônico fora do schema não pode ser
                        # substituído por snapshot histórico. A queda para um
                        # snapshot fazia a rota visual parecer aprovada mesmo
                        # quando o insumo vigente estava quebrado.
                        return {}, base_dir
                    break
                except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                    # ``fact_ledger.json`` é a fonte canônica. Se ele existe e
                    # não abre, devolvemos ledger vazio para que L9--L13
                    # emitam P0; nunca percorremos snapshots como fallback
                    # silencioso. A ausência do arquivo continua permitindo a
                    # descoberta do próximo candidato declarado.
                    if candidato.name == "fact_ledger.json":
                        return {}, base_dir
                    continue
    if base_dir is None and caso:
        try:
            estado = json.loads((caso / "FORJA_STATE.json").read_text(encoding="utf-8"))
            base_dir = (estado.get("inputs") or {}).get("caseFolder") or str(caso)
        except (OSError, json.JSONDecodeError):
            base_dir = str(caso)
    return ledger, base_dir


def verificar(texto, tipo="peca", *, ledger=None, base_dir=None, case_dir=None,
              exigir_economico=None):
    todas = []
    for g in (gate_g1, gate_g3, gate_g4, gate_g5, gate_g7):
        todas.extend(g(texto))
    todas.extend(gate_g2(texto, tipo))
    todas.extend(gate_g6(texto, tipo))
    todas.extend(gate_g8(texto, tipo))
    todas.extend(gate_g9(texto, tipo))
    todas.extend(gate_g11(texto))
    todas.extend(gate_s5_sobreabstracao(texto))
    # Gate especializado e versionado. Import local evita acoplamento circular e
    # mantém o verificador utilizável como script isolado.
    from forja_estilo_humano import analisar as analisar_estilo_humano
    todas.extend(analisar_estilo_humano(texto, tipo))
    # Gates de identidade processual S2 e S4 (05/08/2026).
    #
    # Anteriormente não havia gate aqui porque não havia FATO registrado. As mutações
    # S2 (troca de parte) e S4 (troca de pedido) são simétricas e globais — depois
    # delas o texto fica internamente coerente. O gate que tentou operar só com o
    # texto (comparação de frequência relativa, análise de gênero, etc.) falhou em
    # 100% das 27 mutações porque a coerência interna é tudo o que existe sem
    # FATO EXTERNO (diagnóstico 2026-08-05).
    #
    # Este gate usa F2_IDENTIDADE_PROCESSUAL.json, um artefato por caso que declara
    # quem é a cliente, qual seu papel e qual a direção do pedido dela. O lastro
    # precisa ser EXTERNO (comando do caso, decisão impugnada) — NUNCA derivado da
    # redação, senão seria mutado junto. A validação recusa sourceKey cuja role
    # indique minuta/produção/draft.
    #
    # Gate executa SOMENTE se existe declaração válida. Caso sem declaração = sem
    # veredito (indeterminado), nunca P0 automático.
    if case_dir:
        from forja_identidade_processual import (
            carregar_declaracao, gate_s2_pareamento_nome_papel, gate_s4_presenca_direcao_pedido,
            validar_declaracao_completa, validar_lastro_de_fonte_externa
        )
        from pathlib import Path
        import json as json_m

        # Só erros PREVISTOS de leitura são tolerados, e cada um por seu nome.
        # A primeira versão deste bloco engolia tudo com `except Exception: pass`
        # — o mesmo fallback silencioso que fez o gate anterior de coerência
        # processual ser revertido. Com ele, um defeito no gate se disfarça de
        # "caso sem declaração", e ninguém descobre que a proteção morreu.
        case_path = Path(case_dir)
        try:
            decl = carregar_declaracao(case_path)
        except (OSError, ValueError, json_m.JSONDecodeError):
            decl = None

        if decl and validar_declaracao_completa(decl).valida:
            manifest_path = case_path / "FORJA_CASE_MANIFEST.json"
            manifest = None
            if manifest_path.is_file():
                try:
                    manifest = json_m.loads(manifest_path.read_text(encoding="utf-8"))
                except (OSError, json_m.JSONDecodeError):
                    manifest = None
            # Sem manifesto ou com lastro inválido o veredito é INDETERMINADO:
            # os gates não rodam, e também não se emite P0. Caso ainda não
            # declarado não pode virar bloqueio — são 52 casos sem declaração.
            if manifest is not None and validar_lastro_de_fonte_externa(
                    decl, manifest, base_dir=case_path).valida:
                todas.extend(gate_s2_pareamento_nome_papel(texto, decl))
                todas.extend(gate_s4_presenca_direcao_pedido(texto, decl))
        # S6 e S7 dependem só dos blocos `atos` e `objeto` da declaração, e não
        # do lastro de nome/papel: um caso pode ter a lista de atos conferida
        # sem ter a autuação transcrita. Rodam fora do bloco acima de propósito,
        # e continuam sem opinar quando os blocos não existem.
        if decl:
            from forja_identidade_processual import (
                gate_s6_identidade_do_ato, gate_s7_objeto_devolvido)
            todas.extend(gate_s6_identidade_do_ato(texto, decl))
            todas.extend(gate_s7_objeto_devolvido(texto, decl))
    # Blindagem contra lastro aparente (caso CASO-23, 26/07/2026). Os gates
    # lexicais entram em toda rota; L1/L2/L7/L8 e L9--L13 só são calculados
    # quando a rota fornece o ledger/contexto documental real.
    from forja_lastro import analisar_texto as analisar_lastro, validar_gates_economicos
    todas.extend(analisar_lastro(texto, tipo))
    ledger, base_dir = _carregar_contexto_lastro(case_dir, ledger, base_dir)
    if ledger is not None or case_dir is not None or exigir_economico is not None:
        todas.extend(validar_gates_economicos(
            texto, ledger=ledger, base_dir=base_dir, exigir=exigir_economico
        ))
    return todas


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(sys.argv) < 2:
        print("uso: python forja_verificador.py <arquivo> [--tipo peca|estudo|email]")
        sys.exit(2)
    arq = sys.argv[1]
    tipo = sys.argv[sys.argv.index("--tipo") + 1] if "--tipo" in sys.argv else "peca"
    case_dir = sys.argv[sys.argv.index("--case-dir") + 1] if "--case-dir" in sys.argv else None
    texto = open(arq, encoding="utf-8").read()
    viol = verificar(texto, tipo, case_dir=case_dir)
    print(json.dumps({"arquivo": arq, "tipo": tipo, "total": len(viol),
                      "p0": sum(1 for x in viol if x["sev"] == "P0"),
                      "violacoes": viol}, ensure_ascii=False, indent=2))
    tem_p0 = any(x["sev"] == "P0" for x in viol)
    if tem_p0 and case_dir:
        # M1.1 (plano 19): com --case-dir, P0 notifica o painel — fail-open.
        try:
            from forja_alertas import notificar_p0
            for gate in sorted({x["gate"] for x in viol if x["sev"] == "P0"}):
                motivos = [x["problema"] for x in viol if x["gate"] == gate][:3]
                notificar_p0(case_dir, gate=gate, motivo="; ".join(motivos),
                             origem="forja_verificador")
        except Exception:
            pass
    sys.exit(1 if tem_p0 else 0)
