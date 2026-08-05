# Diagramas — FORJA R1

**Versão:** R1.0-plan  
**Regra:** diagramas de estado atual descrevem observação de 2026-07-15; diagramas-alvo descrevem intenção, não implementação concluída

## D01 — Estado normativo atual

```mermaid
flowchart TD
    Input["Caso/comando"] --> N2["N2 vigente<br/>snapshot legado"]
    Input --> N3["N3 sombra<br/>events + attempts"]
    N3 --> Events["FORJA_EVENTS.jsonl"]
    Events --> State["FORJA_N3_STATE.json"]
    N3 --> N4["N4 candidata<br/>pilot_blocking"]
    N4 --> Package["package/close/delivery"]
    N2 -. "compatibilidade" .-> N3
```

## D02 — Arquitetura-alvo

```mermaid
flowchart TD
    CLI["CLI + wrappers"] --> APP["Application services"]
    APP --> DOMAIN["Domain"]
    APP --> PORTS["Ports"]
    DOMAIN --> CATALOG["Canonical catalogs"]
    DOMAIN --> GATES["Composable gates"]
    PORTS --> EVENT["Event store"]
    PORTS --> FS["Filesystem"]
    PORTS --> WORD["Word/Medina"]
    PORTS --> OFFICE["Management outbox"]
    PORTS --> SEARCH["Legal/science search"]
    PORTS --> TELE["Telemetry"]
    LEGACY["N2 adapters"] --> APP
    N3["N3 runtime"] --> APP
    N4["N4 contracts"] --> DOMAIN
```

## D03 — F0–F10 com F2-A

```mermaid
flowchart LR
    F0["F0 Reconciliação"] --> F1["F1 Ingestão"]
    F1 --> F2["F2 Classificação"]
    F2 --> F2A["F2-A 100 perguntas"]
    F2A --> F3["F3 Fontes/regimento"]
    F3 --> F4["F4 Blueprint/conselho"]
    F4 --> F5["F5 Pesquisa"]
    F5 --> F6["F6 Redação"]
    F6 --> F7["F7 Auditoria"]
    F7 --> F8["F8 QA visual"]
    F8 --> F9["F9 Pacote"]
    F9 --> F10["F10 Entrega/evidência"]
    F2A -. "lacuna material" .-> Block["internal_working"]
    F3 -. "fonte/regimento" .-> Block
    F7 -. "fato/citação" .-> Block
```

## D04 — Direção de dependências

```mermaid
flowchart LR
    CLI["cli"] --> APP["application"]
    ADAPTERS["adapters"] --> PORTS["ports"]
    APP --> PORTS
    APP --> DOMAIN["domain"]
    PORTS --> DOMAIN
    DOMAIN --> CORE["core"]
    APP --> CORE
    CLI --> CORE
    X["Proibido"] -. "domain → adapters/Word/rede" .-> ADAPTERS
```

## D05 — Event store e replay

```mermaid
sequenceDiagram
    participant C as Command
    participant L as Lock
    participant E as EventStore
    participant R as Reducer
    participant S as Snapshot
    C->>L: acquire(caseId)
    C->>E: read(revision)
    C->>C: validate transition
    C->>E: append(event, expectedRevision)
    E->>R: replay(events)
    R->>S: atomic materialization
    S-->>C: stateHash/revision
    C->>L: release
```

## D06 — Attempt e promoção transacional

```mermaid
flowchart TD
    Start["prepare attempt"] --> Freeze["contextHash + contractHash + inputs"]
    Freeze --> Work["produção isolada"]
    Work --> Recheck["revalidar contexto/contrato/inputs"]
    Recheck --> Gates["recalcular gates"]
    Gates --> Decision{"todos aprovados?"}
    Decision -->|não| Preserve["preservar attempt bloqueado"]
    Decision -->|sim| Plan["PromotionPlan"]
    Plan --> Commit["commit atômico"]
    Commit --> Event["evento/recibo único"]
    Event --> Canonical["visão canônica"]
```

## D07 — ArtifactCatalog

