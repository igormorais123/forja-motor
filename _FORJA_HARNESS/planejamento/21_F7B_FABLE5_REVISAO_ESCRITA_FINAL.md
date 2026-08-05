# Decisão arquitetural 21 — F7-B com Claude Fable 5

**Status:** aceita e implementada  
**Data:** 15/07/2026  
**Contrato:** `FORJA-FABLE5-FINAL-v1`

## Contexto

A FORJA já separava redação, auditoria jurídica/factual e composição visual, mas o texto protocolável não possuía um passe editorial final especializado, comprovadamente executado pelo modelo de escrita escolhido pelo Igor. Inserir um novo redator depois de F8 criaria risco de divergência entre texto aprovado e documento diagramado; inseri-lo antes de F7 permitiria que a auditoria consumisse energia revisando linguagem ainda provisória e não garantiria que o resultado final mantivesse o mesmo nível editorial.

## Decisão

Criar `F7-B_REVISAO_EDITORIAL_ESCRITA_FINAL` dentro de `F7_AUDITORIA_JURIDICA_FACTUAL`, depois do gate jurídico/factual sem P0 e imediatamente antes de F8.

O Claude Fable 5 atua como produtor editorial. O orquestrador local atua como verificador independente. A saída só se torna `final_markdown` quando autenticação, modelo, hash de origem, fidelidade e estilo humano são recompostos e aprovados por código.

A chamada é controlada pelo operador/workflow. `forja_run.py` não invoca o Fable; `FABLE5_RESULT*.json` é apenas um fragmento cujos artefatos e gates são fundidos ao `PHASE_RESULT.json` completo de F7, preservando os papéis contratuais da fase.

## Razões

- preserva a numeração histórica F0–F10;
- mantém F7 como fronteira de aprovação textual;
- garante que F8 consuma exatamente o texto final;
- aproveita a assinatura Claude Max sem instituir custo de API;
- permite auditoria por diff, hashes e uso da sessão;
- falha fechado quando o modelo altera conteúdo material.

## Alternativas rejeitadas

### Nova fase F8 e renumeração das demais

Rejeitada porque quebraria estados, relatórios, contratos e consumidores históricos. Uma subfase bloqueante expressa a mudança sem migração destrutiva.

### API Anthropic com chave

Rejeitada porque o pedido é usar a assinatura Claude do Igor e evitar custo recorrente inesperado. O fluxo exige Claude Code OAuth Max e não oferece fallback pago.

### Aceitar a autocertificação do modelo

Rejeitada porque o mesmo agente que escreve não pode ser a única fonte de aprovação. O relatório do Fable é evidência auxiliar; hashes e invariantes são recalculados localmente.

### Reescrever a tentativa anterior após falha

Rejeitada porque edições sucessivas acumulam deriva. Todo retry retorna à origem auditada imutável e recebe apenas os achados da tentativa rejeitada.

### Apenas lint estilístico determinístico

Rejeitada como solução completa porque detectores de vício não produzem a qualidade de prosa pretendida. O lint continua como gate, enquanto o Fable 5 executa a transformação editorial.

## Contrato de dados

Entrada mínima:

- `audited_markdown*`;
- resultado de F7 sem P0;
- identidade do caso e diretório de tentativa.

Saída mínima:

- `final_markdown*`;
- `editorial_report*`;
- `editorial_diff*`;
- `fable5_usage*`;
- `editorial_fidelity*`;
- gates `fable5_oauth_confirmed`, `editorial_source_hash_match`, `editorial_fidelity_pass` e `human_style_final_pass`.

O asterisco representa um sufixo opcional comum ao bundle quando a tentativa contém vários documentos.

## Implementação

- `forja_fable5.py`: autenticação, chamada sem ferramentas, parsing, retry e persistência.
- `forja_editorial_fidelity.py`: comparação e invariantes independentes.
- `forja_run.py`: validação de todos os bundles antes da promoção.
- `forja_package.py`: revalidação do bundle do entregável escolhido.
- `phase_contracts/F7.json`: artefatos e gates obrigatórios.
- `phase_contracts/F8.json`: consumo de `final_markdown` com trilha auditada.
- `FORJA_N3_CONFIG.json`: capacidade `fable5FinalWritingV1`.

## Compatibilidade e implantação

Estados e pacotes históricos permanecem legíveis. A obrigação vale para tentativas F7 criadas sob o contrato atualizado. Não há migração automática de textos históricos e nenhum arquivo anterior é reescrito.

Rollback lógico: desabilitar a orquestração de novas chamadas e preservar todos os artefatos já produzidos. A retirada definitiva do contrato exige decisão explícita, pois F8 e o pacote novo passaram a depender de `final_markdown*`.

## Evidência de aceite

- revisão arquitetural e pós-implementação pelo próprio Claude/Fable;
- correção dos achados materiais levantados na revisão;
- regressão integrada de 42/42 testes em 15/07/2026;
- execução viva sobre peça auditada de aproximadamente 36 KB;
- confirmação de OAuth Claude Max, modelo `claude-fable-5`, hash de origem e quatro gates;
- resultado aprovado na primeira tentativa do ensaio vivo.

## Riscos residuais

- equivalência semântica perfeita não é decidível por checks lexicais;
- o gate atual não cobre toda mudança factual sem números, adição de conteúdo, aspas simples ou pedido sem heading reconhecido;
- mudanças futuras do envelope do Claude Code podem exigir adaptação;
- textos muito grandes podem atingir limite operacional ou timeout;
- a qualidade final ainda depende da qualidade jurídica da origem auditada;
- revisão humana continua obrigatória antes de protocolo ou entrega externa.

## Consequências documentais

Toda mudança futura em modelo, autenticação, artefatos, invariantes, retry ou consumidor final deve atualizar, no mesmo ciclo:

- `PROTOCOLO_FABLE5_ESCRITA_FINAL.md`;
- `docs/ARCHITECTURE.md`, `docs/CONFIGURATION.md` e `docs/TESTING.md`;
- `DOCUMENTACAO_TECNICA.md` e `INDICE_FORJA.md`;
- `FORJA_SPEC_MANIFEST.json` e contratos;
- `RETROSPECTIVAS.md` quando houver aprendizado reutilizável.
