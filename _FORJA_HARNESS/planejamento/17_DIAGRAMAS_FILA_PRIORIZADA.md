# Diagramas — FORJA FILA (priorização automática painel → FORJA)

Par de `15_PRD_FILA_PRIORIZADA.md` e `16_TDD_FILA_PRIORIZADA.md`.

## 1. Fluxo de dados (quem lê e quem escreve o quê)

```mermaid
flowchart LR
    subgraph Painel["gestao_escritorio/ (quadro de comando — humano/Hermes)"]
        DJ["demandas.json<br/>(NUNCA escrito pela fila)"]
        IM["intervencoes_manuais.json"]
        FF["data/forja_fila.json<br/>(escrito pela fila, atômico)"]
        RD["render_dashboard.py<br/>seção 'Próximas peças'"]
        HTML["painel HTML"]
    end
    subgraph Harness["_FORJA_HARNESS/"]
        REC["forja_reconcile.py (F0)<br/>findings de bloqueio"]
        ST["state/case-*/FORJA_STATE.json"]
        FILA["forja_fila.py<br/>classifica + pontua + ordena"]
        FPJ["state/FILA_PRIORIZADA.json<br/>(canônico)"]
        REL["reports/FILA_&lt;data&gt;.md<br/>(humano, score decomposto)"]
    end
    DJ -- leitura --> REC
    DJ -- leitura + sha256 --> FILA
    IM -- leitura --> REC
    REC -- grava --> ST
    ST -- leitura --> FILA
    REC -. "flag filaPriorizadaV1<br/>(falha não derruba F0)" .-> FILA
    FILA -- grava --> FPJ
    FILA -- grava --> REL
    FILA -- grava --> FF
    FF -- leitura (degradação limpa) --> RD
    RD -- gera --> HTML
```

## 2. Máquina de classificação de prontidão (ordem de precedência)

```mermaid
flowchart TD
    D["demanda do painel"] --> C1{"status == cumprida?"}
    C1 -- sim --> FORA["fora da fila"]
    C1 -- não --> C2{"FORJA_STATE em F1-F9?"}
    C2 -- sim --> EP["em_producao"]
    C2 -- não --> C3{"waiting_delivery_evidence?"}
    C3 -- sim --> AE["aguardando_evidencia"]
    C3 -- não --> C4{"P0 de pasta/origem no F0?"}
    C4 -- sim --> BP["bloqueada_pasta"]
    C4 -- não --> C5{"COMANDO_*.md ausente?"}
    C5 -- sim --> BC["bloqueada_comando"]
    C5 -- não --> C6{"anexos externos/incompletos?"}
    C6 -- sim --> BA["bloqueada_acesso"]
    C6 -- não --> C7{"proximaAcao no léxico<br/>de decisão do cliente?"}
    C7 -- sim --> BD["bloqueada_decisao_cliente<br/>(+badge se &gt;48h)"]
    C7 -- não --> PR["pronta → compete na fila<br/>score = urgência + prazo + valor + idade"]
```

## 3. Sequência operacional (dia a dia do Igor)

```mermaid
sequenceDiagram
    participant H as Hermes/Igor (painel)
    participant R as forja_reconcile.py (F0)
    participant F as forja_fila.py
    participant P as painel HTML
    participant A as agente/Efesto (produção)
    H->>H: ajusta urgenciaManual / prazo no painel
    R->>R: audita 23 demandas (findings P0-P2)
    R->>F: chama fila (flag on; falha não derruba F0)
    F->>F: classifica prontidão + score explicável
    F->>P: forja_fila.json → seção "Próximas peças"
    Note over P: Igor vê top 5 + bloqueadas por motivo<br/>sem abrir nenhuma pasta
    A->>F: python forja_fila.py --proxima
    F-->>A: caso do topo (caseId, pasta, comando, score)
    A->>A: dispara produção F1-F10 (comando explícito,<br/>NUNCA automático — anti-requisito do PRD)
```

## 4. Onde a fila NÃO mexe (fronteiras de segurança)

```mermaid
flowchart TD
    FILA["forja_fila.py"]
    FILA -- "só leitura" --> DJ["demandas.json"]
    FILA -- "só leitura" --> ST["FORJA_STATE.json dos casos"]
    FILA -- "nunca toca" --> PIPE["forja_run / forja_headless / F1-F10"]
    FILA -- "nunca toca" --> SYNC["sync_forja_gestao.py / forja_status.json / eventos N3"]
    FILA -- "escreve (derivado, regenerável)" --> OUT["FILA_PRIORIZADA.json + FILA_&lt;data&gt;.md + forja_fila.json"]
```
