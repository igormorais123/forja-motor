# FORJA N3 — RELATÓRIO DE REPLAY EM SOMBRA

Gerado em: `2026-07-10T01:18:11-03:00`  
Modo: `shadow_readonly_copy` — os estados e as peças originais não foram alterados.

## Resultado consolidado

- Estados N2 reproduzidos: **21/21**.
- Estados originais preservados por hash: **21/21**.
- Casos compatíveis sem bloqueio: **15**.
- Casos em que a N3 abriu bloqueio explícito: **6**.
- Diagramas examinados no corpus: **20**, reprovados: **9**.

Bloqueio no replay não altera a peça histórica. Ele demonstra que o fluxo novo interromperia a promoção até correção ou decisão humana registrada.

## Casos

| Caso | Resultado N3 | Regressões | Fontes pendentes | Artefatos ausentes | SVGs reprovados | Motivos |
|---|---:|---:|---:|---:|---:|---|
| case-email-auto-19f38f30238ff4d3 | compatible | 0 | 0 | 0 | 0 | - |
| case-email-auto-19f3ea400b7dec3d | compatible | 0 | 0 | 0 | 0 | - |
| case-email-auto-19f3ed5bdbdcf159 | compatible | 0 | 0 | 0 | 0 | - |
| Plano de Saúde | blocked | 1 | 1 | 0 | 0 | silent_phase_regression, pending_source_in_review_cycle |
| Azimut | blocked | 0 | 0 | 0 | 1 | visual_gate_failed |
| case-email-cafelana-agint-aresp-2698443-19f2f0876e358eab | compatible | 0 | 0 | 0 | 0 | - |
| case-email-cafelana-edcl-19f1f9d3cc69c8c8 | compatible | 0 | 0 | 0 | 0 | - |
| CORSAN | blocked | 0 | 0 | 0 | 3 | visual_gate_failed |
| case-email-jalusa-prestes-5000447 | compatible | 0 | 0 | 0 | 0 | - |
| case-email-jorge-haroldo-edcl-19f3c8200768b56e | compatible | 0 | 0 | 0 | 0 | - |
| case-email-jose-eduardo-siqueira-campos-19f1f92c333b1e4e | compatible | 0 | 0 | 0 | 0 | - |
| case-email-laudo-pericial-contabil-19f1f9467513bbae | compatible | 0 | 0 | 0 | 0 | - |
| Libra Sul | blocked | 0 | 0 | 0 | 2 | visual_gate_failed |
| case-email-memoriais-cautelar-fiscal-5002486 | compatible | 0 | 0 | 0 | 0 | - |
| Natura | blocked | 0 | 0 | 0 | 2 | visual_gate_failed |
| Patrícia/Fábio | blocked | 0 | 0 | 0 | 1 | visual_gate_failed |
| case-whatsapp-audio-cafelana-prevencao-20260708 | compatible | 0 | 0 | 0 | 0 | - |
| case-whatsapp-audio-protocolo-aprendizados-20260708 | compatible | 0 | 0 | 0 | 0 | - |
| case-whatsapp-audio-roraima-senador-20260708 | compatible | 0 | 0 | 0 | 0 | - |
| case-whatsapp-fabio-medina-osorio | compatible | 0 | 0 | 0 | 0 | - |
| case-whatsapp-igor-hermes-contexto | compatible | 0 | 0 | 0 | 0 | - |

## Limites desta execução

- O replay comprova importação, imutabilidade, consistência estrutural, referências de arquivos e lint dos SVGs disponíveis.
- Ele não transforma retrospectivamente estados N2 em prova de cobertura por página; casos sem cadernos de contexto N3 permanecem sem essa comprovação.
- A promoção como padrão continua dependente de três ciclos novos completos, conforme o critério de aceitação do plano.
