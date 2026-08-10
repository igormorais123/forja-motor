# Consulta IA — Decisão arquitetural 21 — F7-B com Claude Fable 5

> Cópia de consulta derivada. O documento canônico permanece no caminho de origem indicado abaixo.

## Metadados e rastreabilidade

- **Documento de origem:** `21_F7B_FABLE5_REVISAO_ESCRITA_FINAL.md`
- **Tipo:** Documento de planejamento
- **SHA-256 da origem:** `a5af7bf254019291684834bb33479ee49788325a478a53be71129ddd2c215c38`
- **Linhas da origem:** 111
- **Blocos integralmente indexados:** 16
- **Geração:** 2026-08-10T13:53:35-03:00
- **Cobertura:** 100% das linhas e do texto da origem, sem omissão.
- **Links relativos normalizados:** 0 destino(s), apenas para preservar a navegação na cópia.

## Roteiro de consulta para IA

**Síntese de localização:** Status: aceita e implementada Data: 15/07/2026 Contrato: FORJA-FABLE5-FINAL-v1

**Termos de recuperação:** claude, não, fable, modelo, decisão, tentativa, json, rejeitada, contrato, final, porque, arquitetural.

Use o índice abaixo para localizar o bloco pertinente. Cada entrada informa as linhas exatas no documento de origem. Para afirmações materiais, leia o bloco integral e confira o arquivo canônico pelo SHA-256.

## Índice detalhado e cobertura integral