```mermaid
flowchart TD
    Catalog["ArtifactCatalog"] --> Schema["Schemas"]
    Catalog --> Contract["Contratos"]
    Catalog --> Flags["Flags"]
    Catalog --> Validators["Validadores"]
    Catalog --> Metrics["Métricas"]
    Catalog --> Docs["Docs/diagramas"]
    Catalog --> Coverage["Teste de cobertura"]
    Contextual["Regras contextuais"] --> Validators
    Invalidation["Grafo de invalidação"] --> Coverage
```

## D08 — Regimento fail-closed

```mermaid
flowchart TD
    Case["Caso"] --> Tribunal["identificar tribunal"]
    Tribunal --> Candidates["buscar somente no escopo autorizado"]
    Candidates --> Count{"quantos candidatos?"}
    Count -->|0| Missing["blocked: missing"]
    Count -->|>1| Ambiguous["blocked: ambiguous"]
    Count -->|1| Metadata["fonte/versão/download/emendas"]
    Metadata --> Complete{"integral e atual?"}
    Complete -->|não| Incomplete["blocked: incomplete/stale"]
    Complete -->|sim| Laws["_LEIS_GERAIS"]
    Laws --> Verified["verified → F3 pode avançar"]
```

## D09 — Verificação de citação

```mermaid
stateDiagram-v2
    [*] --> candidate
    candidate --> identity_verified: tribunal/classe/número
    candidate --> rejected: identidade divergente
    identity_verified --> content_verified: íntegra + trecho
    identity_verified --> unverified: fonte indisponível
    content_verified --> final_use_allowed: política satisfeita
    final_use_allowed --> revoked: auditoria invalida
    unverified --> identity_verified: nova diligência
```

## D10 — Injection scan fail-closed

```mermaid
flowchart TD
    Input["arquivo de entrada"] --> Enumerate["registrar no inventário"]
    Enumerate --> Size{"suportado e dentro do limite?"}
    Size -->|não| Unscanned["P0: unscanned + razão"]
    Size -->|sim| Parse["parser por formato"]
    Parse --> Error{"erro?"}
    Error -->|sim| Unscanned
    Error -->|não| Signals["sinais técnicos/contextuais"]
    Signals --> Decision{"ameaça técnica?"}
    Decision -->|sim| Review["P0: triagem humana"]
    Decision -->|não| Clean["scanned_clean"]
```

## D11 — Entrega por identidade

```mermaid
flowchart TD
    Case["Case ID"] --> Package["AuditedPackage"]
    Package --> Select["artifactId + sha256"]
    Select --> Match{"hash confere?"}
    Match -->|não| Block["bloquear"]
    Match -->|sim| Draft["DeliveryDraft"]
    Draft --> Evidence["evidência do canal"]
    Evidence --> Receipt["DeliveryReceipt"]
    Receipt --> Management["outbox de gestão"]
```

## D12 — ManagementOutbox

```mermaid
sequenceDiagram
    participant A as Application
    participant O as Outbox
    participant M as Gestão
    A->>O: enqueue(event, idempotencyKey)
    O-->>A: persisted receipt
    O->>M: flush pending
    alt gestão disponível
        M-->>O: ack
        O->>O: mark delivered
    else indisponível
        M-->>O: transient failure
        O->>O: keep pending + backoff
    end
```

## D13 — Renderização e QA

```mermaid
flowchart TD
    Source["Markdown/artefatos"] --> Parse["parser"]
    Parse --> Model["modelo intermediário"]
    Model --> Compose["composição no template"]
    Compose --> Vector["SVG → EMF"]
    Vector --> Word["Word COM"]
    Word --> PDF["PDF final"]
    PDF --> Pages["render de todas as páginas"]
    Pages --> Visual["QA visual independente"]
    Visual --> Fidelity["fidelidade MD/DOCX/PDF"]
    Fidelity --> Release{"liberar?"}
```

## D14 — Pirâmide de testes

```mermaid
flowchart TD
    Real["Real<br/>Word/PDF/telemetria"]
    Integration["Integração<br/>eventos/filesystem/outbox"]
    Contract["Contrato/mutação<br/>schemas/gates"]
    Unit["Unidade<br/>funções puras"]
    Real --> Integration --> Contract --> Unit
```

## D15 — Descoberta canônica

