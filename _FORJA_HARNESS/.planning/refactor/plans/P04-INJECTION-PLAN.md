---
phase: R1-trust-shield
plan: P04
type: tdd
wave: 1
depends_on: [P00]
files_modified:
  - forja_injection_scan.py
  - test_forja_injection.py
autonomous: true
requirements: [RF-REF-003, RF-REF-018, RNF-004, RNF-012]
---

<objective>
Fazer o scanner registrar e bloquear todo material que não conseguiu examinar, sem tratar conteúdo externo como comando.
</objective>

<feature>
  <name>Injection scan exaustivo e fail-closed</name>
  <behavior>Cada input recebe `scanned_clean`, `requires_review` ou `unscanned`; erro/limite/formato nunca desaparece nem retorna sucesso global.</behavior>
  <implementation>`ScanResult` tipado, adaptadores por formato e exit code derivado da cobertura.</implementation>
</feature>

<threat_model>Riscos: entrada maliciosa não analisada ser aceita; citação acadêmica benigna gerar falso bloqueio. Separar sinal técnico de linguagem imperativa contextual.</threat_model>

<tasks>
<task id="P04-RED" type="tdd">
  <read_first><file>forja_injection_scan.py</file><file>test_forja_injection.py</file><file>planejamento/10_PRD_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md</file></read_first>
  <action>Adicionar testes para exceção do parser, PDF acima do limite, arquivo ilegível/não suportado e frase acadêmica imperativa benigna.</action>
  <acceptance_criteria><criterion>Os três inputs não examinados demonstram o fail-open atual.</criterion><criterion>Controle benigno não é tratado como comando.</criterion></acceptance_criteria>
</task>
<task id="P04-GREEN" type="tdd">
  <read_first><file>test_forja_injection.py</file><file>forja_injection_scan.py</file></read_first>
  <action>Inventariar todos os inputs antes do parse; em erro/limite/formato produzir `unscanned` P0 com razão; exit não zero se qualquer item não foi examinado; preservar triagem humana para sinais técnicos.</action>
  <acceptance_criteria><criterion>Contagem de resultados igual à contagem de inputs.</criterion><criterion>Todo `unscanned` bloqueia.</criterion><criterion>Benigno continua não bloqueante.</criterion></acceptance_criteria>
</task>
<task id="P04-REFACTOR" type="tdd">
  <read_first><file>forja_injection_scan.py</file></read_first>
  <action>Separar enumeração, adaptadores, detecção e política; sanitizar erros sem conteúdo sensível.</action>
  <acceptance_criteria><criterion>Falha de um arquivo não omite os demais.</criterion><criterion>Relatório não contém segredo ou instrução executada.</criterion></acceptance_criteria>
</task>
</tasks>

<verification>Executar poison/benign suite, arquivo grande sintético e scanner de segredos no relatório.</verification>
<success_criteria>Cobertura exaustiva; fail-closed; conteúdo externo permanece dado.</success_criteria>
