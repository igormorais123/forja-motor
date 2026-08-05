# 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes

> **EMENDAS NORMATIVAS — 25/07/2026.** Este documento vale **acrescido da seção 9 de `36_CONSOLIDACAO_CONSELHO_E_PARECER_FINAL.md`** (emendas E1 a E16: conselho Helena e Cícero, migração do modelo editorial Fable 5 para Opus 5 com revisão cruzada entre famílias, perímetro de sigilo, testes negativos, registro de escopo e Onda -1). Em conflito, prevalece a seção 9. Os `ANEXO_A/B/C` são histórico e não se executam.


**Versão:** 1.0  
**Data:** 25/07/2026  
**Estado:** desenho técnico consolidado para implementação  
**PRD:** `planejamento/33_PRD_FORJA_ASSINATURA_LITE_COCRIACAO_PRECEDENTES.md`  
**Roadmap:** `planejamento/35_ROADMAP_EXECUCAO_FORJA_ASSINATURA_LITE.md`  
**Arquitetura:** `planejamento/32_PLANO_UNICO_CONSOLIDADO_V2_2026-07-25.md`

Este TDD substitui o documento 28 como desenho imediato. A arquitetura N-way do TDD 28 permanece fora da v1.

---

## 1. Objetivo técnico

Estender a esteira F2–F7 sem criar nova fase canônica:

```text
F2-A question tree
  └─ F2-B seleção dialética + consulta + decisões
       ├─ F3-B mapa do destinatário
       └─ F4 signature brief
            └─ F5 trilha jurídica + verificação de âncoras
                 └─ F6 um draft
                      └─ F7/F7-B recomposição e preservação
```

Novos tipos de artefato N4:

- `F3_MAPA_DESTINATARIO.json`;
- `F4_SIGNATURE_BRIEF.json`.

Extensões:

- `F2_QUESTION_TREE.json`;
- `source_ledger`;
- `verified_source_ledger`;
- recibo `gostoJuridico`.

Ativo offline:

- `autoresearch/IDENTITY_CORPUS_MANIFEST.jsonl`.

## 2. Restrições observadas no sistema vivo

1. F0–F10 são resolvidas por `forja_phase_contracts.py`.
2. Schemas e contratos N4 são gerados por `generate_n4_contracts.py`.
3. `forja_n4_common.ARTIFACT_SPECS` é fonte do catálogo gerado.
4. `generate_n4_contracts.EXTENSIONS` é fonte dos outputs e gates N4.
5. `forja_n4_validate.VALIDATORS` e `_schema_findings()` validam o catálogo.
6. `forja_reasoning.validate_question_tree()` já delega F2-A para `forja_exploracao_100`.
7. F2-A já bloqueia questão material não respondida e exige `supportIds` em respostas factuais.
8. `forja_run.py` recompõe o `verified_source_ledger` e o bundle F7-B durante promoção.
9. `forja_package.validate_source_ledger()` é fachada pública de liberação das fontes.
10. `forja_editorial_fidelity.validate_editorial_bundle()` não recompõe hoje o recibo `gostoJuridico`.
11. `FORJA_SEARCH_CONFIG.json` permite menos ações que o agente TeiaJus anuncia.
12. `forja_n4_validate._effective_mode()` resolve apenas o namespace global `n4`.
13. `FORJA_N3_CONFIG.json` já possui casos N4 em `pilot_blocking`; a feature nova não pode herdar esse estado implicitamente.
14. F8 continua consumindo um único `final_markdown`.
15. O baseline dirigido em 25/07/2026 passou: `104 passed, 3 subtests passed`.

---

## 3. Decisões arquiteturais

### DA-01 — Sem nova fase

F2-B e F3-B são subestágios observáveis. A tupla F0–F10 permanece.

### DA-02 — Namespace de feature próprio

Adicionar a `FORJA_N3_CONFIG.json`:

```json
{
  "forjaAssinaturaLite": {
    "schemaVersion": 1,
    "mode": "off",
    "pilotCases": [],
    "consultationOutboundPolicy": "manual_review_only",
    "recipientMapFreshnessHours": 24,
    "allowPaidResearch": false
  }
}
```

Valores de `mode`: `off`, `shadow`, `pilot_blocking`.

