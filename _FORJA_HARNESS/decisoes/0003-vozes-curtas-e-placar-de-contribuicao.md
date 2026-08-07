# 0003 — Vozes curtas do Cursor e o placar que decide se elas ficam

- Status: Aceita
- Data: 07/08/2026
- Quem decidiu: Igor

## Contexto

A assinatura do Cursor dá acesso a 197 modelos, e a FORJA usava um. O titular
pediu duas coisas juntas, e elas se sustentam mutuamente: **aproveitar Kimi K3 e
GLM 5.2 como parecer curto**, com pouco token, só pelo ponto de vista deles; e
**medir quanto cada modelo agrega**, para poder promovê-los com o tempo.

O pedido tem um problema embutido que não é do titular, é da casa: o Kimi K3 foi
retirado do registro em 26/07/2026 **por reprovar a bancada jurídica**. Os
números estão em `telemetria/bench_modelos/REAVALIADO_2026-07-26_004912.json`:
2 de 6 corretas na condição cautelosa, com 2 invenções e 1 falha técnica, e
**0 de 6 na condição solta, com 4 invenções**. O Grok, na mesma prova solta,
fez 6 de 6.

Isso não torna o pedido errado. Torna-o preciso: o K3 é bom de ângulo e péssimo
de fonte, e as duas coisas convivem. O que não pode conviver é ele voltar sem
que a medição volte junto.

## Decisão

**Três peças, e a terceira é a que impede as outras duas de virarem ritual.**

### 1. Registro — `restricoes` no `Modelo`

`kimi-k3-cursor` (remoto `kimi-k3-high`) e `glm-5.2-cursor` (remoto
`glm-5.2-high`), ambos por `provedor="cursor"`, ambos nas fases F4 e F7.

O K3 carrega `restricoes=("nao_afirma_fato",)`. A restrição vira instrução no
prompt e marcação `podeAfirmarFato: false` no artefato — as duas, porque
instrução em prompt é pedido e marcação em artefato é fato do registro.

O GLM **não** carrega restrição, e isso é deliberado: ele nunca passou pela
bancada, e *não aferido* não é o mesmo que *reprovado*. Colapsar os dois estados
num só é o erro que faz uma medição ruim virar preconceito e uma ausência de
medição virar absolvição. A promoção trata os dois casos com mensagens
diferentes.

### 2. Painel — `forja_painel_curto.py`

Roda as duas vozes sobre um documento e devolve **no máximo 4 observações de até
300 caracteres cada**, com o alvo cortado em 6.000 caracteres e `max_tokens=700`.

**Os tetos são cortados no código, não pedidos no prompt.** Pedir brevidade a um
modelo é sugestão. Medido no primeiro uso real: as duas vozes juntas levaram 43
segundos, US$ 0,00, e o GLM estourou o teto de caracteres numa observação — que
saiu truncada **e declarada como truncada**, porque corte silencioso deixa a
saída com cara de completa.

O artefato declara a natureza: não é gate, não é conselho obrigatório, não é
fonte. Helena, Cícero e Diabob continuam sendo o conselho, e nada daqui vira
fundamento, citação, número ou data.

### 3. Placar — `forja_contribuicao.py`

Vocabulário fechado de veredito: `acatada`, `acatada_parcial`, `duplicada`,
`rejeitada`, `errada`. O índice é uma frase: **de cada 100 observações, quantas
mudaram a peça, descontadas as erradas.**

As três armadilhas que ele fecha, e como:

| Armadilha | Defesa |
|---|---|
| Taxa de acatamento premia o óbvio | `duplicada` conta no denominador e não soma. Quem só concorda tira zero |
| Amostra pequena mente com confiança | `elegivel: false` abaixo de 12 observações **e** 3 casos distintos |
| Contar não é ler | `amostra` abre o texto real a partir do painel e não grava nada |

`duplicada` exige `--duplicada-de`: sem apontar de quem é o eco, o veredito
viraria o depósito de tudo que se quer neutralizar sem julgar, e o placar
perderia a distinção que existe para fazer.

**Escada:** `observador` → `consultivo` → `candidato`. Nenhum degrau é
automático, nenhum se pula, todos exigem `--aprovado-por`. `candidato` é
recusado quando o modelo carrega `nao_afirma_fato` (com os números da bancada na
mensagem) e quando o modelo nunca foi aferido (com esse motivo, e não com o
outro). `revalidar` compara a evidência congelada na promoção com a de hoje e
**não altera nada** — devolve a divergência para quem promoveu.

O ledger guarda **decisão e localizador, nunca o texto**: a observação vive no
artefato do caso.

## Consequências

- Passa a valer: qualquer voz nova entra por aqui, e a pergunta "ela agrega?"
  tem resposta medida em vez de impressão.
- Fica proibido: promover por simpatia, e usar o placar de contribuição para
  revogar a bancada de fidelidade à fonte. São réguas de coisas diferentes.
- O painel é **opcional em F4 e F7**, oferecido no `RUN_CONTEXT` como o
  repertório de skills oferece as suas — recurso que o agente não lembra que
  existe é recurso ausente (Lição 270).
- Aceita-se perder: nada é medido enquanto ninguém decidir sobre as
  observações. O placar depende de trabalho humano, e é essa dependência que o
  torna confiável.

## O que NÃO foi feito, e por quê

**O painel não entrou em `requiredOutputs` de nenhuma fase.** Seria contraditório
com o pedido de gastar pouco, e criaria dependência bloqueante de um modelo que
reprovou a bancada. Há regressão que afere essa ausência: se um dia mudar, muda
por ADR e o teste é onde a mudança aparece.

**Nenhum juiz automático de qualidade.** A tentação era pedir a um modelo que
classificasse as observações dos outros. Isso é LLM-as-judge, já rejeitado no
plano de upgrades de 09/07/2026, e aqui seria pior: o juiz mais provável seria
da mesma família que escreveu a peça, e mediria concordância consigo mesmo.

**O teste legado foi reescrito, não afrouxado.**
`test_kimi_k3_foi_retirado_de_todo_o_registro` afirmava a ausência do K3 e
quebrou com a ordem nova. Trocá-lo por `assertIn("kimi-k3-cursor")` apagaria a
medição de 26/07. Ele passou a aferir o motivo pelo qual o K3 saiu: a restrição,
as fases em que ele pode falar, e que **nenhum modelo com `nao_afirma_fato` está
em F3 ou F5** — as fases em que a esteira colhe fonte oficial e confere citação.

## Critério de reabertura

Voz que acumule amostra elegível e índice alto sem que ninguém consiga apontar
uma peça concretamente melhor por causa dela — sinal de que o veredito `acatada`
está sendo dado com generosidade e o placar virou termômetro de simpatia.
