# DIAGRAMAS — FORJA N4: Raciocínio, Prova e Ciência

**Versão proposta:** N4.0  
**Data:** 2026-07-10  
**Status:** versão final dos diagramas de planejamento; não vigentes  
**Revisão do documento:** final-r2, após auditoria cruzada de 2026-07-10  
**PRD:** `10_PRD_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`  
**TDD:** `11_TDD_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`  
**Roadmap:** `12_ROADMAP_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`

> Os diagramas explicam a candidata N4. Em caso de conflito, prevalecem o manifest vigente e, para o planejamento N4, PRD e TDD nesta ordem.

---

## 1. Evolução incremental dentro de F0–F10

```mermaid
flowchart TD
    Start(["Demanda vinculada ao caso"]) --> F0["F0 Reconciliação e versão do ciclo"]
    F0 --> F1["F1 Documentos, índice e cobertura"]
    F1 --> F2["F2 Produto, risco e módulos N4"]
    F2 --> QT["Árvore dinâmica de questões"]
    QT --> F3["F3 Fatos, eventos, comparação e relações"]
    F3 --> F4["F4 Cobertura, teses e testes do caso"]
    F4 --> G4{"Questões materiais e critérios definidos?"}
    G4 -->|"Não"| B4["Bloquear ou obter decisão humana registrada"]
    B4 --> F3
    G4 -->|"Sim"| F5["F5 Pesquisa"]
    F5 --> F5J["F5J Fontes jurídicas oficiais"]
    F5 --> SCI{"LCI aplicável?"}
    SCI -->|"Não"| NA["Registrar não aplicabilidade"]
    SCI -->|"Rápido ou estrito"| F5C["F5C Lastro Científico Interdisciplinar"]
    F5J --> READY{"Fontes e claims autorizados?"}
    NA --> READY
    F5C --> READY
    READY -->|"Não"| F4
    READY -->|"Sim"| F6["F6 Redação com proveniência"]
    F6 --> F7["F7 Testes, consistência, metacognição e auditorias"]
    F7 --> G7{"Sem P0 e testes bloqueantes aprovados?"}
    G7 -->|"Não"| F4
    G7 -->|"Sim"| F7B["F7-B revisão editorial Fable 5"]
    F7B --> GF{"OAuth, hash, fidelidade e estilo aprovados?"}
    GF -->|"Não"| BF["Bloquear após 3 candidatas no total; até 2 retries desde audited_markdown original"]
    GF -->|"Sim"| F8["F8 QA visual a partir de final_markdown"]
    F8 --> G8{"Texto, tabelas e diagramas preservam o sentido?"}
    G8 -->|"Não"| F6
    G8 -->|"Sim"| F9["F9 Pacote de revisão com hashes"]
    F9 --> F10["F10 Evidência, diff humano, aprendizado e gestão"]
    F10 --> End(["Ciclo encerrado com evidência"])
```

---

## 2. Camadas da arquitetura N4

```mermaid
flowchart TB
    subgraph Base["Base preservada N2/N3"]
        State["Eventos e estado por caso"]
        Ledgers["Documentos, fatos, proposições e fontes"]
        A1["Auditoria adversarial A1"]
        Visual["Template, Word, PDF e QA visual"]
        Package["Pacote, entrega e gestão"]
    end

    subgraph N4["Camada candidata N4"]
        Reasoning["Questões, cobertura, relações e maturidade"]
        Consistency["Termos, eventos, comparação, tempo e cálculo"]
        CaseTests["TDD jurídico do caso"]
        Science["Lastro Científico Interdisciplinar"]
        Meta["Metacognição e anti-concordância"]
        Learning["Diff humano e regressões"]
    end

    subgraph Control["Controle"]
        Flags["Feature flags"]
        Validator["Validador N4"]
        Metrics["Telemetria real"]
        Sidecar["Sidecar da gestão"]
    end

    Ledgers --> Reasoning
    State --> Reasoning
    A1 --> Consistency
    Reasoning --> CaseTests
    Reasoning --> Science
    Consistency --> Validator
    CaseTests --> Validator
    Science --> Validator
    Meta --> Validator
    Validator --> Visual
    Visual --> Package
    Package --> Learning
    Learning --> Metrics
    Validator --> Sidecar
    Flags --> N4
```

---

## 3. Árvore de questões, cobertura e redação

