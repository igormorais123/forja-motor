---
phase: R3-catalogs
plan: P07
type: tdd
wave: 3
depends_on: [P02, P05]
files_modified:
  - src/forja/domain/tribunals.py
  - src/forja/domain/phases.py
  - src/forja/domain/artifacts.py
  - src/forja/domain/severity.py
  - src/forja/domain/release_policy.py
  - forja_n4_common.py
  - forja_n4_validate.py
  - forja_n4_invalidation.py
  - generate_n4_contracts.py
  - test_forja_catalogs.py
autonomous: true
requirements: [RF-REF-006, RF-REF-007, RF-REF-022, RNF-005, RNF-006]
---

<objective>Criar fontes canônicas tipadas e eliminar drift de tribunais, fases, artefatos, severidade e geração.</objective>

<feature><name>Catálogos completos e geração sem drift</name><behavior>Todo item possui metadados obrigatórios; derivados são gerados/verificados; definição órfã/duplicada reprova.</behavior><implementation>Catálogos em domain com fachadas nos módulos antigos e `generate_n4_contracts.py --check`.</implementation></feature>

<threat_model>Risco: catálogo novo omitir exceção contextual ou colapsar contratos vigente/candidato. Teste de cobertura e separação por specVersion são bloqueantes.</threat_model>

<tasks>
<task id="P07-RED" type="tdd">
  <read_first><file>forja_n4_common.py</file><file>forja_n4_validate.py</file><file>forja_n4_invalidation.py</file><file>generate_n4_contracts.py</file><file>forja_f2_check.py</file><file>forja_sources.py</file></read_first>
  <action>Criar golden de compatibilidade da fachada `forja_tribunals.py`; testes devem falhar se F2/F3 e o novo domínio divergirem, se artefato estiver sem schema/phase/validator/flag/policy, se severidade for desconhecida, se houver dependência órfã ou drift após geração.</action>
  <acceptance_criteria><criterion>Golden congela o catálogo já corrigido em P02, sem exigir reintrodução da divergência antiga.</criterion><criterion>Teste detecta edição manual em schema gerado.</criterion></acceptance_criteria>
</task>
<task id="P07-GREEN" type="tdd">
  <read_first><file>test_forja_catalogs.py</file><file>FORJA_SPEC_MANIFEST.json</file><file>FORJA_N3_CONFIG.json</file></read_first>
  <action>Migrar a implementação provisória de `forja_tribunals.py` para `src/forja/domain/tribunals.py`, mantendo a primeira como fachada; implementar os demais catálogos tipados, gerar índices/derivados e adicionar `--check` sem escrita; manter contratos atuais e N4 em namespaces/versionamentos separados.</action>
  <acceptance_criteria><criterion>F2, F3 e a fachada apontam ao mesmo catálogo de domínio.</criterion><criterion>100% de artefatos cobertos.</criterion><criterion>`--check` retorna 0 sem drift e não altera mtime.</criterion><criterion>F2-A preserva protocolo e compatibilidade.</criterion></acceptance_criteria>
</task>
<task id="P07-REFACTOR" type="tdd">
  <read_first><file>src/forja/domain/artifacts.py</file><file>forja_n4_validate.py</file></read_first>
  <action>Fazer módulos antigos delegarem aos catálogos; registrar validadores contextuais explicitamente; manter recálculo independente dos gates.</action>
  <acceptance_criteria><criterion>Não existem listas paralelas manuais para o mesmo atributo.</criterion><criterion>Exceções contextuais têm teste nominal.</criterion></acceptance_criteria>
</task>
</tasks>

<verification>Testes de catálogo, schemas, contratos, F2-A, N4 agregada e duas execuções de geração comparadas.</verification>
<success_criteria>Uma fonte por conceito; derivados determinísticos; contratos históricos preservados; gate G3 aprovado.</success_criteria>
