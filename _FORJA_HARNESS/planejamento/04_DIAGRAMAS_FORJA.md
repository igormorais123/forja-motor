# DIAGRAMAS — FORJA N2

**Versão:** N2.0  
**Data:** 2026-07-08  
**Status:** vigente para execução  
**PRD:** `01_PRD_FORJA.md`  
**TDD:** `02_TDD_FORJA.md`  
**Roadmap:** `03_ROADMAP_FORJA.md`

> Estes diagramas substituem os diagramas v2.0 anteriores. O fluxo agora é bloqueante, evidencial e sanitizado.

---

## 1. Fluxo macro F0-F10

```mermaid
flowchart TD
    Start([Inicio]) --> F0["F0 Reconcilia fila real"]
    F0 --> G0{"Origem, pasta e comando existem?"}
    G0 -->|Nao| B0["Bloqueado: intake incompleto"]
    G0 -->|Sim| F1["F1 Ingestao segura"]
    F1 --> F2["F2 Classifica produto, tribunal, prazo e urgencia"]
    F2 --> F3["F3 Fontes, regimento e leis gerais"]
    F3 --> G3{"Regimento e fontes minimas OK?"}
    G3 -->|Nao| B3["Bloqueado: fontes/regimento"]
    G3 -->|Sim| F4["F4 Blueprint estrategico"]
    F4 --> F5["F5 Pesquisa oficial"]
    F5 --> G5{"Citacoes e fatos criticos verificados?"}
    G5 -->|Nao| B5["Bloqueado: pendencia de fonte"]
    G5 -->|Sim| F6["F6 Redacao em template"]
    F6 --> F7["F7 Auditoria juridica e factual"]
    F7 --> G7{"Auditoria sem P0?"}
    G7 -->|Nao| F4
    G7 -->|Sim| F7B["F7-B Fable 5: revisão editorial controlada"]
    F7B --> G7B{"Fidelidade, estilo e OAuth aprovados?"}
    G7B -->|Nao| B7B["Bloqueado: candidata descartada; retry desde origem"]
    G7B -->|Sim| F8["F8 compõe a partir de final_markdown"]
    F8 --> G8{"PDF visual aprovado?"}
    G8 -->|Nao| F6
    G8 -->|Sim| F9["F9 Pacote revisao; draft opcional"]
    F9 --> G9{"Evidencia de entrega?"}
    G9 -->|Nao| W9["Pronta, nao cumprida"]
    G9 -->|Sim| F10["F10 Cumprida com evidencia e aprendizado"]
    F10 --> End([Fim])
```

---

## 2. Maquina de estados

```mermaid
stateDiagram-v2
    [*] --> nova
    nova --> em_reconciliacao
    em_reconciliacao --> blocked: sem pasta/comando/origem
    em_reconciliacao --> em_fontes: intake OK
    em_fontes --> blocked: regimento ou fonte P0 ausente
    em_fontes --> em_planejamento: fontes minimas OK
    em_planejamento --> em_pesquisa: blueprint aprovado
    em_planejamento --> blocked: divergencia grave sem decisao
    em_pesquisa --> blocked: citacao final nao oficial
    em_pesquisa --> em_redacao: citacoes verificadas
    em_redacao --> em_auditoria
    em_auditoria --> em_planejamento: P0 estrutural
    em_auditoria --> em_revisao_editorial: zero P0 em F7
    em_revisao_editorial --> blocked: F7-B reprovado ou OAuth/modelo nao comprovado
    em_revisao_editorial --> em_qa_visual: final_markdown e gates F7-B aprovados
    em_qa_visual --> em_redacao: defeito visual
    em_qa_visual --> pronta_para_revisao: QA OK
    pronta_para_revisao --> aguardando_evidencia_entrega: pacote entregue para revisao
    aguardando_evidencia_entrega --> cumprida: evidencia arquivada
    aguardando_evidencia_entrega --> pronta_para_revisao: faltou prova
    blocked --> em_reconciliacao: bloqueio de intake resolvido
    blocked --> em_fontes: bloqueio de fonte resolvido
    blocked --> cancelada
    cumprida --> [*]
    cancelada --> [*]
```