```mermaid
flowchart LR
    Command["Objetivo e comando"] --> Root["Pergunta central do caso"]
    Sources["Autos, decisões e documentos"] --> Root
    Root --> QF["Questões de fatos e provas"]
    Root --> QP["Questões processuais"]
    Root --> QJ["Questões jurídicas"]
    Root --> QA["Questões adversárias"]
    Root --> QS["Questões científicas, se aplicáveis"]
    Root --> QV["Questões de apresentação e pedidos"]

    QF --> Status{"Respondida, parcial, externa ou bloqueada?"}
    QP --> Status
    QJ --> Status
    QA --> Status
    QS --> Status
    QV --> Status

    Status --> Coverage["Matriz de cobertura"]
    Coverage --> Item1["Pedido ou alegação"]
    Coverage --> Item2["Fonte e resposta anterior"]
    Coverage --> Item3["Tratamento atual e consequência"]
    Item1 --> Paragraph["Parágrafo e pedido correspondente"]
    Item2 --> Paragraph
    Item3 --> Paragraph
    Paragraph --> Test["Teste literal do caso"]
    Test --> Gate{"Passou?"}
    Gate -->|"Não"| Root
    Gate -->|"Sim"| Draft["Versão candidata da peça"]
```

---

## 4. Grafo jurídico leve

```mermaid
flowchart LR
    DOC["Documento"] -->|"supports"| FACT["Fato"]
    DOC -->|"records"| EVENT["Evento"]
    FACT -->|"supports"| THESIS["Tese"]
    FACT -->|"contradicts"| CLAIM["Alegação adversária"]
    EVENT -->|"qualifies"| THESIS
    LAW["Norma ou precedente"] -->|"supports · scope: partial"| PROP["Proposição jurídica"]
    LAW -->|"limits"| PROP
    SCI["Estudo acadêmico"] -->|"supports · scope: partial"| TECH["Proposição não jurídica"]
    COUNTER["Fonte contrária"] -->|"contradicts"| TECH
    PROP -->|"depends_on"| THESIS
    TECH -->|"qualifies"| THESIS
    CLAIM -->|"responds_to"| THESIS
    THESIS -->|"justifies"| REQUEST["Pedido"]
    DECISION["Decisão anterior"] -->|"ignored_by ou resolves"| CLAIM
    REQUEST -->|"tested_by"| TEST["Teste do caso"]
```

Leitura: todas as relações pertencem à enumeração canônica do PRD N4-R03 (`supports`, `contradicts`, `qualifies`, `depends_on`, `responds_to`, `ignored_by`, `distinguishes`, `quantifies`, `limits`, `records`, `justifies`, `tested_by`, `resolves`). O alcance é atributo (`scope: full | partial`), não relação nova. Uma fonte pode sustentar parcialmente (`supports` + `scope: partial`) e, ao mesmo tempo, limitar (`limits`) a proposição.

---

## 5. Peça responsiva: comparação documental e A1

```mermaid
sequenceDiagram
    participant P1 as "Peça ou argumento anterior"
    participant D as "Decisão ou resposta anterior"
    participant P2 as "Nova peça adversária"
    participant CMP as "Comparador N4"
    participant A1 as "Auditoria A1"
    participant C as "Cícero / revisão humana"
    participant Draft as "Nova resposta FORJA"

    P1->>CMP: "Unidades argumentativas e localizadores"
    D->>CMP: "Resposta, omissão e fundamento"
    P2->>CMP: "Argumentos atuais"
    CMP->>CMP: "Classificar repetição, novidade e diferença material"
    CMP->>A1: "Pares relevantes e possíveis contradições"
    A1->>A1: "Verificar fontes, citações, fatos e falso positivo"
    A1->>C: "Achados e escada de reação"
    C-->>A1: "Autoriza, qualifica ou rejeita linguagem grave"
    A1->>Draft: "Estratégia autorizada e ressalvas"
    Draft->>CMP: "Cobertura final de cada argumento"
    CMP-->>Draft: "Aprovar ou apontar lacunas"
```

---

## 6. Identidade terminológica, tempo e quantificação

