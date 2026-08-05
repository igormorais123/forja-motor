import copy
from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "data" / "intervencoes_manuais.json"


UPDATES = {
    "email-jorge-haroldo-edcl-19f3c8200768b56e": {
        "status": "pronta_para_revisao",
        "urgenciaManual": "alta",
        "prazo": "2026-07-14",
        "prazoTexto": "revisão interna solicitada até 14/07/2026; termo final projetado em 07/08/2026 pela suspensão de 02 a 31/07, sujeito à conferência da intimação",
        "resumo": "Minuta N3 dos embargos concluída sobre o inteiro teor oficial do acórdão de 02/07/2026. O eixo principal distingue dolo genérico e específico e questiona o reenquadramento do inciso X para o caput do art. 10 sem reexame de prova.",
        "proximaAcao": "Revisar a minuta de 10 páginas e conferir as seis peças da cadeia recursal nos 28 links do Drive, a sanção exata da origem, a devolução do capítulo da aposentadoria e a intimação eletrônica antes de liberar protocolo.",
        "evidenciaResposta": "Arquivo local N3: Embargos AgInt AREsp 1883361 RS - Jorge Haroldo/_forja_n3_proxima_2026-07-10/MINUTA_EDCL_JORGE_HAROLDO_N3.pdf. QA visual, fidelidade, Helena e Cícero aprovados com bloqueadores de protocolo. Não enviado nem protocolado.",
        "evidenciaTipo": "arquivo",
        "comment": "FORJA N3 10/07: obtido e conferido o inteiro teor oficial do acórdão publicado em 02/07. O resultado real foi 3x2, com Afrânio Vilela e Teodoro vencidos. Minuta interna de 10 páginas concluída em DOCX/PDF, com 3 elementos visuais, fidelidade 100% e inspeção de todas as páginas. Corrigidos o OAB para RS 64.975, o tratamento da aposentadoria conforme jurisprudência atual e a identificação do AgInt no REsp 1.558.863/RJ. Pronta para revisão humana, mas protocolo bloqueado até conferência das peças do Drive, sanção da origem, devolução do capítulo e intimação. Nenhum envio realizado.",
    },
    "email-auto-19f3ea400b7dec3d": {
        "status": "pronta_para_revisao",
        "urgenciaManual": "alta",
        "prazo": "2026-07-14",
        "prazoTexto": "prazo de trabalho informado no e-mail: 14/07/2026; confirmar com o responsável antes de qualquer envio externo",
        "resumo": "Parecer N3 concluído sobre regime disciplinar do Ministério Público, fraude à lei e repercussão eleitoral em 2026. A regra ordinária distingue procedimentos preliminares de PAD, mas o precedente individual do TSE exige estratégia de superação expressa e prova atualizada.",
        "proximaAcao": "Fábio deve revisar o parecer de 21 páginas e definir o cargo pretendido. Depois, obter certidões e inteiros teores dos expedientes do CNMP, corrigir o número da Sindicância 1.00145 e reunir a cadeia integral do RO-El 0601407-70/PR antes de liberar a versão externa.",
        "evidenciaResposta": "Arquivo local N3: Material para elaboração de parecer - interessado Deltan Dallagnol/_forja_n3_proxima_2026-07-10/PARECER_DELTAN_N3.pdf. Há também matriz integral dos quesitos, relatório de fontes, revisões Helena/Cícero e QA das 21 páginas. Não enviado ao consulente.",
        "evidenciaTipo": "arquivo",
        "comment": "FORJA N3 10/07: parecer interno de 21 páginas concluído em DOCX/PDF, acompanhado de matriz completa de respostas aos quesitos, 4 elementos visuais vetoriais, fontes oficiais preservadas, fidelidade de conteúdo 100% e inspeção página a página. A análise corrige dupla contagem de procedimentos, distingue fundamentos heterogêneos de arquivamento e não promete elegibilidade diante do precedente individual do TSE. Pronto para revisão humana. Permanecem bloqueadores externos: cargo pretendido divergente entre e-mail e quesitos, número da Sindicância 1.00145, certidões/decisões integrais do CNMP e cadeia completa do RO-El. Nenhum envio realizado.",
    },
    "email-auto-19f3f25cb64df962": {
        "status": "pronta_para_revisao",
        "urgenciaManual": "alta",
        "prazo": "2026-07-17",
        "prazoTexto": "prazo interno informado de 17/07/2026; protocolo bloqueado por documentos essenciais",
        "resumo": "Petição inicial V6 N3 concluída em 15 páginas. Mateus figura como autor direto; a estipulante e pagadora tem pretensões próprias reservadas. A tutela imediata pede reintegração e exibição, enquanto cirurgia permanece condicionada a relatório atual.",
        "proximaAcao": "Revisar a V6, conferir mandato e assistência dos curadores, numerar o pacote físico conforme o manifesto e decidir se haverá pedido cirúrgico imediato. Se aparecer decisão final da ANS anterior à exclusão, reavaliar a causa de pedir antes do protocolo.",
        "evidenciaResposta": "Arquivo local V6 N3: Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/_forja_n3_reconstrucao_2026-07-10/PETICAO_INICIAL_TJDFT_MATEUS_NIVEL_SOL_V6_N3_10-07-2026.pdf. São 15 páginas, 3 diagramas vetoriais, fidelidade 100%, F7 sem achados, Cícero 90,1 e inspeção integral. Não protocolada.",
        "evidenciaTipo": "arquivo",
        "respondidoComConteudo": False,
        "comment": "FORJA N3 10/07 — fechamento V6: inicial reconstruída em DOCX/PDF, 15 páginas, 3 diagramas vetoriais, manifesto de 11 grupos documentais, fidelidade integral e inspeção de todas as páginas. Mateus é o autor; a estipulante fica fora do polo nesta versão. Reintegração e exibição são o primeiro degrau; cirurgia depende de relatório bucomaxilofacial atual. Pronta para revisão humana, não protocolada.",
    },
    "email-auto-19f3ed5bdbdcf159": {
        "status": "pronta_para_revisao",
        "urgenciaManual": "alta",
        "prazo": "2026-07-15",
        "prazoTexto": "prazo interno informado para 15/07/2026; sessão de 18/08 depende de pauta oficial",
        "resumo": "Memorial Azimut N3 concluído como minuta interna condicionada. Tema 1.368, título/convenção, preclusão, Súmulas 5/7 e art. 520 são tratados separadamente, sem cálculo especulativo.",
        "proximaAcao": "Revisar a minuta de 8 páginas e obter título, instrumentos, cadeia da preclusão, acórdão de conversão, decisão suspensiva, pauta oficial e cálculo homogêneo antes de qualquer liberação externa.",
        "evidenciaResposta": "Arquivo local: Re Relatório Azimut/_forja_n3_reconstrucao_2026-07-10/MEMORIAL_AZIMUT_N3_MINUTA_INTERNA_CONDICIONADA.pdf. F7 sem achados, Cícero preflight pronto, fidelidade 100% e 8 páginas inspecionadas. Não enviada nem protocolada.",
        "evidenciaTipo": "arquivo",
        "respondidoComConteudo": False,
        "comment": "FORJA N3 10/07 — fechamento Azimut: minuta interna condicionada de 8 páginas concluída, com Tema 1.368 no alcance correto, capítulo autônomo do art. 520 e riscos de título, convenção, preclusão e Súmulas 5/7 visíveis. Pronta para revisão humana; bloqueada para protocolo pelos sete grupos documentais listados.",
    },
    "email-libra-sul-agint-stj-19f3c9350d875062": {
        "status": "pronta_para_revisao",
        "urgenciaManual": "alta",
        "prazo": "2026-07-15",
        "prazoTexto": "revisão interna até 15/07/2026; protocolo e sessão dependem de confirmação oficial",
        "resumo": "Memoriais Libra Sul N3 reconstruídos em 7 páginas sobre os fundamentos reais da decisão e do agravo interno, sem atribuir silêncio onde houve impugnação.",
        "proximaAcao": "Revisar a versão N3, confirmar pauta, modalidade, data do fecho e forma de entrega antes de qualquer protocolo ou circulação externa.",
        "evidenciaResposta": "Arquivo local N3: Memoriais AgInt AREsp 2578181 SC - LIBRA SUL/_forja_n3_reconstrucao_2026-07-10/MEMORIAIS_LIBRA_SUL_N3_SUPERIOR.pdf. F7 sem achados, fidelidade 100% e 7 páginas aprovadas no QA. Não enviado nem protocolado.",
        "evidenciaTipo": "arquivo",
        "respondidoComConteudo": False,
        "comment": "FORJA N3 10/07 — fechamento Libra Sul: nova versão superior de 7 páginas concluída em DOCX/PDF, com fidelidade integral, F7 sem achados e inspeção visual de todas as páginas. Corrigidas a falsa premissa de silêncio, a incidência indevida da Súmula 182, o artigo inexistente e a identificação profissional. Pronta para revisão humana; não enviada nem protocolada.",
    },
    "email-patricia-fabio-memoriais-19f3c68ee6d8fef2": {
        "status": "pronta_para_revisao",
        "urgenciaManual": "alta",
        "prazo": "2026-07-14",
        "prazoTexto": "sessão informada para 14/07/2026 às 10h; versão N3 corrigida ainda não enviada",
        "resumo": "Memoriais Patrícia e Fábio N3 reconstruídos em 6 páginas, sem honorários recursais incabíveis e sem uso invertido do art. 944, parágrafo único, do Código Civil.",
        "proximaAcao": "Revisar imediatamente a versão N3 e, se aprovada, decidir a substituição formal dos anexos anteriormente enviados; depois confirmar entrega e eventual protocolo por evidência própria.",
        "evidenciaResposta": "A entrega anterior permanece no histórico, mas foi superada pela auditoria. Arquivo local N3: Memoriais Apelação Patrícia e Fábio - Proc. 0014560-09.2014.8.19.0209/_forja_n3_reconstrucao_2026-07-10/MEMORIAIS_PATRICIA_FABIO_N3_SUPERIOR.pdf. F7 sem achados, fidelidade 100% e 6 páginas aprovadas no QA. A N3 não foi enviada.",
        "evidenciaTipo": "arquivo",
        "respondidoComConteudo": False,
        "comment": "FORJA N3 10/07 — fechamento Patrícia/Fábio: versão corrigida de 6 páginas concluída em DOCX/PDF, com fidelidade integral, F7 sem achados e inspeção visual completa. Removidos o pedido autônomo de honorários recursais e o uso do art. 944, parágrafo único, para agravar o dano. A entrega antiga segue no histórico, mas a N3 está apenas pronta para revisão e não foi enviada.",
    },
    "email-cafelana-edcl-19f1f9d3cc69c8c8": {
        "status": "cumprida",
        "urgenciaManual": "alta",
        "prazo": None,
        "prazoTexto": "entrega anterior comprovada por e-mail; versão N3 superior aguarda decisão de revisão/substituição",
        "resumo": "A demanda original foi entregue por e-mail em 06/07/2026. Uma versão N3 superior de 9 páginas foi reconstruída com quatro omissões delimitadas, Tema 1.076 e revisão Helena/Cícero.",
        "proximaAcao": "Revisar a versão N3 e decidir se ela substituirá ou complementará o arquivo anteriormente enviado; antes de uso externo, conferir IDs, órgão atual, prazo, novos embargos e assinaturas.",
        "evidenciaResposta": "Entrega comprovada: e-mail 19f3973133815e33 com CAFELANA_CR_EDCL_FINAL_02-07-2026.docx. Versão superior local: Cafelana/_forja_n3_edcl_reabertura_2026-07-10/MINUTA_CAFELANA_EDCL_N3.pdf; 9 páginas, 3 elementos visuais, fidelidade 100% e QA aprovado. A N3 não foi enviada.",
        "evidenciaTipo": "email_e_arquivo",
        "respondidoComConteudo": True,
        "comment": "FORJA N3 10/07 — reconciliação Cafelana EDcl: preservada a entrega real do e-mail 19f3973133815e33. A reconstrução N3 superior existe localmente e está pronta para revisão, mas não foi marcada como enviada. O painel distingue a entrega histórica da nova versão.",
    },
    "email-cafelana-agint-aresp-2698443-19f2f0876e358eab": {
        "status": "cumprida",
        "urgenciaManual": "alta",
        "prazo": None,
        "prazoTexto": "entrega anterior comprovada por e-mail; versão N3 superior aguarda decisão de revisão/substituição",
        "resumo": "A demanda original foi entregue por e-mail em 07/07/2026. Uma versão N3 superior de 10 páginas foi reconstruída com prevenção e preclusão tratadas defensivamente, sem afirmar redistribuição positiva não comprovada.",
        "proximaAcao": "Revisar a versão N3 e decidir se ela substituirá ou complementará a entrega anterior; antes de uso externo, conferir intimação, andamento atual, comparação integral do AgInt e assinaturas.",
        "evidenciaResposta": "Entrega comprovada: e-mail 19f3e7e5d148ff19 com DOCX/PDF. Versão superior local: Cafelana/contrarrazões ao AgInt no AREsp nº 2.698.443D/_forja_n3_reabertura_2026-07-10/MINUTA_CAFELANA_AGINT_N3.pdf; 10 páginas, 3 diagramas, fidelidade 100% e QA aprovado. A N3 não foi enviada.",
        "evidenciaTipo": "email_e_arquivo",
        "respondidoComConteudo": True,
        "comment": "FORJA N3 10/07 — reconciliação Cafelana AgInt: preservada a entrega real do e-mail 19f3e7e5d148ff19. A reconstrução N3 superior existe localmente e está pronta para revisão, mas não foi marcada como enviada. O painel distingue a entrega histórica da nova versão.",
    },
    "whatsapp-audio-cafelana-prevencao-20260708": {
        "status": "pronta_para_revisao",
        "urgenciaManual": "alta",
        "prazo": None,
        "prazoTexto": "diretrizes incorporadas às duas reconstruções N3; sem novo envio externo",
        "resumo": "As orientações dos áudios sobre prevenção, preclusão e uso da peça humana foram incorporadas às versões N3 das duas frentes Cafelana.",
        "proximaAcao": "Revisar conjuntamente as versões N3 do AgInt e dos EDcl e decidir se haverá substituição ou complemento das entregas anteriores.",
        "evidenciaResposta": "Arquivos locais: Cafelana/_forja_n3_edcl_reabertura_2026-07-10 e Cafelana/contrarrazões ao AgInt no AREsp nº 2.698.443D/_forja_n3_reabertura_2026-07-10. As versões N3 ainda não foram enviadas.",
        "evidenciaTipo": "arquivo",
        "respondidoComConteudo": False,
        "comment": "TRIAGEM DE ÁUDIO 10/07: diretrizes Cafelana incorporadas nas duas reconstruções N3. Corrigida a associação indevida ao e-mail de Jalusa 19f3f1af06c771c3. Resultado local pronto para revisão; nenhum novo envio atribuído a esta demanda.",
    },
    "whatsapp-audio-roraima-senador-20260708": {
        "status": "pronta_para_revisao",
        "urgenciaManual": "media",
        "prazo": None,
        "prazoTexto": "dossiê de descoberta concluído; contato e contratação dependem de decisão humana",
        "resumo": "Dossiê de qualificação e ficha de reunião para possível cliente de Roraima concluídos. O produto prepara descoberta comercial e jurídica; não é proposta enviada, contrato ou petição.",
        "proximaAcao": "Fábio revisar o dossiê, validar conflito e objetivo do contato e decidir se agenda reunião de descoberta antes de qualquer proposta.",
        "evidenciaResposta": "Arquivos locais: WhatsApp Audio - Roraima Senador cliente - 2026-07-08/DOSSIE_QUALIFICACAO_CLIENTE_RORAIMA_CHICO_RODRIGUES.md e FICHA_REUNIAO_DESCOBERTA_RORAIMA.md. Nenhuma proposta ou entrega externa foi registrada.",
        "evidenciaTipo": "arquivo",
        "respondidoComConteudo": False,
        "comment": "TRIAGEM DE ÁUDIO 10/07: dossiê de qualificação e ficha de reunião concluídos. Corrigida a associação indevida ao e-mail de Jalusa. Pronto para validação humana e eventual contato; nenhuma proposta, contratação ou peça foi afirmada.",
    },
    "whatsapp-audio-protocolo-aprendizados-20260708": {
        "status": "cumprida",
        "urgenciaManual": "media",
        "prazo": None,
        "prazoTexto": "demanda interna concluída em 10/07/2026 por implementação verificável",
        "resumo": "O ciclo pós-entrega da FORJA foi formalizado: comparação entre versões, classificação da alteração humana, retrospectiva, atualização de protocolo, conversão em gate e vínculo com a demanda.",
        "proximaAcao": "Aplicar o protocolo a cada versão humana devolvida e converter novas falhas determinísticas em testes de regressão.",
        "evidenciaResposta": "Arquivo local: WhatsApp Audio - Protocolo de aprendizados IA - 2026-07-08/PROTOCOLO_POS_ENTREGA_FORJA_IMPLEMENTADO.md. Suíte geral: 49 testes aprovados; regressão de citações e telemetria real aprovadas. Conclusão interna, sem envio externo.",
        "evidenciaTipo": "arquivo",
        "respondidoComConteudo": False,
        "comment": "FORJA N3 10/07: demanda interna concluída com protocolo pós-entrega materializado e estado FORJA corrigido. O fluxo liga diff da versão humana, retrospectiva, APRENDIZADOS_FEEDBACK_HUMANO, gates e painel. Suíte geral aprovada com 49 testes; regressão de citações 6/6 e telemetria real aprovadas. Corrigida também a evidência antiga que apontava indevidamente para e-mail alheio. Nenhuma mensagem foi enviada.",
    },
    "email-natura-cabreuva-19f3991ebc75fe03": {
        "status": "aberta",
        "urgenciaManual": "alta",
        "prazo": "2026-07-20",
        "prazoTexto": "minuta solicitada até 20/07/2026; parecer final bloqueado sem o caderno documental",
        "resumo": "Roteiro jurídico interno N3 dos sete quesitos concluído e reinspecionado em 17 páginas. Helena e Cícero confirmam que o produto é adequado para investigação, mas bloqueado como parecer final.",
        "proximaAcao": "Obter acesso integral ao caderno, montar cronologia parcela a parcela, reproduzir a tese municipal e executar pesquisa oficial específica antes de responder conclusivamente aos sete quesitos.",
        "evidenciaResposta": "Arquivo local: Natura Cabreúva - Parecer e Quesitos - prazo 20-07-2026/_forja_n3_reconstrucao_2026-07-10/ROTEIRO_JURIDICO_INTERNO_NATURA_CABREUVA_N3.pdf. F7 sem achados, fidelidade 100%, 17 páginas reinspecionadas e pareceres Helena/Cícero arquivados. Não constitui parecer entregue.",
        "evidenciaTipo": "arquivo",
        "respondidoComConteudo": False,
        "comment": "FORJA N3 10/07 — fechamento Natura: roteiro interno de 17 páginas aprovado em conteúdo, fidelidade e diagramação. Cícero marcou corretamente 63,0 e BLOQUEADA para uso como parecer final, pois o caderno substantivo continua ausente. Demanda permanece aberta e focada na obtenção de documentos.",
    },
    "email-corsan-agerst-19f3dc9ff92081cd": {
        "status": "aberta",
        "urgenciaManual": "alta",
        "prazo": "2026-08-04",
        "prazoTexto": "consulta pública até 04/08/2026; audiência em 11/08/2026 às 14h; deliberação final sem data comprovada",
        "resumo": "Diagnóstico preliminar interno N3 concluído em 17 páginas, com leitura integral do Anexo Único e matriz A01-A54. Helena e Cícero confirmam utilidade interna e bloqueio de qualquer conclusão externa sem fontes originárias.",
        "proximaAcao": "Obter TAACC e anexos, Resolução nº 69/2024 e antecedentes, Processo nº 2026/061 integral, normas locais, documentos do leilão e estudos técnicos; depois responder A01-A54 antes de decidir contribuição, audiência ou parecer.",
        "evidenciaResposta": "Arquivo local: CORSAN AGERST - Proposta de Serviços Jurídicos/_forja_n3_reconstrucao_2026-07-10/DIAGNOSTICO_PRELIMINAR_INTERNO_CORSAN_AGERST_N3.pdf. F7 sem achados, A01-A54 íntegros, fidelidade 100%, 17 páginas reinspecionadas e pareceres Helena/Cícero arquivados. Não constitui entrega ao cliente.",
        "evidenciaTipo": "arquivo",
        "respondidoComConteudo": False,
        "comment": "FORJA N3 10/07 — fechamento CORSAN: diagnóstico interno de 17 páginas aprovado, com 54 linhas rastreáveis, calendário oficial e quatro SVGs sem cortes. Cícero 76,8 ALERTA preservado como sinal das fontes faltantes. Demanda permanece aberta; nenhum parecer, proposta ou manifestação externa foi declarado.",
    },
}


