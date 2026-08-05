# 19 — Plano de instalação das melhorias mapeadas na FORJA

> Data: 12/07/2026. Origem: estudo completo do harness (sessão 12/07, três agentes de exploração
> sobre código, planejamento e telemetria) + veredito sobre o middleware paperclip.
> Status: PLANO APROVADO PARA EXECUÇÃO POR ORDEM DO IGOR (12/07). Implementação por milestone,
> cada milestone fecha com testes verdes + registro em RETROSPECTIVAS.md se gerar lição.
>
> Escopo negativo (rejeições já registradas — NÃO reabrir sem fato novo): RAG/GraphRAG,
> LLM-as-judge, firewall de saída dedicado, controles de sigilo/credencial/quarentena
> inexequíveis (bronca 10/07), migração da FORJA para o paperclip (decisão 12/07 — o
> paperclip é middleware de sessão do Claude Code, não plataforma de pipeline; importamos
> dele apenas o padrão LocalContext, ver M1.2).

## Sumário das lacunas e mapeamento para milestones

| # | Lacuna (estudo 12/07) | Severidade | Milestone |
|---|---|---|---|
| 1 | Mutação semântica não implementada (bloqueia critério 3 de promoção N4) | Crítica | M3.1 |
| 2 | Zero ciclos prospectivos N4 (bloqueia critérios 1 e 10) | Crítica | M3.3 (processo) |
| 3 | Pareceres Helena/Cícero pós-blueprint, não pré-redação (ordem Igor 09/07) | Crítica | M2.1 |
| 4 | Sem alerta proativo de P0 (gate cai e ninguém sabe) | Alta | M1.1 |
| 5 | Sem dashboard em tempo real | Alta | ELIMINADO (decisão Igor 12/07 — projeto visual 3D descartado; não reabrir) |
| 6 | Ledger de citações materiais incompleto (lição 52) | Alta | M3.2 |
| 7 | F8 QA visual ~40% automatizado; F2 classificação manual | Média | M4.2 / M4.3 |
| 8 | N3 travado em sombra (6 casos bloqueados no gate V2) | Média | M3.3 (mesmos ciclos destravam) |
| 9 | Sem histórico de bloqueadores resolvidos; sem tendência de gates | Média | M1.3 |
| 10 | `forja_run.py` sem suite de teste dedicada | Média | M4.1 |
| 11 | Contexto da fila invisível ao abrir sessão (agente precisa varrer `state/`) | Média | M1.2 |
| 12 | Corpus antifraude pequeno (variância operacional não medida) | Baixa | M3.3 (subproduto) |

Ordem de execução: **M1 → M2 → M3 → M4**. M1 e M2 são baratos e de efeito imediato;
M3 é o caminho crítico da promoção N4; M4 é robustez contínua.

---

## M1 — Observabilidade e contexto (estimativa: 6-8h)

### M1.1 Alerta proativo de P0 (2-3h)

Problema: quando um gate derruba um caso (P0 em `blockers[]` / `gates[]`), o estado registra
e o processo para com exit 2 — mas nenhum humano é avisado. Um P0 pode ficar horas invisível.

Implementação:
- Novo módulo `forja_alertas.py` com função única `notificar_p0(case_id, gate, motivo, severidade)`.
- Canal: ponte Hermes já existente (`forja_management_bridge.py` fala com o painel;
  o Hermes já tem canal WhatsApp/telefone — reutilizar `integrations.phoneAlert`/`hermesBridge`
  que o `FORJA_STATE.json` já rastreia). Fallback se a ponte estiver offline: escrever em
  `state/<caseId>/ALERTAS_PENDENTES.jsonl` e o próximo `sync_forja_gestao.py` drena.
- Pontos de disparo (todos já existem, é só chamar a função): `forja_verificador.py`
  (quando classifica P0), `forja_delivery.py` (elo bloqueante reprova, exit 2),
  `forja_render_docx.py` (gate embutido reprova).
- Anti-ruído: deduplicação por `(caseId, gate)` com janela de 6h — o mesmo P0 não
  notifica duas vezes; resolução do bloqueador emite uma única notificação de "resolvido".

Critério de aceite: teste `test_forja_alertas.py` com padrão DEVE_PEGAR/NÃO_PODE_TRAVAR —
P0 novo notifica; P0 repetido em 6h não notifica; P1 não notifica; ponte offline não quebra
o pipeline (fail-open, alerta vai para o JSONL).

### M1.2 LocalContext da FORJA (hook de sessão) (1-2h)

Único empréstimo do paperclip. Script `forja_local_context.py` (na raiz do harness) que:
- Varre `state/*/FORJA_STATE.json` e imprime resumo de 5-10 linhas: casos com
  `status != fulfilled`, fase atual de cada um, P0/P1 abertos, idade do último evento.
- Registrado em `.claude/settings.json` do projeto (SessionStart, matcher no cwd desta
  pasta), timeout 5s, fail-open (erro nunca bloqueia a sessão) — mesmo contrato do
  `local_context.py` do paperclip.

