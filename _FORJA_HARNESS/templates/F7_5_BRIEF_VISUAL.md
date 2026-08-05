# F7.5 — Brief visual (contrato)

**Criado em 03/08/2026.** Fecha a lacuna medida na Onda 1B: o conteúdo semântico
das figuras não é inferível de prosa argumentativa, e sem ele o piso gráfico não
fecha em peça longa.

## Por que este arquivo existe

A esteira gera sozinha o mapa visual — onde entram pull quotes, caixas, linhas
de síntese e quadros. Isso é estrutural e o gerador acerta.

O que ela **não** consegue inferir é o conteúdo semântico de uma figura. Duas
tentativas foram feitas e as duas produziram figura bonita afirmando coisa
falsa:

- **Cronologia catada da prosa** misturou, na mesma linha do tempo, a data do
  próprio documento, um prazo interno de minuta, a data de um julgado citado e
  um fragmento de número CNJ lido como data (CASO-02 e CASO-07, 30/07/2026).
- **Cadeia de tese inferida das aberturas de seção** colocou a **tese da parte
  adversária** como elo do raciocínio da cliente, além de dois conectivos
  terminados em dois-pontos e um fragmento de item de lista (CASO-02,
  30/07/2026).

Em ambos os casos cada frase era verbatim do texto e o conjunto mentia. Não é
problema de heurística, é de premissa: nenhum filtro separa "nossa tese" de
"tese deles" numa frase de abertura. Por isso o dado vem declarado.

Regra da casa que isto respeita: **figura fabricada é pior que figura ausente,
porque parece prova.**

## Onde fica

`F7_5_BRIEF_VISUAL.json`, na mesma pasta do markdown auditado. Sem ele, a peça
ainda é composta, mas só com as figuras estruturalmente seguras (cards de capa,
matriz vinda de tabela existente, cronologia vinda de seção declarada) — e peça
longa não fecha o piso gráfico, acusando `VIS-03`.

## Formato

```json
{
  "ancoras": [
    ["4", "óbices processuais cumulativos"],
    ["09/04/2008", "ato alegado: pagamento pela CDI à LTI"],
    ["2009-2012", "ingresso dos ex-diretores na CASO-16"],
    ["13 anos", "decurso sem materialização de fumus ou periculum"]
  ],
  "cadeiaArgumentativa": [
    "O título judicial reportou-se aos juros legais, sem fixar taxa convencional.",
    "A taxa legal do art. 406 do Código Civil corresponde à Selic (Tema 1368).",
    "Cumular 1% ao mês com a Tabela Prática produz dupla recomposição.",
    "O excesso de execução deve ser liberado, aplicando-se a Selic."
  ],
  "cronologia": [
    ["12/09/2024", "Afetação do Tema 1368 pela Corte Especial."],
    ["08/05/2025", "Julgamento do mérito do repetitivo."],
    ["12/11/2025", "Trânsito em julgado do acórdão."]
  ]
}
```

Todos os campos são opcionais; o que faltar cai no comportamento estrutural.

**`ancoras`** — de 2 a 4 pares `[destaque, descrição]` para os cards da capa.
O destaque é curto (número, data, intervalo, quantidade). Este é o padrão
aprovado em 09/07/2026: dados na cara do julgador, não índice de seções. Sem
brief, os cards trazem os títulos das seções, que é bem mais fraco.

**`cadeiaArgumentativa`** — de 3 a 6 proposições que sustentam a tese, na ordem
lógica. A última é lida como conclusão e recebe destaque. Escreva **a nossa**
cadeia: o gerador não sabe distinguir a nossa da adversária, e foi assim que
errou.

**`cronologia`** — pares `[data, descrição]` dos atos processuais relevantes.
Só os atos: não inclua data do documento, prazo interno nem data de julgado
citado.

## O que o validador recusa

`forja_visual_figuras.validar_brief` roda antes da composição e bloqueia:

| Recusa | Motivo |
|---|---|
| Número ou data que não aparece no markdown | Fato introduzido pela camada visual. A figura não pode afirmar o que a peça não afirma. |
| Menção a e-mail, WhatsApp, Drive, pasta, prazo interno | Origem operacional é bloqueador P0 no corpo da peça pelo protocolo de 11/07/2026, e não entra pela porta da figura. |
| Texto acima de 190 caracteres | Não cabe na caixa; o gate de overflow reprovaria depois. |
| Campo vazio | Melhor ausente que vazio. |
| Cadeia fora de 3 a 6 etapas | Menos não é cadeia; mais não cabe na página. |

## Custo

De um a dois minutos por peça, por quem escreveu o texto e já tem os dados na
cabeça. É o preço de a figura ser confiável por construção em vez de plausível
por inferência.
