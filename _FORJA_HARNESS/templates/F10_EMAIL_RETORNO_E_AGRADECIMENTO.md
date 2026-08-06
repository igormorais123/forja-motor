# F10 — e-mail de retorno: agradecer a correção e pedir a próxima

Este template cobre a ponta do ciclo que nunca existiu. A FORJA captura a peça
protocolada, compara com a nossa e aprende com a diferença — mas nada, em
nenhum lugar do sistema, agradecia a correção nem pedia mais. Correção humana é
o insumo mais caro e mais valioso que a esteira recebe: cada uma custa o tempo
de um advogado sênior lendo linha por linha, e é a única fonte de aprendizado
que não vem de gate automático nenhum.

**Quando enviar.** Depois que a versão humana final ou a peça protocolada
retorna, e depois que o loop pós-protocolo rodou — nunca antes, porque o e-mail
precisa dizer o que foi efetivamente aprendido, e não prometer que se aprenderá.

**Quem envia.** Pessoa, não automação. Este template é para escrever, não para
disparar: e-mail de agradecimento gerado por robô é pior que nenhum, porque o
destinatário reconhece o molde na segunda vez e passa a ignorar.

---

## Regras de redação

1. **Agradecer pelo específico, nunca pelo genérico.** "Obrigado pelas
   correções" não convida a mais nenhuma. Nomeie duas ou três mudanças reais e
   diga o que cada uma ensinou. Quem vê que foi lido de verdade corrige de novo.
2. **Mostrar a consequência estrutural.** Não basta dizer que aprendemos: diga
   o que mudou no processo por causa daquela correção — o item que entrou no
   checklist, a conferência que passou a ser obrigatória. É a diferença entre
   elogiar o revisor e provar que a revisão dele teve efeito.
3. **Perguntar uma coisa só.** Um pedido específico é respondido; um pedido
   aberto ("qualquer crítica é bem-vinda") não é. Escolha a dúvida que mais
   mudaria a próxima peça.
4. **Não se defender de nenhuma correção.** Se discordamos de uma mudança, o
   lugar disso é uma conversa própria, nunca o e-mail de agradecimento — a
   defesa transforma o convite à crítica em convite à discussão, e a próxima
   correção não vem.
5. **Nada de superlativo.** "Correção brilhante" e "ajuste cirúrgico" soam a
   bajulação e desvalorizam o próximo elogio. Descreva, não adjetive.
6. **Sem marcador interno.** `[FONTE:]`, `[INFERÊNCIA]`, nome de arquivo,
   caminho de pasta, identificador de caso e menção a WhatsApp, Drive ou pasta
   local não aparecem — vale aqui o mesmo protocolo de origem operacional das
   peças.

---

## Estrutura

```
Assunto: <mesma thread da entrega> — retorno sobre os ajustes

<Saudação ao destinatário>

Comparei a versão protocolada com a que enviamos e trabalhei em cima das
diferenças. Três delas mudaram como vamos preparar as próximas peças:

1. <mudança concreta que o titular fez>
   O que ensinou: <a regra que passou a valer, em uma frase>
   O que mudou aqui: <o item que entrou no checklist / a conferência que passou
   a ser obrigatória / o trecho do protocolo que foi reescrito>

2. <segunda mudança>
   ...

3. <terceira mudança>
   ...

<Uma pergunta específica, sobre o ponto que mais mudaria a próxima peça.
Exemplo: "Na parte de <tema>, o senhor preferiu <escolha>. Isso vale como
padrão para esta classe de recurso, ou foi próprio deste caso?">

Se em alguma peça futura o senhor puder marcar o que reescreveria mesmo sem
estar errado — preferência de ordem, de ênfase, de vocabulário —, é o tipo de
apontamento que não aparece em conferência nenhuma e é o que mais aproxima o
texto do padrão da casa.

<Fecho>
```

---

## O que anexar, e o que não

**Anexar:** nada, por padrão. O e-mail é curto e se lê no celular.

**Não anexar:** o relatório de comparação, a lista de mudanças detectadas, o
número de alterações. Devolver ao revisor a contabilidade da própria revisão
soa a cobrança, e o dado interessa a nós, não a ele.

---

## Depois de enviar

Registre no caso que o retorno foi agradecido e o que foi perguntado. Quando a
resposta chegar, ela é insumo do mesmo loop: entra como candidato de lição com
`cause: style_preference` ou `legal_rule`, conforme o teor, e segue o mesmo
caminho de adoção — `python forja_aprendizado.py padroes` mostra se aquilo já é
padrão ou ainda é episódio isolado.
