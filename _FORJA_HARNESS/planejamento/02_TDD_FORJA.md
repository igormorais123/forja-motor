# TDD — FORJA N2

**Produto:** FORJA, harness técnico para produção jurídica auditável  
**Versão:** N2.0  
**Data:** 2026-07-08  
**Status:** vigente para implementação  
**PRD:** `01_PRD_FORJA.md`  
**Roadmap:** `03_ROADMAP_FORJA.md`  
**Diagramas:** `04_DIAGRAMAS_FORJA.md`  
**Manifest:** `_FORJA_HARNESS/FORJA_SPEC_MANIFEST.json`  
**Gates de qualidade:** `06_GATES_QUALIDADE_FORJA.md` — catálogo canônico minerado das entregas reais; os contratos por fase da seção 7 DEVEM implementar os gates G* correspondentes (em conflito, o catálogo detalha e o manifest arbitra).

> Este TDD substitui o desenho técnico v1.0. Nenhum agente deve usar flags, custos, escopo ou estados do TDD antigo sem validar contra este documento.

---

## 1. Objetivo técnico

Implementar FORJA como orquestrador local, persistente e bloqueante para demandas jurídicas da fábrica. O sistema deve coordenar ingestão, fontes, regimento, planejamento, pesquisa oficial, redação, auditoria, QA visual, pacote de revisão e fechamento com evidência.

O design técnico é conservador: primeiro estado, contratos e evidência; depois automação headless. O sistema deve degradar explicitamente quando Gmail, Hermes, pesquisa oficial, Word COM ou ferramenta visual falhar.

---

## 2. Topologia

### PC local Igor

- `gestao_escritorio` como painel e dados de fila.
- `_FORJA_HARNESS` como orquestrador, estado, logs e documentação.
- Word COM para DOCX/PDF final.
- Inkscape, Graphviz, Mermaid CLI e Tectonic para visual law quando aplicável.

### VPS Hermes

- Fonte de sinais WhatsApp apenas quando sanitizados.
- Não processar nem expor conversa bruta.
- Não usar VPS antiga como destino padrão.

### Google

- Gmail/gws para leitura/draft quando autenticado.
- Calendar é lembrete humano, não executor técnico.
- Automação real deve ser Codex automation, Windows Task Scheduler ou serviço local validado.

---

## 3. Componentes

| Componente | Responsabilidade |
|---|---|
| `FORJA_SPEC_MANIFEST.json` | fonte normativa de versão, regras e fases |
| `FORJA_STATE.json` | estado persistente por caso |
| `forja_reconcile` | ler painel, comandos, pastas e evidências |
| `forja_ingest` | criar/reconciliar demanda, pasta e anexos |
| `forja_sources` | montar ledger de fontes, regimento e leis gerais |
| `forja_blueprint` | produzir plano jurídico com divergências registradas |
| `forja_official_search` | validar citações em fonte oficial |
| `forja_draft` | gerar DOCX a partir de template ou peça anterior |
| `forja_audit` | verificar fatos, citações, prazos, anexos, placeholders e metadados |
| `forja_visual_qa` | gerar PDF, renderizar páginas e registrar inspeção |
| `forja_delivery` | gerar pacote, draft opcional e reconciliação de evidência |
| `forja_costs` | registrar custo real por fase |

Nomes acima são contratos funcionais. A implementação pode usar scripts ou serviços diferentes, desde que preserve entradas, saídas e gates.

---

## 4. Estrutura de arquivos

```text
_FORJA_HARNESS/
  FORJA_SPEC_MANIFEST.json
  planejamento/
    01_PRD_FORJA.md
    02_TDD_FORJA.md
    03_ROADMAP_FORJA.md
    04_DIAGRAMAS_FORJA.md
    05_FORJA_NIVEL_2_ANALISE_E_PLANO_CORRIGIDO.md
  state/
    <caseId>/
      FORJA_STATE.json
      logs/
      checkpoints/
      artifacts.json
  cache/
    fontes_oficiais/
    jurisprudencia/
  reports/
```

Se a pasta `state/` ainda não existir, a primeira implementação deve criá-la.

---

## 5. Schema de estado

### `FORJA_STATE.json`

```json
{
  "caseId": "case-...",
  "specVersion": "N2.0",
  "createdAt": "2026-07-08T00:00:00-03:00",
  "updatedAt": "2026-07-08T00:00:00-03:00",
  "currentPhase": "F0_RECONCILIACAO_FILA",
  "status": "running",
  "inputs": {
    "demandId": "demanda-...",
    "caseFolder": "C:/...",
    "commandFile": "COMANDO_DO_EMAIL.md"
  },
  "phaseHistory": [],
  "artifacts": [],
  "gates": [],
  "sourceLedger": [],
  "deliveryEvidence": null,
  "costLog": []
}
```

