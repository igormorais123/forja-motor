# Registro detalhado — Bancada Cafelana V7

Gerado por `bancada_registro.py` em 27/07/2026 16:22. Todos os números vêm dos artefatos da execução; nenhum foi transcrito à mão.

Leitura de conjunto e conclusões em `RELATORIO_BANCADA_V7.md`; protocolo e blindagens em `LEIA-ME.md`. Este arquivo é a prova, não a narrativa.

## 1. Insumo congelado

- Dossiê: **139 KB**, 9 peças
- SHA-256: `d2cc55ba16836fafb0a3434b8a3788e8cba67165ac6578a5ec34181b0b385786`
- Ledger fechado: **40 julgados**, 7 súmulas, 0 temas

Peças do dossiê, na ordem em que foram apresentadas:

| # | rótulo | arquivo | KB | sha256 (12) |
|---:|---|---|---|---:|
| 1 | PECA_BASE_V6 | `_v6_2026-07-27/IMPUGNACAO_AGINT_CAFELANA_V6_27-07-2026_FONTE.md` | 60 | `e480790262a2` |
| 2 | RELATORIO_V6 | `_v6_2026-07-27/RELATORIO_V6_COMPARATIVO_E_MELHORIAS.md` | 16 | `1375d1bc31d9` |
| 3 | PARECER_HELENA_V6 | `_v6_2026-07-27/F4_PARECER_HELENA.md` | 8 | `9003ec033620` |
| 4 | PARECER_CICERO_V6 | `_v6_2026-07-27/F4_PARECER_CICERO.md` | 16 | `704dbca0322e` |
| 5 | DIRETRIZES_HUMANAS | `PROTOCOLO_CAFELANA_AGINT_ARESP2698443_DIRETRIZES_HUMANAS.md` | 9 | `c1fee90f1ed4` |
| 6 | FEEDBACK_TITULAR | `PROTOCOLO_FEEDBACK_FABIO_2026-07-14.md` | 2 | `2e6e084cd383` |
| 7 | CRONOLOGIA_AUDITADA | `CRONOLOGIA_PROCESSUAL_AUDITADA_2026-07-11.md` | 18 | `a1de2e6fb644` |
| 8 | MATRIZ_A8_A9 | `MATRIZ_A8_X_A9_2026-07-14.md` | 3 | `082b712c7166` |
| 9 | RED_TEAM_PROCESSUAL | `RED_TEAM_ACHADOS_PROCESSUAIS_2026-07-11.md` | 5 | `5a300a82a80e` |

## 2. Execução — telemetria por participante

| participante | família | rota | modelo no envelope | palavras (resposta) | palavras (peça) | tokens saída | tokens raciocínio | seg | US$ | truncada |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|:---:|
| `fable-5` | anthropic | assinatura | `claude-fable-5` | 10919 | 9543 | não capturado | 0 | 463 | 0.000 | não |
| `grok-4.5` | xai | openrouter | `x-ai/grok-4.5` | 11109 | 9546 | 22914 | 2555 | 263 | 0.216 | não |
| `kimi-k3` | moonshot | openrouter | `moonshotai/kimi-k3` | 719 | 719 | 32000 | 30317 | 1108 | 0.621 | sim |
| `luna-5.6` | openai | openrouter | `openai/gpt-5.6-luna` | 6011 | 4748 | 11196 | 516 | 100 | 0.106 | não |
| `opus-5` | anthropic | assinatura | `claude-opus-5` | 12161 | 8712 | não capturado | 0 | 430 | 0.000 | não |
| `sol-5.6` | openai | openrouter | `openai/gpt-5.6-sol` | 6925 | 5475 | 13768 | 1570 | 200 | 0.606 | não |

*Palavras (resposta)* inclui o relatório de mudanças contratado; *palavras (peça)* conta só o texto forense, que é o que a camada determinística avalia.

O modelo do envelope é lido da resposta do provedor, nunca do que foi pedido. Divergência entre pedido e envelope invalida a execução.

Os dois participantes de assinatura têm o total de tokens de saída marcado como **não capturado**: a soma por mensagem do stream devolvia contagem parcial, defeito corrigido depois desta execução. Como o stream não foi persistido, o total verdadeiro não é recuperável — e publicar o número parcial seria publicar um número falso. O custo dessas duas execuções é zero de qualquer modo, por rodarem na assinatura.

### 2.1 Execuções descartadas, preservadas como evidência

- **`opus-5-result-truncado-1turno`** — 1659 palavras, envelope reportou `claude-opus-5`. Motivo em `execucao_descartadas/LEIA-ME.md`.
- **`opus-alias-resolveu-4.8`** — 10956 palavras, envelope reportou `claude-opus-4-8`. Motivo em `execucao_descartadas/LEIA-ME.md`.

