---
phase: R1-trust-shield
plan: P02
type: tdd
wave: 1
depends_on: [P00]
files_modified:
  - forja_sources.py
  - forja_f2_check.py
  - forja_tribunals.py
  - test_forja_sources_strict.py
autonomous: true
requirements: [RF-REF-003, RF-REF-006, RNF-001, RNF-004]
---

<objective>
Tornar o gate de regimento inequivocamente fail-closed e unificar o catálogo de tribunais.
</objective>

<feature>
  <name>Verificação estrita de regimento</name>
  <behavior>Somente um regimento do tribunal correto, dentro do escopo do caso, integral e com fonte/versão/download/emendas permite avanço.</behavior>
  <implementation>Resultado tipado `verified|missing|ambiguous|incomplete|stale|wrong_tribunal` e catálogo único `forja_tribunals.py`.</implementation>
</feature>

<threat_model>
Risco jurídico crítico: selecionar primeiro arquivo de outro caso ou degradar falta material para P1. Qualquer ambiguidade, erro ou ausência é bloqueante.
</threat_model>

<tasks>
<task id="P02-RED" type="tdd">
  <read_first><file>forja_sources.py</file><file>forja_f2_check.py</file><file>../AGENTS.md</file></read_first>
  <action>Criar casos negativos para ausência, fora da pasta, dois candidatos, texto curto, metadados ausentes, emendas ausentes e tribunal divergente; criar controle benigno completo.</action>
  <acceptance_criteria><criterion>Ao menos um caso atual demonstra liberação indevida antes do GREEN.</criterion><criterion>Controle benigno não bloqueia.</criterion></acceptance_criteria>
</task>
<task id="P02-GREEN" type="tdd">
  <read_first><file>test_forja_sources_strict.py</file><file>forja_sources.py</file></read_first>
  <action>Implementar resolvedor estrito no escopo do caso e uma fachada compatível `forja_tribunals.py` como fonte provisória única de CNJ/tribunal; decisão bloqueante para todo resultado diferente de `verified`; exigir `../_LEIS_GERAIS` quando aplicável. P07 migrará a implementação para o domínio sem reabrir a divergência já corrigida.</action>
  <acceptance_criteria><criterion>Todos os negativos produzem P0/blocked.</criterion><criterion>F2 e F3 importam o mesmo catálogo.</criterion><criterion>Nenhum `rglob` global decide o primeiro resultado.</criterion></acceptance_criteria>
</task>
<task id="P02-REFACTOR" type="tdd">
  <read_first><file>forja_tribunals.py</file><file>forja_sources.py</file></read_first>
  <action>Separar descoberta, validação de metadados e política de liberação; manter CLI/artefatos atuais compatíveis e documentar `forja_tribunals.py` como fachada provisória para P07.</action>
  <acceptance_criteria><criterion>Funções puras podem ser testadas sem filesystem real.</criterion><criterion>Formato existente do mapa F3 continua legível.</criterion></acceptance_criteria>
</task>
</tasks>

<verification>Executar negativos/benignos, suíte F2/F3 e caso-piloto sobre cópia; revisar relatório sem mencionar proveniência operacional na peça.</verification>
<success_criteria>Somente `verified` avança; catálogo único; P0 jurídico fechado.</success_criteria>
