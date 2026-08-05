---
phase: R0-baseline
plan: P00
type: execute
wave: 0
depends_on: []
files_modified:
  - .planning/refactor/baseline/BASELINE_MANIFEST.json
  - .planning/refactor/baseline/RESTORE_RUNBOOK.md
  - .planning/refactor/baseline/CLI_CONTRACTS.json
autonomous: true
requirements: [RF-REF-001, RF-REF-016, RNF-003, RNF-014]
---

<objective>
Criar um baseline isolado, reproduzível e restaurável antes de qualquer alteração funcional.
</objective>

<threat_model>
Riscos: sobrescrever trabalho existente, copiar segredo para relatório, backup incompleto e restore não testado. Controles: worktree separado, inventário sanitizado, hashes, backup privado e restauração em diretório temporário.
</threat_model>

<tasks>
<task id="P00-T1" type="execute">
  <read_first>
    <file>../AGENTS.md</file>
    <file>FORJA_SPEC_MANIFEST.json</file>
    <file>FORJA_N3_CONFIG.json</file>
    <file>.planning/refactor/00-CONTEXT.md</file>
  </read_first>
  <action>Criar branch/worktree `codex/forja-r1-refactor` a partir de `codeSourceCommit`; copiar somente o pacote `.planning/refactor` usando `PLANNING_PACKAGE_HASHES.json`, verificar 100% dos hashes e registrar se o bootstrap veio de snapshot não rastreado ou de `planningCommit`. Nunca copiar o restante do workspace sujo.</action>
  <acceptance_criteria>
    <criterion>O worktree resolve para caminho distinto do workspace operacional.</criterion>
    <criterion>`git rev-parse HEAD` no worktree é igual a `codeSourceCommit`.</criterion>
    <criterion>O pacote de planejamento existe no worktree e todos os hashes conferem antes de qualquer plano subsequente.</criterion>
    <criterion>O workspace original não recebe alteração.</criterion>
  </acceptance_criteria>
</task>
<task id="P00-T2" type="execute">
  <read_first>
    <file>.planning/codebase/STRUCTURE.md</file>
    <file>.planning/codebase/TESTING.md</file>
    <file>.planning/codebase/INTEGRATIONS.md</file>
  </read_first>
  <action>Gerar `BASELINE_MANIFEST.json` com inventário de Python, testes, contratos, schemas, configs, CLIs, integrações, arquivos protegidos, hashes, tamanhos e classificação `source|contract|mutable|historical|foreign-copy`.</action>
  <acceptance_criteria>
    <criterion>JSON válido contém `codeSourceCommit`, `planningSnapshotHash`, `generatedAt`, `protectedFiles`, `testFiles`, `cliEntrypoints` e `mutableRoots`.</criterion>
    <criterion>Nenhum valor do manifesto corresponde a padrão de token/senha.</criterion>
  </acceptance_criteria>
</task>
<task id="P00-T3" type="execute">
  <read_first>
    <file>forja_regua.py</file>
    <file>validate_forja_n3.py</file>
    <file>forja_run.py</file>
    <file>forja_delivery.py</file>
  </read_first>
  <action>Caracterizar comandos atuais em `CLI_CONTRACTS.json`: argumentos, exit code, stdout/stderr sanitizados, arquivos lidos/escritos e capacidades externas. Executar somente comandos não mutáveis ou sobre fixtures temporárias.</action>
  <acceptance_criteria>
    <criterion>Todo entrypoint Python detectado possui registro ou justificativa de exclusão.</criterion>
    <criterion>Contrato identifica claramente comandos reais/Word/remotos.</criterion>
  </acceptance_criteria>
</task>
<task id="P00-T4" type="execute">
  <read_first>
    <file>FORJA_SPEC_MANIFEST.json</file>
    <file>.planning/refactor/06-TESTES_ROLLBACK_E_CUTOVER.md</file>
  </read_first>
  <action>Criar backup privado dos arquivos protegidos e `RESTORE_RUNBOOK.md`; restaurar em diretório temporário, comparar hashes e apagar somente a cópia temporária após a prova.</action>
  <acceptance_criteria>
    <criterion>Restore temporário reproduz 100% dos hashes protegidos.</criterion>
    <criterion>Runbook responde onde está o backup, como restaurar e o que não está coberto.</criterion>
  </acceptance_criteria>
</task>
</tasks>

<verification>
- validar JSON dos manifests;
- executar scanner de segredos nos relatórios;
- comparar status/timestamps do workspace original;
- anexar log do restore com contagens e hashes.
</verification>

<success_criteria>
- baseline reproduzível;
- backup e restore comprovados;
- zero alteração funcional ou perda de trabalho;
- gate G0 aprovado.
</success_criteria>
