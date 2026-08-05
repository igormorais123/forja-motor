---
phase: R3-core
plan: P06
type: tdd
wave: 3
depends_on: [P05]
files_modified:
  - src/forja/core/json_io.py
  - src/forja/core/hashing.py
  - src/forja/core/locking.py
  - src/forja/core/paths.py
  - src/forja/core/time.py
  - src/forja/core/ids.py
  - src/forja/core/errors.py
  - forja_n3_common.py
  - test_forja_core_compatibility.py
autonomous: true
requirements: [RF-REF-005, RF-REF-008, RF-REF-018, RNF-005, RNF-006]
---

<objective>Extrair primitives neutras preservando integralmente a API observável de `forja_n3_common.py`.</objective>

<feature><name>Fachada compatível para primitives core</name><behavior>IO, hash, lock, path, tempo e IDs mantêm resultados/erros do baseline, com resultados tipados novos por baixo.</behavior><implementation>Mover uma primitive por commit e reexportar do módulo antigo.</implementation></feature>

<threat_model>Riscos: mudar hash, atomicidade, timeout/stale, timezone ou path confinement. Golden tests congelam cada invariante antes da extração.</threat_model>

<tasks>
<task id="P06-RED" type="tdd">
  <read_first><file>forja_n3_common.py</file><file>forja_state_machine.py</file><file>forja_run.py</file></read_first>
  <action>Criar golden tests para JSON ausente/inválido/default, escrita atômica interrompida, path escape, lock timeout/stale, timestamp timezone-aware, IDs e hash canônico.</action>
  <acceptance_criteria><criterion>Testes capturam valores e exceções atuais.</criterion><criterion>Fault injection prova que arquivo parcial não é visível.</criterion></acceptance_criteria>
</task>
<task id="P06-GREEN" type="tdd">
  <read_first><file>test_forja_core_compatibility.py</file><file>forja_n3_common.py</file></read_first>
  <action>Implementar módulos `src/forja/core` e fazer `forja_n3_common.py` reexportar os mesmos símbolos; nenhuma assinatura pública é removida.</action>
  <acceptance_criteria><criterion>Imports antigos e novos passam.</criterion><criterion>Golden hashes e locks permanecem idênticos.</criterion><criterion>Path escape continua rejeitado.</criterion></acceptance_criteria>
</task>
<task id="P06-REFACTOR" type="tdd">
  <read_first><file>src/forja/core/errors.py</file><file>forja_n3_common.py</file></read_first>
  <action>Consolidar helpers repetidos de JSON/tempo/collections/IDs onde houver teste; manter facade sem lógica nova e registrar telemetria de import apenas se não afetar startup.</action>
  <acceptance_criteria><criterion>Clones alvo removidos ou delegam ao core.</criterion><criterion>Zero ciclo de import.</criterion></acceptance_criteria>
</task>
</tasks>

<verification>Suíte core, state machine, run/package, replay de fixture e análise de imports.</verification>
<success_criteria>Primitives modulares; fachada compatível; invariantes de atomicidade/hashing/locking preservados.</success_criteria>