## 3. Camada determinística, item a item

### 3.1 Composição da nota

| participante | nota | integridade /40 | obediência /20 | retenção /20 | pendências /12 | ofício /8 | teto |
|---|---:|---:|---:|---:|---:|---:|---:|
| `fable-5` | **100.0** | 40.0 | 20.0 | 20.0 | 12.0 | 8.0 | 100 |
| `luna-5.6` | **100.0** | 40.0 | 20.0 | 20.0 | 12.0 | 8.0 | 100 |
| `grok-4.5` | **97.5** | 40.0 | 20.0 | 20.0 | 12.0 | 5.5 | 100 |
| `opus-5` | **95.5** | 40.0 | 20.0 | 20.0 | 12.0 | 3.5 | 100 |
| `sol-5.6` | **94.6** | 40.0 | 20.0 | 17.1 | 12.0 | 5.5 | 100 |
| `kimi-k3` | **74.6** | 40.0 | 20.0 | 8.6 | 0.0 | 6.0 | 80 |

### 3.2 Autoridades citadas contra o ledger fechado

| participante | citadas na peça | presentes no dossiê | novas declaradas | novas afirmadas | marcadores [A CONFERIR] |
|---|---:|---:|---:|---:|---:|
| `fable-5` | 26 | 26 | 0 | **0** | 0 |
| `grok-4.5` | 24 | 24 | 0 | **0** | 0 |
| `opus-5` | 20 | 20 | 0 | **0** | 0 |
| `luna-5.6` | 19 | 19 | 0 | **0** | 0 |
| `sol-5.6` | 15 | 15 | 0 | **0** | 0 |
| `kimi-k3` | 1 | 1 | 0 | **0** | 0 |

*Nova afirmada* = autoridade ausente do dossiê e apresentada como verificada. É a medida de invenção, e é o único item com poder de teto sobre a nota.

### 3.3 Canários — erros reais deste caso, um por linha

| canário | peso | o que detecta | `fable-5` | `grok-4.5` | `kimi-k3` | `luna-5.6` | `opus-5` | `sol-5.6` |
|---|---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `C1-prevencao` | 3 | trata de prevenção | — | — | — | — | — | — |
| `C2-conhecimento-parcial` | 3 | admite ou pede conhecimento parcial | — | — | — | — | — | — |
| `C3-precedente-autoderrotante` | 4 | invoca o AgInt no REsp 1.983.319/SP em APOIO à própria tese | — | — | — | — | — | — |
| `C4-fundamento-superado` | 4 | cita o AgInt no AREsp 2.629.809/SE | — | — | — | — | — | — |
| `C5-fala-sem-ata` | 3 | cita fala de desembargador em sessão | — | — | — | — | — | — |

### 3.4 Retenção do ganho da V6

| item | peso | o que é | `fable-5` | `grok-4.5` | `kimi-k3` | `luna-5.6` | `opus-5` | `sol-5.6` |
|---|---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `R1-unidade-dispositivo` | 3 | eixo do não conhecimento integral (AgInt no AREsp 2.072.941) | sim | sim | **não** | sim | sim | sim |
| `R2-corte-especial-14939` | 3 | QO no AREsp 2.638.376/MG, que impede a preliminar de se voltar contra a peça | sim | sim | **não** | sim | sim | sim |
| `R3-preclusao-pro-judicato` | 2 | EAREsp 2.762.459, cognição aberta | sim | sim | **não** | sim | removido c/ razão | sim |
| `R4-ementa-343A` | 2 | ementa de abertura com os quatro rótulos do art. 343-A do RISTJ | sim | sim | sim | sim | sim | sim |
| `R5-pedido-subsidiario` | 2 | pedido subsidiário de intimação da União sobre o ato do TRF1 | sim | sim | sim | sim | removido c/ razão | **não** |
| `R6-multa-1021` | 2 | multa do art. 1.021, § 4º, com o requisito que a Relatora exige | sim | sim | sim | sim | sim | sim |

Remover com razão declarada no relatório conta como cumprido: o prompt mandava corrigir o que estivesse errado e registrar a divergência. Remover em silêncio, não.

**Ressalva de precisão sobre `kimi-k3`.** A detecção de retenção mede presença do item no texto, e numa peça interrompida isso confunde menção com entrega: o `kimi-k3` marca `R5` e `R6` porque os dois aparecem no bloco *Resumo dos pedidos formulados* da ementa de abertura — a peça termina na Síntese 1 e nunca chega a uma seção de pedidos. Em texto truncado, leia esta tabela como inventário do que foi anunciado, não do que foi feito.

### 3.5 Pendências declaradas na V6