Não reutilizar diretamente `n4.mode`, pois ele já possui pilotos vivos.

### DA-03 — Compatibilidade por protocolo

O envelope N4 continua `schemaVersion: 1`. A evolução aditiva será marcada por protocolos específicos:

- `FORJA-F2B-DIALECTIC-v1`;
- `FORJA-RECIPIENT-MAP-v1`;
- `FORJA-SIGNATURE-BRIEF-v1`;
- `FORJA-LEGAL-SEARCH-TRACE-v1`;
- `FORJA-PRECEDENT-ANCHOR-v1`;
- `FORJA-GOSTO-EDGE-v2`.

Artefatos históricos permanecem legíveis. O modo bloqueante exige os protocolos novos somente para casos elegíveis.

### DA-04 — Schemas gerados, não editados isoladamente

Alterar primeiro:

- `forja_n4_common.py`;
- `generate_n4_contracts.py`.

Depois executar o gerador e revisar o diff de:

- `n4_schemas/ARTIFACT_CATALOG.json`;
- schemas individuais;
- `phase_contracts_n4/F*.json`;
- `phase_contracts_n4/EXTENSIONS.json`.

Edição manual apenas dos arquivos gerados é proibida.

### DA-05 — Um draft

Não alterar `phase_contracts/F6.json` para múltiplos candidatos. F6 recebe um brief aprovado e produz um `draft_markdown`.

---

## 4. Modo efetivo

Adicionar em `forja_n4_validate.py` uma resolução genérica preservando a fachada atual:

```python
def _effective_named_mode(
    config: dict,
    case_dir: Path,
    namespace: str,
    override: str | None = None,
) -> tuple[str, str]:
    ...

def _effective_mode(config, case_dir, override=None):
    return _effective_named_mode(config, case_dir, "n4", override)

def effective_signature_lite_mode(config, case_dir, override=None):
    return _effective_named_mode(
        config, case_dir, "forjaAssinaturaLite", override
    )
```

Regras:

- modo desconhecido: erro;
- `off`: não materializa nem exige artefato;
- `shadow`: materializa e reporta, sem bloquear saída canônica;
- `pilot_blocking`: bloqueia somente `pilotCases`; fora deles, `shadow`;
- override é auditável;
- ausência de namespace equivale a `off`.

`validate_case()` deve resolver também o modo da feature e acrescentar
`F3_MAPA_DESTINATARIO.json` e `F4_SIGNATURE_BRIEF.json` ao conjunto requerido
somente quando o modo efetivo da feature não for `off`. Não adicionar esses
arquivos a `FLAG_FILES` sob um booleano concorrente: o namespace
`forjaAssinaturaLite.mode` é a fonte única de ativação.

Reason codes:

- `FAL-MODE-UNKNOWN`;
- `FAL-PILOT-IDENTITY-MISSING`;
- `FAL-OVERRIDE-RECORDED`.

---

## 5. F2-B — extensão da árvore e consulta

### 5.1 Fonte canônica

Alterar:

- `generate_n4_contracts.QUESTION_TREE_SCHEMA`;
- `forja_exploracao_100.py`;
- `forja_reasoning.validate_question_tree()`;
- `test_forja_exploracao_100.py`;
- `test_forja_n4.py`.

### 5.2 Estrutura aditiva

Adicionar ao `F2_QUESTION_TREE.json`:

```json
{
  "dialecticProtocolVersion": "FORJA-F2B-DIALECTIC-v1",
  "dialecticConsultation": {
    "status": "not_selected|draft|awaiting_review|sent|partially_answered|answered|blocked|not_applicable",
    "selectedQuestionIds": ["Q001"],
    "renderedBodySha256": null,
    "outboundPolicy": "manual_review_only",
    "outboundReceiptId": null,
    "responseRefs": [],
    "round": 1
  },
  "decisionLedger": []
}
```

Campos adicionais por pergunta selecionada:

```json
{
  "questionType": "fact|evidence|authorization|objective|strategy|presentation",
  "selectionReason": "...",
  "alreadyResearched": ["source-id"],
  "humanAuthority": "responsible_lawyer|client|office|titular",
  "silencePolicy": "block_dependent|keep_options_open|explicit_reversible_default|not_applicable",
  "silenceConsequence": "...",
  "defaultValue": null
}
```