### Status válidos

- `pending`
- `running`
- `blocked`
- `degraded`
- `ready_for_review`
- `waiting_delivery_evidence`
- `fulfilled`
- `cancelled`
- `failed`

### Severidade de bloqueio

- `P0`: impede peça final, draft ou marcação como pronta.
- `P1`: permite continuar fase interna, mas exige correção antes de F9.
- `P2`: melhoria ou alerta de qualidade.

---

## 6. Extensão em `demandas.json`

```json
{
  "forja": {
    "version": "N2.0",
    "enabled": true,
    "caseId": "case-...",
    "phase": "F0_RECONCILIACAO_FILA",
    "phaseStatus": "running",
    "caseFolder": "C:/...",
    "commandFile": "COMANDO_DO_EMAIL.md",
    "approvedRecipients": [],
    "blockedReasons": [],
    "deliveryEvidence": {
      "status": "none|draft_created|sent_confirmed|manual_override",
      "path": null,
      "confirmedAt": null
    },
    "costs": {
      "budgetUsd": null,
      "actualUsd": null,
      "requiresApproval": false
    }
  }
}
```

Regra: o JSON operacional registra somente o que serve para execução e auditoria: IDs, pasta, comando, anexos, gates, fontes, evidências, artefatos e custos. Conteúdo completo de comunicação só entra quando for artefato necessário do caso, com caminho e origem.

---

## 7. Contratos por fase

### F0 — Reconciliação da fila

**Entrada:** `demandas.json`, `intervencoes_manuais.json`, `status_integracoes.json`, comandos, pastas, evidências.  
**Saída:** estado de integrações, pendências e `FORJA_STATE.json` criado/atualizado.  
**Bloqueia se:** demanda sem pasta, sem comando, sem origem ou com status contraditório.  
**Observação:** Gmail sem login vira `degraded` ou `needs_login`, nunca `ok`.

### F1 — Ingestão segura

**Entrada:** e-mail/comando/sinal sanitizado.  
**Saída:** pasta, comando, lista de anexos, hashes quando viável, entrada do painel.  
**Bloqueia se:** anexo essencial faltando, pasta ambígua sem deduplicação ou comando vazio.

### F2 — Classificação produto/risco

**Entrada:** comando e inventário inicial.
**Saída:** tipo de produto, tribunal provável, prazo, urgência, destinatário de revisão, evidência mínima e `F2_QUESTION_TREE.json` no protocolo `FORJA-F2A-100-v1`.
**Contrato F2-A:** exatamente 100 perguntas `Q001..Q100`; 10 óticas × 10; pergunta, âncora, importância, resposta, natureza epistemológica e rota; fatos/eventos/precedentes/cálculos com `supportIds`; lacunas com consequência; duas soluções comparadas; definição do problema, diagnóstico e handoff F3–F7.
**Bloqueia se:** tipo de produto indefinido, tribunal indefinido quando necessário, pasta/comando ausente, anexos esperados não mapeados, contagem/diversidade inválida, resposta factual sem lastro, rota ausente ou questão material bloqueada para fins de F6.

### F3 — Fontes, regimento e leis gerais

**Entrada:** pasta do caso, comando, `_LEIS_GERAIS`, regimento e `F2_QUESTION_TREE.json`.
**Saída:** `F3_MAPA_FONTES_E_REGIMENTO.md` e ledger de fontes.  
**Bloqueia se:** regimento ausente/incompleto, emendas sem conferência, fonte crítica não localizada.

### F4 — Blueprint estratégico

**Entrada:** mapa de fontes, documentos, produto, risco e `F2_QUESTION_TREE.json`.
**Saída:** `F4_BLUEPRINT_ESTRATEGICO.md`.  
**Bloqueia se:** tese depende de fato não documentado sem marcação, ou divergência estratégica grave sem decisão.

### F5 — Pesquisa oficial

**Entrada:** blueprint e temas de pesquisa.  
**Saída:** `F5_JURISPRUDENCIA_VERIFICADA.md`, `F5_CITACOES_REMOVIDAS.md`.  
**Bloqueia se:** citação final não tem fonte oficial ou arquivo oficial arquivado.

### F6 — Redação em template

**Entrada:** template/peça anterior, blueprint, fontes e citações verificadas.  
**Saída:** minuta DOCX.  
**Bloqueia se:** documento nasceu de arquivo vazio, quebrou timbre/padrão, contém placeholder ou usa fato sem fonte.

### F7 — Auditoria jurídica/factual