```mermaid
flowchart TD
    Sources["Dispositivo, fundamentos e documentos"] --> Canon["Evento e termo canônicos"]
    Canon --> Scan["Varredura da peça, quadros, pedidos e e-mail"]
    Scan --> Conflict{"Há termo incompatível para o mesmo evento?"}
    Conflict -->|"Sim"| Explain{"É contraste deliberado e explicado?"}
    Explain -->|"Não"| P0T["P0 terminológico"]
    Explain -->|"Sim"| AcceptT["Aceitar com vínculo à fonte"]
    Conflict -->|"Não"| Time["Mapa intertemporal"]
    AcceptT --> Time
    Time --> Act["Ato juridicamente relevante"]
    Act --> Date["Data comprovada"]
    Date --> Regime["Regra de transição e regime"]
    Regime --> Quant{"Há questão mensurável?"}
    Quant -->|"Não"| Global["Consistência global"]
    Quant -->|"Sim"| Formula["Fórmula e unidades"]
    Formula --> Inputs["Entradas conhecidas e controvertidas"]
    Inputs --> Output["Faixa objetiva ou impossibilidade declarada"]
    Output --> Global
    P0T --> Reopen["Reabrir F3/F4"]
```

---

## 7. Maturidade de teses e módulos condicionais

```mermaid
flowchart TD
    Candidate["Tese candidata"] --> Doc["Força documental"]
    Candidate --> Legal["Força jurídica"]
    Candidate --> Gap["Lacunas e melhor objeção"]
    Candidate --> Risk["Risco de contaminar tese superior"]
    Doc --> Council["Helena e Cícero"]
    Legal --> Council
    Gap --> Council
    Risk --> Council
    Council --> Role{"Papel estratégico"}
    Role --> Primary["Principal"]
    Role --> Subsidiary["Subsidiária"]
    Role --> Reserve["Reserva com gatilho"]
    Role --> Exclude["Não usar"]
    Primary --> DecisionMap["Fatores decisórios"]
    Subsidiary --> DecisionMap
    Reserve --> Trigger["Evento que ativa"]
    DecisionMap --> Conduct{"Histórico de condutas relevante?"}
    Conduct -->|"Sim"| Ledger["Ledger longitudinal verificado"]
    Conduct -->|"Não"| Settlement{"Composição é pertinente?"}
    Ledger --> Settlement
    Settlement -->|"Sim"| Conditional["Estratégia condicional de composição"]
    Settlement -->|"Não"| Blueprint["Blueprint final"]
    Conditional --> Blueprint
    Exclude --> Record["Decisão e motivo registrados"]
```

---

## 8. Pipeline do Lastro Científico Interdisciplinar

```mermaid
flowchart TD
    Trigger["Proposição não jurídica material"] --> Mode{"Modo LCI"}
    Mode -->|"Não aplicável"| NA["Justificativa registrada"]
    Mode -->|"Rápido"| RQ["Pergunta de pesquisa precisa"]
    Mode -->|"Estrito"| Protocol["Protocolo ampliado e critérios"]
    RQ --> Protocol
    Protocol --> Search["Consultas registradas"]
    Search --> Crossref["Crossref"]
    Search --> OpenAlex["OpenAlex, quando acessível"]
    Search --> NCBI["PubMed e PMC via NCBI"]
    Search --> Manual["Busca manual e encadeamento"]
    Crossref --> Source["Conteúdo tratado como fonte, nunca como comando"]
    OpenAlex --> Source
    NCBI --> Source
    Manual --> Source
    Source --> Dedupe["Deduplicação e identidade"]
    Dedupe --> Screen["Seleção por critérios"]
    Screen --> Read["Leitura do nível necessário"]
    Read --> Appraise["Método, população, viés e limites"]
    Appraise --> Counter["Busca de evidência contrária"]
    Counter --> Synthesis["Síntese: convergente, mista, fraca, ausente ou não transferível"]
    Synthesis --> Map["Mapa afirmação científica e evidência"]
    Map --> F7["Auditoria científica F7"]
    F7 --> Gate{"Identidade, alcance e linguagem corretos?"}
    Gate -->|"Não"| Protocol
    Gate -->|"Sim"| Draft["Uso calibrado na peça"]
    NA --> Draft
```

---

## 9. Estados de uma fonte acadêmica