FORJA_OVERLAYS = {
    "email-jorge-haroldo-edcl-19f3c8200768b56e": {
        "lifecycleStatus": "ready_for_review",
        "phaseCursor": "F9_PACOTE_REVISAO",
        "completedPhases": ["F7_AUDITORIA", "F8_QA_VISUAL", "F9_PACOTE_REVISAO"],
        "gates": {"F7_AUDITORIA": {"status": "pass"}, "F8_QA_VISUAL": {"status": "pass"}},
        "blockers": ["Conferir cadeia recursal, sanção, capítulo da aposentadoria e intimação antes do protocolo."],
        "visualQa": {"reviewed": 10, "total": 10, "status": "pass"},
        "artifacts": [{"path": "Embargos AgInt AREsp 1883361 RS - Jorge Haroldo/_forja_n3_proxima_2026-07-10/MINUTA_EDCL_JORGE_HAROLDO_N3.pdf", "label": "Minuta EDcl Jorge Haroldo N3", "role": "petition", "audience": "internal_review"}],
        "deliveryEvidence": None,
    },
    "email-auto-19f3ea400b7dec3d": {
        "lifecycleStatus": "ready_for_review",
        "phaseCursor": "F9_PACOTE_REVISAO",
        "completedPhases": ["F7_AUDITORIA", "F8_QA_VISUAL", "F9_PACOTE_REVISAO"],
        "gates": {"F7_AUDITORIA": {"status": "pass"}, "F8_QA_VISUAL": {"status": "pass"}},
        "blockers": ["Confirmar cargo pretendido, expedientes do CNMP e cadeia integral do processo eleitoral."],
        "visualQa": {"reviewed": 21, "total": 21, "status": "pass"},
        "artifacts": [{"path": "Material para elaboração de parecer - interessado Deltan Dallagnol/_forja_n3_proxima_2026-07-10/PARECER_DELTAN_N3.pdf", "label": "Parecer Deltan N3", "role": "opinion", "audience": "internal_review"}],
        "deliveryEvidence": None,
    },
    "email-auto-19f3f25cb64df962": {
        "lifecycleStatus": "ready_for_review",
        "phaseCursor": "F9_PACOTE_REVISAO",
        "completedPhases": ["F7_AUDITORIA", "F8_QA_VISUAL", "F9_PACOTE_REVISAO"],
        "gates": {"F7_AUDITORIA": {"status": "pass"}, "F8_QA_VISUAL": {"status": "pass"}, "CICERO": {"status": "pass", "score": 90.1}},
        "blockers": ["Conferir mandato, assistência, anexos físicos e eventual relatório bucomaxilofacial antes do protocolo."],
        "visualQa": {"reviewed": 15, "total": 15, "status": "pass"},
        "artifacts": [{"path": "Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/_forja_n3_reconstrucao_2026-07-10/PETICAO_INICIAL_TJDFT_MATEUS_NIVEL_SOL_V6_N3_10-07-2026.pdf", "label": "Petição inicial Mateus V6 N3", "role": "petition", "audience": "internal_review"}],
        "deliveryEvidence": None,
    },
    "email-auto-19f3ed5bdbdcf159": {
        "lifecycleStatus": "ready_for_review",
        "phaseCursor": "F9_PACOTE_REVISAO",
        "completedPhases": ["F7_AUDITORIA", "F8_QA_VISUAL", "F9_PACOTE_REVISAO"],
        "gates": {"F7_AUDITORIA": {"status": "pass"}, "F8_QA_VISUAL": {"status": "pass"}},
        "blockers": ["Obter os sete grupos documentais listados antes do protocolo."],
        "visualQa": {"reviewed": 8, "total": 8, "status": "pass"},
        "artifacts": [{"path": "Re Relatório Azimut/_forja_n3_reconstrucao_2026-07-10/MEMORIAL_AZIMUT_N3_MINUTA_INTERNA_CONDICIONADA.pdf", "label": "Memorial Azimut N3 condicionado", "role": "memorial", "audience": "internal_review"}],
        "deliveryEvidence": None,
    },
    "email-libra-sul-agint-stj-19f3c9350d875062": {
        "lifecycleStatus": "ready_for_review",
        "phaseCursor": "F9_PACOTE_REVISAO",
        "completedPhases": ["F7_AUDITORIA", "F8_QA_VISUAL", "F9_PACOTE_REVISAO"],
        "gates": {"F7_AUDITORIA": {"status": "pass"}, "F8_QA_VISUAL": {"status": "pass"}},
        "blockers": ["Confirmar pauta, modalidade, data do fecho e forma de entrega antes do protocolo."],
        "visualQa": {"reviewed": 7, "total": 7, "status": "pass"},
        "artifacts": [{"path": "Memoriais AgInt AREsp 2578181 SC - LIBRA SUL/_forja_n3_reconstrucao_2026-07-10/MEMORIAIS_LIBRA_SUL_N3_SUPERIOR.pdf", "label": "Memoriais Libra Sul N3", "role": "memorial", "audience": "internal_review"}],
        "deliveryEvidence": None,
    },
    "email-patricia-fabio-memoriais-19f3c68ee6d8fef2": {
        "lifecycleStatus": "ready_for_review",
        "phaseCursor": "F9_PACOTE_REVISAO",
        "completedPhases": ["F7_AUDITORIA", "F8_QA_VISUAL", "F9_PACOTE_REVISAO"],
        "gates": {"F7_AUDITORIA": {"status": "pass"}, "F8_QA_VISUAL": {"status": "pass"}},
        "blockers": ["Revisar e decidir a substituição formal dos anexos anteriormente enviados."],
        "visualQa": {"reviewed": 6, "total": 6, "status": "pass"},
        "artifacts": [{"path": "Memoriais Apelação Patrícia e Fábio - Proc. 0014560-09.2014.8.19.0209/_forja_n3_reconstrucao_2026-07-10/MEMORIAIS_PATRICIA_FABIO_N3_SUPERIOR.pdf", "label": "Memoriais Patrícia e Fábio N3", "role": "memorial", "audience": "internal_review"}],
        "deliveryEvidence": None,
    },
    "whatsapp-audio-cafelana-prevencao-20260708": {
        "lifecycleStatus": "ready_for_review",
        "phaseCursor": "F9_PACOTE_REVISAO",
        "completedPhases": ["F7_AUDITORIA", "F8_QA_VISUAL", "F9_PACOTE_REVISAO"],
        "gates": {"F7_AUDITORIA": {"status": "pass"}, "F8_QA_VISUAL": {"status": "pass"}},
        "blockers": ["Revisar as duas versões N3 e decidir eventual substituição das entregas anteriores."],
        "visualQa": {"reviewed": 19, "total": 19, "status": "pass"},
        "artifacts": [
            {"path": "Cafelana/_forja_n3_edcl_reabertura_2026-07-10/MINUTA_CAFELANA_EDCL_N3.pdf", "label": "Cafelana EDcl N3", "role": "petition", "audience": "internal_review"},
            {"path": "Cafelana/contrarrazões ao AgInt no AREsp nº 2.698.443D/_forja_n3_reabertura_2026-07-10/MINUTA_CAFELANA_AGINT_N3.pdf", "label": "Cafelana AgInt N3", "role": "petition", "audience": "internal_review"},
        ],
        "deliveryEvidence": None,
    },
    "whatsapp-audio-roraima-senador-20260708": {
        "lifecycleStatus": "ready_for_review",
        "phaseCursor": "F4_BLUEPRINT",
        "completedPhases": ["F0_RECONCILIACAO_FILA", "F2_CLASSIFICACAO", "F4_BLUEPRINT"],
        "gates": {"ESCOPO_DESCOBERTA": {"status": "pass"}},
        "blockers": [],
        "visualQa": {"reviewed": 0, "total": 0, "status": "not_applicable"},
        "artifacts": [
            {"path": "WhatsApp Audio - Roraima Senador cliente - 2026-07-08/DOSSIE_QUALIFICACAO_CLIENTE_RORAIMA_CHICO_RODRIGUES.md", "label": "Dossiê de qualificação Roraima", "role": "discovery", "audience": "internal_review"},
            {"path": "WhatsApp Audio - Roraima Senador cliente - 2026-07-08/FICHA_REUNIAO_DESCOBERTA_RORAIMA.md", "label": "Ficha de reunião Roraima", "role": "discovery", "audience": "internal_review"},
        ],
        "deliveryEvidence": None,
    },
    "whatsapp-audio-protocolo-aprendizados-20260708": {
        "lifecycleStatus": "fulfilled_by_reconciliation",
        "phaseCursor": "F10_APRENDIZADO_CONCLUIDO",
        "completedPhases": ["F10_APRENDIZADO_CONCLUIDO"],
        "gates": {"IMPLEMENTACAO_INTERNA": {"status": "pass"}},
        "blockers": [],
        "visualQa": {"reviewed": 0, "total": 0, "status": "not_applicable"},
        "artifacts": [{"path": "WhatsApp Audio - Protocolo de aprendizados IA - 2026-07-08/PROTOCOLO_POS_ENTREGA_FORJA_IMPLEMENTADO.md", "label": "Protocolo pós-entrega FORJA", "role": "protocol", "audience": "internal"}],
        "deliveryEvidence": {"status": "internal_implementation_verified", "detail": "Protocolo interno implementado; não houve envio externo."},
    },
    "email-natura-cabreuva-19f3991ebc75fe03": {
        "lifecycleStatus": "blocked",
        "phaseCursor": "F9_PACOTE_REVISAO_CONDICIONADO",
        "completedPhases": ["F7_AUDITORIA", "F8_QA_VISUAL", "F9_PACOTE_REVISAO_CONDICIONADO"],
        "gates": {"F7_AUDITORIA": {"status": "pass"}, "F8_QA_VISUAL": {"status": "pass"}, "CADERNO_DOCUMENTAL": {"status": "p1"}},
        "blockers": ["Caderno documental substantivo não acessado; parecer final não pode ser produzido."],
        "visualQa": {"reviewed": 17, "total": 17, "status": "pass"},
        "artifacts": [{"path": "Natura Cabreúva - Parecer e Quesitos - prazo 20-07-2026/_forja_n3_reconstrucao_2026-07-10/ROTEIRO_JURIDICO_INTERNO_NATURA_CABREUVA_N3.pdf", "label": "Roteiro jurídico Natura N3", "role": "internal_method", "audience": "internal_review"}],
        "deliveryEvidence": None,
    },
    "email-corsan-agerst-19f3dc9ff92081cd": {
        "lifecycleStatus": "blocked",
        "phaseCursor": "F9_PACOTE_REVISAO_CONDICIONADO",
        "completedPhases": ["F7_AUDITORIA", "F8_QA_VISUAL", "F9_PACOTE_REVISAO_CONDICIONADO"],
        "gates": {"F7_AUDITORIA": {"status": "pass"}, "F8_QA_VISUAL": {"status": "pass"}, "FONTES_ORIGINARIAS": {"status": "p1"}},
        "blockers": ["TAACC, processos, normas locais e documentos técnicos originários ainda faltam para conclusão externa."],
        "visualQa": {"reviewed": 17, "total": 17, "status": "pass"},
        "artifacts": [{"path": "CORSAN AGERST - Proposta de Serviços Jurídicos/_forja_n3_reconstrucao_2026-07-10/DIAGNOSTICO_PRELIMINAR_INTERNO_CORSAN_AGERST_N3.pdf", "label": "Diagnóstico CORSAN/AGERST N3", "role": "diagnostic", "audience": "internal_review"}],
        "deliveryEvidence": None,
    },
}


