# S2 e S4 — por que estão em zero, e por que a campanha planejada não resolveria

**Data:** 2026-08-05. **Método:** dois agentes independentes, um procurando a verdade externa e
outro tentando provar que ela é dispensável. Nenhum dos dois escreveu código de produção.

## O que estava planejado, e está errado

O `LAPIDACAO_VEREDITO_FINAL` deixou como próxima campanha: *"comparar o papel e o pedido
declarados contra o que o próprio caso registra em `FORJA_CASE_MANIFEST.json`"*.

**Esse plano não é executável, porque o manifesto não registra nada disso.** As chaves são
`caseId`, `demandId`, `inputs`, `n4SourceRegistry`, `n4Audit`, `f1Delta`, `mode`, `spec*`,
`createdAt`, `eventRevision`. Nenhuma declara parte, papel ou pedido. Eu escrevi aquele plano
sem abrir o manifesto.

## A medição

Varredura dos 27 casos com manifesto e dos artefatos de fase F2 a F7:

| Declaração procurada | Casos que a têm |
|---|---|
| quem é a cliente | **0 de 27** |
| papel processual da cliente (agravante? agravada?) | **0 de 27** |
| direção do pedido da cliente (provimento? desprovimento?) | **0 de 27** |
| tipo de peça (`product`, em prosa livre) | 7 de 27 |

O campo `product` é o único sinal existente, e não serve: está em 7 casos, é texto livre
(`"memoriais de apelação"`, `"pacote interno de apoio à reunião Cafelana"`) e mesmo quando
preenchido não distingue apelante de apelado.

## A consequência, que é o achado

**S2 e S4 não estão em zero porque falta um gate. Estão em zero porque falta um FATO.**

Nenhuma verificação pode conferir a coerência de um texto contra uma verdade que o sistema
nunca registrou. As duas mutações são trocas globais e simétricas — depois delas o texto
permanece internamente coerente, e a coerência interna é tudo o que existe para ler. Foi
exatamente isso que condenou `forja_coerencia_processual`: não era gate mal calibrado, era o
único gate possível sem o fato, e por isso reprovava peça legítima.

Um segundo agente foi encarregado de me refutar, construindo um detector só-texto com sete
hipóteses (assimetria de gênero, frequência relativa de papéis, papel no fecho versus no
endereçamento, termos direcionais não mutados). Nenhuma matou mutante. **A refutação dele é
fraca por amostra** — exercitou 4 mutantes S2 e 1 S4, não os 23 e 12 da bateria — e vale como
indício, não como prova. O que decide é a contagem acima.

Uma razão adicional apareceu na medição e merece registro: o texto que a bateria muta vem de
`CANONICAL_TEXT_FROM_FINAL_DOCX.txt` e similares, isto é, **da saída da própria peça**. Qualquer
artefato derivado dela seria mutado junto. A verdade precisa nascer fora da redação — do comando
do caso ou da decisão impugnada nos autos — ou o gate nasce cego por construção.

## O que fechar S2 e S4 exigiria de verdade

1. **Criar a declaração**: cliente, papel processual e direção do pedido, por caso, em campo
   estruturado com vocabulário fechado.
2. **Lastreá-la em fonte externa à redação**, com sha256 no `n4SourceRegistry` — o comando do
   caso ou a decisão impugnada, nunca a minuta.
3. **Só então** o gate, que passa a ser trivial e robusto: o texto pede na direção que a
   declaração afirma?

O passo 1 muda o protocolo de entrada de caso, e é aí que está o custo real. É decisão do Igor,
com Helena e Cícero, não reparo de engenharia — e tem um modo de falha conhecido nesta casa:
**campo declarativo preenchido à mão vira formulário**, que foi precisamente o que aconteceu com
o F2A (14 árvores reais, 1 consequência distinta em 100 perguntas). A declaração só vale se for
derivada da fonte e conferida contra ela, não digitada.

## O que NÃO fazer

Construir o gate agora sobre os 7 casos com `product` preenchido. Seria gate computado sobre
conjunto quase vazio, com aparência de progresso e nenhuma proteção — o primeiro item da lista
de falso progresso que o avaliador desta campanha foi instruído a rejeitar.
