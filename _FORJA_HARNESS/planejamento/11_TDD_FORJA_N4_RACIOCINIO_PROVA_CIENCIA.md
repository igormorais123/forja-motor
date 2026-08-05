# TDD — FORJA N4: Raciocínio, Prova e Ciência

**Versão proposta:** N4.0  
**Data:** 2026-07-10  
**Status:** versão final do desenho técnico; não implementado  
**Revisão do documento:** final-r2, após auditoria cruzada de 2026-07-10  
**PRD:** `10_PRD_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`  
**Roadmap:** `12_ROADMAP_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`  
**Diagramas:** `13_DIAGRAMAS_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`  
**Base técnica:** `08_PLANO_FORJA_N3_INTEGRIDADE_VISUAL_E_GESTAO.md`  
**Manifest vigente:** `../FORJA_SPEC_MANIFEST.json`

> Este TDD descreve implementação futura. Nenhum contrato, schema, flag ou estado aqui indicado está ativo até ser criado, testado em sombra e promovido nos termos do roadmap.

---

## 1. Objetivo técnico

Adicionar à arquitetura file-first da FORJA uma camada de raciocínio auditável que:

- decomponha o caso em questões e relações verificáveis;
- prove cobertura de pedidos, alegações e omissões;
- detecte inconsistências globais;
- execute testes jurídicos específicos do caso;
- produza pesquisa acadêmica interdisciplinar quando aplicável;
- classifique correções humanas por causa;
- preserve F0–F10, eventos, hashes, pacote, visual e gestão atuais.

O desenho evita uma plataforma paralela. A N4 será composta por módulos pequenos, artefatos JSON/Markdown, validadores determinísticos e integrações explícitas aos contratos de fase.

---

## 2. Decisões arquiteturais

### D1 — F0–F10 permanece intacto

Não serão criadas fases F11 ou F12. A pesquisa científica será uma via interna `F5C` executada dentro de F5 e condicionada pela classificação de F2.

### D2 — Ledgers atuais são fonte, N4 é relação derivada

Fatos, documentos, proposições e fontes continuam nos ledgers N3. A N4 não copiará seu conteúdo integral; armazenará referências estáveis e relações.

### D3 — Arquivo primeiro

O armazenamento inicial será JSON/Markdown versionado por caso. Banco relacional, vetorial ou de grafos não é dependência da N4.

### D4 — Artefatos candidatos isolados

Enquanto a N4 estiver em sombra, seus arquivos ficarão em:

```text
_FORJA_HARNESS/state/<caseId>/n4_artifacts/
```

O `FORJA_CASE_MANIFEST.json` futuro listará arquivo, tipo, hash, schema, fase, produtor, revisor e status. O código vigente não deve interpretar esses arquivos sem flag.

### D5 — Validação híbrida

- estrutura, IDs, hashes, datas, números, cobertura e invariantes: código determinístico;
- classificação semântica, alcance de fontes, objeções e síntese: execução inteligente;
- conclusão grave ou acusatória: gate humano já previsto na FORJA.

### D6 — Falha explícita

Base acadêmica indisponível, documento ilegível, DOI divergente ou teste sem resposta não vira aprovação. O estado deve ser `degraded`, `blocked`, `partial` ou `not_applicable`, conforme contrato.

### D7 — Sem dependência obrigatória de modelo novo

A N4 usa o roteamento existente. Revisor independente significa nova execução e novo `runId`; não exige outro fornecedor.

---

## 3. Topologia incremental

```text
forja_run.py
  ├─ contratos F0-F10 existentes
  ├─ forja_reasoning.py
  ├─ forja_consistency.py
  ├─ forja_case_tests.py
  ├─ forja_science.py
  ├─ forja_metacognition.py
  ├─ forja_learning.py
  └─ forja_n4_validate.py
```

Os nomes são contratos propostos. A implementação pode distribuí-los em pacote interno, desde que não misture responsabilidades nem quebre os artefatos.

---

## 4. Componentes propostos

## 4.1 `forja_reasoning.py`

Responsabilidades:

- construir e atualizar árvore de questões;
- montar matriz de cobertura;
- derivar grafo jurídico leve;
- calcular completude estrutural sem decidir mérito;
- manter maturidade de teses;
- produzir módulos condicionais de conduta, fatores decisórios e composição.

Não pode:

- alterar `fact_ledger` silenciosamente;
- transformar falta de resposta em `not_applicable` sem justificativa;
- redigir a peça final;
- promover fase.

## 4.2 `forja_consistency.py`

Responsabilidades:

- identidade canônica de eventos e termos;
- comparação estruturada entre documentos;
- verificação intertemporal;
- cenários de quantificação;
- consistência transversal entre peça, pedidos, visuais, relatório e e-mail;
- detecção de alterações de sentido.

Algoritmos determinísticos devem ser usados para números, datas, referências e IDs. Similaridade textual apenas sugere pares para análise semântica.

## 4.3 `forja_case_tests.py`

Responsabilidades:

- versionar testes específicos do caso;
- distinguir teste bloqueante, obrigatório para revisão e informativo;
- executar testes determinísticos;
- registrar avaliação semântica independente;
- impedir relaxamento retroativo do critério;
- invalidar resultados quando a peça ou o teste muda de hash.

## 4.4 `forja_science.py`

Responsabilidades:

- classificar modo LCI;
- gerar protocolo de busca;
- consultar adaptadores bibliográficos;
- deduplicar e verificar identidade das fontes;
- manter fichas de estudos;
- avaliar adequação metodológica por disciplina e proposição;
- sintetizar convergência, divergência e limites;
- mapear evidência científica para afirmações autorizadas;
- auditar citações científicas da peça.

## 4.5 `forja_metacognition.py`

Responsabilidades:

- separar premissa declarada de premissa confirmada;
- detectar consenso derivado da mesma fonte ou resumo;
- registrar mudança de recomendação e sua causa;
- apontar otimização artificial de métricas;
- produzir melhor objeção e alternativa explicativa.

## 4.6 `forja_learning.py`

Responsabilidades:

- consumir o diff humano já existente;
- classificar cada alteração por causa;
- propor teste de regressão para erro estrutural;
- manter proposta de aprendizado separada da regra vigente;
- promover regra somente após aprovação e teste.

## 4.7 `forja_n4_validate.py`

Validador agregador:

- valida schemas;
- verifica IDs, referências e hashes;
- confirma aplicabilidade dos módulos;
- roda gates N4;
- gera `N4_VALIDATION.json`;
- não altera conteúdo para fazê-lo passar.

---

## 5. Estrutura de artefatos por fase

