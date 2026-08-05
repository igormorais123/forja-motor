---
phase: R5-delivery
plan: P09
type: tdd
wave: 5
depends_on: [P08]
files_modified:
  - src/forja/application/build_package.py
  - src/forja/application/close_cycle.py
  - src/forja/ports/delivery.py
  - src/forja/adapters/legacy_n2/delivery.py
  - forja_delivery.py
  - forja_package.py
  - forja_close_cycle.py
  - forja_delivery_integrity.py
  - test_forja_delivery_identity.py
autonomous: true
requirements: [RF-REF-011, RF-REF-013, RNF-002, RNF-004]
---

<objective>Selecionar e fechar entrega exclusivamente por identidade auditada e hash.</objective>

<feature><name>Entrega por artifactId + sha256</name><behavior>Dois candidatos nunca geram escolha silenciosa; hash divergente bloqueia; retry reutiliza receipt e draft não conclui demanda.</behavior><implementation>Serviço único de pacote/fechamento, com adaptador heurístico legado explícito.</implementation></feature>

<threat_model>Risco jurídico/operacional: enviar versão errada ou considerar draft como entrega. A identidade do pacote é imutável e vinculada à evidência.</threat_model>

<tasks>
<task id="P09-RED" type="tdd"><read_first><file>forja_delivery.py</file><file>forja_package.py</file><file>forja_delivery_integrity.py</file></read_first><action>Criar casos com dois DOCX, filename enganoso, hash alterado após QA, retry e draft sem evidência.</action><acceptance_criteria><criterion>Primeiro-glob atual é reproduzido como falha.</criterion><criterion>Draft não é aceito como cumprimento.</criterion></acceptance_criteria></task>
<task id="P09-GREEN" type="tdd"><read_first><file>test_forja_delivery_identity.py</file><file>forja_close_cycle.py</file></read_first><action>Implementar seleção por ID/hash, AuditedPackage, DeliveryDraft e DeliveryReceipt; adaptador glob retorna ambiguidade; receipt usa idempotencyKey.</action><acceptance_criteria><criterion>Hash auditado igual ao entregue.</criterion><criterion>Retry não duplica receipt/draft.</criterion><criterion>Dois candidatos bloqueiam.</criterion></acceptance_criteria></task>
<task id="P09-REFACTOR" type="tdd"><read_first><file>src/forja/application/build_package.py</file><file>forja_delivery.py</file></read_first><action>Fazer package/close/integrity reutilizarem serviço sem remover recálculo independente dos gates.</action><acceptance_criteria><criterion>Uma regra de seleção canônica.</criterion><criterion>Gates continuam recalculados em fronteiras independentes.</criterion></acceptance_criteria></task>
</tasks>

<verification>Suíte package/delivery, hash tamper, idempotência e caso real controlado sem envio externo.</verification>
<success_criteria>Arquivo exato; evidência vinculada; sem escolha heurística silenciosa.</success_criteria>
