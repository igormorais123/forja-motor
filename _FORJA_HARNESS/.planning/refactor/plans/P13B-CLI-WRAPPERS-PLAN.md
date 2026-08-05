---
phase: R6-cli-wrappers
plan: P13B
type: execute
wave: 6
depends_on: [P09, P10, P11, P12, P13A]
files_modified:
  - src/forja/commands/run.py
  - src/forja/commands/validate.py
  - src/forja/commands/package.py
  - src/forja/commands/close.py
  - src/forja/commands/deliver.py
  - .planning/refactor/baseline/CLI_CONTRACTS.json
  - test_forja_cli_contracts.py
autonomous: true
requirements: [RF-REF-005, RF-REF-017, RF-REF-018, RF-REF-021, RNF-007, RNF-011]
---

<objective>Migrar wrappers antigos, um por vez, somente depois de os serviços de estado, entrega, gestão, render e validação estarem estabilizados.</objective>

<threat_model>Riscos: automação oculta depender de argumento/exit/stdout, arquivo compartilhado com outro owner e log expor dados. A allowlist nasce de `CLI_CONTRACTS.json`; um wrapper por tarefa/commit; qualquer diff externo bloqueia.</threat_model>

<tasks>
<task id="P13B-T1" type="execute"><read_first><file>.planning/refactor/baseline/CLI_CONTRACTS.json</file><file>test_forja_cli_contracts.py</file><file>src/forja/cli.py</file></read_first><action>Gerar allowlist explícita dos wrappers legados e mapear cada um a `run|validate|package|close|deliver`; excluir wrappers pertencentes a owner ainda ativo.</action><acceptance_criteria><criterion>Não existe wildcard em `files_modified`.</criterion><criterion>Cada wrapper tem serviço estabilizado e teste anterior.</criterion></acceptance_criteria></task>
<task id="P13B-T2" type="execute"><read_first><file>src/forja/commands/run.py</file><file>src/forja/commands/validate.py</file><file>src/forja/commands/package.py</file><file>src/forja/commands/close.py</file><file>src/forja/commands/deliver.py</file></read_first><action>Converter cada wrapper da allowlist em fachada fina, sequencialmente, preservando interface e emitindo telemetria local sem argumentos sensíveis.</action><acceptance_criteria><criterion>Contrato antigo e novo passa após cada wrapper.</criterion><criterion>Telemetria contém comando lógico/versão, não payload jurídico.</criterion><criterion>Alteração fora da allowlist reprova e interrompe o lote.</criterion></acceptance_criteria></task>
</tasks>

<verification>Contratos de todos os CLIs, diff contra allowlist, secret scan de logs, suíte, replay de efeitos e execução em cwd diferentes.</verification>
<success_criteria>Subcomandos de serviço estáveis; wrappers compatíveis e observáveis; owners não compartilham arquivos em paralelo.</success_criteria>
