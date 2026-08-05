---
phase: R6-render
plan: P11
type: tdd
wave: 6
depends_on: [P06, P07]
files_modified:
  - src/forja/ports/renderer.py
  - src/forja/adapters/word_medina/renderer.py
  - src/forja/rendering/model.py
  - src/forja/rendering/parser.py
  - forja_visual.py
  - forja_render_docx.py
  - forja_visual_qa.py
  - forja_qa_paginas.py
  - test_forja_render_pipeline.py
autonomous: true
requirements: [RF-REF-013, RF-REF-014, RNF-006, RNF-010, RNF-013]
---

<objective>Decompor renderização em parser, modelo, composição, Word e QA sem regressão visual ou factual.</objective>

<feature><name>DocumentRenderer com QA independente</name><behavior>Input estruturado produz DOCX/PDF/recibos rastreáveis; capacidade ausente, render falho e QA bloqueado são estados diferentes; compositor não se autoaprova.</behavior><implementation>Modelo intermediário testável e adaptador Word/Medina preservando template, EMF e PDF via COM.</implementation></feature>

<threat_model>Riscos: omitir texto/tabela, substituir EMF por raster, metadata errada ou autoaprovação. Comparação estrutural e inspeção de todas as páginas são bloqueantes.</threat_model>

<tasks>
<task id="P11-RED" type="tdd"><read_first><file>forja_visual.py</file><file>forja_render_docx.py</file><file>forja_visual_qa.py</file><file>../_FERRAMENTAS/word_visual_pipeline.py</file></read_first><action>Criar testes de caracterização de parsing, blocos, títulos, tabelas, placeholders, metadata, runId e capacidades; congelar outputs reais representativos sem reescrever históricos.</action><acceptance_criteria><criterion>Testes cobrem hotspots e defeitos Natura/CORSAN/Libra/Patrícia.</criterion><criterion>Golden estrutural existe antes da extração.</criterion></acceptance_criteria></task>
<task id="P11-GREEN" type="tdd"><read_first><file>test_forja_render_pipeline.py</file><file>../_FERRAMENTAS/PADRAO_WORD_MEDINA_OSORIO.md</file></read_first><action>Implementar parser/modelo/porta/adaptador; manter template, SVG→EMF, Word COM, PDF, metadados Medina e ledger de todas as páginas; separar producerRunId de reviewerRunId.</action><acceptance_criteria><criterion>Core/parser roda sem Word.</criterion><criterion>Adaptador real produz EMF vetorial e PDF via Word.</criterion><criterion>Todas as páginas possuem QA independente.</criterion></acceptance_criteria></task>
<task id="P11-REFACTOR" type="tdd"><read_first><file>src/forja/adapters/word_medina/renderer.py</file><file>forja_visual.py</file><file>forja_render_docx.py</file></read_first><action>Reduzir funções grandes a orquestradores/fachadas; manter CLIs e outputs compatíveis; registrar diferenças visuais intencionais como bloqueadores até aprovação.</action><acceptance_criteria><criterion>Hotspots diminuem sem nova função equivalente gigante.</criterion><criterion>Wrappers mantêm assinatura e exit codes.</criterion></acceptance_criteria></task>
</tasks>

<verification>Unidade/parser, integração fake, Word COM real, EMF, PDF, metadata, render/inspeção de todas as páginas e fidelity MD/DOCX/PDF.</verification>
<success_criteria>Pipeline modular, visualmente equivalente, sem autocertificação e com gate real.</success_criteria>
