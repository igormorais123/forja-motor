---
phase: R5-management
plan: P10
type: tdd
wave: 5
depends_on: [P08]
files_modified:
  - src/forja/ports/management.py
  - src/forja/application/sync_management.py
  - src/forja/adapters/management_sidecar/outbox.py
  - forja_management_bridge.py
  - forja_reconcile.py
  - forja_fila.py
  - test_forja_management_outbox.py
  - test_forja_n3_management.py
autonomous: true
requirements: [RF-REF-012, RF-REF-018, RNF-004, RNF-011]
---

<objective>Desacoplar gestão da transação do caso por outbox idempotente e preservar precedência de evidência.</objective>

<feature><name>ManagementOutbox file-first</name><behavior>Evento do caso persiste mesmo com gestão indisponível; retry sincroniza exatamente uma vez; evidência de entrega vence snapshot atrasado.</behavior><implementation>Outbox persistente com idempotencyKey, estados pending/delivered/failed_retryable e adaptador sidecar.</implementation></feature>

<threat_model>Riscos: perda/duplicação de status, falsa conclusão e exposição de conversa. Payload mínimo e sanitizado; demanda não conclui por draft.</threat_model>

<tasks>
<task id="P10-RED" type="tdd"><read_first><file>forja_management_bridge.py</file><file>forja_reconcile.py</file><file>test_forja_n3_management.py</file></read_first><action>Criar testes de pane antes/depois do enqueue, retry, ack perdido, duplicidade e precedência de entrega comprovada; corrigir expectativa desatualizada do conflito.</action><acceptance_criteria><criterion>Teste atual desatualizado é documentado como mudança esperada.</criterion><criterion>Pelo menos um cenário demonstra acoplamento atual.</criterion></acceptance_criteria></task>
<task id="P10-GREEN" type="tdd"><read_first><file>test_forja_management_outbox.py</file><file>forja_management_bridge.py</file></read_first><action>Implementar outbox atômica, enqueue na aplicação, flush separado, ack idempotente e payload com caseId/demandId/eventId/status/links sem conversa bruta.</action><acceptance_criteria><criterion>Pane mantém item pending.</criterion><criterion>Retry gera um sidecar lógico.</criterion><criterion>Draft não conclui demanda.</criterion></acceptance_criteria></task>
<task id="P10-REFACTOR" type="tdd"><read_first><file>src/forja/application/sync_management.py</file><file>forja_fila.py</file></read_first><action>Substituir imports dinâmicos por porta/adaptador; manter bridge atual como wrapper e telemetria sanitizada.</action><acceptance_criteria><criterion>Transação do caso não importa scripts da gestão.</criterion><criterion>Wrapper mantém contratos atuais.</criterion></acceptance_criteria></task>
</tasks>

<verification>Falhas/retries, sidecar real em diretório temporário, testes de gestão e scanner de privacidade.</verification>
<success_criteria>Gestão desacoplada; sync uma vez; precedência correta; gate G5 aprovado.</success_criteria>
