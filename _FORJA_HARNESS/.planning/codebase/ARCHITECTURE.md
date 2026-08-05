# Arquitetura da FORJA

**Levantamento:** 2026-07-15  
**Natureza:** descrição do estado atual e arquitetura-alvo proposta

## Síntese

A FORJA é um harness local de produção jurídica orientado por fases, artefatos versionados, gates e rastreabilidade. Sua evolução ocorreu de forma aditiva:

- N2 mantém snapshots e rotinas legadas;
- N3 introduz event store, replay, attempts e promoção por hash;
- N4 introduz schemas, novos artefatos e validação candidata.

Não foram encontrados ciclos estáticos no grafo de imports Python. O acoplamento relevante é conceitual: cada geração conhece detalhes das outras.

## Arquitetura atual

```mermaid
flowchart TD
    Input["Caso e comando"] --> Legacy["N2 legado<br/>FORJA_STATE.json"]
    Input --> Runtime["N3 runtime<br/>events + attempts"]
    Runtime --> Events["FORJA_EVENTS.jsonl"]
    Events --> Replay["derive_state / replay"]
    Replay --> State["FORJA_N3_STATE.json"]
    Runtime --> Phases["F0 a F10"]
    Phases --> Candidate["N4 candidate artifacts"]
    Candidate --> Schemas["n4_schemas"]
    Candidate --> Aggregate["forja_n4_validate"]
    Aggregate --> Package["forja_package"]
    Package --> Render["DOCX / PDF / QA"]
    Package --> Close["forja_close_cycle"]
    Close --> Management["gestao_escritorio"]

    Legacy -. "reconciliação" .-> Runtime
    Runtime -. "ARTIFACT_SPECS" .-> Candidate
    Candidate -. "IO, hash e lock" .-> Runtime
```

## Fluxo das fases

```mermaid
flowchart LR
    F0["F0 Intake"] --> F1["F1 Corpus e identidade"]
    F1 --> F2["F2 Produto e urgência"]
    F2 --> F2A["F2-A<br/>100 perguntas"]
    F2A --> F3["F3 Fontes e regimento"]
    F3 --> F4["F4 Conselho"]
    F4 --> F5["F5 Estratégia e blueprint"]
    F5 --> F5C["F5-C Claims x evidências"]
    F5C --> F6["F6 Redação"]
    F6 --> F7["F7 Citações e verificação"]
    F7 --> F8["F8 Visual e render"]
    F8 --> F9["F9 QA e pacote"]
    F9 --> F10["F10 Entrega e fechamento"]

    F2A -. "lacuna material" .-> Block["internal_working"]
    F3 -. "regimento/fonte insuficiente" .-> Block
    F7 -. "citação não verificada" .-> Block
    F8 -. "QA visual falhou" .-> Block
```

Os nomes exatos devem continuar sendo derivados dos contratos e manifestos. Este diagrama representa responsabilidades, não substitui os arquivos canônicos.

## Estado e eventos N3

`forja_state_machine.py` é uma das partes mais sólidas da base. O estado N3 é derivado; os eventos são a trilha auditável.

```mermaid
sequenceDiagram
    participant CLI as CLI/serviço
    participant Lock as Case lock
    participant Store as Event store
    participant Reducer as derive_state
    participant Snapshot as FORJA_N3_STATE.json

    CLI->>Lock: adquirir lock
    CLI->>Store: ler revision e eventos
    CLI->>CLI: validar transição e expectedRevision
    CLI->>Store: append de evento idempotente
    Store->>Reducer: replay integral
    Reducer->>Snapshot: escrita atômica do estado derivado
    Snapshot-->>CLI: revision/hash resultante
    CLI->>Lock: liberar lock
```

Invariantes a preservar:

- append-only;
- idempotência;
- revisão otimista;
- proibição de regressão silenciosa;
- escrita atômica;
- replay determinístico;
- histórico preservado em invalidações.

## Execução por attempts

`forja_run.py` cria diretórios isolados, registra hashes de contexto e promove resultados. O fluxo desejado é:

```mermaid
flowchart TD
    Start["start attempt"] --> Context["fixar contextHash e contractHash"]
    Context --> Work["produzir em attempt isolado"]
    Work --> Validate["validar artefatos e gates"]
    Validate -->|bloqueado| Keep["preservar attempt para auditoria"]
    Validate -->|aprovado| Promote["promoção transacional"]
    Promote --> Event["registrar evento canônico"]
    Event --> Canonical["atualizar visão canônica"]
```

