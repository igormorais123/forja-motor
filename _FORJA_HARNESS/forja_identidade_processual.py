# -*- coding: utf-8 -*-
"""
forja_identidade_processual.py — Captura e validação de identidade processual.

Motivo (diagnóstico 2026-08-05): As mutações S2 (troca de parte) e S4 (troca de
pedido) estão em 0% porque nenhum dos 27 casos registra quem é a cliente, qual é
seu papel processual e qual a direção do pedido dela. Sem esse FATO EXTERNO ao
texto da peça, nenhum gate consegue distinguir "a peça cita o pedido do adversário"
de "a peça pede contra si mesma".

Este módulo cria o artefato F2_IDENTIDADE_PROCESSUAL.json com:
  - cliente: {nome, papel} — papel em vocabulário fechado
  - adverso: {nome, papel} — mesmo vocabulário
  - direcaoPedido: provimento|desprovimento|...
  - lastro: {sourceKey, sha256, trechoVerbatim} — obrigatório, de fonte EXTERNA

O LASTRO deve vir de FORA da redação: comando do caso, decisão impugnada, e-mail.
NUNCA da minuta ou do CANONICAL_TEXT_FROM_FINAL_DOCX.txt — esses seriam mutados
junto e o gate nasceria cego.

Schema versão: FORJA-IDENTIDADE-PROCESSUAL-v1
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

VERSAO = "FORJA-IDENTIDADE-PROCESSUAL-v1"

# Vocabulário fechado de papéis processuais. Nota: "terceiro_interessado" é papel
# raro; incluído por completude. A realidade esperada é cliente = agravante ou
# apelante ou similar, adverso = agravado ou apelado ou similar.
# Inclui variações de gênero (feminino e masculino).
PAPEIS_VALIDOS = {
    "agravante", "agravado", "agravada",
    "apelante", "apelado", "apelada",
    "embargante", "embargado", "embargada",
    "autor", "autora", "reu", "rea",
    "exequente", "executado", "executada",
    "recorrente", "recorrido", "recorrida",
    "impetrante", "impetrado", "impetrada",
    "terceiro_interessado", "terceira_interessada",
}

# Direção do pedido: o que a cliente pede. Vocabulário fechado.
DIRECOES_VALIDAS = {
    "provimento",      # reforma favorável ao recorrente
    "desprovimento",   # mantém decisão original favorável ao recorrente
    "procedencia",     # sentença de primeiro grau na direção do autor
    "improcedencia",   # sentença de primeiro grau na direção do réu
    "acolhimento",     # admissão de recurso ou incidente
    "rejeicao",        # rejeição de recurso ou incidente
    "manutencao",      # mantém o que foi antes
    "reforma",         # reforma
}

# Papéis que denotam ativo (cliente pedindo algo):
PAPEIS_ATIVOS = {"agravante", "apelante", "embargante", "autor", "autora", "exequente", "recorrente", "impetrante"}

# Papéis que denotam passivo (cliente sendo pedida):
PAPEIS_PASSIVOS = {"agravado", "agravada", "apelado", "apelada", "embargado", "embargada", "reu", "rea", "executado", "executada", "recorrido", "recorrida", "impetrado", "impetrada"}


def schema_identidade_processual() -> dict:
    """Retorna o schema esperado de F2_IDENTIDADE_PROCESSUAL.json.

    Pronto para incluir em spec docs ou validation.
    """
    return {
        "schemaVersion": 1,
        "artifactType": "F2_IDENTIDADE_PROCESSUAL",
        "caseId": "string (preenchido pelo harness)",
        "cliente": {
            "nome": "string (nome próprio da cliente)",
            "papel": f"enum ({', '.join(sorted(PAPEIS_VALIDOS))})",
        },
        "adverso": {
            "nome": "string (nome próprio do adversário)",
            "papel": f"enum ({', '.join(sorted(PAPEIS_VALIDOS))})",
        },
        "direcaoPedido": f"enum ({', '.join(sorted(DIRECOES_VALIDAS))})",
        "lastro": {
            "sourceKey": "string (chave de n4SourceRegistry do FORJA_CASE_MANIFEST.json)",
            "sha256": "string (hash do arquivo fonte para auditoria)",
            "trechoVerbatim": "string (trecho literal que sustenta a declaração, ≥25 chars)",
        },
        # Blocos opcionais. Sem eles os gates S6 e S7 não rodam e não opinam —
        # o caso fica indeterminado, nunca reprovado por ausência de declaração.
        "atos": {
            "impugnado": "string (o ato que ESTA peça impugna, com identificador)",
            "proprios": "lista (identificadores deste mesmo trabalho: autos, recurso)",
            "relacionados": "lista (o que pode ser citado legitimamente; tudo fora vira P0)",
        },
        "objeto": {
            "devolvido": "string (o que o tribunal pode decidir neste recurso)",
            "excluidos": "lista (temas fora do objeto; sustentá-los na peça vira P0)",
        },
        "createdAt": "ISO 8601 timestamp",
        "note": "string (opcional: contexto do declarante, lacunas detectadas, etc.)",
    }


class ValidacaoIdentidadeProcessual:
    """Resultado da validação de uma declaração."""

    def __init__(self, valida: bool = False, erros: list = None, avisos: list = None):
        self.valida = valida
        self.erros = erros or []
        self.avisos = avisos or []


def validar_papel(papel: str) -> bool:
    """Verdadeiro se papel está no vocabulário fechado."""
    return papel.lower().strip() in PAPEIS_VALIDOS


def validar_direcao(direcao: str) -> bool:
    """Verdadeiro se direção está no vocabulário fechado."""
    return direcao.lower().strip() in DIRECOES_VALIDAS


def validar_lastro_de_fonte_externa(
    decl: dict,
    manifest: dict,
    *,
    base_dir: Path | str | None = None,
) -> ValidacaoIdentidadeProcessual:
    """
    Valida que o lastro vem de fonte EXTERNA à redação.

    Erros P0:
      - lastro ausente
      - lastro apontando para artefato derivado (minuta, draft, CANONICAL_TEXT_FROM_FINAL_DOCX)
      - sourceKey apontando para role='minuta' ou role='produção' no manifesto
      - trecho verbatim ausente ou muito curto
      - trecho não encontrado na fonte apontada (P1)

    Avisos:
      - fonte não localizada (P1: não conferível, mas não erro)
    """
    erros = []
    avisos = []

    # L0: Lastro existe
    lastro = decl.get("lastro")
    if not lastro:
        erros.append("P0: lastro ausente — declaração sem fonte")
        return ValidacaoIdentidadeProcessual(valida=False, erros=erros)

    sourceKey = lastro.get("sourceKey", "").strip()
    if not sourceKey:
        erros.append("P0: sourceKey vazio — impossível localizar fonte no manifesto")
        return ValidacaoIdentidadeProcessual(valida=False, erros=erros)

    # L1: SourceKey apontando para fonte EXTERNA, não interna
    n4SourceRegistry = manifest.get("n4SourceRegistry", {})
    if sourceKey not in n4SourceRegistry:
        erros.append(f"P0: sourceKey '{sourceKey}' não localizado no n4SourceRegistry")
        return ValidacaoIdentidadeProcessual(valida=False, erros=erros)

    fonte_info = n4SourceRegistry[sourceKey]

    # Rejeitar referências que visam o texto da própria peça ou seus derivados
    path_str = (fonte_info.get("path") or "").lower()
    if any(palavra in path_str for palavra in [
        "draft",
        "canonical_text_from_final_docx",
        "minuta",
        "produção",
        "final_docx",
        "final_markdown",
    ]):
        erros.append(
            f"P0: sourceKey '{sourceKey}' aponta para artefato derivado da redação "
            f"('{path_str}'), não para fonte externa — o lastro nasceria mutado junto"
        )
        return ValidacaoIdentidadeProcessual(valida=False, erros=erros)

    # L2: Transcrição existe e é não-vazia
    trecho = (lastro.get("trechoVerbatim") or "").strip()
    if not trecho:
        avisos.append("P1: trechoVerbatim ausente — source conferido mas sem transcrição")
    elif len(trecho) < 25:
        avisos.append(
            f"P1: trechoVerbatim muito curto ({len(trecho)} chars) — "
            "pode não ser suficiente para provar leitura real"
        )

    # L3: SHA256 registrado para auditoria (não é erro se faltar, mas bom ter)
    sha256 = lastro.get("sha256", "").strip()
    if not sha256:
        avisos.append("P1: sha256 ausente — não há checksum de integridade do arquivo")

    return ValidacaoIdentidadeProcessual(valida=len(erros) == 0, erros=erros, avisos=avisos)


def validar_declaracao_completa(decl: dict) -> ValidacaoIdentidadeProcessual:
    """
    Valida a estrutura e vocabulário de uma declaração.

    Erros P0:
      - cliente ou adverso ausentes ou sem nome/papel
      - papel em vocabulário inválido
      - direcaoPedido em vocabulário inválido
    """
    erros = []
    avisos = []

    # Cliente
    cliente = decl.get("cliente") or {}
    if not cliente:
        erros.append("P0: cliente ausente")
    else:
        nome_cliente = (cliente.get("nome") or "").strip()
        if not nome_cliente:
            erros.append("P0: cliente.nome vazio")

        papel_cliente = (cliente.get("papel") or "").strip()
        if not papel_cliente:
            erros.append("P0: cliente.papel vazio")
        elif not validar_papel(papel_cliente):
            erros.append(f"P0: cliente.papel '{papel_cliente}' não está em PAPEIS_VALIDOS")

    # Adverso
    adverso = decl.get("adverso") or {}
    if not adverso:
        erros.append("P0: adverso ausente")
    else:
        nome_adverso = (adverso.get("nome") or "").strip()
        if not nome_adverso:
            erros.append("P0: adverso.nome vazio")

        papel_adverso = (adverso.get("papel") or "").strip()
        if not papel_adverso:
            erros.append("P0: adverso.papel vazio")
        elif not validar_papel(papel_adverso):
            erros.append(f"P0: adverso.papel '{papel_adverso}' não está em PAPEIS_VALIDOS")

    # Direção do pedido
    direcao = (decl.get("direcaoPedido") or "").strip()
    if not direcao:
        erros.append("P0: direcaoPedido vazio")
    elif not validar_direcao(direcao):
        erros.append(f"P0: direcaoPedido '{direcao}' não está em DIRECOES_VALIDAS")

    return ValidacaoIdentidadeProcessual(valida=len(erros) == 0, erros=erros, avisos=avisos)


def carregar_declaracao(case_dir: Path | str) -> Optional[dict]:
    """
    Carrega F2_IDENTIDADE_PROCESSUAL.json de um caso.

    Retorna None se o arquivo não existe.
    """
    case_dir = Path(case_dir)
    decl_path = case_dir / "n4_artifacts" / "F2_IDENTIDADE_PROCESSUAL.json"

    if not decl_path.exists():
        return None

    try:
        return json.loads(decl_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


# =============================================================================
# GATES DE MUTAÇÃO SEMÂNTICA — S2 e S4
# =============================================================================

def _normalizar_nome(nome: str) -> str:
    """Normaliza nome para comparação: minúsculas, sem extra space, sem variações."""
    nome = nome.lower().strip()
    nome = re.sub(r'\s+', ' ', nome)
    # Remove sufixos comuns de título que não afetam identidade
    nome = re.sub(r'\b(ltda|s\.?a\.?|eireli|mei|spa|epp)\.?$', '', nome, flags=re.I)
    return nome.strip()


def gate_s2_pareamento_nome_papel(
    texto: str,
    decl: Optional[dict],
) -> list[dict]:
    """
    Gate S2: pareamento nome ↔ papel da cliente.

    O NOME da cliente NÃO é mutado por S2. Se a declaração diz "CASO-04 = agravada"
    mas o texto passa a colar "CASO-04" a "agravante", há divergência.

    Medida: proximidade em janela de ~200 caracteres. Conta as duas direções.
    Veredito por maioria: se maioria das ocorrências está em divergência, é P0.

    Retorna lista de dicts {sev, gate, problema, contexto}.
    """
    achados = []

    # Indeterminado: sem declaração
    if not decl:
        return []

    cliente = decl.get("cliente") or {}
    nome_cliente = (cliente.get("nome") or "").strip()
    papel_cliente = (cliente.get("papel") or "").strip()

    if not nome_cliente or not papel_cliente:
        return []  # Indeterminado

    # Normalizar para busca
    nome_norm = _normalizar_nome(nome_cliente)
    papel_norm = papel_cliente.lower().strip()

    # Buscar ocorrências do NOME no texto
    matches = list(re.finditer(re.escape(nome_norm), texto.lower(), re.IGNORECASE))
    if not matches:
        # Nome não aparece no texto — é incomum mas legítimo (pode estar nos autos)
        return []

    # Para cada match, verificar se o papel DECLARADO aparece próximo
    divergencias = 0
    confirmacoes = 0
    total = len(matches)

    JANELA = 200  # caracteres antes e depois

    for match in matches:
        ini = max(0, match.start() - JANELA)
        fim = min(len(texto), match.end() + JANELA)
        contexto_janela = texto[ini:fim].lower()

        # Verificar se o papel declarado aparece nesta janela
        # Flexão: agravado(s)(a)(as), papel/papéis, etc.
        papel_pattern = papel_norm.replace('ado', '[ao]d[oa]s?').replace('ante', 'ante[sa]?')
        if re.search(papel_pattern, contexto_janela, re.IGNORECASE):
            confirmacoes += 1
        else:
            divergencias += 1

    # Veredito: maioria = decisor. Se >50% das janelas NÃO têm o papel declarado, é P0.
    if divergencias > confirmacoes:
        contexto = _ctx(texto, matches[0].start(), matches[0].end(), 100)
        achados.append({
            "gate": "S2-pareamento-nome-papel",
            "sev": "P0",
            "familia": "S2_troca_de_parte",
            "problema": (
                f"Nome '{nome_cliente}' (papel='{papel_cliente}') aparece {total} vezes "
                f"no texto, mas o papel declarado está próximo em apenas "
                f"{confirmacoes}/{total} ocorrências (divergências: {divergencias})"
            ),
            "contexto": contexto,
            "versao": VERSAO,
        })

    return achados


def gate_s4_presenca_direcao_pedido(
    texto: str,
    decl: Optional[dict],
) -> list[dict]:
    """
    Gate S4: presença da direção declarada.

    Se a declaração diz "desprovimento" e a palavra "desprovimento" (e flexões)
    desaparece por completo do texto enquanto "provimento" aparece, há divergência.

    Numa peça legítima, a direção declarada ESTÁ presente (pode estar citando o
    pedido do adversário, mas está lá).

    Retorna lista de dicts {sev, gate, problema, contexto}.
    """
    achados = []

    # Indeterminado: sem declaração
    if not decl:
        return []

    direcao = (decl.get("direcaoPedido") or "").strip().lower()
    if not direcao:
        return []  # Indeterminado

    # Expandir flexões baseado na direção
    if direcao == "provimento":
        padrao_buscado = r'\b(?:provimento|reforma\b)'
        contrario = r'\bdesprovimento'
    elif direcao == "desprovimento":
        padrao_buscado = r'\bdesprovimento'
        contrario = r'\bprovimento'
    elif direcao == "procedencia":
        padrao_buscado = r'\b(?:procedência|procedencia)'
        contrario = r'\b(?:improcedência|improcedencia)'
    elif direcao == "improcedencia":
        padrao_buscado = r'\b(?:improcedência|improcedencia)'
        contrario = r'\b(?:procedência|procedencia)'
    elif direcao == "acolhimento":
        padrao_buscado = r'\b(?:acolhimento|acolhida?)'
        contrario = r'\b(?:rejeição|rejeicao)'
    elif direcao == "rejeicao":
        padrao_buscado = r'\b(?:rejeição|rejeicao)'
        contrario = r'\b(?:acolhimento|acolhida?)'
    else:
        # Direção não mapeada — retornar indeterminado
        return []

    texto_lower = texto.lower()

    # Buscar a direção declarada
    matches_buscado = list(re.finditer(padrao_buscado, texto_lower, re.IGNORECASE))
    matches_contrario = list(re.finditer(contrario, texto_lower, re.IGNORECASE))

    # ---- Sinal do REQUERIMENTO -------------------------------------------
    #
    # A regra global abaixo — "a direção declarada sumiu do texto inteiro" — só
    # dispara quando a troca é total. A mutação real troca UMA ocorrência por
    # vez, e no caso CASO-04 AgInt o texto tem `desprovimento` três vezes: uma
    # troca deixa duas, e a regra global fica cega.
    #
    # O que resolve é olhar onde a cliente fala em nome próprio. No corpo da
    # peça as duas direções convivem legitimamente, porque a peça narra o que o
    # adversário pediu; no requerimento final, não: ali só cabe o que a cliente
    # quer. Se a direção contrária aparece no requerimento e a declarada não,
    # a peça está pedindo contra si mesma.
    regiao = _regiao_requerimento(texto)
    if regiao:
        regiao_lower = regiao.lower()
        tem_declarada = re.search(padrao_buscado, regiao_lower, re.IGNORECASE)
        contra_regiao = list(re.finditer(contrario, regiao_lower, re.IGNORECASE))
        if contra_regiao and not tem_declarada:
            achados.append({
                "gate": "S4-direcao-no-requerimento",
                "sev": "P0",
                "familia": "S4_troca_de_pedido",
                "problema": (
                    f"No requerimento a peça pede '{contra_regiao[0].group().strip()}', "
                    f"e a identidade processual do caso declara que a cliente pede "
                    f"'{direcao}' — a peça estaria pedindo contra a própria cliente"
                ),
                "contexto": _ctx(regiao, contra_regiao[0].start(), contra_regiao[0].end(), 110),
                "versao": VERSAO,
            })

    # P0: direção declarada AUSENTE no texto
    if not matches_buscado:
        # Mas se a direção contrária aparece massivamente, pode ser mutação
        if matches_contrario:
            contexto = _ctx(texto, matches_contrario[0].start(), matches_contrario[0].end(), 100)
            achados.append({
                "gate": "S4-presenca-direcao",
                "sev": "P0",
                "familia": "S4_troca_de_pedido",
                "problema": (
                    f"Direção declarada '{direcao}' não aparece no texto, "
                    f"mas sua contrária '{contrario.replace(r'\\b', '')}' aparece "
                    f"{len(matches_contrario)} vezes — possível troca S4"
                ),
                "contexto": contexto,
                "versao": VERSAO,
            })

    return achados


_MARCADORES_REQUERIMENTO = (
    r"ante o exposto", r"diante do exposto", r"pelo exposto", r"por todo o exposto",
    r"isso posto", r"em face do exposto", r"do exposto",
    r"requer(?:-se|em|em-se)?\b", r"pede deferimento", r"nestes termos",
    r"termos em que", r"pugna(?:-se|m)?\b",
)


def _regiao_requerimento(texto: str) -> str:
    """A parte final em que a cliente fala em nome próprio.

    Delimitada pelo PRIMEIRO marcador que ocorre na metade final da peça — o
    que ABRE o requerimento, e não o que o fecha. Pegar o último marcador
    parecia natural e estava errado: "pede deferimento" e "nestes termos" vêm
    DEPOIS da lista de pedidos, e a região resultante era só o bloco de
    assinatura, sem nenhum verbo de pedido dentro. O gate ficava
    silenciosamente cego.

    O corte pela metade é conservador de propósito: marcador que aparece cedo
    demais não é requerimento, é argumentação que por acaso usa a palavra, e
    devolver isso faria o gate ler o corpo da peça como pedido. Sem marcador
    confiável a função devolve vazio, e o gate fica indeterminado em vez de
    chutar sobre um pedaço arbitrário do texto.
    """
    if not texto:
        return ""
    baixo = texto.lower()
    metade = len(texto) * 0.5
    inicio = None
    for marcador in _MARCADORES_REQUERIMENTO:
        for m in re.finditer(marcador, baixo):
            if m.start() >= metade and (inicio is None or m.start() < inicio):
                inicio = m.start()
    if inicio is None:
        return ""
    return texto[inicio:]


def _ctx(texto: str, ini: int, fim: int, alcance: int = 60) -> str:
    """Contexto ao redor de um match."""
    a = max(0, ini - alcance)
    b = min(len(texto), fim + alcance)
    return re.sub(r'\s+', ' ', texto[a:b]).strip()


# ---------------------------------------------------------------------------
# S6 e S7 — identidade do ato recursal e objeto devolvido (06/08/2026)
#
# Vieram de correção escrita do titular, em dois casos distintos e depois de a
# regra já existir por escrito no protocolo da casa desde 11/07/2026. Em um
# deles o titular teve de listar, um a um, os recursos do MESMO cliente que a
# peça citava sem pertencerem àquele trabalho; no outro, apontou transposição
# de dados de um processo paralelo para o processo efetivamente pautado, com
# referências incorretas ao recurso, aos eventos e ao órgão julgador.
#
# O erro não é escrever um número errado: é escrever o número CERTO de outro
# processo do mesmo cliente. O texto fica internamente coerente, e nenhum gate
# lexical tem como discordar dele.
#
# Uma regra que vive só como instrução de prompt disputa atenção com todo o
# resto e perde. Estes dois gates são a decisão do Igor em 06/08/2026 de
# convertê-la em bloqueio verificável, no mesmo desenho dos S2/S4: **lastro
# externo declarado, e caso sem declaração não tem veredito** — nunca P0
# automático por ausência.
# ---------------------------------------------------------------------------

# Identificadores de ato processual que aparecem no corpo de uma peça.
RE_ATOS = re.compile(
    r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b"                    # CNJ
    r"|\b(?:REsp|AREsp|AgInt|AgRg|EAREsp|EREsp|RE|ARE|AI|RO)\s*n?[º°.]?\s*"
    r"[\d][\d.\-/]{3,}\b",                                          # recurso numerado
    re.I,
)


def _atos_declarados(decl: Optional[dict]) -> set:
    """Identificadores que a declaração reconhece como deste trabalho."""
    if not decl:
        return set()
    bloco = decl.get("atos") or {}
    declarados = []
    for chave in ("impugnado", "proprios", "relacionados"):
        valor = bloco.get(chave)
        if isinstance(valor, str):
            declarados.append(valor)
        elif isinstance(valor, list):
            declarados.extend(str(item) for item in valor)
    return {_chave_ato(item) for item in declarados if str(item).strip()}


def _chave_ato(bruto: str) -> str:
    """Só os dígitos: compara identificador sem depender de pontuação ou rótulo."""
    return re.sub(r"\D", "", str(bruto))


def gate_s6_identidade_do_ato(texto: str, decl: Optional[dict]) -> list[dict]:
    """Todo ato citado na peça foi declarado como pertencente a este trabalho?

    O erro que ele fecha não é escrever um número errado: é escrever o número
    CERTO **de outro processo do mesmo cliente**. Nenhum gate lexical apanha
    isso, porque o texto fica internamente coerente — só uma lista externa do
    que pertence a este trabalho separa um do outro.

    Sem `atos` na declaração o gate não roda e não opina.
    """
    declarados = _atos_declarados(decl)
    if not declarados:
        return []
    achados = []
    vistos = set()
    for m in RE_ATOS.finditer(texto):
        bruto = m.group(0)
        chave = _chave_ato(bruto)
        if len(chave) < 6 or chave in declarados or chave in vistos:
            continue
        # O mesmo ato escrito de outro jeito — com e sem dígito verificador, com
        # e sem sufixo do tribunal — difere no começo ou no fim, nunca no meio.
        # A comparação por conteúdo em qualquer posição era frouxa demais: um
        # número curto aparece por acaso dentro de um CNJ longo e seria
        # absolvido, que é exatamente o erro que este gate existe para pegar.
        if any(chave.startswith(alvo) or alvo.startswith(chave) or
               chave.endswith(alvo) or alvo.endswith(chave)
               for alvo in declarados):
            continue
        vistos.add(chave)
        achados.append({
            "sev": "P0",
            "gate": "S6_IDENTIDADE_DO_ATO",
            "problema": (f"ato processual citado e não declarado neste trabalho: "
                         f"'{bruto.strip()}'. Ou ele pertence a outro desdobramento "
                         f"do caso, ou falta declará-lo em atos.relacionados."),
            "contexto": _ctx(texto, m.start(), m.end()),
        })
    return achados


def gate_s7_objeto_devolvido(texto: str, decl: Optional[dict]) -> list[dict]:
    """A peça sustenta tema que a declaração excluiu do objeto do recurso?

    Nasceu da correção mais recorrente do titular: a peça trata de tudo o que é
    verdadeiro sobre o caso, e não do que o tribunal pode decidir. A lista de
    exclusões é declarada por pessoa — inferir escopo de prosa argumentativa é
    o erro que a esteira já cometeu na figura de cronologia.
    """
    excluidos = ((decl or {}).get("objeto") or {}).get("excluidos") or []
    if not excluidos:
        return []
    achados = []
    for tema in excluidos:
        tema = str(tema).strip()
        if len(tema) < 4:
            continue
        for m in re.finditer(re.escape(tema), texto, re.I):
            achados.append({
                "sev": "P0",
                "gate": "S7_OBJETO_DEVOLVIDO",
                "problema": (f"a peça sustenta '{tema}', declarado FORA do objeto "
                             f"devolvido ao tribunal neste recurso."),
                "contexto": _ctx(texto, m.start(), m.end()),
            })
            break  # uma ocorrência basta para acusar o tema
    return achados


if __name__ == "__main__":
    import sys

    # Script de teste/auditoria
    if len(sys.argv) < 2:
        print("uso: python forja_identidade_processual.py <case-dir>")
        print("      python forja_identidade_processual.py --schema")
        sys.exit(2)

    if sys.argv[1] == "--schema":
        import json
        print(json.dumps(schema_identidade_processual(), ensure_ascii=False, indent=2))
        sys.exit(0)

    case_dir = Path(sys.argv[1])

    # Carregar declaração
    decl = carregar_declaracao(case_dir)
    if not decl:
        print(f"✗ Declaração não existe em {case_dir / 'n4_artifacts' / 'F2_IDENTIDADE_PROCESSUAL.json'}")
        sys.exit(1)

    # Carregar manifesto
    manifest_path = case_dir / "FORJA_CASE_MANIFEST.json"
    if not manifest_path.exists():
        print(f"✗ Manifesto não existe em {manifest_path}")
        sys.exit(1)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    # Validar estrutura
    val_struct = validar_declaracao_completa(decl)
    print(f"\n=== Validação de Estrutura ===")
    if val_struct.valida:
        print("✓ Estrutura válida")
    else:
        for erro in val_struct.erros:
            print(f"  {erro}")
    for aviso in val_struct.avisos:
        print(f"  ⚠ {aviso}")

    # Validar lastro
    val_lastro = validar_lastro_de_fonte_externa(decl, manifest, base_dir=case_dir)
    print(f"\n=== Validação de Lastro ===")
    if val_lastro.valida:
        print("✓ Lastro válido")
    else:
        for erro in val_lastro.erros:
            print(f"  {erro}")
    for aviso in val_lastro.avisos:
        print(f"  ⚠ {aviso}")

    print(f"\n=== Declaração ===")
    print(json.dumps(decl, ensure_ascii=False, indent=2))
