---
phase: R1-trust-shield
plan: P03
type: tdd
wave: 1
depends_on: [P00]
files_modified:
  - forja_citations.py
  - test_forja_citations_source_verification.py
  - test_forja_citacoes.py
autonomous: true
requirements: [RF-REF-003, RF-REF-018, RNF-001, RNF-004]
---

<objective>
Impedir que presença nominal de número em arquivo autocertifique jurisprudência para uso final.
</objective>

<feature>
  <name>Pipeline explícito de verificação de fonte</name>
  <behavior>`candidate → identity_verified → content_verified → final_use_allowed`; saltos e identidade divergente são rejeitados.</behavior>
  <implementation>Separar detecção, identidade, literalidade e política de uso mantendo ledger compatível.</implementation>
</feature>

<threat_model>Risco: citar decisão errada ou atribuir frase a autoridade incorreta. Fonte indisponível nunca vira inexistência nem aprovação.</threat_model>

<tasks>
<task id="P03-RED" type="tdd">
  <read_first><file>forja_citations.py</file><file>test_forja_citacoes.py</file><file>planejamento/06_GATES_QUALIDADE_FORJA.md</file></read_first>
  <action>Criar negativos: número só no filename, ocorrência genérica em texto, tribunal/classe divergente, trecho literal ausente, fonte revogada; controles com fonte oficial e trecho correspondente.</action>
  <acceptance_criteria><criterion>O caminho atual que define `finalUseAllowed=True` apenas por presença local é reproduzido como falha.</criterion><criterion>Controles oficiais passam.</criterion></acceptance_criteria>
</task>
<task id="P03-GREEN" type="tdd">
  <read_first><file>test_forja_citations_source_verification.py</file><file>forja_citations.py</file></read_first>
  <action>Adicionar estados explícitos e exigir identidade + conteúdo + política para `finalUseAllowed`; indisponibilidade retorna `unverified`; revogação remove autorização sem apagar histórico.</action>
  <acceptance_criteria><criterion>Nenhum candidato salta para uso final.</criterion><criterion>Ledger mantém fonte, localizador, hash, estado e razão.</criterion></acceptance_criteria>
</task>
<task id="P03-REFACTOR" type="tdd">
  <read_first><file>forja_citations.py</file><file>forja_n4_validate.py</file></read_first>
  <action>Extrair funções puras de identidade/literalidade/política e manter contrato atual por wrapper; conectar N4 ao estado explícito sem relaxar gates.</action>
  <acceptance_criteria><criterion>Taxonomia de seis falhas continua coberta.</criterion><criterion>Formato histórico permanece legível.</criterion></acceptance_criteria>
</task>
</tasks>

<verification>Executar regressões de veneno, controles benignos, F7 e auditoria adversarial; confirmar zero fonte autocertificada.</verification>
<success_criteria>Uso final somente com identidade e literalidade; estados auditáveis; nenhum falso “não existe”.</success_criteria>
