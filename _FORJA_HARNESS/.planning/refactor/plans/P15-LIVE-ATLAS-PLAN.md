---
phase: R8-live-atlas
plan: P15
type: execute
wave: 8
depends_on: [P14]
files_modified:
  - docs/architecture/
  - docs/decisions/
  - docs/operations/
  - tools/generate_architecture_atlas.py
  - tests/test_architecture_atlas.py
  - .planning/codebase/
autonomous: true
requirements: [RF-REF-019, RF-REF-020, RNF-005, RNF-013]
---

<objective>Criar atlas vivo, matriz de impacto e navegação segura para humanos e IAs.</objective>

<threat_model>Risco: documentação bonita ficar desatualizada ou incluir segredos/outputs. Gerador usa AST/catálogos e allowlist de metadados, ignorando var/archive/foreign.</threat_model>

<tasks>
<task id="P15-T1" type="execute"><read_first><file>.planning/refactor/04-DIAGRAMAS_REFATORACAO_FORJA.md</file><file>.planning/codebase/CHANGE_IMPACT.md</file><file>src/forja/domain/artifacts.py</file></read_first><action>Implementar gerador/verificador para imports, catálogos, fases, artefatos, testes e ownership; produzir Mermaid determinístico sem conteúdo de casos.</action><acceptance_criteria><criterion>Alteração estrutural sem regeneração reprova teste.</criterion><criterion>Gerador ignora var/archive/foreign.</criterion></acceptance_criteria></task>
<task id="P15-T2" type="execute"><read_first><file>.planning/codebase/README.md</file><file>.planning/refactor/05-MATRIZ_RASTREABILIDADE.md</file></read_first><action>Separar docs de arquitetura, ADRs, operações e changelog; criar índice de onboarding e matriz `alterar X → módulos → testes → docs → rollback`.</action><acceptance_criteria><criterion>Cada domínio tem owner, input/output, fonte, invariantes, consumidores, testes e rollback.</criterion><criterion>Todos os links internos resolvem.</criterion></acceptance_criteria></task>
<task id="P15-T3" type="execute"><read_first><file>tools/generate_architecture_atlas.py</file><file>docs/architecture/</file></read_first><action>Renderizar todo Mermaid, validar legibilidade mínima e gerar PDF técnico atualizado por Word COM/EMF com QA de todas as páginas.</action><acceptance_criteria><criterion>100% dos blocos Mermaid renderiza.</criterion><criterion>PDF não possui texto de diagrama abaixo de 8 pt.</criterion><criterion>Todas as páginas inspecionadas.</criterion></acceptance_criteria></task>
</tasks>

<verification>Teste de drift, links, secret scan, mmdc, PDF/PNG page QA e onboarding por agente novo em modo leitura.</verification>
<success_criteria>Atlas ligado ao código; IA navega com segurança; documentação legível e atualizável.</success_criteria>
