# TDD — FORJA-ASSINATURA

> **RECLASSIFICADO EM 25/07/2026 — desenho experimental de longo prazo.**  
> O TDD vigente para execução é `planejamento/34_TDD_FORJA_ASSINATURA_LITE_COCRIACAO_PRECEDENTES.md`.

**Versão:** 1.0 revisada  
**Data:** 24/07/2026  
**Estado:** desenho técnico para implementação  
**PRD:** `planejamento/27_PRD_FORJA_ASSINATURA.md`  
**Plano:** `planejamento/26_PLANO_IMPLEMENTACAO_FORJA_ASSINATURA.md`

## 1. Objetivo técnico

Adicionar à FORJA uma subesteira hash-bound que:

1. explora geometrias em F4-S;
2. confirma lastro em F5;
3. produz microbriefs e shortlist em F5-S;
4. materializa incumbente e desafiante em F6-A;
5. julga cegamente em F6-B;
6. promove um único `draft_markdown` em F6-C;
7. mede recall/steelman;
8. garante preservação estrutural em F7/F7-B;
9. registra decisão para análise offline sem alimentar o gerador.

Não criar nova fase canônica. F4-S, F5-S e F6-A/B/C são subestágios internos
observáveis; a tupla F0–F10 permanece.

## 2. Restrições do sistema vivo

1. `forja_phase_contracts.py` resolve os contratos F0–F10.
2. `phase_contracts/F6.json` não possui inputs condicionais.
3. `forja_run.py` publica artefatos e recompõe gates; `exit 0` não é promoção.
4. `forja_n4_validate.py` possui `FLAG_FILES`, `VALIDATORS` e modo efetivo por
   `pilotCases`.
5. `forja_ar_blind.py` é binário; N-way exige componente novo.
6. `forja_ar_evolucao.py` usa menor SHA em desempate múltiplo; a nova camada
   não pode chamar esse caminho para decidir mérito.
7. `forja_fable5.py` valida `gostoJuridico` em função privada.
8. `forja_editorial_fidelity.py` recompõe o bundle F7-B e deve receber o
   validador público de assinatura.
9. F8 consome `final_markdown`; essa interface não muda.
10. contratos N4 e catálogo são gerados; não criar fonte paralela.

## 3. Topologia

```text
F4 inputs
  │
  ├─ signature.snapshot ─────────────┐
  ├─ F4-S map                        │
  └─ F4-S geometries                 │
           │                         │
           ▼                         │
      F5 grounding                   │
           │                         │
           ▼                         │
   F5-S microbriefs + shortlist      │
           │                         │
           ├──────────────┐          │
           ▼              ▼          │
 candidate_0        challenger_1     │
 incumbent flow     signature flow   │
           └──────┬───────┘          │
                  ▼                  │
           legal eligibility         │
                  ▼                  │
           blind N-way judge         │
                  ▼                  │
        recall + steelman diagnostics│
                  ▼                  │
             selection              │
                  ▼                  │
       one canonical draft_markdown │
                  ▼                  │
                 F7 ── structural revalidation
                  ▼
                F7-B ── final signature fidelity
                  ▼
             final_markdown
                  ▼
                  F8
```

## 4. Estrutura de arquivos-alvo

```text
forja/
  signature/
    __init__.py
    models.py
    contracts.py
    config.py
    snapshot.py
    geometry.py
    grounding.py
    candidates.py
    blind.py
    selection.py
    recall.py
    topology.py
    invalidation.py
    memory.py
    telemetry.py
    reason_codes.py

forja_signature.py

n4_schemas/
  f4_signature_map.schema.json
  f4_signature_geometries.schema.json
  f5_signature_shortlist.schema.json
  f6_signature_candidates.schema.json
  f6_signature_judgment.schema.json
  f6_signature_selection.schema.json
  f6_signature_recall.schema.json

tests/ ou raiz conforme padrão atual:
  test_forja_assinatura.py
  test_forja_assinatura_contracts.py
  test_forja_assinatura_blind.py
  test_forja_assinatura_integration.py
```

Compatibilidade com o layout real prevalece. Se os testes permanecerem na raiz,
não criar um segundo padrão apenas para esta feature.

## 5. Fronteiras de responsabilidade

### 5.1 Domínio puro

Módulos sem filesystem, subprocesso ou rede:

- `models.py`;
- `geometry.py`;
- `selection.py`;
- `topology.py`;
- `invalidation.py`;
- `reason_codes.py`.

