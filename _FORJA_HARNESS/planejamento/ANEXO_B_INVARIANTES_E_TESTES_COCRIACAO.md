# 34 — TDD: cocriação, mapa do destinatário e precedentes estratégicos

**Protocolo:** `FORJA-COCRIACAO-v1`
**Data:** 25/07/2026. **Estado:** desenho técnico para revisão. **Não autoriza implementação.**
**Rege-se pelo PRD `33`.** Em conflito, prevalece o PRD. Ondas e portões estão no `35`.

---

## 1. Princípio de encaixe

Nada de pacote novo, CLI nova, máquina de estados nova ou fase nova. Tudo entra como:

- **payload** em shell já declarado no catálogo N4;
- **extensão aditiva versionada** de artefato N2/N3 já produzido em casos reais;
- **subfase** no padrão já exercido duas vezes: F2-A da exploração e F7-B do Fable 5;
- **bloco de prompt** nas fases existentes.

`final_markdown` continua sendo o cânone consumido por F8. A tupla F0–F10 não muda.

---

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

## 3. Payloads

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

### 3.7 Recibo `gostoJuridico` v2

Dois campos: `signatureBriefSha256` e `selectedRouteId`. **A recomposição migra** de `forja_fable5.py` para `forja_editorial_fidelity.validate_editorial_bundle()`, corrigindo o achado 5 da revisão adversarial de 24/07 — hoje o recibo é validado dentro do executor, fora da recomputação final.

---

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

## 5. Migração e compatibilidade

1. **Versionamento.** `source_ledger`, `verified_source_ledger` e `F2_QUESTION_TREE` vão a `schemaVersion: 2`. Leitores aceitam 1 e 2; escritores emitem 2.
2. **Defaults legados.** A ausência de `searchTrail`, `anchorProfile` ou `consultaSelection` em artefato v1 é válida e não gera `issue`.
3. **Catálogo.** `ARTIFACT_CATALOG.json` recebe `F3_DESTINATARIO_MAP.json` e passa a declarar `applicability` explícita para os três artefatos em uso. **Os outros 22 shells permanecem intocados** — não ativar shell sem consumidor, RF-6.3.
4. **Replay de fixtures.** `n4_fixtures/` ganha um caso v1 puro e um v2 completo; o replay precisa passar nos dois.
5. **Proibição.** Rebaseline automático da Régua continua proibido. Divergência de baseline é classificada e aceita explicitamente, ou barra a onda.
6. **Consumidores a revalidar:** `forja_run.py`, `forja_package.py`, `forja_delivery.py`, `forja_reconcile.py`, `forja_metricas_f7.py`, `forja_n4_validate.py` e `forja_regua.py`. Cada um recebe teste de leitura de artefato v1 e v2.

---

## 6. Configuração e flags

Flag única `cocriacaoV1`, com os estados já usados pela FORJA: `off | shadow | pilot`. Reaproveita `forja_n4_validate.FLAG_FILES` e `_effective_mode()`, que já rebaixa caso fora de `pilotCases` para sombra — padrão identificado na revisão adversarial e que não deve ser reinventado.

| Estado | Comportamento |
|---|---|
| `off` | nada é produzido; contratos condicionais inativos |
| `shadow` | mapa, brief e cobertura são produzidos e validados; **nenhum output de F6 muda**; consulta gerada como minuta interna, sem envio |
| `pilot` | ativo apenas em `pilotCases`; F6 consome o brief; F7 e F7-B recompõem; consulta enviada por pessoa autorizada |

Teto de custo por caso pela telemetria existente, sem perfil por estágio.

---

## 7. Matriz de testes

### 7.1 Unidade
- validadores de A1, A2 e A3, com casos mínimos válidos e inválidos;
- invariantes 1 a 7 do brief, uma por teste;
- invariantes 1 a 5 do mapa;
- invariantes 1 a 5 da ficha de âncora;
- rebaixamento automático de `composicaoAtual` vencida para `stale`.

### 7.2 Contrato
- presença condicional por flag: `off` não exige; `shadow` e `pilot` exigem;
- leitura de artefato v1 por consumidor v2, para os sete consumidores do §5.6;
- `F3_DESTINATARIO_MAP` registrado no catálogo e resolvido pelo validador de fase.

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

### 7.4 Metamórficos
- reordenar rotas não altera o `contentHash` da decisão nem o resultado;
- renomear `routeId` preservando vínculos não altera a validação;
- remover âncora não decisiva não invalida a rota; remover âncora decisiva invalida e reabre F4.

### 7.5 Adversariais
- brief que declara âncora inexistente no `source_ledger`;
- consulta que reintroduz marcador `[FONTE: arquivo]` — RF-2.8;
- mapa com `composicaoAtual` copiada de espelho antigo;
- ficha com `trechoLiteral` que não existe na íntegra do hash declarado;
- rota escolhida que depende de pergunta com `silenceEffect = blocks_claim`.

### 7.6 Regressão real
`test_licao41.py`, `test_real_telemetria_licao41.py`, `test_forja_citacoes.py`, `test_forja_verificador.py`, `test_forja_fable5.py`, `test_forja_estilo_humano.py`, `test_forja_exploracao_100.py` e `test_forja_autoresearch.py` — todos verdes antes e depois de cada onda.

### 7.7 Canários
Acrescentar dois canários de falha única a `forja_ar_canarios.py`: âncora com trecho literal alterado em um caractere; mapa com `checkedAt` retroagido além do `maxAgeDays`. Ambos precisam matar por sensor específico, sem derrubar os controles benignos.

---

## 8. Telemetria

Reutilizar `telemetria/legal_search/` e `reports/METRICAS_GATES.json`. Métricas novas, todas derivadas de artefato e não de estimativa:

- perguntas emitidas por caso; rodadas; taxa de resposta; **perguntas com `acervoProbe.matched = true` que chegaram à emissão** — precisa ser zero;
- rotas por caso; rota única com justificativa; pendências bloqueantes na seleção;
- campos do mapa em `confirmed`, `stale`, `unknown` e `not_applicable`, por bloco;
- âncoras por peça; âncoras com íntegra; operações por tipo;
- resultados negativos registrados;
- custo e latência por caso sob a flag.

---

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

## 10. Fronteiras que este desenho não pode cruzar

1. Nenhum gate jurídico ou factual existente é enfraquecido. AH-01 a AH-08 permanecem fail-closed em `strict_protocol`.
2. Nenhum envio externo automatizado.
3. Nenhuma leitura de memória decisória em produção.
4. Nenhum escore numérico de aderência ou de regime.
5. Nenhuma alegação de autoria humana sobre texto gerado.
6. Nenhum shell do catálogo ativado sem payload, consumidor, invalidador e teste.
7. `final_markdown` permanece o cânone de F8.
