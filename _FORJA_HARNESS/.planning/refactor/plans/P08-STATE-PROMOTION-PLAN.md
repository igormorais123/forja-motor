---
phase: R4-state-promotion
plan: P08
type: tdd
wave: 4
depends_on: [P06, P07]
files_modified:
  - src/forja/application/promote_attempt.py
  - src/forja/ports/event_store.py
  - src/forja/ports/case_repository.py
  - src/forja/adapters/filesystem/event_store.py
  - forja_run.py
  - forja_state_machine.py
  - forja_headless.py
  - test_forja_promotion_transaction.py
  - test_forja_replay_equivalence.py
autonomous: true
requirements: [RF-REF-008, RF-REF-009, RF-REF-010, RNF-002, RNF-004, RNF-005]
---

<objective>Unificar resolução e tornar promoção de attempts transacional, revalidada e recuperável.</objective>

<feature><name>Promoção atômica com replay compatível</name><behavior>Contexto/contrato/inputs divergentes ou falha em qualquer fronteira impedem publicação canônica; eventos históricos continuam reproduzíveis.</behavior><implementation>PromotionPlan validado, unidade file-first, recibo/evento final único e resolvedor 0/1/N.</implementation></feature>

<threat_model>Risco crítico: estado parcial, case errado ou reinterpretação histórica. Fault injection e expectedRevision bloqueiam efeitos ambíguos.</threat_model>

<tasks>
<task id="P08-RED" type="tdd">
  <read_first><file>forja_run.py</file><file>forja_state_machine.py</file><file>forja_headless.py</file></read_first>
  <action>Criar testes para contextHash/contractHash/input alterados, 0/1/N cases, concorrência, falhas antes/depois da cópia, validação N4 e append; congelar replay de eventos históricos.</action>
  <acceptance_criteria><criterion>Ao menos um cenário atual deixa parcialidade ou falta revalidação.</criterion><criterion>Golden replay existe antes do GREEN.</criterion></acceptance_criteria>
</task>
<task id="P08-GREEN" type="tdd">
  <read_first><file>test_forja_promotion_transaction.py</file><file>test_forja_replay_equivalence.py</file></read_first>
  <action>Implementar resolvedor estrito, PromotionPlan, revalidação final, staging/commit atômico e evento/recibo após sucesso; falha preserva attempt bloqueado sem ponteiro canônico.</action>
  <acceptance_criteria><criterion>Todos os fault points deixam estado permitido.</criterion><criterion>Múltiplos cases produzem AmbiguousCaseError.</criterion><criterion>Writer antigo falha por revision conflict.</criterion></acceptance_criteria>
</task>
<task id="P08-REFACTOR" type="tdd">
  <read_first><file>src/forja/application/promote_attempt.py</file><file>forja_run.py</file></read_first>
  <action>Reduzir `forja_run.promote_attempt` a fachada/orquestrador; registrar `resolvedAt/resolvedBy` em evento versionado sem reescrever histórico.</action>
  <acceptance_criteria><criterion>Replay antigo permanece idêntico.</criterion><criterion>Evento novo possui versão e reducer explícito.</criterion></acceptance_criteria>
</task>
</tasks>

<verification>Fault injection completo, concorrência, replay histórico, retomada após interrupção e suíte package/N4.</verification>
<success_criteria>Zero parcialidade; resolvedor inequívoco; replay compatível; gate G4 aprovado.</success_criteria>
