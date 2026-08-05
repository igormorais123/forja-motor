---
phase: R1-trust-shield
plan: P01
type: tdd
wave: 1
depends_on: [P00]
files_modified:
  - FORJA_TEST_SUITES.json
  - forja_regua.py
  - validate_forja_n3.py
  - test_forja_citacoes.py
  - test_forja_verificador.py
  - test_forja_regua.py
  - test_forja_test_discovery.py
autonomous: true
requirements: [RF-REF-002, RF-REF-022, RNF-008]
---

<objective>
Garantir que a régua descubra e classifique todos os testes e nunca produza falso verde por omissão.
</objective>

<feature>
  <name>Descoberta canônica e manifesto completo de suítes</name>
  <behavior>Todo `test_*.py` deve pertencer a exatamente uma ou mais camadas declaradas; arquivo órfão ou inexistente no manifesto reprova antes da execução.</behavior>
  <implementation>Manifesto JSON único consumido pelos dois runners, com relatório de executados, omitidos e razões.</implementation>
</feature>

<threat_model>
Risco: marcar teste como executado sem executá-lo, ocultar teste real caro ou coletar código com efeito colateral. O manifesto é validado contra o filesystem e o runner grava comandos/resultados reais.
</threat_model>

<tasks>
<task id="P01-RED" type="tdd">
  <read_first><file>forja_regua.py</file><file>validate_forja_n3.py</file><file>test_forja_citacoes.py</file><file>test_forja_verificador.py</file></read_first>
  <action>Criar `test_forja_test_discovery.py` que adiciona fixture sintética órfã e exige falha; reproduzir a falha de coleta causada por `sys.stdout` alterado no import; afirmar que os 35 testes observados estão cobertos.</action>
  <acceptance_criteria><criterion>O teste novo falha antes da implementação pelo motivo `unclassified test`.</criterion><criterion>A falha de stdout é demonstrada sem deixar estado global persistente.</criterion></acceptance_criteria>
</task>
<task id="P01-GREEN" type="tdd">
  <read_first><file>test_forja_test_discovery.py</file><file>forja_regua.py</file><file>validate_forja_n3.py</file></read_first>
  <action>Criar `FORJA_TEST_SUITES.json` com camadas `unit`, `contract`, `integration`, `mutation`, `real`, `word`, `remote`; fazer ambos os runners consumirem a mesma fonte; mover redirecionamento de stdout para contexto de execução, nunca import.</action>
  <acceptance_criteria><criterion>Todo `test_*.py` possui classificação.</criterion><criterion>Arquivo órfão retorna exit code não zero.</criterion><criterion>Relatório distingue omitido por capacidade de não descoberto.</criterion></acceptance_criteria>
</task>
<task id="P01-REFACTOR" type="tdd">
  <read_first><file>FORJA_TEST_SUITES.json</file><file>test_forja_regua.py</file></read_first>
  <action>Eliminar listas duplicadas de suítes; preservar flags atuais como fachadas e adicionar teste que compara filesystem, manifesto e comandos efetivamente executados.</action>
  <acceptance_criteria><criterion>Existe uma única lista canônica de arquivos.</criterion><criterion>Runners antigos mantêm interface e exit codes.</criterion></acceptance_criteria>
</task>
</tasks>

<verification>
Executar teste de descoberta isolado, coleta global, suíte rápida e validação N3; verificar que a bateria real não é alegada quando omitida.
</verification>

<success_criteria>
- 100% dos testes classificados;
- coleta global estável;
- falso verde por omissão impossível;
- commits RED e GREEN em ordem.
</success_criteria>