Entradas e saídas são estruturas Python imutáveis ou cópias defensivas.

### 5.2 Adapters

I/O e execução:

- `contracts.py`: schema/catalog;
- `config.py`: resolução de modo e budget;
- `snapshot.py`: leitura e hash;
- `grounding.py`: integração com ledgers;
- `candidates.py`: invocações isoladas;
- `blind.py`: bundles, mapping e julgadores;
- `recall.py`: invocações leitor/verificador;
- `memory.py`: append-only;
- `telemetry.py`: eventos;
- `forja_signature.py`: CLI/fachada.

### 5.3 Integrações existentes

- F4: sidecars de mapa/geometria;
- F5: source ledger;
- F6: execução interna e um output canônico;
- F7: correção jurídica;
- F7-B: edição local e validação;
- N4: catálogo, schemas, flag e modo por caso;
- AUTO-RESEARCH: avaliação offline;
- state machine: eventos e supersession.

## 6. Modelo de dados comum

Todo artefato:

```json
{
  "schemaVersion": 1,
  "protocolVersion": "FORJA-ASSINATURA-v1",
  "caseId": "case-...",
  "attemptId": "attempt-...",
  "generatedAt": "ISO-8601",
  "producer": {
    "component": "forja.signature...",
    "version": "..."
  },
  "inputSnapshotSha256": "64-hex",
  "configSha256": "64-hex",
  "artifactSha256": "64-hex",
  "supersedes": null
}
```

O `artifactSha256` é calculado sobre payload canônico sem o próprio campo.

### 6.1 Enums

```text
SignatureMode =
  off | shadow | pilot_blocking | default_on

ExecutionAssurance =
  envelope_verified | orchestrator_attested | self_declared

JudgeIndependenceMode =
  cross_family | cross_session_same_family | unverified

CandidateRole =
  incumbent | challenger

CandidateStatus =
  generated | blocked | eligible | rejected | selected

SelectionStatus =
  incumbent_preserved | challenger_selected | abstained_invalid
```

Enums desconhecidos falham no schema.

## 7. Configuração

Adicionar seção `signature` em `FORJA_N3_CONFIG.json` somente na W1, com
`mode=off`.

Campos obrigatórios:

```json
{
  "signature": {
    "protocolVersion": "FORJA-ASSINATURA-v1",
    "mode": "off",
    "pilotCases": [],
    "minGeometries": 5,
    "maxGeometries": 7,
    "microbriefCandidates": 3,
    "fullDraftCandidates": 2,
    "maxFullDraftCandidates": 3,
    "ambiguityRuleId": "signature-shortlist-margin-v1",
    "recallCardMaxWords": 80,
    "recallInputPolicy": "body_without_executive_summary",
    "judgeIndependencePolicy": "prefer_cross_family",
    "allowedDegradedJudgeMode": "cross_session_same_family",
    "rejectSelfJudge": true,
    "productionMemoryReadPolicy": "deny",
    "budgetProfileId": "signature-pilot-v1",
    "preserveIncumbentOnTie": true,
    "newPaidApiAllowed": false
  }
}
```

### 7.1 Resolução do modo

```python
def effective_mode(configured_mode, pilot_cases, case_identity, override=None):
    if override is not None:
        return configured_mode, validate_mode(override)
    if configured_mode != "pilot_blocking":
        return configured_mode, configured_mode
    if case_identity in pilot_cases:
        return configured_mode, "pilot_blocking"
    return configured_mode, "shadow"
```

Reutilizar/refatorar o comportamento atual de
`forja_n4_validate._effective_mode()` para uma API pública comum. Não copiar a
lógica em dois módulos.

### 7.2 Budget profile

Schema obrigatório:

```json
{
  "profileId": "signature-pilot-v1",
  "measuredAt": "ISO-8601",
  "baselineReportSha256": "64-hex",
  "maxCallsByStage": {
    "f4s": 0,
    "f5s": 0,
    "f6a": 0,
    "f6b": 0,
    "recall": 0
  },
  "maxInputTokensPerCase": 0,
  "maxOutputTokensPerCase": 0,
  "maxElapsedSecondsPerCase": 0,
  "maxJudgesPerPair": 0,
  "maxBlindComparisonsPerCase": 0,
  "maxRetriesByStage": {},
  "onExceeded": "preserve_incumbent"
}
```