**Entrada:** minuta, ledger, jurisprudência, anexos e regimento.  
**Saída:** `F7_RELATORIO_AUDITORIA.md`, `CHECKLIST_FONTES_E_PENDENCIAS.md`.  
**Bloqueia se:** qualquer P0 estiver aberto.

#### F7-B — Revisão editorial e escrita final pelo Claude Fable 5

**Posição:** subfase de F7 executada somente depois de `f7_gate_result` comprovar zero P0 e antes de F8.

**Executor:** `forja_fable5.py`; o runner genérico não a dispara automaticamente.

**Entrada:** `audited_markdown`, `f7_gate_result`, `RUN_CONTEXT.json` da tentativa F7.

**Saída canônica:** `final_markdown`; F8 e pacotes novos não usam `audited_markdown` como texto final.

**Evidências:** `editorial_report`, `editorial_diff`, `fable5_usage`, `editorial_fidelity` e o fragmento `FABLE5_RESULT`.

**Bloqueia se:** OAuth Claude Max não for comprovado, o modelo real não for `claude-fable-5`, houver divergência de hash/invariante ou gate editorial reprovado.

O executor chama `claude -p --model fable --output-format json --permission-mode dontAsk --tools ""`, fornece o conteúdo por stdin e valida previamente `claude auth status` (`loggedIn=true`, `authMethod=claude.ai`, `subscriptionType=max`). Não usa API key. O envelope de uso deve registrar sessão, modelo, autenticação, hashes e tokens observados.

`forja_editorial_fidelity.py` recompõe, diretamente dos arquivos, quatro gates contratuais: `fable5_oauth_confirmed`, `editorial_source_hash_match`, `editorial_fidelity_pass` e `human_style_final_pass`. A fidelidade compara números/datas/valores, marcadores processuais, autoridades, aspas, marcadores de auditoria, títulos, retenção mínima de conteúdo, pedidos/fecho e ausência de origem operacional. O modelo não autocertifica a aprovação.

São permitidas três candidatas internas no total: a inicial e até dois retries. Cada retry recebe os achados determinísticos da candidata anterior, mas recomeça do `audited_markdown` original; não edita incrementalmente a saída rejeitada. Esse laço não altera `retryPolicy.maxAttempts=4` da fase F7: quatro tentativas de fase e três candidatas editoriais internas são contadores distintos.

`FABLE5_RESULT.json` contém apenas o fragmento `status`, `producer`, `producerRole`, `gates` e `artifacts`. Para promoção, o orquestrador deve incorporar esse fragmento ao `PHASE_RESULT.json` da tentativa, preservando também os artefatos jurídicos F7. O fragmento isolado nunca constitui resultado completo da fase.

### F8 — QA visual

**Entrada:** DOCX auditado.  
**Saída:** PDF, imagens renderizadas, relatório de inspeção.  
**Bloqueia se:** qualquer página não foi inspecionada, diagrama ilegível, rodapé/timbre/folio quebrado ou sobreposição.

### F9 — Pacote de revisão e draft opcional

**Entrada:** DOCX/PDF aprovados e checklist sem P0.  
**Saída:** pacote de revisão; draft Gmail apenas se autorizado.  
**Bloqueia se:** `approvedRecipients` vazio para draft, anexos errados, Gmail degradado sem fallback manual.

### F10 — Entrega, evidência e aprendizado

**Entrada:** evidência de entrega/protocolo/envio ou intervenção manual.  
**Saída:** `F10_DOCUMENTACAO_FINAL/`, atualização de painel, aprendizado.  
**Bloqueia se:** não houver evidência real.

---

## 8. Ledger de fontes

Cada item crítico deve ser gravado com:

```json
{
  "id": "src-001",
  "claim": "Fato ou citação usada",
  "classification": "FONTE_ARQUIVO|FONTE_OFICIAL|DECLARACAO|INFERENCIA|HIPOTESE|NAO_VERIFICADO",
  "sourcePathOrUrl": "C:/... ou URL oficial",
  "pageOrEvent": "p. 12 / evento 183 / item 4",
  "verifiedAt": "2026-07-08T00:00:00-03:00",
  "finalUseAllowed": true
}
```

`NAO_VERIFICADO` sempre tem `finalUseAllowed=false`.

---

## 9. Adaptadores técnicos

### Gmail/gws

- Preferir `gws.cmd` em PowerShell.
- `invalid_grant` ou `precisa_login` vira `needs_login`.
- Draft depende de autorização e destinatários da demanda.
- Nunca enviar automaticamente.

### Hermes/WhatsApp

- Entrada permitida: sinal sanitizado, card de triagem, `COMANDO_DO_WHATSAPP.md`.
- Proibido: conversa bruta em painel, chat ou relatório público.

### Pesquisa oficial

- Fonte não oficial é apenas descoberta.
- Fonte oficial ou arquivo oficial arquivado é obrigatório para citação final.

