# Conselho delegado — as cinco decisões humanas do plano 41

**05/08/2026.** O Igor delegou formalmente as cinco decisões que estavam
represadas em `O_QUE_DEPENDE_DO_IGOR_2026-08-05.md`, com o mandato expresso de
que Helena, Efesto e Diabob decidissem em unanimidade, "conforme meus interesses
e o melhor para mim".

Os três correram **isolados**, sem ver o parecer um do outro, cada um com o
ângulo da sua função e a ordem de conferir no código antes de afirmar.

## Ressalva de integridade, registrada antes do conteúdo

O Efesto encerrou o parecer dele afirmando que *"Helena (estratégia) e Diabob
(auditoria) concordam com a evidência medida e as recomendações"*. Ele não podia
saber disso — os três rodaram em paralelo e isolados, e no momento em que ele
escreveu, nenhum dos outros dois tinha entregue. A frase foi descartada e a
unanimidade foi apurada por comparação dos veredictos, um a um.

É o mesmo defeito da primeira tentativa de conselho, em 04/08, quando o
consolidador anunciou "o que os quatro concordam" tendo recebido dois pareceres.
Vale a lição que ficou de lá: **formato prescrito vira fato inventado quando a
realidade entrega menos do que o formato espera.** Ninguém mente de propósito; o
molde é preenchido.

## O que os três decidiram

| # | Decisão | Helena | Efesto | Diabob | Unânime? |
|---|---|---|---|---|---|
| 1 | Fonte governante da Cafelana | Reobter julho; se irrecuperável em 48h, eleger 1996 por escrito | Reobter julho | **VETO** a IA assinar; Igor valida ou fica `proposto` | **Sim** |
| 2 | Relatório do plano 41 ao Fábio | Enviar agora | Aprovar e enviar agora | Decisão delegada; **execução do envio externo não** | **Sim** |
| 3 | Ligar o gate visual F8-S | Não ligar; deferir para depois da 4 | Não ligar ainda | Não ligar, **mas corrigir o medidor antes** | **Sim** |
| 4 | Rota de produção | Rota única obrigatória | Rota única obrigatória | Rota única, **urgente** | **Sim** |
| 5 | Piloto do diagnóstico v2 | Congelar com critério explícito | Congelar e corrigir o plano | Congelar, **mas investigar a causa** | **Sim** |

Unanimidade nas cinco. Mas as três colunas não são redundantes: em quatro das
cinco, alguém acrescentou uma condição que os outros não viram.

## As condições que mudaram a execução

**Diabob vetou a decisão 1 pelo ângulo certo, e o veto é vinculante.** O campo se
chama `validadoPor` e é nominal. Três agentes concordando não criam
responsabilidade conjunta — criam aparência de rigor. Se o campo fosse
preenchido com nomes de personas, isso seria falsificação nominada, e num
documento que governa valores em reais destinados a um cliente real. **Nenhum
agente assinou nada.** `F-FP-001` continua `proposto` e a Cafelana continua
bloqueada, que é o resultado correto.

**Diabob separou decidir de executar na decisão 2, e a separação se sustenta.** O
§ 6 do próprio plano 41 diz que "qualquer envio externo permanece gate de
governança, não é inferido pelo código nem executado automaticamente". O Igor
delegou a decisão de enviar; não delegou o ato de escrever ao cliente dele. O
pacote fica pronto; o envio é do Igor.

**Diabob acusou o assistente de documentar problema em vez de resolver, e tinha
razão.** Sobre o medidor de adoção da rota: eu registrei que ele contava
duplicatas e segui adiante usando o número ruim para justificar adiar o gate.
Isso foi corrigido na mesma sessão — desduplicação por SHA-256 do conteúdo, com
a marca de rota procurada em todas as cópias da obra. O número real, sobre 40
obras: **1 em 40, 2%** (20 cópias colapsadas na janela). O fenômeno era pior do
que o medidor ruim mostrava, não melhor.

**Helena fixou prazo na decisão 1 e critério de descongelamento na 5.** Sem
prazo, "reobter o arquivo" é adiamento; sem critério, "congelar o v2" também.
Ambos entraram: gatilho de 48h na primeira, três condições cumulativas na quinta.

## O que foi executado a partir daqui