Entrada de `decisionLedger`:

```json
{
  "decisionId": "DEC-...",
  "questionIds": ["Q001"],
  "responseRef": "message-or-meeting-id",
  "responseAuthor": "...",
  "channel": "email|whatsapp|audio|meeting|other",
  "epistemicStatus": "office_declaration|confirmed_document|confirmed_official_source|legal_inference|strategic_hypothesis|not_verified",
  "decision": "...",
  "affectedArtifactIds": ["F4_SIGNATURE_BRIEF.json"],
  "remainingOpenIssues": [],
  "decidedAt": "...",
  "approvedBy": "..."
}
```

### 5.3 Seleção determinística

Uma pergunta só pode entrar em `selectedQuestionIds` se:

- status atual for `blocked`;
- materialidade for `decisive` ou `material`, salvo justificativa;
- `caseAnchor` e `whyItMatters` existirem;
- nenhuma fonte registrada já a responder;
- `silencePolicy` e `humanAuthority` existirem.

O seletor deve ordenar por:

1. impacto sobre identidade do produto;
2. risco factual ou de autorização;
3. impacto sobre rota;
4. dependências downstream;
5. ID como desempate determinístico.

Não impor truncamento em 12. Acima de 12, emitir `FAL-F2B-QUESTION-VOLUME` P1 e exigir justificativa de rodada.

Os estados canônicos das perguntas continuam `answered`, `blocked` e
`not_applicable`. As ramificações legadas de
`forja_reasoning.validate_question_tree()` para `retired` e
`accepted_by_human`, hoje não admitidas pelo schema F2-A, devem ser removidas
ou explicitamente versionadas. Nenhum produtor novo pode emitir estado que o
schema gerado rejeite.

### 5.4 Gates

- `dialectic_questions_material`;
- `dialectic_questions_not_answered_in_record`;
- `silence_policy_safe`;
- `human_decisions_attributed`;
- `material_decisions_resolved_or_blocked`.

Reason codes mínimos:

- `FAL-F2B-REDUNDANT`;
- `FAL-F2B-NO-MATERIALITY`;
- `FAL-F2B-NO-SILENCE-POLICY`;
- `FAL-F2B-FACT-DEFAULT`;
- `FAL-F2B-PARTIAL-CLOSED`;
- `FAL-F2B-DECISION-NO-AUTHOR`;
- `FAL-F2B-OFFICE-AS-FACT`;
- `FAL-F2B-OUTBOUND-UNAUTHORIZED`.

### 5.5 Renderização

Adicionar ao CLI existente `forja_exploracao_100.py`:

- `render-consultation <json> --output <md>`;
- `record-response <json> --response <json>`.

Template:

- `templates/F2_CONSULTA_ADVOGADO.md`.

O renderizador:

- não altera respostas;
- inclui apenas perguntas selecionadas;
- grava hash no artefato;
- recusa render se houver pergunta sem consequência;
- não envia mensagem.

O gravador de resposta:

- é append-only para decisões;
- não converte automaticamente `office_declaration` em suporte factual;
- mantém questão aberta quando a resposta for parcial.

---

## 6. F3-B — mapa do destinatário

### 6.1 Registro

Adicionar a `forja_n4_common.ARTIFACT_SPECS`:

```python
"F3_MAPA_DESTINATARIO.json": {
    "type": "recipient_map",
    "phase": "F3_FONTES_REGIMENTO_LEIS",
    "keys": ["recipient", "competence", "prevention", "composition", "positions"]
}
```

Adicionar `recipient_map` aos outputs F3 de `generate_n4_contracts.EXTENSIONS`.

### 6.2 Schema

Campos:

```json
{
  "protocolVersion": "FORJA-RECIPIENT-MAP-v1",
  "recipient": {
    "court": "...",
    "organ": "...",
    "rapporteur": "...",
    "identityStatus": "confirmed|unknown"
  },
  "competence": {
    "status": "confirmed|unknown|not_applicable",
    "basis": "...",
    "sourceIds": []
  },
  "prevention": {
    "status": "confirmed|unknown|not_applicable",
    "originCaseId": null,
    "basis": null,
    "sourceIds": []
  },
  "composition": {
    "status": "confirmed|stale|unknown|not_applicable",
    "members": [],
    "checkedAt": null,
    "validUntil": null,
    "sourceIds": []
  },
  "positions": [],
  "divergences": [],
  "appellateRoute": {},
  "limitations": []
}
```

