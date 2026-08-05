from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "data" / "intervencoes_manuais.json"


UPDATES = {
    "email-corsan-agerst-19f3dc9ff92081cd": {
        "status": "aberta",
        "urgenciaManual": "alta",
        "prazo": "2026-08-04",
        "prazoTexto": "consulta pública até 04/08/2026; audiência em 11/08/2026 às 14h; data de deliberação não comprovada",
        "resumo": "Diagnóstico preliminar interno N3 reconstruído a partir das fontes locais e do Anexo Único integral. O material anterior continha erros factuais, percentuais e conclusões sem base e não deve ser usado.",
        "proximaAcao": "Obter TAACC e anexos, Resoluções 21/2019, 22/2019 e 69/2024, Processo 61/2026 integral, normas locais e documentos técnicos; depois revisar A01-A54 antes de qualquer circulação externa.",
        "evidenciaResposta": "Arquivo local N3: CORSAN AGERST - Proposta de Serviços Jurídicos/_forja_n3_reconstrucao_2026-07-10/DIAGNOSTICO_PRELIMINAR_INTERNO_CORSAN_AGERST_N3.pdf. Não constitui entrega ao cliente.",
        "evidenciaTipo": "arquivo",
        "comment": "AUDITORIA N3 10/07: a versão anterior foi reprovada porque ignorou o Anexo Único existente, errou o calendário e criou percentuais, custos e impactos sem base. Reconstrução interna concluída em 17 páginas: 54 linhas A01-A54 rastreáveis, consulta 06/07-04/08 e audiência 11/08 às 14h, zero moeda/percentual e QA aprovado. Continua aberta e condicionada aos documentos originários faltantes; não usar os rascunhos Gmail anteriores.",
    },
    "email-libra-sul-agint-stj-19f3c9350d875062": {
        "status": "pronta_para_revisao",
        "urgenciaManual": "alta",
        "prazo": "2026-07-15",
        "prazoTexto": "revisão interna até 15/07/2026; protocolo e sessão dependem de confirmação oficial",
        "resumo": "Memoriais N3 reconstruídos sobre os fundamentos reais da decisão e o conteúdo efetivo do agravo interno, com foco nas Súmulas 5 e 7 e dialeticidade apenas no ponto demonstrado.",
        "proximaAcao": "Revisão humana jurídica/editorial da versão N3 de 7 páginas; confirmar pauta, modalidade, data do fecho e forma de entrega antes de protocolo.",
        "evidenciaResposta": "Arquivo local N3: Memoriais AgInt AREsp 2578181 SC - LIBRA SUL/_forja_n3_reconstrucao_2026-07-10/MEMORIAIS_LIBRA_SUL_N3_SUPERIOR.pdf. Ainda não enviado.",
        "evidenciaTipo": "arquivo",
        "comment": "AUDITORIA N3 10/07: os rascunhos anteriores afirmavam silêncio onde o AgInt efetivamente impugnava, citavam incorretamente a Súmula 182, usavam art. 343-A inexistente e continham fatos sem prova. Nova versão superior com 7 páginas, fonte canônica única, fidelidade 100% e QA visual aprovado. Corrigida também a assinatura para OAB/DF 29.786. Estado atual: pronta para revisão humana; não enviada.",
    },
    "email-patricia-fabio-memoriais-19f3c68ee6d8fef2": {
        "status": "pronta_para_revisao",
        "urgenciaManual": "alta",
        "prazo": "2026-07-14",
        "prazoTexto": "sessão informada para 14/07/2026 às 10h; versão N3 corrigida ainda não enviada",
        "resumo": "Versão entregue em 10/07 foi reaberta após auditoria identificar honorários recursais incabíveis e uso invertido do art. 944, parágrafo único. Nova versão N3 corrige ambos e preserva os eixos úteis.",
        "proximaAcao": "Revisar imediatamente a versão N3 de 6 páginas e, se aprovada, substituir por novo envio os anexos remetidos às 03:41; depois confirmar entrega aos julgadores e protocolo.",
        "evidenciaResposta": "A entrega anterior por e-mail permanece registrada, mas foi superada pela auditoria. Arquivo local N3 corrigido em Anexos do email/MEMORIAIS - PATRICIA E FABIO - N3 SUPERIOR PARA REVISAO - 10-07-2026.pdf; ainda não enviado.",
        "evidenciaTipo": "arquivo",
        "comment": "AUDITORIA N3 10/07: a versão enviada às 03:41 reintroduziu dois erros jurídicos reconhecidos no próprio checklist: art. 944, parágrafo único, usado para agravar dano e honorários do art. 85, § 11, no recurso dos próprios vencedores. Demanda reaberta para revisão. Nova versão N3 com 6 páginas removeu os dois eixos, preservou os demais pedidos da apelação, passou em fidelidade/QA e foi arquivada como PARA REVISAO. Não registrar a N3 como enviada ou protocolada.",
    },
    "email-natura-cabreuva-19f3991ebc75fe03": {
        "status": "aberta",
        "urgenciaManual": "media",
        "prazo": "2026-07-20",
        "prazoTexto": "minuta até 20/07/2026; parecer final bloqueado sem o caderno documental",
        "resumo": "Roteiro jurídico interno N3 dos sete quesitos concluído sem conclusões fáticas. O material organiza testes, provas necessárias e limites, mas não é parecer à Natura.",
        "proximaAcao": "Obter acesso integral ao Drive, montar cronologia parcela a parcela e executar pesquisa oficial completa de STF, STJ e TJs antes de responder conclusivamente aos sete quesitos.",
        "evidenciaResposta": "Arquivo local N3: Natura Cabreúva - Parecer e Quesitos - prazo 20-07-2026/_forja_n3_reconstrucao_2026-07-10/ROTEIRO_JURIDICO_INTERNO_NATURA_CABREUVA_N3.pdf. Não constitui parecer entregue.",
        "evidenciaTipo": "arquivo",
        "comment": "AUDITORIA N3 10/07: versões anteriores ainda atribuíam viabilidades, efeitos de notificação e estratégias sem fatos do caso. Reconstrução interna concluída em 17 páginas, com sete quesitos condicionais, apenas súmulas confirmadas no corpus, fidelidade 100% e QA aprovado. Permanece aberta; o parecer final depende do Drive, cronologia do crédito e pesquisa oficial qualificada. Não usar o rascunho Gmail anterior como parecer conclusivo.",
    },
    "email-auto-19f3f25cb64df962": {
        "status": "aberta",
        "urgenciaManual": "alta",
        "prazo": "2026-07-17",
        "prazoTexto": "prazo interno informado de 17/07/2026; protocolo bloqueado por documentos essenciais",
        "resumo": "Petição inicial V5 N3 preserva a tese procedimental da RN 558, mas assume divergências da DPS e do TCB e não está apta para protocolo.",
        "proximaAcao": "Regularizar procuração conjunta, reconciliar DPS e contrato, esclarecer autoria/autorização do TCB, montar manifesto probatório e obter laudo bucomaxilofacial e prova contemporânea do perigo.",
        "evidenciaResposta": "Entrega anterior de V3 permanece no histórico, mas não libera protocolo. Arquivo local V5 N3: Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/_forja_n3_reconstrucao_2026-07-10/PETICAO_INICIAL_TJDFT_MATEUS_NIVEL_SOL_V5_N3_10-07-2026.pdf.",
        "evidenciaTipo": "arquivo",
        "comment": "AUDITORIA N3 10/07: a DPS traz contrato/vigência diferentes da proposta; o TCB tem zero assinaturas e a conversa certificada mostra a secretária cogitando assinar como Fábio. V5 N3 gerada em 13 páginas, sem pedido de sigilo, com esses fatos assumidos e RN 558 preservada como eixo autônomo. QA visual aprovado, mas protocolo continua bloqueado por procuração, reconciliação da DPS, autoria do TCB, manifesto, laudo atual e prova de perigo/dano.",
    },
    "email-auto-19f3ed5bdbdcf159": {
        "status": "aberta",
        "urgenciaManual": "alta",
        "prazo": "2026-07-15",
        "prazoTexto": "prazo interno informado para 15/07/2026; sessão de 18/08 depende de pauta oficial",
        "resumo": "Memorial Azimut N3 reconstruído como minuta interna condicionada, com Tema 1.368, título/convenção, preclusão, Súmulas 5/7 e art. 520 tratados separadamente.",
        "proximaAcao": "Obter título integral, três instrumentos contratuais, cronologia completa da preclusão, acórdão de conversão, decisão do efeito suspensivo, pauta oficial e cálculo homogêneo antes de liberar protocolo.",
        "evidenciaResposta": "Arquivo local N3: Re Relatório Azimut/_forja_n3_reconstrucao_2026-07-10/MEMORIAL_AZIMUT_N3_MINUTA_INTERNA_CONDICIONADA.pdf. Não constitui entrega ou peça protocolável.",
        "evidenciaTipo": "arquivo",
        "comment": "AUDITORIA N3 10/07: o rascunho anterior continha art. 343-A inexistente, placeholders, cálculo com datas incompatíveis e omitia o capítulo do art. 520. Nova minuta interna de 8 páginas removeu cálculo/excesso, usa o Tema 1.368 no alcance correto e assume os riscos de título, convenção, preclusão e Súmulas 5/7. QA/fidelidade aprovados. Continua aberta e bloqueada até os sete documentos/controles listados; não usar os drafts Gmail anteriores.",
    },
}


