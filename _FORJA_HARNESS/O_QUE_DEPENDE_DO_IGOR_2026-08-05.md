# O que depende de você — 05/08/2026

> ## ATUALIZAÇÃO — você delegou, o conselho decidiu, e sobraram duas
>
> Ainda em 05/08 você delegou estas cinco decisões a Helena, Efesto e Diabob,
> exigindo unanimidade. Os três correram isolados e **decidiram por unanimidade
> nas cinco**. Três já foram executadas; **duas voltaram para você, e voltaram
> por decisão deles, não por omissão minha**:
>
> - **A fonte da Cafelana (item 1) — o Diabob vetou que qualquer agente
>   assinasse.** O campo `validadoPor` é nominal e governa valores em reais que
>   vão ao seu cliente. Três IAs concordando não criam responsabilidade
>   conjunta; criam aparência de rigor. Nada foi assinado, o caso segue
>   bloqueado, e isso é o resultado correto — não uma pendência esquecida.
> - **O envio ao Fábio (item 2) — decidiram enviar, e decidiram que quem envia
>   é você.** Você delegou a decisão de enviar; não delegou o ato de escrever ao
>   seu cliente. O pacote está pronto e conferido.
>
> As outras três estão feitas: medidor corrigido, porta única de produção
> implantada e diagnóstico v2 congelado com critério. Detalhe de cada uma em
> `CONSELHO_DELEGADO_5_DECISOES_2026-08-05.md`.
>
> O texto abaixo é o original, preservado para você ver o que foi decidido
> contra o quê.

---

Cinco decisões. Todas conferidas no estado vivo hoje, não copiadas do que os
planos afirmam. Cada uma traz: o que está travado, o que muda conforme você
decidir, e a minha recomendação com o motivo.

Nada aqui exige conhecimento técnico para decidir. Onde a escolha for técnica,
eu já decidi e digo o que fiz.

---

## 1. Cafelana — a fonte que governa os números (a mais cara)

**Situação medida hoje.** O caso está bloqueado. O fato que declara qual
documento governa a base econômica existe no ledger, mas está assim:

| Campo | Valor atual |
|---|---|
| `validationStatus` | `proposto` — ninguém validou |
| `dataBase` | **1996-05-31** |
| `validadoPor` | vazio |
| cenário | "valor homologado na data-base, antes de atualização" |

E o registro do caso diz que **a fonte econômica atualizada até julho de 2026
nunca foi recuperada**: o arquivo local cobre 1996 a 2004 e o link do
WeTransfer expirou.

**O que isso significa em linguagem de negócio.** O erro que o Fábio apontou em
03/08 foi construir faixas em reais sem que nenhum documento tivesse sido eleito
como governante. O harness agora impede que isso se repita — mas impedir
significa travar. Enquanto ninguém disser por escrito qual documento governa,
nenhum número econômico novo sai da Cafelana. Está travado por desenho, e o
travamento está correto.

**Suas opções.**

1. **Reobter o material de julho.** Pedir ao Fábio (ou a quem enviou) o reenvio
   do arquivo que o WeTransfer perdeu. Depois disso eu registro, confiro o hash
   contra o disco e você valida nominalmente.
2. **Eleger o laudo homologado de 1996 como base**, declarando por escrito o
   critério de atualização até hoje. É legítimo, mas precisa ser uma escolha
   explícita e registrada — não um efeito colateral de o outro arquivo ter
   sumido.
3. Manter bloqueado.

**Recomendação: a opção 1.** Validar 1996 porque é o que sobrou reproduz, em
outro nível, exatamente o erro que originou todo este trabalho — decidir com a
fonte que se tem em vez da que governa. A diferença é que agora seria uma
escolha consciente, e ela ficaria registrada com o seu nome.

**O que eu preciso de você, concretamente:** o arquivo (ou a decisão da opção 2)
e uma frase autorizando a validação nominal — seu nome e a data entram nos
campos `validadoPor` / `validadoEm`.

---

## 2. Plano 41 — aprovar o relatório e responder ao Fábio

**Situação.** Os passos 1 a 10 estão executados e revalidados. O passo 11 é o
único que sobra, e é seu: aprovar e enviar.

Os arquivos existem e estão prontos:

- `RELATORIO_EVIDENCIA_GATE_DOCUMENTAL_2026-08.md` (36,7 KB) e a versão de
  leitura em HTML (11,3 KB)
- `RELATORIO_REVISAO_CRUZADA_GATE_DOCUMENTAL_2026-08.md` — a revisão feita por
  outra família de modelo lendo o código, não o meu relatório

**O que o relatório diz, em uma frase.** O que o Fábio pediu em seis requisitos
foi implantado como controle automático, com a declaração honesta do limite: os
gates obrigam a declarar a fonte governante e conferem que cada número tem
âncora — **não julgam se a fonte sustenta o número**. Isso continua sendo leitura
jurídica humana.

**Recomendação: aprovar e enviar agora, separado da questão do item 1.** Em
03/08 você prometeu a ele que "os testes de regressão do fluxo documental estão
sendo implantados e serão reportados em separado, com evidência de execução".
Essa promessa está cumprida e tem data. Segurá-la esperando a fonte prevalente
mistura duas coisas com prazos diferentes — e a parte que está pronta é
justamente a que responde à crítica dele.

**O que eu preciso de você:** ler o HTML (é o de leitura humana, 5 minutos) e
dizer se envio na thread ou se você mesmo envia.