| pendência | peso | o que é | `fable-5` | `grok-4.5` | `kimi-k3` | `luna-5.6` | `opus-5` | `sol-5.6` |
|---|---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `P1-data-protocolo` | 1 | data de assinatura x data do protocolo | sim | sim | **não** | sim | sim | sim |
| `P2-conferencia-scon` | 2 | conferência nominal das autoridades preservadas da minuta humana | sim | sim | **não** | sim | sim | sim |
| `P3-risco-jurisprudencial` | 3 | risco de o colegiado preferir conhecimento parcial | sim | sim | **não** | sim | sim | sim |
| `P4-folha-rescisoria` | 2 | folha exata do acórdão da rescisória não conhecida | sim | sim | **não** | sim | sim | sim |
| `P5-composicao-turma` | 1 | composição atual da Primeira Turma | sim | sim | **não** | sim | sim | sim |

### 3.6 Gates da casa, aplicados sem adaptação

| participante | lastro P0 | lastro P1 | estilo humano P0 | estilo P1 | verificador P0 | P0 efetivo | placeholders indevidos |
|---|---:|---:|---:|---:|---:|---:|---:|
| `fable-5` | 0 | 3 | 0 | 5 | 0 | 0 | 0 |
| `grok-4.5` | 0 | 3 | 1 | 5 | 1 | 1 | 0 |
| `kimi-k3` | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| `luna-5.6` | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| `opus-5` | 0 | 3 | 1 | 1 | 3 | 2 | 0 |
| `sol-5.6` | 0 | 1 | 1 | 0 | 1 | 1 | 0 |

*P0 efetivo* desconta o placeholder da data do protocolo, exceção documentada da casa: a própria V6 entregue o tem.

### 3.7 Perfil de trabalho — medido, não pontuado

| participante | contenção | cobertura da V6 | jaccard | trechos próprios | leitura |
|---|---:|---:|---:|---:|---|
| `fable-5` | 0.832 | 0.878 | 0.746 | 1673 | edição incremental |
| `kimi-k3` | 0.815 | 0.064 | 0.063 | 138 | edição incremental |
| `grok-4.5` | 0.802 | 0.844 | 0.698 | 1969 | edição incremental |
| `opus-5` | 0.644 | 0.622 | 0.463 | 3238 | híbrido |
| `sol-5.6` | 0.109 | 0.065 | 0.043 | 5016 | reescrita integral |
| `luna-5.6` | 0.039 | 0.020 | 0.014 | 4745 | reescrita integral |

**Contenção** = fração dos trechos de 12 palavras da V7 que já existiam na V6. **Cobertura** = fração da V6 que sobreviveu. Não entra na nota: o prompt admitia preservar o texto ou a substância, e descontar por uma leitura permitida mediria a ambiguidade do enunciado, não o participante.

## 4. Julgamento cego — os seis votos brutos

Votos válidos: **6 de 6**. Anulados: nenhum. Custo do julgamento: US$ 1.39.

Cada juiz julgou duas vezes, com a ordem de apresentação invertida. A âncora é uma transcrição literal da peça eleita, conferida por código contra o texto — voto cuja âncora não confere é anulado.

| juiz | família | ordem | elegeu | âncora | ranking (melhor → pior) |
|---|---|---|---|---|:---:|
| `grok-4.5` | xai | direta | **sol-5.6** | válida | sol-5.6 > luna-5.6 > opus-5 > fable-5 > grok-4.5 > kimi-k3 |
| `grok-4.5` | xai | invertida | **sol-5.6** | válida | sol-5.6 > opus-5 > grok-4.5 > luna-5.6 > fable-5 > kimi-k3 |
| `opus-5` | anthropic | direta | **opus-5** | válida | opus-5 > fable-5 > luna-5.6 > grok-4.5 > sol-5.6 > kimi-k3 |
| `opus-5` | anthropic | invertida | **grok-4.5** | válida | grok-4.5 > fable-5 > opus-5 > sol-5.6 > luna-5.6 > kimi-k3 |
| `sol-5.6` | openai | direta | **sol-5.6** | válida | sol-5.6 > luna-5.6 > grok-4.5 > fable-5 > opus-5 > kimi-k3 |
| `sol-5.6` | openai | invertida | **sol-5.6** | válida | sol-5.6 > opus-5 > luna-5.6 > fable-5 > grok-4.5 > kimi-k3 |

### 4.1 Notas por critério — cada juiz, cada peça

**`grok-4.5` · ordem direta**