Zeros acima ilustram tipos, não valores aceitos. O validador exige inteiros
positivos. W0 mede o baseline; W1 grava números e hash antes de W2.

## 8. Snapshot

### 8.1 Input

Referências aos artefatos canônicos, não cópias soltas.

### 8.2 Algoritmo

1. resolver paths;
2. confirmar existência;
3. recomputar SHA-256;
4. confirmar ledger/version;
5. montar objeto com paths relativos, hashes e papéis;
6. canonicalizar JSON;
7. calcular `inputSnapshotSha256`;
8. persistir antes da primeira chamada.

### 8.3 Proibição

Nenhum candidato, julgamento ou recall pode referir snapshot distinto no mesmo
lote. Mudança posterior cria nova tentativa.

## 9. F4-S — mapa e geometrias

### 9.1 `F4_SIGNATURE_MAP.json`

Campos de domínio:

```json
{
  "decisionQuestion": "...",
  "motherSentence": "...",
  "defaultVersion": "...",
  "decisiveAnchor": {
    "factIds": [],
    "sourceIds": []
  },
  "legalLimit": {
    "claimIds": [],
    "authorityIds": []
  },
  "bestCounterargument": "...",
  "demonstratedConsequence": "...",
  "requestedDisposition": "...",
  "mandatoryContentIds": [],
  "knownGapIds": []
}
```

Validações:

- strings não vazias;
- todos os IDs resolvem;
- `knownGapIds` não aparecem como fatos;
- providência pertence ao blueprint/pedidos;
- frase-mãe não adiciona certeza;
- conteúdo dos autos não é interpretado como instrução.

### 9.2 `F4_SIGNATURE_GEOMETRIES.json`

Cada geometria:

```json
{
  "geometryId": "g-...",
  "primaryAxis": "causality",
  "coreQuestion": "...",
  "openingMove": "...",
  "argumentOrder": [
    {"position": 1, "claimIds": ["c-1"], "purpose": "..."}
  ],
  "factIds": [],
  "authorityIds": [],
  "issueIds": [],
  "counterargument": "...",
  "response": "...",
  "decisionalConsequence": "...",
  "whyNotDefault": "...",
  "groundingStatus": "pending"
}
```

### 9.3 Diversidade determinística

Representação:

```python
signature(geometry) = (
    primary_axis,
    tuple(claim_id for step in argument_order for claim_id in step.claim_ids),
)
```

Dois candidatos são materialmente diversos quando:

1. `primaryAxis` difere; e
2. a distância normalizada de edição entre sequências de `claimIds` é maior ou
   igual ao limiar do protocolo.

O limiar é congelado no config/rubrica. Léxico ou metáfora não entram no cálculo.
Um juiz semântico pode gerar diagnóstico, mas não aprova o gate sozinho.

## 10. F5 — grounding

Função pura:

```python
ground_geometry(geometry, source_ledger, proposition_ledger) -> GroundingResult
```

Resultado por referência:

- `resolved`;
- `missing`;
- `stale`;
- `revoked`;
- `unsupported_relation`.

Agregação:

- qualquer referência central `missing|stale|revoked` → `blocked`;
- referência periférica ausente → `partially_grounded`;
- todas válidas → `grounded`.

Não realizar busca web dentro do domínio. Pesquisa adicional retorna ao fluxo
F5 existente.

## 11. F5-S — microbrief e shortlist

### 11.1 Execução isolada

O orquestrador:

1. seleciona geometrias grounded;
2. monta prompt por geometria sem output irmão;
3. calcula `promptSha256`;
4. cria sessão;
5. registra envelope real ou atestação;
6. invoca;
7. persiste output antes da próxima decisão.

Retry conserva `candidateId` e incrementa `retryIndex`; não aumenta diversidade.

### 11.2 Shortlist

Vetos primeiro. Entre elegíveis, executar comparação estrutural curta. Saída:

```json
{
  "microbriefs": [],
  "challengerRanking": [],
  "primaryChallengerGeometryId": "g-...",
  "secondaryChallengerGeometryId": "g-...",
  "ambiguity": {
    "ruleId": "signature-shortlist-margin-v1",
    "observedMargin": 0.0,
    "threshold": 0.0,
    "expand": false
  },
  "strategies": ["g-..."],
  "fallback": null,
  "abstained": false
}
```

Se nenhuma desafiante passa:

