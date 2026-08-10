# Lições da FORJA — como consultar

O que a casa aprendeu está em `../RETROSPECTIVAS.md`: 382 lições em 1.104
linhas, na ordem em que os erros aconteceram. É um bom registro e um péssimo
índice — ninguém lê 1.104 linhas antes de escrever uma função, e foi por isso
que a mesma coisa já foi redescoberta mais de uma vez.

Esta pasta existe para tornar o acervo consultável. Ela não substitui o arquivo:
os índices apontam para a linha, e a lição se lê na fonte.

## Os três caminhos

| se a sua pergunta é | use |
|---|---|
| "o que a casa já sabe sobre *isto*?" | [`INDICE_TEMATICO.md`](INDICE_TEMATICO.md) — 15 temas |
| "o que aprendemos naquele caso / naquele dia?" | [`INDICE_CRONOLOGICO.md`](INDICE_CRONOLOGICO.md) — 32 rodadas |
| "existe lição sobre esta palavra?" | `python ../forja_licoes.py --buscar <termo>` |

A busca varre título **e** corpo, e não por capricho: só no título, `--buscar
prazo` devolvia zero num acervo com nove lições sobre contagem de prazo. Índice
que só encontra quem já sabe o nome do que procura não resolve esquecimento.

## Comandos

```
python forja_licoes.py                 # o retrato: quantas, quantas ancoradas
python forja_licoes.py --temas         # quantas lições em cada tema
python forja_licoes.py --tema visual   # as lições de um tema
python forja_licoes.py --buscar hash   # acha pelo assunto, no título e no corpo
python forja_licoes.py --orfas         # lições sem nada que as faça reprovar
python forja_licoes.py --ambiguas      # citações em código que não decidem
python forja_licoes.py --documentar    # reescreve os dois índices desta pasta
python forja_licoes.py --indexar       # grava o índice legível por máquina
```

Os dois índices são **gerados**. Não os edite: a fonte é `RETROSPECTIVAS.md`, e
uma correção feita aqui desaparece na próxima geração. Depois de acrescentar
lição ao arquivo, rode `--documentar`.

## O que ler antes de confiar no índice

**O tema é navegação, não autoridade.** Ele vem de vocabulário declarado no
código, por termo que aparece no texto da lição. Diz onde procurar; não diz o
que a lição decide. Leia a lição antes de citá-la.

**107 lições estão em "sem tema".** Não são piores que as outras — são as que o
vocabulário não alcançou. Ficam listadas em vez de sumirem, porque lacuna
visível é lacuna que alguém pode fechar.

**Não há tema de prazo, e a ausência foi medida.** A palavra aparece na fábrica
em "prazo de revalidação", "prazo interno", "prazo do ciclo" — mais fora do
assunto processual do que dentro. O tema devolvia três lições e as três eram de
outra coisa. Para prazo processual, use `--buscar prazo`; rótulo errado é pior
que rótulo nenhum.

**A numeração não é confiável como referência.** 48 números designam mais de uma
lição, porque a sequência foi reiniciada várias vezes ao longo do arquivo. Nove
das 27 citações que o código faz por número apontam para número duplicado — não
erram o alvo, ficam sem alvo. Cada lição tem por isso um `id` estável derivado
do título (`licao-<hash>`), que não muda quando o arquivo cresce; é ele que
serve para referência nova.

**Coluna "o que a faz reprovar".** Diz se existe código, teste ou contrato de
fase que cita aquela lição — ou seja, se ela virou alguma coisa que trava
sozinha. A esmagadora maioria não virou, e isso é esperado: muita lição é
julgamento humano e deve continuar sendo. O que não pode é ninguém conseguir
responder quais são quais.

## Como isso se mantém honesto

`test_forja_licoes.py`, no baseline, é catraca: os tetos de ambiguidade são o
estado medido em 10/08/2026 e só podem descer. Citação nova para número já
duplicado reprova; citação para lição inexistente reprova sempre.