Cada posição:

- `positionId`;
- nível: `rapporteur`, `organ`, `same_section_other_organ`, `section`, `special_court`, `plenary`, `other`;
- `issueId`;
- `decisionIds`;
- `status`;
- `asOf`;
- `summary`;
- `sourceIds`.

### 6.3 Validador

Adicionar `validate_recipient_map()` em `forja_reasoning.py` e registrá-lo em:

- `forja_reasoning.VALIDATORS`;
- `forja_n4_validate.VALIDATORS`;
- `_cross_reference_findings()`.

Gates:

- `recipient_identity_sourced`;
- `competence_sourced_or_unknown`;
- `prevention_sourced_or_unknown`;
- `composition_current_or_unknown`;
- `positions_reference_sources`;
- `topology_scope_justified`.

Falhas:

- `FAL-F3-RECIPIENT-UNSOURCED`;
- `FAL-F3-PREVENTION-DATAJUD-ONLY`;
- `FAL-F3-COMPOSITION-STALE`;
- `FAL-F3-COMPOSITION-NO-OFFICIAL-SOURCE`;
- `FAL-F3-POSITION-NO-DECISION`;
- `FAL-F3-TOPOLOGY-UNJUSTIFIED`.

### 6.4 Freshness

O validador calcula freshness com `recipientMapFreshnessHours`. Não confiar em `status=confirmed` autodeclarado. Em `pilot_blocking`, composição stale vira P0 se a estratégia depender dela; caso contrário, P1 com uso proibido.

---

## 7. F4 — signature brief

### 7.1 Registro

Adicionar a `ARTIFACT_SPECS`:

```python
"F4_SIGNATURE_BRIEF.json": {
    "type": "signature_brief",
    "phase": "F4_BLUEPRINT_ESTRATEGICO",
    "keys": ["decisiveQuestion", "routes", "selectedRouteId", "mandatoryContent"]
}
```

Adicionar `signature_brief` aos outputs F4 N4.

### 7.2 Schema

```json
{
  "protocolVersion": "FORJA-SIGNATURE-BRIEF-v1",
  "decisiveQuestion": "...",
  "demonstratedConsequence": "...",
  "routes": [
    {
      "routeId": "R1",
      "thesisIds": [],
      "description": "...",
      "anchorCandidateIds": [],
      "bestObjection": "...",
      "response": "...",
      "decision": "selected|rejected|open",
      "decisionReason": "..."
    }
  ],
  "selectedRouteId": "R1",
  "humanDecisionId": "DEC-...",
  "motherSentence": "...",
  "decisiveFactIds": [],
  "decisiveDocumentIds": [],
  "mandatoryContent": [],
  "blockingIssues": []
}
```

### 7.3 Validador

Adicionar `validate_signature_brief()` em `forja_reasoning.py`.

Regras:

- IDs referenciam `F2_QUESTION_TREE`, `F3_REASONING_GRAPH`, `F4_THESIS_MATURITY`, `source_ledger` ou mapa;
- exatamente uma rota `selected` quando não houver bloqueio;
- `selectedRouteId` coincide com a rota;
- rota material possui `humanDecisionId`;
- uma rota exige `singleRouteReason`;
- mais de quatro exige `complexityReason`;
- rotas não podem ter mesmo conjunto de teses, âncoras e objeção;
- âncora não verificada é candidata, nunca final;
- `blockingIssues` impede `draftRelease`.

Reason codes:

- `FAL-F4-NO-DECISIVE-QUESTION`;
- `FAL-F4-ROUTE-DUPLICATE`;
- `FAL-F4-ROUTE-ARTIFICIAL`;
- `FAL-F4-SELECTION-MISMATCH`;
- `FAL-F4-SELECTION-NO-HUMAN-DECISION`;
- `FAL-F4-ANCHOR-DANGLING`;
- `FAL-F4-BLOCKED-RELEASE`.