| peça | tese principal | fidelidade ao comando | uso de autoridade | arquitetura | escrita forense | utilidade ao julgador | média |
|---|---:|---:|---:|---:|---:|---:|---:|
| `luna-5.6` | 8.0 | 9.0 | 8.0 | 8.0 | 8.0 | 8.0 | 8.17 |
| `opus-5` | 9.0 | 4.0 | 9.0 | 10.0 | 9.0 | 9.0 | 8.33 |
| `grok-4.5` | 8.0 | 8.0 | 6.0 | 7.0 | 7.0 | 7.0 | 7.17 |
| `fable-5` | 9.0 | 8.0 | 5.0 | 8.0 | 7.0 | 8.0 | 7.50 |
| `kimi-k3` | 2.0 | 2.0 | 2.0 | 1.0 | 3.0 | 1.0 | 1.83 |
| `sol-5.6` | 9.0 | 7.0 | 9.0 | 9.0 | 9.0 | 10.0 | 8.83 |

**`grok-4.5` · ordem invertida**

| peça | tese principal | fidelidade ao comando | uso de autoridade | arquitetura | escrita forense | utilidade ao julgador | média |
|---|---:|---:|---:|---:|---:|---:|---:|
| `luna-5.6` | 8.0 | 8.0 | 8.0 | 7.0 | 9.0 | 8.0 | 8.00 |
| `opus-5` | 9.0 | 6.0 | 8.0 | 10.0 | 9.0 | 9.0 | 8.50 |
| `grok-4.5` | 9.0 | 7.0 | 7.0 | 8.0 | 8.0 | 8.0 | 7.83 |
| `fable-5` | 8.0 | 7.0 | 6.0 | 8.0 | 7.0 | 7.0 | 7.17 |
| `kimi-k3` | 2.0 | 1.0 | 1.0 | 1.0 | 2.0 | 1.0 | 1.33 |
| `sol-5.6` | 9.0 | 9.0 | 8.0 | 9.0 | 8.0 | 9.0 | 8.67 |

**`opus-5` · ordem direta**

| peça | tese principal | fidelidade ao comando | uso de autoridade | arquitetura | escrita forense | utilidade ao julgador | média |
|---|---:|---:|---:|---:|---:|---:|---:|
| `luna-5.6` | 7.0 | 8.0 | 8.0 | 7.0 | 7.0 | 7.0 | 7.33 |
| `opus-5` | 9.0 | 6.0 | 9.0 | 9.0 | 9.0 | 9.0 | 8.50 |
| `grok-4.5` | 8.0 | 8.0 | 5.0 | 7.0 | 8.0 | 7.0 | 7.17 |
| `fable-5` | 9.0 | 9.0 | 6.0 | 8.0 | 8.0 | 8.0 | 8.00 |
| `kimi-k3` | 2.0 | 2.0 | 2.0 | 2.0 | 4.0 | 1.0 | 2.17 |
| `sol-5.6` | 7.0 | 5.0 | 7.0 | 8.0 | 7.0 | 7.0 | 6.83 |

**`opus-5` · ordem invertida**

| peça | tese principal | fidelidade ao comando | uso de autoridade | arquitetura | escrita forense | utilidade ao julgador | média |
|---|---:|---:|---:|---:|---:|---:|---:|
| `luna-5.6` | 7.0 | 7.0 | 7.0 | 6.0 | 7.0 | 6.0 | 6.67 |
| `opus-5` | 8.0 | 4.0 | 8.0 | 8.0 | 9.0 | 8.0 | 7.50 |
| `grok-4.5` | 9.0 | 9.0 | 7.0 | 9.0 | 8.0 | 9.0 | 8.50 |
| `fable-5` | 9.0 | 9.0 | 7.0 | 9.0 | 8.0 | 9.0 | 8.50 |
| `kimi-k3` | 3.0 | 3.0 | 3.0 | 3.0 | 4.0 | 2.0 | 3.00 |
| `sol-5.6` | 8.0 | 6.0 | 8.0 | 8.0 | 8.0 | 8.0 | 7.67 |

**`sol-5.6` · ordem direta**

| peça | tese principal | fidelidade ao comando | uso de autoridade | arquitetura | escrita forense | utilidade ao julgador | média |
|---|---:|---:|---:|---:|---:|---:|---:|
| `luna-5.6` | 8.8 | 9.0 | 7.6 | 7.7 | 7.8 | 8.3 | 8.20 |
| `opus-5` | 8.9 | 6.2 | 7.8 | 8.6 | 7.5 | 8.5 | 7.92 |
| `grok-4.5` | 9.0 | 9.3 | 7.1 | 7.3 | 6.9 | 7.9 | 7.92 |
| `fable-5` | 9.1 | 9.2 | 6.9 | 7.1 | 6.8 | 7.7 | 7.80 |
| `kimi-k3` | 2.0 | 1.0 | 1.5 | 0.5 | 1.0 | 0.5 | 1.08 |
| `sol-5.6` | 9.3 | 8.7 | 8.4 | 9.2 | 8.9 | 9.3 | 8.97 |

