# Consulta IA — 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos

> Cópia de consulta derivada. O documento canônico permanece no caminho de origem indicado abaixo.

## Metadados e rastreabilidade

- **Documento de origem:** `ANEXO_B_INVARIANTES_E_TESTES_COCRIACAO.md`
- **Tipo:** Anexo
- **SHA-256 da origem:** `7a4c7a5e4e2049b24479dd812b9e95e1bbb97da256aaab0ae47fabda70f8fd9c`
- **Linhas da origem:** 336
- **Blocos integralmente indexados:** 25
- **Geração:** 2026-08-10T13:53:35-03:00
- **Cobertura:** 100% das linhas e do texto da origem, sem omissão.
- **Links relativos normalizados:** 0 destino(s), apenas para preservar a navegação na cópia.

## Roteiro de consulta para IA

**Síntese de localização:** Protocolo: FORJA-COCRIACAO-v1 Data: 25/07/2026. Estado: desenho técnico para revisão. Não autoriza implementação. Rege-se pelo PRD 33. Em conflito, prevalece o PRD. Ondas e portões estão no 35.

**Termos de recuperação:** não, json, status, enum, quando, string, exige, brief, novo, payload, extensão, aditiva.

Use o índice abaixo para localizar o bloco pertinente. Cada entrada informa as linhas exatas no documento de origem. Para afirmações materiais, leia o bloco integral e confira o arquivo canônico pelo SHA-256.

## Índice detalhado e cobertura integral