### Word/visual law

- DOCX final deve partir de template ou peça anterior.
- PDF final via Word COM.
- SVG para EMF via Inkscape quando houver diagrama vetorial.
- Render e inspeção de todas as páginas.

### Custos

- Registrar modelo, tokens, custo estimado e custo real quando disponível.
- Se custo exceder limite configurado, bloquear e pedir autorização.

---

## 10. APIs locais sugeridas

Se integradas ao painel local, usar endpoints com semântica conservadora:

- `POST /api/forja/reconcile`
- `POST /api/forja/start`
- `GET /api/forja/status/<caseId>`
- `POST /api/forja/phase/<caseId>/advance`
- `POST /api/forja/block/<caseId>`
- `POST /api/forja/approve-draft/<caseId>`
- `POST /api/forja/delivery-evidence/<caseId>`
- `GET /api/forja/artifacts/<caseId>`

Endpoints não devem aceitar `cumprida` sem payload de evidência.

---

## 11. Tratamento de erros

| Erro | Estado | Ação |
|---|---|---|
| Gmail sem login | `degraded` ou `needs_login` | mostrar login/fallback, não alegar leitura completa |
| Pasta/comando ausente | `blocked` P0 | pedir reconciliação manual |
| Regimento ausente | `blocked` P0 | obter PDF oficial integral e converter |
| Fonte oficial indisponível | `blocked` P0 se citação final depende disso | remover citação ou aguardar validação |
| Word COM falha | `degraded` | tentar novamente; fallback não vira final sem autorização |
| QA visual incompleto | `blocked` P0 | renderizar/inspecionar páginas faltantes |
| Sem evidência de entrega | `waiting_delivery_evidence` | manter pronta, não cumprida |

---

## 12. Proibições técnicas

- Não usar `git reset --hard` ou checkout destrutivo.
- Não mover conteúdo de `_SOMBRA_*` para pasta principal automaticamente.
- Não apagar duplicidades sem inventário e recomendação.
- Não transformar conversa, anotação ou resumo em prova de entrega sem evidência arquivada.
- Não usar `Document()` vazio para peça final.
- Não usar Google Calendar como executor técnico.
- Não criar simulação de probabilidade de vitória como relatório final.

---

## 13. Ordem de implementação recomendada

1. Estado, schema e manifest.
2. Reconciliação de fila e evidência.
3. Gate de fontes/regimento.
4. Pesquisa oficial e ledger.
5. Redação com template.
6. Auditoria e QA visual.
7. Draft opcional.
8. Fechamento com evidência.

Claude/headless ou multiagente só entram depois dos contratos acima existirem.

---

## 14. Subsistema de auditoria adversarial — A1

`forja_adversarial_audit.py` implementa um ledger encadeado para peças responsivas:

1. F3 produz `adversarial_audit`, vinculado pelo SHA-256 à peça adversária;
2. F4 produz `adversarial_strategy`, vinculado ao hash do audit aprovado;
3. F7 produz `adversarial_recheck`, vinculado aos hashes do audit e da estratégia;
4. `forja_run.py` impede promoção quando o validador da fase rejeita o artefato;
5. `forja_package.py` incorpora os três hashes ao pacote N3;
6. `forja_delivery.py` exige o audit no fechamento N2 de novas peças detectadas como resposta.

O adaptador `forja_headless.py` injeta o protocolo obrigatório em F3, F4 e F7 independentemente do prompt fornecido ao agente. A classificação de produto normaliza acentos e reconhece as classes usuais de resposta. Casos não aplicáveis exigem justificativa explícita; não basta omitir o artefato.

O modelo de confiança é conservador: descoberta ampla, confirmação por fonte oficial, tentativa de refutação independente e autorização humana para qualquer acusação externa ou pedido sancionatório. Especificação integral em `planejamento/09_AUDITORIA_ADVERSARIAL_PONTOS_DECISIVOS.md`.

---

## 15. Adendo técnico implementado — cânone editorial F7-B (15/07/2026)

A integração acima é aditiva ao desenho N2 histórico. O contrato vigente de F7 inclui `final_markdown`, `editorial_report`, `editorial_diff`, `fable5_usage` e `editorial_fidelity`; o contrato F8 exige `final_markdown` junto da trilha auditada. Para múltiplos textos, IDs e nomes usam sufixo seguro compartilhado, como `final_markdown_nota` e `audited_markdown_nota`, evitando associação por ordem ou nome aproximado.

Qualquer mudança material desejável identificada pelo editor deve permanecer em `duvidas` no relatório, sem entrar no texto. O limite semântico é de produto e não pode ser relaxado por prompt, retry ou decisão do modelo.
