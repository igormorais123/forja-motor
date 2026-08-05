# Auditoria da integração FORJA ↔ TeiaJus ↔ STJ

**Data:** 12/07/2026  
**Auditor:** harness-engineering  
**Alvo:** `_FORJA_HARNESS/forja_legal_search.py` + `teiajus.connectors.stj`

## Resultado

```yaml
score:
  pass: 7
  flag: 1
  block: 0
```

| # | Estado | Evidência | Conclusão |
|---|---|---|---|
| 1. Contrato | FLAG | `contracts/INTEGRACAO_STJ_TEIAJUS_2026-07-12.md` | completo, mas arquivos novos ainda não estão versionados em commit |
| 2. Estado persistente | PASS | `FORJA_SEARCH_CONFIG.json`, `CAPACIDADES_ATUAIS.md`, telemetria | retomada independe da conversa |
| 3. Verificação real | PASS | `tests/test_stj.py`, suíte completa e três chamadas oficiais | teste executável e fonte real |
| 4. Traces brutos | PASS | `telemetria/legal_search/` + artefatos F5 | request, status, duração, hashes e resposta preservados |
| 5. Assumptions | PASS | `FORJA_SEARCH_CONFIG.json > stj.assumptions` | schema CKAN e gap JSON×ZIP têm condição de expiração |
| 6. Regras em código | PASS | allowlist, limite 30 MiB, hash, `textGaps`, flag de mutação | falha fechada não depende de prompt |
| 7. Esforço calibrado | PASS | conector determinístico, sem LLM | rede e parsing apenas; revisão jurídica permanece F5/F7 |
| 8. Índice | PASS | `INDICE_FORJA.md`, `MAPA_IA.md`, `OPERACAO_STJ.md` | documentação profunda fora do índice curto |

## Testes reais

- `stj_health`: `ready`; 10/10 órgãos com recurso `20260531`; Diário com metadado `20260710`.
- `stj_search`: 3 acórdãos de improbidade retornados; recurso oficial SHA-256
  `61a9c96fbb7dc6073e64142de8db41ed094652a0dee967c3ed97b9969cbca300`.
- `stj_daily_decisions`: íntegra obtida; hash do texto
  `600b41d6ef6bf34df481191f7c8349991dea1d1311d50e9045558d611a59e95d`.
- Lote diário auditado: 396 metadados, 337 textos no ZIP; o primeiro gap foi
  registrado e a busca continuou até uma íntegra válida.
- `stj_datajud_preview`: `ReadTimeout` após retentativas de 5 segundos; fonte
  externa degradada, sem processo órfão e sem escrita no banco principal.

## Aperfeiçoamento derivado da falha real

Antes, um `SeqDocumento` sem TXT derrubava toda a consulta. Depois, a lacuna é
registrada em `textGaps`, o lote continua e somente resultados com texto efetivo
recebem `textSha256`. Regressão coberta por teste específico.

## Pendência

Versionar os arquivos novos quando o conjunto de alterações paralelas do
workspace estiver pronto para commit. Não há bloqueio técnico ou jurídico para
uso read-only da integração.

