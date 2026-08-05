---
phase: R6-cli-framework
plan: P13A
type: execute
wave: 6
depends_on: [P05, P06]
files_modified:
  - src/forja/cli.py
  - src/forja/commands/__init__.py
  - src/forja/commands/doctor.py
  - src/forja/commands/qa.py
  - src/forja/errors.py
  - test_forja_cli_contracts.py
autonomous: true
requirements: [RF-REF-005, RF-REF-017, RF-REF-018, RNF-007]
---

<objective>Estabilizar o framework da CLI, contratos, `doctor`, `qa` e exit codes sem migrar wrappers dependentes de serviços ainda instáveis.</objective>

<threat_model>Riscos: framework incorporar regra jurídica, biblioteca chamar SystemExit e contrato mascarar capacidade ausente. P13A toca somente a allowlist declarada e não expõe `validate|package|close|deliver`.</threat_model>

<tasks>
<task id="P13A-T1" type="execute"><read_first><file>.planning/refactor/baseline/CLI_CONTRACTS.json</file><file>.planning/codebase/ARCHITECTURE.md</file><file>src/forja/cli.py</file></read_first><action>Criar `test_forja_cli_contracts.py` parametrizado por contrato, cobrindo help, args, exit, stdout/stderr e efeitos em tempdir.</action><acceptance_criteria><criterion>Todo entrypoint possui teste ou exclusão justificada.</criterion><criterion>Testes não acionam envio/protocolo.</criterion></acceptance_criteria></task>
<task id="P13A-T2" type="execute"><read_first><file>test_forja_cli_contracts.py</file><file>src/forja/errors.py</file><file>forja_regua.py</file></read_first><action>Estabilizar registry e parsing para `doctor` e `qa`; mapear erros tipados para exit codes documentados; impedir alteração fora da allowlist do frontmatter.</action><acceptance_criteria><criterion>`forja --help`, `doctor` e `qa` passam.</criterion><criterion>Parsing não contém regra jurídica.</criterion><criterion>Bibliotecas não chamam SystemExit.</criterion><criterion>Diff fora da allowlist reprova.</criterion></acceptance_criteria></task>
</tasks>

<verification>Contratos do framework, allowlist de diff, secret scan de logs, suíte e execução em cwd diferentes.</verification>
<success_criteria>Framework estável e isolado; `doctor|qa` compatíveis; nenhum wrapper de serviço migrado cedo.</success_criteria>