---

## 8. F5 — trilha de pesquisa jurídica

### 8.1 Extensão do `source_ledger`

Não criar novo artefato obrigatório. Adicionar bloco:

```json
{
  "legalResearchProtocol": "FORJA-LEGAL-SEARCH-TRACE-v1",
  "searchRuns": [
    {
      "queryId": "QRY-...",
      "database": "...",
      "endpointOrTool": "...",
      "executedAt": "...",
      "query": "...",
      "filters": {},
      "resultIds": [],
      "discarded": [{"resultId": "...", "reason": "..."}],
      "negativeResult": false,
      "notSearched": [],
      "replayRef": "...",
      "limitations": []
    }
  ]
}
```

Os ledgers reais existem em mais de uma forma histórica (`entries`, `sources`
ou lista direta). O bloco `searchRuns` é top-level e aditivo; a implementação
não deve reformatar entradas antigas. `_ledger_entries()` continua sendo a
normalização canônica para a liberação.

Atualizar produtores F5 e validar em uma função pública nova:

- `forja_package.validate_legal_research_trace(payload, mode)`.

`validate_source_ledger()` continua sendo a fachada de liberação e passa a incluir o resultado dessa validação.

### 8.2 Gates

- query ID único;
- base identificada;
- horário e filtros presentes;
- resultados e descartes não sobrepostos;
- resultado negativo associado a query executada;
- replay existente quando declarado;
- ação TeiaJus permitida.

Reason codes:

- `FAL-F5-QUERY-INCOMPLETE`;
- `FAL-F5-RESULT-DISCARD-OVERLAP`;
- `FAL-F5-NEGATIVE-NO-QUERY`;
- `FAL-F5-REPLAY-MISSING`;
- `FAL-F5-PAID-ACTION-DENIED`.

---

## 9. F7 — precedente-âncora

### 9.1 Extensão do `verified_source_ledger`

Entrada marcada `anchor: true` deve possuir:

```json
{
  "anchorProtocol": "FORJA-PRECEDENT-ANCHOR-v1",
  "anchorId": "ANC-...",
  "routeId": "R1",
  "fullTextStatus": "verified|insufficient|not_applicable",
  "holding": {
    "text": "...",
    "locator": "...",
    "excerptSha256": "..."
  },
  "confusableObiter": [],
  "decisiveFacts": [],
  "elementComparison": [],
  "operation": "apply|distinguish|limit_scope|argue_overruling",
  "regime": {
    "legalBasis": [],
    "authorityType": "...",
    "dutyOrEffect": "...",
    "competentBody": "...",
    "changePath": "...",
    "validityStatus": "...",
    "checkedAt": "..."
  }
}
```

### 9.2 Regras

- `routeId` deve ser a rota selecionada ou uma rota explicitamente comparada;
- `holding` exige íntegra suficiente;
- ementa isolada produz `fullTextStatus=insufficient`;
- trecho e locator são hash-bound;
- `elementComparison` deve cobrir elementos declarados como determinantes;
- regime não recebe score universal;
- autoridade antiga ou monocrática não é rebaixada automaticamente;
- âncora inválida retorna reason code de reabertura F4.

Atualizar:

- `forja_package.validate_source_ledger()`;
- `forja_run._validate_f7_source_ledger()`;
- `forja_claim_binding.py`, se o binding de parágrafo precisar conhecer `anchorId`;
- testes anti-alucinação e anti-cheat.

Reason codes:

- `FAL-F7-ANCHOR-NO-FULL-TEXT`;
- `FAL-F7-HOLDING-NO-LOCATOR`;
- `FAL-F7-HOLDING-HASH-MISMATCH`;
- `FAL-F7-FACT-FRAME-INCOMPLETE`;
- `FAL-F7-REGIME-INCOMPLETE`;
- `FAL-F7-ANCHOR-INVALIDATES-ROUTE`.

---

## 10. TeiaJus

### 10.1 Allowlist v1

Atualizar `FORJA_SEARCH_CONFIG.json` somente após teste de capabilities. Adicionar como leitura:

- `research_sources`;
- `research_plan`;
- `research_search`;
- `research_mission_get`.

Não adicionar:

