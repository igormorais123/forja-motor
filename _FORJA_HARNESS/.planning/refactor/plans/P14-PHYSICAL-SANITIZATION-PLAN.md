---
phase: R7-physical-sanitization
plan: P14
type: execute
wave: 7
depends_on: [P09, P10, P11, P12, P13B]
files_modified:
  - tests/
  - tools/
  - experiments/n4/
  - migrations/
  - archive/
  - var/
  - FORJA_TEST_SUITES.json
  - REPOSITORY_LAYOUT.md
  - MIGRATION_MANIFEST.json
autonomous: false
requirements: [RF-REF-015, RF-REF-016, RF-REF-021, RNF-003, RNF-014]
---

<objective>Separar código, testes, ferramentas, experimentos, histórico e outputs sem perda ou quebra de automação.</objective>

<threat_model>Risco crítico de apagar estado, segredo, evidência, skill ativa ou projeto útil. Movimentos seguem manifesto/hash; exclusões exigem checkpoint humano e restore testado.</threat_model>

<tasks>
<task id="P14-T1" type="execute"><read_first><file>.planning/codebase/STRUCTURE.md</file><file>.planning/refactor/baseline/BASELINE_MANIFEST.json</file></read_first><action>Produzir `MIGRATION_MANIFEST.json` item a item com origem, destino, hash, classe, consumidor, wrapper, backup, restore e recomendação `manter|mover|arquivar|excluir_depois`.</action><acceptance_criteria><criterion>Todo item movido aparece no manifesto.</criterion><criterion>Nenhum `state`, evento, contrato ou evidence recebe `excluir_depois`.</criterion></acceptance_criteria></task>
<task id="P14-T2A" type="execute"><read_first><file>MIGRATION_MANIFEST.json</file><file>FORJA_TEST_SUITES.json</file><file>test_forja_cli_contracts.py</file></read_first><action>Mover somente fontes auxiliares, testes e ferramentas por micro-lotes; atualizar `FORJA_TEST_SUITES.json`, runners, imports, configs, subprocessos e links; manter wrappers de path no local antigo.</action><acceptance_criteria><criterion>Cada micro-lote passa descoberta canônica, contratos e imports antes do próximo.</criterion><criterion>Zero teste órfão/path inexistente.</criterion><criterion>Runtime ativo não é tocado neste lote.</criterion></acceptance_criteria></task>
<task id="P14-T2B" type="execute"><read_first><file>MIGRATION_MANIFEST.json</file><file>.planning/codebase/STRUCTURE.md</file></read_first><action>Mover experimentos e histórico somente após prova de ausência de consumidor runtime; manter índice/ponte no local anterior e comparar hashes.</action><acceptance_criteria><criterion>Busca de referências e telemetria não encontra consumidor ativo.</criterion><criterion>Índice histórico resolve todos os destinos.</criterion><criterion>Restore de amostra reproduz hashes.</criterion></acceptance_criteria></task>
<task id="P14-T2C" type="checkpoint"><read_first><file>MIGRATION_MANIFEST.json</file><file>FORJA_N3_CONFIG.json</file><file>.planning/refactor/baseline/BASELINE_MANIFEST.json</file></read_first><action>Antes de mover qualquer raiz mutável (`state`, cache, telemetria, reports, renders ou `var`), apresentar mapa macro→micro, backup, restore, consumidores e estratégia dual-read/single-write. Prosseguir somente com checkpoint explícito; após cada raiz, provar retomada do runtime e rollback.</action><acceptance_criteria><criterion>Checkpoint identifica cada raiz ativa.</criterion><criterion>Dual-read/single-write ou compatibilidade equivalente está testada.</criterion><criterion>Smoke tests, replay e restore passam após cada raiz.</criterion></acceptance_criteria></task>
<task id="P14-T3" type="execute"><read_first><file>MIGRATION_MANIFEST.json</file><file>.planning/codebase/STRUCTURE.md</file></read_first><action>Aplicar o limite de domínio já decidido: FocoEdital não pertence à FORJA. Não importar, recriar, indexar nem tratar cópia residual como subprojeto visual. Se uma cópia reaparecer no harness, registrar origem e hashes e encaminhar sua remoção do escopo por procedimento auditável, sem fundir conteúdo com o projeto canônico.</action><acceptance_criteria><criterion>Nenhum caminho interno da FORJA referencia FocoEdital como componente.</criterion><criterion>Documentação identifica o limite de domínio e o projeto canônico externo.</criterion><criterion>Qualquer resíduo é classificado como estrangeiro, não como fonte FORJA.</criterion></acceptance_criteria></task>
<task id="P14-T4" type="execute"><read_first><file>MIGRATION_MANIFEST.json</file><file>../.gitignore</file><file>FORJA_TEST_SUITES.json</file></read_first><action>Documentar retenção de cache/telemetria/reports/renders; impedir que buscas/imports de runtime percorram var/archive/foreign; gerar `REPOSITORY_LAYOUT.md` e revalidar todos os caminhos declarados.</action><acceptance_criteria><criterion>Busca arquitetural ignora outputs.</criterion><criterion>Política informa backup, retenção e limpeza.</criterion><criterion>Manifesto de testes não possui órfão ou path antigo sem wrapper.</criterion></acceptance_criteria></task>
</tasks>

<physical_state_update date="2026-07-16">
O acervo visual pesado foi retirado do harness e arquivado em `C:\Users\IgorPC\.claude\projects\Forja visual 3d`. O arquivo externo não é dependência runtime. FocoEdital não pertence à FORJA: a cópia acidental e seus documentos foram removidos do arquivo visual; a duplicata foi eliminada após backup privado e restauração verificados no `MIGRATION_MANIFEST.json`. O caminho antigo não existe mais e não deve ser recriado.
</physical_state_update>

<verification>Manifest/hash antes/depois, descoberta canônica, suíte completa, CLIs, links, subprocessos, smoke de runtime, secret scan e restore de amostra por classe e por raiz ativa.</verification>
<success_criteria>Árvore navegável; zero perda; wrappers ativos; nenhuma exclusão sem aprovação.</success_criteria>