```text
state/<caseId>/
├── FORJA_CASE_MANIFEST.json
├── n4_artifacts/
│   ├── F2_N4_CLASSIFICATION.json
│   ├── F2_QUESTION_TREE.json
│   ├── F3_EVENT_IDENTITY.json
│   ├── F3_DOCUMENT_COMPARISON.json
│   ├── F3_REASONING_GRAPH.json
│   ├── F3_CONDUCT_LEDGER.json
│   ├── F4_COVERAGE_MATRIX.json
│   ├── F4_THESIS_MATURITY.json
│   ├── F4_CASE_ACCEPTANCE_TESTS.json
│   ├── F4_DECISION_FACTOR_MAP.json
│   ├── F4_SETTLEMENT_MAP.json
│   ├── F4_INTERTEMPORAL_MAP.json
│   ├── F4_QUANTIFICATION_SCENARIOS.json
│   ├── F5C_RESEARCH_PROTOCOL.json
│   ├── F5C_STUDY_LEDGER.json
│   ├── F5C_EVIDENCE_SYNTHESIS.json
│   ├── F5C_CLAIM_EVIDENCE_MAP.json
│   ├── F7_CASE_TEST_RESULTS.json
│   ├── F7_GLOBAL_CONSISTENCY.json
│   ├── F7_METACOGNITIVE_AUDIT.json
│   ├── F7_SCIENCE_AUDIT.json
│   ├── F9_DELIVERY_SELECTION.json
│   ├── F10_DELIVERY_INTEGRITY.json
│   ├── F10_HUMAN_DIFF_CLASSIFICATION.json
│   └── N4_VALIDATION.json
└── events/
```

Arquivos condicionais continuam obrigatórios como registro de aplicabilidade. Quando o módulo não se aplicar, o arquivo mínimo conterá `applicability: "not_applicable"` e justificativa; omissão não equivale a não aplicabilidade.

---

## 6. Contrato comum de artefato N4

Todo artefato terá envelope mínimo:

```json
{
  "schemaVersion": 1,
  "specVersion": "N4.0-candidate",
  "caseId": "case-id",
  "artifactType": "question_tree",
  "phase": "F2_CLASSIFICACAO_PRODUTO_RISCO",
  "applicability": "required",
  "status": "draft",
  "sourceHashes": ["sha256-input"],
  "producerRunId": "run-id",
  "reviewerRunId": null,
  "createdAt": "2026-07-10T00:00:00-03:00",
  "updatedAt": "2026-07-10T00:00:00-03:00",
  "contentHash": "sha256",
  "issues": []
}
```

Invariantes:

1. `producerRunId` e `reviewerRunId` não podem ser iguais na aprovação;
2. mudança no conteúdo altera `contentHash` e invalida revisões dependentes;
3. `required` não pode terminar como `not_applicable`;
4. `sourceHashes` devem existir no manifesto do caso;
5. `approved` exige schema válido e gate correspondente.

---

## 7. Schemas funcionais

## 7.1 Árvore de questões

```json
{
  "questions": [
    {
      "questionId": "Q-PROC-001",
      "parentId": null,
      "category": "procedural_event",
      "text": "Qual foi exatamente o resultado processual do acórdão?",
      "origin": "document_comparison",
      "materiality": "decisive",
      "status": "answered",
      "answer": "não conhecimento",
      "supportIds": ["FACT-012", "DOC-004#p18"],
      "dependsOn": [],
      "unansweredConsequence": "block_f6",
      "owner": "F3",
      "reviewStatus": "confirmed"
    }
  ],
  "coverage": {
    "total": 1,
    "material": 1,
    "answeredMaterial": 1,
    "blockedMaterial": 0
  }
}
```

Regras:

- IDs são estáveis;
- pergunta removida vira `retired`, não desaparece;
- resposta depende de `supportIds` quando factual;
- pergunta material sem resposta bloqueia F6 ou exige decisão humana registrada.

Enumeração canônica de `category` (espelha o PRD N4-R01; valores fora dela reprovam o schema):

`fact` | `evidence` | `procedural_event` | `merit` | `precedent` | `calculation` | `request` | `risk` | `opponent_response` | `science` | `visual`

## 7.2 Matriz de cobertura

```json
{
  "items": [
    {
      "coverageId": "COV-001",
      "kind": "opponent_claim",
      "originDocumentId": "DOC-011",
      "originLocator": "p. 7, item 3",
      "statement": "alegação material",
      "supportIds": ["PROP-031"],
      "priorResponseIds": ["DEC-007#p12"],
      "currentTreatment": "rebutted",
      "draftParagraphIds": ["P-042", "P-043"],
      "requestedConsequence": "rejeição",
      "materiality": "decisive",
      "status": "covered"
    }
  ]
}
```

Estados válidos:

- `covered`;
- `partially_covered`;
- `intentionally_excluded`;
- `blocked`;
- `not_applicable`.

`intentionally_excluded` exige razão estratégica, riscos e decisão Helena/Cícero quando material.

## 7.3 Grafo jurídico leve

```json
{
  "nodes": [
    {"id": "FACT-012", "type": "fact", "sourceArtifact": "F3_FACT_LEDGER.json"},
    {"id": "THESIS-002", "type": "thesis", "sourceArtifact": "F4_THESIS_MATURITY.json"}
  ],
  "edges": [
    {
      "edgeId": "E-001",
      "from": "FACT-012",
      "to": "THESIS-002",
      "relation": "supports",
      "scope": "partial",
      "reason": "o fato sustenta apenas a premissa temporal",
      "reviewStatus": "confirmed"
    }
  ]
}
```

Enumeração canônica de `relation` (idêntica ao PRD N4-R03):

`supports` | `contradicts` | `qualifies` | `depends_on` | `responds_to` | `ignored_by` | `distinguishes` | `quantifies` | `limits` | `records` | `justifies` | `tested_by` | `resolves`

Validações:

- nó referenciado deve existir;
- relação deve pertencer à enumeração; "sustenta parcialmente" é `supports` + `scope: partial`, nunca relação nova;
- `supports` e `justifies` não podem omitir `scope` (`full` ou `partial`);
- ciclos são permitidos apenas quando semanticamente justificados; dependência circular bloqueante é sinalizada;
- grafo não substitui o texto dos ledgers-fonte.

## 7.4 Identidade de eventos e termos

```json
{
  "events": [
    {
      "eventId": "EVENT-009",
      "canonicalLabel": "não conhecimento da ação rescisória",
      "sourceId": "DOC-004",
      "locator": "p. 18, dispositivo",
      "allowedParaphrases": ["insucesso da pretensão rescindente por não conhecimento"],
      "forbiddenEquivalents": ["improcedência", "rejeição de mérito"],
      "temporalPosition": 9
    }
  ]
}
```

O validador varre título, corpo, quadros, legendas, pedidos, relatório e e-mail. Ocorrência proibida pode ser aceita apenas se estiver contrastando conceitos e tiver marcação semântica correspondente.

## 7.5 Comparação documental

```json
{
  "comparisonSets": [
    {
      "setId": "CMP-EDCL-001",
      "documents": ["DOC-EMB-1", "DOC-JULG-1", "DOC-EMB-2"],
      "units": [
        {
          "unitId": "CMP-U-001",
          "priorArgument": "texto normalizado",
          "priorResponse": "texto e localizador",
          "currentArgument": "texto normalizado",
          "classification": "repeated_with_no_material_novelty",
          "novelElements": [],
          "prequestioningAssessment": "requires_legal_review",
          "consequence": "triage_only",
          "reviewStatus": "pending"
        }
      ]
    }
  ]
}
```

Classificações possíveis:

- `repeated_with_no_material_novelty`;
- `repeated_with_new_basis`;
- `new_issue_from_prior_decision`;
- `legitimate_clarification`;
- `possible_prequestioning`;
- `not_comparable`;
- `uncertain`.