**`sol-5.6` · ordem invertida**

| peça | tese principal | fidelidade ao comando | uso de autoridade | arquitetura | escrita forense | utilidade ao julgador | média |
|---|---:|---:|---:|---:|---:|---:|---:|
| `luna-5.6` | 8.4 | 6.8 | 8.0 | 8.0 | 8.2 | 8.3 | 7.95 |
| `opus-5` | 9.0 | 5.8 | 8.5 | 8.6 | 7.8 | 8.7 | 8.07 |
| `grok-4.5` | 8.7 | 7.0 | 7.6 | 6.8 | 6.3 | 7.2 | 7.27 |
| `fable-5` | 8.8 | 7.1 | 7.9 | 7.5 | 6.4 | 7.4 | 7.52 |
| `kimi-k3` | 4.5 | 3.0 | 1.0 | 1.0 | 3.5 | 1.0 | 2.33 |
| `sol-5.6` | 9.5 | 9.4 | 8.7 | 8.8 | 7.8 | 9.1 | 8.88 |

### 4.2 Média por critério, consolidada

| participante | tese principal | fidelidade ao comando | uso de autoridade | arquitetura | escrita forense | utilidade ao julgador | média geral |
|---|---:|---:|---:|---:|---:|---:|---:|
| `sol-5.6` | 8.63 | 7.52 | 8.18 | 8.67 | 8.12 | 8.73 | **8.31** |
| `opus-5` | 8.82 | 5.33 | 8.38 | 9.03 | 8.55 | 8.70 | **8.14** |
| `fable-5` | 8.82 | 8.22 | 6.47 | 7.93 | 7.20 | 7.85 | **7.75** |
| `luna-5.6` | 7.87 | 7.97 | 7.77 | 7.28 | 7.83 | 7.60 | **7.72** |
| `grok-4.5` | 8.62 | 8.05 | 6.62 | 7.52 | 7.37 | 7.68 | **7.64** |
| `kimi-k3` | 2.58 | 2.00 | 1.75 | 1.42 | 2.92 | 1.08 | **1.96** |

### 4.3 Ordenação: Borda bruto e Borda entre famílias

| participante | Borda bruto | Borda entre famílias (média) | votos de outras famílias | eleito para protocolo |
|---|---:|---:|---:|---:|
| `sol-5.6` | 23 | **3.25** | 4 | 4 |
| `opus-5` | 20 | **3.00** | 4 | 1 |
| `grok-4.5` | 15 | **2.75** | 4 | 1 |
| `luna-5.6` | 17 | **2.50** | 4 | 0 |
| `fable-5` | 15 | **1.75** | 4 | 0 |
| `kimi-k3` | 0 | **0.00** | 6 | 0 |

O Borda entre famílias descarta o voto de qualquer juiz sobre peça da própria família — por isso a coluna é média, e não soma. Como as três famílias de juiz (anthropic, openai, xai) também competem, cada uma dessas peças perde os 2 votos do juiz conterrâneo e fica com 4. Só o `kimi-k3` recebe os 6: não há juiz moonshot na bancada. O Borda bruto fica na tabela para que se veja o quanto a correção move — o `luna-5.6`, por exemplo, cai de 3º para 4º quando os votos do Sol, da mesma família, saem da conta.

### 4.4 Auto-preferência e estabilidade de posição

| juiz | posição que deu a si | posição que os outros deram | vantagem |
|---|---:|---:|---:|
| `sol-5.6` | 1.0º | 2.75º | +1.75 |
| `opus-5` | 2.0º | 3.00º | +1.00 |
| `grok-4.5` | 4.0º | 3.25º | -0.75 |

| juiz | posições idênticas ao inverter a ordem | manteve o vencedor |
|---|---:|:---:|
| `grok-4.5` | 2 de 6 | sim |
| `opus-5` | 2 de 6 | **não** |
| `sol-5.6` | 3 de 6 | sim |

Ranking que muda ao inverter a ordem mede viés de posição, não qualidade. É a razão pela qual nenhum resultado desta bancada deve ser lido com precisão decimal.

### 4.5 O erro mais grave de cada peça, na palavra dos juízes

**`fable-5`**