def main() -> None:
    manual = read_json(MANUAL, {"schema": 1, "updatedAt": now_iso(), "items": {}})
    manual.setdefault("schema", 1)
    items = manual.setdefault("items", {})
    stamp = now_iso()
    changed = 0

    for item_id, update in UPDATES.items():
        entry = items.setdefault(item_id, {"comentarios": [], "overrides": {}})
        comments = entry.setdefault("comentarios", [])
        comment_id = f"forja-n3-reconstrucao-20260710-{item_id}"
        if not any(comment.get("id") == comment_id for comment in comments):
            comments.append({
                "id": comment_id,
                "at": stamp,
                "tipo": "forja-n3-auditoria",
                "texto": update["comment"],
                "autor": "FORJA N3/Codex",
            })
            changed += 1

        overrides = entry.setdefault("overrides", {})
        for key in (
            "status", "urgenciaManual", "prazo", "prazoTexto", "resumo",
            "proximaAcao", "evidenciaResposta", "evidenciaTipo",
        ):
            if overrides.get(key) != update[key]:
                overrides[key] = update[key]
                changed += 1
        if overrides.get("respondidoComConteudo") is not False:
            overrides["respondidoComConteudo"] = False
            changed += 1
        entry["updatedAt"] = stamp

    manual["updatedAt"] = stamp
    atomic_write_json(MANUAL, manual)
    print({"ok": True, "changed": changed, "items": len(UPDATES)})


if __name__ == "__main__":
    main()