Critério de aceite: abrir sessão nesta pasta injeta o resumo; com `state/` vazio ou
JSON corrompido, injeta aviso e não quebra.

### M1.3 Histórico de bloqueadores + tendência de gates (3h)

- Estender o registro de bloqueador com `resolvedAt` e `resolvedBy` (preencher quando o
  gate reavaliar como verde; hoje o snapshot só tem o estado atual). Compatibilidade:
  campo novo opcional, casos antigos continuam válidos — nenhuma migração.
- Novo script `forja_metricas_gates.py`: varre todos os `FORJA_STATE.json` +
  `FORJA_EVENTS.jsonl` e agrega: frequência de queda por gate, tempo médio por fase,
  tempo médio de resolução de P0, casos por estado. Saída: `reports/METRICAS_GATES.json`
  + tabela markdown. Este JSON também alimenta o painel.

Critério de aceite: rodar sobre os 30+ casos históricos sem erro; relatório aponta o
gate que mais caiu (validação manual em 3 casos conhecidos: Patrícia, Libra Sul, Cafelana).

---

## M2 — Ordem dos pareceres Helena/Cícero (estimativa: 3-4h)

### M2.1 Pareceres ANTES da redação (ordem do Igor 09/07, lição 62)

Estado atual: gate G5.7 bloqueia a entrega sem `F4_PARECER_HELENA.md` e
`F4_PARECER_CICERO.md`, mas o fluxo real produz os pareceres depois do blueprint e às
vezes em paralelo à redação. A exigência é: **blueprint pronto → pareceres → só então F6**.

Implementação:
- No contrato de fase F6 (`phase_contracts/`): pré-condição nova — os dois pareceres
  existem E têm `mtime`/evento anterior ao primeiro artefato de redação (`F6_MINUTA_MD.md`).
  No event store N3, verificar por sequência de eventos (parecer registrado antes de
  `phase_started(F6)`), que é mais confiável que mtime.
- No `forja_delivery.py`, elo 10: além de exigir presença (já existe), exigir a ordem —
  reprovação vira P0 `PARECER_POS_REDACAO` com mensagem clara.
- Transição: casos com F6 já iniciado antes de 12/07 são aceitos com a regra antiga
  (mesmo padrão de transição usado nos formatos legados de metadados). Casos novos, regra nova.
- Cada parecer mantém o formato atual (recomendações numeradas + decisão do redator
  acatada/rejeitada/por quê no relatório de melhorias).

Critério de aceite: teste com caso sintético — parecer depois da minuta reprova com o
P0 novo; parecer antes aprova; caso legado (F6 anterior a 12/07) não trava.

---

## M3 — Caminho crítico da promoção N4 (estimativa: 20-30h + casos reais)

### M3.1 Mutação semântica (12-16h) — maior lacuna técnica

Objetivo: `semanticMutationScore >= 80%` (critério 3 de promoção). Hoje só existe mutação
literal (remover/inserir texto exigido); falta detectar que a peça mutada **mudou de sentido
jurídico** e o pipeline não percebeu.

Implementação em `forja_mutation_semantic.py`, com tipologia por família de risco
(derivada das lições 49 e da taxonomia de citação de 6 modos):

| Operador | O que muta | O gate que DEVE pegar |
|---|---|---|
| S1 inversão de tese | "é cabível" → "não é cabível" na proposição decisiva | tabela de lastro (U6) / F7 |
| S2 troca de parte | autor↔réu, agravante↔agravado em trecho decisivo | consistência (forja_consistency) |
| S3 troca de valor/data | valor da causa, data de intimação, prazo | aritmética de datas (G do verificador) |
| S4 troca de pedido | pedido principal substituído por subsidiário | árvore de questões (forja_reasoning) |
| S5 sobreabstração | proposição específica vira genérica sem lastro | cobertura/proposições (forja_context) |
| S6 deturpação de precedente | ratio→dictum, tese do julgado invertida | ledger de citações (M3.2) |

- Motor: aplicar cada operador sobre os 3 casos-baseline (Patrícia, Libra Sul, Saúde),
  rodar o pipeline de validação N4 completo e medir quantas mutações são bloqueadas.
  Score = bloqueadas/aplicadas por família. Mutações são geradas por regra determinística
  (regex/AST do markdown estruturado) SEMPRE que possível; onde exigir reescrita
  (S5, S6), o texto mutado é fixo no corpus (curado uma vez, versionado), não gerado
  a cada run — reprodutibilidade acima de cobertura.
- Corpus versionado em `n4_schemas/corpus_mutacao_semantica/` com o mesmo padrão do
  corpus literal (mutações + controles benignos que NÃO podem travar).
- Integração: `forja_n4_validate.py` passa a reportar `semanticMutationScore` ao lado
  do literal; `forja_n4_anti_fraud_audit.py` consome os dois.

Critério de aceite: score computado e reprodutível nos 3 baselines; cada operador com
≥2 mutações e ≥1 controle benigno; famílias abaixo de 80% viram pendência nominada
(não silenciosa) no JSON de validação.