Nenhuma classificação gera sanção automaticamente.

## 7.6 Maturidade de teses

```json
{
  "theses": [
    {
      "thesisId": "THESIS-002",
      "statement": "tese resumida",
      "role": "primary",
      "documentaryStrength": "strong",
      "legalStrength": "moderate",
      "gaps": ["GAP-003"],
      "bestObjection": "objeção mais forte",
      "contaminationRisk": "low",
      "activationTrigger": "sempre",
      "properVehicle": "contrarrazões",
      "helenaDecision": "adopt",
      "ciceroDecision": "adopt_with_qualification"
    }
  ]
}
```

Não haverá cálculo agregado de “força da tese” que esconda dimensões diferentes.

## 7.7 Testes jurídicos do caso

```json
{
  "suiteId": "CASE-TDD-v1",
  "draftedBeforeFinalText": true,
  "tests": [
    {
      "testId": "CT-CASE-001",
      "question": "Todas as ocorrências do evento usam a classificação processual correta?",
      "severity": "blocking",
      "method": "deterministic_plus_semantic",
      "expected": "zero conflito sem justificativa",
      "evidenceRequired": ["F3_EVENT_IDENTITY.json", "audited_markdown"],
      "immutableFromHash": "sha256",
      "status": "pending"
    }
  ]
}
```

Alteração de teste exige:

- `supersedesTestId`;
- razão;
- autor da decisão;
- hash anterior;
- reexecução completa.

## 7.8 Intertemporalidade

```json
{
  "issues": [
    {
      "issueId": "TEMP-001",
      "legalRegimeQuestion": "regime aplicável",
      "triggeringAct": "ato jurisdicional equivalente",
      "triggeringDate": "2020-01-15",
      "dateSourceId": "DOC-021#p4",
      "transitionRuleSourceId": "SRC-LEGAL-083",
      "conclusion": "regime X",
      "residualUncertainty": null
    }
  ]
}
```

Data inferida não pode ser gravada como comprovada.

## 7.9 Quantificação

```json
{
  "scenarios": [
    {
      "scenarioId": "QUANT-001",
      "question": "qual o proveito econômico mensurável?",
      "formula": "base * percentual",
      "knownInputs": [
        {"name": "base", "value": 1000, "unit": "BRL", "sourceId": "DOC-031#p9"}
      ],
      "disputedInputs": [
        {"name": "percentual", "range": [0.1, 0.2], "basisIds": ["PROP-044"]}
      ],
      "outputs": {"minimum": 100, "maximum": 200, "unit": "BRL"},
      "limitations": ["depende de definição judicial do percentual"],
      "calculationMethod": "deterministic"
    }
  ]
}
```

Valores monetários devem preservar unidade, data-base e regra de arredondamento. Intervalos só existem se as extremidades tiverem base.

## 7.10 Ledger longitudinal de condutas

```json
{
  "conducts": [
    {
      "conductId": "COND-001",
      "pole": "opposing_party",
      "description": "descrição neutra da conduta alegada",
      "date": "2023-05-10",
      "dateSourceId": "DOC-014#p3",
      "verificationStatus": "verified",
      "sourceIds": ["DOC-014#p3"],
      "laterCorrection": null,
      "externalPhrasingAllowed": "frase autorizada para a peça, ou null",
      "ciceroApproval": "required_pending"
    }
  ]
}
```

Regras: `verificationStatus` ∈ `verified | partial | not_verified | contradicted`; conduta `not_verified` ou `contradicted` tem `externalPhrasingAllowed: null` obrigatório; qualquer formulação acusatória exige `ciceroApproval: approved` antes de F6.

## 7.11 Mapa de fatores decisórios

```json
{
  "decisions": [
    {
      "decisionId": "DEC-007",
      "decisionSourceId": "DOC-020",
      "locator": "p. 12-14",
      "factors": [
        {
          "factorId": "DF-001",
          "kind": "explicit_requirement",
          "statement": "o julgador exigiu prova documental da data do ato",
          "evidenceOutcome": "considered_insufficient",
          "openQuestion": null,
          "effectOnNextFiling": "comprovar a data por documento, não por alegação"
        }
      ]
    }
  ]
}
```

Regras: `kind` ∈ `explicit_requirement | evidence_assessment | judicial_caution | open_question`; todo fator cita decisão e localizador; o mapa descreve critérios demonstrados, nunca perfil pessoal do julgador.

## 7.12 Estratégia condicional de composição

```json
{
  "applicability": "required",
  "interests": ["interesse objetivo documentado"],
  "nonNegotiables": ["limite com fonte ou decisão do cliente registrada"],
  "possibleConcessions": [
    {"concession": "descrição", "trigger": "condição de ativação", "proceduralEffect": "efeito processual"}
  ],
  "noAgreementAlternative": "cenário sem acordo, em termos qualitativos",
  "qualitativeZone": "faixa qualitativa de composição possível",
  "prohibitions": ["sem probabilidade numérica", "sem valor sem base", "sem intenção presumida da parte contrária"]
}
```

Regras: nenhum campo aceita número inventado; interesse ou limite sem fonte ou sem decisão humana registrada fica `blocked`; o artefato é interno e nunca transcrito na peça.

## 7.13 Integridade da versão entregue

```json
{
  "packageArtifactId": "ART-PACKAGE-001",
  "selectedArtifactId": "ART-DOCX-004",
  "packageHash": "sha256-package-file",
  "selectedHash": "sha256-package-file",
  "preSendMatch": true,
  "layoutProfileId": "medina-visual-law-v1",
  "postDeliveryVerification": {
    "mode": "artifact_evidence",
    "deliveredHash": null,
    "deliveryEvidenceId": "DELIVERY-019",
    "status": "confirmed"
  }
}
```

Modos pós-entrega:

- `channel_hash`: o canal disponibiliza o anexo e o hash real é comparado;
- `artifact_evidence`: o canal não devolve os bytes; a seleção pré-envio, o `artifactId`, o hash e a evidência externa formam a cadeia de confirmação.

`preSendMatch: false` sempre bloqueia. `deliveredHash: null` não bloqueia quando `mode: artifact_evidence` e a evidência correspondente é válida.

---

## 8. Lastro Científico Interdisciplinar — F5C

## 8.1 Classificação em F2

`F2_N4_CLASSIFICATION.json` terá:

```json
{
  "science": {
    "mode": "rapid",
    "triggerPropositionIds": ["PROP-081"],
    "domains": ["psychology"],
    "justification": "a tese usa proposição não jurídica material",
    "requiredBeforeF6": true
  }
}
```

Regras de decisão:

- `not_applicable`: nenhuma proposição não jurídica material;
- `rapid`: apoio técnico/contextual material, mas não exclusivo;
- `strict`: a conclusão depende substancialmente de afirmação científica contestável ou de alto impacto.

## 8.2 Protocolo de busca

`F5C_RESEARCH_PROTOCOL.json` conterá:

- `researchQuestion`;
- decomposição por população/contexto, exposição/intervenção, comparação, resultado/conceito e desenho, conforme a disciplina;
- sinônimos e conceitos de áreas adjacentes;
- bases e rotas de descoberta;
- consultas literais;
- período e idiomas;
- critérios de inclusão/exclusão;
- estratégia de deduplicação;
- regra de parada;
- método de seleção;
- critérios de avaliação;
- data da busca.

