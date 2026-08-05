# REVISÃO CRUZADA FORJA — CORSAN N5

Você é o revisor jurídico-editorial adversarial de um relatório interno. Leia integralmente:

1. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/ADITAMENTO_INTERNO_N5_IMOVEL_SANTA_CRUZ_PA67_AI35.md`;
2. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/fontes_zip/texto_extraido/TRASLADO_COMPRA_E_VENDAE_5591_LIVRO_E_0013_FOLHA_087_VersaoImpressao__91312bd992.txt`;
3. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/fontes_zip/texto_extraido/Auto_de_Infração___35_2026__2b7e3d7905.txt`;
4. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/fontes_zip/texto_extraido/Parecer_273_PGM_2026___Proc__Adm__67_2026___Fiscalização___Venda_Sede_Administra__0566acdba5.txt`;
5. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/fontes_zip/texto_extraido/008610031062026_377_379__c9c5563b11.txt`;
6. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/ocr_zip_chave/OCR_LEDGER.jsonl`;
7. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/ocr/OCR_LEDGER.jsonl`;
8. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/fontes_zip/msg_anexos/CORSAN - Santa Cruz do Sul - Resposta ao Ofício 0330-2026 - PGM (05.05.2026) V2.docx.pdf`;
9. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/fontes_zip/INDICE_PDFS.jsonl`;
10. `CORSAN AGERST - Proposta de Serviços Jurídicos/_indexacao_283_folios_2026-07-29/RELATORIO_FINAL_INDEXACAO_E_DIAGNOSTICO_CORSAN_PROCON_283_FOLIOS.md`.
11. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/fontes_zip/extraido/Imóvel - Medina/13. Dívida ativa/Notificação 914.26 - Divida Ativa - AGERST.pdf`;
12. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/fontes_zip/extraido/Imóvel - Medina/11. Multa da AGERST/Despacho decisório 35.26- processo adm punitivo 67.26.pdf`.
13. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/ocr/paginas/Oficio 330.26_p0002.jpg`;
14. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/fontes_zip/extraido/Imóvel - Medina/Corsan AGERST - linha do tempo imóvel.pptx`.

Objetivo: detectar erros materiais, afirmações sem lastro, confusão entre fato e alegação, risco de misturar processos autônomos, omissões que mudem a decisão, inconsistência de datas/valores/identidades e inadequação do escopo comercial.

Cheque obrigatoriamente:

- compradora correta: escritura/matrícula versus “Incorporações” nos atos da AGERST;
- vínculo e possível inconsistência entre os números 162/2024 e 2026/67;
- existência ou não, no lote, do recurso alegado em 23/04/2026 e de decisão recursal;
- distinção entre AI nº 35/débitos 700747-700748 e a multa PROCON/CDA nº 1542/2026;
- valor do AI (R$ 82.965,73), valor atualizado da dívida ativa (R$ 88.242,68) e limites da prova;
- objeto e diligências do MPRS, sem converter investigação em culpa;
- se os prazos e providências recomendados estão formulados de modo seguro e operacional;
- se a redação deixa claro o que foi leitura primária, OCR, alegação, inferência e lacuna.
- confirme no PDF original da Notificação nº 914, e não apenas no bloco OCR de baixa confiança, o valor impresso, o vencimento e o texto sobre protesto;
- verifique se todos os achados P0/P1 da revisão anterior foram efetivamente corrigidos, sem criar nova confusão entre a tese oficial de reversibilidade e o risco interno de preferência.

Responda exclusivamente em JSON válido, sem markdown:

{
  "verdict": "approved|approved_with_p2|blocked",
  "p0": [{"finding": "...", "evidence": "...", "fix": "..."}],
  "p1": [{"finding": "...", "evidence": "...", "fix": "..."}],
  "p2": [{"finding": "...", "evidence": "...", "fix": "..."}],
  "fidelity": {
    "facts_preserved": true,
    "allegations_separated": true,
    "process_identity_safe": true,
    "amounts_safe": true,
    "scope_safe": true
  },
  "summary": "..."
}