- `research_mission`;
- `captcha_solve`;
- `apify_contact_enrich`;
- qualquer ação `read_paid`;
- qualquer mutação sem flag explícita.

### 10.2 CLI

O subcomando genérico `execute` já existe. Na primeira versão, não criar aliases antes de provar uso recorrente. O TDD exige:

- validação de parâmetros por ação permitida;
- captura em `artifact_dir`;
- telemetria sanitizada;
- registro do action mode retornado por capabilities;
- recusa se capabilities divergir da política local.

### 10.3 Classificação de fonte

Cada resultado recebe:

- `discovery_only`;
- `metadata_evidence`;
- `official_summary`;
- `official_full_text`;
- `administrative_data`;
- `administrative_decision`.

DataJud: no máximo `metadata_evidence`.  
Espelho/ementa STJ: `official_summary`.  
Texto diário com hash: candidato a `official_full_text`, sujeito aos gates.  
CGU CEIS/CNEP/CEAF/CEPIM/leniência: `administrative_data`.

---

## 11. Identidade e AUTO-RESEARCH

### 11.1 Manifest

Criar `autoresearch/IDENTITY_CORPUS_MANIFEST.jsonl`, sem conteúdo bruto, com:

- `itemId`;
- `path` ou referência controlada;
- `sha256`;
- `documentType`;
- `date`;
- `declaredAuthor`;
- `fabioRole`;
- `attributionConfidence`;
- `sourceChannel`;
- `versionRole`;
- `relatedItemIds`;
- `permittedUse`;
- `contentClass`;
- `reviewedBy`;
- `reviewedAt`.

Enums devem reutilizar, quando compatível:

- `CONTENT_CLASSES`;
- `CONTRIBUTION_ORIGINS`;
- `CONFIDENCE`;
- `CONTRIBUTION_STATUS`;

de `forja_learning.py`.

### 11.2 Validação

Adicionar a `forja_learning.py`:

- `validate_identity_corpus_entry()`;
- `validate_identity_corpus_manifest()`.

Regras:

- hash obrigatório;
- arquivo ou referência existe;
- autoria desconhecida não recebe `human_authored`;
- transcript usa `permittedUse=thought_oral`;
- diff exige origem de cada mudança antes de promover preferência;
- conteúdo privado não é copiado para relatórios;
- regra global exige aprovação e duas evidências independentes, preservando disciplina atual.

### 11.3 Integração com AUTO-RESEARCH

O corpus de identidade não altera `AR_CORPUS.json`. Ele é uma camada de metadados usada para:

- selecionar exemplos autorizados;
- estratificar avaliações;
- explicar proveniência;
- medir aceitação e reescrita.

F6 não lê itens `unknown` ou não autorizados. Nenhuma memória de caso é exposta por similaridade sem política.

---

## 12. F6 e F7-B

### 12.1 Input de F6

Em sombra, o incumbente continua. A variante experimental recebe:

- `F4_SIGNATURE_BRIEF.json`;
- anchors F5 verificadas;
- padrões de identidade autorizados;
- mesmos fatos, proposições e fontes do incumbente.

O Python não seleciona automaticamente um novo texto de produção na Onda 2. O AUTO-RESEARCH pareado compara outputs offline.

### 12.2 Recibo `gostoJuridico` v2

Atualizar `forja_fable5.py` para aceitar `FORJA-GOSTO-EDGE-v2`:

- `signatureBriefSha256`;
- `selectedRouteId`;
- rotas consideradas em faixa flexível;
- âncoras por ID;
- consequência;
- protocolo anterior aceito em casos legados.

Remover o gate fixo de “três direções” para v2. Manter v1 legível.

### 12.3 Recomposição independente

Adicionar à assinatura de `validate_editorial_bundle()` parâmetros opcionais:

```python
signature_brief_path: Path | None = None
```

Quando presente:

- recomputar hash do brief;
- conferir `selectedRouteId`;
- conferir âncoras e conteúdo obrigatório;
- validar recibo v2 sem confiar no relatório do modelo.

Preservar chamadas existentes por default `None`.

Atualizar consumidores:

- `forja_run._validate_fable5_editorial()`;
- `forja_package.py`;
- `test_forja_fable5.py`;
- `test_forja_run.py`;
- `test_forja_n3_package.py`.