Risco atual: a promoção verifica `contractHash`, mas o `contextHash` precisa ser revalidado na fronteira final. Cópias/eventos podem ocorrer antes da conclusão do gate N4; isso requer uma política transacional explícita e teste de rollback/estado parcial.

## Catálogo N4 distribuído

Hoje a definição de um artefato pode aparecer em:

- `forja_n4_common.py::ARTIFACT_SPECS`;
- `forja_n4_validate.py::VALIDATORS`;
- `forja_n4_validate.py::FLAG_FILES`;
- `forja_n4_invalidation.py::DEPENDENCIES`;
- `generate_n4_contracts.py`;
- `forja_run_metrics.py`;
- regras contextuais no agregador.

```mermaid
flowchart LR
    A["ARTIFACT_SPECS"] --> V["VALIDATORS"]
    A --> S["Schemas"]
    A --> F["FLAG_FILES"]
    A --> D["DEPENDENCIES"]
    A --> M["Métricas"]
    A --> C["Contratos"]
    V --> G["validate_case"]
    F --> G
    D -. "manual" .-> G
```

Arquitetura-alvo: `ArtifactCatalog` canônico e tipado, capaz de gerar schemas, índices, documentação e checks de completude. Validadores contextuais permanecem código, mas são registrados explicitamente.

## Entrega atual

Três caminhos coexistem:

```mermaid
flowchart TD
    Case["Caso"] --> D2["forja_delivery<br/>N2 heurístico"]
    Case --> D3["forja_package + close_cycle<br/>N3 por hash"]
    Case --> D4["forja_delivery_integrity<br/>N4"]
    D2 --> Office["Gestão/entrega"]
    D3 --> Office
    D4 --> Office
```

O caminho N2 usa glob e primeiro resultado em alguns pontos; o N3 usa identidade e hash. A identidade N3 deve ser canônica, preservando o N2 apenas como adaptador de descoberta legada com alerta de ambiguidade.

## Hubs de dependência

| Módulo | Papel | Sinal arquitetural |
|---|---|---|
| `forja_n3_common.py` | paths, IO, hashing, locks, config | 48 consumidores; precisa virar fachada |
| `forja_n4_common.py` | catálogo e envelope N4 | fonte parcial de verdade |
| `forja_state_machine.py` | eventos e estado derivado | núcleo a preservar |
| `forja_n4_validate.py` | agregador de validações | fan-out alto e muitas responsabilidades |
| `forja_run.py` | attempts e promoção | orquestrador central |
| `forja_package.py` | Definition of Done e pacote | defesa contra autocertificação |

## Arquitetura-alvo

```mermaid
flowchart TD
    CLI["CLI fina e wrappers legados"] --> App["Application services"]
    App --> Domain["Domain<br/>phases, artifacts, tribunals, gates"]
    App --> Ports["Ports"]
    Domain --> Catalog["Canonical catalogs"]
    Domain --> Validators["Composable validators"]
    Ports --> Event["Event store"]
    Ports --> Files["Filesystem"]
    Ports --> Word["Word/Medina renderer"]
    Ports --> Office["Management outbox"]
    Ports --> Search["Legal/science search"]
    Ports --> Telemetry["Telemetry"]
    Legacy["N2 adapters"] --> App
    N3["N3 runtime"] --> App
    N4["N4 contracts"] --> Domain
```

### Camadas propostas

- `core`: IO, tempo, IDs, hashing, locks, paths e erros.
- `domain`: fases, tribunais, artefatos, severidades e políticas.
- `application`: start/resume/promote, validate, package, close e reconcile.
- `ports`: contratos para filesystem, Word, gestão, busca e telemetria.
- `adapters`: implementações locais/Windows/legadas.
- `cli`: parsing e apresentação, sem regra jurídica.

## Hotspots

| Símbolo | Tamanho aproximado | Extração indicada |
|---|---:|---|
| `forja_visual.compor` | 321 linhas | parsing, layout, tabelas, emissão |
| `forja_delivery.main` | 186 linhas | CLI, resolução, regra, integração |
| `forja_render_docx.render` | 165 linhas | composição, Word, exportação, QA |
| `forja_pso_pet.validate_plan` | 161 linhas | schema, regras, métricas |
| `forja_n4_m6_cycles.run` | 161 linhas | orquestração e operações |
| `validate_adversarial_audit` | 136 linhas | ledger, regras e relatório |
| `forja_n4_validate.validate_case` | 115+ linhas | pipeline de validadores |

## Regra de migração

Nenhuma camada deve ser substituída de uma vez. Extrair, reexportar pela fachada existente, comparar comportamento, observar telemetria e só então remover o caminho antigo.