```json
{
  "strategies": [],
  "fallback": "candidate_0",
  "abstained": true,
  "reasonCode": "SIG-SHORTLIST-NO-ELIGIBLE-CHALLENGER"
}
```

O limiar vem da configuração; não é escolhido após ver os outputs.

## 12. F6-A — candidatos

### 12.1 `candidate_0`

Contrato:

- `candidateId = "candidate_0"`;
- `candidateRole = "incumbent"`;
- `generationMode = "incumbent_pipeline"`;
- mesmo `inputSnapshotSha256`;
- sessão própria;
- prompt incumbente atual, sem mapa/geometrias/shortlist;
- texto integral persistido antes do cegamento.

### 12.2 Desafiante

- recebe a shortlist e ledgers por hash;
- não recebe texto do incumbente;
- não recebe memória decisória;
- preserva conteúdo obrigatório;
- produz `paragraph_provenance`.

### 12.3 Terceiro candidato

Só existe se:

```python
expand = (
    config.expandToThirdDraftOnAmbiguity
    and shortlist.ambiguity.ruleId == config.ambiguityRuleId
    and shortlist.ambiguity.observedMargin <= shortlist.ambiguity.threshold
)
```

Não gerar terceiro draft para resolver desacordo ocorrido depois no julgamento.
Isso mudaria o orçamento com base no resultado.

### 12.4 Manifesto

```json
{
  "candidates": [
    {
      "candidateId": "candidate_0",
      "candidateRole": "incumbent",
      "generationMode": "incumbent_pipeline",
      "geometryId": null,
      "artifactPath": "...",
      "artifactSha256": "64-hex",
      "inputSnapshotSha256": "64-hex",
      "promptSha256": "64-hex",
      "executor": {
        "family": "...",
        "model": "...",
        "sessionId": "...",
        "assurance": "orchestrator_attested"
      },
      "siblingAccess": false,
      "paragraphProvenancePath": "...",
      "status": "eligible"
    }
  ]
}
```

## 13. Elegibilidade

`eligibility(candidate, ledgers, gates) -> EligibilityDecision`

Ordem:

1. schema e hashes;
2. snapshot;
3. proveniência;
4. fatos/números/datas;
5. autoridades;
6. pedidos/polaridade;
7. conteúdo obrigatório;
8. origem operacional;
9. injeção/vazamento;
10. estilo como sentinela.

Saída contém todos os achados; não parar no primeiro, salvo risco de segurança
que impeça leitura.

## 14. F6-B — cegamento e julgamento

### 14.1 Extensão, não mutação do A/B

Criar primitives N-way em `forja/signature/blind.py`. Reutilizar:

- `canonicalize`;
- `leak_scan`;
- HMAC externo;
- âncoras;
- swap;
- verificação de hashes.

Não alterar a semântica binária existente até os testes de regressão passarem.

### 14.2 Bundles

Para cada par elegível:

- A/B;
- B/A;
- nomes opacos;
- mesmo conteúdo canonicalizado;
- mapping fora do workspace;
- commitment dentro do workspace;
- hash por bundle.

### 14.3 Julgadores

O planner de bancada recebe famílias disponíveis e produz:

```json
{
  "requestedMode": "prefer_cross_family",
  "effectiveMode": "cross_session_same_family",
  "judges": [
    {
      "judgeId": "...",
      "family": "...",
      "sessionId": "...",
      "assurance": "orchestrator_attested",
      "promptSha256": "..."
    }
  ],
  "correlated": true
}
```

Regras:

- mesma `sessionId` de gerador e juiz → inválido;
- juiz com acesso ao mapping/workspace → inválido;
- `self_declared` em modo bloqueante → inválido;
- ausência de segunda família não é falsa falha se o modo degradado está
  permitido;
- modo degradado exige swap e prompts disjuntos.

### 14.4 Voto

```json
{
  "pairId": "...",
  "judgeId": "...",
  "order": 1,
  "winnerPosition": "L|R|ABSTAIN",
  "anchor": "trecho literal",
  "holisticPreference": "L|R|ABSTAIN",
  "diagnostics": {
    "caseIdentity": "...",
    "decisionalClarity": "...",
    "groundedSpecificity": "...",
    "counterargumentStrength": "...",
    "economy": "...",
    "editorialHumanity": "..."
  },
  "confidenceBand": "low|medium|high"
}
```

Diagnósticos explicam; não são somados por média.

## 15. Primitivas de seleção