Para `rapid`, a regra de parada pode ser saturação prática documentada. Para `strict`, devem existir rastreio de inclusões/exclusões e, quando apropriado, fluxo compatível com revisão sistemática.

## 8.3 Adaptadores de descoberta

### Crossref

- uso principal: DOI e metadados bibliográficos;
- operações: busca por título, DOI e filtros;
- identidade confirmada por DOI + título + autores/ano;
- resposta indisponível gera `crossref_status: unavailable`, não `not_found`.

### OpenAlex

- uso principal: descoberta ampla, citações e relações entre trabalhos;
- a documentação oficial atual exige chave de acesso, ainda que exista faixa gratuita;
- a N4 não dependerá de plano pago;
- ausência de chave ou limite esgotado aciona busca manual/alternativa e registra degradação.

### NCBI E-utilities / PubMed / PMC

- uso principal: saúde, medicina, psicologia biomédica e áreas afins;
- operações: busca, identificação e recuperação de metadados/resumos ou texto disponível;
- PMID, PMCID e DOI devem ser conciliados quando presentes.

### Rotas adicionais

Adaptadores disciplinares serão opcionais e só entram após teste próprio. Busca manual e encadeamento de referências continuam válidos se registrados.

## 8.4 Pipeline científico

1. formular pergunta científica precisa, com população/contexto e resultado ou conceito adequados à disciplina;
2. escolher áreas e conceitos-ponte;
3. executar consultas registradas;
4. deduplicar por DOI/PMID/título/autoria;
5. confirmar identidade bibliográfica;
6. normalizar o conteúdo como fonte de pesquisa; texto imperativo encontrado no material não altera o fluxo, e o scanner existente apenas registra anomalia técnica real sem bloquear por frase isolada;
7. separar versão publicada, preprint e correções;
8. selecionar por critérios explícitos;
9. ler o nível necessário da fonte;
10. preencher ficha de método, população, resultado e limites;
11. procurar evidência contrária e explicações alternativas;
12. avaliar transferência para a proposição do caso;
13. sintetizar sem exceder os dados;
14. mapear afirmação autorizada;
15. auditar a citação no texto final.

Metadado ou título localizado não sustenta proposição científica. Afirmação decisiva exige leitura do trecho relevante; uso apenas de resumo deve ser explicitado e limita o alcance.

## 8.5 Ledger de estudos

Estrutura central:

```json
{
  "studies": [
    {
      "studyId": "SCI-001",
      "title": "Título",
      "authors": ["Autor A"],
      "year": 2024,
      "identifiers": {"doi": "10.x/x", "pmid": null, "openalex": "W..."},
      "version": "version_of_record",
      "peerReviewStatus": "confirmed",
      "studyDesign": "cohort",
      "discipline": "psychology",
      "population": "descrição",
      "sample": "descrição",
      "method": "descrição",
      "mainFinding": "descrição calibrada",
      "reportedEffect": null,
      "limitations": ["limitação"],
      "funding": "reported",
      "conflicts": "none_reported",
      "publicationStatus": "current",
      "supportsClaimIds": ["SCI-CLAIM-001"],
      "doesNotSupport": ["diagnóstico individual"],
      "transferability": "limited",
      "fullTextStatus": "read_relevant_sections",
      "verification": {
        "identity": "confirmed",
        "content": "confirmed",
        "correctionRetraction": "checked"
      }
    }
  ]
}
```

## 8.6 Avaliação metodológica

A classificação terá duas dimensões separadas:

1. desenho e risco de viés;
2. adequação à proposição e à disciplina.

Campos mínimos:

- pergunta respondida pelo estudo;
- desenho adequado à pergunta;
- representatividade e tamanho da amostra;
- controles e confundidores;
- validade das medidas;
- incerteza estatística, quando aplicável;
- limitações reconhecidas;
- replicação/convergência;
- validade externa;
- capacidade de apoiar associação, mecanismo ou causalidade.

Não será aplicada automaticamente a regra “meta-análise vence tudo”. Revisão ruim não supera estudo primário adequado apenas pelo rótulo.

## 8.7 Mapa afirmação científica → evidência

```json
{
  "claims": [
    {
      "scienceClaimId": "SCI-CLAIM-001",
      "propositionId": "PROP-081",
      "draftText": "A literatura indica associação entre X e Y em populações comparáveis.",
      "epistemicStatus": "supported",
      "useType": "contextual_support",
      "supportingStudyIds": ["SCI-001", "SCI-004"],
      "contraryStudyIds": ["SCI-006"],
      "synthesisStatus": "mixed",
      "transferLimits": ["não comprova o fato individual"],
      "causalLanguageAllowed": false,
      "finalUseAllowed": true
    }
  ]
}
```

## 8.8 Auditoria científica em F7

`F7_SCIENCE_AUDIT.json` verificará:

- identidade e versão da fonte;
- correção, retratação ou expressão de preocupação;
- correspondência entre fonte e frase;
- status de revisão por pares;
- nível de leitura realizado;
- limites de população/contexto;
- associação versus causalidade;
- evidência contrária;
- diferença entre apoio geral e prova individual;
- consistência da referência bibliográfica;
- correspondência com tabelas, gráficos e diagramas.

P0 científicos:

- fonte inexistente ou identidade divergente;
- fonte retratada usada sem finalidade crítica explícita;
- frase incompatível com o resultado;
- conclusão causal não autorizada;
- diagnóstico individual inferido de estudo populacional;
- dado, efeito ou amostra inventados;
- gráfico que altera escala, unidade ou sentido.

---

## 9. Integração aos contratos F0–F10

## F0

- registrar `n4SpecHash` e flags no run;
- não criar artefato N4 para caso sem vínculo inequívoco.

## F1

- garantir índice e cobertura dos documentos necessários;
- preservar versões para comparação;
- identificar ausência de documento essencial à matriz comparativa.

## F2

Novas saídas candidatas:

- `n4_classification`;
- `question_tree`.

Novos gates:

- `n4_modules_classified`;
- `material_questions_initialized`;
- `science_mode_classified`.

## F3

Novas saídas candidatas:

- `event_identity`;
- `document_comparison`;
- `reasoning_graph` inicial;
- `conduct_ledger` quando aplicável.

Novos gates:

- `event_identity_sourced`;
- `comparison_inputs_complete_or_blocked`;
- `reasoning_references_valid`.

A1 continua canônica para jurisprudência falsa, contradição e indícios sancionáveis.

## F4

Novas saídas candidatas:

- `coverage_matrix`;
- `thesis_maturity`;
- `case_acceptance_tests`;
- `decision_factor_map`;
- `settlement_map`;
- `intertemporal_map`;
- `quantification_scenarios`.

Novos gates:

- `material_coverage_complete`;
- `thesis_roles_decided`;
- `case_tests_frozen_before_final_draft`;
- `conditional_modules_resolved`.

Helena e Cícero avaliam as teses; o registro de divergência permanece obrigatório.

## F5

A pesquisa jurídica oficial permanece inalterada. F5C roda em paralelo quando `science.mode != not_applicable`.

Novas saídas candidatas:

- `science_research_protocol`;
- `science_study_ledger`;
- `science_evidence_synthesis`;
- `science_claim_evidence_map`.