---

## 3. O gate visual F8-S — ligar o bloqueio, e quando

**O que mudou desde a última vez que conversamos sobre isso.** A objeção do
Diabob era que ligar o bloqueio sem uma referência congelada do padrão aprovado
era arriscado: um falso positivo travaria peça correta, com prazo correndo.
Essa referência existe desde 04/08 (`BASELINE_APROVADO.json`, três âncoras
reais), e há um canário que estraga peça aprovada de propósito e exige que o
gate acuse. O risco que ele levantou está coberto.

**Mas encontrei um dado que muda a pergunta.** Medi quantas entregas recentes
passam pela rota que tem os gates: **1 em 20**. Ligar o bloqueio hoje alcança
essa uma peça e mais nada.

**Ressalva honesta sobre esse número:** o medidor conta o mesmo arquivo várias
vezes quando ele existe em pastas diferentes (um relatório aparece 4 vezes na
lista) e inclui arquivos que não são entrega nossa. O fenômeno — a maior parte
da produção não passa pela rota — continua verdadeiro; o "5%" é indicativo, não
exato. Vou corrigir o medidor.

**Recomendação: não ligar ainda.** Ligar agora é gesto simbólico: custa pouco,
não trava nada e também não protege nada. A ordem correta é o item 4 primeiro.
Se você preferir ligar mesmo assim para não deixar a decisão pendurada, eu ligo
— o custo real é próximo de zero.

---

## 4. A decisão que vale mais: qual é a rota oficial de produção

**O achado.** Nenhum código de produção usa a entrada canônica de produção
visual. Ela é chamada apenas por testes e pela régua de qualidade. As peças
saem por outros caminhos.

Conferi de onde vieram os DOCX recentes: foram gerados pelo pipeline a partir do
template do escritório — não editados à mão no Word, como cheguei a suspeitar.
Ou seja, o problema não é gente contornando o sistema. É que **existe mais de um
caminho de gerar peça, e o que tem os gates não é o que se usa**.

É a terceira vez que esse padrão aparece, e nas três vezes a descoberta veio de
alguém investigando outra coisa por acaso. Já instalei um medidor permanente
disso.

**A escolha é sua porque é de política da fábrica, não técnica:**

1. **Rota única obrigatória** — eu elimino os caminhos alternativos e faço a
   entrada canônica ser o único jeito de gerar peça. Mais seguro, e por algumas
   semanas mais atritado: tudo que hoje sai por atalho vai reclamar.
2. **Rota preferencial** — mantenho os caminhos, mas todos passam a chamar os
   mesmos gates antes de gravar. Menos atrito, e a garantia depende de eu não
   esquecer nenhum caminho novo no futuro.
3. Deixar como está e continuar apertando os gates que quase ninguém percorre.

**Recomendação: a 1.** A opção 2 é a que a fábrica já tentou implicitamente, e o
resultado é o que estamos medindo. A opção 3 é a que produziu vinte dias de
edição visual parada sem ninguém notar. O atrito da 1 é real, mas é um atrito que
aparece — que é a diferença que importa.

---

## 5. Plano 40 — o piloto do diagnóstico v2 segue?

**Situação.** O plano-mestre diz, em uma seção, que as cem perguntas continuam
obrigatórias para caso novo; e diz, em outra, que uma versão v2 do diagnóstico
substitui essa cota nos ciclos novos. Fui conferir no código: **a versão v2 não
existe em lugar nenhum** — nem chave, nem configuração, nem despacho. E o
próprio plano manda que versão desconhecida falhe.

Na prática, se o piloto começasse hoje, os dois regimes coexistiriam sem nada
que os separasse.

**Suas opções:** (a) o piloto do v2 vai acontecer e eu implemento a separação
agora; (b) o v2 fica congelado e eu corrijo o plano para não prometer o que não
existe.

**Recomendação: (b), congelar e corrigir o texto.** O diagnóstico das cem
perguntas já tem um problema conhecido e medido — virou formulário preenchido em
vez de exploração real. Trocar o motor antes de entender por que o atual
degradou tende a produzir o mesmo resultado com nome novo. Prefiro atacar a
causa e só então propor substituto.

---

## O que NÃO depende de você — vou fazer sem perguntar

- Corrigir o medidor de adoção da rota (duplicatas e arquivos que não são
  entrega nossa).
- Corrigir o texto do plano 40 para não prometer o diagnóstico v2, assim que
  você responder o item 5.
- Os metadados do template levam o nome de uma terceira pessoa (`thais mulati`)
  para dentro de toda peça gerada. Vou sanitizar — é higiene, não decisão.
- A reconciliação entre `AGENTS.md` e `CLAUDE.md` (os dois documentos que
  orientam Claude e Codex divergiram: 78 trechos só num, 47 só no outro). Vou
  propor a versão reconciliada e te mostrar antes de aplicar.

---

## Resumo de uma linha por item

| # | Decisão | Minha recomendação |
|---|---|---|
| 1 | Fonte governante da Cafelana | Reobter o material de julho; não validar 1996 por falta de opção |
| 2 | Enviar o relatório do plano 41 ao Fábio | Enviar agora, separado do item 1 |
| 3 | Ligar o gate visual bloqueante | Esperar o item 4; custo de ligar agora é baixo, benefício também |
| 4 | Rota única de produção | Rota única obrigatória |
| 5 | Piloto do diagnóstico v2 | Congelar e corrigir o plano |