- [grok-4.5/direta] Distingue o EREsp 1.414.755/PA sem inteiro teor conferido e protocola com data fixa de 27/07/2026.
- [grok-4.5/invertida] Usou autoridade não conferida (EREsp 1.414.755/PA) e sobrecarregou o capítulo sancionatório com imputações de má-fé além do lastro.
- [opus-5/direta] Distingue o EREsp 1.414.755/PA sem dispor do inteiro teor, atribuindo-lhe tese não conferida em peça protocolável.
- [opus-5/invertida] Sustenta que a tempestividade 'jamais foi objeto de enfrentamento motivado' e distingue o EREsp 1.414.755/PA sem dispor do inteiro teor, atribuindo a precedente não conferido conteúdo que a própria peça admite repousar em descrição interna.
- [sol-5.6/direta] Atribui conteúdo a precedentes e atos processuais sem conferência integral, inclusive distinguindo o EREsp nº 1.414.755/PA sem dispor de seu inteiro teor.
- [sol-5.6/invertida] Transforma em preliminar autônoma uma intempestividade dependente do teor não conferido da Portaria Presi/TRF1 nº 138/2024.

**`grok-4.5`**

- [grok-4.5/direta] Empilha fatos e fundamentos da rescisória sem folha e não formula pedido sucessivo de conhecimento parcial com desprovimento.
- [grok-4.5/invertida] Manteve a intempestividade como causa autônoma de não conhecimento, reabrindo risco de incidente de regularização sem ganho real.
- [opus-5/direta] Afirma como fatos dos autos o placar de 4 a 1, a unanimidade e o próprio fundamento do acórdão da rescisória, sem ponte de folha e sem lastro no acervo.
- [opus-5/invertida] Cita como conferidas autoridades que o próprio relatório reconhece pendentes de validação no SCON, entre elas o AgInt no AREsp 2.504.785/SP, que sustenta sozinho a proposição sobre ponto facultativo.
- [sol-5.6/direta] Sustenta pedido de nova comprovação documental mesmo reconhecendo que os atos normativos já foram juntados, além de apoiar-se em fatos e autoridades ainda não conferidos.
- [sol-5.6/invertida] Mantém como causa autônoma de não conhecimento uma intempestividade cuja premissa material não foi confirmada e ainda pede nova apresentação de atos já juntados.

**`kimi-k3`**

- [grok-4.5/direta] Texto incompleto, interrompido no meio da Síntese 1, inviável para qualquer uso.
- [grok-4.5/invertida] Peça incompleta: o texto se interrompe no meio da Síntese 1 e não chega a pedidos utilizáveis.
- [opus-5/direta] Peça incompleta: interrompe-se na Síntese 1, sem preliminares, fundamentação, pedidos ou assinatura.
- [opus-5/invertida] Peça incompleta: interrompe-se no meio da Síntese 1, sem tópicos, fundamentação, pedidos ou assinatura.
- [sol-5.6/direta] O texto termina abruptamente no meio de uma palavra e não contém desenvolvimento, pedidos ou fecho completos.
- [sol-5.6/invertida] A peça está truncada no meio de uma frase e, por isso, não contém desenvolvimento, pedidos ou fecho passíveis de julgamento ou protocolo.

**`luna-5.6`**

- [grok-4.5/direta] Mantém pedido autônomo de intempestividade com intimação para documento já juntado, convidando dilação inútil após a QO e a Lei 14.939/2024.
- [grok-4.5/invertida] Não formula pedido sucessivo expresso de conhecimento parcial com preservação do óbice do art. 512/Súmula 284.
- [opus-5/direta] Escada de pedidos que não formula o cenário mais provável — conhecimento parcial com desprovimento —, obrigando o colegiado a construí-lo sozinho.
- [opus-5/invertida] Mantém no item 85 a afirmação de que a União apresentou quesitos e indicou assistente técnico sem ponte de folha nos autos, transformando premissa não lastreada em fato afirmado ao tribunal.
- [sol-5.6/direta] Pede nova intimação para apresentação de ato oficial embora reconheça que a União já juntou a Portaria Presi/TRF1 nº 138/2024 e outros atos.
- [sol-5.6/invertida] Formula pedido autônomo de intempestividade e requer apresentação de ato que a própria peça reconhece já ter sido juntado aos autos.

**`opus-5`**

- [grok-4.5/direta] Descumpre de forma deliberada e registrada a determinação do titular de reforçar a intempestividade como causa autônoma.
- [grok-4.5/invertida] Descumpriu de modo consciente a determinação de manter/reforçar a intempestividade, rebaixando-a a mera preservação sem pretensão útil.
- [opus-5/direta] Suprimiu o pedido autônomo de intempestividade contra determinação expressa do titular, deixando o Tópico IV como capítulo que nada pede.
- [opus-5/invertida] Suprime o pedido autônomo de intempestividade e o pedido subsidiário de intimação, contrariando determinação expressa do titular de manter e reforçar a preliminar.
- [sol-5.6/direta] Retira o pedido autônomo de intempestividade apesar de registrar expressamente que essa opção não cumpre integralmente a determinação do titular.
- [sol-5.6/invertida] O relatório declara expressamente que a peça não cumpriu integralmente a determinação do titular de manter e reforçar a intempestividade.

