# Triagem das reprovações do censo — 04/08/2026

O censo de disparo mediu 19 reprovações sobre 63 tentativas reais do acervo. Reprovação
não é defeito até alguém ler o caso: metade delas era erro do gate, e um gate que reprova
trabalho bem-feito custa mais caro que um gate ausente, porque ensina o operador a ignorar
o sinal. Este documento separa as duas coisas, nominalmente.

## Eram defeito do gate — corrigidos, com contraprova em regressão

**1. `p0_zero` — severidade escondida em JSON serializado (2 casos)**
O F7 do Cafelana declara 48 P0 e traz 49 achados cuja severidade vive dentro da string
`detail = '{"severity": "P0", ...}'`. Lendo só o topo do achado, o gate via zero P0 e
chamava de contraditória uma contagem correta. Era o sexto dialeto do artefato. `forja_p0.py`
passou a desempacotar `detail`/`payload`/`raw`; três casos novos em `test_forja_p0.py`.

**2. `jurisdictional_question_defined` — o gate cobrava o rótulo, não a substância (5 casos)**
Cinco blueprints reais cumprem a regra da casa com outro título: "Pergunta central" na
Natura Cabreúva, "Pergunta decisória" no Cafelana. E o Cafelana não tem juízo a quem
perguntar — o produto ali é uma reunião com a AGU. A regra de 08/07 exige uma frase dizendo
o que se pede a quem decide; exigir a palavra "jurisdicional" era cobrar vocabulário.
O reconhecedor passou a aceitar a família de rótulos, mantendo a exigência de frase: título
sem texto embaixo continua reprovado, senão bastaria escrever o cabeçalho.

**3. `adversarial_decisions_recorded` — o censo pareou tentativa descartada (1 caso)**
O hash da auditoria no Cafelana confere no par promovido. O que divergia era uma tentativa
descartada, confrontada com a estratégia vigente — divergir é a definição de ter sido
descartada. Segunda vez que este censo inventou um `fail` de hash por parear errado; a
primeira já estava documentada dentro da própria função que faz o pareamento.

## São defeito real — dependem de decisão sua

**4. `regimento_available` — Cafelana não declara regimento algum (2 tentativas)**
A F3 do caso não aponta arquivo de regimento interno. Considerar o regimento do tribunal é
regra inviolável da casa desde 06/07/2026. O caso é uma reunião com a AGU, e é plausível que
não haja tribunal envolvido — mas isso precisa estar **escrito** no mapa de fontes, não
inferido pelo silêncio. Decisão: declarar a inaplicabilidade por escrito, ou juntar o
regimento.

**5. `facts_rechecked` — Cafelana declara que os fatos NÃO foram reconferidos**
O próprio artefato diz que o recheque não ocorreu, e a fase reportou o gate como aprovado.
É a autovalidação em estado puro, capturada em caso real. A tentativa está `blocked`, então
nada saiu — mas a contradição entre o que o artefato diz e o que a fase declarou é o padrão
que esta frente inteira existe para eliminar.

**6. `critical_facts_sourced` — um caso sem lastro de fato**
No VerifACT, 6 de 6 fatos não declaram lastro nem se declaram bloqueados.

> **Correção deste laudo, mesma tarde.** A primeira versão listava aqui um segundo caso — o
> Nylton, com "ledger da F3 sem fato nenhum". Era falso. O ledger existe, tem nove fatos e
> traz localizador processual em cada linha; ele só existe em **markdown**, e o gate abria
> apenas a forma JSON. Um censo de formas construído depois derrubou o achado. Fica o
> registro de que este documento também precisou ser auditado.

**7. Conselho Helena/Cícero — pareceres sem recomendação numerada (3 casos)**
Casos Nylton e Vale Trading: os pareceres existem e não trazem recomendações que possam ser
decididas uma a uma, e o arquivo de deliberações não registra decisão identificável. O
protocolo de 09/07 exige que o redator registre acatada/rejeitada/por quê para cada
recomendação — sem numeração, não há o que registrar.

## Estado após a triagem

Das 19 reprovações, **9 eram do instrumento** e estão corrigidas com contraprova; **10 são
reais** e se concentram em três casos: Cafelana (reconstrução, tentativas bloqueadas),
VerifACT e Nylton. Nenhuma delas está em peça entregue ao cliente.

Uma décima reprovação, o `regimento_available` do Vale Trading, desceu de `fail` para `warn`:
o mapa declara o Regimento do TRF4 em prosa, com a emenda posterior nomeada, e não aponta o
arquivo. Cumpre a regra e não permite reconferir a versão daqui — que é exatamente o que
`warn` significa.

A lição que fica para o próximo gate: medir primeiro, calibrar contra o acervo, e tratar
toda reprovação de trabalho aprovado como hipótese de defeito do gate até prova em contrário.
E a lição que este documento aprendeu sobre si mesmo: **um laudo de triagem também é um
artefato, e também erra.** Cinco dos nove erros do instrumento eram a mesma coisa — o gate
lia JSON e o artefato era markdown —, e essa classe inteira só apareceu quando alguém parou
de conferir caso a caso e mediu a FORMA dos artefatos do acervo.

## Revalidação após a correção do instrumento — 04/08/2026

O censo foi executado novamente contra 63 tentativas. Os seguintes pontos mudaram de estado:

- **Cafelana — regimento:** as duas reprovações pertencem a tentativas históricas. O mapa
  promovido atual declara o TRF1 e `Cafelana/REGIMENTO_INTERNO_TRF1.md`; a F3 promovida passa.
  Os registros antigos permanecem no histórico e não são reescritos.
- **Cafelana — recheque:** a tentativa de reparo declara `factsRechecked: true`. O caso ainda
  está bloqueado por avaliação semântica independente `T-F4-004`, recibos humanos e perguntas
  materiais pendentes; o reparo não autoriza promoção.
- **VerifACT — fatos críticos:** o ledger já traz `sourceIds`. O gate passou a reconhecer essa
  forma canônica e `critical_facts_sourced` passou em todas as seis ocorrências medidas; não
  houve alteração do conteúdo jurídico do caso.
- **Vale — conselho:** o registro JSON com `decisions[]` agora é lido. Ele deixou de ser
  contado como arquivo ausente; a falta de responsável humano continua visível como P1.
- **Nylton — conselho:** permanece pendente. Os artefatos históricos têm pareceres sem
  recomendações numeradas e resumo de decisão sem decisão por recomendação. Para fechar, é
  necessário novo F4 com recomendações numeradas e deliberação correspondente, sem fabricar
  responsável ou decisão.

O recomputo do lastro F7 também revelou quatro vereditos reais de `fact_grounding_verbatim`:
três no Cafelana, por fontes ainda não reabertas ou pendência declarada, e um no Vale, que
também tem base econômica sem fonte prevalente. Esses são bloqueios de conferência/documentação,
não defeitos que o código possa preencher.
