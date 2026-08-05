from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "_FORJA_HARNESS"))
from forja_n4_common import expected_content_hash  # noqa: E402


CASES = [
    {
        "slug": "ESTRE",
        "folder": ROOT
        / "PRAZO 03 8 - Elaboração de memoriais – ED no AI nº 5004634-21.2026.4.03.0000 - ESTRE AMBIENTAL X TRANSPETRO",
        "process": "5004634-21.2026.4.03.0000",
        "party": "Estre Ambiental S.A.",
        "judgment_id": "378294201",
        "distinctive": (
            "Os embargos afirmam que a Estre não participou da licitação "
            "006.8.009.10.0 nem construiu embarcações; a imputação descrita é de "
            "benefício indireto, o que exige correlação própria com a prova técnica."
        ),
        "ed_glob": "e-protocolo PJE ED no AI 5004634*.pdf",
        "appeal_glob": "2 - Recurso de Agravo de Instrumento*.pdf",
        "judgment_glob": "6 - ACÓRDÃO AI 5004634*.pdf",
    },
    {
        "slug": "ERM",
        "folder": ROOT
        / "PRAZO 03 08 - Elaboração de memoriais – ED no AI nº 5004633-36.2026.4.02.0000 - ERM OSV CONSTRUCAO NAVAL X TRA",
        "process": "5004633-36.2026.4.03.0000",
        "party": "ERM OSV Construção Naval Ltda. e outros",
        "judgment_id": "378294200",
        "distinctive": (
            "Os embargos sustentam que a complexidade contratual não identifica, "
            "sem individualização, a lacuna probatória nem a utilidade de cada "
            "perícia naval ou contábil diante do acervo CGU/TCU."
        ),
        "ed_glob": "e-protocolo PJE ED no AI 5004633*.pdf",
        "appeal_glob": "2 - Recurso de Agravo Instrumento*.pdf",
        "judgment_glob": "6 - ACÓRDÃO - AI 5004633*.pdf",
    },
]