Novo gate:

- `science_evidence_ready_or_explicitly_blocked`.

## F6

Entradas adicionais:

- cobertura aprovada;
- testes congelados;
- termos canônicos;
- claims científicos autorizados;
- limites e objeções.

O mapa parágrafo→lastro deve aceitar `scienceClaimId` além de `factId` e `propositionId`.

## F7

Novas saídas:

- resultados dos testes do caso;
- consistência global;
- auditoria metacognitiva;
- auditoria científica.

Novos gates:

- `case_tests_passed`;
- `global_consistency_passed`;
- `metacognitive_audit_completed`;
- `science_audit_passed_or_not_applicable`.

Compatibilidade obrigatória com a base vigente: somente após esses gates e os demais gates F7 alcançarem zero P0, o fluxo executa a subfase editorial F7-B. Ela não substitui testes, consistência, metacognição, auditoria científica nem A1.

## F8

Novas verificações:

- entrada textual canônica igual ao `final_markdown` aprovado e vinculado ao `audited_markdown` pelo bundle F7-B;
- legenda e fonte de gráfico/tabela;
- escalas, unidades e denominadores;
- correspondência entre visual e afirmação;
- ausência de sobreposição e texto acumulado;
- nenhuma extrapolação visual além dos dados.

## F9

O pacote interno inclui artefatos N4 pelo manifesto. A peça protocolável continua limpa. Hash diferente entre auditoria e arquivo bloqueia. Antes de preparar a entrega, F9 grava `F9_DELIVERY_SELECTION.json` com o artefato exato selecionado e seu hash.

## F10

Novas saídas:

- classificação do diff humano;
- integridade da entrega em `F10_DELIVERY_INTEGRITY.json`;
- propostas de teste;
- métricas por módulo;
- sincronização de status N4 no sidecar da gestão.

---

## 10. Eventos N4

Eventos candidatos:

- `n4_module_classified`;
- `question_added`;
- `question_answered`;
- `question_blocked`;
- `coverage_item_resolved`;
- `event_identity_confirmed`;
- `document_comparison_completed`;
- `thesis_maturity_decided`;
- `case_test_frozen`;
- `case_test_executed`;
- `science_protocol_approved`;
- `science_source_verified`;
- `science_synthesis_completed`;
- `global_consistency_failed`;
- `metacognitive_issue_found`;
- `human_diff_classified`;
- `delivery_selection_verified`;
- `delivery_integrity_recorded`;
- `regression_test_proposed`;
- `n4_gate_promoted`;
- `n4_gate_reopened`.

Cada evento deve usar a mesma disciplina N3 de atomicidade, revisão esperada e idempotência.

---

## 11. Máquina de invalidação

| Mudança | Invalida |
|---|---|
| documento-fonte | F3 comparação, identidade, relações, F4, F5C, F6–F9 dependentes |
| fact/proposition ledger | grafo, cobertura, teses, testes e peça dependentes |
| teste do caso | resultados F7 e pacote |
| estudo ou status editorial | síntese, claim map, auditoria científica e parágrafos dependentes |
| Markdown | F7, F8 e pacote |
| DOCX/PDF | F8 e pacote |
| fórmula ou entrada | cenários, gráficos e parágrafos quantitativos |
| decisão Helena/Cícero | tese e blueprint dependentes |

Invalidação não apaga resultado anterior. Marca-o `stale` e registra o evento que a causou.

---

## 12. Consistência global

O validador trabalhará em quatro camadas:

### C1 — Identidade literal

- nomes;
- números CNJ;
- IDs de documentos;
- artigos e precedentes;
- datas;
- valores e unidades;
- nomes de estudos e identificadores.

### C2 — Identidade semântica

- classificação de eventos;
- posição das teses;
- alcance de precedentes;
- associação/causalidade;
- ressalvas e condições.

### C3 — Coerência decisória

- premissas levam à conclusão declarada;
- pedido corresponde à fundamentação;
- subsidiária não contradiz principal sem tratamento;
- quantificação corresponde à fórmula;
- ciência apoia a proposição efetivamente usada.

### C4 — Coerência entre artefatos

- peça;
- quadros/tabelas/diagramas;
- relatório de auditoria;
- relatório de melhorias;
- e-mail de entrega;
- pacote da gestão.

### C5 — Integridade física do documento final (lições da auditoria de 2026-07-10)

- metadados do DOCX/PDF (autor, empresa, última modificação por) conforme o padrão do escritório, verificados APÓS o render final e após TODA regeneração;
- margens, fonte, entrelinhas, recuo e áreas visuais medidos contra o `layoutProfileId` registrado no pacote; o perfil pode ser o Word ordinário ou uma variante visual law aprovada, sem converter diferenças deliberadas em falso P0;
- reconciliação registro de hashes ↔ arquivos em disco: divergência bloqueia e exige reindexação com evento, nunca edição do registro;
- hash do arquivo selecionado para entrega = hash do pacote auditado;
- após a entrega, conferir o hash real quando o canal expuser o anexo; nos demais canais, registrar `artifactId`, hash pré-envio e evidência externa correspondente.

P0 em qualquer camada impede F9. Divergência física comprovada na camada C5 impede também o fechamento em F10; ausência de acesso aos bytes pós-envio não é P0 se a cadeia alternativa de evidência estiver completa.

---

## 13. Auditoria metacognitiva

Estrutura mínima:

```json
{
  "premises": [
    {
      "premiseId": "PREM-001",
      "statement": "premissa",
      "originType": "user_instruction",
      "confirmedBySourceIds": [],
      "status": "declared_not_confirmed",
      "usedInDraft": false
    }
  ],
  "consensusChecks": [
    {
      "issueId": "META-001",
      "agentsAgreeing": 3,
      "independentSourceCount": 1,
      "verdict": "shared_source_not_independent_consensus"
    }
  ],
  "recommendationChanges": [
    {
      "recommendationId": "REC-003",
      "from": "reserve",
      "to": "primary",
      "reasonType": "new_verified_fact",
      "supportIds": ["FACT-099"]
    }
  ]
}
```

O auditor não deve desqualificar instrução do usuário; deve apenas separar objetivo, preferência e fato comprovado.

---

## 14. Integração com a gestão do escritório

O sidecar `gestao_escritorio/data/forja_status.json` poderá receber, por caso/demanda:

```json
{
  "n4": {
    "enabled": true,
    "mode": "shadow",
    "questionCoverage": "18/20",
    "materialBlocks": 2,
    "caseTests": "9/12",
    "scienceMode": "rapid",
    "scienceStatus": "in_review",
    "globalConsistency": "pending",
    "nextAction": "confirmar data do ato processual",
    "artifactIds": ["artifact-id"]
  }
}
```

Regras:

- sidecar continua derivado;
- não reescrever `demandas.json` com conteúdo N4;
- `enabled` não significa concluído;
- percentual não substitui bloqueios materiais;
- link usa `artifactId`, nunca `file:///`;
- `cumprida` continua dependente de F10 e evidência externa.

---

## 15. Feature flags

