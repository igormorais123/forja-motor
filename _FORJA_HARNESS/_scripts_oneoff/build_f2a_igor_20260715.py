from __future__ import annotations

import hashlib
import json
from pathlib import Path

from forja_exploracao_100 import build_scaffold
from forja_n4_common import expected_content_hash


ROOT = Path(__file__).resolve().parent


CASES = {
    "case-igor-melissa-endereco-20260715": {
        "anchor": "Processo 0812709-43.2025.8.07.0016; item 24 da reconvenção ID 267336993; atualização do endereço de Melissa e exequibilidade da convivência",
        "short": "da reiteração do item 24 e da verificação institucional do endereço residencial de Melissa",
        "command": ROOT / "PETICAO_ENDERECO_EXEQUIBILIDADE_FORJA_20260715" / "COMANDO_FORJA.md",
        "sources": "MAPA.md; ID 267336993; decisão ID 271866597; comprovante ID 256889476; comunicação ID 256889493; CPC, Código Civil e ECA em fontes oficiais",
        "problem": "Converter uma alegação de possível desatualização do endereço em pedido institucional, proporcional e executável, sem afirmar mudança, fraude, ocultação dolosa ou alienação parental sem prova.",
        "diagnosis": "Há pedido reconvencional documentado e não enfrentado pela decisão de 09/04/2026, comprovante de residência de outubro de 2025 e recusa escrita de fornecer o endereço ao pai. O dado superveniente é apenas indiciário. A solução robusta é atualização documental e, se necessário, constatação oficial, com proteção da criança e sem investigação privada.",
        "solutions": [
            ("H01", "Intimação para atualização do endereço com comprovante recente e fixação de ponto objetivo de entrega e retirada.", ["Resposta da parte e conferência prévia do PJe"], ["Possível alegação de segurança ou privacidade"], ["Q001", "Q031", "Q071"]),
            ("H02", "Na ausência de resposta suficiente, constatação oficial no endereço cadastrado e solução logística neutra.", ["Ordem judicial específica e diligência não invasiva"], ["Diligência negativa não prova, isoladamente, ocultação dolosa"], ["Q021", "Q061", "Q074"]),
        ],
    },
    "case-igor-melissa-acordo-doutorado-20260715": {
        "anchor": "Agravo 0723365-65.2026.8.07.0000; proposta pós-audiência de 30/06/2026; guarda compartilhada e concessão acadêmica documentada pelo IDP",
        "short": "da proposta de autocomposição no agravo, com o doutorado presencial como medida objetiva da concessão paterna",
        "command": ROOT / "PETICAO_ACORDO_DOUTORADO_FORJA_20260715" / "COMANDO_FORJA.md",
        "sources": "MAPA.md; agravo 0723365-65.2026.8.07.0000; decisão ID 85309244; reconvenção ID 267336993; documentos e quadro de horários do IDP; CPC, Código Civil e ECA em fontes oficiais",
        "problem": "Transformar uma proposta pós-audiência extensa e acusatória em oferta conciliatória clara, executável e compatível com o interesse da criança, sem renúncia prematura e sem converter pedido de desculpas em confissão forçada.",
        "diagnosis": "O núcleo negociável é guarda compartilhada com lar materno, manutenção temporária do regime vigente, deveres bilaterais objetivos, reconhecimento escrito e não repetição. O calendário IDP demonstra o custo concreto da concessão, mas não autoriza dramatização nem prova horários além do bloco documentado. Multa só deve alcançar obrigações objetivas e verificáveis.",
        "solutions": [
            ("H01", "Proposta global enxuta, com núcleo indivisível, compromissos bilaterais verificáveis e reconhecimento escrito de impacto e não repetição.", ["Aceitação expressa, oitiva do MP e homologação"], ["A exigência de desculpas pode reduzir a adesão"], ["Q003", "Q051", "Q072"]),
            ("H02", "Permitir contraproposta parcial, preservando como núcleo mínimo guarda compartilhada, informação parental e disciplina logística.", ["Delimitação do que pode ser parcialmente composto"], ["Fragmentação pode reduzir a contrapartida pretendida pelo Agravante"], ["Q006", "Q073", "Q078"]),
        ],
    },
}


