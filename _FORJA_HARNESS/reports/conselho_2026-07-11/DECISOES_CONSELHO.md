# Decisões sobre o conselho de auditoria — 11/07/2026

Conselho: Efesto (técnica), Helena (estratégia), Cícero (jurídica), Diabob (red team).
Relatórios individuais nesta pasta. Toda recomendação abaixo foi decidida após
**verificação empírica no código/estado real** — dois achados do Diabob caíram na checagem
(confirma a Lição 47: achado de auditor é hipótese, não fato).

Filtro aplicado por ordem do Igor (11/07): nada de burocracia clichê, nada de controle de
"ética/compliance de IA" fora do objetivo, nenhuma mudança que quebre ou atrape o pipeline.

## Achados de auditor DERRUBADOS na verificação

| Achado | Alegação | Realidade verificada |
|---|---|---|
| D6 (Diabob) | `sanitize_pdfs_pendentes.py` não existe | Existe na raiz do harness (listagem do diretório) |
| D8 (Diabob) | `BLINDAGEM_IDPI` ausente do código | Existe em `forja_headless.py:37` e é aplicada a toda fase (linha 58) |
| D1 (parcial) | Gate Helena+Cícero "não bloqueia" | Elo 10 do `forja_delivery.py` valida conteúdo com régua anti-fraude (≥800 chars, ≥3 recomendações, sem placeholder) e impede `fulfilled`. O que era real: a reprovação não deixava rastro legível por máquina (ver D7 acatado) |

## ACATADO e implementado (11/07/2026)

1. **D3 (Diabob) + Lição 48 — lastro de fidelidade do visual law.**
   `forja_visual.py` agora grava `FIDELIDADE_VISUAL.json` (docxSha256, mdSha256, contagens,
   timestamp) após o gate de fidelidade passar; o elo 4-B do `forja_delivery.py` exige o
   lastro com hash batendo (mesmo padrão do F7). Pega DOCX visual de versão errada ou
   alterada após o gate — exatamente o modo de falha do caso Patrícia. Casos pré-gate são
   aceitos por evidência legada (nomes reais encontrados: RELATORIO_VISUAL_LAW.json,
   RELATORIO_FINAL_VISUAL_LAW.json, resultado.json, retorno.json, visual_law_metadata.json).
2. **D7 (Diabob) / C2 (Cícero) / H10 (Helena) — reprovação com rastro e falha alta.**
   `forja_delivery.py`: trilha reprovada grava `trilhaBloqueadores` (lista dos elos que
   falharam, com motivo) no FORJA_STATE.json, inclui `bloqueadores` no JSON de saída e
   sai com exit code 2 — automação encadeada falha alto em vez de seguir em silêncio.
3. **C6 (Cícero) — lição Libra Sul: regimento citado, não só presente.**
   Elo 2 agora valida CONTEÚDO: `F3_MAPA_FONTES_E_REGIMENTO.md` precisa citar o regimento
   interno do tribunal (grep por "REGIMENTO"). Os 5 F3 reais existentes passam — trava só
   o caso futuro que pular a etapa.
4. **Regressão nova**: `test_forja_conselho_1107.py` (10 casos: 7 do lastro visual + 3 do F3),
   integrada ao padrão das suítes existentes. Suítes anteriores (régua, verificador,
   citações) revalidadas verdes após as mudanças.

## REJEITADO (com porquê — não reabrir sem fato novo)

| Recomendação | Origem | Porquê rejeitada |
|---|---|---|
| Detector automático de precedente superado (modo 6) | Cícero R1 | Não determinístico — viraria gate de papel (teatro). Permanece humano no F7 com cache de fontes datado |
| Flag NLP para afirmação sem fonte nos autos | Cícero R5 | LLM-as-judge, rejeitado no plano 07; matriz factual continua manual (G5.1) |
| Consolidar N2/N3 em executor único (12h) | Diabob | Mexe no núcleo que roda em produção; risco > benefício agora. Fica para transição planejada N2→N3 (Efesto também recomendou adiar) |
| Painel → priorização automática (16h) e feedback loop instrumentado (20h+) | Helena R1.1/R2.2 | Investimento grande de horas = decisão de negócio do Igor, não alçada técnica. Registrado como opção |
| Centralizar utils em `forja_n3_common.py` | Efesto R1 | Refactor cosmético tocando 7 arquivos em produção; churn sem ganho funcional |
| try/except no bloco F7 do render | Efesto R2 | Redundante: F7 já roda fail-closed antes de artefato e o F10 bloqueia sem F7 |
| Checklist humano de "leitura de regimento confirmada" | Cícero R4 | Burocracia clichê; substituído pelo gate automático de conteúdo do F3 (item 3 acatado) |
| Gate de código para "Pontos que exigem o seu olho" no e-mail | Cícero R2 | Corpo do e-mail não é inspecionável em todos os caminhos de envio — gate inexequível viola a política de 10/07. Permanece no protocolo de prompt (U11) |

## Opções de investimento que ficam para decisão do Igor (risco de negócio: horas)

- **Priorização automática painel→FORJA** (~16h): Helena estima dobrar a vazão (4→8 peças/semana).
- **Instrumentar feedback do Fábio por classe de erro** (~8h + 2 semanas de coleta): validaria com dados se os 30-40% de tempo de auditoria estão bem gastos.
- **Transição N2→N3 como executor único** (~1-2 semanas): elimina os dois pipelines paralelos apontados por Diabob (D5) e Efesto (E4).
