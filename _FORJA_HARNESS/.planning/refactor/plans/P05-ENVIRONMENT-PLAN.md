---
phase: R2-reproducibility
plan: P05
type: execute
wave: 2
depends_on: [P01, P02, P03, P04]
files_modified:
  - pyproject.toml
  - uv.lock
  - src/forja/__init__.py
  - src/forja/cli.py
  - forja_capabilities.py
  - test_forja_capabilities.py
autonomous: true
requirements: [RF-REF-004, RF-REF-005, RF-REF-018, RNF-006, RNF-008, RNF-010]
---

<objective>
Criar ambiente reproduzível e esqueleto modular sem mover ainda o runtime atual.
</objective>

<threat_model>Risco: lock incompatível com Word/Windows ou instalação global mascarar dependência ausente. Validar em ambiente limpo e separar grupos opcionais.</threat_model>

<tasks>
<task id="P05-T1" type="execute">
  <read_first><file>.planning/codebase/STACK.md</file><file>validate_forja_n3.py</file><file>forja_regua.py</file></read_first>
  <action>Criar `pyproject.toml` com `src` layout, Python suportado, dependências core e extras `word`, `visual`, `science`, `dev`; configurar pytest, Ruff e typing gradual; gerar `uv.lock`.</action>
  <acceptance_criteria><criterion>Build/install limpo funciona.</criterion><criterion>Core não exige Word ou ciência.</criterion><criterion>Lock é reproduzível.</criterion></acceptance_criteria>
</task>
<task id="P05-T2" type="execute">
  <read_first><file>FORJA_N3_CONFIG.json</file><file>forja_render_docx.py</file><file>forja_visual.py</file></read_first>
  <action>Criar `forja_capabilities.py` que detecta Python, Word COM, template, Inkscape, Mermaid, Graphviz e dependências opcionais, retornando `available|missing|degraded` sem executar entrega.</action>
  <acceptance_criteria><criterion>Capacidade ausente não é reportada como disponível.</criterion><criterion>Teste usa fakes e roda sem Word.</criterion></acceptance_criteria>
</task>
<task id="P05-T3" type="execute">
  <read_first><file>forja_headless.py</file><file>forja_run.py</file><file>forja_regua.py</file></read_first>
  <action>Criar esqueleto `src/forja` e entrypoint `forja` apenas com `doctor` e `qa`; scripts existentes permanecem fonte funcional e wrappers não são removidos.</action>
  <acceptance_criteria><criterion>`forja doctor` e `forja qa --help` funcionam.</criterion><criterion>Todos os comandos antigos continuam executando testes de contrato.</criterion></acceptance_criteria>
</task>
</tasks>

<verification>Instalar a partir do lock em ambiente limpo; executar suíte não-real, doctor e contratos de CLI; comparar baseline Ruff sem autofix.</verification>
<success_criteria>Ambiente reproduzível; extras isolados; zero comando antigo quebrado; gate G2 aprovado.</success_criteria>
