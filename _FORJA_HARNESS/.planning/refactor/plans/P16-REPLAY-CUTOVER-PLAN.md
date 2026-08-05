---
phase: R9-replay-cutover
plan: P16
type: execute
wave: 9
depends_on: [P15]
files_modified:
  - reports/refactor/
  - telemetria/refactor/
  - FORJA_SPEC_MANIFEST.json
  - FORJA_N3_CONFIG.json
  - docs/operations/ROLLBACK.md
autonomous: false
requirements: [RF-REF-021, RF-REF-022, RNF-001, RNF-002, RNF-014, RNF-015]
---

<objective>Provar equivalência real, ativar caminhos internos gradualmente e remover compatibilidade somente com evidência.</objective>

<threat_model>Riscos: falsa promoção N4, regressão em peça real, shim ainda usado, cutover sem rollback. Flags uma a uma, N4 permanece pilot_blocking e toda remoção exige checkpoint.</threat_model>

<tasks>
<task id="P16-T1" type="execute"><read_first><file>.planning/refactor/06-TESTES_ROLLBACK_E_CUTOVER.md</file><file>FORJA_SPEC_MANIFEST.json</file><file>FORJA_N3_CONFIG.json</file></read_first><action>Executar seis replays em cópias imutáveis; comparar evento, estado, pacote, gestão, DOCX/PDF e relatórios; registrar diferenças esperadas/inesperadas.</action><acceptance_criteria><criterion>Zero divergência inesperada.</criterion><criterion>Nenhum caso histórico é reescrito.</criterion></acceptance_criteria></task>
<task id="P16-T2" type="checkpoint"><read_first><file>reports/refactor/</file><file>planejamento/12_ROADMAP_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md</file></read_first><action>Somente para buscar G9B, executar três ciclos prospectivos reais quando houver demandas adequadas, mantendo N4 `pilot_blocking`; comprovar F2-A, regimento, Helena/Cícero, mutação, QA, entrega e rollback. A indisponibilidade desses ciclos não impede G9A.</action><acceptance_criteria><criterion>Três ciclos completos sem texto final preexistente como oráculo.</criterion><criterion>Mutação semântica ≥0,8 nas famílias aplicáveis ou bloqueio explícito.</criterion><criterion>Resultado é elegibilidade de promoção, não conclusão técnica retroativa.</criterion></acceptance_criteria></task>
<task id="P16-T3" type="execute"><read_first><file>telemetria/refactor/</file><file>MIGRATION_MANIFEST.json</file></read_first><action>Observar wrappers por janela definida; para cada candidato, provar zero uso, zero referência, suíte/replay verde e restore; solicitar aprovação antes de remover. Qualquer shim cuja segurança dependa de ciclos prospectivos permanece até G9B.</action><acceptance_criteria><criterion>Cada shim possui dossiê individual.</criterion><criterion>Uso detectado cancela remoção.</criterion><criterion>Compatibilidade dependente de G9B não é removida em G9A.</criterion></acceptance_criteria></task>
<task id="P16-T4" type="checkpoint"><read_first><file>FORJA_SPEC_MANIFEST.json</file><file>FORJA_N3_CONFIG.json</file><file>reports/refactor/</file></read_first><action>Separar conclusão da refatoração da decisão de promover N3/N4; atualizar manifest/config somente se critérios normativos próprios forem satisfeitos e houver autorização correspondente.</action><acceptance_criteria><criterion>Refatoração pode fechar sem promoção.</criterion><criterion>N4 não sai de pilot_blocking por inferência.</criterion></acceptance_criteria></task>
</tasks>

<verification>G9A exige seis replays, Word/PDF/telemetria, outbox, restore, secret scan e auditoria independente. G9B acrescenta três ciclos prospectivos e decisão normativa própria.</verification>
<success_criteria>G9A fecha tecnicamente R1 com compatibilidade preservada; G9B registra elegibilidade separada; remoção somente comprovada; zero promoção normativa implícita.</success_criteria>