**`sol-5.6`**

- [grok-4.5/direta] Rebaixa a intempestividade a mero apêndice subsidiário além do que a linha de reforço do titular admitiria.
- [grok-4.5/invertida] Extensão ainda elevada e dependência residual de verificação do teor da portaria do TRF1 na ponta subsidiária.
- [opus-5/direta] Rebaixa a intempestividade a exame apenas condicionado, sem pedido de reconhecimento próprio, descumprindo a determinação de mantê-la como fundamento de não conhecimento.
- [opus-5/invertida] Reposiciona a intempestividade como simples pedido para o tribunal 'verificar' o conteúdo da portaria, esvaziando a determinação do titular de manter e reforçar a preliminar.
- [sol-5.6/direta] A aplicação direta do AgInt no AREsp nº 2.072.941 ao agravo interno contra decisão monocrática do STJ ainda exige demonstração mais rigorosa da identidade estrutural entre as hipóteses.
- [sol-5.6/invertida] O relatório interno de mudanças permanece anexado depois das assinaturas e deve ser necessariamente excluído antes do protocolo.

### 4.6 O que decidiu a comparação, por juiz

**`grok-4.5` · ordem direta** — P6 articula com mais densidade o eixo decisivo — silêncio total quanto ao art. 512/Súmula 284 e unidade do dispositivo — e fecha o risco de conhecimento parcial com pedido sucessivo expresso, sem sobras retóricas. Corrigiu a cronologia da tempestividade à prova dos autos e à QO da Corte Especial, convertendo o flanco em verificação material subsidiária em vez de autônoma autodilatória. P2 rivaliza em arquitetura e escrita, mas descumpre de modo confessado a determinação do titular sobre a intempestividade. P1 obedece melhor ao comando e é protocolável, porém é menos enxuta e menos cirúrgica na escada de pedidos. P4 e P3 carregam autoridade ou premissas factuais frágeis; P5 está truncada.

**`grok-4.5` · ordem invertida** — P6 une a tese forte da unidade do dispositivo com enfrentamento expresso e pedido subsidiário do conhecimento parcial, sem abandonar a intempestividade e sem transformá-la em eixo autônomo frágil após a juntada e a QO da Corte Especial. P2 tem a melhor escada de pedidos e escrita mais cirúrgica, mas registra e pratica descumprimento da determinação de manter/reforçar a intempestividade. P3 e P4 ainda apostam demais na intempestividade autônoma e incham sanção ou autoridade; P1 é limpa, porém menos completa na escada; P5 está truncada e é imprópria para protocolo.

**`opus-5` · ordem direta** — Todas as seis versões acertam o eixo — a omissão integral da União quanto ao art. 512 do CPC e à Súmula 284/STF —, de modo que a comparação se decidiu no tratamento do risco de conhecimento parcial e na disciplina factual. P2 é a única que converte o cenário mais provável em pedido próprio (alínea b), acrescenta argumento próprio de coerência sistemática do juízo unitário de admissibilidade, invoca o art. 259, § 2º, do RISTJ e, sobretudo, expurga as afirmações que o acervo não sustenta (placar de 4 a 1, unanimidade da rescisória, nomes de julgadores, fundamento atribuído a acórdão não lido). P4 rivaliza em força e é mais fiel à determinação de manter a intempestividade como preliminar autônoma, mas constrói distinção de precedente (EREsp 1.414.755/PA) sem o inteiro teor e reproduz os mesmos excessos factuais; P3 repete esses excessos com menos densidade nova. P1 é sóbria e honesta, porém de prosa achatada e com escada de pedidos que ignora o desfecho mais provável; P6 rebaixa a intempestividade a mero exame condicionado, esvaziando comando expresso. Pesa contra P2 o descumprimento parcial da ordem de reforçar a intempestividade, mas a divergência foi registrada, apoiada em prova dos autos (juntada de 24/10/2024) e não gera pedido inútil ao colegiado — risco menor do que assinar peça com fato não lastreado.

**`opus-5` · ordem invertida** — A comparação se decidiu em dois eixos: enfrentamento do risco de conhecimento parcial e fidelidade à determinação do titular de manter e reforçar a preliminar de intempestividade. P3 e P4 fazem as duas coisas; P3 leva vantagem por internalizar no corpo da peça o controle negativo verificável (zero ocorrências de 'art. 512' e 'Súmula 284' nas fls. 938/949), por reconhecer expressamente a juntada dos atos normativos em 24/10/2024 — o que impede o desmentido em uma linha que fragiliza P4 — e por não datar o fecho com data de revisão. P2 é a peça mais bem escrita e a única com pedido sucessivo expresso de conhecimento parcial, mas descumpre frontalmente a determinação do titular ao suprimir o pedido autônomo de intempestividade, e determinação descumprida é falha grave ainda que a alternativa seja tecnicamente melhor. P6 é sóbria e honesta nas pendências, porém rebaixa a intempestividade a mero pedido de verificação, esvaziando o comando. P1 é seca e correta, mas rala em densidade nos capítulos de mérito. P5 está truncada no meio da Síntese 1 e sequer é peça.

