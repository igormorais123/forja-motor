Você é o revisor visual cruzado adversarial da FORJA. Modelo solicitado: claude-opus-5.

Revise exclusivamente a versão recomposta do relatório CORSAN N5. Cafelana está fora do escopo e não deve ser aberta. A rodada anterior encontrou quatro P1 visuais: página em branco, capa rompida pela síntese, fragmentação mecânica das tabelas e aberturas de seção órfãs. Confirme diretamente se todos foram corrigidos sem perda de fidelidade.

Arquivos obrigatórios:

1. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/ADITAMENTO_INTERNO_N5_IMOVEL_SANTA_CRUZ_PA67_AI35.md`
2. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/ADITAMENTO_INTERNO_N5_IMOVEL_SANTA_CRUZ_PA67_AI35_V2_AJUSTADO_VISUAL.docx`
3. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/ADITAMENTO_INTERNO_N5_IMOVEL_SANTA_CRUZ_PA67_AI35_V2_AJUSTADO_VISUAL.pdf`
4. `CORSAN AGERST - Proposta de Serviços Jurídicos/_integracao_santa_cruz_2026-07-30/MAPA_VISUAL_V2_CORSAN_N5.json`
5. As 59 imagens `qa_v2_ajustado_visual/p01.png` a `p59.png`; abra e inspecione todas, não apenas os contatos.
6. Os dois SVG e os dois EMF embutidos no DOCX.

Verificações bloqueantes:

- hashes do DOCX e PDF iguais aos do manifesto `_FORJA_HARNESS/reports/manifest_visual_lote_20260730.json`;
- exatamente 59 páginas e nenhuma página inteiramente vazia;
- capa autônoma e íntegra; síntese começando na página 2;
- nenhuma abertura de seção ou subseção órfã no rodapé;
- tabelas fluindo continuamente, sem rótulos “Bloco N”, sem quebras forçadas por contagem fixa e sem páginas estruturalmente vazias;
- linhas de tabela podem atravessar página quando necessário, mas não podem apresentar corte, sobreposição, perda de cabeçalho, texto ilegível ou confusão de coluna;
- dois diagramas EMF dentro do corpo, legíveis, sem overflow;
- nenhuma alteração ou omissão de conteúdo em relação ao markdown congelado;
- nenhum placeholder ou origem operacional indevida.

P0 e P1 bloqueiam. Espaço de encerramento natural na última página pode ser P2 se o conteúdo estiver íntegro. Responda com um único JSON válido, sem markdown:

{
  "reviewerModelRequested": "claude-opus-5",
  "reviewType": "cross_family_visual_rereview",
  "filesRead": [],
  "pagesReviewed": [],
  "findings": [{"severity":"P0|P1|P2|P3","location":"...","finding":"...","requiredFix":"..."}],
  "p0Count": 0,
  "p1Count": 0,
  "releaseRecommendation": "BLOCKED|APPROVED_WITH_MINOR_NOTES|APPROVED",
  "fidelityConclusion": "...",
  "visualConclusion": "..."
}
