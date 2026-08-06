"""Contrato determinístico da subfase F2-A: exploração em 100 perguntas.

O módulo não responde questões jurídicas. Ele cria um andaime adaptável e valida
que o agente examinou o caso por dez óticas, respondeu com proveniência honesta,
explicitou lacunas e entregou cada conclusão às fases seguintes da FORJA.

Artefato canônico: ``F2_QUESTION_TREE.json``.
Protocolo: ``FORJA-F2A-100-v1``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

from forja_n3_common import now_iso
from forja_n4_common import SPEC_VERSION, expected_content_hash
from forja_severidade import blocking_findings, normalized_severity


PROTOCOL_VERSION = "FORJA-F2A-100-v1"
LENSES = (
    "mandato_resultado",
    "fatos_cronologia",
    "prova_fontes",
    "processo_competencia",
    "direito_precedentes",
    "adversario_julgador",
    "riscos_etica_impactos",
    "alternativas_solucoes",
    "quantificacao_execucao",
    "comunicacao_visual_validacao",
)
DOWNSTREAM_PHASES = ("F3", "F4", "F5", "F6", "F7")
STATUSES = {"answered", "blocked", "not_applicable"}
EPISTEMIC_STATUSES = {
    "confirmed_document",
    "confirmed_official_source",
    "office_declaration",
    "legal_inference",
    "strategic_hypothesis",
    "not_verified",
    "not_applicable",
}
FACTUAL_CATEGORIES = {"fact", "evidence", "procedural_event", "precedent", "calculation"}

# ---------------------------------------------------------------------------
# F2-B — consulta dialética ao advogado (FORJA-F2B-DIALECTIC-v1)
#
# A subfase existe porque o titular do escritório determinou que a IA não deve
# "matar no peito e entregar pronto": deve perguntar antes de escrever. A regra
# que torna isso útil em vez de irritante é uma só — não se pergunta o que o
# acervo já responde. Cada pergunta enviada custa atenção de um advogado
# ocupado, e pergunta redundante gasta esse crédito sem devolver decisão.
# ---------------------------------------------------------------------------

DIALECTIC_PROTOCOL = "FORJA-F2B-DIALECTIC-v1"

CONSULTATION_STATUSES = {
    "not_selected", "draft", "awaiting_review", "sent",
    "partially_answered", "answered", "blocked", "not_applicable",
}
QUESTION_TYPES = {"fact", "evidence", "authorization", "objective", "strategy", "presentation"}
HUMAN_AUTHORITIES = {"responsible_lawyer", "client", "office", "titular"}
SILENCE_POLICIES = {
    "block_dependent",            # o silêncio bloqueia o que depende da resposta
    "keep_options_open",          # segue-se sem fechar a escolha
    "explicit_reversible_default",  # adota-se um padrão declarado e reversível
    "not_applicable",
}
# Fato e autorização nunca admitem default: presumir fato é inventar, e presumir
# autorização é agir sem mandato. Ambos ou têm resposta, ou bloqueiam.
TYPES_WITHOUT_DEFAULT = {"fact", "evidence", "authorization"}
RESPONSE_CHANNELS = {"email", "whatsapp", "audio", "meeting", "other"}
CONSULTATION_VOLUME_SOFT_LIMIT = 12


def _selection_rank(question: dict) -> tuple:
    """Ordem determinística das perguntas na consulta.

    Identidade do produto vem primeiro porque erra-se cedo e caro; risco factual
    e de autorização vem em seguida porque bloqueia; e o ID desempata, para que
    duas execuções sobre a mesma árvore produzam a mesma consulta.
    """
    tipo = str(question.get("questionType") or "")
    identidade = 0 if tipo in {"objective", "presentation"} else 1
    risco = 0 if tipo in {"fact", "evidence", "authorization"} else 1
    rota = 0 if tipo == "strategy" else 1
    downstream = -len(question.get("downstreamTargets") or [])
    return (identidade, risco, rota, downstream, str(question.get("questionId") or ""))


def selectable_findings(question: dict) -> list[dict]:
    """Motivos que impedem uma pergunta de ir ao advogado."""
    qid = question.get("questionId")
    achados = []
    if question.get("status") != "blocked":
        achados.append(_issue(
            "FAL-F2B-NOT-BLOCKED",
            f"{qid}: só se pergunta o que está aberto; questão respondida não vai à consulta",
        ))
    if question.get("materiality") not in {"decisive", "material"} and not _norm(
        question.get("selectionReason")
    ):
        achados.append(_issue(
            "FAL-F2B-NO-MATERIALITY",
            f"{qid}: questão não material exige justificativa de seleção",
        ))
    if not _norm(question.get("caseAnchor")) or not _norm(question.get("whyItMatters")):
        achados.append(_issue(
            "FAL-F2B-NO-ANCHOR",
            f"{qid}: pergunta sem âncora do caso ou sem importância declarada",
        ))
    if question.get("alreadyResearched"):
        achados.append(_issue(
            "FAL-F2B-REDUNDANT",
            f"{qid}: o acervo já responde — {', '.join(str(v) for v in question['alreadyResearched'][:3])}",
        ))
    if question.get("humanAuthority") not in HUMAN_AUTHORITIES:
        achados.append(_issue(
            "FAL-F2B-NO-AUTHORITY",
            f"{qid}: pergunta sem autoridade humana competente para respondê-la",
        ))
    politica = question.get("silencePolicy")
    if politica not in SILENCE_POLICIES:
        achados.append(_issue(
            "FAL-F2B-NO-SILENCE-POLICY",
            f"{qid}: pergunta sem política de silêncio declarada",
        ))
    elif not _norm(question.get("silenceConsequence")):
        achados.append(_issue(
            "FAL-F2B-NO-SILENCE-POLICY",
            f"{qid}: política de silêncio sem consequência concreta",
        ))
    if (
        politica == "explicit_reversible_default"
        and str(question.get("questionType") or "") in TYPES_WITHOUT_DEFAULT
    ):
        achados.append(_issue(
            "FAL-F2B-FACT-DEFAULT",
            f"{qid}: fato, prova e autorização não admitem valor padrão; ou há resposta, ou bloqueia",
        ))
    if question.get("questionType") not in QUESTION_TYPES:
        achados.append(_issue("FAL-F2B-NO-TYPE", f"{qid}: pergunta sem tipo declarado"))
    return achados


def select_consultation_questions(payload: dict) -> tuple[list[str], list[dict]]:
    """Escolhe, de forma determinística, o que perguntar ao advogado."""
    elegiveis, achados = [], []
    for question in payload.get("questions") or []:
        if question.get("status") != "blocked":
            continue
        proprios = selectable_findings(question)
        if proprios:
            achados.extend(proprios)
            continue
        elegiveis.append(question)
    selecionadas = [str(q.get("questionId")) for q in sorted(elegiveis, key=_selection_rank)]
    if len(selecionadas) > CONSULTATION_VOLUME_SOFT_LIMIT and not _norm(
        (payload.get("dialecticConsultation") or {}).get("roundJustification")
    ):
        # Não se trunca a lista: cortar perguntas materiais para caber num número
        # é esconder trabalho. Exige-se justificativa da rodada.
        achados.append(_issue(
            "FAL-F2B-QUESTION-VOLUME",
            f"{len(selecionadas)} perguntas acima do limite de conforto "
            f"({CONSULTATION_VOLUME_SOFT_LIMIT}); justifique a rodada ou divida em duas",
            severity="p1",
        ))
    return selecionadas, achados


def validate_dialectic(payload: dict) -> list[dict]:
    """Valida a consulta e o ledger de decisões; ausência do bloco é legítima."""
    consulta = payload.get("dialecticConsultation")
    if consulta is None:
        return []
    achados = []
    if payload.get("dialecticProtocolVersion") != DIALECTIC_PROTOCOL:
        achados.append(_issue(
            "FAL-F2B-PROTOCOL",
            f"protocolo dialético ausente ou divergente; esperado {DIALECTIC_PROTOCOL}",
        ))
    status = consulta.get("status")
    if status not in CONSULTATION_STATUSES:
        achados.append(_issue("FAL-F2B-STATUS", f"status de consulta inválido: {status!r}"))

    # Envio autônomo é proibido na v1: a FORJA prepara, a pessoa autorizada envia.
    if consulta.get("outboundPolicy") != "manual_review_only":
        achados.append(_issue(
            "FAL-F2B-OUTBOUND-UNAUTHORIZED",
            "a consulta só pode sair sob revisão humana; envio autônomo não é autorizado nesta versão",
        ))
    if status in {"sent", "partially_answered", "answered"} and not _norm(
        consulta.get("outboundReceiptId")
    ):
        achados.append(_issue(
            "FAL-F2B-OUTBOUND-UNAUTHORIZED",
            "consulta marcada como enviada sem recibo de envio humano",
        ))

    perguntas = {str(q.get("questionId")): q for q in payload.get("questions") or []}
    for qid in consulta.get("selectedQuestionIds") or []:
        question = perguntas.get(str(qid))
        if question is None:
            achados.append(_issue("FAL-F2B-UNKNOWN-QUESTION", f"{qid}: pergunta selecionada não existe na árvore"))
            continue
        achados.extend(selectable_findings(question))

    vistos = set()
    for entrada in payload.get("decisionLedger") or []:
        decision_id = str(entrada.get("decisionId") or "")
        if not decision_id:
            achados.append(_issue("FAL-F2B-DECISION-NO-ID", "entrada do ledger sem identificador"))
        elif decision_id in vistos:
            achados.append(_issue("FAL-F2B-DECISION-DUPLICATE", f"{decision_id}: decisão repetida no ledger"))
        vistos.add(decision_id)
        if not _norm(entrada.get("responseAuthor")) or entrada.get("channel") not in RESPONSE_CHANNELS:
            achados.append(_issue(
                "FAL-F2B-DECISION-NO-AUTHOR",
                f"{decision_id}: decisão sem autor identificado ou canal válido",
            ))
        epistemico = entrada.get("epistemicStatus")
        if epistemico not in EPISTEMIC_STATUSES:
            achados.append(_issue(
                "FAL-F2B-DECISION-EPISTEMIC",
                f"{decision_id}: natureza epistemológica da resposta ausente ou inválida",
            ))
        # Declaração do escritório é declaração: vale como decisão, não como fato
        # provado. Promovê-la a fato é o modo mais silencioso de inventar.
        if epistemico == "office_declaration":
            alvos = [perguntas.get(str(q)) for q in entrada.get("questionIds") or []]
            factuais = [
                q for q in alvos
                if q and (q.get("questionType") in {"fact", "evidence"}
                          or q.get("category") in FACTUAL_CATEGORIES)
            ]
            if factuais and not (entrada.get("supportIds") or []):
                achados.append(_issue(
                    "FAL-F2B-OFFICE-AS-FACT",
                    f"{decision_id}: declaração do escritório respondendo questão factual sem lastro documental",
                ))

    if status == "partially_answered" and not (payload.get("decisionLedger") or []):
        achados.append(_issue(
            "FAL-F2B-PARTIAL-CLOSED",
            "consulta parcialmente respondida sem nenhuma decisão registrada",
        ))
    if status == "answered":
        respondidas = {
            str(q) for entrada in payload.get("decisionLedger") or []
            for q in entrada.get("questionIds") or []
        }
        pendentes = [
            str(q) for q in consulta.get("selectedQuestionIds") or [] if str(q) not in respondidas
        ]
        if pendentes:
            achados.append(_issue(
                "FAL-F2B-PARTIAL-CLOSED",
                f"consulta dada por respondida com pendências: {', '.join(pendentes[:5])}",
            ))
    return achados

MANDATORY_PROMPT = """
## SUBFASE OBRIGATÓRIA F2-A — EXPLORAÇÃO EM 100 PERGUNTAS