---

## 13. Invalidação

Adicionar arestas ao mecanismo N4 de invalidação:

| Mudança | Invalida |
|---|---|
| resposta/decisão F2-B | mapa ou brief que a referenciam |
| competência, prevenção ou composição | mapa e brief |
| `selectedRouteId` | pesquisa de âncoras, draft e F7 |
| anchor/full text/hash | brief selecionado e draft |
| padrão de identidade promovido | apenas variante editorial e avaliações |
| fonte ou trecho | ledger, anchor, parágrafo e package |

Invalidação é append-only e registra:

- artefato raiz;
- hash anterior e novo;
- dependentes;
- reason code;
- ação exigida;
- ator e horário.

Não apagar artefatos stale.

---

## 14. Arquivos a alterar

### Núcleo declarativo

- `FORJA_N3_CONFIG.json`;
- `forja_n4_common.py`;
- `generate_n4_contracts.py`;
- `phase_contracts_n4/F2.json` a `F7.json` — gerados;
- `phase_contracts_n4/EXTENSIONS.json` — gerado;
- `n4_schemas/ARTIFACT_CATALOG.json` — gerado;
- schemas novos e schema F2 — gerados.

### Validadores e execução

- `forja_exploracao_100.py`;
- `forja_reasoning.py`;
- `forja_n4_validate.py`;
- `forja_package.py`;
- `forja_run.py`;
- `forja_fable5.py`;
- `forja_editorial_fidelity.py`;
- `forja_learning.py`;
- `forja_n4_invalidation.py`;
- `forja_legal_search.py`, apenas se a validação de action exigir mudança.

### Configuração e templates

- `FORJA_SEARCH_CONFIG.json`;
- `templates/F2_CONSULTA_ADVOGADO.md`;
- `autoresearch/IDENTITY_CORPUS_MANIFEST.jsonl`.

### Testes

- novo `test_forja_assinatura_lite.py`;
- `test_forja_exploracao_100.py`;
- `test_forja_n4.py`;
- `test_forja_legal_search.py`;
- `test_forja_fable5.py`;
- `test_forja_run.py`;
- `test_forja_n3_package.py`;
- `test_forja_anti_hallucination_v2.py`;
- `test_forja_anti_cheat.py`;
- `test_forja_autoresearch.py`;
- `test_forja_architecture.py`.

Não criar pacote `forja/signature/` nem CLI própria.

---

## 15. Matriz requisito → componente → teste

| Requisito | Componente | Teste principal |
|---|---|---|
| RF-01 | resolver modo | `test_mode_off_shadow_pilot_cases` |
| RF-02, RF-03 | F2-B | `test_material_selection_and_silence_policy` |
| RF-04, RF-05 | render/ledger | `test_consultation_hash_and_partial_response` |
| RF-06 | outbound | `test_outbound_without_receipt_is_denied` |
| RF-07, RF-08 | recipient map | `test_datajud_cannot_confirm_composition_or_prevention` |
| RF-09, RF-10 | brief | `test_route_selection_and_non_artificiality` |
| RF-11 | search trace | `test_query_replay_negative_and_discarded_results` |
| RF-12 | anchor | `test_anchor_requires_full_text_holding_locator` |
| RF-13 | TeiaJus | `test_paid_and_non_allowlisted_actions_denied` |
| RF-14 | admin source | `test_cgu_registry_not_administrative_precedent` |
| RF-15, RF-16 | identity | `test_identity_attribution_and_permitted_use` |
| RF-17 | F6/F7-B | `test_single_draft_and_signature_recomposition` |
| RF-18 | invalidation | `test_anchor_change_reopens_brief_and_draft` |
| RF-19 | migration | `test_legacy_artifacts_remain_valid` |
| RF-20 | telemetry | `test_mode_hash_query_and_decision_are_recorded` |

---

## 16. Testes obrigatórios

### 16.1 Unidade

- resolução de modo;
- seleção e ordenação de perguntas;
- política de silêncio;
- autoria da decisão;
- freshness;
- duplicidade de rotas;
- cross-reference;
- search trace;
- holding/locator/hash;
- classificação de fonte;
- manifest de identidade;
- recibo v2.

