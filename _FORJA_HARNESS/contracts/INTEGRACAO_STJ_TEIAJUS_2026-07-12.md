# Contrato de tarefa — STJ no TeiaJus e na ponte FORJA

```yaml
contract:
  id: integracao-stj-forja-teiajus
  date: 2026-07-12
  agent: codex

  objective: |
    Tornar o STJ uma fonte de primeira classe do Sistema de Busca Jurídica e
    disponibilizar suas capacidades à FORJA por contrato JSON auditável, com
    proveniência oficial, distinção entre metadado público e inteiro teor,
    telemetria, testes reais, documentação e falha fechada.

  required_outputs:
    - kind: file
      path: ../Sistema de Busca Jurídica/teiajus/src/teiajus/connectors/stj.py
    - kind: file
      path: ../Sistema de Busca Jurídica/teiajus/tests/test_stj.py
    - kind: diff
      path: ../Sistema de Busca Jurídica/teiajus/src/teiajus/agent_api.py
    - kind: diff
      path: _FORJA_HARNESS/forja_legal_search.py
    - kind: test_pass
      command: python -m pytest tests -q
    - kind: test_pass
      command: python -m pytest _FORJA_HARNESS/test_forja_legal_search.py -q

  evidence_of_completion:
    - command: python _FORJA_HARNESS/forja_legal_search.py capabilities
      expected_exit: 0
      expected_stdout_contains: STJ
    - command: python _FORJA_HARNESS/forja_legal_search.py stj-search --limit 1
      expected_exit: 0
      expected_stdout_contains: requestId
    - artifact: _FORJA_HARNESS/telemetria/legal_search/
      check: requisição, resposta, fonte, duração, status e hashes

  permissions:
    read:
      - _FORJA_HARNESS/**
      - ../Sistema de Busca Jurídica/**
    write:
      - _FORJA_HARNESS/forja_legal_search.py
      - _FORJA_HARNESS/FORJA_SEARCH_CONFIG.json
      - _FORJA_HARNESS/test_forja_legal_search.py
      - _FORJA_HARNESS/contracts/INTEGRACAO_STJ_TEIAJUS_2026-07-12.md
      - _FORJA_HARNESS/telemetria/legal_search/**
      - _FORJA_HARNESS/reports/AUDITORIA_INTEGRACAO_STJ_2026-07-12.md
      - _FORJA_HARNESS/DOCUMENTACAO_TECNICA.md
      - _FORJA_HARNESS/INDICE_FORJA.md
      - ../Sistema de Busca Jurídica/teiajus/src/teiajus/connectors/stj.py
      - ../Sistema de Busca Jurídica/teiajus/src/teiajus/agent_api.py
      - ../Sistema de Busca Jurídica/teiajus/src/teiajus/__main__.py
      - ../Sistema de Busca Jurídica/teiajus/tests/test_stj.py
      - ../Sistema de Busca Jurídica/teiajus/tests/test_agent_api.py
      - ../Sistema de Busca Jurídica/teiajus/README.md
      - ../Sistema de Busca Jurídica/ESTADO_HARNESS.md
      - ../Sistema de Busca Jurídica/CAPACIDADES_ATUAIS.md
      - ../Sistema de Busca Jurídica/MAPA_IA.md
      - ../Sistema de Busca Jurídica/pontos para continuar.txt
      - ../Sistema de Busca Jurídica/teiajus/OPERACAO_STJ.md
      - ../Sistema de Busca Jurídica/planejamento/*.md
    forbidden:
      - ../Sistema de Busca Jurídica/teiajus/teiajus.db
      - ../Sistema de Busca Jurídica/teiajus/auditoria/**
      - _FORJA_HARNESS/state/**
      - '**/.secrets/**'
    network: true
    install_packages: false

  stop_criteria:
    success: testes passam e pelo menos uma capacidade STJ oficial responde com telemetria
    blocked: três falhas consecutivas da mesma rota oficial sem alternativa pública segura
    escalate_to_igor:
      - custo externo novo
      - certificado ou login pessoal necessário
      - mudança destrutiva no banco real

  expected_failures:
    - mode: official_route_changed
      symptom: endpoint STJ retorna HTML inesperado, 403 ou schema diferente
      action: falhar fechado, preservar trace e usar somente rota oficial validada
    - mode: authenticated_content_required
      symptom: metadado público disponível, inteiro teor exige login ou certificado
      action: registrar limite e não inferir conteúdo
    - mode: source_attribution_failure
      symptom: resultado sem URL, identificador ou hash de proveniência
      action: não promover a evidência para F5

  trace:
    log_path: _FORJA_HARNESS/telemetria/legal_search/<requestId>.json
    capture: [request_sanitized, response_summary, official_url, exit_code, duration_ms, hashes]
```