```json
{
  "n4QuestionTreeV1": false,
  "n4CoverageMatrixV1": false,
  "n4ReasoningGraphV1": false,
  "n4CaseTestsV1": false,
  "n4TerminologyV1": false,
  "n4DocumentComparisonV1": false,
  "n4IntertemporalV1": false,
  "n4QuantificationV1": false,
  "n4ScienceEvidenceV1": false,
  "n4MetacognitiveAuditV1": false,
  "n4ConditionalStrategyV1": false,
  "n4LearningV1": false,
  "n4DeliveryIntegrityV1": false,
  "n4ManagementViewV1": false
}
```

Mapa flag → capacidade do PRD (para auditoria de cobertura das flags):

| Flag | Capacidades PRD |
|---|---|
| `n4QuestionTreeV1` | N4-R01 |
| `n4CoverageMatrixV1` | N4-R02 |
| `n4ReasoningGraphV1` | N4-R03 |
| `n4CaseTestsV1` | N4-R05 |
| `n4TerminologyV1` | N4-R10 |
| `n4DocumentComparisonV1` | N4-R11 |
| `n4IntertemporalV1` | N4-R12 |
| `n4QuantificationV1` | N4-R13 |
| `n4ScienceEvidenceV1` | N4-R14, N4-R15 (parte científica) |
| `n4MetacognitiveAuditV1` | N4-R06 |
| `n4ConditionalStrategyV1` | N4-R04, N4-R07, N4-R08, N4-R09 |
| `n4LearningV1` | N4-R17 |
| `n4DeliveryIntegrityV1` | N4-R16 e Gate N4-10 |
| `n4ManagementViewV1` | visão N4 no sidecar/painel |

N4-R16 (consistência global) e N4-R18 (evidência da execução) não têm flag própria: ativam-se automaticamente conforme os módulos ligados, porque só verificam artefatos que existirem.

Dependências:

- cobertura depende da árvore de questões e ledgers N3;
- grafo depende de IDs canônicos;
- testes dependem de cobertura e identidade de eventos;
- ciência depende de classificação e protocolo;
- consistência global depende dos módulos ativados;
- integridade da entrega depende de pacote F9 atual, F7/F8 válidos e evidência F10;
- gestão depende do validador N4 e do sidecar N3;
- nenhum módulo promove F9 ou F10 sozinho.

---

## 16. Modos de execução

### `off`

Nenhum artefato N4 é exigido. O comportamento anterior permanece.

### `shadow`

Artefatos N4 são produzidos e avaliados, mas não bloqueiam o fluxo vigente. Divergências são relatadas.

### `pilot_blocking`

Gates selecionados bloqueiam apenas casos-piloto explicitamente marcados.

### `default_on`

Disponível somente após promoção normativa. Módulos condicionais continuam classificados por caso.

---

## 17. Tratamento de falhas

| Falha | Estado | Conduta |
|---|---|---|
| documento necessário ausente | `blocked` | listar documento e questão afetada |
| OCR duvidoso | `partial` | exigir leitura visual ou fonte alternativa |
| DOI não resolve | `unverified_identity` | buscar por título/autoria; não citar até confirmar |
| base científica indisponível | `degraded` | registrar e usar rota alternativa; não declarar ausência |
| full text inacessível | `abstract_only` | limitar uso ou bloquear claim decisivo |
| estudo corrigido/retratado | `editorial_update_found` | reavaliar síntese e invalidar dependências |
| termo processual conflitante | `p0` | voltar a F3/F4 |
| fórmula sem entrada | `blocked` | declarar variável faltante |
| teste contraditório | `test_design_review` | revisar teste com nova versão, sem aprovar a peça |
| revisor com mesmo runId | `invalid_review` | nova revisão independente |
| sidecar indisponível | `sync_pending` | manter estado canônico e repetir depois |
| texto imperativo dentro de fonte externa | `source_text_ignored` | manter como conteúdo da fonte; não executar e não bloquear por frase isolada |
| registro de hashes divergente do disco | `registry_resync` | bloquear o pacote dependente, reconciliar com evento e revalidar |
| metadados ou layout fora do perfil selecionado | `p0` | regerar o arquivo e repetir a verificação C5 |

---

## 18. Testes de regressão obrigatórios

### Estrutura e rastreabilidade

| ID | Cenário | Resultado esperado |
|---|---|---|
| N4-S-01 | questão material sem resposta | bloquear prontidão |
| N4-S-02 | pergunta removida entre versões | manter histórico como `retired` |
| N4-S-03 | edge aponta para fato inexistente | reprovar grafo |
| N4-S-04 | pedido material sem parágrafo correspondente | reprovar cobertura |
| N4-S-05 | fato decisivo usa localizador genérico | reprovar uso como comprovado |

### Coerência e comparação

| ID | Cenário | Resultado esperado |
|---|---|---|
| N4-C-01 | “não conhecimento” vira “improcedência” | P0 terminológico |
| N4-C-02 | mesmo evento com datas incompatíveis | P0 temporal |
| N4-C-03 | segundos embargos repetem texto, mas trazem questão nova | classificar novidade; não concluir protelação automática |
| N4-C-04 | similaridade alta com legítimo prequestionamento | exigir revisão jurídica |
| N4-C-05 | pedido final contradiz tese principal | P0 global |
| N4-C-06 | ressalva desaparece do quadro visual | P0 de fidelidade |
| N4-C-07 | DOCX final com autor pessoal ou layout divergente do `layoutProfileId` escolhido | P0 na camada C5; regerar e reverificar |
| N4-C-08 | arquivo selecionado para entrega difere por hash do pacote auditado | bloquear o fechamento (Gate N4-10) |

### Testes do caso

| ID | Cenário | Resultado esperado |
|---|---|---|
| N4-T-01 | mudar teste após falha | invalidar resultados e exigir versão |
| N4-T-02 | produtor aprova próprio teste sem nova execução | rejeitar |
| N4-T-03 | hash da peça muda | invalidar resultados F7 |
| N4-T-04 | teste sem evidência exigida | falhar |

### Ciência

| ID | Cenário | Resultado esperado |
|---|---|---|
| N4-SCI-01 | DOI existe, mas título é de outro artigo | rejeitar identidade |
| N4-SCI-02 | estudo retratado usado como apoio | P0 |
| N4-SCI-03 | estudo observacional descrito como causal | P0 sem justificativa metodológica |
| N4-SCI-04 | população incompatível com o caso | marcar transferência limitada ou bloquear |
| N4-SCI-05 | apenas metadado disponível | impedir uso substantivo |
| N4-SCI-06 | evidência contrária ignorada | reprovar síntese |
| N4-SCI-07 | revisão sistemática fraca supera estudo adequado só pelo rótulo | reprovar avaliação |
| N4-SCI-08 | gráfico troca unidade ou denominador | P0 visual/científico |
| N4-SCI-09 | artigo não localizado após uma base | registrar diligência, não inexistência |
| N4-SCI-10 | claim populacional usado como diagnóstico individual | P0 |
| N4-SCI-11 | artigo sobre prompt injection contém a frase “ignore as regras” como objeto de estudo | ignorar como comando e avaliar a fonte normalmente; zero falso bloqueio |

### Metacognição e aprendizado

