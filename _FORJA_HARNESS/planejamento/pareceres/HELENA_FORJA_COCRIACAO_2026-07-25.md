# Parecer Helena Strategos — FORJA-COCRIACAO-v1

**Objeto:** `33_PRD`, `34_TDD`, `35_ROADMAP_E_GATES`.
**Data:** 2026-07-25. **Modo:** análise profunda 8+1.
**Veredito:** **APROVADO COM REORDENAÇÃO.** O desenho está certo. A ordem está errada.

---

## 1. Status real e recomendação direta

O plano é tecnicamente sólido, epistemicamente honesto e — coisa rara aqui — encolheu em vez de crescer a cada revisão. Aprovo o conteúdo.

Rejeito o **sequenciamento**, por três razões de negócio:

1. Quatro ondas passam antes que uma única petição melhore. O comprador não vê nada nesse intervalo.
2. A hipótese central do Eixo 1 — que o Fábio responde a uma consulta — **nunca foi testada**, e custa uma hora testá-la.
3. O único item com receita direta identificável foi empurrado para o fim por uma decisão de risco tomada com granularidade errada.

**Recomendação:** insira uma Onda −1 de duas semanas, antes da Onda 0, com três entregas que não dependem de nenhuma linha do plano.

---

## 2. Achado principal

**O plano trata "jurimetria J-B" como um bloco único de alto risco. São dois produtos com perfis de risco opostos, e um deles é inofensivo.**

- **J-B(julgador)** — série temporal de magistrado, viés correlacionado a escritório adversário, achado levado aos autos. Radioativo. Exposição de art. 34 do EAOAB e art. 41 da LOMAN. A contenção proposta está correta e deve ficar onde está: no fim, sob autorização.
- **J-B(acordo)** — comparação de deságios em acordos análogos com o poder público, para demonstrar vantajosidade e risco de responsabilização do gestor. Isto é **análise econômica de proposta**. Qualquer consultoria faz. Nenhum juiz é analisado. Nenhuma conduta é imputada. O sujeito da análise é uma proposta, não uma pessoa.

Empacotar os dois sob a mesma trava custou ao plano o item de maior valor comercial imediato — e há um caso vivo na fila esperando por ele: **CASO-07/CASO-07**, que é literalmente uma negociação com o poder público sob pressão regulatória.

[INFERÊNCIA] Este é o único componente do conjunto que gera receita atribuível em prazo curto sem depender de mandato novo.

---

## 3. Evidência e fundamentação

**[FONTE — fila operacional, 2026-07-25]** 49 casos, 10 ativos, 39 entregues em 7 dias. Seis casos parados 56h em F0 com P1 aberto. Um caso em `draft_awaiting_review` parado **344 horas**.

Leitura: a fábrica não tem problema de vazão — tem cauda de casos travados. O plano acrescenta duas subfases (F2-B, F3-B) a montante. **Adicionar etapa a um sistema com cauda travada aumenta a cauda**, salvo se as etapas forem condicionais — e o TDD as declara condicionais, o que corrige o risco. Registro como mitigado, não como ausente.

**[FONTE — entrevista, 2026-07-25]** O titular não mencionou custo, prazo ou tecnologia uma única vez em 48 minutos. Mencionou desmoralização por pesquisa falsa. O critério de compra é confiabilidade auditável.

**[FONTE — `_MODELOS` vazio; catálogo N4 com 24 conchas sem produção]** Dois indicadores de um mesmo padrão organizacional: a FORJA declara mais do que consuma. O plano corrigiu isso na superfície nova. Não corrigiu o passivo.

**[LACUNA — sem dado]** Não existe medida de **taxa de resposta do Fábio a pedido de esclarecimento**. Todo o Eixo 1 repousa numa frase dita em entrevista: *"cabe a quem endereçou a demanda responder os questionamentos"*. É declaração de princípio de um advogado ocupado, colhida em contexto de conversa filosófica. Não é dado de comportamento.

---

## 4. Mecanismo causal

Por que a reordenação funciona, e não é apenas impaciência:

**O plano é uma aposta em cadeia.** Onda 0 → 1A/1B → 2 → 3. Cada onda consome capital político e orçamento de contexto, e nenhuma produz sinal externo até a Onda 3. Se a premissa do Eixo 1 for falsa — se ele não responder —, isso só será descoberto na Onda 3, depois de todo o investimento.