```mermaid
flowchart TD
    Files["todos test_*.py"] --> Discover["discovery"]
    Manifest["manifesto de suítes"] --> Discover
    Discover --> Compare{"todo teste classificado?"}
    Compare -->|não| Fail["falhar: órfão"]
    Compare -->|sim| Unit["unit"]
    Compare -->|sim| Contract["contract"]
    Compare -->|sim| Integration["integration"]
    Compare -->|sim| Mutation["mutation"]
    Compare -->|sim| Real["real"]
    Unit --> Report["relatório único"]
    Contract --> Report
    Integration --> Report
    Mutation --> Report
    Real --> Report
```

## D16 — Ciclo TDD

```mermaid
flowchart LR
    Characterize["caracterizar"] --> Red["RED"]
    Red --> Green["GREEN mínimo"]
    Green --> Refactor["REFACTOR"]
    Refactor --> Broad["suíte ampla"]
    Broad --> Real{"efeito externo?"}
    Real -->|sim| Canary["canário real"]
    Real -->|não| Evidence["evidência"]
    Canary --> Evidence
```

## D17 — Estrutura atual e alvo

```mermaid
flowchart LR
    subgraph Current["Atual"]
      Root["raiz: runtime + testes + CLIs"]
      Mutable["state/cache/reports"]
      Experiments["pilotos/one-offs"]
      Foreign["cópia FocoEdital"]
    end
    subgraph Target["Alvo"]
      Src["src/forja"]
      Tests["tests"]
      Tools["tools"]
      Exp["experiments/migrations/archive"]
      Var["var"]
    end
    Root --> Src
    Root --> Tests
    Root --> Tools
    Experiments --> Exp
    Mutable --> Var
    Foreign -. "backup + link canônico" .-> Exp
```

## D18 — Migração física por fachada

```mermaid
flowchart TD
    Baseline["teste de caracterização"] --> New["implementação em src/forja"]
    New --> Facade["wrapper no caminho antigo"]
    Facade --> Equivalence["equivalência"]
    Equivalence --> Telemetry["telemetria de uso"]
    Telemetry --> Window{"janela sem uso?"}
    Window -->|não| Keep["manter wrapper"]
    Window -->|sim| Remove["remoção com rollback"]
```

## D19 — Ciclo de shim

```mermaid
stateDiagram-v2
    [*] --> active_legacy
    active_legacy --> facade: implementação nova disponível
    facade --> observed: telemetria ligada
    observed --> facade: uso detectado
    observed --> removal_candidate: janela sem uso
    removal_candidate --> removed: testes + restore aprovados
    removed --> restored: regressão detectada
```

## D20 — Mapa de impacto

```mermaid
flowchart TD
    Change["mudança"] --> Catalog{"catálogo/contrato?"}
    Change --> State{"estado/evento?"}
    Change --> Render{"Word/PDF?"}
    Change --> Delivery{"entrega/gestão?"}
    Catalog --> ContractTests["schema + --check"]
    State --> Replay["replay + concorrência"]
    Render --> VisualQA["Word/PDF + todas as páginas"]
    Delivery --> Evidence["ID/hash + outbox"]
    ContractTests --> Full["régua completa"]
    Replay --> Full
    VisualQA --> Full
    Evidence --> Full
```

## D21 — Ownership paralelo

```mermaid
flowchart TD
    Coordinator["coordenador"] --> Core["owner core"]
    Coordinator --> Domain["owner domain/catalogs"]
    Coordinator --> Render["owner render"]
    Coordinator --> Validate["owner validators"]
    Coordinator --> CLI["owner CLI framework/docs"]
    Core -. "sem arquivo compartilhado" .- Domain
    Render -. "sem arquivo compartilhado" .- Validate
    CLI --> Merge["integração após gates"]
    Core --> Merge
    Domain --> Merge
    Render --> Merge
    Validate --> Merge
    Merge --> Wrappers["migração sequencial de wrappers após P09-P12"]
```

## D22 — Rollback por onda

```mermaid
flowchart LR
    Change["onda executada"] --> Gate{"gate aprovado?"}
    Gate -->|sim| Next["próxima onda"]
    Gate -->|não| Preserve["preservar evidência"]
    Preserve --> Flag["desligar flag/fachada"]
    Flag --> Restore["restore por manifesto/hash"]
    Restore --> Recheck["reexecutar baseline"]
    Recheck --> Stop["parar e diagnosticar"]
```