---

## 3. Fonte de verdade

```mermaid
flowchart LR
    Painel["Painel e demandas.json<br/>gestao operacional"]
    Comando["COMANDO_DO_EMAIL/WHATSAPP/MANUAL<br/>orientacao"]
    Anexos["Anexos, autos, PDFs, DOCX<br/>prova documental"]
    Oficial["Portais oficiais e regimentos<br/>fonte normativa"]
    Evidencia["Email enviado, protocolo,<br/>WhatsApp entregue ou override<br/>evidencia de cumprimento"]
    FORJA["FORJA_STATE.json<br/>orquestracao"]

    Painel --> FORJA
    Comando --> FORJA
    Anexos --> FORJA
    Oficial --> FORJA
    Evidencia --> FORJA

    Painel -. nao prova fato juridico .-> Anexos
    FORJA -. nao marca cumprida sem .-> Evidencia
```

---

## 4. Sequencia de reconciliacao e ingestao

```mermaid
sequenceDiagram
    participant Scheduler as "Automacao validada ou execucao manual"
    participant Panel as "Painel local"
    participant Data as "demandas/intervencoes/status"
    participant Folders as "Pastas de casos"
    participant Gmail as "Gmail/gws"
    participant Hermes as "Hermes sanitizado"
    participant State as "FORJA_STATE"

    Scheduler->>Panel: iniciar reconciliacao
    Panel->>Data: ler JSONs
    Panel->>Folders: localizar comandos e anexos
    Panel->>Gmail: testar acesso se aplicavel
    Gmail-->>Panel: ok ou needs_login/degraded
    Panel->>Hermes: ler apenas sinais sanitizados
    Hermes-->>Panel: comandos/cards, sem conversa bruta
    Panel->>State: criar/atualizar estado
    State-->>Panel: pendencias e proxima acao
```

---

## 5. Gate de fontes e regimento

```mermaid
flowchart TD
    A["Entrada: comando + pasta"] --> B["Identificar tribunal"]
    B --> C["Ler REGIMENTO_INTERNO_TRIBUNAL.md"]
    C --> D{"Regimento integral com metadados?"}
    D -->|Nao| E["Bloquear: obter fonte oficial integral"]
    D -->|Sim| F["Conferir emendas posteriores"]
    F --> G["Consultar _LEIS_GERAIS"]
    G --> H["Classificar fatos no ledger"]
    H --> I{"Ha fato/citacao critica nao verificada?"}
    I -->|Sim| J["Bloquear ou marcar artefato interno"]
    I -->|Nao| K["Liberar blueprint/pesquisa"]
```

---

## 6. Pesquisa e citacao oficial

```mermaid
flowchart TD
    A["Tema juridico"] --> B["Busca exploratoria"]
    B --> C["Candidato de precedente"]
    C --> D{"Fonte oficial encontrada?"}
    D -->|Nao| E["Nao entra como citacao final"]
    D -->|Sim| F["Registrar numero, orgao, relator, data, teor e link/arquivo"]
    F --> G{"Teor confere com uso no texto?"}
    G -->|Nao| H["Remover ou reescrever como parafrase segura"]
    G -->|Sim| I["Citacao final permitida"]
```

---

## 7. Redacao, auditoria e QA visual

```mermaid
flowchart TD
    A["Blueprint + fontes verificadas"] --> B{"Template ou peca anterior?"}
    B -->|Nao| X["Bloqueado: documento vazio proibido"]
    B -->|Sim| C["Redigir minuta DOCX"]
    C --> D["Auditoria factual e juridica"]
    D --> E{"P0 aberto?"}
    E -->|Sim| F["Voltar a blueprint, pesquisa ou redacao"]
    E -->|Nao| G["PDF via Word COM"]
    G --> H["Renderizar 100 por cento das paginas"]
    H --> I{"Visual aprovado?"}
    I -->|Nao| C
    I -->|Sim| J["Pacote de revisao"]
```