def main() -> None:
    manual = read_json(MANUAL, {"schema": 1, "updatedAt": now_iso(), "items": {}})
    manual.setdefault("schema", 1)
    items = manual.setdefault("items", {})
    stamp = now_iso()
    changed = 0

    for item_id, update in UPDATES.items():
        entry_changed = False
        entry = items.setdefault(item_id, {"comentarios": [], "overrides": {}})
        comments = entry.setdefault("comentarios", [])
        comment_id = f"forja-n3-fechamento-20260710-{item_id}"
        if not any(comment.get("id") == comment_id for comment in comments):
            comments.append({
                "id": comment_id,
                "at": stamp,
                "tipo": "forja-n3-producao",
                "texto": update["comment"],
                "autor": "FORJA N3/Codex",
            })
            changed += 1
            entry_changed = True

        overrides = entry.setdefault("overrides", {})
        for key in (
            "status", "urgenciaManual", "prazo", "prazoTexto", "resumo",
            "proximaAcao", "evidenciaResposta", "evidenciaTipo",
        ):
            if overrides.get(key) != update[key]:
                overrides[key] = update[key]
                changed += 1
                entry_changed = True
        responded = bool(update.get("respondidoComConteudo", False))
        if overrides.get("respondidoComConteudo") is not responded:
            overrides["respondidoComConteudo"] = responded
            changed += 1
            entry_changed = True
        forja = FORJA_OVERLAYS.get(item_id)
        if forja is not None:
            forja = copy.deepcopy(forja)
            forja.setdefault("nextAction", update["proximaAcao"])
            if entry.get("forja") != forja:
                entry["forja"] = forja
                changed += 1
                entry_changed = True
        if entry_changed:
            entry["updatedAt"] = stamp

    if changed:
        manual["updatedAt"] = stamp
        atomic_write_json(MANUAL, manual)
    print({"ok": True, "changed": changed, "items": len(UPDATES)})


if __name__ == "__main__":
    main()