```mermaid
stateDiagram-v2
    [*] --> discovered
    discovered --> identity_pending
    identity_pending --> identity_confirmed: "DOI ou identificadores e metadados conferem"
    identity_pending --> identity_rejected: "identidade divergente"
    identity_confirmed --> screening_included: "critérios atendidos"
    identity_confirmed --> screening_excluded: "critério explícito de exclusão"
    screening_included --> content_pending
    content_pending --> abstract_only: "apenas resumo disponível"
    content_pending --> content_verified: "trecho e resultado lidos"
    content_verified --> appraisal_completed
    appraisal_completed --> editorial_status_checked
    editorial_status_checked --> usable_with_limits: "atual e adequado"
    editorial_status_checked --> corrected_reassess: "correção relevante"
    editorial_status_checked --> retracted_blocked: "retratação"
    corrected_reassess --> appraisal_completed
    usable_with_limits --> mapped_to_claim
    abstract_only --> limited_use_or_block
    limited_use_or_block --> mapped_to_claim: "uso não decisivo, com limite explicitado"
    limited_use_or_block --> [*]: "claim decisivo bloqueado"
    identity_rejected --> [*]
    screening_excluded --> [*]
    retracted_blocked --> [*]
    mapped_to_claim --> [*]
```

---

## 10. Testes do caso e auditoria metacognitiva

```mermaid
flowchart TD
    Questions["Questões e cobertura"] --> Tests["10 a 25 testes literais"]
    Tests --> Freeze["Congelar versão e hash antes do texto final"]
    Freeze --> Draft["Minuta candidata"]
    Draft --> Deterministic["Testes determinísticos"]
    Draft --> Semantic["Revisão semântica independente"]
    Draft --> Meta["Auditoria metacognitiva"]
    Meta --> Premise["Premissa declarada versus confirmada"]
    Meta --> Consensus["Concordância independente versus repetição"]
    Meta --> Change["Mudança de recomendação e causa"]
    Meta --> Gaming["Métrica otimizada sem ganho real"]
    Deterministic --> Result["Resultados por teste"]
    Semantic --> Result
    Premise --> Result
    Consensus --> Result
    Change --> Result
    Gaming --> Result
    Result --> Pass{"Todos os bloqueantes passam?"}
    Pass -->|"Sim"| F7B["Liberar para F7-B; mérito congelado"]
    F7B --> F8["Após fidelidade determinística, liberar final_markdown para F8"]
    Pass -->|"Não"| Correct["Corrigir artefato ou reabrir fase"]
    Correct --> Tests
    Tests --> Changed{"O critério precisa mudar?"}
    Changed -->|"Sim"| Version["Nova versão, justificativa e reexecução"]
    Version --> Freeze
    Changed -->|"Não"| Draft
```

---

## 11. Aprendizado por correção humana

```mermaid
flowchart LR
    AI["Versão FORJA"] --> Diff["Diff com versão humana aprovada"]
    Human["Versão humana"] --> Diff
    Diff --> Classify{"Causa da mudança"}
    Classify --> Fact["Fato"]
    Classify --> Law["Direito ou fonte"]
    Classify --> Retrieval["Recuperação ou planejamento"]
    Classify --> Term["Terminologia, cálculo ou ciência"]
    Classify --> Visual["Visual"]
    Classify --> Style["Estilo ou preferência"]
    Fact --> Structural{"Erro estrutural reproduzível?"}
    Law --> Structural
    Retrieval --> Structural
    Term --> Structural
    Visual --> Structural
    Style --> Preference["Memória de preferência, sem gate global automático"]
    Structural -->|"Não"| Record["Registrar caso e causa"]
    Structural -->|"Sim"| Fixture["Criar fixture e teste proposto"]
    Fixture --> Review["Revisão e aprovação do teste"]
    Review --> Regression["Adicionar à bateria de regressão"]
    Regression --> Future["Executar em ciclos futuros"]
```

---

## 12. Gestão, modos e rollback

```mermaid
flowchart TD
    Event["Evento canônico do caso"] --> State["Estado FORJA"]
    State --> Validator["Validador N4"]
    Validator --> Sidecar["Sidecar da gestão"]
    Sidecar --> Panel["Painel do escritório"]
    Panel --> View["Modo, cobertura, testes, LCI, bloqueios e próximo passo"]
    View --> Link["Artefatos por artifactId"]

    Flags{"Modo N4"} -->|"off"| Old["Fluxo N2/N3"]
    Flags -->|"shadow"| Compare["Relatório de comparação sem bloquear"]
    Flags -->|"pilot_blocking"| Pilot["Gates apenas no caso escolhido"]
    Flags -->|"default_on após promoção"| Default["Contrato N4 vigente"]

    Validator --> Block{"Existe P0?"}
    Block -->|"Sim"| PanelBlock["Painel destaca bloqueio acima de percentuais"]
    Block -->|"Não"| Progress["Avanço condicionado aos demais gates"]

    Failure["Regressão ou falha de integração"] --> Rollback["Desligar flags N4"]
    Rollback --> Old
    Rollback --> Preserve["Preservar eventos e artefatos para auditoria"]
```

