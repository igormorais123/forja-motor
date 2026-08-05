# Contrato de tarefa — Integração FORJA + TeiaJus

```yaml
contract:
  id: integracao-forja-teiajus
  date: 2026-07-12
  agent: codex

  objective: |
    Permitir que a FORJA Harness consulte e comande, por contrato JSON estável,
    os recursos do Sistema de Busca Jurídica sem execução arbitrária, sem copiar
    o banco e preservando proveniência, telemetria e gates jurídicos existentes.

  required_outputs:
    - kind: file
      path: ../Sistema de Busca Jurídica/teiajus/src/teiajus/agent_api.py
    - kind: file
      path: _FORJA_HARNESS/forja_legal_search.py
    - kind: file
      path: _FORJA_HARNESS/FORJA_SEARCH_CONFIG.json
    - kind: test_pass
      command: python -m pytest tests -q
    - kind: test_pass
      command: python -m pytest _FORJA_HARNESS/test_forja_legal_search.py -q

  evidence_of_completion:
    - command: python _FORJA_HARNESS/forja_legal_search.py capabilities
      expected_exit: 0
      expected_stdout_contains: search_cases
    - command: python _FORJA_HARNESS/forja_legal_search.py search --limit 1
      expected_exit: 0
      expected_stdout_contains: requestId
    - artifact: _FORJA_HARNESS/telemetria/legal_search/
      check: requisição e resposta sanitizadas, duração, status e hashes

  budget:
    max_attempts: 3
    max_wall_clock_min: 90

  permissions:
    read:
      - _FORJA_HARNESS/**
      - ../Sistema de Busca Jurídica/teiajus/**
    write:
      - _FORJA_HARNESS/forja_legal_search.py
      - _FORJA_HARNESS/FORJA_SEARCH_CONFIG.json
      - _FORJA_HARNESS/test_forja_legal_search.py
      - _FORJA_HARNESS/contracts/INTEGRACAO_TEIAJUS_2026-07-12.md
      - _FORJA_HARNESS/telemetria/legal_search/**
      - _FORJA_HARNESS/DOCUMENTACAO_TECNICA.md
      - _FORJA_HARNESS/INDICE_FORJA.md
      - ../Sistema de Busca Jurídica/teiajus/src/teiajus/agent_api.py
      - ../Sistema de Busca Jurídica/teiajus/tests/test_agent_api.py
      - ../Sistema de Busca Jurídica/teiajus/README.md
    forbidden:
      - ../Sistema de Busca Jurídica/teiajus/teiajus.db
      - ../Sistema de Busca Jurídica/teiajus/auditoria/**
      - _FORJA_HARNESS/state/**
      - '**/.secrets/**'
    network: true
    install_packages: false

  stop_criteria:
    success: todos os testes passam e a FORJA executa capabilities, health e busca real
    blocked: três falhas consecutivas com a mesma causa ou regressão não isolável
    escalate_to_igor:
      - custo externo novo
      - exposição pública de segredo
      - mudança destrutiva no banco existente

  expected_failures:
    - mode: dependency_or_path_drift
      symptom: projeto TeiaJus ou Python não localizado
      action: falhar fechado com diagnóstico e sem fallback silencioso
    - mode: external_source_unavailable
      symptom: DataJud ou tribunal indisponível
      action: registrar telemetria e preservar banco/artefatos parciais
    - mode: schema_validation_error
      symptom: pedido ou resposta fora do contrato JSON
      action: rejeitar antes da execução e testar o caso de regressão

  trace:
    log_path: _FORJA_HARNESS/telemetria/legal_search/<requestId>.json
    capture: [request_sanitized, response_summary, command, exit_code, duration_ms, hashes]
```