### M3.2 Ledger de citações materiais (6-8h) — lição 52

Estrutura por peça: afirmação material decisiva → fonte primária → trecho/localizador →
alcance e ressalva. Distinto do registro físico de fontes (`source_registry`), que só prova
integridade de arquivo.

- Novo artefato `F5_LEDGER_MATERIAL.json` gerado em F5 e completado em F7: para cada uma
  das 10-15 proposições decisivas (a tabela de lastro U6 já as lista), campos
  `{proposicao, fontePrimaria, localizador, trecho, alcance, ressalva, verificadoEm}`.
- `forja_citations.py` ganha exportador que cruza o checklist de citações com a tabela
  de lastro; o que ficar sem fonte primária vira P1 nominado no F7 (não P0 — a régua
  de bloqueio continua sendo a citação inexistente/deturpada, modos 1-6).
- O relatório de melhorias passa a embutir a tabela do ledger (hoje a tabela de lastro é
  manual; o ledger a torna verificável).

Critério de aceite: gerar o ledger retroativo para 1 caso-baseline; teste de regressão
com proposição sem fonte → P1 aparece; proposição lastreada → silêncio.

### M3.3 Três ciclos prospectivos (processo, não código — 2h de preparação)

A promoção N4 e o destravamento do N3 dependem de 3 ciclos NOVOS (classes/tribunais
distintos) com congelamento anterior à redação. Isso não se implementa — se executa
quando as próximas demandas reais chegarem. O que o plano instala:

- `RUNBOOK_CICLO_PROSPECTIVO.md` (raiz): checklist de 1 página — congelar árvore de
  questões e blueprint ANTES da redação (hash registrado no event store), rodar o caso
  em `pilot_blocking`, colher os 10 critérios de promoção ao final, registrar no
  `FORJA_CASE_MANIFEST.json` o par (`mode`, `promotionEligible`).
- Regra de seleção: próximas 3 demandas reais de classes distintas entram automaticamente
  no piloto, salvo urgência declarada pelo Igor (aí a demanda roda N2 e não conta).
- Cada ciclo prospectivo alimenta o corpus antifraude (lacuna 12) sem trabalho extra:
  os artefatos congelados viram casos de teste.

Critério de aceite: runbook escrito; primeiro caso novo que chegar após M2 entra no
piloto e produz os artefatos do checklist.

---

## M4 — Robustez contínua (estimativa: 8-12h, paralelizável)

### M4.1 Suite de teste para `forja_run.py` (3-4h)
Executor de fases N3 roda em sombra sem teste dedicado. Criar `test_forja_run.py`:
transições válidas F0→F10, fase inválida rejeitada, contrato ausente falha com mensagem
clara, replay idempotente (mesma sequência de eventos → mesmo estado), P0 interrompe.

### M4.2 F8 — ampliar QA visual automático (3-4h)
Hoje ~40%: detecta sobreposição/corte/truncamento. Adicionar checagens determinísticas
baratas já validadas nos kits (`medina_svg_kit`): fonte mínima impressa (<8pt reprova),
largura de inserção vs `largura_recomendada_cm`, contraste texto/fundo abaixo do limiar,
página com densidade anômala (heurística de pixels não-brancos fora da faixa das páginas
vizinhas — pega diagrama estourado que só o zoom pegava). O que continuar manual
(estratégia visual, hierarquia) permanece manual — sem teatro de automação.

### M4.3 F2 — classificação assistida (2-3h)
Schema `FORJA_PRODUCT_CLASSIFICATION.json` validado automaticamente (tipo de peça ∈ enum,
tribunal coerente com o CNJ do processo — regra do segmento já documentada no protocolo,
perfil PSO-Pet ∈ {leve, completo, intensivo}). A decisão continua do agente; o schema
só impede classificação incompleta de seguir para F3.

---

## Cronograma e dependências

```
Semana 1: M1.1 → M1.2 → M1.3 → M2.1          (efeito imediato; ~10h)
Semana 2-3: M3.1 (mutação semântica) ‖ M3.2 (ledger)   (~20h)
Contínuo: M3.3 conforme demandas reais chegarem (3 ciclos ≈ 2-4 semanas de calendário)
Paralelo/encaixe: M4.1-M4.3 (~10h)
```

Regras transversais de execução (valem para todo milestone):
1. Toda mudança no pipeline roda `test_forja_verificador.py`, `test_licao41.py` e
   `test_real_telemetria_licao41.py` antes de ser declarada pronta.
2. Nenhum gate novo entra sem par DEVE_PEGAR/NÃO_PODE_TRAVAR no teste.
3. Nenhum controle inexequível ou fora de domínio (política registrada 10/07).
4. Lição nova → RETROSPECTIVAS.md; mudança de spec → FORJA_SPEC_MANIFEST.json e
   DOCUMENTACAO_TECNICA.md no mesmo commit.
5. Fila propõe, humano dispara: nada deste plano protocola ou envia peça sozinho.