---

## 13. Roadmap e gates de promoção

```mermaid
flowchart LR
    M0["M0 Provar base N3"] --> G0{"Baseline real?"}
    G0 -->|"Não"| Fix0["Corrigir alicerce"]
    Fix0 --> M0
    G0 -->|"Sim"| M1["M1 Questões, cobertura e testes"]
    M1 --> M2["M2 Relações e consistência"]
    M2 --> M3["M3 Lastro científico"]
    M2 --> M4["M4 Estratégia condicional"]
    M3 --> M5["M5 Metacognição, aprendizado e gestão"]
    M4 --> M5
    M5 --> Replay["Replay offline em cópias"]
    Replay --> Shadow["Sombra em casos novos"]
    Shadow --> Pilot["Pilotos bloqueantes controlados"]
    Pilot --> Gate{"Zero P0 conhecido, ganho real e rollback comprovado?"}
    Gate -->|"Não"| Improve["Isolar módulo e corrigir"]
    Improve --> Replay
    Gate -->|"Sim"| Docs["Atualizar contratos, docs e manifest juntos"]
    Docs --> Promote["Promover N4 gradualmente"]
```

---

## 14. Leitura executiva

A N4 acrescenta cinco ideias centrais à FORJA:

1. **completude demonstrável:** perguntas e matriz de cobertura antes da redação;
2. **coerência demonstrável:** eventos, termos, tempo, cálculo e relações verificados no documento inteiro;
3. **apoio científico sério:** pesquisa interdisciplinar proporcional, com método, limites e evidência contrária;
4. **aprendizado demonstrável:** correção humana classificada e transformada em teste apenas quando estrutural;
5. **entrega íntegra:** metadados, perfil de layout e hash são verificados no arquivo selecionado; a evidência pós-entrega usa o hash real quando disponível ou a cadeia `artifactId` + hash pré-envio + comprovante nos demais canais (Gate N4-10).

Nada disso substitui os controles existentes. A candidata N4 depende de uma N3 real, preserva F0–F10 e só se torna obrigatória após replays, sombra, pilotos e promoção normativa.

## 15. Estado final dos canários M6

```mermaid
flowchart LR
    P["Patrícia/Fábio: baseline retrospectiva"] --> OK["24/24, mutações 10/10, QA 6/6"]
    L["Libra Sul: baseline retrospectiva"] --> OK2["24/24, mutações 10/10, QA 7/7"]
    S["Saúde: baseline retrospectiva"] --> OK3["24/24, mutações 10/10, QA 12/12"]
    C["Cafelana: origem revogada"] --> STOP["Bloqueada até AgInt primário"]
    OK --> MODE["pilot_blocking ampliado"]
    OK2 --> MODE
    OK3 --> MODE
    STOP --> MODE
    MODE --> NO["promotionEligible = false"]
    NO --> NEXT["Promoção exige ciclos prospectivos novos"]
```

---

## 16. Diagrama do estado implantado em 11/07/2026

```mermaid
flowchart LR
    Config["Configuração N4"] --> Pick{"Caso listado como piloto?"}
    Pick -- "não" --> Shadow["Executa em sombra; informa sem travar"]
    Pick -- "sim" --> Pilot["Piloto bloqueante controlado"]
    Pilot --> Core["Questões, cobertura, terminologia, testes, ciência e consistência"]
    Pilot --> Advisory["Estratégia condicional permanece consultiva"]
    Core --> Gate{"P0 em grupo promovido?"}
    Gate -- "sim" --> Stop["Interrompe somente o piloto"]
    Gate -- "não" --> F7B["F7-B preserva mérito e produz final_markdown"]
    F7B --> Package["F9 seleciona o arquivo final auditado pelo bundle de hashes"]
    Package --> Delivery["F10 confirma hash do canal ou evidência externa"]
    Delivery --> Management["Gestão recebe estado, bloqueios e links dos artefatos"]
    Shadow --> Management
    Management --> Promote{"Casos mínimos e três ciclos novos completos?"}
    Promote -- "não" --> Candidate["N4 continua candidata"]
    Promote -- "sim, após decisão formal" --> Default["Promoção geral em operação normativa única"]
```