- [SRC-S001 · L1–L6 · Decisão arquitetural 21 — F7-B com Claude Fable 5](#src-s001)
  - Assuntos: decisão, arquitetural, f7-b, claude, fable, status, aceita, implementada
  - Trecho-guia: Status: aceita e implementada Data: 15/07/2026 Contrato: FORJA-FABLE5-FINAL-v1
  - SHA-256 do bloco: `f4d63f6e01174758122f8acec6a577df0c07a661404e9df450995191c14c25ea`
  - [SRC-S002 · L7–L10 · Contexto](#src-s002)
    - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Contexto
    - Assuntos: contexto, auditoria, texto, não, editorial, final, pelo, separava
    - Trecho-guia: A FORJA já separava redação, auditoria jurídica/factual e composição visual, mas o texto protocolável não possuía um passe editorial final especializado, comprovadamente executado pelo modelo de escrita escolhido pelo Igor. Inserir um novo redator depois de F8 criaria risco de di
    - SHA-256 do bloco: `5cd4626b15659708ba92bfe0c140b40daf9fe5b200f755ff7b27c7a42e964f1a`
  - [SRC-S003 · L11–L18 · Decisão](#src-s003)
    - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Decisão
    - Assuntos: decisão, fable, atua, são, json, criar, f7-b_revisao_editorial_escrita_final, dentro
    - Trecho-guia: Criar F7-BREVISAOEDITORIALESCRITAFINAL dentro de F7AUDITORIAJURIDICAFACTUAL, depois do gate jurídico/factual sem P0 e imediatamente antes de F8.
    - SHA-256 do bloco: `c3acd2c14ddabd6e3c583e873ff2a2fbfa033c6a04b742edc0beae2c1e15c9f2`
  - [SRC-S004 · L19–L27 · Razões](#src-s004)
    - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Razões
    - Assuntos: razões, preserva, numeração, histórica, f10, mantém, fronteira, aprovação
    - Trecho-guia: preserva a numeração histórica F0–F10; mantém F7 como fronteira de aprovação textual; garante que F8 consuma exatamente o texto final; aproveita a assinatura Claude Max sem instituir custo de API; permite auditoria por diff, hashes e uso da sessão; falha fechado quando o modelo a
    - SHA-256 do bloco: `b9865b6a864fd8651daf7ca517a3a302c482462d565150b493c740c775dd04c2`
  - [SRC-S005 · L28–L29 · Alternativas rejeitadas](#src-s005)
    - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Alternativas rejeitadas
    - Assuntos: alternativas, rejeitadas
    - Trecho-guia: Documento de consulta sobre Alternativas rejeitadas.
    - SHA-256 do bloco: `7da7d2d78ff1eb457c0711a5001d59070e81d385585e42968fde410adbc09b02`
    - [SRC-S006 · L30–L33 · Nova fase F8 e renumeração das demais](#src-s006)
      - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Alternativas rejeitadas > Nova fase F8 e renumeração das demais
      - Assuntos: nova, fase, renumeração, demais, rejeitada, porque, quebraria, estados
      - Trecho-guia: Rejeitada porque quebraria estados, relatórios, contratos e consumidores históricos. Uma subfase bloqueante expressa a mudança sem migração destrutiva.
      - SHA-256 do bloco: `7b5833a9a9aaf12ea93d428f90850557d23ac171805afb1574a2320474c826ac`
    - [SRC-S007 · L34–L37 · API Anthropic com chave](#src-s007)
      - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Alternativas rejeitadas > API Anthropic com chave
      - Assuntos: api, anthropic, chave, claude, rejeitada, porque, pedido, usar
      - Trecho-guia: Rejeitada porque o pedido é usar a assinatura Claude do Igor e evitar custo recorrente inesperado. O fluxo exige Claude Code OAuth Max e não oferece fallback pago.
      - SHA-256 do bloco: `39ff02f47f2e40c8d439f12ceded9b9601f503db1bdc7bda76895c1c797f3fb1`
    - [SRC-S008 · L38–L41 · Aceitar a autocertificação do modelo](#src-s008)
      - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Alternativas rejeitadas > Aceitar a autocertificação do modelo
      - Assuntos: aceitar, autocertificação, modelo, rejeitada, porque, mesmo, agente, escreve
      - Trecho-guia: Rejeitada porque o mesmo agente que escreve não pode ser a única fonte de aprovação. O relatório do Fable é evidência auxiliar; hashes e invariantes são recalculados localmente.
      - SHA-256 do bloco: `428cc16ef27193324efd52fc12a7f05a15cd4c78386f28164e7689a7fa2b73b9`
    - [SRC-S009 · L42–L45 · Reescrever a tentativa anterior após falha](#src-s009)
      - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Alternativas rejeitadas > Reescrever a tentativa anterior após falha
      - Assuntos: tentativa, reescrever, anterior, após, falha, rejeitada, porque, edições
      - Trecho-guia: Rejeitada porque edições sucessivas acumulam deriva. Todo retry retorna à origem auditada imutável e recebe apenas os achados da tentativa rejeitada.
      - SHA-256 do bloco: `9f3289ffab24e74f86734b31dadc92ab6de203f31dde0db95015c4f969cc75fd`
    - [SRC-S010 · L46–L49 · Apenas lint estilístico determinístico](#src-s010)
      - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Alternativas rejeitadas > Apenas lint estilístico determinístico
      - Assuntos: lint, apenas, estilístico, determinístico, rejeitada, solução, completa, porque
      - Trecho-guia: Rejeitada como solução completa porque detectores de vício não produzem a qualidade de prosa pretendida. O lint continua como gate, enquanto o Fable 5 executa a transformação editorial.
      - SHA-256 do bloco: `e21e1ab51116153f38feef72fb6dc636790ed0f811b08b79ceb955e5ff1b0af5`
  - [SRC-S011 · L50–L68 · Contrato de dados](#src-s011)
    - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Contrato de dados
    - Assuntos: contrato, dados, mínima, tentativa, entrada, audited_markdown, resultado, identidade
    - Trecho-guia: auditedmarkdown; resultado de F7 sem P0; identidade do caso e diretório de tentativa.
    - SHA-256 do bloco: `0b78a2f529b2ff4a256e0bd9c63c5d7e3fa91dd490f44e046d513faa9a536080`
  - [SRC-S012 · L69–L78 · Implementação](#src-s012)
    - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Implementação
    - Assuntos: json, implementação, phase_contracts, forja_fable5, autenticação, chamada, ferramentas, parsing
    - Trecho-guia: forjafable5.py: autenticação, chamada sem ferramentas, parsing, retry e persistência. forjaeditorialfidelity.py: comparação e invariantes independentes. forjarun.py: validação de todos os bundles antes da promoção. forjapackage.py: revalidação do bundle do entregável escolhido. p
    - SHA-256 do bloco: `804d5f83ca6a0246aecddb333442d052d1a577e517b440624147b5a51a5e3115`
  - [SRC-S013 · L79–L84 · Compatibilidade e implantação](#src-s013)
    - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Compatibilidade e implantação
    - Assuntos: compatibilidade, implantação, históricos, contrato, estados, pacotes, permanecem, legíveis
    - Trecho-guia: Estados e pacotes históricos permanecem legíveis. A obrigação vale para tentativas F7 criadas sob o contrato atualizado. Não há migração automática de textos históricos e nenhum arquivo anterior é reescrito.
    - SHA-256 do bloco: `d21cedff3c81fae711ba8faa180dfca98e43e2b3f98e60e242830527e64cbd14`
  - [SRC-S014 · L85–L93 · Evidência de aceite](#src-s014)
    - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Evidência de aceite
    - Assuntos: evidência, aceite, revisão, claude, arquitetural, pós-implementação, pelo, próprio
    - Trecho-guia: revisão arquitetural e pós-implementação pelo próprio Claude/Fable; correção dos achados materiais levantados na revisão; regressão integrada de 42/42 testes em 15/07/2026; execução viva sobre peça auditada de aproximadamente 36 KB; confirmação de OAuth Claude Max, modelo claude-
    - SHA-256 do bloco: `d2e0356078c4752bd73f5e920f87acb83a735a5c942740abd29b3ccbdd641cd2`
  - [SRC-S015 · L94–L102 · Riscos residuais](#src-s015)
    - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Riscos residuais
    - Assuntos: riscos, residuais, não, podem, qualidade, equivalência, semântica, perfeita
    - Trecho-guia: equivalência semântica perfeita não é decidível por checks lexicais; o gate atual não cobre toda mudança factual sem números, adição de conteúdo, aspas simples ou pedido sem heading reconhecido; mudanças futuras do envelope do Claude Code podem exigir adaptação; textos muito gran
    - SHA-256 do bloco: `73871dc98a6ddcc041b72713b946dc4e461305c970dc751d3125506f8c189b76`
  - [SRC-S016 · L103–L111 · Consequências documentais](#src-s016)
    - Caminho: Decisão arquitetural 21 — F7-B com Claude Fable 5 > Consequências documentais
    - Assuntos: docs, consequências, documentais, toda, mudança, futura, modelo, autenticação
    - Trecho-guia: Toda mudança futura em modelo, autenticação, artefatos, invariantes, retry ou consumidor final deve atualizar, no mesmo ciclo:
    - SHA-256 do bloco: `9f04d461ca6bb456747c8416d3e19fd02eff2189690c50b1e59bf9dbee245cd3`

## Conteúdo integral indexado

Os marcadores HTML abaixo são apenas âncoras de navegação. O texto reproduz integralmente a origem normalizada em UTF-8; somente destinos de links relativos podem ter sido recalculados para apontar ao mesmo arquivo a partir desta pasta.

<a id="src-s001"></a>

# Decisão arquitetural 21 — F7-B com Claude Fable 5

**Status:** aceita e implementada  
**Data:** 15/07/2026  
**Contrato:** `FORJA-FABLE5-FINAL-v1`


<a id="src-s002"></a>

## Contexto

A FORJA já separava redação, auditoria jurídica/factual e composição visual, mas o texto protocolável não possuía um passe editorial final especializado, comprovadamente executado pelo modelo de escrita escolhido pelo Igor. Inserir um novo redator depois de F8 criaria risco de divergência entre texto aprovado e documento diagramado; inseri-lo antes de F7 permitiria que a auditoria consumisse energia revisando linguagem ainda provisória e não garantiria que o resultado final mantivesse o mesmo nível editorial.


<a id="src-s003"></a>

## Decisão

Criar `F7-B_REVISAO_EDITORIAL_ESCRITA_FINAL` dentro de `F7_AUDITORIA_JURIDICA_FACTUAL`, depois do gate jurídico/factual sem P0 e imediatamente antes de F8.

O Claude Fable 5 atua como produtor editorial. O orquestrador local atua como verificador independente. A saída só se torna `final_markdown` quando autenticação, modelo, hash de origem, fidelidade e estilo humano são recompostos e aprovados por código.

A chamada é controlada pelo operador/workflow. `forja_run.py` não invoca o Fable; `FABLE5_RESULT*.json` é apenas um fragmento cujos artefatos e gates são fundidos ao `PHASE_RESULT.json` completo de F7, preservando os papéis contratuais da fase.


<a id="src-s004"></a>

## Razões

- preserva a numeração histórica F0–F10;
- mantém F7 como fronteira de aprovação textual;
- garante que F8 consuma exatamente o texto final;
- aproveita a assinatura Claude Max sem instituir custo de API;
- permite auditoria por diff, hashes e uso da sessão;
- falha fechado quando o modelo altera conteúdo material.


<a id="src-s005"></a>

## Alternativas rejeitadas


<a id="src-s006"></a>

### Nova fase F8 e renumeração das demais

Rejeitada porque quebraria estados, relatórios, contratos e consumidores históricos. Uma subfase bloqueante expressa a mudança sem migração destrutiva.


<a id="src-s007"></a>

### API Anthropic com chave

Rejeitada porque o pedido é usar a assinatura Claude do Igor e evitar custo recorrente inesperado. O fluxo exige Claude Code OAuth Max e não oferece fallback pago.


<a id="src-s008"></a>

### Aceitar a autocertificação do modelo

Rejeitada porque o mesmo agente que escreve não pode ser a única fonte de aprovação. O relatório do Fable é evidência auxiliar; hashes e invariantes são recalculados localmente.


<a id="src-s009"></a>

### Reescrever a tentativa anterior após falha

Rejeitada porque edições sucessivas acumulam deriva. Todo retry retorna à origem auditada imutável e recebe apenas os achados da tentativa rejeitada.


<a id="src-s010"></a>

### Apenas lint estilístico determinístico

Rejeitada como solução completa porque detectores de vício não produzem a qualidade de prosa pretendida. O lint continua como gate, enquanto o Fable 5 executa a transformação editorial.


<a id="src-s011"></a>

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


<a id="src-s012"></a>

## Implementação

- `forja_fable5.py`: autenticação, chamada sem ferramentas, parsing, retry e persistência.
- `forja_editorial_fidelity.py`: comparação e invariantes independentes.
- `forja_run.py`: validação de todos os bundles antes da promoção.
- `forja_package.py`: revalidação do bundle do entregável escolhido.
- `phase_contracts/F7.json`: artefatos e gates obrigatórios.
- `phase_contracts/F8.json`: consumo de `final_markdown` com trilha auditada.
- `FORJA_N3_CONFIG.json`: capacidade `fable5FinalWritingV1`.


<a id="src-s013"></a>

## Compatibilidade e implantação

Estados e pacotes históricos permanecem legíveis. A obrigação vale para tentativas F7 criadas sob o contrato atualizado. Não há migração automática de textos históricos e nenhum arquivo anterior é reescrito.

Rollback lógico: desabilitar a orquestração de novas chamadas e preservar todos os artefatos já produzidos. A retirada definitiva do contrato exige decisão explícita, pois F8 e o pacote novo passaram a depender de `final_markdown*`.


<a id="src-s014"></a>

## Evidência de aceite

- revisão arquitetural e pós-implementação pelo próprio Claude/Fable;
- correção dos achados materiais levantados na revisão;
- regressão integrada de 42/42 testes em 15/07/2026;
- execução viva sobre peça auditada de aproximadamente 36 KB;
- confirmação de OAuth Claude Max, modelo `claude-fable-5`, hash de origem e quatro gates;
- resultado aprovado na primeira tentativa do ensaio vivo.


<a id="src-s015"></a>

## Riscos residuais

- equivalência semântica perfeita não é decidível por checks lexicais;
- o gate atual não cobre toda mudança factual sem números, adição de conteúdo, aspas simples ou pedido sem heading reconhecido;
- mudanças futuras do envelope do Claude Code podem exigir adaptação;
- textos muito grandes podem atingir limite operacional ou timeout;
- a qualidade final ainda depende da qualidade jurídica da origem auditada;
- revisão humana continua obrigatória antes de protocolo ou entrega externa.


<a id="src-s016"></a>

## Consequências documentais

Toda mudança futura em modelo, autenticação, artefatos, invariantes, retry ou consumidor final deve atualizar, no mesmo ciclo:

- `PROTOCOLO_FABLE5_ESCRITA_FINAL.md`;
- `docs/ARCHITECTURE.md`, `docs/CONFIGURATION.md` e `docs/TESTING.md`;
- `DOCUMENTACAO_TECNICA.md` e `INDICE_FORJA.md`;
- `FORJA_SPEC_MANIFEST.json` e contratos;
- `RETROSPECTIVAS.md` quando houver aprendizado reutilizável.