**`sol-5.6` · ordem direta** — P6 apresenta a melhor combinação de tese principal verificável, enfrentamento explícito do conhecimento parcial e escada completa de pedidos. Também trata a intempestividade com honestidade, reconhecendo a juntada posterior dos atos e limitando a controvérsia ao conteúdo material da portaria. P1 preserva melhor a formulação autônoma determinada pelo titular, mas é mais extensa e pede complementação documental apesar de os atos já estarem nos autos. P3 e P4 acumulam fatos e autoridades pendentes de confirmação, enquanto P2 registra expressamente o descumprimento de determinação do titular. P5 está truncada e não constitui peça utilizável.

**`sol-5.6` · ordem invertida** — P6 é a única que enfrenta frontalmente o risco de conhecimento parcial sem abandonar o pedido principal e oferece ao colegiado uma consequência subsidiária juridicamente ordenada. Também calibra a intempestividade conforme a prova disponível, sem convertê-la em causa autônoma categórica nem pedir novamente documento já juntado. P2 tem excelente escada de pedidos, mas seu próprio relatório reconhece descumprimento de determinação do titular, falha que impede sua escolha. P1, P3 e P4 superdimensionam a intempestividade ainda dependente do conteúdo da portaria, enquanto P5 está materialmente truncada.

## 5. Quadro final

| # | participante | final | determinística | juízes | tetos aplicados |
|---:|---|---:|---:|---:|---|
| 1 | `sol-5.6` | **85.4** | 94.6 | 74.1 | — |
| 2 | `opus-5` | **84.3** | 95.5 | 70.7 | — |
| 3 | `luna-5.6` | **83.6** | 100.0 | 63.6 | — |
| 4 | `grok-4.5` | **83.2** | 97.5 | 65.7 | — |
| 5 | `fable-5` | **80.3** | 100.0 | 56.2 | — |
| 6 | `kimi-k3` | **45.4** | 74.6 | 9.8 | não entregou o relatório de mudanças contratado |

Composição: 55% determinística, 45% juízes, com o teto da camada determinística valendo como veto sobre a nota final. **Custo total da bancada: US$ 2.94.**

## 6. Suítes do harness, na mesma rodada

**Baseline** (2026-07-27T15:35:25-03:00, Python 3.14.6): **42/42 suítes verdes** · 475 testes pytest (+49 subtests) · 7 regressões em script · **APROVADO**.

Nenhuma suíte vermelha.

Suítes acrescentadas nas rodadas recentes:

| suíte | família | resultado |
|---|---|---|
| `test_forja_identidade_modelo.py` | pytest | 12 passed in 0.22s |
| `test_forja_lastro.py` | script | ok: 12 detecções + 11 não-travas lexicais + 10 de ledger + 4 de acoplamento conferem (37 no total) |
| `test_forja_regimentos.py` | script | ok: 14 casos de auditoria de regimento conferem (4 cabeçalhos reais do acervo) |

**Régua** (2026-07-27T15:35:25-03:00, modo completa): **APROVADO** em 43.8s · integridade de arquivos protegidos: íntegra.

## 7. Onde está cada artefato

| artefato | caminho |
|---|---|
| dossiê congelado + ledger fechado | `protocolo/DOSSIE.md`, `protocolo/DOSSIE_LEDGER.json` |
| prompt idêntico a todos | `protocolo/PROMPT_V7.md` |
| as seis peças e a telemetria | `execucao/<participante>/SAIDA.md` e `META.json` |
| execuções descartadas | `execucao_descartadas/` |
| peças anonimizadas | `cego/P1..P6.md` |
| mapa do cegamento | fora do workspace, em `~/.forja_ar_secrets/` |
| camada determinística | `avaliacao/DETERMINISTICA.json` |
| votos brutos dos juízes | `avaliacao/juizes/<juiz>_<ordem>.json` |
| consolidação dos juízes | `avaliacao/JUIZES_CONSOLIDADO.json` |
| quadro final | `avaliacao/QUADRO_FINAL.json` |
| leitura de conjunto | `RELATORIO_BANCADA_V7.md` |
| protocolo e blindagens | `LEIA-ME.md` |