Antes de pesquisa, conselho, blueprint ou redação, leia o inventário, o comando e
os documentos disponíveis. Produza `question_tree` no protocolo
`FORJA-F2A-100-v1`: exatamente 100 perguntas adaptadas ao caso, IDs Q001..Q100,
dez perguntas em cada uma das dez óticas canônicas. Responda todas com âncora do
caso, importância e natureza epistemológica. Fato, evento, precedente ou cálculo
respondido exige `supportIds`; lacuna recebe `blocked`, consequência e diligência,
nunca resposta inventada. Consolide definição do problema, síntese diagnóstica,
ao menos duas hipóteses de solução com condições/riscos, handoff F3-F7 e bloqueio
da redação enquanto houver questão material aberta. Siga integralmente
`_FORJA_HARNESS/templates/F2A_EXPLORACAO_100_PERGUNTAS.md`.
""".strip()


def mandatory_prompt_for_phase(phase: str) -> str:
    return MANDATORY_PROMPT + "\n\n" if str(phase).startswith("F2_") else ""


LENS_RATIONALES = {
    "mandato_resultado": "separa o pedido recebido do resultado jurídico e prático realmente alcançável",
    "fatos_cronologia": "reconstrói o que ocorreu, em que ordem e qual evento muda a conclusão",
    "prova_fontes": "mede o lastro, a proveniência interna e a ponte processual de cada premissa",
    "processo_competencia": "testa veículo, competência, cognição, prazo, rito e identidade dos atos",
    "direito_precedentes": "identifica normas, regimes temporais, precedentes e limites de aplicação",
    "adversario_julgador": "antecipa objeções, incentivos, dúvidas e caminhos decisórios rivais",
    "riscos_etica_impactos": "expõe riscos jurídicos, reputacionais e efeitos colaterais da tese",
    "alternativas_solucoes": "compara intervenções, subsidiárias, reservas, acordos e gatilhos de mudança",
    "quantificacao_execucao": "torna cálculos, recursos, dependências e execução verificáveis",
    "comunicacao_visual_validacao": "projeta compreensão, visual law, testes de aceite e revisão humana",
}


# Dez sementes por ótica. O agente deve reescrevê-las com o ``caseAnchor`` real;
# o andaime nasce bloqueado e nunca é evidência de que a análise foi concluída.
SEEDS = {
    "mandato_resultado": [
        ("mandate", "Qual é o pedido literal recebido e o que ele não autoriza presumir?"),
        ("request", "Qual resultado prático o solicitante espera obter?"),
        ("request", "Qual resultado juridicamente direto esta peça pode produzir?"),
        ("risk", "Há diferença entre a solução pedida e o problema real do caso?"),
        ("mandate", "Quem decide, quem revisa e quem será afetado pela entrega?"),
        ("request", "Quais resultados são principais, subsidiários e apenas desejáveis?"),
        ("risk", "Que premissa do comando pode refletir expectativa, e não fato dos autos?"),
        ("mandate", "Quais limites de escopo, prazo, custo ou exposição foram fixados?"),
        ("request", "Como reconhecer objetivamente que a demanda foi bem atendida?"),
        ("risk", "Que pergunta ao solicitante mudaria materialmente a solução?"),
    ],
    "fatos_cronologia": [
        ("fact", "Quais fatos são incontroversos e quais são apenas alegados?"),
        ("procedural_event", "Qual é a sequência cronológica completa dos eventos decisivos?"),
        ("fact", "Qual fato, se falso, derruba a tese principal?"),
        ("procedural_event", "Qual evento originou a necessidade da peça atual?"),
        ("fact", "Há datas, nomes, valores ou versões incompatíveis entre documentos?"),
        ("procedural_event", "Que eventos estão ausentes entre dois marcos conhecidos?"),
        ("fact", "Quais causas explicam o problema e quais são meros sintomas?"),
        ("procedural_event", "Que ato posterior alterou, confirmou ou superou ato anterior?"),
        ("fact", "Qual é a melhor explicação rival para os mesmos fatos?"),
        ("fact", "Que novo fato faria a narrativa precisar ser reconstruída?"),
    ],
    "prova_fontes": [
        ("evidence", "Qual documento sustenta cada proposição material e em qual localizador?"),
        ("evidence", "A íntegra do ato atualmente impugnado está disponível e autêntica?"),
        ("evidence", "Que documento é mencionado, mas ainda não está nos autos ou não acompanhará a peça?"),
        ("evidence", "Há fonte secundária sendo tratada como se fosse fonte primária?"),
        ("evidence", "Quais documentos têm OCR, páginas, assinatura ou versão duvidosos?"),
        ("evidence", "Qual prova contrária relevante foi localizada e como afeta a tese?"),
        ("evidence", "Que ausência foi indevidamente convertida em prova de inexistência?"),
        ("evidence", "A referência processual externa pode ser usada sem revelar a origem operacional?"),
        ("evidence", "Que fato depende de declaração do escritório ainda não confirmada nos autos?"),
        ("evidence", "Que diligência de prova tem maior valor para reduzir incerteza?"),
    ],
    "processo_competencia": [
        ("jurisdiction", "Qual é o tribunal, órgão e julgador competentes para o ato?"),
        ("procedural_event", "Qual recurso, decisão ou manifestação está exatamente em análise?"),
        ("jurisdiction", "Qual é a pergunta jurisdicional que o julgador pode efetivamente responder?"),
        ("procedural_event", "O veículo processual escolhido é cabível nesta fase e contra este ato?"),
        ("procedural_event", "Qual é o prazo, termo inicial e método independente de contagem?"),
        ("jurisdiction", "Quais limites de cognição impedem examinar parte do mérito ou da prova?"),
        ("procedural_event", "Há preclusão, coisa julgada, prevenção, destaque ou retratação relevante?"),
        ("jurisdiction", "Que regra regimental altera competência, pauta, sustentação ou processamento?"),
        ("procedural_event", "Quais atos homônimos precisam de identificadores para evitar ambiguidade?"),
        ("request", "Os pedidos correspondem ao poder decisório disponível neste momento?"),
    ],
    "direito_precedentes": [
        ("merit", "Quais normas formam a regra jurídica aplicável ao problema central?"),
        ("precedent", "Que precedente é indispensável e foi conferido na fonte oficial?"),
        ("precedent", "O trecho atribuído ao julgado é ratio, dictum, ementa ou paráfrase?"),
        ("merit", "Há mudança legislativa ou regra intertemporal capaz de alterar a conclusão?"),
        ("precedent", "Existe precedente contrário mais próximo dos fatos do caso?"),
        ("merit", "Quais requisitos cumulativos a tese precisa demonstrar?"),
        ("merit", "Que conceito jurídico está sendo usado com mais de um sentido?"),
        ("precedent", "A similitude fática entre o precedente e o caso foi demonstrada ou presumida?"),
        ("merit", "Qual fundamento autônomo poderia manter a decisão mesmo vencida a tese principal?"),
        ("precedent", "Que pesquisa oficial falta para distinguir, confirmar ou abandonar a tese?"),
    ],
    "adversario_julgador": [
        ("opponent_response", "Qual é o melhor argumento da parte contrária, formulado em sua versão mais forte?"),
        ("opponent_response", "Que resposta provável neutraliza a tese principal sem enfrentar todos os fatos?"),
        ("risk", "Qual dúvida um julgador cético terá nos primeiros dois minutos de leitura?"),
        ("risk", "Que caminho decisório permite negar o pedido pelo fundamento mais estreito?"),
        ("opponent_response", "Que contradição ou exagero a parte contrária poderá explorar?"),
        ("risk", "Que pedido pode parecer inútil, inexequível ou excessivo ao julgador?"),
        ("opponent_response", "Que documento adverso precisa ser enfrentado expressamente?"),
        ("risk", "Que incentivo institucional favorece uma solução diferente da pretendida?"),
        ("opponent_response", "O que a peça revela desnecessariamente e pode virar munição contrária?"),
        ("risk", "Qual concessão argumentativa aumentaria credibilidade sem perder o núcleo da tese?"),
    ],
    "riscos_etica_impactos": [
        ("risk", "Qual é o pior dano plausível se a estratégia estiver errada?"),
        ("ethics", "Alguma formulação acusa conduta, intenção ou má-fé sem lastro suficiente?"),
        ("risk", "Que efeito colateral a tese pode produzir em outros recursos ou posições do cliente?"),
        ("ethics", "Há menção a origem operacional — e-mail, WhatsApp, pasta, caminho local — no corpo da peça?"),
        ("risk", "Qual risco reputacional existe para o cliente, escritório ou tese institucional?"),
        ("risk", "Que incerteza precisa ser comunicada ao revisor humano, e não escondida?"),
        ("ethics", "Que premissa a peça assume sem prova nos autos, e o que muda se ela for falsa?"),
        ("risk", "Que consequência prática ocorre se o pedido for acolhido apenas parcialmente?"),
        ("risk", "Há conflito entre ganho imediato e posição jurídica futura?"),
        ("ethics", "Que decisão exige autorização humana por risco jurídico ou negocial?"),
    ],
    "alternativas_solucoes": [
        ("alternative", "Quais são pelo menos duas soluções juridicamente distintas para o problema?"),
        ("alternative", "Que solução atua sobre a causa, e qual apenas trata o sintoma?"),
        ("alternative", "Qual alternativa exige menos premissas não verificadas?"),
        ("request", "Que pedido subsidiário preserva utilidade se a tese principal falhar?"),
        ("alternative", "Há solução extraprocessual, consensual ou operacional superior à peça?"),
        ("alternative", "Que elementos úteis da alternativa rejeitada podem ser incorporados?"),
        ("risk", "Qual é o gatilho verificável para trocar de estratégia?"),
        ("alternative", "Que sequência de intervenções produz o resultado com menor risco?"),
        ("alternative", "A inação ou espera estratégica é uma alternativa legítima neste momento?"),
        ("alternative", "Que experimento, diligência ou minuta interna pode testar a solução antes do protocolo?"),
    ],
    "quantificacao_execucao": [
        ("calculation", "Quais valores, percentuais, datas ou quantidades influenciam a decisão?"),
        ("calculation", "Cada cálculo pode ser reproduzido a partir de entradas e fontes declaradas?"),
        ("execution", "Que documentos, pessoas, sistemas e aprovações são dependências da execução?"),
        ("execution", "Qual é o caminho crítico entre a análise e a entrega utilizável?"),
        ("calculation", "Que cenário mínimo, provável e máximo deve ser comparado?"),
        ("execution", "Que falha operacional pode invalidar uma solução juridicamente correta?"),
        ("calculation", "Quais variáveis são conhecidas, disputadas ou ainda desconhecidas?"),
        ("execution", "Como verificar que anexo, versão e arquivo corretos chegaram ao destino?"),
        ("execution", "Que etapa pode ser automatizada sem substituir decisão jurídica humana?"),
        ("execution", "Qual evidência final demonstrará que a intervenção foi executada?"),
    ],
    "comunicacao_visual_validacao": [
        ("communication", "Qual mensagem o julgador precisa compreender primeiro?"),
        ("communication", "A ordem das seções acompanha a ordem real de decisão?"),
        ("visual", "Que relação complexa merece diagrama e qual função cognitiva ele cumpre?"),
        ("visual", "Que visual poderia criar falsa certeza, escala ou causalidade?"),
        ("communication", "Quais termos canônicos evitam ambiguidade entre atos ou teses?"),
        ("communication", "Que informação deve ficar no relatório interno e nunca na peça?"),
        ("risk", "Quais testes literais devem ser congelados antes da redação final?"),
        ("visual", "Como a leitura página a página revelará overflow, colisão ou hierarquia ruim?"),
        ("communication", "Quais três a seis pontos exigem o olho do revisor humano?"),
        ("risk", "Que evidência provará que a solução final preservou fatos, fontes, pedidos e layout?"),
    ],
}


def _chave_comparavel(valor: object) -> str:
    """Reduz um valor a uma chave de comparação sem nunca levantar exceção.

    A primeira versão usava `json.dumps` direto e isso derrubou o canário de
    mutação em 05/08/2026: um artefato destruído carregava valor não
    serializável, `json.dumps` levantou `TypeError`, e o validador inteiro saiu
    da contagem de gates — 40 examinados viraram 39, 35 reprovando viraram 34.
    O gate ficou cego exatamente no caso em que deveria acusar.

    A lição é geral e vale para qualquer gate desta casa: **a serialização
    auxiliar de uma checagem jamais pode ser capaz de derrubar a checagem**. Aqui
    só interessa distinguir valores entre si; a forma exata da chave é
    irrelevante, e portanto `repr` serve de reserva sem perder nada.
    """
    try:
        return json.dumps(valor, sort_keys=True, ensure_ascii=False)
    except (TypeError, ValueError):
        return repr(valor)


def _issue(code: str, detail: str, severity: str = "p0") -> dict:
    return {"code": code, "severity": severity, "detail": detail}


def _norm(text: object) -> str:
    folded = unicodedata.normalize("NFKD", str(text or "").casefold())
    folded = "".join(char for char in folded if not unicodedata.combining(char))
    return re.sub(r"\W+", " ", folded).strip()


def _texto(value: object) -> str:
    """Texto para leitura humana: preserva acento, caixa e pontuação.

    Existe para não se confundir com `_norm`, que dobra caixa e remove
    diacríticos para efeito de comparação. Usar a normalização na renderização
    entregaria ao advogado um texto mutilado.
    """
    return " ".join(str(value or "").split())


def _placeholder(text: object) -> bool:
    value = _norm(text)
    return bool(re.search(r"\b(?:pendente|preencher|todo)\b|ainda nao respondida|adaptar a pergunta", value))


def build_scaffold(case_id: str, case_anchor: str) -> dict:
    """Cria 100 perguntas-semente bloqueadas; não simula respostas."""
    questions = []
    counter = 0
    for lens in LENSES:
        for category, text in SEEDS[lens]:
            counter += 1
            questions.append({
                "questionId": f"Q{counter:03d}",
                "lens": lens,
                "category": category,
                "text": text,
                "caseAnchor": case_anchor,
                "whyItMatters": LENS_RATIONALES[lens],
                "materiality": "material",
                "status": "blocked",
                "answer": "Ainda não respondida: adaptar a pergunta e examinar as fontes do caso.",
                "epistemicStatus": "not_verified",
                "supportIds": [],
                "unansweredConsequence": "Impede considerar concluída a exploração F2-A.",
                "downstreamTargets": ["F3"],
            })
    stamp = now_iso()
    payload = {
        "schemaVersion": 1,
        "specVersion": SPEC_VERSION,
        "protocolVersion": PROTOCOL_VERSION,
        "caseId": case_id,
        "artifactType": "question_tree",
        "phase": "F2_CLASSIFICACAO_PRODUTO_RISCO",
        "applicability": "required",
        "status": "draft",
        "sourceHashes": [],
        "producerRunId": "f2a-scaffold",
        "reviewerRunId": None,
        "createdAt": stamp,
        "updatedAt": stamp,
        "issues": [],
        "problemDefinition": "PENDENTE: formular a lacuna entre a situação comprovada e o resultado juridicamente alcançável.",
        "diagnosticSynthesis": "PENDENTE: responder e sintetizar as 100 perguntas sem transformar hipótese em fato.",
        "questions": questions,
        "coverage": {
            "total": 100,
            "material": 100,
            "answeredMaterial": 0,
            "blockedMaterial": 100,
            "perLens": {lens: 10 for lens in LENSES},
        },
        "solutionHypotheses": [
            {"hypothesisId": "H01", "description": "PENDENTE", "conditions": ["PENDENTE"], "risks": ["PENDENTE"], "questionIds": ["Q001"], "downstreamTargets": ["F4"]},
            {"hypothesisId": "H02", "description": "PENDENTE", "conditions": ["PENDENTE"], "risks": ["PENDENTE"], "questionIds": ["Q002"], "downstreamTargets": ["F4"]},
        ],
        "downstreamHandoff": {phase: ["Q001"] for phase in DOWNSTREAM_PHASES},
        "openDecisiveQuestions": [],
        "draftRelease": "blocked",
    }
    payload["contentHash"] = expected_content_hash(payload)
    return payload


def validate_exploration_100(payload: dict, *, require_protocol: bool = True) -> list[dict]:
    findings: list[dict] = []
    protocol = payload.get("protocolVersion")
    if require_protocol and protocol != PROTOCOL_VERSION:
        findings.append(_issue("N4-Q-100-PROTOCOL", f"protocolVersion deve ser {PROTOCOL_VERSION}"))
    if protocol not in {None, PROTOCOL_VERSION}:
        findings.append(_issue("N4-Q-100-PROTOCOL", f"protocolo desconhecido: {protocol}"))

    questions = payload.get("questions") or []
    if len(questions) != 100:
        findings.append(_issue("N4-Q-100-COUNT", f"a exploração exige exatamente 100 perguntas; recebeu {len(questions)}"))

    ids = [str(item.get("questionId") or "") for item in questions]
    expected_ids = [f"Q{i:03d}" for i in range(1, 101)]
    if len(questions) == 100 and ids != expected_ids:
        findings.append(_issue("N4-Q-100-IDS", "questionId deve formar a sequência estável Q001..Q100"))

    lens_counts = Counter(str(item.get("lens") or "") for item in questions)
    for lens in LENSES:
        if lens_counts[lens] != 10:
            findings.append(_issue("N4-Q-100-LENS", f"ótica {lens} deve ter 10 perguntas; recebeu {lens_counts[lens]}"))
    unknown_lenses = sorted(set(lens_counts) - set(LENSES) - {""})
    if unknown_lenses:
        findings.append(_issue("N4-Q-100-LENS", f"óticas desconhecidas: {', '.join(unknown_lenses)}"))

    normalized_texts = [_norm(item.get("text")) for item in questions]
    if len(set(normalized_texts)) != len(normalized_texts):
        findings.append(_issue("N4-Q-100-DUPLICATE", "há perguntas repetidas; quantidade não substitui diversidade"))

    # Diversidade dos campos que carregam o pensamento, e não só do enunciado.
    #
    # A checagem de duplicidade acima já tinha o instinto certo — "quantidade não
    # substitui diversidade" — mas olhava apenas `text`. Cem perguntas distintas
    # podem carregar a mesma âncora, a mesma consequência e o mesmo roteamento,
    # e foi exatamente isso que aconteceu: medido em 05/08/2026 nas 14 árvores do
    # acervo com este protocolo, `unansweredConsequence` tem de 0 a 8 valores
    # distintos entre 100 perguntas, `caseAnchor` tem 1 ou 10, `downstreamTargets`
    # tem de 1 a 5. As 14 condições estruturais que este validador confere são
    # todas satisfeitas por formulário bem preenchido.
    #
    # O piso é 10 valores distintos em 100 — a razão de 0,10 que o padrão
    # "um por ótica" já alcança. Não é limiar inventado: é o teto observado no
    # acervo inteiro, e portanto o menor patamar que não reprova o melhor que a
    # casa já produziu.
    #
    # **Severidade P1, deliberadamente.** Com este piso as 14 árvores existentes
    # seriam acusadas, e não por engano — elas são formulário. Mas promover a P0
    # hoje pararia o F2A amanhã, sem que exista uma única árvore boa para servir
    # de âncora de calibração. Nesta casa trava inexequível vira waiver diário e
    # contamina a confiança nos outros gates. A promoção a P0 fica condicionada a
    # existir ao menos uma árvore de exploração real aprovada pelo dono.
    # O piso acompanha os graus de liberdade do campo, e não um número único.
    # A primeira versão aplicava 10 valores distintos a todos os quatro campos, e
    # o próprio controle benigno da suíte a reprovou: `downstreamTargets` sai de
    # vocabulário fechado de cinco fases (F3..F7), de modo que exigir dez valores
    # distintos ali é impossível por construção — seria trava inexequível criada
    # no mesmo ato que pretendia impedi-las. Campo de texto livre admite piso de
    # um décimo; campo de vocabulário fechado admite apenas a exigência de que
    # nem tudo seja roteado do mesmo jeito.
    if len(questions) >= 10:
        piso_livre = max(2, len(questions) // 10)
        pisos = {
            "caseAnchor": piso_livre,
            "whyItMatters": piso_livre,
            "unansweredConsequence": piso_livre,
            "downstreamTargets": 2,
        }
        pobres = []
        for campo, piso in pisos.items():
            distintos = {
                _chave_comparavel(item.get(campo))
                for item in questions
                if isinstance(item, dict) and item.get(campo) not in (None, "", [], {})
            }
            if len(distintos) < piso:
                pobres.append(f"{campo}={len(distintos)} (piso {piso})")
        if pobres:
            findings.append(_issue(
                "N4-Q-100-DIVERSITY",
                f"campos repetidos entre {len(questions)} perguntas: "
                f"{', '.join(pobres)}; exploração preenchida por repetição não é "
                "exploração",
                severity="p1"))

    # Exploração sem nenhuma lacuna declarada é implausível — e desliga a única
    # checagem que cobraria consequência.
    #
    # `unansweredConsequence` só é exigido quando `status == "blocked"` (adiante,
    # em N4-Q-NO-CONSEQUENCE). Como quem produz a árvore também escolhe o status,
    # declarar as 100 como `answered` isenta o produtor do único campo que o
    # obrigaria a dizer o que se perde por não saber. A precondição da checagem
    # está nas mãos de quem ela deveria conferir, e foi assim que o campo ficou
    # vazio em 8 das 14 árvores sem que nada acusasse.
    # O `isinstance` aqui não é defensivo por hábito: sem ele o canário de mutação
    # cai de 40 gates examinados para 39. Um artefato destruído traz `questions`
    # com itens que não são dicionário, `item.get` levanta AttributeError, e o
    # validador inteiro some da contagem — isto é, o gate fica CEGO exatamente no
    # caso em que ele mais precisa acusar. Foi assim que esta checagem, escrita
    # para melhorar o F2A, quebrou a catraca em 05/08/2026. O canário pegou.
    if len(questions) >= 10:
        bloqueadas = sum(1 for item in questions
                         if isinstance(item, dict) and item.get("status") == "blocked")
        if bloqueadas == 0:
            findings.append(_issue(
                "N4-Q-100-NO-GAP",
                f"nenhuma das {len(questions)} perguntas ficou bloqueada; um caso "
                "real raramente responde tudo, e sem lacuna a consequência da "
                "lacuna nunca é cobrada",
                severity="p1"))

    blocked_decisive: list[str] = []
    for item in questions:
        qid = str(item.get("questionId") or "?")
        for key in ("text", "caseAnchor", "whyItMatters", "answer"):
            if len(str(item.get(key) or "").strip()) < 12:
                findings.append(_issue("N4-Q-100-DEPTH", f"{qid}: {key} ausente ou superficial"))
            if _placeholder(item.get(key)):
                findings.append(_issue("N4-Q-100-PLACEHOLDER", f"{qid}: {key} ainda contém marcador de andaime"))
        if item.get("status") not in STATUSES:
            findings.append(_issue("N4-Q-100-STATUS", f"{qid}: status inválido"))
        epistemic = item.get("epistemicStatus")
        if epistemic not in EPISTEMIC_STATUSES:
            findings.append(_issue("N4-Q-100-EPISTEMIC", f"{qid}: natureza epistemológica inválida"))
        if item.get("status") == "answered" and item.get("category") in FACTUAL_CATEGORIES and not item.get("supportIds"):
            findings.append(_issue("N4-Q-NO-SUPPORT", f"{qid}: resposta factual, processual, jurisprudencial ou numérica sem lastro"))
        if item.get("status") == "answered" and epistemic == "not_verified":
            findings.append(_issue("N4-Q-100-ANSWER-NOT-VERIFIED", f"{qid}: não verificado não pode ser declarado respondido"))
        if item.get("status") == "blocked":
            if not str(item.get("unansweredConsequence") or "").strip():
                findings.append(_issue("N4-Q-NO-CONSEQUENCE", f"{qid}: lacuna sem consequência explícita"))
            if item.get("materiality") == "decisive":
                blocked_decisive.append(qid)
        if item.get("status") == "not_applicable":
            if epistemic != "not_applicable" or not str(item.get("notApplicableReason") or "").strip():
                findings.append(_issue("N4-Q-100-NA", f"{qid}: não aplicabilidade sem classificação e razão"))
        targets = item.get("downstreamTargets") or []
        if not targets or any(target not in DOWNSTREAM_PHASES for target in targets):
            findings.append(_issue("N4-Q-100-ROUTE", f"{qid}: roteamento ausente ou inválido"))

    coverage = payload.get("coverage") or {}
    material = sum(item.get("materiality") in {"decisive", "material"} for item in questions)
    answered_material = sum(item.get("materiality") in {"decisive", "material"} and item.get("status") == "answered" for item in questions)
    blocked_material = sum(item.get("materiality") in {"decisive", "material"} and item.get("status") == "blocked" for item in questions)
    actual = {"total": len(questions), "material": material, "answeredMaterial": answered_material, "blockedMaterial": blocked_material}
    for key, value in actual.items():
        if coverage.get(key) != value:
            findings.append(_issue("N4-Q-COUNT", f"coverage.{key}={coverage.get(key)!r}; calculado={value}"))
    if coverage.get("perLens") != {lens: lens_counts[lens] for lens in LENSES}:
        findings.append(_issue("N4-Q-100-COVERAGE", "coverage.perLens não corresponde às perguntas"))

    if len(str(payload.get("problemDefinition") or "").strip()) < 40 or _placeholder(payload.get("problemDefinition")):
        findings.append(_issue("N4-Q-100-PROBLEM", "definição do problema ausente ou superficial"))
    if len(str(payload.get("diagnosticSynthesis") or "").strip()) < 80 or _placeholder(payload.get("diagnosticSynthesis")):
        findings.append(_issue("N4-Q-100-DIAGNOSIS", "síntese diagnóstica ausente ou superficial"))

    hypotheses = payload.get("solutionHypotheses") or []
    if len(hypotheses) < 2:
        findings.append(_issue("N4-Q-100-SOLUTIONS", "comparar pelo menos duas hipóteses de solução"))
    for hypothesis in hypotheses:
        hid = str(hypothesis.get("hypothesisId") or "?")
        if not str(hypothesis.get("description") or "").strip() or _placeholder(hypothesis.get("description")) or not hypothesis.get("conditions") or not hypothesis.get("risks"):
            findings.append(_issue("N4-Q-100-SOLUTION-DEPTH", f"{hid}: solução sem descrição, condições ou riscos"))
        if not hypothesis.get("questionIds") or any(qid not in ids for qid in hypothesis.get("questionIds") or []):
            findings.append(_issue("N4-Q-100-SOLUTION-LINK", f"{hid}: solução não ligada a perguntas válidas"))

    handoff = payload.get("downstreamHandoff") or {}
    for phase in DOWNSTREAM_PHASES:
        routed = handoff.get(phase) or []
        if not routed or any(qid not in ids for qid in routed):
            findings.append(_issue("N4-Q-100-HANDOFF", f"{phase}: passagem ausente ou aponta para pergunta inexistente"))

    declared_open = sorted(payload.get("openDecisiveQuestions") or [])
    if declared_open != sorted(blocked_decisive):
        findings.append(_issue("N4-Q-100-OPEN-DECISIVE", "openDecisiveQuestions não corresponde às questões decisivas bloqueadas"))
    expected_release = "blocked" if blocked_material else "ready_for_drafting"
    if payload.get("draftRelease") != expected_release:
        findings.append(_issue("N4-Q-100-RELEASE", f"draftRelease deve ser {expected_release}"))
    return findings


# ---------------------------------------------------------------------------
# Gates computados da F2 a partir do validador acima
# ---------------------------------------------------------------------------
# `exploration_100_complete`, `answers_provenance_classified` e
# `downstream_handoff_ready` eram escritos pelo agente da F2 — oito execuções,
# oito `pass` — enquanto ESTE validador, chamado na mesma rota desde a ordem de
# 14/07/2026, já computava tudo o que os três afirmam. O gate existia, a
# capacidade existia, e faltava só ligar um nome ao outro.
#
# Nenhum limiar novo nasce aqui. Cada gate é a ausência dos achados que já
# significam a sua violação, e o mapa abaixo é a única decisão: qual código de
# achado pertence a qual afirmação. Códigos não mapeados caem no gate de
# completude, que é o mais abrangente — assim um achado novo nunca fica órfão e
# aprovado por omissão.
_GATES_EXPLORACAO = {
    # A exploração aconteceu: 100 perguntas, dez por ótica, sem repetição,
    # com profundidade, cobertura conferida, problema, diagnóstico e soluções.
    "exploration_100_complete": {
        "N4-Q-100-PROTOCOL", "N4-Q-100-COUNT", "N4-Q-100-IDS", "N4-Q-100-LENS",
        "N4-Q-100-DUPLICATE", "N4-Q-100-DEPTH", "N4-Q-100-PLACEHOLDER",
        "N4-Q-100-COVERAGE", "N4-Q-COUNT", "N4-Q-100-PROBLEM", "N4-Q-100-DIAGNOSIS",
        "N4-Q-100-SOLUTIONS", "N4-Q-100-SOLUTION-DEPTH", "N4-Q-100-SOLUTION-LINK",
    },
    # Cada resposta declara a sua natureza epistemológica e, sendo factual,
    # o seu lastro. Lacuna não é resposta: fica bloqueada, com consequência.
    "answers_provenance_classified": {
        "N4-Q-100-EPISTEMIC", "N4-Q-100-STATUS", "N4-Q-NO-SUPPORT",
        "N4-Q-100-ANSWER-NOT-VERIFIED", "N4-Q-NO-CONSEQUENCE", "N4-Q-100-NA",
        "N4-Q-100-OPEN-DECISIVE", "N4-Q-100-RELEASE",
    },
    # A passagem para F3-F7 existe e aponta para perguntas que existem.
    "downstream_handoff_ready": {
        "N4-Q-100-ROUTE", "N4-Q-100-HANDOFF",
    },
}


def gates_da_exploracao(payload: dict, *, require_protocol: bool = True) -> dict:
    """Nomeia, como gates do contrato F2, o que `validate_exploration_100` computa."""
    findings = validate_exploration_100(payload or {}, require_protocol=require_protocol)
    codigos = {str(item.get("code") or "") for item in findings}
    by_code = {}
    for item in findings:
        code = str(item.get("code") or "")
        # Se o mesmo código aparecer com severidades distintas, a ocorrência
        # mais severa prevalece. A decisão é por ocorrência, não por catálogo.
        if normalized_severity(item) == "p0" or code not in by_code:
            by_code[code] = item
    mapeados = set().union(*_GATES_EXPLORACAO.values())
    nao_mapeados = codigos - mapeados

    gates = {}
    for gate, seus_codigos in _GATES_EXPLORACAO.items():
        atingido = any(
            code in seus_codigos and normalized_severity(by_code.get(code)) == "p0"
            for code in codigos
        )
        if gate == "exploration_100_complete":
            # Código novo não pode desaparecer. Porém, durante a calibração, um
            # achado P1 continua sendo informação e não se transforma em P0 só
            # porque ainda não entrou no mapa de gates.
            atingido = atingido or any(
                code in nao_mapeados and normalized_severity(by_code.get(code)) == "p0"
                for code in nao_mapeados
            )
        gates[gate] = "fail" if atingido else "pass"
    return {"versao": PROTOCOL_VERSION, "findings": findings, "gates": gates,
            "codigosNaoMapeados": sorted(nao_mapeados),
            "blockingFindings": blocking_findings(findings)}


_ROTULO_TIPO = {
    "objective": "Objetivo e resultado esperado",
    "presentation": "Forma de apresentação",
    "fact": "Fatos",
    "evidence": "Prova e documentos",
    "authorization": "Autorização",
    "strategy": "Estratégia",
}
_ROTULO_AUTORIDADE = {
    "responsible_lawyer": "advogado responsável",
    "client": "cliente",
    "office": "escritório",
    "titular": "titular",
}


def render_consultation(payload: dict, *, template: Path | None = None) -> str:
    """Compõe a consulta em Markdown a partir das perguntas selecionadas.

    O renderizador não responde, não reordena por conveniência e não inclui o
    que não foi selecionado. Ele também não esconde o que ficou de fora: a
    seção final nomeia as perguntas descartadas e o motivo, para que a pessoa
    que revisa possa discordar da triagem.
    """
    consulta = payload.get("dialecticConsultation") or {}
    selecionadas = [str(v) for v in consulta.get("selectedQuestionIds") or []]
    if not selecionadas:
        raise ValueError("nenhuma pergunta selecionada; não há consulta a renderizar")
    perguntas = {str(q.get("questionId")): q for q in payload.get("questions") or []}

    faltando = [qid for qid in selecionadas if qid not in perguntas]
    if faltando:
        raise ValueError(f"perguntas selecionadas ausentes da árvore: {', '.join(faltando)}")
    sem_consequencia = [
        qid for qid in selecionadas if not _norm(perguntas[qid].get("silenceConsequence"))
    ]
    if sem_consequencia:
        raise ValueError(
            "recusa de renderização: pergunta sem consequência declarada — "
            + ", ".join(sem_consequencia)
        )

    ordenadas = sorted((perguntas[qid] for qid in selecionadas), key=_selection_rank)
    blocos, consequencias = [], []
    for indice, question in enumerate(ordenadas, start=1):
        rotulo = _ROTULO_TIPO.get(str(question.get("questionType")), "Ponto em aberto")
        autoridade = _ROTULO_AUTORIDADE.get(str(question.get("humanAuthority")), "responsável")
        blocos.append(
            f"## {indice}. {rotulo}\n\n"
            f"{_texto(question.get('text'))}\n\n"
            f"**Por que decide:** {_texto(question.get('whyItMatters'))}\n\n"
            f"**No caso:** {_texto(question.get('caseAnchor'))}\n\n"
            f"*Quem pode responder: {autoridade}.*"
        )
        consequencias.append(f"{indice}. {_texto(question.get('silenceConsequence'))}")

    descartadas = [
        q for q in payload.get("questions") or []
        if q.get("status") == "blocked" and str(q.get("questionId")) not in selecionadas
    ]
    if descartadas:
        linhas = []
        for question in descartadas[:8]:
            motivos = selectable_findings(question)
            razao = motivos[0]["detail"].split(": ", 1)[-1] if motivos else "não selecionada nesta rodada"
            linhas.append(f"- {question.get('questionId')}: {razao}")
        omitidas = (
            "Estas ficaram de fora da rodada, e o motivo está declarado para que "
            "o senhor possa discordar da triagem:\n\n" + "\n".join(linhas)
        )
    else:
        omitidas = "Nenhuma outra questão aberta ficou de fora desta rodada."

    caminho = template or (Path(__file__).resolve().parent / "templates" / "F2_CONSULTA_ADVOGADO.md")
    modelo = caminho.read_text(encoding="utf-8")
    return modelo.format(
        caseId=payload.get("caseId") or "caso não identificado",
        round=consulta.get("round") or 1,
        generatedAt=consulta.get("preparedAt") or "",
        intro=_texto(payload.get("problemDefinition"))[:600]
        or "Segue o que preciso decidir com o senhor antes de escrever.",
        blocos="\n\n".join(blocos),
        consequencias="\n".join(consequencias),
        omitidas=omitidas,
    )


def record_response(payload: dict, entry: dict) -> dict:
    """Acrescenta uma decisão ao ledger sem reescrever o que já estava lá.

    O ledger é append-only por desenho: uma decisão registrada é o rastro de que
    alguém respondeu algo em determinado dia. Corrigir apagando destrói a trilha;
    corrigir é acrescentar nova entrada.
    """
    ledger = list(payload.get("decisionLedger") or [])
    decision_id = str(entry.get("decisionId") or "")
    if not decision_id:
        raise ValueError("decisão sem decisionId")
    if any(str(item.get("decisionId")) == decision_id for item in ledger):
        raise ValueError(f"decisão já registrada: {decision_id}; o ledger não é reescrito")
    ledger.append(entry)

    atualizado = {**payload, "decisionLedger": ledger}
    consulta = dict(atualizado.get("dialecticConsultation") or {})
    selecionadas = {str(v) for v in consulta.get("selectedQuestionIds") or []}
    respondidas = {
        str(q) for item in ledger for q in item.get("questionIds") or []
    }
    if selecionadas:
        pendentes = selecionadas - respondidas
        consulta["status"] = "answered" if not pendentes else "partially_answered"
        consulta["remainingQuestionIds"] = sorted(pendentes)
    atualizado["dialecticConsultation"] = consulta
    return atualizado


def main() -> int:
    parser = argparse.ArgumentParser(description="Inicializa ou valida a exploração F2-A em 100 perguntas")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--case-id", required=True)
    init.add_argument("--case-anchor", required=True)
    init.add_argument("--output", type=Path, required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("path", type=Path)
    select = sub.add_parser("select-consultation", help="escolhe deterministicamente o que perguntar")
    select.add_argument("path", type=Path)
    render = sub.add_parser("render-consultation", help="compõe a consulta em Markdown")
    render.add_argument("path", type=Path)
    render.add_argument("--output", type=Path, required=True)
    record = sub.add_parser("record-response", help="acrescenta uma decisão ao ledger")
    record.add_argument("path", type=Path)
    record.add_argument("--response", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "init":
        args.output.write_text(json.dumps(build_scaffold(args.case_id, args.case_anchor), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(args.output)
        return 0

    payload = json.loads(args.path.read_text(encoding="utf-8-sig"))

    if args.command == "select-consultation":
        selecionadas, achados = select_consultation_questions(payload)
        print(json.dumps(
            {"selectedQuestionIds": selecionadas, "findings": achados},
            ensure_ascii=False, indent=2,
        ))
        return 1 if blocking_findings(achados) else 0

    if args.command == "render-consultation":
        texto = render_consultation(payload)
        args.output.write_text(texto, encoding="utf-8")
        digest = hashlib.sha256(texto.encode("utf-8")).hexdigest()
        # O hash é gravado no artefato para que a mensagem revisada e a
        # renderização registrada sejam comprovadamente o mesmo texto.
        consulta = dict(payload.get("dialecticConsultation") or {})
        consulta["renderedBodySha256"] = digest
        payload["dialecticConsultation"] = consulta
        args.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"output": str(args.output), "renderedBodySha256": digest}, ensure_ascii=False))
        return 0

    if args.command == "record-response":
        entrada = json.loads(args.response.read_text(encoding="utf-8-sig"))
        atualizado = record_response(payload, entrada)
        args.path.write_text(json.dumps(atualizado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        achados = validate_dialectic(atualizado)
        print(json.dumps({
            "status": (atualizado.get("dialecticConsultation") or {}).get("status"),
            "findings": achados,
        }, ensure_ascii=False, indent=2))
        return 1 if blocking_findings(achados) else 0

    findings = validate_exploration_100(payload) + validate_dialectic(payload)
    blocking = blocking_findings(findings)
    print(json.dumps({"approved": not blocking, "findings": findings}, ensure_ascii=False, indent=2))
    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