| ID | Cenário | Resultado esperado |
|---|---|---|
| N4-M-01 | três agentes repetem uma única fonte | não tratar como consenso independente |
| N4-M-02 | premissa de e-mail não confirmada | manter como declaração |
| N4-M-03 | preferência de estilo isolada | não criar gate global |
| N4-M-04 | erro factual recorrente com fixture | propor teste e exigir aprovação |
| N4-M-05 | métrica melhora removendo perguntas difíceis | detectar gaming |

### Gestão e rollback

| ID | Cenário | Resultado esperado |
|---|---|---|
| N4-G-01 | flag N4 desligada | N3/N2 continua sem perda |
| N4-G-02 | caso histórico em replay | nenhuma peça original alterada |
| N4-G-03 | sidecar mostra 100%, mas há P0 | painel destaca bloqueio, não prontidão |
| N4-G-04 | artefato com acento/espaço | abrir por `artifactId` |
| N4-G-05 | N4 em sombra falha | fluxo vigente segue e divergência é registrada |
| N4-G-06 | registro de hashes diverge do arquivo em disco | bloquear expedição e exigir reconciliação com evento |

---

## 19. Corpus de avaliação

O corpus N4 deve conter cópias imutáveis de casos que exercitem capacidades distintas:

- peça responsiva com alegação de repetição ou contradição;
- caso com confusão entre resultado processual e mérito;
- caso com questão intertemporal;
- caso contábil/econômico com quantificação;
- caso de saúde ou psicologia com LCI;
- peça longa com risco de perda de contexto;
- peça com diagramas e tabelas complexas;
- casos negativos construídos com fonte semelhante, mas inadequada.

Cada fixture terá resultado esperado e justificativa. O objetivo é testar o gate, não reescrever a peça histórica.

---

## 20. Telemetria

`FORJA_RUN_METRICS.json` será estendido com:

- versão e flags N4;
- perguntas totais, materiais, respondidas e bloqueadas;
- itens de cobertura por estado;
- nós e relações inválidas;
- conflitos terminológicos e temporais;
- testes do caso por severidade;
- modo LCI;
- consultas, bases, fontes encontradas, incluídas e excluídas;
- fontes com identidade, conteúdo e estado editorial confirmados;
- síntese convergente, mista, fraca, ausente ou não transferível;
- mudanças de recomendação por causa;
- correções humanas por categoria;
- duração e custo apenas quando realmente medidos.

Telemetria não deve armazenar apenas porcentagem agregada. Contagens e IDs dos bloqueios devem permanecer recuperáveis.

---

## 21. Requisitos não funcionais

### Determinismo

- hashes reproduzíveis;
- JSON estável;
- enums validados;
- cálculos repetíveis;
- datas com fuso e fonte.

### Idempotência

Reexecução com mesma entrada e versão não duplica perguntas, estudos, eventos ou sidecar.

### Retomada

Falha de base, Word, rede ou agente permite retomar do último artefato válido.

### Auditabilidade

Toda promoção registra produtor, revisor, entrada, saída, decisão e hash.

### Compatibilidade

Flags desligadas preservam o comportamento existente. Leitores antigos ignoram `n4_artifacts/`.

### Desempenho

Módulos condicionais não executam quando `not_applicable`. Pesquisa LCI respeita regra de parada e cache bibliográfico.

---

## 22. Rollback

1. desligar flags N4;
2. impedir leitura de `n4_artifacts/` pelo runner;
3. manter os arquivos para auditoria;
4. recalcular sidecar sem bloco N4;
5. retomar fluxo N3/N2 pela versão registrada;
6. não apagar eventos nem reinterpretar estados passados.

Rollback não pode marcar automaticamente caso como pronto. Deve apenas restaurar o contrato anterior.

---

## 23. Ordem técnica recomendada

1. comprovar baseline N3 real;
2. criar schemas e fixtures N4;
3. implementar árvore, cobertura e testes do caso;
4. implementar identidade terminológica e consistência global;
5. implementar grafo e maturidade de teses;
6. implementar comparação, temporalidade e quantificação;
7. implementar F5C científico em sombra;
8. implementar metacognição e aprendizado;
9. integrar gestão;
10. executar replays e pilotos bloqueantes;
11. promover apenas o conjunto estável.

Essa ordem entrega primeiro os controles que capturam erros observados e deixa módulos condicionais mais complexos para depois da base comprovada.

---

## 24. Dependências de referência

### Internas

- `FORJA_SPEC_MANIFEST.json`;
- `forja_state_machine.py`;
- `forja_run.py`;
- `forja_context.py`;
- `forja_adversarial_audit.py`;
- `forja_package.py`;
- `forja_close_cycle.py`;
- `forja_run_metrics.py`;
- contratos F0–F10;
- kit visual Medina e Word COM;
- sidecar da gestão.

### Acadêmicas e bibliográficas

- OpenAlex Developers: `https://developers.openalex.org/`;
- Crossref REST API: `https://www.crossref.org/documentation/retrieve-metadata/rest-api/`;
- Crossmark e atualizações: `https://www.crossref.org/services/crossmark/`;
- NCBI APIs/E-utilities: `https://www.ncbi.nlm.nih.gov/home/develop/api/`;
- PRISMA 2020: `https://www.prisma-statement.org/prisma-2020`;
- Academic Research Suite local, usada como referência metodológica, sem substituir os contratos FORJA.

---

## 25. Critério técnico de pronto

A implementação N4 estará pronta para promoção somente quando:

1. todos os schemas e contratos forem versionados;
2. a bateria N4 passar sobre fixtures e artefatos reais;
3. pelo menos um caso de cada classe crítica passar em sombra;
4. pilotos bloqueantes detectarem os defeitos esperados sem regressão indevida;
5. F7/F8/F9 preservarem hashes e sentido;
6. sidecar e painel mostrarem o estado correto;
7. rollback for comprovado;
8. N4 produzir ganho verificável de cobertura e detecção, não apenas mais arquivos;
9. manifest e documentos normativos forem atualizados juntos na promoção.

### Estado implementado em 11/07/2026

O contrato foi comprovado retrospectivamente em CASO-19/Fábio, CASO-16 e Saúde. Cada caso materializou 24/24 artefatos, executou 10 testes ligados ao hash do texto final, matou 10/10 mutações literais, passou pelas cinco camadas reproduzidas e recebeu QA visual automática por página. Isso valida regressão mecânica e estrutura, não aprovação jurídica nem ciclo prospectivo: cada caso possui dois P1 de conselho, `executionMode=retrospective_baseline` e `promotionEligible=false`.

### Adendo técnico anti-autocertificação - 11/07/2026

1. `suiteHash` inclui modo temporal, declaração de anterioridade, datas e justificativa retrospectiva.
2. Datas prospectivas são interpretadas como ISO 8601 com fuso; comparação textual não é aceita.
3. O agregador resolve o texto canônico no registro de fontes, reexecuta F7 e mutações e compara o resultado salvo.
4. `mutationScore`, `killed`, `total` e a lista de mutações obedecem invariantes matemáticos.
5. C1-C5 são reexecutadas sobre caminhos, hashes, fidelidade, questões, F7 e imagens de todas as páginas.
6. `expected_count=0` produz `not_evaluated`, nunca aprovação.
7. Artefato aplicável em `draft`, `pending_review`, `blocked` ou `stale` impede aprovação.
8. A promoção exige mutação literal e semântica >= 80%, além de decisões Helena/Cícero com parecer e localizador.
9. O QA visual atual é automático; seus registros carregam `reviewType=automated` e `humanReviewed=false`.
10. Falha de sincronização N4 deixa a integridade da gestão como `stale`, sem interromper o fluxo N2/N3 em sombra.

