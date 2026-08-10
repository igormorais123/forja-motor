# 0004 — O revisor padrão da FORJA é o `gpt-5.6-sol` no esforço alto

**Data:** 10/08/2026
**Quem decidiu:** o titular do harness (Igor), por ordem expressa.
**Alcance:** toda a FORJA, em qualquer fase e em qualquer caso.

## A decisão

Onde a esteira **revisa**, o modelo é **`gpt-5.6-sol` no esforço `high`**, pela
assinatura OAuth do Codex. Onde a esteira **produz** pelo Codex, permanece o
`gpt-5.6-luna` no esforço `max`, decidido em 06/08/2026 — esta ficha supera
aquela ordem **apenas na parte de revisão**.

Revisão, aqui, é o que confere trabalho pronto: revisão cruzada entre famílias,
red team, auditoria de gate, conferência de citação e de número. Redigir a peça
continua no modelo de produção.

## Por que

A escolha não é de preferência, e sim de resultado medido no mesmo dia. Na
revisão cruzada de um memorial em liquidação, o Sol encontrou **três P0 que o
produtor não via**:

1. um QA visual declarado como concluído sobre um render que já não existia no
   disco — o produtor havia inspecionado treze páginas e o arquivo tinha nove;
2. uma contradição interna criada por decisão do próprio produtor: a peça
   sustentava um critério de conversão cambial e, no fecho, declarava
   integralmente mantido o capítulo que pedia o critério oposto;
3. uma contagem que vinha de deduplicação destrutiva, colapsando oito pares de
   operações distintas com o mesmo número em anos diferentes.

Os três têm a mesma assinatura: são erros que **não levantam exceção** e deixam o
texto internamente coerente. Nenhum gate lexical discorda deles. É exatamente a
classe de defeito para a qual um revisor de outra família serve, e o perfil já
estava descrito no catálogo de modelos como `revisao_adversarial` e
`achar_erro_do_opus`.

## O que foi feito, e não apenas escrito

- `forja_modelos.py`: constantes `CODEX_MODELO_REVISAO_FORJA` e
  `CODEX_ESFORCO_REVISAO_FORJA`, separadas das de produção.
- `forja_revisao_cruzada.py`: a rota. Ela **lê as constantes**, não repete o nome
  do modelo — senão mudar a ordem deixaria o executor para trás.
- `test_forja_cursor_grok.py`: regressão das constantes, do executor e da
  exigência de que **revisor e produtor sejam distintos**. Se um dia
  coincidirem, o gate `cross_model_review_verified` passaria a aprovar o
  produtor revisando a si mesmo.
- `CLAUDE.md`, `AGENTS.md` e a referência de modelos da skill `forja`.

## As quatro armadilhas que o executor fecha

Todas medidas em 10/08/2026, e todas produzem falha silenciosa:

1. **Sem `--cd` explícito** o Codex não enxerga o diretório e responde que o
   sandbox bloqueou a leitura. A mesma pergunta, com e sem a flag, devolveu
   "não verificável" e a resposta certa. Parecer sem fonte tem cara de parecer.
2. **MCPs da sessão** entram na chamada, estouram o orçamento de contexto das
   skills e disparam ferramentas alheias à revisão.
3. **Sandbox somente leitura**: revisor que altera artefato deixa de ser
   independente do objeto revisado.
4. **Prompt por argumento, nunca por stdin** — no Codex. **No Cursor é o
   inverso**, porque o wrapper é um `.cmd` e o cmd.exe corta o argumento na
   primeira quebra de linha. Dois binários com armadilhas opostas: uniformizar os
   dois quebra um deles.

## O que esta decisão não faz

Não torna a revisão cruzada opcional nem substitui a auditoria F7, o conselho de
Helena, Cícero e Diabob, ou a revisão humana. Também não muda o gate de
proveniência do Diabob, que continua no Grok 4.5 pela assinatura do Cursor: a
terceira família existe para que o contraditório não venha de quem escreveu nem
de quem revisou.