Esta seção calcula elegibilidade, grafo e vencedor potencial. A função final só
é chamada em F6-C depois de os resultados de recall e steelman estarem válidos.

### 15.1 Vetos

Remover candidatos inelegíveis.

Se `candidate_0` for inelegível, o fluxo inteiro falha juridicamente: não usar
uma desafiante editorial para encobrir falha do baseline. Retornar para a fase
que originou o veto.

### 15.2 Matriz

Para cada par elegível, consolidar somente voto:

- válido;
- consistente sob swap;
- ancorado;
- produzido sob modo permitido.

### 15.3 Vencedor

```python
def select(candidates, pairwise, config):
    eligible = veto_filter(candidates)
    if not eligible:
        return invalid("SIG-NO-LEGAL-CANDIDATE")

    if only_incumbent(eligible):
        return preserve_incumbent("SIG-NO-ELIGIBLE-CHALLENGER")

    stable = stable_pairwise_graph(pairwise, config)
    winner = unique_condorcet_winner(stable)

    if winner is None:
        return preserve_incumbent("SIG-ABSTAIN-CYCLE-OR-TIE")
    if winner == "candidate_0":
        return preserve_incumbent("SIG-INCUMBENT-WON")
    if not minimum_margin_met(winner, stable, config):
        return preserve_incumbent("SIG-ABSTAIN-LOW-MARGIN")
    return select_challenger(winner)
```

Nunca ordenar por SHA para mérito. SHA serve apenas para identidade e
determinismo de armazenamento.

### 15.4 Terceiro juiz

É permitido somente se a regra já estiver no manifest:

- quais desacordos o acionam;
- limite de chamadas;
- família/sessão permitida;
- como o voto resolve;
- quando ainda deve haver abstenção.

## 16. Recall e conclusão F6-C

### 16.1 Remoção da síntese

F6 deve produzir marcadores canônicos de início/fim da síntese. Função:

```python
strip_executive_summary(markdown) -> body_markdown
```

Falha fechada quando:

- nenhum marcador;
- marcadores múltiplos;
- ordem inválida;
- corpo vazio;
- remoção atinge seção além da síntese.

Não usar LLM para localizar a síntese.

### 16.2 Leitor e verificador

Sessões separadas:

- leitor: corpo → cartão;
- verificador: cartão + mapa → fidelidade.

O leitor não recebe mapa, rubrica de campos nem síntese. O verificador não
recebe a peça.

### 16.3 Uso na seleção

- falso → elimina desafiante;
- questão/providência ausente → impede vitória;
- demais campos → diagnóstico;
- resultado não reabre candidato já inelegível;
- recall não compensa veto.

### 16.4 Seleção final

F6-C combina a matriz válida da seção 15, recall e steelman. Só então:

1. emite `F6_SIGNATURE_SELECTION.json`;
2. altera o estado de `blind_preferred` para `selected_for_f7`;
3. promove exatamente o hash selecionado para `draft_markdown`.

Falha de recall, empate ou margem insuficiente seleciona `candidate_0`; falha
jurídica do próprio incumbente reabre a fase de origem e não é mascarada por
uma desafiante.

## 17. Topologia de assinatura

### 17.1 Canonicalização

```json
{
  "motherSentenceNormalized": "...",
  "sections": [
    {
      "sectionId": "...",
      "thesisId": "...",
      "claimIds": ["..."],
      "ordinal": 1
    }
  ],
  "requestedDispositionIds": [],
  "polarityVector": []
}
```

Não incluir:

- pontuação;
- fronteira de frase;
- conectivos;
- escolhas lexicais;
- tamanho de parágrafo.

### 17.2 Comparação

Classes:

- `local_editorial_change`: passa;
- `legal_correction_nonstructural`: passa e registra;
- `structural_change`: invalida seleção;
- `request_or_polarity_change`: P0;
- `unclassifiable`: fail-closed.

### 17.3 Integração F7-B

Extrair o validador de recibo de `forja_fable5._taste_receipt_findings()` para
API pública. `validate_editorial_bundle()` chama:

1. fidelidade existente;
2. recibo de gosto;
3. topologia de assinatura;
4. hashes de seleção;
5. policy version.

O package recompõe; não confia no relatório.

## 18. Memória

### 18.1 Evento