LENS_ANSWERS = {
    "mandato_resultado": "O mandato autoriza reescrever a peça já idealizada, preservando o veículo processual, a finalidade prática e os limites probatórios; não autoriza inventar andamento, admitir renúncia ou expor origem operacional.",
    "fatos_cronologia": "A cronologia será limitada aos atos, datas e documentos conferidos; qualquer evento posterior não disponível será tratado como verificação pré-protocolo, sem convertê-lo em fato afirmado.",
    "prova_fontes": "Cada proposição material dependerá das fontes enumeradas no comando e de localizador processual; relato do cliente ou indício será nomeado com menor força epistemológica.",
    "processo_competencia": "O veículo, o órgão e os pedidos serão mantidos dentro da cognição disponível, distinguindo o processo de origem do agravo e evitando pedir ao julgador providência fora de sua competência.",
    "direito_precedentes": "A fundamentação será legal e oficial, sem jurisprudência ornamental: CPC, Código Civil e ECA, com conferência do Regimento Interno do TJDFT quando pertinente ao processamento.",
    "adversario_julgador": "A redação enfrentará a melhor objeção contrária em sua forma mais forte, reduzirá excessos e oferecerá ao julgador um caminho decisório estreito, proporcional e executável.",
    "riscos_etica_impactos": "A peça não acusará intenção, fraude, alienação ou má-fé sem prova; protegerá dados da criança, evitará investigação privada e reservará decisões negociais sensíveis à revisão humana.",
    "alternativas_solucoes": "A solução principal será acompanhada de alternativas subsidiárias menos invasivas, com gatilhos objetivos para mudança de estratégia e preservação da utilidade processual.",
    "quantificacao_execucao": "Datas, horários, prazos, valores e anexos serão reproduzíveis a partir das fontes; a entrega será validada por hash, renderização Word/PDF e inspeção visual integral.",
    "comunicacao_visual_validacao": "A peça abrirá com síntese executiva, seguirá a ordem real de decisão, usará apenas quadros funcionais e será submetida a revisão jurídica, factual, visual e humana antes do protocolo.",
}


def build(case_id: str, cfg: dict) -> dict:
    payload = build_scaffold(case_id, cfg["anchor"])
    source_hash = hashlib.sha256(cfg["command"].read_bytes()).hexdigest()
    for idx, question in enumerate(payload["questions"], start=1):
        lens = question["lens"]
        question["text"] = question["text"].rstrip("?") + f" no contexto {cfg['short']}?"
        question["caseAnchor"] = cfg["anchor"]
        question["whyItMatters"] = f"A resposta controla a segurança factual, a utilidade e a executabilidade {cfg['short']}."
        question["materiality"] = "material" if idx % 5 else "review_required"
        question["status"] = "answered"
        question["answer"] = LENS_ANSWERS[lens] + f" Aplicação específica da questão Q{idx:03d}: conferir o ponto contra {cfg['sources']}."
        if question["category"] in {"fact", "evidence", "procedural_event", "precedent", "calculation"}:
            question["epistemicStatus"] = "confirmed_document" if question["category"] != "precedent" else "confirmed_official_source"
            question["supportIds"] = ["SRC-COMANDO", f"SRC-{lens.upper()}"]
        elif question["category"] in {"alternative", "risk", "opponent_response", "communication", "visual", "execution", "request", "mandate", "ethics"}:
            question["epistemicStatus"] = "strategic_hypothesis"
            question["supportIds"] = []
        else:
            question["epistemicStatus"] = "legal_inference"
            question["supportIds"] = []
        question["downstreamTargets"] = ["F3", "F4"] if idx <= 80 else ["F6", "F7"]
        question.pop("unansweredConsequence", None)
    payload["status"] = "approved"
    payload["sourceHashes"] = [source_hash]
    payload["producerRunId"] = "igor-f2a-producer-20260715"
    payload["reviewerRunId"] = "igor-f2a-reviewer-20260715"
    payload["problemDefinition"] = cfg["problem"]
    payload["diagnosticSynthesis"] = cfg["diagnosis"]
    payload["coverage"] = {
        "total": 100,
        "material": 80,
        "answeredMaterial": 80,
        "blockedMaterial": 0,
        "perLens": {lens: 10 for lens in LENS_ANSWERS},
    }
    payload["solutionHypotheses"] = [
        {"hypothesisId": hid, "description": desc, "conditions": cond, "risks": risks, "questionIds": qids, "downstreamTargets": ["F4", "F6"]}
        for hid, desc, cond, risks, qids in cfg["solutions"]
    ]
    payload["downstreamHandoff"] = {
        "F3": ["Q011", "Q021", "Q031", "Q041"],
        "F4": ["Q001", "Q051", "Q061", "Q071"],
        "F5": ["Q041", "Q050"],
        "F6": ["Q003", "Q072", "Q091"],
        "F7": ["Q067", "Q087", "Q100"],
    }
    payload["openDecisiveQuestions"] = []
    payload["draftRelease"] = "ready_for_drafting"
    payload["issues"] = [{"code": "HUMAN-PJE-CHECK", "severity": "review_required", "detail": "Conferir ata e andamentos atuais no PJe antes do protocolo."}]
    payload["contentHash"] = expected_content_hash(payload)
    return payload


for case_id, cfg in CASES.items():
    out = ROOT / "state" / case_id / "n4_artifacts" / "F2_QUESTION_TREE.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build(case_id, cfg), ensure_ascii=False, indent=2), encoding="utf-8")
    print(out)