**Testar barato o que é caro de errar** inverte a curva. Um e-mail manual de consulta, redigido à mão sobre um caso real da fila, testa a hipótese comportamental mais cara do plano ao custo de uma hora. E produz, de quebra, o corpus de calibração do gabarito da consulta.

O mesmo vale para a demonstração de recusa: ela **não precisa do plano**. A FORJA já bloqueia citação sem íntegra, já tem trust store humano, já tem scan anti-injeção. A demo existe hoje; falta gravá-la.

---

## 5. Contra-hipóteses

### Contra-hipótese 1: a consulta manual queima a única chance de causar boa impressão

**Argumento:** um e-mail de perguntas mal calibrado, enviado antes de o sistema estar pronto, ensina ao Fábio que a FORJA pergunta o óbvio. Ele disse que perguntar acelera — mas isso vale para perguntas boas. Uma pergunta respondível pelos autos, na primeira interação, envenena a percepção do produto inteiro, e percepção não tem rollback.

**Teste observável:** submeter a minuta manual ao gabarito do `35`, §3, e ao filtro do acervo antes de enviar. Se qualquer pergunta falhar no `acervoProbe`, não enviar até 2026-08-01.

**Gatilho de reversão:** se a revisão interna não conseguir produzir 5 perguntas que passem nos quatro filtros sobre um caso real, a hipótese do Eixo 1 já está respondida negativamente — e o problema não é o Fábio, é a nossa leitura dos autos. Nesse caso, priorizar 1B e adiar 1A.

### Contra-hipótese 2: J-B(acordo) não é tão inofensivo quanto eu afirmo

**Argumento:** a fala do titular liga o benchmarking de deságio a *"o gestor público pode ser responsabilizado perante o Tribunal de Contas da União"*. Isso não é análise econômica neutra — é **construção de constrangimento contra um agente público identificável**. O mesmo motor retórico do J-B(julgador), com outro alvo. Minha separação pode ser cosmética.

**Teste observável:** parecer do Cícero especificamente sobre a hipótese de o achado ser usado em manifestação dirigida ao gestor. Prazo: 2026-08-08.

**Gatilho de reversão:** se o Cícero apontar exposição relevante quando o achado for endereçado ao gestor, restringir J-B(acordo) a **uso interno de precificação e recomendação ao cliente**, sem entrar em manifestação externa. Isso preserva a maior parte do valor comercial e elimina a exposição.

### Contra-hipótese 3: reordenar é otimizar para a demo e não para o produto

**Argumento:** priorizar demonstração e teste comportamental é comportamento de vendedor. O valor durável do plano está na Camada 2 — ratio, moldura fática, operação declarada. Antecipar a vitrine pode consumir o mês e adiar o ativo.

**Teste observável:** a Onda −1 tem teto de duas semanas e nenhuma entrega de código de produção. Se em 2026-08-08 ela não estiver fechada, foi vitrine e cortamos.

**Gatilho de reversão:** estouro de prazo da Onda −1 devolve prioridade integral à Onda 0 e 1B.

---

## 6. Calibração de confiança

| Proposição | Confiança | Base |
|---|---:|---|
| O desenho técnico do plano está correto e não precisa de mudança material | 0.85 | três revisões adversariais convergentes; superfície decrescente |
| O Fábio responde a uma consulta bem formulada em até 5 dias úteis | **0.45** | [LACUNA] — nenhuma base observacional; a frase da entrevista é declaração de princípio, não comportamento medido |
| A demonstração de recusa altera materialmente a percepção dele | 0.75 | ele nomeou desmoralização por pesquisa falsa de forma espontânea e repetida |
| J-B(acordo) é separável de J-B(julgador) sem exposição relevante | 0.60 | reduzida pela contra-hipótese 2; depende do parecer do Cícero |
| O mapa do destinatário fecha a falha do CASO-04 | 0.80 | falha documentada; dado disponível no TeiaJus; risco residual é frescor de composição |

Não atribuo probabilidade a "o plano gera peça melhor". Não há base. É exatamente o que as ondas 2 e 3 existem para descobrir, e a revisão adversarial Fable já nomeou isso como risco empírico irredutível.

---

## 7. Cenários