```json
{
  "decisionId": "...",
  "caseLineage": "...",
  "product": "...",
  "selectedCandidateHash": "...",
  "rejectedCandidateHashes": [],
  "reasonCodes": [],
  "anchors": [],
  "judgeIndependenceMode": "...",
  "previousDecisionId": null,
  "eventSha256": "...",
  "previousEventSha256": "..."
}
```

### 18.2 Política de acesso

```python
def load_production_generation_context(...):
    assert config.productionMemoryReadPolicy == "deny"
    return context_without_decision_memory
```

Teste por instrumentação deve registrar os arquivos e blocos passados a cada
invocação. Regex isolada no prompt não basta; o teste compara allowlist de
inputs.

AR offline pode ler memória somente depois de formar corpus sanitizado e split.

## 19. Invalidação

Mapa de dependências:

```text
snapshot
 ├─ map
 ├─ geometries
 ├─ grounding
 ├─ shortlist
 ├─ candidates
 ├─ judgments
 ├─ recall
 └─ selection
```

Algoritmo:

1. receber evento de mudança;
2. recomputar hash da origem;
3. localizar nós descendentes;
4. marcar `stale`, nunca apagar;
5. emitir evento append-only;
6. reabrir no primeiro subestágio afetado;
7. impedir promoção de descendente stale.

## 20. Registro N4

### 20.1 Catálogo

Adicionar artefatos ao `generate_n4_contracts.py`, regenerar:

- schemas;
- `ARTIFACT_CATALOG.json`;
- `phase_contracts_n4`;
- mapas derivados.

Não editar catálogo e gerador como fontes concorrentes.

### 20.2 Flag

Feature sugerida:

```text
n4SignatureV1
```

Arquivos exigidos dependem do modo efetivo do caso. A validação deve provar:

- fora do piloto + configurado `pilot_blocking` → shadow, não bloqueia;
- dentro do piloto → arquivos e validators obrigatórios;
- `default_on` → contrato F6 formal.

## 21. Eventos

Adicionar ao state machine apenas após contratos:

```text
signature_snapshot_created
signature_geometries_created
signature_shortlist_created
signature_candidates_materialized
signature_blind_completed
signature_recall_completed
signature_selection_decided
signature_selection_invalidated
signature_final_fidelity_validated
```

Cada evento:

- `runId`;
- `attemptId`;
- `caseId`;
- `expectedRevision`;
- `idempotencyKey`;
- `artifactHashes`;
- `previousEventHash`;
- payload versionado.

## 22. Reason codes mínimos

```text
SIG-CONFIG-INVALID
SIG-BUDGET-PROFILE-MISSING
SIG-BUDGET-EXCEEDED
SIG-SNAPSHOT-DRIFT
SIG-GEOMETRY-NOT-DIVERSE
SIG-GEOMETRY-UNGROUNDED
SIG-SHORTLIST-NO-ELIGIBLE-CHALLENGER
SIG-CANDIDATE0-MISSING
SIG-CANDIDATE-SIBLING-LEAK
SIG-EXECUTION-UNVERIFIED
SIG-JUDGE-SELF
SIG-JUDGE-FAMILY-CORRELATED
SIG-BLIND-MAPPING-LEAK
SIG-BLIND-POSITION-BIAS
SIG-ABSTAIN-CYCLE-OR-TIE
SIG-ABSTAIN-LOW-MARGIN
SIG-INCUMBENT-WON
SIG-RECALL-SUMMARY-NOT-STRIPPED
SIG-RECALL-FALSE
SIG-TOPOLOGY-CHANGED
SIG-MEMORY-READ-DENIED
SIG-SELECTION-STALE
```

Reason code desconhecido não é aceito como texto livre em decisão.

## 23. CLI proposta

```powershell
python forja_signature.py snapshot --case-id <id>
python forja_signature.py map --case-id <id>
python forja_signature.py ground --case-id <id>
python forja_signature.py shortlist --case-id <id>
python forja_signature.py candidates --case-id <id>
python forja_signature.py blind --case-id <id>
python forja_signature.py recall --case-id <id>
python forja_signature.py select --case-id <id>
python forja_signature.py validate --case-id <id>
python forja_signature.py status --case-id <id>
```

Toda mutação exige `--attempt-id` explícito ou resolve a tentativa viva de modo
unívoco. `status` é read-only.

## 24. Testes

### 24.1 Unidade

- config e modo efetivo;
- budget profile positivo;
- canonical hash;
- resolução de IDs;
- distância estrutural;
- grounding;
- expansão de terceiro draft;
- veto filter;
- Condorcet;
- ciclo/empate;
- remoção de síntese;
- topologia;
- invalidation graph;
- reason codes.