ANSWERS = {
    "mandato_resultado": [
        "O mandato é preparar memoriais internos em apoio aos embargos de declaração da Transpetro; não autoriza criar fatos, ampliar pedidos, protocolar ou enviar a destinatário externo.",
        "O resultado prático esperado é permitir leitura rápida das omissões decisivas e oferecer à Turma uma ordem objetiva de integração do acórdão.",
        "A peça pode obter pronunciamento integrativo e, se o saneamento retirar premissa do resultado, efeitos modificativos; não pode substituir a instrução nem provar sozinha fatos controvertidos.",
        "A solução pedida é o acolhimento dos embargos, mas o problema real é a ausência de correlação explícita entre cabimento, lacuna probatória, especialidade da perícia e imputação individual.",
        "A 4ª Turma do TRF3 decide, a Desembargadora Federal Mônica Nobre relata e o escritório revisa; partes e instrução da ação originária serão afetadas.",
        "Principal: suprir omissões. Consequencial: não conhecer ou negar provimento ao agravo. Subsidiário: delimitar objeto, metodologia, período, data-base, acesso e sigilo da prova.",
        "Valores, duração provável e suficiência do acervo são alegações documentadas nos embargos, não constatações técnicas independentes.",
        "O escopo é interno, com prazo do expediente, uso exclusivo do acervo recebido e fontes oficiais; envio externo e protocolo permanecem fora da autorização.",
        "A demanda estará atendida quando houver memorial fiel ao recurso, revisão cruzada, validação formal e visual, e entrega interna com recibo verificável.",
        "A única pergunta capaz de alterar materialmente a solução seria a existência de nova ordem ou documento processual posterior; nenhum foi identificado no acervo fechado desta execução.",
    ],
    "fatos_cronologia": [
        "São documentados a ação de origem, o agravo, o acórdão e os embargos. Necessidade, custo e resultado futuro das perícias permanecem controvertidos; os valores econômicos são alegações dos embargos.",
        "A sequência relevante é ação de improbidade de 2014, decisão probatória de origem, agravo de instrumento, acórdão que determinou prova técnica e embargos de declaração da Transpetro.",
        "A tese perde força se o acórdão já tiver respondido de forma individualizada à urgência, à lacuna probatória, à natureza do acervo oficial e à utilidade de cada perícia; a leitura comparada não mostrou isso.",
        "O evento que gerou a peça foi a oposição de embargos contra o acórdão que deu provimento ao agravo e determinou o prosseguimento da instrução com prova técnica.",
        "O número correto do processo termina em 4.03.0000; a menção 4.02.0000 no nome da pasta ERM é erro operacional. Valores e estimativas são preservados como alegações do recurso.",
        "Não foi localizado marco processual posterior aos embargos no acervo. Por isso o memorial não presume decisão, intimação ou fato superveniente.",
        "A causa processual é a falta de resposta individualizada a fundamentos autônomos; complexidade e custo são elementos de ponderação, não substitutos dessa omissão.",
        "O acórdão superou a decisão de origem ao determinar a prova técnica; os embargos são o ato posterior que pede integração desse julgamento.",
        "A explicação rival mais forte é que a complexidade da causa e o microssistema coletivo justificam recorribilidade imediata e instrução ampla; ela é enfrentada sem negar abstratamente esses pontos.",
        "Nova decisão, novo laudo ou documento que demonstre lacuna técnica concreta exigiria reconstrução da narrativa e eventual revisão dos pedidos.",
    ],
    "prova_fontes": [
        "As proposições materiais são vinculadas à decisão agravada, ao agravo, às contrarrazões, ao acórdão e aos embargos, com identificação nominal dos PDFs no ledger interno.",
        "A íntegra do ato impugnado está no PDF oficial do acórdão juntado ao conjunto recebido e foi conferida em texto e imagem.",
        "Os relatórios CGU e acórdãos TCU são mencionados nos embargos, mas suas íntegras autônomas não integram o pacote; a peça limita-se a registrar a indicação feita no recurso.",
        "Nenhuma notícia ou resumo foi tratado como fonte primária. Regimento, acórdão e peças processuais foram separados de inferências estratégicas.",
        "O OCR é trilha auxiliar e foi marcado como tal; os PDFs nativos com texto, hashes e imagens de conferência permanecem as fontes canônicas.",
        "A prova contrária relevante é o próprio acórdão, que reconhece complexidade e defere a prova; a resposta exige demonstrar a falta de correlação individual, não negar o conteúdo do julgamento.",
        "A ausência de fato novo ou lacuna identificada no acórdão não foi convertida em inexistência absoluta de prova possível; foi formulada como dever de explicitação.",
        "A peça usa apenas referências processuais, como acórdão, decisão, embargos e atos oficiais, sem mencionar e-mail, pasta local ou origem operacional.",
        "Nenhum fato material depende apenas de declaração informal do escritório; data de entrega e destinatário interno ficam no ledger operacional, fora da peça.",
        "A diligência probatória de maior valor seria obter a íntegra autônoma dos relatórios CGU/TCU e eventual decisão posterior, mas isso não impede memoriais fiéis ao conteúdo expressamente transcrito nos embargos.",
    ],
    "processo_competencia": [
        "O ato é dirigido à 4ª Turma do TRF3, sob relatoria da Desembargadora Federal Mônica Nobre, no agravo identificado no cabeçalho.",
        "Estão em análise os embargos de declaração da Transpetro contra o acórdão de ID indicado, e não o agravo ou a decisão de origem de forma indistinta.",
        "A pergunta jurisdicional é se o acórdão contém omissão, contradição ou obscuridade sobre fundamentos decisivos e quais consequências decorrem do saneamento.",
        "Os embargos são cabíveis para integração nos termos dos arts. 262 a 264 do Regimento Interno do TRF3; efeitos modificativos são tratados como consequência, não pedido autônomo de rejulgamento.",
        "O pacote recebido já contém embargos opostos; os memoriais não inauguram prazo recursal nem fazem cálculo autônomo de tempestividade.",
        "O julgamento não deve transformar embargos em nova instrução probatória; limita-se à integração do acórdão e à delimitação do comando já proferido.",
        "Não foi identificada coisa julgada, retratação ou destaque superveniente no acervo; a decisão de origem e o acórdão são individualizados para evitar preclusão narrativa.",
        "O Regimento consolidado até a Emenda Regimental 25/2026 confirma disciplina dos embargos nos arts. 262 a 264 e sua apresentação em mesa pelo relator.",
        "Os atos homônimos são nomeados como decisão de origem, agravo de instrumento, acórdão embargado e embargos de declaração, sempre com número ou ID.",
        "Os pedidos cabem no poder integrativo da Turma: sanar vícios, atribuir consequência necessária e, subsidiariamente, tornar executável a prova deferida.",
    ],
    "direito_precedentes": [
        "A matriz normativa indicada no recurso inclui CPC, Lei da Ação Popular, Lei de Improbidade e Regimento Interno do TRF3, aplicada ao cabimento, fundamentação e prova.",
        "O precedente central é o Tema 988 do STJ, usado para a urgência decorrente da inutilidade do exame posterior; a peça não acrescenta precedente não conferido no acervo.",
        "A formulação sobre o Tema 988 é uma síntese da tese repetitiva, não citação literal nem ampliação de sua ratio.",
        "A Lei 14.230/2021 é tratada como alteração normativa posterior à narrativa de 2014, sem presumir que tenha criado fatos novos.",
        "O argumento contrário mais próximo é a recorribilidade imediata pelo art. 19, parágrafo 1º, da Lei da Ação Popular aplicado ao microssistema coletivo; ele é enfrentado expressamente.",
        "A tese exige omissão relevante, fundamento previamente devolvido, aptidão para alterar o resultado e consequência compatível com o caráter integrativo.",
        "Complexidade técnica, necessidade da prova, pertinência e utilidade são conceitos distintos e são usados separadamente.",
        "A similitude com o Tema 988 é jurídica e limitada ao requisito de urgência; não se presume identidade fática com o caso paradigma.",
        "Mesmo afastada a tese de cabimento, o acórdão poderia ser mantido pela proteção ampla à prova na LIA; por isso a peça enfrenta utilidade, acervo existente e delimitação.",
        "Pesquisa oficial adicional só seria necessária para inserir novo precedente; a versão final evita essa expansão e permanece vinculada aos fundamentos já articulados.",
    ],
    "adversario_julgador": [
        "O melhor argumento contrário é que a complexidade dos contratos, a ampla defesa e o microssistema coletivo justificam recorribilidade e prova técnica ampla.",
        "A resposta mais provável é que o acórdão já fundamentou suficientemente ao reconhecer a complexidade; por isso o memorial exige correlação concreta, não volume argumentativo.",
        "A dúvida inicial do julgador será se os embargos apenas repetem o agravo; a abertura esclarece que o pedido é integrativo e enumera omissões autônomas.",
        "O caminho estreito para rejeição é considerar inexistente omissão relevante ou entender que a analogia legal resolve integralmente o cabimento.",
        "Exagero evitado: não se afirma que auditorias oficiais substituem necessariamente toda perícia, apenas que não podem ser tratadas como pareceres unilaterais sem exame.",
        "O pedido de efeitos modificativos poderia parecer excessivo; ele foi condicionado ao saneamento de omissão capaz de retirar a premissa do resultado.",
        "O documento adverso central é o acórdão embargado, cuja fundamentação e dispositivo são enfrentados diretamente.",
        "Há incentivo institucional à instrução ampla em ação de improbidade; a estratégia responde com pertinência, proporcionalidade e executabilidade, sem pedir supressão abstrata de prova.",
        "A peça exclui origem operacional, mensagens, hipóteses internas e dados não necessários, reduzindo munição lateral.",
        "Concede-se que a causa é tecnicamente complexa e que prova relevante deve ser produzida; sustenta-se apenas que complexidade não elimina o dever de individualização.",
    ],
    "riscos_etica_impactos": [
        "O pior risco é obter rejeição dos embargos e ainda fragilizar a posição ao exagerar fatos ou custos; por isso as cifras são qualificadas como alegações documentadas.",
        "A redação não atribui má-fé, intenção ou fraude como fato próprio; quando necessário, descreve imputações existentes no processo.",
        "Uma tese absoluta contra perícia poderia prejudicar posições futuras; a alternativa subsidiária de delimitação preserva coerência e contraditório.",
        "Dados sigilosos, mensagens e caminhos locais permanecem fora do produto protocolável; informações operacionais são referidas apenas como objeto potencial de proteção.",
        "O risco reputacional é parecer resistente à prova; a peça o reduz ao aceitar prova pertinente e pedir correlação e fronteiras executáveis.",
        "O revisor deve saber que valores, duração da perícia e suficiência do acervo não receberam confirmação técnica independente.",
        "A estratégia respeita veracidade e lealdade ao separar documento, alegação e inferência e ao não ocultar o fundamento favorável à instrução ampla.",
        "Se acolhido apenas o pedido subsidiário, a perícia ocorrerá, mas com objeto, metodologia, período, acesso e sigilo definidos.",
        "Não há conflito inevitável: o pedido principal preserva a tese processual e o subsidiário protege a execução futura.",
        "Protocolo, alteração de pedidos, inclusão de fatos novos ou envio externo dependem de autorização humana; a entrega desta execução é exclusivamente interna.",
    ],
    "alternativas_solucoes": [
        "Solução principal: integração com possível efeito modificativo. Solução subsidiária: manutenção da prova com delimitação técnica e proteção de dados.",
        "A integração das omissões atua sobre a causa do problema; mera repetição da inconformidade trataria apenas o sintoma e foi evitada.",
        "A alternativa de delimitação exige menos premissas, pois continua útil mesmo que a Turma mantenha o acórdão.",
        "O pedido subsidiário deve fixar especialidade, fatos controvertidos, metodologia, período, data-base, acesso, contraditório e sigilo.",
        "Eventual consenso sobre escopo pericial pode reduzir custo e conflito, mas depende das partes e não substitui o julgamento dos embargos.",
        "Da alternativa rejeitada de rediscussão ampla aproveitou-se apenas a necessidade de uma síntese clara dos pontos decisivos.",
        "O gatilho para trocar de estratégia é decisão posterior que rejeite a omissão ou documento que demonstre lacuna técnica concreta já delimitada.",
        "A sequência de menor risco é integrar cabimento, individualizar lacuna e acervo, ponderar impacto e, por fim, delimitar subsidiariamente.",
        "A espera não é útil diante da demanda de memoriais já formulada; somente fato superveniente justificaria suspensão da entrega interna.",
        "O teste anterior ao protocolo é a revisão cruzada de fidelidade, seguida de leitura do PDF página a página e conferência dos pedidos contra os embargos.",
    ],
    "quantificacao_execucao": [
        "Influenciam a decisão a tramitação desde 2014, os valores e prazos indicados nos embargos e a quantidade de comboios; todos permanecem qualificados como alegações do recurso.",
        "Os cálculos são reprodutíveis apenas na aritmética apresentada pelos embargos; não houve conciliação com documentos contábeis externos.",
        "Dependências: PDFs do caso, Regimento do TRF3, modelo Word do escritório, revisão cruzada, Word para PDF e conta interna para entrega.",
        "O caminho crítico é leitura das fontes, exploração F2-A, minuta auditada, revisão cruzada, montagem DOCX, conversão PDF, QA visual e envio interno.",
        "Não se criou cenário financeiro próprio; o memorial registra faixa temporal e econômica alegada, sem convertê-la em prognóstico pericial.",
        "Falhas de versão, anexo ou número processual podem invalidar a entrega; por isso o processo 4.03.0000 e os hashes são conferidos antes do envio.",
        "São conhecidos os números transcritos nos embargos; são disputadas pertinência e necessidade; são desconhecidos custo e duração efetivos da perícia futura.",
        "A chegada correta será verificada pelo ID da mensagem enviada, nomes e hashes dos anexos e leitura do item em enviados.",
        "OCR, extração de texto, validação de estrutura e renderização podem ser automatizados; conclusão jurídica e liberação externa permanecem humanas.",
        "O recibo do e-mail interno, o ledger FORJA aprovado e os arquivos finais com hashes demonstrarão a execução.",
    ],
    "comunicacao_visual_validacao": [
        "A primeira mensagem é que os embargos pedem integração de omissões concretas, não simples rejulgamento do agravo.",
        "A ordem segue a decisão: cabimento, individualização da lacuna, classificação do acervo, impacto, consequência e pedido subsidiário.",
        "Um quadro comparativo relaciona questão, dado dos embargos e integração necessária; sua função é reduzir ambiguidade entre fundamentos.",
        "Gráficos financeiros ou causais criariam falsa precisão e foram excluídos; cifras permanecem em texto qualificado.",
        "Os termos canônicos são decisão de origem, agravo de instrumento, acórdão embargado, embargos de declaração e prova técnica requerida.",
        "Hashes, nomes de pastas, OCR, e-mails e qualificações internas ficam no relatório de auditoria e nunca na peça.",
        "Devem ficar congelados número do processo, partes, ID do acórdão, dispositivos, cifras qualificadas, pedidos, fecho e assinatura.",
        "A revisão de todas as páginas deve verificar fólio, margens, cabeçalho, quebras, tabelas, citações, rodapé, overflow e placeholders.",
        "O revisor humano deve conferir identidade processual, aderência aos embargos, tratamento do Tema 988, qualificação das cifras, pedidos e versão anexada.",
        "A preservação será comprovada por comparação textual, hashes, gates da FORJA, PDF renderizado e recibo de entrega interna.",
    ],
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def first(folder: Path, pattern: str) -> Path:
    matches = sorted((folder / "Anexos do email").glob(pattern))
    if not matches:
        raise FileNotFoundError(f"{folder}: {pattern}")
    return matches[0]


def build(case: dict) -> Path:
    path = case["folder"] / "_forja" / "F2_QUESTION_TREE.json"
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    ed = first(case["folder"], case["ed_glob"])
    appeal = first(case["folder"], case["appeal_glob"])
    judgment = first(case["folder"], case["judgment_glob"])
    regimento = case["folder"] / "REGIMENTO_INTERNO_TRF3.pdf"
    sources = [
        ("SRC-ED", ed),
        ("SRC-AGRAVO", appeal),
        ("SRC-ACORDAO", judgment),
        ("SRC-RITRF3", regimento),
    ]
    source_ids = [sid for sid, _ in sources]
    data["sourceHashes"] = [
        {"supportId": sid, "file": item.name, "sha256": sha256(item)}
        for sid, item in sources
    ]
    data["producerRunId"] = f"forja-f2a-{case['slug'].lower()}-20260729"
    data["reviewerRunId"] = "pending-cross-family-review"
    data["updatedAt"] = datetime.now().astimezone().isoformat(timespec="seconds")
    data["status"] = "completed"
    data["problemDefinition"] = (
        f"No AI {case['process']}, definir se o acórdão de ID {case['judgment_id']} "
        "deixou de enfrentar fundamentos capazes de alterar o resultado e, "
        "subsidiariamente, quais fronteiras tornam a prova técnica executável."
    )
    data["diagnosticSynthesis"] = (
        f"O acervo documenta decisão de origem, agravo, acórdão e embargos. "
        f"{case['distinctive']} A estratégia de menor risco é pedir integração "
        "por uma ordem decisória verificável, qualificar cifras e duração como "
        "alegações do recurso e preservar pedido subsidiário de delimitação."
    )
    counters: dict[str, int] = {}
    for question in data["questions"]:
        lens = question["lens"]
        index = counters.get(lens, 0)
        counters[lens] = index + 1
        question["caseAnchor"] = (
            f"AI {case['process']}; ED da Transpetro contra o acórdão "
            f"ID {case['judgment_id']}; memoriais relativos a {case['party']}."
        )
        question["status"] = "answered"
        question["answer"] = ANSWERS[lens][index]
        if question["category"] in {
            "fact",
            "evidence",
            "procedural_event",
            "precedent",
            "calculation",
        }:
            question["epistemicStatus"] = (
                "confirmed_official_source"
                if question["category"] == "precedent"
                else "confirmed_document"
            )
            question["supportIds"] = source_ids
        else:
            question["epistemicStatus"] = (
                "strategic_hypothesis"
                if question["category"] in {"alternative", "risk", "opponent_response"}
                else "legal_inference"
            )
            question["supportIds"] = []
        question["unansweredConsequence"] = ""
    data["coverage"] = {
        "total": 100,
        "material": 100,
        "answeredMaterial": 100,
        "blockedMaterial": 0,
        "perLens": {lens: 10 for lens in ANSWERS},
    }
    data["solutionHypotheses"] = [
        {
            "hypothesisId": "H01",
            "description": "Integração das omissões com efeitos modificativos apenas como consequência necessária do saneamento.",
            "conditions": [
                "fundamentos previamente devolvidos e não enfrentados",
                "potencial concreto de alteração do resultado",
            ],
            "risks": [
                "a Turma considerar suficiente a fundamentação existente",
                "o pedido ser lido como rediscussão do mérito",
            ],
            "questionIds": ["Q032", "Q041", "Q049", "Q051", "Q060"],
            "downstreamTargets": ["F4", "F5", "F6", "F7"],
        },
        {
            "hypothesisId": "H02",
            "description": "Manutenção subsidiária da prova, com comando delimitado e salvaguardas de contraditório, proporcionalidade e sigilo.",
            "conditions": [
                "a Turma manter o provimento do agravo",
                "ser possível vincular fatos controvertidos a especialidades e metodologia",
            ],
            "risks": [
                "escopo ainda genérico gerar instrução sem fronteiras",
                "custos e duração efetivos permanecerem desconhecidos",
            ],
            "questionIds": ["Q040", "Q074", "Q078", "Q085", "Q088"],
            "downstreamTargets": ["F4", "F5", "F6", "F7"],
        },
    ]
    data["downstreamHandoff"] = {
        "F3": ["Q011", "Q012", "Q021", "Q022", "Q032"],
        "F4": ["Q041", "Q042", "Q045", "Q049", "Q050"],
        "F5": ["Q051", "Q053", "Q057", "Q060", "Q071"],
        "F6": ["Q071", "Q074", "Q078", "Q083", "Q084"],
        "F7": ["Q091", "Q092", "Q097", "Q099", "Q100"],
    }
    data["openDecisiveQuestions"] = []
    data["draftRelease"] = "ready_for_drafting"
    data["issues"] = []
    data["contentHash"] = expected_content_hash(data)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return path


if __name__ == "__main__":
    for case_data in CASES:
        print(build(case_data))