### 16.2 Contrato e migração

- gerador idempotente;
- catálogo e schemas sincronizados;
- contratos N4 sincronizados;
- artefatos v1 legíveis;
- novos artefatos exigidos só no modo aplicável;
- chamadas antigas de `validate_editorial_bundle()` válidas.

### 16.3 Integração

- F2-B → F4;
- mapa → brief;
- brief → search trace;
- anchor inválida → reabertura;
- brief → F6 variante;
- F7-B → package;
- TeiaJus artifact → source ledger.

### 16.4 Adversariais

- pergunta já respondida enviada;
- fato com default;
- resposta parcial marcada resolvida;
- `office_declaration` usada como prova;
- composição stale apresentada como atual;
- DataJud apresentado como prevenção;
- ementa apresentada como ratio;
- anchor com locator falso;
- rota duplicada lexicalmente;
- ação TeiaJus paga disfarçada de leitura;
- diff sem autoria atribuído a Fábio;
- recibo `gostoJuridico` adulterado;
- `approved=true` sem recomputação.

### 16.5 Metamórficos

- trocar ordem das rotas sem mudar ID selecionado;
- renomear parte sem alterar relações;
- retirar decisão humana;
- retirar fonte da composição;
- alterar um termo do holding;
- trocar routeId no recibo;
- mudar hash do brief;
- converter transcript em peça escrita;
- remover query que sustenta resultado negativo.

### 16.6 Regressão

Baseline dirigido:

```powershell
python -m pytest -q -p no:cacheprovider `
  test_forja_exploracao_100.py `
  test_forja_legal_search.py `
  test_forja_fable5.py `
  test_forja_n4.py `
  test_forja_run.py `
  test_forja_anti_hallucination_v2.py
```

Baseline observado antes da implementação: `104 passed, 3 subtests passed`.

A contagem futura deve vir da execução viva, não deste número histórico.

---

## 17. Comandos de verificação por mudança

```powershell
python generate_n4_contracts.py
python -m json.tool n4_schemas\ARTIFACT_CATALOG.json > $null
python forja_phase_contracts.py

python -m pytest -q -p no:cacheprovider `
  test_forja_assinatura_lite.py `
  test_forja_exploracao_100.py `
  test_forja_n4.py `
  test_forja_legal_search.py `
  test_forja_fable5.py `
  test_forja_run.py `
  test_forja_n3_package.py `
  test_forja_anti_hallucination_v2.py `
  test_forja_anti_cheat.py `
  test_forja_autoresearch.py `
  test_forja_architecture.py

python validate_forja_n3.py --real-word --run-replay
python forja_regua.py
```

Depois de mudança estrutural relevante:

```powershell
python "C:\Users\IgorPC\.claude\projects\00_MAPA_ARQUITETURA_IA\REGENERAR_MAPAS_ARQUITETURA.py"
python "C:\Users\IgorPC\.claude\projects\00_MAPA_ARQUITETURA_IA\APROFUNDAR_MAPAS_ARQUITETURA.py"
```

Renderizar e inspecionar os HTMLs, consultar Graphify e atualizar hashes.

---

## 18. Critério técnico de concluído

1. modos e `pilotCases` têm namespace próprio;
2. artefatos novos estão no catálogo, schemas e contratos gerados;
3. F2-B não pergunta o que o acervo responde;
4. silêncio material não cria fato;
5. resposta e decisão têm autoria e proveniência;
6. mapa não trata metadado como prova de composição/prevenção;
7. brief tem rota útil, decisão e referências válidas;
8. pesquisa jurídica é reproduzível;
9. anchor decisiva possui conteúdo, locator, hash, confronto e regime;
10. TeiaJus recusa ação paga ou não autorizada;
11. corpus não produz falsa autoria;
12. F6 mantém um draft;
13. F7/F7-B recompõem brief, rota e recibo;
14. invalidadores foram exercitados;
15. casos legados passam;
16. rollback `off` passa;
17. suíte dirigida, suíte ampliada, replay e Régua passam;
18. mapas arquiteturais foram regenerados e validados;
19. nenhuma alegação de eficácia excede a evidência.

Sem piloto, o estado máximo é `technical_capability_complete`. Promoção posterior exige os gates do PRD.