### 24.2 Contrato

- todos os sete schemas válido/inválido;
- `candidate_0` obrigatório;
- assurance enum;
- independence enum;
- fallback de shortlist;
- decision com âncora;
- recall com hash;
- seleção com snapshot;
- artifacts no catálogo;
- gerador e derivados sem drift.

### 24.3 Integração

1. `off` sem invocações e sem diff de output;
2. shadow produz sidecars e mantém incumbente;
3. piloto fora da lista não bloqueia;
4. piloto dentro da lista bloqueia sem artefatos;
5. baseline + desafiante → seleção;
6. abstenção → hash de `candidate_0`;
7. desafiante vence → único `draft_markdown`;
8. F7 não estrutural → seleção válida;
9. F7 estrutural → seleção stale;
10. F7-B local → `final_markdown`;
11. F7-B estrutural → bloqueio;
12. F8/package sem regressão.

### 24.4 Metamórficos

- inverter posição;
- renomear candidato;
- trocar autor/modelo no rótulo;
- aumentar comprimento sem conteúdo;
- repetir palavras da rubrica;
- preservar palavras e mudar nexo;
- trocar nomes mantendo relações;
- remover âncora;
- retirar síntese antes do recall;
- fundir frases sem mudar topologia;
- reordenar teses mantendo vocabulário.

### 24.5 Sabotagem

- mapping adulterado;
- mapping dentro do workspace;
- prompt irmão;
- memória decisória no prompt;
- `verified=true` sem envelope;
- mesma sessão como juiz;
- family spoofing;
- âncora inexistente;
- snapshot alterado após julgamento;
- `approved=true` sem recomputação;
- menor SHA como desempate;
- terceiro draft fora da regra;
- budget editado após resultado;
- tentativa de sair do shadow sem denominador;
- seleção histórica stale promovida.

### 24.6 Canários de detector

- mudança de pedido;
- inversão de polaridade;
- troca de frase-mãe;
- reordenação de tese;
- remoção de conteúdo obrigatório;
- edição local legítima;
- falso positivo de fusão de frases;
- síntese não marcada;
- recall com elemento inventado.

## 25. Matriz requisito → teste

| Requisito | Testes principais |
|---|---|
| RF-01 | modo efetivo, off, piloto dentro/fora |
| RF-02 | snapshot drift, hash chain |
| RF-03/04 | mapa, IDs, diversidade, injection |
| RF-05 | grounding e invalidação por fonte |
| RF-06 | isolamento, shortlist, fallback |
| RF-07/08 | candidate0, terceiro draft, assurance |
| RF-09 | gates jurídicos e estilo |
| RF-10/11 | HMAC, swap, família, self-judge |
| RF-12 | Condorcet, margem, empate, SHA |
| RF-13/14 | síntese removida, falso recall, steelman |
| RF-15 | único cânone e estados |
| RF-16/17 | topologia, F7/F7-B, stale |
| RF-18 | negative prompt access |
| RF-19 | budget e fallback |
| RF-20 | telemetry schema e missingness |

## 26. Testes de promoção da política

O harness de avaliação deve pré-registrar:

- split por linhagem;
- produtos e tribunais;
- mínimo por estrato;
- margem de preferência;
- concordância;
- função sequencial de parada;
- missingness;
- budget;
- hashes de código/sensor/corpus.

Estados:

```text
technical_candidate_passed
→ independent_review_passed
→ human_promotion_approved
→ pilot_blocking
→ default_on
```

`technical_candidate_passed` requer:

- suíte e Régua;
- canários;
- zero regressão;
- ganho prospectivo sobre `candidate_0`;
- custo dentro do profile;
- rollback testado;
- nenhuma evidência stale.

## 27. Observabilidade

### 27.1 Eventos por caso

- tempo e tokens por estágio;
- candidatos tentados/elegíveis;
- reason codes;
- modo de independência;
- matriz pareada;
- recall;
- decisão;
- fallback;
- alterações em F7/F7-B.

### 27.2 Agregados

Separar por:

- produto;
- tribunal;
- fase processual;
- linhagem;
- modo;
- família/modelo;
- garantia de execução.

Não publicar média global de qualidade.

### 27.3 Alertas