---

## 8. Entrega e cumprimento

```mermaid
sequenceDiagram
    participant Forja as "FORJA"
    participant Igor as "Igor"
    participant Gmail as "Gmail"
    participant Evidence as "Pasta de evidencias"
    participant Panel as "Painel"

    Forja->>Igor: pacote DOCX/PDF/relatorios
    alt draft autorizado
        Forja->>Gmail: criar draft com approvedRecipients
        Gmail-->>Forja: draftId
    else sem autorizacao
        Forja-->>Igor: pacote local apenas
    end

    Igor->>Gmail: envia manualmente, se aprovado
    Igor->>Evidence: arquiva prova de envio/protocolo/entrega
    Evidence-->>Forja: evidencia localizada
    Forja->>Panel: marcar cumprida

    Note over Forja,Panel: Sem evidencia, status fica pronta ou aguardando evidencia.
```

---

## 9. Arquitetura de componentes

```mermaid
flowchart TD
    subgraph Local["PC Igor"]
        Panel["Painel local 127.0.0.1:8765"]
        Data["JSONs gestao_escritorio"]
        Harness["_FORJA_HARNESS"]
        State["FORJA_STATE.json"]
        Word["Word COM"]
        Tools["Inkscape / Graphviz / Mermaid CLI / Tectonic"]
    end

    subgraph Sources["Fontes"]
        CaseFiles["Pastas de caso e anexos"]
        Official["Portais oficiais e regimentos"]
        Gmail["Gmail/gws"]
        Hermes["Hermes sanitizado"]
    end

    subgraph Outputs["Saidas"]
        Package["Pacote de revisao"]
        Evidence["Evidencia de entrega"]
        Learning["Aprendizados do caso"]
    end

    Panel --> Data
    Panel --> Harness
    Harness --> State
    CaseFiles --> Harness
    Official --> Harness
    Gmail --> Harness
    Hermes --> Harness
    Harness --> Word
    Harness --> Tools
    Word --> Package
    Package --> Evidence
    Evidence --> Data
    Harness --> Learning
```

---

## 10. Leitura executiva

O fluxo correto do FORJA N2 é:

1. reconciliar a realidade;
2. bloquear entrada incompleta;
3. provar fonte e regimento;
4. planejar com divergencia registrada;
5. validar citacoes oficialmente;
6. redigir em template;
7. auditar;
8. revisar editorialmente com Fable 5, recompor os gates e então renderizar e inspecionar;
9. entregar pacote ou draft autorizado;
10. marcar cumprida apenas com evidencia.

Se algum diagrama conflitar com o PRD/TDD/Manifest, vence o manifest e a regra mais restritiva.

---

## 11. Adendo de leitura — fronteira F7-B (15/07/2026)

```mermaid
flowchart LR
    Audit["audited_markdown + f7_gate_result sem P0"] --> Run["forja_fable5.py\nacionamento explícito"]
    Run --> Auth{"OAuth Max e claude-fable-5 comprovados?"}
    Auth -->|Nao| Block["Bloqueia sem promover"]
    Auth -->|Sim| Candidate["candidata editorial"]
    Candidate --> Fidelity["forja_editorial_fidelity.py\nhashes e invariantes recompostos"]
    Fidelity -->|Reprovou; ate 3| Origin["retomar audited_markdown original"]
    Origin --> Run
    Fidelity -->|Aprovou| Fragment["FABLE5_RESULT fragmento"]
    Fragment --> Merge["incorporar ao PHASE_RESULT F7"]
    Merge --> Canon["final_markdown canonico"]
    Canon --> F8["F8 QA visual"]
```

As três candidatas editoriais do diagrama (inicial + até dois retries) são internas a uma tentativa F7. O contrato da fase continua admitindo até quatro tentativas externas, cada uma com diretório e trilha próprios. O runner não chama o Fable 5 por conta própria.