O registro de fontes foi ampliado de hash simples para `{path, sha256, status, reason, originPath}` sem quebrar o formato anterior. Fontes `revoked`, `stale`, ausentes, alteradas ou com declaração explícita de invalidação na origem geram P0. Essa regra detectou e retirou a falsa aprovação do piloto CASO-04.

O modo operacional permanece `pilot_blocking` com lista explícita. A promoção para `default_on` exige `executionMode=prospective`, `frozenAt < finalProducedAt`, mutation score mínimo de 80% e camadas C1–C5 com evidência medida.

---

## 26. Estado técnico implementado em 11/07/2026
1. Os 24 contratos de artefato foram gerados em `n4_schemas/` e são aplicados pelo validador agregado, além das regras semânticas específicas.
2. Os contratos candidatos F0-F10 estão em `phase_contracts_n4/`, anexados sem substituir os contratos N3.
3. O runner promove artefatos N4 validados, arquiva versões anteriores e registra `N4_EXECUTION_TRACE.jsonl`.
4. O validador diferencia `complete`, `approved` e `blocksCurrentFlow`; ausência em sombra não bloqueia nem aparece como aprovação.
5. `pilot_blocking` só vale para casos listados e apenas para os grupos promovidos no roadmap; módulos estratégicos continuam consultivos.
6. A integridade F9/F10 foi testada de ponta a ponta com bytes do pacote, hash pré-envio e evidência externa.
7. O painel abre artefatos N4 somente pelo catálogo e confere o hash atual antes de abrir.
8. A desativação permanece disponível por flags e modo, sem apagar eventos ou artefatos.

Evidência consolidada: `../reports/IMPLEMENTACAO_FORJA_N4_2026-07-11.md`.

---

## 27. Perfil técnico PSO-Pet 1.0

Referência normativa complementar: `14_METODO_VAN_AKEN_APLICADO_A_PETICOES.md`.

### 27.1 Decisão técnica

O perfil reutiliza os artefatos N4 existentes. Não cria banco, nova fase ou validador obrigatório nesta etapa. O roteiro `../templates/F4_METODO_SOLUCAO_PROBLEMA_PETICAO.md` funciona como índice humano entre:

- `F2_QUESTION_TREE.json` — definição do problema e perguntas;
- `F3_EVENT_IDENTITY.json` e `F3_REASONING_GRAPH.json` — modelo e diagnóstico;
- `F4_COVERAGE_MATRIX.json`, `F4_THESIS_MATURITY.json` e blueprint — requisitos, alternativas e arquitetura;
- `F4_CASE_ACCEPTANCE_TESTS.json` — requisitos convertidos em testes;
- `F7_CASE_TEST_RESULTS.json` e `F7_GLOBAL_CONSISTENCY.json` — validação;
- `F9_DELIVERY_SELECTION.json` e `F10_DELIVERY_INTEGRITY.json` — intervenção executada;
- `F10_HUMAN_DIFF_CLASSIFICATION.json` e retrospectiva — avaliação e aprendizado.

### 27.2 Iterações permitidas

Uma descoberta posterior pode reabrir F2, F3 ou F4. A reabertura deve registrar artefato afetado, evidência nova, decisão anterior, nova decisão e hashes invalidados. Não é permitido corrigir silenciosamente a definição do problema depois da redação.

### 27.3 Aplicabilidade

- `light`: núcleo mínimo para questão simples;
- `full`: ciclo completo para recurso, resposta ou múltiplas teses;
- `intensive`: ciclo completo, comparação documental, cenários e CIMO-Pet.

O classificador pode recomendar o perfil, mas a extensão permanece `shadow` até cumprir o marco de validação prospectiva do roadmap.

### 27.4 Futuro gate determinístico

Somente após validação prospectiva poderá ser criado schema específico. O gate futuro deve verificar presença, ordem temporal, referências aos artefatos canônicos e decisões do conselho. Não deve avaliar mérito por contagem de campos nem exigir alternativas artificiais.

---

## 28. Adendo técnico de compatibilidade — F7-B/Fable 5 (15/07/2026)

Este desenho N4 continua não vigente, mas deve compor com a implementação posterior da base sem regressão.

### 28.1 Fronteira de execução

`forja_run.py` cria e promove tentativas, mas não invoca Fable 5 automaticamente. Dentro de uma tentativa `F7_AUDITORIA_JURIDICA_FACTUAL` com `RUN_CONTEXT.json`, `audited_markdown` e `f7_gate_result` sem P0, o operador chama `forja_fable5.py`. O executor valida pertencimento ao caso/fase e confina todos os caminhos ao diretório da tentativa.

### 28.2 Contrato e composição do resultado

O executor produz:

- `final_markdown[<suffix>].md` — texto canônico;
- `editorial_report[<suffix>].json` — hashes e relatório do editor;
- `editorial_diff[<suffix>].patch` — comparação com a origem;
- `fable5_usage[<suffix>].json` — sessão, modelo, OAuth, hashes e uso observado;
- `editorial_fidelity[<suffix>].json` — resultado determinístico;
- `FABLE5_RESULT[<suffix>].json` — fragmento de gates/artefatos.

O `FABLE5_RESULT` deve ser incorporado ao `PHASE_RESULT` completo da tentativa F7. Ele não contém as demais saídas jurídicas obrigatórias e, isoladamente, não satisfaz o contrato nem autoriza promoção. Múltiplos textos são pareados por sufixo seguro comum, nunca por posição em lista.

### 28.3 Autenticação e limites

O comando usa o alias `fable`, mas o envelope precisa provar `claude-fable-5`. Antes da chamada, `claude auth status` deve indicar `loggedIn=true`, `authMethod=claude.ai` e `subscriptionType=max`. Não há chave ou faturamento de API.

O prompt permite apenas clareza, ritmo, vocabulário, encadeamento e concisão. Permanecem semanticamente imutáveis fatos, datas, números, valores, citações, dispositivos, precedentes, marcadores processuais, ressalvas, capítulos, estratégia, prequestionamento, pedidos, fecho e assinaturas. Mudança material desejável vai para `duvidas`, não para o texto.

### 28.4 Gates e repetição

`forja_editorial_fidelity.py` recompõe `fable5_oauth_confirmed`, `editorial_source_hash_match`, `editorial_fidelity_pass` e `human_style_final_pass`. As comparações incluem hashes reais, números, marcadores, autoridades, aspas, marcadores de auditoria, títulos, retenção mínima de 90% do conteúdo não branco, pedidos/fecho, origem operacional e P0 de estilo. O relatório do modelo é evidência auxiliar, não autocertificação.

Há no máximo três candidatas editoriais internas por execução, cada uma refeita do `audited_markdown` original com os achados da candidata rejeitada. Isso é ortogonal ao `retryPolicy.maxAttempts=4` da fase F7: quatro diretórios/tentativas externas continuam sendo o limite do orquestrador. Só a candidata integralmente aprovada vira `final_markdown` de F8/F9.