- taxa de P0 > baseline;
- taxa de `unverified`;
- aumento de abstenção;
- terceiro draft acima do esperado;
- estouro de budget;
- mudança estrutural em F7/F7-B;
- recall inválido;
- regressão package/F8.

Limiares vêm do manifest de rollout.

## 28. Desempenho e cache

Chave de cache:

```text
protocolVersion
+ componentVersion
+ inputSnapshotSha256
+ promptSha256
+ configSha256
+ modelIdentity
```

Não reutilizar cache quando:

- modelo não é verificável;
- source ledger muda;
- rubrica muda;
- prompt muda;
- candidato muda;
- schema muda.

Filtros baratos precedem LLM:

1. schema;
2. IDs;
3. hash;
4. grounding;
5. gates determinísticos;
6. só então geração/julgamento/recall.

## 29. Segurança e privacidade

- HMAC key fora do workspace;
- mapping fora do workspace;
- logs sem conteúdo integral quando hashes bastarem;
- corpus público somente sanitizado;
- prompt injection tratada nos inputs jurídicos e nos bundles de juiz;
- nenhum segredo em telemetry;
- paths externos validados;
- nenhuma API paga nova;
- nenhum envio externo de peça.

## 30. Ordem de implementação e commits

### W0 — baseline

Somente medição, classificação de drift e relatório.

### W1 — linguagem

Arquivos:

- pacote vazio + tipos;
- schemas;
- config `off`;
- reason codes;
- tests de contrato;
- budget profile.

Sem chamada a modelo.

### W2 — F4-S

Mapa, geometria, diversidade, shadow e checkpoint.

### W3 — grounding

Integração F5 e invalidação por fonte.

### W4 — microbrief/shortlist

Adapters de invocação, isolamento e fallback.

### W5 — candidatos

Materialização de `candidate_0`, desafiante e gate.

### W6 — blind/selection

Primitives N-way, modo de independência e seleção.

### W7 — recall/steelman

Marcadores de síntese, leitor/verificador e canários.

### W8 — F7/F7-B

Topologia, recibo público e recomputação no package.

### W9 — memória/AR

Write-only em produção; leitura offline; indicadores.

### W10 — calibração

Manifest amostral e julgamento contra pares humanos.

### W11–W13 — rollout

Shadow, piloto e default-on, uma promoção por vez.

### W14 — documentação

Manifest, contratos, catálogo, mapas e hashes.

Cada onda:

- commit atômico;
- teste próprio;
- regressão;
- relatório;
- rollback;
- decisão de avanço.

## 31. Comandos de verificação

```powershell
python -m pytest -q -p no:cacheprovider `
  test_forja_assinatura.py `
  test_forja_assinatura_contracts.py `
  test_forja_assinatura_blind.py `
  test_forja_assinatura_integration.py `
  test_forja_autoresearch.py `
  test_forja_fable5.py `
  test_forja_estilo_humano.py `
  test_forja_run.py `
  test_forja_anti_hallucination_v2.py `
  test_forja_n4.py `
  test_forja_pso_pet.py `
  test_forja_mutation_semantic.py

python forja_phase_contracts.py
python -m json.tool FORJA_SPEC_MANIFEST.json
python validate_forja_n3.py --real-word --run-replay
python forja_regua.py
```

Na W14:

```powershell
python "C:\Users\IgorPC\.claude\projects\00_MAPA_ARQUITETURA_IA\REGENERAR_MAPAS_ARQUITETURA.py"
python "C:\Users\IgorPC\.claude\projects\00_MAPA_ARQUITETURA_IA\APROFUNDAR_MAPAS_ARQUITETURA.py"
graphify update .
```

## 32. Critério técnico de concluído

1. todos os schemas têm validator, owner e teste;
2. `candidate_0` é material e sempre recuperável;
3. piloto é condicional por caso;
4. isolamento tem evidência do orquestrador;
5. modo de julgamento real é persistido;
6. self-judge e menor SHA são impossíveis;
7. recall não vê síntese;
8. F7/F7-B preservam topologia ou invalidam;
9. memória não entra em geração;
10. budget degrada para incumbente;
11. F7 recebe um draft e F8 um final;
12. rollback `off` foi exercitado;
13. suíte e Régua estão verdes;
14. mapas e hashes foram regenerados;
15. promoção prospectiva satisfez os critérios do PRD.

Sem o item 15, a implementação pode ser marcada
`technical_capability_complete`, mas não `default_on_approved`.