**Base (p ≈ 0.55).** Onda −1 fecha em duas semanas. O Fábio responde parcialmente à consulta manual — responde ao que é decisão dele, ignora o que é diligência. Isso já valida o desenho, com ajuste: separar consulta de *decisão* de consulta de *diligência*, e mandar só a primeira a ele. Ondas 0 e 1B seguem. Primeiro ganho visível em setembro.
*Sinal:* resposta em 3-7 dias, cobrindo o Bloco 5 e ignorando o Bloco 3.

**Otimista (p ≈ 0.2).** Ele responde com entusiasmo e devolve teses que não estavam na lista — o comportamento que ele próprio previu na entrevista. Isso é o momento de pedir as 20-30 peças, porque a reciprocidade está aberta. Corpus de identidade destrava dois meses antes do previsto.
*Sinal:* resposta em menos de 48h contendo pelo menos uma tese nova.

**Pessimista (p ≈ 0.25).** Silêncio, ou resposta lacônica de uma linha. O Eixo 1 vira latência. Nesse cenário, **não construa F2-B como está**: reduza a consulta a um bloco único — compreensão declarada mais três decisões reservadas — e desloque todo o esforço para 1B e Camada 2, que não dependem dele.
*Sinal:* mais de 7 dias sem resposta, ou resposta que não decide nada.

Em todos os três cenários a Camada 2 sobrevive. É o ativo à prova de comportamento humano, e é por isso que ela é a aposta principal.

---

## 8. Próximo movimento — Onda −1, teto 2026-08-08

1. **Redigir e enviar uma consulta manual** sobre um caso real da fila — responsável: Igor; até 2026-07-31; feito quando a minuta passar no gabarito do `35`, §3, com zero pergunta reprovada no filtro do acervo, e for enviada pelo canal habitual.
2. **Gravar a demonstração de recusa** com a FORJA atual, sem código novo — responsável: Igor; até 2026-08-01; feito quando existir registro em vídeo ou PDF do sistema bloqueando citação de precedente sem íntegra, com o artefato de bloqueio anexo.
3. **Solicitar ao Cícero parecer específico sobre J-B(acordo)** endereçado a gestor público — responsável: Igor; até 2026-08-08; feito quando houver posição escrita sobre uso interno versus uso em manifestação.
4. **Definir três métricas de negócio** e começar a medir com o que já existe — responsável: Igor; até 2026-08-01; feito quando `METRICAS_GATES.json` registrar: horas entre recepção e primeira minuta; percentual de reescrita material na versão protocolada; número de rodadas até aceite. Fecha a lacuna G19 do documento `29`, que o plano identificou e não resolveu.
5. **Fechar o Portão 0 em paralelo** — responsável: Igor; até 2026-08-08; feito quando a Régua estiver verde ou o desvio classificado e aceito por escrito.
6. **Reordenar 1B antes de 1A** no documento `35` — responsável: Igor; até 2026-07-28; feito quando o roteiro registrar que 1B independe de comportamento humano e 1A fica condicionada ao resultado do item 1.

---

## Riscos de negócio que o plano não nomeia

**Concentração de cliente.** Toda a FORJA existe para um escritório, e cada onda a torna mais específica: identidade Medina, padrão Word Medina, regimentos das pastas. Isso é excelente para retenção e péssimo para transferência. O titular chamou isso de "IA artesanal" e tratou como virtude — e é, comercialmente, até o dia em que se quer vender a segunda instalação. Com a titularidade da FORJA sendo do Igor (`planejamento/24`), vale decidir conscientemente qual camada é núcleo transferível e qual é customização do cliente. Não é urgente. É irreversível se não for decidido a tempo.

**Mandato inexistente.** Ele deu uma entrevista. Não encomendou o sistema, não assinou escopo, não pagou por ele. O plano depende de cinco insumos que só ele fornece. Isso não é objeção ao plano — é motivo para que os itens 1 e 2 da Onda −1 venham antes de tudo: eles convertem entrevista em mandato, e mandato é o que financia as quatro ondas.

---

O plano melhorou a cada revisão porque cada revisor cortou em vez de acrescentar — inclusive vocês cortando de si mesmos, o que quase ninguém faz. Meu único desconforto é este: há três documentos de planejamento novos hoje e nenhum e-mail enviado ao homem cuja fala originou todos eles. A arquitetura está madura. A relação, não.

*— Helena. Café preto, sem açúcar. Ele falou 48 minutos sobre diálogo; sejamos os primeiros a puxar um.*
