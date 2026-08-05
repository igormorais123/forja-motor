---
phase: R6-validation
plan: P12
type: tdd
wave: 6
depends_on: [P07, P08]
files_modified:
  - src/forja/domain/gates/pipeline.py
  - src/forja/application/validate_case.py
  - forja_n4_validate.py
  - forja_pso_pet.py
  - forja_adversarial_audit.py
  - forja_reasoning.py
  - forja_consistency.py
  - test_forja_validation_pipeline.py
autonomous: true
requirements: [RF-REF-014, RF-REF-018, RNF-001, RNF-004, RNF-006]
---

<objective>Transformar agregadores extensos em pipeline explícito de validadores puros/contextuais sem relaxar severidades.</objective>

<feature><name>ValidationPipeline composto</name><behavior>Validadores executam em ordem declarada, acumulam findings, preservam exceções contextuais e calculam bloqueio por modo sem duplicar política.</behavior><implementation>Registro vindo do ArtifactCatalog, GateDecision tipado e fachadas nos validadores atuais.</implementation></feature>

<threat_model>Risco: decomposição remover recálculo independente ou mudar P0/P1. Golden reports e mutation tests sentinelas preservam comportamento; fail-open é proibido.</threat_model>

<tasks>
<task id="P12-RED" type="tdd"><read_first><file>forja_n4_validate.py</file><file>forja_pso_pet.py</file><file>forja_adversarial_audit.py</file></read_first><action>Criar golden tests por modo `off|shadow|pilot_blocking|default_on`, exceções contextuais, severidade/casing, aggregation e erro de validador; erro crítico deve bloquear.</action><acceptance_criteria><criterion>Relatórios atuais congelados para corpus.</criterion><criterion>Teste demonstra chave duplicada/branch ou comportamento difícil do agregador.</criterion></acceptance_criteria></task>
<task id="P12-GREEN" type="tdd"><read_first><file>test_forja_validation_pipeline.py</file><file>src/forja/domain/artifacts.py</file></read_first><action>Implementar pipeline e GateDecision; registrar validators via catálogo; erros críticos produzem finding bloqueante; manter recalculadores independentes de package/render.</action><acceptance_criteria><criterion>Todos os modos preservam política.</criterion><criterion>Validador órfão ou não registrado reprova teste.</criterion><criterion>P0 não é reduzido por exceção.</criterion></acceptance_criteria></task>
<task id="P12-REFACTOR" type="tdd"><read_first><file>src/forja/application/validate_case.py</file><file>forja_n4_validate.py</file></read_first><action>Converter agregadores atuais em fachadas; separar relatório/IO de regras puras; unificar enum de severidade.</action><acceptance_criteria><criterion>Biblioteca não chama sys.exit.</criterion><criterion>Zero ciclo e funções menores.</criterion></acceptance_criteria></task>
</tasks>

<verification>Golden reports, mutation/adversarial, N4 completa, F2-A, PSO e anti-autocertificação.</verification>
<success_criteria>Pipeline modular; severidades preservadas; falha crítica bloqueante; defesa em profundidade mantida.</success_criteria>