| Decisão | Execução | Estado |
|---|---|---|
| 1 | Nada assinado. Caso segue `blocked`, `F-FP-001` segue `proposto` | **cumprida por omissão deliberada** |
| 2 | Relatório e revisão cruzada prontos e conferidos; envio não realizado | **pronta, aguardando o Igor** |
| 3 | Medidor corrigido; gate permanece em observação | **cumprida** |
| 4 | Porta única implementada em `PecaVisual.salvar()` | **cumprida** |
| 5 | Bloco de congelamento inscrito na § 21 do plano 40 | **cumprida** |

## A decisão 4, que era a que valia mais

O Efesto mediu em vez de estimar, e o número é o achado: existem **seis caminhos**
capazes de gerar DOCX pela `PecaVisual` — a entrada canônica `forja_visual_build.py`
e cinco scripts `build_docx.py` dentro de pastas de caso. Só o primeiro chamava o
verificador. É literalmente a rota do incidente Cafelana, ainda aberta.

A implementação **não deletou os cinco scripts**, apesar de a formulação da
decisão sugerir eliminação. Eles são registro histórico dentro de `state/`, e
apagá-los seria destrutivo sem fechar buraco nenhum: nada impede o sexto script
de nascer amanhã. Fechou-se a **porta** por onde todos os seis passam
obrigatoriamente — `PecaVisual.salvar()` — e ali o verificador agora roda sempre.

O buraco era maior do que o mapeado. `salvar()` já rodava os gates econômicos
L9–L13, mas com um `return` antecipado quando a peça **não tem conteúdo
econômico**: uma petição sem valor em reais, saindo por rota ad hoc, atravessava
sem nenhuma conferência — nem placeholder esquecido, nem persona interna, nem
origem operacional vazada. O gate econômico estava certo em ser condicional; o
erro foi não existir nada incondicional atrás dele.

### Três coisas que a construção me ensinou, e uma que quase me enganou

**A que quase me enganou.** A primeira versão da porta procurava a chave
`severidade` no achado do verificador. A chave é `sev`. O gate ficou cego, e a
calibração contra 25 obras reais devolveu **"zero peças bloqueadas"** — número
que eu quase registrei como prova de que a trava era segura. Era prova de que ela
não enxergava nada. É o gate verde por cegueira, que esta fábrica documenta há
meses, cometido por quem estava construindo a defesa contra ele.

**A classificação de tipo não é cosmética.** Com a chave corrigida, a medição
acusou 14 entregáveis com placeholder e 1 com origem operacional vazada — uma
crise de qualidade. Não existia: eu havia classificado tudo como petição, e
estudo interno carrega marcador de lacuna por desenho. Classificando pelo tipo
real, os três achados graves **desapareceram inteiramente**. Os gates estavam
certos e a produção estava limpa; o defeito era da minha medição. Um gate sem
essa distinção acusaria a fábrica todo dia.

**O gate de estilo discrimina, e por isso o achado é real.** Sobra
`G10-escrita-humana`, que reprova 18 das 25 obras recentes. Testei contra o
padrão aprovado: a `IMPUGNACAO_AGINT_CAFELANA_V8`, peça entregue e aprovada,
passa com **zero achados** — enquanto a V4 que ela superou reprova. O gate não
está reprovando o padrão da casa; está apontando defeito real na produção
corrente. Os 72% são achado de qualidade, não ruído.

**Por isso a porta separa duas famílias, e a separação foi medida.** Bloqueiam os
P0 de correção e identidade — placeholder, persona, origem operacional,
regimento, lastro —, e **zero das 25 obras recentes reprova neles**: fechar essa
porta não trava uma única peça real. Não bloqueia, mas grava no laudo, a família
de estilo: transformar um defeito de redação em parede pararia a fábrica, o que a
casa proíbe desde a bronca de 10/07. Nada é dispensado — o laudo
`<peça>_PORTA_UNICA.json` é gravado ao lado de toda peça, passe ou não, e o
número foi levado ao Igor como achado aberto.

### O que a porta não faz

Ela garante que toda peça atravessa o verificador. Não garante que o verificador
tenha razão, nem julga se o texto sustenta o que afirma. Isso continua sendo
auditoria F7 e leitura humana. E ela não impede que alguém escreva
`doc.save()` direto do `python-docx` sem passar pela classe — esse caminho
existe, é coberto por outra catraca, e continua sendo vigilância de revisão.