- [SRC-S001 · L1–L8 · 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos](#src-s001)
  - Assuntos: tdd, cocriação, mapa, destinatário, precedentes, estratégicos, prd, protocolo
  - Trecho-guia: Protocolo: FORJA-COCRIACAO-v1 Data: 25/07/2026. Estado: desenho técnico para revisão. Não autoriza implementação. Rege-se pelo PRD 33. Em conflito, prevalece o PRD. Ondas e portões estão no 35.
  - SHA-256 do bloco: `369e56fca1c66a1874a5491a9d77db0b7c1ca523d8cea82f366dc194fb743657`
  - [SRC-S002 · L9–L21 · 1. Princípio de encaixe](#src-s002)
    - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 1. Princípio de encaixe
    - Assuntos: nova, princípio, encaixe, nada, pacote, novo, cli, máquina
    - Trecho-guia: Nada de pacote novo, CLI nova, máquina de estados nova ou fase nova. Tudo entra como:
    - SHA-256 do bloco: `f9b0d407949507257ac882b19190641b2618d7985e6f85672b7901104a10d065`
  - [SRC-S003 · L22–L41 · 2. Inventário de mudanças](#src-s003)
    - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 2. Inventário de mudanças
    - Assuntos: json, extensão, aditiva, arquivo, inventário, mudanças, módulo, payload
    - Trecho-guia: Módulos novos: quatro arquivos. Não é pacote. Cada um com um validador público e testes próprios.
    - SHA-256 do bloco: `674be1551f982db43225108a182d0f16c9403da3edb9e59221823e7d0ba9c1c8`
  - [SRC-S004 · L42–L43 · 3. Payloads](#src-s004)
    - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 3. Payloads
    - Assuntos: payloads
    - Trecho-guia: Documento de consulta sobre 3. Payloads.
    - SHA-256 do bloco: `d8917aa698e22a6ccfc08046e92c598c68ff2616cc5161bad1d6eece45d64639`
    - [SRC-S005 · L44–L83 · 3.1 F4DECISIONFACTORMAP — o signature brief](#src-s005)
      - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 3. Payloads > 3.1 F4DECISIONFACTORMAP — o signature brief
      - Assuntos: string, não, status, ids, statement, supportids, enum, selected
      - Trecho-guia: Herda integralmente o envelope N4 já existente: schemaVersion, specVersion, caseId, artifactType, phase, applicability, status, sourceHashes, producerRunId, reviewerRunId, createdAt, updatedAt, contentHash, issues, justification. Não redefinir envelope.
      - SHA-256 do bloco: `50a1c95f6ae53da99cc67019134b0a23c06299a39506226d4f6924c2782cbf5b`
    - [SRC-S006 · L84–L98 · 3.2 F4COVERAGEMATRIX — cobertura de famílias](#src-s006)
      - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 3. Payloads > 3.2 F4COVERAGEMATRIX — cobertura de famílias
      - Assuntos: famílias, cobertura, enum, status, examinada_proposta, quando, f4coveragematrix, f4_coverage_matrix
      - Trecho-guia: Invariante: as nove famílias presentes, sem exceção. Proibido campo de contagem mínima de teses — RF-1.2.
      - SHA-256 do bloco: `47d29cf1e0dc757ca4e387144f095bfc74b80f9104ca944a8771a9750af959c7`
    - [SRC-S007 · L99–L131 · 3.3 F3DESTINATARIOMAP — tipo novo](#src-s007)
      - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 3. Payloads > 3.3 F3DESTINATARIOMAP — tipo novo
      - Assuntos: não, sourceref, rf-3, checkedat, status, precedentids, sourcekind, exige
      - Trecho-guia: Envelope N4 idêntico aos demais, para herdar validação e catálogo. Payload:
      - SHA-256 do bloco: `1009cdab1d797f6056b65b239c606a6034cb2e0fcd28b3ff0c99750fd52bd2d6`
    - [SRC-S008 · L132–L147 · 3.4 sourceledger v2 — trilha de busca](#src-s008)
      - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 3. Payloads > 3.4 sourceledger v2 — trilha de busca
      - Assuntos: busca, trilha, base, reason, negativeresult, sourceledger, source_ledger, acréscimo
      - Trecho-guia: negativeResult é obrigatório quando a busca visava órgão prevento ou turma competente e não retornou precedente favorável — RF-5.3.
      - SHA-256 do bloco: `e96efb58a199387a76402f51989f55e648a51d3057f7a78ff0a9ac98f7a856e7`
    - [SRC-S009 · L148–L177 · 3.5 verifiedsourceledger v2 — ficha das âncoras](#src-s009)
      - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 3. Payloads > 3.5 verifiedsourceledger v2 — ficha das âncoras
      - Assuntos: rf-5, operacao, ficha, âncoras, apenas, numero, integra, obtained
      - Trecho-guia: Aplicada apenas aos anchorIds declarados no brief. Acréscimo:
      - SHA-256 do bloco: `24808b282489101fcd80e610fc971f746236ae43f7eb536978a91ef12665ce3c`
    - [SRC-S010 · L178–L200 · 3.6 F2QUESTIONTREE v2 — seleção e silêncio](#src-s010)
      - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 3. Payloads > 3.6 F2QUESTIONTREE v2 — seleção e silêncio
      - Assuntos: seleção, silêncio, int, true, acervoprobe, matched, rf-2, silenceclass
      - Trecho-guia: Invariante crítica, derivada de RF-2.4: silenceClass em fatomaterial ou autorizacao proíbe silenceEffect = defaultallowed. A violação é P0 de contrato, provada por teste negativo.
      - SHA-256 do bloco: `8dd47fb083f5880e357ccf66354d6d64d1a1b8c36a9e9580a98cb9d3df3e7d60`
    - [SRC-S011 · L201–L206 · 3.7 Recibo gostoJuridico v2](#src-s011)
      - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 3. Payloads > 3.7 Recibo gostoJuridico v2
      - Assuntos: recibo, gostojuridico, dois, campos, signaturebriefsha256, selectedrouteid, recomposição, migra
      - Trecho-guia: Dois campos: signatureBriefSha256 e selectedRouteId. A recomposição migra de forjafable5.py para forjaeditorialfidelity.validateeditorialbundle(), corrigindo o achado 5 da revisão adversarial de 24/07 — hoje o recibo é validado dentro do executor, fora da recomputação final.
      - SHA-256 do bloco: `72bb662dd9c1a12f63429d1067368e881a9d0c3c959d9681e2ba5999fe95de2b`
  - [SRC-S012 · L207–L222 · 4. Alterações nos contratos de fase](#src-s012)
    - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 4. Alterações nos contratos de fase
    - Assuntos: json, gates, required, sob, flag, alterações, contratos, fase
    - Trecho-guia: Todas aditivas. Nenhum output existente sai.
    - SHA-256 do bloco: `56844ac75c6de6fca4e654259a795702955de8dec1a9cfc04b348516ca67043c`
  - [SRC-S013 · L223–L233 · 5. Migração e compatibilidade](#src-s013)
    - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 5. Migração e compatibilidade
    - Assuntos: migração, compatibilidade, artefato, não, json, recebe, replay, versionamento
    - Trecho-guia: 1. Versionamento. sourceledger, verifiedsourceledger e F2QUESTIONTREE vão a schemaVersion: 2. Leitores aceitam 1 e 2; escritores emitem 2. 2. Defaults legados. A ausência de searchTrail, anchorProfile ou consultaSelection em artefato v1 é válida e não gera issue. 3. Catálogo. ART
    - SHA-256 do bloco: `1ae007b9f66a02cdbb2e851b7894c5fc1a16b07b23e40400ea2f0bef102f3343`
  - [SRC-S014 · L234–L247 · 6. Configuração e flags](#src-s014)
    - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 6. Configuração e flags
    - Assuntos: configuração, flags, pela, off, shadow, pilot, caso, pilotcases
    - Trecho-guia: Flag única cocriacaoV1, com os estados já usados pela FORJA: off | shadow | pilot. Reaproveita forjan4validate.FLAGFILES e effectivemode(), que já rebaixa caso fora de pilotCases para sombra — padrão identificado na revisão adversarial e que não deve ser reinventado.
    - SHA-256 do bloco: `42b3784bde40002906b77a7c8cc5107c23ab56f967172f95fb26a72a4837e3ff`
  - [SRC-S015 · L248–L249 · 7. Matriz de testes](#src-s015)
    - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 7. Matriz de testes
    - Assuntos: matriz, testes
    - Trecho-guia: Documento de consulta sobre 7. Matriz de testes.
    - SHA-256 do bloco: `021c8b2e27ce4de8f6e9698eb001d9ff2c53f606bd54d90b8e100ac42e81aabf`
    - [SRC-S016 · L250–L256 · 7.1 Unidade](#src-s016)
      - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 7. Matriz de testes > 7.1 Unidade
      - Assuntos: invariantes, unidade, validadores, casos, mínimos, válidos, inválidos, brief
      - Trecho-guia: validadores de A1, A2 e A3, com casos mínimos válidos e inválidos; invariantes 1 a 7 do brief, uma por teste; invariantes 1 a 5 do mapa; invariantes 1 a 5 da ficha de âncora; rebaixamento automático de composicaoAtual vencida para stale.
      - SHA-256 do bloco: `190ccd64a4e56066a78183ebf7fef2cd3d1a1c9f49c66bd6c670a6e5f16e5c96`
    - [SRC-S017 · L257–L261 · 7.2 Contrato](#src-s017)
      - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 7. Matriz de testes > 7.2 Contrato
      - Assuntos: contrato, presença, condicional, flag, off, não, exige, shadow
      - Trecho-guia: presença condicional por flag: off não exige; shadow e pilot exigem; leitura de artefato v1 por consumidor v2, para os sete consumidores do §5.6; F3DESTINATARIOMAP registrado no catálogo e resolvido pelo validador de fase.
      - SHA-256 do bloco: `4e5a6952fba8240557ec5fd805fa004d88a1835c9a54838d754d252a87496d7b`
    - [SRC-S018 · L262–L279 · 7.3 Negativos obrigatórios — cada um prova uma proibição do PRD](#src-s018)
      - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 7. Matriz de testes > 7.3 Negativos obrigatórios — cada um prova uma proibição do PRD
      - Assuntos: rf-5, prova, rf-2, negativos, obrigatórios, cada, proibição, prd
      - Trecho-guia: Documento de consulta sobre 7.3 Negativos obrigatórios — cada um prova uma proibição do PRD.
      - SHA-256 do bloco: `e033257442ca60962537605bf68314fe66873340084792d59c57262582bd9209`
    - [SRC-S019 · L280–L284 · 7.4 Metamórficos](#src-s019)
      - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 7. Matriz de testes > 7.4 Metamórficos
      - Assuntos: não, metamórficos, altera, remover, âncora, decisiva, invalida, reordenar
      - Trecho-guia: reordenar rotas não altera o contentHash da decisão nem o resultado; renomear routeId preservando vínculos não altera a validação; remover âncora não decisiva não invalida a rota; remover âncora decisiva invalida e reabre F4.
      - SHA-256 do bloco: `91255fa0cfb6fe718d31488dd4c18e7cd065f1e99c40aa8cb5df6ccceb25d7c5`
    - [SRC-S020 · L285–L291 · 7.5 Adversariais](#src-s020)
      - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 7. Matriz de testes > 7.5 Adversariais
      - Assuntos: adversariais, brief, declara, âncora, inexistente, source_ledger, consulta, reintroduz
      - Trecho-guia: brief que declara âncora inexistente no sourceledger; consulta que reintroduz marcador [FONTE: arquivo] — RF-2.8; mapa com composicaoAtual copiada de espelho antigo; ficha com trechoLiteral que não existe na íntegra do hash declarado; rota escolhida que depende de pergunta com si
      - SHA-256 do bloco: `44fcdea55ebc518d616f4dc5bbe6bcb1ff653f0e8bd5cd19bff019df534ad62b`
    - [SRC-S021 · L292–L294 · 7.6 Regressão real](#src-s021)
      - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 7. Matriz de testes > 7.6 Regressão real
      - Assuntos: regressão, real, test_licao41, test_real_telemetria_licao41, test_forja_citacoes, test_forja_verificador, test_forja_fable5, test_forja_estilo_humano
      - Trecho-guia: testlicao41.py, testrealtelemetrialicao41.py, testforjacitacoes.py, testforjaverificador.py, testforjafable5.py, testforjaestilohumano.py, testforjaexploracao100.py e testforjaautoresearch.py — todos verdes antes e depois de cada onda.
      - SHA-256 do bloco: `b76497409aa70aac1de07ad4e06f966c1c5b86f12ff0d05fbbc286cd6a192bd0`
    - [SRC-S022 · L295–L299 · 7.7 Canários](#src-s022)
      - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 7. Matriz de testes > 7.7 Canários
      - Assuntos: canários, acrescentar, dois, falha, única, forja_ar_canarios, âncora, trecho
      - Trecho-guia: Acrescentar dois canários de falha única a forjaarcanarios.py: âncora com trecho literal alterado em um caractere; mapa com checkedAt retroagido além do maxAgeDays. Ambos precisam matar por sensor específico, sem derrubar os controles benignos.
      - SHA-256 do bloco: `135268d53a361840ed577b8afcafca06c780a88f8b897e0a70669cbe082a2906`
  - [SRC-S023 · L300–L312 · 8. Telemetria](#src-s023)
    - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 8. Telemetria
    - Assuntos: telemetria, caso, perguntas, âncoras, reutilizar, legal_search, reports, metricas_gates
    - Trecho-guia: Reutilizar telemetria/legalsearch/ e reports/METRICASGATES.json. Métricas novas, todas derivadas de artefato e não de estimativa:
    - SHA-256 do bloco: `38f21548a8872c9225d5e4acd1852368324adae8d9dc39382cdfb15f2a02cb22`
  - [SRC-S024 · L313–L327 · 9. Falha e resgate](#src-s024)
    - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 9. Falha e resgate
    - Assuntos: falha, resgate, resposta, composição, motivo, bloqueia, caso, desligar
    - Trecho-guia: O rollback é sempre desligar cocriacaoV1. Nenhum artefato novo é insumo obrigatório de F8, F9 ou F10.
    - SHA-256 do bloco: `325f9cb295cabcd7baec9a6fd38bab49fb0d3a232122595cfd6fffd9f17816da`
  - [SRC-S025 · L328–L336 · 10. Fronteiras que este desenho não pode cruzar](#src-s025)
    - Caminho: 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos > 10. Fronteiras que este desenho não pode cruzar
    - Assuntos: nenhum, fronteiras, este, desenho, não, pode, cruzar, nenhuma
    - Trecho-guia: 1. Nenhum gate jurídico ou factual existente é enfraquecido. AH-01 a AH-08 permanecem fail-closed em strictprotocol. 2. Nenhum envio externo automatizado. 3. Nenhuma leitura de memória decisória em produção. 4. Nenhum escore numérico de aderência ou de regime. 5. Nenhuma alegação
    - SHA-256 do bloco: `7f8c1a7bb0d475fa028756b259d4a1ace4129acf7a943d197ea37c3d9a6c9095`

## Conteúdo integral indexado

Os marcadores HTML abaixo são apenas âncoras de navegação. O texto reproduz integralmente a origem normalizada em UTF-8; somente destinos de links relativos podem ter sido recalculados para apontar ao mesmo arquivo a partir desta pasta.

<a id="src-s001"></a>

# 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos

**Protocolo:** `FORJA-COCRIACAO-v1`
**Data:** 25/07/2026. **Estado:** desenho técnico para revisão. **Não autoriza implementação.**
**Rege-se pelo PRD `33`.** Em conflito, prevalece o PRD. Ondas e portões estão no `35`.

---


<a id="src-s002"></a>

## 1. Princípio de encaixe

Nada de pacote novo, CLI nova, máquina de estados nova ou fase nova. Tudo entra como:

- **payload** em shell já declarado no catálogo N4;
- **extensão aditiva versionada** de artefato N2/N3 já produzido em casos reais;
- **subfase** no padrão já exercido duas vezes: F2-A da exploração e F7-B do Fable 5;
- **bloco de prompt** nas fases existentes.

`final_markdown` continua sendo o cânone consumido por F8. A tupla F0–F10 não muda.

---


<a id="src-s003"></a>

## 2. Inventário de mudanças

| # | Objeto | Natureza | Fase | Módulo dono proposto |
|---|---|---|---|---|
| A1 | `F4_DECISION_FACTOR_MAP.json` | **payload em shell existente** — é o signature brief | F4 | `forja_signature_brief.py` (um arquivo) |
| A2 | `F4_COVERAGE_MATRIX.json` | **payload em shell existente** — cobertura de famílias de tese | F4 | mesmo módulo de A1 |
| A3 | `F3_DESTINATARIO_MAP.json` | **tipo novo**, o único do plano | F3 | `forja_destinatario.py` (um arquivo) |
| B1 | `source_ledger` | extensão aditiva v2 — trilha de busca e resultado negativo | F5 | `forja_sources.py` |
| B2 | `verified_source_ledger` | extensão aditiva v2 — ficha profunda das âncoras | F7 | `forja_citations.py` |
| B3 | recibo `gostoJuridico` | extensão aditiva — `signatureBriefSha256`, `selectedRouteId` | F7-B | `forja_fable5.py` + `forja_editorial_fidelity.py` |
| C1 | `F2_QUESTION_TREE.json` | extensão aditiva v2 — seleção, classe de silêncio, decisão, rodada | F2 | `forja_exploracao_100.py` |
| C2 | Consulta ao advogado | **renderizador e ledger**, sem tipo novo | F2-B | `forja_consulta.py` (um arquivo) |
| D1 | `IDENTITY_CORPUS_MANIFEST.jsonl` | ativo curatorial, fora do caminho crítico | — | `forja_identity_corpus.py` |
| E1 | Blocos de prompt F3-B, F4, F6 | texto | F3, F4, F6 | prompts existentes |
| E2 | Flag `cocriacaoV1` | configuração | — | `FORJA_N3_CONFIG.json` + `forja_n4_validate` |

**Módulos novos: quatro arquivos.** Não é pacote. Cada um com um validador público e testes próprios.

---


<a id="src-s004"></a>

## 3. Payloads


<a id="src-s005"></a>

### 3.1 `F4_DECISION_FACTOR_MAP` — o signature brief

Herda integralmente o envelope N4 já existente: `schemaVersion`, `specVersion`, `caseId`, `artifactType`, `phase`, `applicability`, `status`, `sourceHashes`, `producerRunId`, `reviewerRunId`, `createdAt`, `updatedAt`, `contentHash`, `issues`, `justification`. **Não redefinir envelope.**

Payload proposto:

```
decisiveQuestion            string, 1 frase
consequenceDemonstrated     { statement, supportIds[], epistemicStatus }
routes[]                    2 a 4 em regra; 1 exige singleRouteJustification
  routeId                   string
  statement                 string
  natureza                  enum: processual | prejudicial | merito |
                            subsidiaria | constitucional_prequestionamento
  origem                    enum: sistema | interlocutor | acervo_escritorio
  dependsOnFactIds[]        IDs do fact_ledger
  dependsOnAnchorIds[]      IDs candidatos de precedente
  riscoEstrategico          string
  status                    enum: selected | rejected | reserved
  rejectionReason           obrigatório quando status = rejected
selectedRouteId             string; null enquanto houver pendência bloqueante
selectionDecidedBy          { actor, role, decidedAt } — humano quando risco material
singleRouteJustification    string | null
motherSentence              string, provisória
decisiveFactIds[]           IDs
anchorCandidateIds[]        IDs
bestCounterArgument         { statement, response, supportIds[] }
mandatoryContent[]          o que a redação não pode sacrificar
blockingPendencies[]        { questionId, classe, efeito }
```

**Invariantes verificáveis**
1. Toda rota `rejected` tem `rejectionReason` não vazio.
2. `selectedRouteId` aponta para rota existente com `status = selected`, e há exatamente uma.
3. `selectedRouteId` é `null` se houver `blockingPendencies` de classe material — RF-4.6.
4. Todo `dependsOnFactIds` existe no `fact_ledger` do mesmo `attempt`.
5. Todo `anchorCandidateIds` existe no `source_ledger` **ou** está marcado como não verificado, e nesse caso a rota não pode ser `selected`.
6. `routes` entre 1 e 6; fora da faixa de 2 a 4 exige justificativa registrada.
7. `consequenceDemonstrated.supportIds` não vazio quando `epistemicStatus = record_evidence`.


<a id="src-s006"></a>

### 3.2 `F4_COVERAGE_MATRIX` — cobertura de famílias

```
families[]
  family      enum: competencia | admissibilidade | prejudiciais |
              prescricao_decadencia | nulidades | merito_principal |
              merito_subsidiario | constitucional_prequestionamento |
              consequencia_institucional
  status      enum: examinada_proposta | examinada_descartada | nao_aplicavel
  reason      obrigatório quando status != examinada_proposta
  routeIds[]  vínculo com o brief quando proposta
```

**Invariante:** as nove famílias presentes, sem exceção. Proibido campo de contagem mínima de teses — RF-1.2.


<a id="src-s007"></a>

### 3.3 `F3_DESTINATARIO_MAP` — tipo novo

Envelope N4 idêntico aos demais, para herdar validação e catálogo. Payload:

```
competencia        { orgao, fundamento, sourceRef }
prevencao          { existe: true|false|nao_apurado, relator, origem,
                     processoRelacionado, fundamentoRegimental, sourceRef }
composicaoAtual    { membros[], checkedAt, sourceUrl, status }
posicaoRelator     [ { questao, entendimento, precedentIds[], sourceKind } ]
posicaoColegiada   [ { orgao, entendimento, precedentIds[], sourceKind } ]
divergencia        [ { orgaos[], descricao, precedentIds[], aproveitamento } ]
rotaRecursal       { viaProjetada, pressupostos[], sourceRef }
prequestionamento  ledger paralelo:
                   [ { materia, dispositivo, origemNaDecisaoRecorrida } ]
```

**Campo de frescor obrigatório em todo dado mutável**, conforme RF-3.4:

```
checkedAt        ISO-8601
sourceId | url   fonte oficial
freshnessPolicy  { maxAgeDays, revalidateOn }
status           enum: confirmed | stale | unknown | not_applicable
```

**Invariantes**
1. `composicaoAtual.status = confirmed` exige `checkedAt` dentro de `maxAgeDays` e `sourceUrl` oficial. Fora disso, rebaixa para `stale` automaticamente na leitura.
2. `prevencao.existe = true` exige `fundamentoRegimental` e `sourceRef` nos autos ou na distribuição. **Metadado de DataJud não satisfaz** — RF-3.2.
3. `posicaoRelator[].sourceKind` em `integra_hash`, `reproducao_oficial` ou `espelho_descoberta`; se for `espelho_descoberta`, o item **não pode** virar âncora.
4. Blocos não aplicáveis ao tribunal — seção e Corte Especial em tribunal sem essa estrutura — recebem `not_applicable` com motivo, e não ficam vazios (RF-3.3).
5. Campo não apurado exige motivo (RF-3.5).


<a id="src-s008"></a>

### 3.4 `source_ledger` v2 — trilha de busca

Acréscimo aditivo:

```
searchTrail[]
  queryId, base, endpoint, executedAt, terms, filters,
  orgaos[], recorteTemporal, returnedIds[],
  discardedIds[] { id, reason },
  basesNaoConsultadas[] { base, reason },
  negativeResult { searched, found: false, scope, consequence },
  replayRef, knownLimitations[]
```

`negativeResult` é obrigatório quando a busca visava órgão prevento ou turma competente e não retornou precedente favorável — RF-5.3.


<a id="src-s009"></a>

### 3.5 `verified_source_ledger` v2 — ficha das âncoras

Aplicada **apenas** aos `anchorIds` declarados no brief. Acréscimo:

```
anchorProfile
  identity { classe, numero, orgao, relator, julgadoEm, publicadoEm, colegiado }
  integra { obtained: bool, sha256, localizacao, fonte }
  questaoDecidida
  fundamentosDeterminantes[] { texto, trechoLiteral, localizacao }
  obiterConfundivel[]
  molduraFaticaDeterminante[]
  confronto[] { elemento, paradigma, nossoCaso, ancoraNossa,
                relacao: coincide|difere|nao_apurado }
  operacao  enum: aplicar | distinguir | delimitar_alcance | sustentar_superacao
  operacaoFundamentacao
  regime { baseNormativa, tipoAutoridade, deverOuEfeito, orgaoCompetente,
           caminhoDistincaoOuSuperacao, vigencia }
  vigenciaConferidaEm
  distinguishingAdversario { hipotese, respostaAntecipada }
  revisorHumano { actor, decidedAt } | null
```

**Invariantes**
1. `operacao` obrigatória; a ausência impede a citação — RF-5.5.
2. `fundamentosDeterminantes[].trechoLiteral` exige `integra.obtained = true` **quando a proposição sustentada depender do fundamento** — RF-5.8. Ementa isolada admite apenas descrição limitada, marcada como tal.
3. `regime` é objeto, nunca número — RF-5.7.
4. Precedente vinculante com `confronto` divergente **não** recebe rebaixamento de força; recebe `operacao` em `delimitar_alcance` ou `sustentar_superacao` — RF-5.6.
5. `revisorHumano` obrigatório quando a âncora sustenta a rota selecionada.


<a id="src-s010"></a>

### 3.6 `F2_QUESTION_TREE` v2 — seleção e silêncio

```
consultaSelection
  selected: bool
  rank: int                      ordem por impacto
  admissionFilters { notAnswered, canChangeDecision,
                     addressedToDecider, declaresSilenceEffect }  todos true
  acervoProbe { probedAt, indexRef, matched: false }   RF-2.3
silenceClass  enum: fato_material | autorizacao | estrategica_decisiva |
                    preferencia_nao_material | estrategica_nao_material
silenceEffect enum: blocks_claim | blocks_action | keeps_routes_open |
                    default_allowed
decisionRecord
  answerText | answerSummary, author, channel, epistemicStatus,
  decisionProduced, affectedArtifacts[], remainingPendency, decidedAt, version
roundIndex int
```

**Invariante crítica, derivada de RF-2.4:** `silenceClass` em `fato_material` ou `autorizacao` **proíbe** `silenceEffect = default_allowed`. A violação é P0 de contrato, provada por teste negativo.

**Invariante de confiança:** `acervoProbe.matched = true` impede a seleção. Pergunta respondível pelo acervo não é emitida.


<a id="src-s011"></a>

### 3.7 Recibo `gostoJuridico` v2

Dois campos: `signatureBriefSha256` e `selectedRouteId`. **A recomposição migra** de `forja_fable5.py` para `forja_editorial_fidelity.validate_editorial_bundle()`, corrigindo o achado 5 da revisão adversarial de 24/07 — hoje o recibo é validado dentro do executor, fora da recomputação final.

---


<a id="src-s012"></a>

## 4. Alterações nos contratos de fase

Todas aditivas. Nenhum output existente sai.

| Contrato | Acréscimo | Condicionalidade |
|---|---|---|
| `F2.json` | outputs `consulta_advogado`, `consulta_ledger`; gate `consulta_admission_filters_passed` | `conditional`: exigido quando houver pergunta material bloqueada |
| `F3.json` | output `destinatario_map`; gates `destinatario_sources_declared`, `destinatario_freshness_valid` | `conditional` por classe de caso |
| `F4.json` | outputs `signature_brief`, `coverage_matrix`; gates `route_selected_or_blocked`, `coverage_families_complete` | `required` sob a flag |
| `F5.json` | gate `search_trail_recorded` | `required` sob a flag |
| `F7.json` | gates `anchor_profiles_complete`, `anchor_operation_declared`, `editorial_brief_hash_match` | `required` sob a flag |

`phase_contracts_n4/` recebe as extensões correspondentes. `forja_phase_contracts.py` valida presença **condicional**, e não incondicional, para não quebrar os 49 casos existentes.

---


<a id="src-s013"></a>

## 5. Migração e compatibilidade

1. **Versionamento.** `source_ledger`, `verified_source_ledger` e `F2_QUESTION_TREE` vão a `schemaVersion: 2`. Leitores aceitam 1 e 2; escritores emitem 2.
2. **Defaults legados.** A ausência de `searchTrail`, `anchorProfile` ou `consultaSelection` em artefato v1 é válida e não gera `issue`.
3. **Catálogo.** `ARTIFACT_CATALOG.json` recebe `F3_DESTINATARIO_MAP.json` e passa a declarar `applicability` explícita para os três artefatos em uso. **Os outros 22 shells permanecem intocados** — não ativar shell sem consumidor, RF-6.3.
4. **Replay de fixtures.** `n4_fixtures/` ganha um caso v1 puro e um v2 completo; o replay precisa passar nos dois.
5. **Proibição.** Rebaseline automático da Régua continua proibido. Divergência de baseline é classificada e aceita explicitamente, ou barra a onda.
6. **Consumidores a revalidar:** `forja_run.py`, `forja_package.py`, `forja_delivery.py`, `forja_reconcile.py`, `forja_metricas_f7.py`, `forja_n4_validate.py` e `forja_regua.py`. Cada um recebe teste de leitura de artefato v1 e v2.

---


<a id="src-s014"></a>

## 6. Configuração e flags

Flag única `cocriacaoV1`, com os estados já usados pela FORJA: `off | shadow | pilot`. Reaproveita `forja_n4_validate.FLAG_FILES` e `_effective_mode()`, que já rebaixa caso fora de `pilotCases` para sombra — padrão identificado na revisão adversarial e que não deve ser reinventado.

| Estado | Comportamento |
|---|---|
| `off` | nada é produzido; contratos condicionais inativos |
| `shadow` | mapa, brief e cobertura são produzidos e validados; **nenhum output de F6 muda**; consulta gerada como minuta interna, sem envio |
| `pilot` | ativo apenas em `pilotCases`; F6 consome o brief; F7 e F7-B recompõem; consulta enviada por pessoa autorizada |

Teto de custo por caso pela telemetria existente, sem perfil por estágio.

---


<a id="src-s015"></a>

## 7. Matriz de testes


<a id="src-s016"></a>

### 7.1 Unidade
- validadores de A1, A2 e A3, com casos mínimos válidos e inválidos;
- invariantes 1 a 7 do brief, uma por teste;
- invariantes 1 a 5 do mapa;
- invariantes 1 a 5 da ficha de âncora;
- rebaixamento automático de `composicaoAtual` vencida para `stale`.


<a id="src-s017"></a>

### 7.2 Contrato
- presença condicional por flag: `off` não exige; `shadow` e `pilot` exigem;
- leitura de artefato v1 por consumidor v2, para os sete consumidores do §5.6;
- `F3_DESTINATARIO_MAP` registrado no catálogo e resolvido pelo validador de fase.


<a id="src-s018"></a>

### 7.3 Negativos obrigatórios — cada um prova uma proibição do PRD

| Teste | Prova |
|---|---|
| `test_silencio_fato_material_nao_vira_default` | RF-2.4: `silenceClass = fato_material` com `default_allowed` reprova |
| `test_pergunta_respondivel_pelo_acervo_nao_emite` | RF-2.3: `acervoProbe.matched = true` bloqueia a seleção |
| `test_prevencao_por_datajud_nao_confirma` | RF-3.2: `prevencao.existe = true` só com fundamento e fonte nos autos |
| `test_composicao_vencida_nao_e_confirmed` | RF-3.4 |
| `test_ratio_de_ementa_sem_integra_reprova` | RF-5.8 |
| `test_precedente_sem_operacao_nao_e_citavel` | RF-5.5 |
| `test_vinculante_com_moldura_diversa_nao_rebaixa` | RF-5.6: exige `delimitar_alcance` ou `sustentar_superacao` |
| `test_regime_nao_aceita_numero` | RF-5.7 |
| `test_rota_selecionada_com_pendencia_material_reprova` | RF-4.6 |
| `test_ausencia_de_familia_na_cobertura_reprova` | RF-1.3 |
| `test_envio_externo_autonomo_bloqueado` | RF-2.7 |
| `test_shell_ativado_sem_consumidor_reprova` | RF-6.3 |
| `test_campo_do_brief_virou_subtitulo_reprova` | RF-4.5, heurística no gate de estilo |


<a id="src-s019"></a>

### 7.4 Metamórficos
- reordenar rotas não altera o `contentHash` da decisão nem o resultado;
- renomear `routeId` preservando vínculos não altera a validação;
- remover âncora não decisiva não invalida a rota; remover âncora decisiva invalida e reabre F4.


<a id="src-s020"></a>

### 7.5 Adversariais
- brief que declara âncora inexistente no `source_ledger`;
- consulta que reintroduz marcador `[FONTE: arquivo]` — RF-2.8;
- mapa com `composicaoAtual` copiada de espelho antigo;
- ficha com `trechoLiteral` que não existe na íntegra do hash declarado;
- rota escolhida que depende de pergunta com `silenceEffect = blocks_claim`.


<a id="src-s021"></a>

### 7.6 Regressão real
`test_licao41.py`, `test_real_telemetria_licao41.py`, `test_forja_citacoes.py`, `test_forja_verificador.py`, `test_forja_fable5.py`, `test_forja_estilo_humano.py`, `test_forja_exploracao_100.py` e `test_forja_autoresearch.py` — todos verdes antes e depois de cada onda.


<a id="src-s022"></a>

### 7.7 Canários
Acrescentar dois canários de falha única a `forja_ar_canarios.py`: âncora com trecho literal alterado em um caractere; mapa com `checkedAt` retroagido além do `maxAgeDays`. Ambos precisam matar por sensor específico, sem derrubar os controles benignos.

---


<a id="src-s023"></a>

## 8. Telemetria

Reutilizar `telemetria/legal_search/` e `reports/METRICAS_GATES.json`. Métricas novas, todas derivadas de artefato e não de estimativa:

- perguntas emitidas por caso; rodadas; taxa de resposta; **perguntas com `acervoProbe.matched = true` que chegaram à emissão** — precisa ser zero;
- rotas por caso; rota única com justificativa; pendências bloqueantes na seleção;
- campos do mapa em `confirmed`, `stale`, `unknown` e `not_applicable`, por bloco;
- âncoras por peça; âncoras com íntegra; operações por tipo;
- resultados negativos registrados;
- custo e latência por caso sob a flag.

---


<a id="src-s024"></a>

## 9. Falha e resgate

| Falha | Resposta |
|---|---|
| Âncora cai na verificação de F5 | invalida a rota, reabre F4, preserva o resto do brief |
| Fonte oficial indisponível para composição | `status = unknown` com motivo; **não** bloqueia o caso; bloqueia a afirmação sobre composição |
| TeiaJus degradado | a trilha registra `basesNaoConsultadas` com motivo; o caso segue com cobertura declarada menor |
| Consulta sem resposta | efeito por classe, RF-2.4; nunca paralisa a cognição |
| Regressão detectada em piloto | desligar a flag; os artefatos permanecem para diagnóstico |
| Divergência de baseline da Régua | barra a onda até classificação explícita |

O rollback é sempre desligar `cocriacaoV1`. Nenhum artefato novo é insumo obrigatório de F8, F9 ou F10.

---


<a id="src-s025"></a>

## 10. Fronteiras que este desenho não pode cruzar

1. Nenhum gate jurídico ou factual existente é enfraquecido. AH-01 a AH-08 permanecem fail-closed em `strict_protocol`.
2. Nenhum envio externo automatizado.
3. Nenhuma leitura de memória decisória em produção.
4. Nenhum escore numérico de aderência ou de regime.
5. Nenhuma alegação de autoria humana sobre texto gerado.
6. Nenhum shell do catálogo ativado sem payload, consumidor, invalidador e teste.
7. `final_markdown` permanece o cânone de F8.
