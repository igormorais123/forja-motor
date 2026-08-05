# -*- coding: utf-8 -*-
"""
forja_lastro.py — Blindagem contra alucinação por lastro aparente.

Motivo (caso CASO-23, 26/07/2026). Três camadas de revisão — red team interno
de doze perguntas, gate F7 e dois revisores externos de famílias distintas —
devolveram zero P0 sobre uma minuta que continha quatro P0. Todas examinaram o
TEXTO. Os erros estavam na FONTE, e a fonte não fora aberta.

A causa comum de todos eles não foi invenção do nada. Foi **lastro aparente**:
afirmação marcada como confirmada em documento, com localizador plausível, cujo
localizador ninguém abriu. `fact_ledger` F012 dizia "confirmed_document" com
apoio em "E252-ANEXO-AI-p20-31"; a página existia, o documento existia, e o
documento dizia o contrário.

Daí o eixo destes gates: **citar o localizador não é ter lido o localizador.**
A única prova barata de leitura é a transcrição verbatim. Um modelo que precisa
colar o trecho é obrigado a abrir a fonte; um modelo que só precisa citar a
página pode inventá-la com aparência perfeita.

Os treze gates funcionais L1–L13 abaixo têm cada um uma falha real desta
execução como âncora. Guardas L0 e de conferência operacional impedem que
ledger vazio, vocabulário ausente ou insumo inválido pareçam aprovação. Não há
gate especulativo aqui — a regra da casa é que métrica nova precisa de falha
observada (ver `planejamento/22_PRD_AUTORESEARCH_FORJA.md`).

| gate | falha real que o originou |
|------|---------------------------|
| L1 | F012 marcado `confirmed_document` sem transcrição; a fonte dizia o oposto |
| L2 | transcrição que não existe na fonte apontada |
| L3 | "confirmada em todas as instâncias" sobre REsp **não conhecido** |
| L4 | "93% dessa distância" — denominador trocado no meio da frase |
| L5 | "§ 16: mesmas partes e a mesma liquidação" — eram liquidações distintas |
| L6 | "normas de 2002, 2016 e 2018" — a de 2018 não existia |
| L7 | recomendação de base de cálculo contra critério fixado nos autos |
| L8 | objeção externa acatada sem reabrir a fonte, contra minuta correta |

Uso como biblioteca:
    from forja_lastro import analisar_texto, validar_lastro_fatos, validar_decisoes_revisao

Uso como script:
    python forja_lastro.py <arquivo.md> [--ledger fact_ledger.json] [--base-dir DIR]
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import sys
import unicodedata
from pathlib import Path

VERSAO = "FORJA-LASTRO-v2"

# A incidência econômica é deliberadamente estreita. A calibração persistida em
# ``CALIBRACAO_MONETARIA.json`` demonstrou que números com separador de milhar
# capturam RE, Lei e Decreto em escala. Os gates L9--L13 só entram quando existe
# marcador explícito de moeda, e não quando há apenas um número grande.
# O espaço opcional entre "R" e "$" não existe em português correto, e não há
# nenhuma ocorrência dele no acervo — conferido em 04/08/2026 sobre todos os .md.
# Ele entra porque este marcador decide se os gates L9-L13 rodam, e errar para o
# lado de auditar a mais custa uma conferência, enquanto errar para o lado de não
# detectar deixa cifra sem lastro sair na peça. OCR de decisão digitalizada e
# colagem de PDF produzem essa forma.
_MOEDA_EXPLICITA = re.compile(
    r"(?:R\s?\$|\breais\b|\bmilh(?:õ|o)es\s+de\s+reais\b|"
    r"\bbilh(?:õ|o)es\s+de\s+reais\b)", re.I)
_CIFRA_MONETARIA = re.compile(
    r"R\s?\$\s*[+-]?\d[\d .]*(?:,\d{1,2})?|"
    r"[+-]?\d[\d .]*(?:,\d{1,2})?\s+(?:milh(?:õ|o)es|bilh(?:õ|o)es)\s+de\s+reais",
    re.I)
_DATA_BASE = re.compile(
    r"(?:data[- ]base|base\s+de\s+c[aá]lculo|atualizad[oa]\s+at[eé])"
    r"\s*[:：-]?\s*(?P<valor>"
    r"\d{4}[-/]\d{1,2}(?:[-/]\d{1,2})?|"
    r"\d{1,2}/\d{1,2}/\d{4}|"
    r"\d{1,2}/\d{4}|"
    r"(?:jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)[a-zç]*\s*(?:de\s*|/)?\d{4}"
    r")",
    re.I,
)
_DATA_SOLTA = re.compile(
    r"(?P<valor>\d{4}[-/]\d{1,2}(?:[-/]\d{1,2})?|\d{1,2}/\d{4}|"
    r"(?:jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)[a-zç]*\s*(?:de\s*|/)?\d{4})",
    re.I,
)
_MESES = {
    "jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
    "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12,
}
_ECONOMICO_NO_NOME = re.compile(
    r"(?:laudo|parecer.{0,24}(?:cont[aá]bil|econ[oô]mic)|mem[oó]ria.{0,20}c[aá]lculo|"
    r"per[ií]cia|resultado[_ -]?calculo|resultado[_ -]?c[aá]lculo|"
    r"homologa[cç][aã]o|base.{0,16}econ[oô]mic|c[aá]lculo)",
    re.I,
)
_ROTULO_DERIVADO = re.compile(
    r"(?:derivad[oa]|c[aá]lculo\s+(?:derivado|recalculado)|faixa\s+(?:calculada|derivada)|"
    r"corredor\s+(?:calculado|derivado)|base\s*[×x*]|base\s+mais|base\s+menos)", re.I)
# Sinal de que o valor pertence a outro: laudo, decisão, contrato, parte
# adversária. Usado para separar a citação real da isenção que veio só da
# tipografia — um `>` ou um par de aspas ao redor do próprio cálculo.
_ORIGEM_ALHEIA = re.compile(
    r"(?:laudo|per[íi]cia|senten[çc]a|ac[oó]rd[aã]o|decis[ãa]o|condena[çc][ãa]o|"
    r"contrato|ap[óo]lice|parte\s+advers[aá]ria|r[ée]u|autor|uni[ãa]o|"
    r"evento\s+\d+|Doc\.\s*\d+|fl(?:s)?\.\s*\d+)", re.I)
# A proveniência é deliberadamente explícita. Tipografia é apenas uma pista:
# `>` e aspas podem introduzir uma transcrição, mas também podem ser usadas
# para mascarar um cálculo próprio. Só as duas classes abaixo são isenções
# aceitas pelo L11; a terceira permanece em conferência de âncora.
_PROVENIENCIA_FONTE = "fonte_externa_declarada"
_PROVENIENCIA_NORMATIVA = "normativa"
_PROVENIENCIA_TIPOGRAFICA = "tipografia_sem_origem"
_PROVENIENCIA_CALCULADA = "calculado_ou_desconhecido"
_ROTULO_JURIDICO_LOCAL = re.compile(
    r"(?:lei|decreto|s[úu]mula|tema|REsp?|AREsp|AgInt|EDcl|processo|autos|"
    r"art(?:igo)?|inciso|par[aá]grafo|§)\s*(?:n[ºo°]?\s*)?[^\n]{0,24}", re.I)

# Status do ledger que afirmam lastro documental. Só estes exigem transcrição:
# `legal_inference`, `strategic_hypothesis` e `not_verified` são honestos sobre
# o que são e não podem ser tratados como se afirmassem fato provado.
#
# Medido em 04/08/2026 no ledger real da CASO-04: dos 11 fatos, **zero** eram
# alcançados por L1/L2, porque o caso escreve `documented_fact` e
# `official_current_source` enquanto o gate só conhecia `confirmed_document` e
# `confirmed_official_source` — sinônimos separados por uma palavra. O gate
# rodava, não achava nada para conferir e devolvia `pass`. Gate computado sobre
# conjunto vazio não é gate; é a mesma falsa cobertura do gate declarado, num
# disfarce melhor.
STATUS_COM_LASTRO = {
    "confirmed_document",
    "confirmed_official_source",
    "documented_fact",
    "official_current_source",
    "PROVADO",
    "CONFLITANTE",
}

# Status que legitimamente NÃO exigem transcrição: dizem o que são. Existem
# nomeados aqui — e não por omissão — para que a lista abaixo consiga separar
# "isento por natureza" de "vocabulário que ninguém previu".
STATUS_SEM_LASTRO = {
    "legal_inference",
    "strategic_hypothesis",
    "documented_strategy",
    "not_verified",
    "blocked",
    "pending",
    "INFERENCIA",
    "NAO_VERIFICADO",
}

# Palavras que declaram estabilidade processual. Nenhuma delas é proibida; todas
# exigem que o próprio texto mostre a razão. O perigo não é usá-las, é usá-las
# como resumo apressado de uma cadeia recursal que diz outra coisa.
SUPERLATIVO_PROCESSUAL = [
    (r"em\s+todas\s+as\s+inst[âa]ncias", "afirma confirmação em todas as instâncias"),
    (r"(?:em|nas)\s+(?:duas|tr[êe]s|quatro)\s+inst[âa]ncias", "afirma decisão em N instâncias"),
    (r"quest[ãa]o\s+encerrada", "declara questão encerrada"),
    (r"em\s+definitivo\b", "declara definitividade"),
    (r"defini[ct]ivamente\s+(?:decidid|julgad|resolvid)", "declara definitividade"),
    (r"\bincontrovers[oa]\b", "declara incontrovérsia"),
    (r"j[áa]\s+pacificad[oa]\s+(?:pel|em\s+definitivo)", "declara pacificação"),
]

# O par que produziu o erro real. Não conhecer recurso não é confirmar mérito:
# o tribunal superior não substitui o acórdão recorrido. Coocorrência dos dois
# campos semânticos no mesmo documento é bloqueador, porque o texto está
# afirmando, em algum lugar, que um não conhecimento confirmou alguma coisa.
_NAO_CONHECIMENTO = re.compile(
    r"n[ãa]o\s+(?:foi\s+)?conhecid|n[ãa]o\s+conhec(?:eu|imento)|"
    r"S[úu]mula\s+(?:7|211|282|283|284|356)\b",
    re.I)
_CONFIRMACAO = re.compile(
    r"confirmad[oa]\s+(?:pel|em\s+todas)|confirmou\s+o\s+m[ée]rito|"
    r"mantid[oa]\s+pelo\s+(?:STJ|STF|Superior\s+Tribunal|Supremo)|"
    r"em\s+todas\s+as\s+inst[âa]ncias|(?:em|nas)\s+tr[êe]s\s+inst[âa]ncias",
    re.I)

# Percentual cujo denominador é um substantivo vago. "93% do principal do Anexo I"
# é conferível; "93% dessa distância" muda a base no meio da frase e ninguém nota.
_PERCENTUAL_VAGO = re.compile(
    r"\d{1,3}(?:[.,]\d+)?\s*%\s+(?:d[aeo]s?\s+)?"
    r"(?:dess[ae]|dest[ae]|daquel[ae]|do|da)?\s*"
    r"(?:dist[âa]ncia|diferen[çc]a|discrep[âa]ncia|gap|total(?!\s+d)|montante(?!\s+d)|valor(?!\s+d))",
    re.I)

# Afirmação de identidade entre atos ou processos. Foi o P0 mais grave do caso:
# identidade é conclusão jurídica sobre dois documentos, nunca inferência de
# semelhança. Exige que os dois identificadores estejam à vista.
_IDENTIDADE_PROCESSUAL = [
    (r"mesma\s+liquida[çc][ãa]o", "afirma identidade de liquidação"),
    (r"mesma\s+execu[çc][ãa]o", "afirma identidade de execução"),
    (r"mesmo\s+t[íi]tulo\s+executivo", "afirma identidade de título executivo"),
    (r"mesmos\s+autos", "afirma identidade de autos"),
    (r"id[êe]ntic[oa]s?\s+(?:objeto|pedido|causa\s+de\s+pedir)", "afirma identidade de objeto"),
]
_NUMERO_CNJ = re.compile(r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b|\b\d{2}\.\d{2}\.\d{5}-\d\b")

# Negar identidade é o comportamento desejado — é a correção que este gate quer
# produzir. Travar a negação ensinaria a contornar o gate em vez de conferir.
_NEGACAO_EXPLICITA = re.compile(
    r"n[ãa]o\s+(?:se\s+trata|[ée]\b|s[ãa]o\b|envolve|constitui|h[áa]\b|que\b)|"
    r"\btampouco\b|distint[oa]s?\s+d|diversa?\s+d|e\s+n[ãa]o\b",
    re.I)
# "mas não a mesma liquidação": o "não" fica colado, com artigo no meio.
_NEGACAO_COLADA = re.compile(r"n[ãa]o\s+(?:[ao]s?\s+)?$", re.I)
# Janela curta de propósito: a negação precisa estar junto da afirmação, não em
# qualquer ponto do parágrafo, senão um "não" distante limparia o gate.
_JANELA_NEGACAO = 45


def _negado(antes: str) -> bool:
    """Verdadeiro quando o trecho imediatamente anterior nega a afirmação.

    Travar a negação seria o pior resultado possível para estes gates: ensinaria
    a contornar em vez de conferir. E a frase correta produzida neste caso —
    "envolve as mesmas partes, mas não a mesma liquidação" — é justamente a
    redação que o gate existe para provocar.
    """
    return bool(_NEGACAO_COLADA.search(antes) or _NEGACAO_EXPLICITA.search(antes))

# Enumeração de normas por ano, sem nomear a norma. Foi assim que "2018" entrou
# na minuta sem que norma alguma de 2018 existisse no laudo criticado.
_NORMAS_POR_ANO = re.compile(
    r"normas?\s+(?:de|dos?\s+anos?\s+de)\s+"
    r"((?:1[89]|20)\d{2}(?:\s*(?:,|e)\s*(?:1[89]|20)\d{2})+)",
    re.I)
_NORMA_NOMEADA = re.compile(
    r"(?:Lei(?:\s+Complementar)?|Decreto(?:-Lei)?|Instru[çc][ãa]o\s+Normativa|Portaria|"
    r"Resolu[çc][ãa]o|Medida\s+Provis[óo]ria|Emenda)\s*"
    r"(?:n?[ºo°.]*\s*)?[\d.]+\s*/\s*((?:1[89]|20)\d{2})",
    re.I)


def _norm(texto: str) -> str:
    """Normaliza para comparação de transcrição: sem acento, sem hífen de quebra,
    espaço colapsado, minúsculas. PDF de autos digitalizados quebra palavra no
    fim de linha e troca aspas; comparar cru geraria falso negativo em massa."""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = texto.replace("-\n", "").replace("­", "")
    texto = re.sub(r"[“”„‟\"']", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.lower().strip()


def _ctx(texto: str, ini: int, fim: int, alcance: int = 60) -> str:
    a = max(0, ini - alcance)
    b = min(len(texto), fim + alcance)
    return re.sub(r"\s+", " ", texto[a:b]).strip()


# ---------------------------------------------------------------------------
# L1 e L2 — lastro do ledger
# ---------------------------------------------------------------------------

# Extensões que o L2 sabe ler como texto. A lista é de inclusão deliberada: o
# que não estiver nela é tratado como não conferível e vira P1 honesto, nunca
# acusação de transcrição inventada.
_EXT_TEXTO = {".md", ".txt", ".json", ".csv", ".yaml", ".yml", ".html", ".xml", ".py", ".log", ".tex"}

# Teto de leitura. Acima disto o custo de conferir supera o benefício e o risco
# de estourar memória é real — o laudo prevalente da CASO-04 tem 2,14 GB.
_LIMITE_LEITURA_BYTES = 8 * 1024 * 1024


def _conferivel_como_texto(alvo: Path) -> bool:
    if alvo.suffix.lower() not in _EXT_TEXTO:
        return False
    try:
        return alvo.stat().st_size <= _LIMITE_LEITURA_BYTES
    except OSError:
        return False


def validar_lastro_fatos(ledger: dict, *, base_dir: Path | str | None = None,
                         exigir_transcricao: bool = True) -> list[dict]:
    """L1: fato que afirma lastro documental precisa de localizador E transcrição.
    L2: havendo transcrição e fonte alcançável, a transcrição precisa existir lá.

    `exigir_transcricao=False` rebaixa L1 a P1. Serve para ledger legado, que não
    pode ser reprovado retroativamente — mas o padrão é exigir, porque o custo de
    colar um trecho é baixo e o custo de não colar já foi medido.
    """
    achados: list[dict] = []
    base = Path(base_dir) if base_dir else None

    # Ledger vazio é o caso-limite do MC-15: percorrer zero fatos produz zero
    # achados, e zero achados é lido rio abaixo como aprovação. Um ledger sem
    # fatos não é um ledger limpo — é um ledger que não foi escrito.
    fatos = (ledger or {}).get("facts")
    if fatos is None:
        for alternativa in ("fatos", "claims", "proposicoes"):
            if (ledger or {}).get(alternativa) is not None:
                achados.append({
                    "gate": "L0-ledger-vocabulario", "sev": "P0", "factId": "-",
                    "problema": (f"ledger usa a chave '{alternativa}' e não 'facts' — "
                                 "nenhum fato foi examinado"),
                    "acao": "renomeie a chave para 'facts'", "versao": VERSAO})
                return achados
    if not isinstance(fatos, list) or not fatos:
        achados.append({
            "gate": "L0-ledger-vazio", "sev": "P0", "factId": "-",
            "problema": ("ledger sem lista de fatos — nenhum fato foi examinado; "
                         "a ausência de achados aqui não é aprovação"),
            "acao": "preencha 'facts' com as proposições decisivas da peça",
            "versao": VERSAO})
        return achados

    for fato in fatos:
        if not isinstance(fato, dict):
            achados.append({"gate": "L0-ledger-vazio", "sev": "P0", "factId": "-",
                            "problema": "entrada de 'facts' não é um objeto — fato não examinado",
                            "versao": VERSAO})
            continue
        fid = str(fato.get("id") or fato.get("factId") or "?")
        status = str(fato.get("status") or fato.get("classification") or "").strip()
        if not status:
            # Status ausente saía pelo mesmo `continue` do vocabulário isento,
            # sem deixar rastro: bastava omitir o campo para o fato escapar de
            # L1/L2. Omissão é desconhecimento, não isenção.
            achados.append({
                "gate": "L1-status-ausente", "sev": "P1", "factId": fid,
                "problema": f"{fid}: sem status — o fato não foi auditado por L1/L2",
                "acao": "declare o status do fato", "versao": VERSAO})
            continue
        if status not in STATUS_COM_LASTRO:
            # Vocabulário desconhecido não pode significar silêncio. Um status
            # que o gate não conhece é indistinguível, na saída, de um fato
            # auditado e aprovado — foi assim que o ledger da CASO-04 passou
            # com 0 de 11 fatos conferidos. Isento por natureza fica quieto;
            # desconhecido aparece.
            if status and status not in STATUS_SEM_LASTRO:
                achados.append({
                    "gate": "L1-status-desconhecido", "sev": "P1", "factId": fid,
                    "problema": (f"{fid}: status '{status}' não é conhecido pelo gate — "
                                 "o fato não foi auditado por L1/L2"),
                    "acao": ("declare o status em STATUS_COM_LASTRO ou STATUS_SEM_LASTRO; "
                             "enquanto não estiver, este fato passa sem conferência"),
                    "versao": VERSAO})
            continue

        # Localizador é o que permite ir ao documento e conferir. O ledger da
        # CASO-04 escreve `locator` + `quoteSource` + `sha256`, que é lastro
        # mais forte que um `support` genérico — e mesmo assim os 6 fatos bem
        # formados reprovavam em P0 por não usarem a palavra esperada. Aceitar
        # só `support` transformava o gate em auditor que reprova o acerto,
        # que o § 4 do protocolo manda desligar.
        apoio = (fato.get("support") or fato.get("sources") or fato.get("sourceIds")
                 or fato.get("locator") or fato.get("quoteSource") or [])
        if not apoio:
            achados.append({"gate": "L1-lastro", "sev": "P0", "factId": fid,
                            "problema": f"{fid}: status '{status}' sem localizador de apoio"})
            continue

        trecho = (fato.get("quote") or fato.get("trechoSuporte") or "").strip()
        if not trecho:
            # Pendência declarada é honestidade, não defeito silencioso: o autor
            # sabe e diz que não abriu a fonte. Continua impedindo promoção, mas
            # é P1, porque a alternativa — inventar a transcrição para o gate
            # ficar verde — é exatamente o comportamento que estes gates existem
            # para desencorajar.
            declarada = bool(fato.get("groundingPending"))
            achados.append({
                "gate": "L1-lastro-pendente" if declarada else "L1-lastro",
                "sev": "P1" if declarada or not exigir_transcricao else "P0",
                "factId": fid,
                "problema": (f"{fid}: pendência de lastro declarada — fonte não reaberta"
                             if declarada else
                             f"{fid}: status '{status}' com localizador mas sem transcrição "
                             "verbatim — citar a página não prova tê-la lido"),
                "acao": "abra a fonte e cole o trecho no campo 'quote'",
                "versao": VERSAO})
            continue

        if len(_norm(trecho)) < 25:
            achados.append({"gate": "L1-lastro", "sev": "P1", "factId": fid,
                            "problema": f"{fid}: transcrição curta demais para provar leitura",
                            "versao": VERSAO})

        # L2 — a transcrição existe mesmo na fonte apontada?
        caminho = fato.get("quoteSource") or fato.get("arquivoFonte")
        if base and caminho:
            alvo = base / caminho
            if not alvo.exists():
                # Distinguir arquivo sumido de campo que nunca foi caminho. Boa
                # parte dos ledgers usa `quoteSource` como nome legível da fonte
                # ("Portaria Normativa PGU/AGU nº 29, de 13/11/2025"), e dizer
                # "não localizada" sobre isso sugere um arquivo perdido que
                # nunca existiu, mandando o revisor procurar o que não há.
                parece_caminho = bool(Path(str(caminho)).suffix) and len(str(caminho)) < 160
                achados.append({
                    "gate": "L2-transcricao" if parece_caminho else "L2-transcricao-manual",
                    "sev": "P1", "factId": fid,
                    "problema": (f"{fid}: fonte '{caminho}' não localizada para conferir"
                                 if parece_caminho else
                                 f"{fid}: fonte '{str(caminho)[:70]}' está nomeada, não endereçada — "
                                 "a transcrição depende de conferência humana"),
                    "acao": ("confirme o caminho do arquivo na pasta do caso" if parece_caminho else
                             "aponte o arquivo arquivado da fonte ou registre quem conferiu"),
                    "versao": VERSAO})
            elif not _conferivel_como_texto(alvo):
                # Fonte binária (PDF digitalizado, DOCX, imagem) ou grande
                # demais. Antes desta guarda o L2 lia o arquivo como UTF-8 e,
                # não achando o trecho no meio do binário, acusava o autor de
                # ter reconstruído a citação de memória — a acusação mais grave
                # que este módulo faz, contra quem transcreveu corretamente de
                # um PDF. O laudo da CASO-04 tem 2,14 GB: além do falso P0, a
                # leitura carregaria o arquivo inteiro na memória.
                achados.append({
                    "gate": "L2-transcricao-manual", "sev": "P1", "factId": fid,
                    "problema": (f"{fid}: fonte '{caminho}' não é conferível automaticamente "
                                 "(binária ou muito grande) — a transcrição depende de conferência humana"),
                    "acao": "confira o trecho na fonte e registre quem conferiu",
                    "versao": VERSAO})
            else:
                try:
                    conteudo = alvo.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    conteudo = ""
                if conteudo and _norm(trecho) not in _norm(conteudo):
                    achados.append({
                        "gate": "L2-transcricao", "sev": "P0", "factId": fid,
                        "problema": (f"{fid}: transcrição não encontrada em '{caminho}' — "
                                     "o trecho pode ter sido reconstruído de memória"),
                        "versao": VERSAO})
    return achados


# ---------------------------------------------------------------------------
# L7 — critério vigente declarado
# ---------------------------------------------------------------------------

def exigir_criterio_vigente(ledger: dict) -> list[dict]:
    """L7: em fase de liquidação ou cumprimento, o ledger precisa declarar qual
    decisão fixa HOJE o critério em disputa, com transcrição.

    Âncora: a minuta recomendou base de cálculo e método sem que existisse, em
    lugar algum do estado do caso, um registro do que a decisão vigente havia
    determinado. Duas decisões dos autos já tinham resolvido a questão contra a
    tese sustentada, e isso só apareceu ao abrir os eventos por acaso.
    """
    for fato in ledger.get("facts") or []:
        papel = str(fato.get("role") or fato.get("papel") or "")
        if papel == "criterio_vigente":
            if not (fato.get("quote") or fato.get("trechoSuporte")):
                return [{"gate": "L7-criterio-vigente", "sev": "P0",
                         "problema": "critério vigente declarado sem transcrição da decisão",
                         "versao": VERSAO}]
            return []
    return [{"gate": "L7-criterio-vigente", "sev": "P0",
             "problema": ("nenhum fato marcado com role='criterio_vigente': o estado do caso "
                          "não diz qual decisão fixa hoje o critério em disputa"),
             "acao": "identifique a decisão vigente, transcreva o dispositivo e marque o fato",
             "versao": VERSAO}]


# ---------------------------------------------------------------------------
# L8 — objeção de revisor externo
# ---------------------------------------------------------------------------

def validar_decisoes_revisao(payload: dict) -> list[dict]:
    """L8: objeção de revisor contra afirmação que TEM lastro no ledger não pode
    ser acatada sem reabrir a fonte.

    Âncora: um revisor externo objetou aos dois períodos de cálculo do § 24. Eu
    concordei sem abrir os autos. A decisão do juízo determinava exatamente
    aqueles dois períodos, com o motivo declarado. A minuta estava certa; a
    objeção e a concordância estavam erradas. Convergência entre revisores não
    substitui a fonte — e o revisor externo, por definição, não tem os autos.
    """
    achados: list[dict] = []
    for obj in payload.get("objections") or payload.get("objecoes") or []:
        oid = str(obj.get("id") or obj.get("titulo") or "?")
        decisao = str(obj.get("decision") or obj.get("decisao") or "").lower()
        if not decisao.startswith(("acat", "accept")):
            continue
        tinha_lastro = bool(obj.get("targetHadSupport") or obj.get("alvoComLastro"))
        reabriu = bool(obj.get("sourceReopened") or obj.get("fonteReaberta"))
        if tinha_lastro and not reabriu:
            achados.append({
                "gate": "L8-objecao", "sev": "P0", "objecaoId": oid,
                "problema": (f"objeção '{oid}' acatada contra afirmação com lastro, sem reabrir "
                             "a fonte — revisor externo não tem os autos"),
                "acao": "reabra o documento e registre o resultado antes de decidir",
                "versao": VERSAO})
    return achados


# ---------------------------------------------------------------------------
# L3 a L6 — gates lexicais sobre o texto
# ---------------------------------------------------------------------------

def analisar_texto(texto: str, tipo: str = "peca") -> list[dict]:
    """Gates lexicais. Rodam sobre qualquer artefato textual do harness."""
    achados: list[dict] = []

    # L3 — não conhecer não é confirmar
    if _NAO_CONHECIMENTO.search(texto) and _CONFIRMACAO.search(texto):
        m = _CONFIRMACAO.search(texto)
        achados.append({
            "gate": "L3-superlativo", "sev": "P0",
            "trecho": _ctx(texto, m.start(), m.end()),
            "problema": ("o texto registra não conhecimento de recurso e, no mesmo documento, "
                         "afirma confirmação: tribunal superior que não conhece não substitui "
                         "o acórdão recorrido"),
            "acao": "troque por 'via recursal esgotada, acórdão incólume'",
            "versao": VERSAO})

    for pat, msg in SUPERLATIVO_PROCESSUAL:
        for m in re.finditer(pat, texto, re.I):
            achados.append({
                "gate": "L3-superlativo", "sev": "P1",
                "trecho": _ctx(texto, m.start(), m.end()),
                "problema": f"{msg} — categoria processual precisa ser nomeada",
                "acao": ("diga qual é: coisa julgada material, preclusão, estabilidade de "
                         "interlocutória ou esgotamento da via recursal"),
                "versao": VERSAO})

    # L4 — percentual com denominador vago
    for m in _PERCENTUAL_VAGO.finditer(texto):
        if _negado(texto[max(0, m.start() - _JANELA_NEGACAO):m.start()]):
            continue
        achados.append({
            "gate": "L4-denominador", "sev": "P1",
            "trecho": _ctx(texto, m.start(), m.end()),
            "problema": "percentual sobre base vaga: o denominador muda sem que o leitor perceba",
            "acao": "nomeie a base exata do percentual",
            "versao": VERSAO})

    # L5 — identidade processual afirmada sem os dois identificadores à vista
    for pat, msg in _IDENTIDADE_PROCESSUAL:
        for m in re.finditer(pat, texto, re.I):
            if _negado(texto[max(0, m.start() - _JANELA_NEGACAO):m.start()]):
                continue
            janela = texto[max(0, m.start() - 400):min(len(texto), m.end() + 400)]
            if len(set(_NUMERO_CNJ.findall(janela))) < 2:
                achados.append({
                    "gate": "L5-identidade", "sev": "P0",
                    "trecho": _ctx(texto, m.start(), m.end()),
                    "problema": (f"{msg} sem os dois identificadores à vista — identidade é "
                                 "conclusão sobre dois documentos, não semelhança percebida"),
                    "acao": "cite os dois números de processo ou retire a afirmação de identidade",
                    "versao": VERSAO})

    # L6 — normas enumeradas por ano sem norma nomeada
    anos_nomeados = {m.group(1) for m in _NORMA_NOMEADA.finditer(texto)}
    for m in _NORMAS_POR_ANO.finditer(texto):
        anos = re.findall(r"(?:1[89]|20)\d{2}", m.group(1))
        orfaos = [a for a in anos if a not in anos_nomeados]
        if orfaos:
            achados.append({
                "gate": "L6-norma-por-ano", "sev": "P0",
                "trecho": _ctx(texto, m.start(), m.end()),
                "problema": (f"normas citadas só pelo ano ({', '.join(orfaos)}) sem norma nomeada "
                             "no texto: crítica não conferível e ano fácil de inventar"),
                "acao": "nomeie cada norma (Lei/Decreto/IN + número + ano)",
                "versao": VERSAO})

    return achados


def fatos_sem_lastro(ledger: dict) -> list[str]:
    """Ids de fatos que afirmam lastro documental sem transcrição verbatim.

    F8 e a entrega usam esta lista como elo bloqueante: nenhum desses fatos pode
    sustentar proposição de peça protocolável, ainda que a pendência esteja
    honestamente declarada.
    """
    pendentes = []
    for fato in (ledger or {}).get("facts") or []:
        if not isinstance(fato, dict):
            continue
        status = str(fato.get("status") or fato.get("classification") or "").strip()
        # Status ausente ou fora do vocabulário conhecido não é isenção: era o
        # caminho de escape do elo 9-B — bastava omitir o campo para o fato sair
        # da lista de pendências sem nunca ter sido conferido. Só os status
        # declaradamente isentos ficam de fora.
        if status in STATUS_SEM_LASTRO:
            continue
        if not (fato.get("quote") or fato.get("trechoSuporte") or "").strip():
            pendentes.append(str(fato.get("id") or fato.get("factId") or "?"))
    return pendentes


# ---------------------------------------------------------------------------
# L9 a L13 — fonte prevalente e valores econômicos (FORJA-LASTRO-v2)
# ---------------------------------------------------------------------------

def material_economico(texto: str) -> bool:
    """Retorna se o texto contém marcador explícito de valor monetário.

    A função é compartilhada pelo verificador, pela composição e pela rota visual.
    Não considera números com ponto de milhar sozinhos: a calibração de 03/08
    mostrou que essa regra confundia processos, leis e decretos com dinheiro.
    """
    return bool(_MOEDA_EXPLICITA.search(texto or ""))


def _sha256_file(caminho: Path, *, bloco: int = 1024 * 1024) -> str:
    """Calcula SHA-256 em fluxo, sem carregar a fonte inteira na memória."""
    digest = hashlib.sha256()
    with caminho.open("rb") as stream:
        while True:
            parte = stream.read(bloco)
            if not parte:
                break
            digest.update(parte)
    return digest.hexdigest()


def _normalizar_data_base(valor: object) -> str | None:
    """Normaliza datas-base para ``AAAA-MM``.

    ``jul/2026`` e ``2026-07`` representam a mesma base mensal; o dia, quando
    presente, não muda a comparação da competência. Datas inválidas não viram
    uma aprovação silenciosa.
    """
    if valor is None:
        return None
    texto = str(valor).strip().lower()
    if not texto:
        return None
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    m = re.search(r"\b(\d{4})[-/](\d{1,2})(?:[-/]\d{1,2})?\b", texto)
    if m:
        ano, mes = int(m.group(1)), int(m.group(2))
        return f"{ano:04d}-{mes:02d}" if 1 <= mes <= 12 else None
    m = re.search(r"\b(\d{1,2})/(\d{4})\b", texto)
    if m:
        mes, ano = int(m.group(1)), int(m.group(2))
        return f"{ano:04d}-{mes:02d}" if 1 <= mes <= 12 else None
    m = re.search(r"\b(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)[a-z]*\s*(?:de\s*|/)?(\d{4})\b", texto)
    if m:
        mes = _MESES.get(m.group(1)[:3])
        return f"{int(m.group(2)):04d}-{mes:02d}" if mes else None
    return None


def _data_base_do_produto(texto: str) -> str | None:
    for m in _DATA_BASE.finditer(texto or ""):
        normalizada = _normalizar_data_base(m.group("valor"))
        if normalizada:
            return normalizada
    return None


def _numero_monetario(valor: str) -> float | None:
    """Converte uma cifra brasileira para comparação tolerante.

    A conversão é apenas aritmética de gate; ela não interpreta a fonte nem
    decide o significado jurídico do número.
    """
    bruto = str(valor or "").lower().replace("\u00a0", " ").strip()
    multiplicador = 1.0
    if "bilh" in bruto:
        multiplicador = 1_000_000_000.0
    elif "milh" in bruto:
        multiplicador = 1_000_000.0
    bruto = re.sub(r"r\$|milh(?:õ|o)es?\s+de\s+reais|bilh(?:õ|o)es?\s+de\s+reais|reais", "", bruto, flags=re.I)
    bruto = re.sub(r"[^0-9,.-]", "", bruto)
    if not bruto:
        return None
    if "," in bruto:
        bruto = bruto.replace(".", "").replace(",", ".")
    elif bruto.count(".") > 1:
        bruto = bruto.replace(".", "")
    try:
        return float(bruto) * multiplicador
    except ValueError:
        return None


def _valores_monetarios(texto: str) -> list[dict]:
    valores: list[dict] = []
    for match in _CIFRA_MONETARIA.finditer(texto or ""):
        bruto = match.group(0).strip()
        linha_ini = texto.rfind("\n", 0, match.start()) + 1
        linha_fim = texto.find("\n", match.end())
        if linha_fim < 0:
            linha_fim = len(texto)
        linha = texto[linha_ini:linha_fim]
        janela = texto[max(0, match.start() - 100):min(len(texto), match.end() + 100)]
        # Valor que a peça CITA não é cálculo nosso e não pode exigir âncora
        # própria — sem esta distinção o L11 trava toda peça que mencione valor
        # de julgado, que é o modo de falha mais provável do gate.
        #
        # Medido em 04/08/2026 sobre 2.491 valores do acervo: a versão anterior
        # reconhecia 2,9% como citação. Duas causas nominais, ambas corrigidas
        # aqui: (1) só aspas curvas eram aceitas, de modo que a transcrição
        # verbatim de `BLUEPRINT_LAUDO.md` — "HOMOLOGA o laudo complementar,
        # fixando a liquidação em R$ 524.141.077,62" — era lida como cálculo do
        # escritório; (2) não havia marcador de origem alheia, então "o laudo de
        # R$ 1.072.604.895,00 não é certificado" também virava cálculo nosso.
        #
        # Marcador tipográfico sozinho — `>` de citação em bloco ou um par de
        # aspas — nunca é prova de origem. Antes, ele marcava `citado=True` e
        # retirava o valor da conferência de âncora; bastava prefixar o próprio
        # cálculo com `>` para silenciar o L11. Agora a tipografia gera uma
        # proveniência frágil: fica registrada como P2 e continua na análise de
        # órfão. A isenção só existe quando a origem externa ou a regra normativa
        # também aparecem no contexto.
        so_tipografico = bool(
            linha.lstrip().startswith(">")
            or ("“" in janela and "”" in janela)
            or janela.count('"') >= 2
        )
        janela_antes = texto[max(0, match.start() - 90):match.start()]
        origem_declarada = bool(
            # A origem precisa estar ligada ao valor, preferencialmente antes
            # dele. Procurar a palavra "laudo" em toda a janela permitiria
            # mascarar um cálculo próprio acrescentando uma referência alheia
            # depois da cifra.
            _ORIGEM_ALHEIA.search(janela_antes)
            or re.search(r"(?:valor|cifra)\s+(?:citado|transcrito)|parte\s+advers[aá]ria|"
                         r"ac[oó]rd[aã]o.{0,35}valor|contrato.{0,35}valor", janela_antes, re.I)
            # Origem alheia declarada imediatamente antes do valor. A janela é
            # curta de propósito: "o laudo de R$ X" é citação; "com base no
            # laudo, calculamos ... R$ X" três linhas abaixo, não.
            or re.search(r"(?:laudo|per[íi]cia|senten[çc]a|ac[oó]rd[aã]o|condena[çc][ãa]o|"
                         r"contrato|ap[óo]lice|evento\s+\d+|Doc\.\s*\d+|nota\s+fiscal|"
                         r"proposta\s+d[ao]s?\s+r[ée]|impugna[çc][ãa]o)"
                         r"[^.\n]{0,40}?(?:de|em|no valor de|fixando|totalizando|traz(?:em)?)?\s*"
                         r"R\$\s*$", janela_antes, re.I)
        )
        normativa = bool(re.search(
            r"(?:al[çc]ada|limiar|teto|piso|acima\s+de|superior\s+a|"
            r"lei|decreto|portaria|resolu[çc][ãa]o|instru[çc][ãa]o\s+normativa)"
            r"[^.\n]{0,60}$", janela_antes, re.I))
        if normativa:
            proveniencia = _PROVENIENCIA_NORMATIVA
        elif origem_declarada:
            proveniencia = _PROVENIENCIA_FONTE
        elif so_tipografico:
            proveniencia = _PROVENIENCIA_TIPOGRAFICA
        else:
            proveniencia = _PROVENIENCIA_CALCULADA
        # Tipografia não é citação confirmada. Esta linha é a blindagem contra
        # o bypass: qualquer alteração futura na forma de calcular a
        # proveniência continua sujeita a esta enumeração fechada.
        citado = proveniencia in {_PROVENIENCIA_FONTE, _PROVENIENCIA_NORMATIVA}
        valores.append({
            "raw": bruto,
            "numero": _numero_monetario(bruto),
            "inicio": match.start(),
            "fim": match.end(),
            "contexto": re.sub(r"\s+", " ", janela).strip(),
            "citado": citado,
            "proveniencia": proveniencia,
            # Verdadeiro quando a isenção veio só da tipografia, sem nenhum
            # sinal de origem alheia. Consumido pelo L11 para registrar a
            # isenção frágil, mas o valor continua sendo conferido.
            "isencaoFragil": proveniencia == _PROVENIENCIA_TIPOGRAFICA,
            "derivado": bool(_ROTULO_DERIVADO.search(janela)),
        })
    return valores


def _fonte_path(fato: dict, base_dir: Path | None) -> Path | None:
    bruto = next((fato.get(k) for k in (
        "quoteSource", "arquivoFonte", "sourcePath", "path", "sourcePathOrUrl"
    ) if fato.get(k)), None)
    if not bruto or str(bruto).startswith(("http://", "https://")):
        return None
    caminho = Path(str(bruto))
    if not caminho.is_absolute() and base_dir:
        caminho = base_dir / caminho
    # Sem confinamento, o próprio fato escolhia qual arquivo o gate iria hashear:
    # `..\..\fora-do-caso\fonte.md` ou um caminho absoluto qualquer fazem a
    # SHA-256 conferir contra um arquivo que o autor controla. O hash provaria
    # apenas que o arquivo não mudou depois — não que é a fonte do caso.
    if base_dir:
        try:
            caminho.resolve().relative_to(Path(base_dir).resolve())
        except (ValueError, OSError):
            return None
    return caminho


def _fonte_prevalente(ledger: dict) -> list[dict]:
    fatos = [f for f in (ledger or {}).get("facts") or [] if isinstance(f, dict)]
    return [f for f in fatos if str(f.get("role") or f.get("papel") or "").casefold()
            in {"fonte_prevalente", "fonte prevalente"}]


def _achado(gate: str, problema: str, *, sev: str = "P0", acao: str | None = None,
            **extra) -> dict:
    item = {"gate": gate, "sev": sev, "problema": problema, "versao": VERSAO}
    if acao:
        item["acao"] = acao
    item.update(extra)
    return item


def validar_fonte_prevalente(ledger: dict | None, *, base_dir: Path | str | None = None,
                             exigir: bool = True) -> list[dict]:
    """L9: fonte econômica precisa ser um papel validado e íntegro no ledger.

    O agente pode registrar ``validationStatus: proposto``; somente a validação
    nominal humana (`validadoPor`/`validadoEm`) autoriza a passagem. A hash é
    conferida novamente contra o arquivo apontado, nunca contra o valor escrito
    no próprio fato.
    """
    if not exigir:
        return []
    base = Path(base_dir) if base_dir else None
    fontes = _fonte_prevalente(ledger or {})
    if not fontes:
        return [_achado("L9-fonte-prevalente", "material econômico sem fato com role='fonte_prevalente'",
                         acao="eleja a fonte governante no fact_ledger e aguarde validação humana")]
    validas = [f for f in fontes if str(f.get("validationStatus") or "").casefold() == "validado"]
    if len(validas) != 1:
        return [_achado(
            "L9-fonte-prevalente",
            f"material econômico exige exatamente uma fonte prevalente validada; encontradas {len(validas)}",
            acao="mantenha uma única fonte com validationStatus='validado', validadoPor e validadoEm")]
    fato = validas[0]
    fid = str(fato.get("id") or fato.get("factId") or "?")
    if not fato.get("validadoPor") or not fato.get("validadoEm"):
        return [_achado("L9-fonte-prevalente", f"{fid}: fonte marcada validado sem validador nominal e data",
                         acao="registre validadoPor e validadoEm após a conferência humana", factId=fid)]
    esperado = str(fato.get("sha256") or "").lower()
    caminho = _fonte_path(fato, base)
    if not esperado or caminho is None or not caminho.is_file():
        return [_achado("L9-fonte-prevalente", f"{fid}: fonte prevalente sem arquivo alcançável e sha256 verificável",
                         acao="aponte o arquivo governante e registre sua SHA-256", factId=fid)]
    try:
        atual = _sha256_file(caminho).lower()
    except OSError as exc:
        return [_achado("L9-fonte-prevalente", f"{fid}: não foi possível ler a fonte prevalente: {exc}", factId=fid)]
    if atual != esperado:
        return [_achado("L9-fonte-prevalente", f"{fid}: sha256 da fonte prevalente diverge do arquivo em disco",
                         acao="reabra o arquivo, recalcule a hash e revalide a fonte", factId=fid,
                         esperado=esperado, encontrado=atual)]
    return []


def _anchor_entries(ledger: dict) -> list[dict]:
    entradas: list[dict] = []
    for chave in ("monetaryAnchors", "economicAnchors", "valorAnchors", "anchors", "lastro"):
        valor = (ledger or {}).get(chave)
        if isinstance(valor, list):
            entradas.extend(item for item in valor if isinstance(item, dict))
    for fato in (ledger or {}).get("facts") or []:
        if not isinstance(fato, dict):
            continue
        for chave in ("monetaryAnchors", "economicAnchors", "valorAnchors", "anchors"):
            valor = fato.get(chave)
            if isinstance(valor, list):
                entradas.extend(item for item in valor if isinstance(item, dict))
    return entradas


def _texto_da_ancora(entrada: dict) -> str:
    return " ".join(str(entrada.get(k) or "") for k in (
        "value", "valor", "amount", "proposicao", "proposition", "label", "descricao", "source",
        "sourceId", "sourceIds", "factId", "factIds", "role", "path"
    ))


def _ancora_aponta_prevalente(entrada: dict, fontes: list[dict]) -> bool:
    texto = _texto_da_ancora(entrada).casefold()
    referencias = set()
    for fato in fontes:
        for valor in (fato.get("id"), fato.get("factId"), fato.get("sha256"),
                      fato.get("quoteSource"), fato.get("arquivoFonte"), fato.get("sourcePath")):
            if valor:
                referencias.add(str(valor).casefold())
    return any(ref and ref in texto for ref in referencias) or "fonte_prevalente" in texto or "fonte prevalente" in texto


def validar_data_base(texto: str, ledger: dict | None, *, exigir: bool = True) -> list[dict]:
    """L10: a data-base expressa no produto coincide com a fonte governante."""
    if not exigir:
        return []
    fontes = _fonte_prevalente(ledger or {})
    validas = [f for f in fontes if str(f.get("validationStatus") or "").casefold() == "validado"]
    if not validas:
        return []  # L9 explica a ausência; evita cascata enganosa.
    esperado = _normalizar_data_base(validas[0].get("dataBase") or validas[0].get("data_base"))
    encontrado = _data_base_do_produto(texto)
    if not esperado:
        return [_achado("L10-data-base", "fonte prevalente validada sem dataBase normalizável",
                         acao="registre dataBase no fato fonte_prevalente")]
    if not encontrado:
        return [_achado("L10-data-base", f"produto econômico sem data-base explícita; a fonte governa {esperado}",
                         acao="declare a data-base da cifra no produto")]
    if encontrado != esperado:
        return [_achado("L10-data-base", f"data-base do produto ({encontrado}) diverge da fonte prevalente ({esperado})",
                         acao="recalcule ou corrija a data-base antes de circular", esperado=esperado,
                         encontrado=encontrado)]
    return []


def validar_valores_monetarios(texto: str, ledger: dict | None, *, exigir: bool = True) -> list[dict]:
    """L11: todo valor calculado material precisa de âncora U6 na fonte eleita."""
    if not exigir:
        # A função também é chamada diretamente por calibradores e scripts de
        # manutenção. Sem esta guarda, uma chamada isolada com `exigir=False`
        # continuava devolvendo lista vazia e reabria o mesmo bypass que a rota
        # canônica já fechou em `validar_gates_economicos`.
        if material_economico(texto):
            return [_achado(
                "L0-economico-desativado",
                "caller tentou desligar L11 diante de produto com material econômico",
                acao="remova exigir=False; o lastro econômico é obrigatório",
            )]
        return []
    todos = _valores_monetarios(texto)
    # `citado` só é verdadeiro para origem externa ou regra normativa
    # explicitamente identificada. A tipografia frágil permanece na lista para
    # que um cálculo próprio com `>` não desapareça da análise.
    valores = [item for item in todos if not item["citado"]]
    achados = []
    # Isenção que veio só da tipografia fica registrada, mas não altera a
    # conclusão do L11. P2: não bloqueia a peça por si só, porém deixa a
    # proveniência incompleta visível e impede que a exceção volte a ser
    # silenciosa.
    for item in todos:
        if item.get("isencaoFragil"):
            achados.append(_achado(
                "L11-isencao-tipografica",
                f"valor {item['raw']} usa marcador tipográfico sem origem alheia "
                "declarada; a cifra continua sujeita à âncora U6",
                acao="declare a fonte do valor ou remova o marcador de citação",
                sev="P2", valor=item["raw"], trecho=item["contexto"],
                proveniencia=item.get("proveniencia"),
                isencaoFragil=True))
    if not valores:
        return achados
    fontes = _fonte_prevalente(ledger or {})
    ancoras = _anchor_entries(ledger or {})
    for item in valores:
        casou = False
        for ancora in ancoras:
            if not _ancora_aponta_prevalente(ancora, fontes):
                continue
            texto_ancora = _texto_da_ancora(ancora)
            numero_ancora = next((
                _numero_monetario(str(ancora.get(k))) for k in ("value", "valor", "amount", "expectedValue")
                if ancora.get(k) is not None
            ), None)
            if numero_ancora is not None and item["numero"] is not None:
                if abs(numero_ancora - item["numero"]) <= max(0.01, abs(item["numero"]) * 0.0001):
                    casou = True
                    break
            if item["raw"].casefold() in texto_ancora.casefold() or item["contexto"].casefold()[:40] in texto_ancora.casefold():
                casou = True
                break
        if not casou:
            achados.append(_achado(
                "L11-valor-orfao",
                f"valor monetário {item['raw']} sem âncora U6 ligada à fonte prevalente",
                # NASCE EM P1 POR MEDIÇÃO, e a decisão está no § 5 do plano 41:
                # "se a distinção não ficar confiável no teste, o L11 nasce em
                # P1, não P0". Medido em 04/08/2026 sobre 2.491 valores do
                # acervo, com amostra de 20 classificada à mão: ~55% dos valores
                # que o gate trata como cálculo nosso são de terceiro, citados
                # ou normativos. Como P0, ele travaria a maior parte das peças
                # que apenas mencionam valor de julgado. Sobe para P0 quando a
                # separação citado × calculado for medida como confiável — e a
                # medida é `forja_calibra_gates_economicos.py`, não impressão.
                sev="P1",
                acao="registre o valor e a fonte na tabela de lastro antes de circular",
                trecho=item["contexto"], valor=item["raw"],
            ))
    return achados


def _descartes(ledger: dict) -> list[dict]:
    itens = []
    for chave in ("discardedSources", "sourceDiscards", "documentosDescartados", "descartesFonte"):
        valor = (ledger or {}).get(chave)
        if isinstance(valor, list):
            itens.extend(item for item in valor if isinstance(item, dict))
    return itens


def _inventario_economico(base_dir: Path | None) -> list[dict]:
    if not base_dir or not base_dir.is_dir():
        return []
    itens = []
    for caminho in sorted(base_dir.rglob("*")):
        if not caminho.is_file() or any(part in {".git", "__pycache__", "runs", "n3_artifacts"} for part in caminho.parts):
            continue
        nome = caminho.name
        if not _ECONOMICO_NO_NOME.search(nome):
            continue
        texto = ""
        if caminho.suffix.casefold() in {".md", ".txt", ".json", ".csv"}:
            try:
                texto = caminho.read_text(encoding="utf-8", errors="replace")[:40_000]
            except OSError:
                pass
        data = None
        for fonte_data in (nome, texto[:5000]):
            for match in _DATA_SOLTA.finditer(fonte_data):
                data = _normalizar_data_base(match.group("valor"))
                if data:
                    break
            if data:
                break
        nome_norm = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().lower()
        autoridade = 3 if re.search(r"laudo|perici", nome_norm) else 2 if "parecer" in nome_norm else 1
        try:
            sha = _sha256_file(caminho)
        except OSError:
            sha = None
        itens.append({"path": str(caminho), "name": nome, "dataBase": data,
                      "authority": autoridade, "sha256": sha})
    return itens


def _examinado(item: dict, examinados: list) -> bool:
    alvo = str(item.get("path") or "").casefold().replace("\\", "/")
    nome = str(item.get("name") or "").casefold()
    for entrada in examinados:
        valor = entrada.get("path") if isinstance(entrada, dict) else entrada
        if not valor:
            continue
        texto = str(valor).casefold().replace("\\", "/")
        if texto == alvo or texto.endswith("/" + nome) or texto == nome:
            return True
    return False


def _descartado(item: dict, descartes: list[dict]) -> bool:
    alvo = str(item.get("path") or "").casefold().replace("\\", "/")
    nome = str(item.get("name") or "").casefold()
    for entrada in descartes:
        valor = next((entrada.get(k) for k in ("path", "arquivo", "documento", "name") if entrada.get(k)), None)
        motivo = str(entrada.get("reason") or entrada.get("motivo") or "").strip()
        if valor and motivo and (str(valor).casefold().replace("\\", "/") in {alvo, nome} or alvo.endswith("/" + str(valor).casefold().replace("\\", "/"))):
            return True
    return False


def validar_hierarquia_fontes(ledger: dict | None, *, base_dir: Path | str | None = None,
                              exigir: bool = True) -> list[dict]:
    """L12: confronta o fato eleito com o inventário físico do caso."""
    if not exigir:
        return []
    fontes = [f for f in _fonte_prevalente(ledger or {})
              if str(f.get("validationStatus") or "").casefold() == "validado"]
    if not fontes:
        return []
    base = Path(base_dir) if base_dir else None
    inventario = _inventario_economico(base)
    if not inventario:
        return []
    eleito = _fonte_path(fontes[0], base)
    eleito_norm = str(eleito.resolve()).casefold() if eleito and eleito.exists() else ""
    examinados = (ledger or {}).get("documentosExaminados") or (ledger or {}).get("examinedDocuments") or []
    descartes = _descartes(ledger or {})
    data_eleita = _normalizar_data_base(fontes[0].get("dataBase") or fontes[0].get("data_base"))
    autoridade_eleita = 3 if eleito and re.search(r"laudo|per[ií]cia", eleito.name, re.I) else 2 if eleito and re.search(r"parecer", eleito.name, re.I) else 1
    achados = []
    for item in inventario:
        item_norm = str(Path(item["path"]).resolve()).casefold()
        if eleito_norm and item_norm == eleito_norm:
            continue
        if _descartado(item, descartes):
            continue
        if not _examinado(item, examinados):
            achados.append(_achado("L12-hierarquia-fonte",
                                   f"documento econômico candidato não consta em documentosExaminados: {item['name']}",
                                   acao="abra o documento ou registre descarte escrito com motivo", documento=item["name"]))
            continue
        if data_eleita and item.get("dataBase") and item["dataBase"] > data_eleita:
            achados.append(_achado("L12-hierarquia-fonte",
                                   f"documento econômico com data-base posterior ({item['dataBase']}) não foi eleito: {item['name']}",
                                   acao="eleja a fonte posterior ou descarte-a por escrito", documento=item["name"]))
        elif item.get("authority", 0) > autoridade_eleita:
            achados.append(_achado("L12-hierarquia-fonte",
                                   f"documento com autoridade documental superior não foi eleito: {item['name']}",
                                   acao="justifique a hierarquia ou eleja a fonte superior", documento=item["name"]))
    return achados


def validar_aritmetica_derivada(texto: str, ledger: dict | None, *, exigir: bool = True) -> list[dict]:
    """L13: recompõe cálculo derivado contra base e percentual declarados."""
    if not exigir:
        return []
    if not _ROTULO_DERIVADO.search(texto or ""):
        return []
    calculos = []
    for chave in ("derivedCalculations", "calculosDerivados", "derivedValues", "calculos"):
        valor = (ledger or {}).get(chave)
        if isinstance(valor, list):
            calculos.extend(item for item in valor if isinstance(item, dict))
    for fato in (ledger or {}).get("facts") or []:
        if isinstance(fato, dict) and isinstance(fato.get("derivedCalculations"), list):
            calculos.extend(item for item in fato["derivedCalculations"] if isinstance(item, dict))
    if not calculos:
        return [_achado("L13-aritmetica-derivada", "produto apresenta valor/faixa derivada sem memória de cálculo",
                         acao="registre base, percentual, resultado esperado e tolerância no ledger")]
    valores = _valores_monetarios(texto)
    achados = []
    for calc in calculos:
        base = _numero_monetario(str(calc.get("baseValue") or calc.get("base") or ""))
        percentual = calc.get("percentage", calc.get("percentual", calc.get("rate")))
        esperado = _numero_monetario(str(calc.get("expectedValue") or calc.get("valorEsperado") or calc.get("result") or ""))
        if base is None or percentual is None or esperado is None:
            achados.append(_achado("L13-aritmetica-derivada", f"cálculo derivado incompleto: {calc.get('id') or calc.get('label') or '?'}",
                                   acao="informe baseValue, percentage e expectedValue"))
            continue
        try:
            taxa = float(percentual)
            if abs(taxa) > 1:
                taxa /= 100.0
        except (TypeError, ValueError):
            achados.append(_achado("L13-aritmetica-derivada", f"percentual inválido no cálculo {calc.get('id') or '?'}"))
            continue
        operacao = str(calc.get("operation") or calc.get("operacao") or "add").casefold()
        # Operação desconhecida caía no ramo da multiplicação e aprovava um
        # resultado que ninguém pediu: `subtract` com base 100 e 10% conferia
        # contra 10, quando o esperado seria 90. Recompor errado é pior que não
        # recompor, porque o gate assina embaixo.
        if operacao in {"add", "mais", "acrescimo", "acréscimo"}:
            recomputado = base * (1 + taxa)
        elif operacao in {"multiply", "percent", "percentual", "aplicar", "fracao", "fração"}:
            recomputado = base * taxa
        elif operacao in {"subtract", "menos", "deducao", "dedução", "desconto"}:
            recomputado = base * (1 - taxa)
        else:
            achados.append(_achado("L13-aritmetica-derivada",
                                   f"operação '{operacao}' não é reconhecida pelo recomputo "
                                   f"no cálculo {calc.get('id') or calc.get('label') or '?'}",
                                   acao="use add, multiply ou subtract, ou estenda o gate"))
            continue
        tolerancia = float(calc.get("tolerance", calc.get("tolerancia", 0.01)) or 0.01)
        if abs(recomputado - esperado) > tolerancia:
            achados.append(_achado("L13-aritmetica-derivada",
                                   f"cálculo {calc.get('id') or calc.get('label') or '?'} incompatível: base×percentual resulta {recomputado:.2f}, ledger declara {esperado:.2f}",
                                   acao="recalcule a faixa contra a base validada", esperado=esperado, recomputado=recomputado))
        rotulo = str(calc.get("label") or calc.get("id") or "").casefold()
        if rotulo and not any(rotulo in str(v.get("contexto") or "").casefold() for v in valores):
            # Ausência de rótulo no texto não inventa P0 adicional: o L11 cobre
            # a âncora do número e o cálculo já foi conferido acima.
            continue
    return achados


def validar_gates_economicos(texto: str, *, ledger: dict | None = None,
                             base_dir: Path | str | None = None,
                             exigir: bool | None = None) -> list[dict]:
    """Executa L9--L13 somente para produto com material econômico."""
    detectado = material_economico(texto)
    # A incidência pode ser determinada automaticamente ou reforçada pela rota
    # canônica, mas não pode ser desligada por um caller diante de texto que
    # contém material econômico. ``exigir=False`` era uma porta ad hoc para
    # omitir L9--L13 e produzir aprovação com lastro não examinado.
    if detectado and exigir is not None and not bool(exigir):
        return [_achado(
            "L0-economico-desativado",
            "caller tentou desligar L9-L13 diante de produto com material econômico",
            acao="remova exigir=False; gates econômicos são obrigatórios para este produto",
        )]
    aplicar = detectado if exigir is None else bool(exigir)
    if not aplicar:
        return []
    return (
        validar_fonte_prevalente(ledger, base_dir=base_dir)
        + validar_data_base(texto, ledger)
        + validar_valores_monetarios(texto, ledger)
        + validar_hierarquia_fontes(ledger, base_dir=base_dir)
        + validar_aritmetica_derivada(texto, ledger)
    )


def verificar_tudo(texto: str, *, ledger: dict | None = None, revisao: dict | None = None,
                   base_dir: Path | str | None = None, tipo: str = "peca",
                   exigir_criterio: bool = False, exigir_economico: bool | None = None) -> list[dict]:
    """Conveniência: roda os gates aplicáveis ao material disponível.

    ``exigir_economico`` é reservado a uma rota que já sabe que o produto é
    econômico; omitido, a incidência é determinada pela marcação estreita de
    moeda. A ausência de contexto de ledger não passa silenciosamente: L9
    reprova produto econômico.
    """
    achados = analisar_texto(texto, tipo)
    if ledger:
        achados += validar_lastro_fatos(ledger, base_dir=base_dir)
        if exigir_criterio:
            achados += exigir_criterio_vigente(ledger)
    achados += validar_gates_economicos(
        texto, ledger=ledger, base_dir=base_dir, exigir=exigir_economico
    )
    if revisao:
        achados += validar_decisoes_revisao(revisao)
    return achados


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(sys.argv) < 2:
        print("uso: python forja_lastro.py <arquivo.md> [--ledger F] [--base-dir D] "
              "[--revisao F] [--exigir-criterio] [--exigir-economico]")
        sys.exit(2)

    def _arg(nome):
        return sys.argv[sys.argv.index(nome) + 1] if nome in sys.argv else None

    alvo = sys.argv[1]
    led = json.loads(Path(_arg("--ledger")).read_text(encoding="utf-8")) if _arg("--ledger") else None
    rev = json.loads(Path(_arg("--revisao")).read_text(encoding="utf-8")) if _arg("--revisao") else None
    viol = verificar_tudo(Path(alvo).read_text(encoding="utf-8"), ledger=led, revisao=rev,
                          base_dir=_arg("--base-dir"),
                          exigir_criterio="--exigir-criterio" in sys.argv,
                          exigir_economico=True if "--exigir-economico" in sys.argv else None)
    print(json.dumps({"arquivo": alvo, "versao": VERSAO, "total": len(viol),
                      "p0": sum(1 for v in viol if v["sev"] == "P0"),
                      "violacoes": viol}, ensure_ascii=False, indent=2))
    sys.exit(1 if any(v["sev"] == "P0" for v in viol) else 0)
