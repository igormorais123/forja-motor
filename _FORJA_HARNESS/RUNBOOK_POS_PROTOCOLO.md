# Runbook do loop pós-protocolo

## Resultado operacional

O job consulta o Gmail em leitura, usa o vínculo canônico de demanda/caso,
captura anexos elegíveis e gera o ramo F10 pós-protocolo. Ele não envia e-mail,
não assina e não protocola documentos.

## Estados

- `not_detected`: não há retorno elegível.
- `identity_ambiguous`: retorno preservado em quarentena, sem vínculo conclusivo.
- `captured`: original e cópia canônica foram preservados.
- `claimed`: a mensagem declara protocolo, mas falta elo de arquivo.
- `verified`: existe elo verificável entre prova e arquivo.
- `ai_baseline_unresolved`: falta reconstruir a versão exata entregue.
- `diff_ready`: comparação e relatório foram gerados.
- `review_pending`: lições aguardam decisão.
- `learning_promoted`: ao menos uma lição foi aprovada com fixture e teste.
- `complete`: revisão e decisões do retorno foram encerradas.

## Nomenclatura

Antes da prova, a pasta se chama `VERSÃO HUMANA FINAL — ...`. Somente
`protocol_verified` autoriza `PEÇA PROTOCOLADA — ...`.

## Recuperação por reason code

| Código | Próxima ação |
|---|---|
| `PP-01` | resolver manualmente o caso; não mover o anexo |
| `PP-02` / `PP-BASELINE-HASH` | localizar o envio exato e criar `F10_POST_PROTOCOL_BASELINE_BACKFILL.json`; nunca sobrescrever F9/F10 |
| `PP-03` | obter comprovante ou versão carimbada com elo de arquivo |
| `PP-04` | nenhuma; o reenvio já foi agregado à evidência existente |
| `PP-06` | abrir o arquivo e repetir a extração com ferramenta compatível |
| `PP-BASELINE-AMBIGUOUS` | identificar qual entrega ocorreu por último |
| `PP-OCR-LOW-CONFIDENCE` | substituir OCR ou revisar manualmente |

## Execução manual

```powershell
.\run_post_protocol_job.ps1
```

Para validar pareamentos sem baixar:

```powershell
python .\forja_post_protocol.py scan-gmail --shadow
```

## Rollback

Defina `features.n4PostProtocolV1` como `false` em `FORJA_N3_CONFIG.json`.
O job passa a retornar `disabled`. Arquivos já capturados permanecem intactos.

## Aprendizado controlado

O retorno humano gera candidatos, não regras automáticas. Uma lição só entra em
`learning_registry/ACTIVE_RULES.json` depois de:

1. origem humana identificada;
2. decisão explícita;
3. fixture de regressão;
4. teste prospectivo verde;
5. promoção no menor escopo aplicável.

Na próxima peça compatível, o validador prospectivo exige prova de que a regra
promovida foi aplicada. Ausência produz `PP-LEARNING-NOT-APPLIED` e bloqueia a
promoção da candidata.

## Artefatos e histórico

- A versão entregue pela FORJA é resolvida por `artifactId`, hash e horário real
  de envio; “arquivo mais recente” não é base válida.
- Retornos sucessivos são preservados em
  `n4_artifacts/post_protocol_history/<contentKey>/`.
- O original, o comparativo integral e os textos permanecem no cofre local
  ignorado pelo Git.
- O estado rastreado contém somente IDs, hashes, classificações, decisões e
  reason codes.
- Backfill histórico usa
  `F10_POST_PROTOCOL_BASELINE_BACKFILL.json` em `pending_review`; F9/F10
  originais permanecem byte a byte intactos.
