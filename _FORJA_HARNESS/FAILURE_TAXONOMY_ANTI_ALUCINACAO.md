# Taxonomia anti-alucinação jurídica

| Código | Falha | Gate |
|---|---|---|
| AH-01 | autoridade inexistente ou classe não inventariada | inventário canônico + fonte oficial |
| AH-02 | tribunal, número ou classe trocados | identidade da autoridade |
| AH-03 | aspa ou trecho não consta da fonte | excerpt verbatim hash-bound |
| AH-04 | proposição final não é a proposição revisada | vínculo documento/parágrafo/proposição |
| AH-05 | tese deturpada, ratio confundida ou polaridade invertida | revisão humana + gate editorial |
| AH-06 | precedente/norma superado, revogado ou fora do contexto | replay vivo + revisão humana |
| AH-07 | política rebaixada ou pacote envelhecido | policy hash + revalidação F9/F10 |
| AH-08 | autocertificação por JSON, arquivo ou URL fabricável | recomputação independente |
| AH-09 | **lastro aparente**: fato marcado como confirmado em documento, com localizador plausível que ninguém abriu | transcrição verbatim obrigatória (`forja_lastro.py`, L1/L2) |
| AH-10 | não conhecimento de recurso relatado como confirmação de mérito | L3 — coocorrência bloqueante |
| AH-11 | identidade entre atos ou processos afirmada por semelhança | L5 — exige os dois números CNJ à vista |
| AH-12 | norma citada só pelo ano, sem norma nomeada | L6 — ano é fácil de inventar e não é conferível |

O tratamento é fail-closed para `strict_protocol`. “Não localizado” significa
pendência, não inexistência.