## 17. Anti-autocertificação e decisão do conselho
```mermaid
flowchart TD
    A["Texto canônico registrado"] --> B["Reexecutar testes e mutações"]
    B --> C{"Resultado salvo coincide?"}
    C -- "não" --> X["Bloquear auto-certificação"]
    C -- "sim" --> D["Reproduzir C1-C5 e QA por página"]
    D --> E{"Helena e Cícero aprovaram com parecer e localizador?"}
    E -- "não" --> H["Baseline estrutural; revisão humana obrigatória"]
    E -- "sim" --> F{"Ciclo prospectivo e mutação semântica >= 80%?"}
    F -- "não" --> H
    F -- "sim" --> G["Elegível para decisão de promoção"]
```

O diagrama separa aprovação mecânica, decisão jurídica e promoção. Nenhum score agregado supera fonte revogada, conselho contrário ou ausência de evidência semântica.

---

## 18. Petição como intervenção projetada — PSO-Pet

```mermaid
flowchart TD
    Command["Comando recebido"] --> Mess["Emaranhado processual"]
    Mess --> Define["Problema focal e resultado direto"]
    Define --> Diagnose["História diagnóstica e explicações rivais"]
    Diagnose --> Requirements["Requisitos da intervenção"]
    Requirements --> Alternatives["Alternativas estratégicas"]
    Alternatives --> Synthesis["Síntese da arquitetura"]
    Synthesis --> Evaluate{"Atende aos requisitos?"}
    Evaluate -->|"Não"| Reopen{"Rever alternativa, requisito negociável ou diagnóstico"}
    Reopen --> Alternatives
    Reopen --> Diagnose
    Evaluate -->|"Sim"| Detail["Redação e desenho visual"]
    Detail --> Validate["Validação contra requisitos e melhor objeção"]
    Validate --> Plan["Protocolo, acompanhamento e contingência"]
    Plan --> Outcome["Resultado direto observado"]
    Outcome --> Learn["Avaliação formativa e CIMO-Pet"]
    Learn --> Memory["Retrospectiva, fixture ou hipótese de melhoria"]
```

Leitura: as fases F0–F10 continuam como controle de estado. As setas de retorno representam iteração cognitiva registrada, não regressão silenciosa nem autorização para ignorar gates concluídos.

---

## 19. Fronteira operacional F7/F7-B/F8 — adendo de 15/07/2026

```mermaid
flowchart TD
    F7["PHASE_RESULT F7 em construção"] --> P0{"f7_gate_result: zero P0?"}
    P0 -->|"Não"| Legal["corrigir mérito em nova tentativa F7"]
    P0 -->|"Sim"| Explicit["operador chama forja_fable5.py\nrunner não chama automaticamente"]
    Explicit --> Auth{"Claude Max OAuth + claude-fable-5?"}
    Auth -->|"Não"| Block["bloqueado; sem API fallback"]
    Auth -->|"Sim"| Rewrite["reescrever apenas forma desde audited_markdown"]
    Rewrite --> Gate["forja_editorial_fidelity.py\nrecompõe 4 gates"]
    Gate -->|"reprovou e tentativa interna menor que 3"| Rewrite
    Gate -->|"reprovou na terceira"| Block
    Gate -->|"aprovou"| Frag["FABLE5_RESULT é fragmento"]
    Frag --> Merge["incorporar ao PHASE_RESULT completo"]
    Merge --> Canon["final_markdown canônico"]
    Canon --> F8["F8 e pacote"]

    Phase["retryPolicy F7: até 4 tentativas externas"] -. "contador separado" .-> F7
```

O retorno visual a `Rewrite` significa nova candidata gerada do `audited_markdown` original, nunca edição da candidata rejeitada. A revisão não pode alterar fatos, datas, números, valores, autoridades, citações, marcadores, ressalvas, teses, capítulos, pedidos, fecho ou assinaturas. A N4 pode ampliar auditorias antes do F7-B, mas não conferir ao editor competência de mérito.
