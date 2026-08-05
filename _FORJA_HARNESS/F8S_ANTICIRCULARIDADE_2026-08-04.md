# F8-S: resposta medida à acusação de circularidade

**04–05/08/2026.** Ordem do Igor: *"o f8-s que o diabob viu é relevante quero que
resolva e implemente o que precisa para resolver."*

A acusação, em uma frase: o gate de assinatura visual foi escrito pelo mesmo
agente que produz as peças, os limiares foram escolhidos por esse agente, a
cobertura foi medida com esse mesmo gate, e a peça declarada CONFORME passou num
gate que o autor calibrou. Pelo resultado, isso é indistinguível de um
instrumento moldado até aprovar o que o pipeline emite.

Cada pergunta foi respondida por medição, não por argumento. Duas delas
derrubaram o gate.

---

## 1. O gate mede o que diz medir? — **Não media. Dois falsos negativos.**

### Falso negativo A: figura era arquivo no pacote, não figura na página

`imagensVetoriais` contava os `.emf`/`.wmf` dentro de `word/media/`. Ataque
executado: peguei uma peça que o gate **reprovava** por falta de figura, copiei
para dentro do pacote quatro EMF de outra peça — sem referenciá-los em lugar
nenhum, sem que aparecessem em página alguma — e acrescentei os tokens da paleta
dentro de um comentário XML invisível.

**A peça virou CONFORME.** Nenhum pixel mudou na tela.

Corrigido: figura agora é contada pela cadeia de relacionamento — o corpo cita um
`r:embed`, o `document.xml.rels` resolve o id para um alvo em `media/`. Arquivo
solto no zip não conta mais, e o laudo passou a expor `vetoriaisOrfas` para que
lixo de montagem apareça em vez de virar crédito.

### Falso negativo B: referência sem arquivo contava como figura

Descoberto pelo canário anti-moldagem **minutos depois** de corrigido o primeiro:
com a contagem por referência, apagar os EMF do pacote deixava as referências
órfãs e o gate continuava contando quatro figuras. Um DOCX assim mostra o quadro
vazio com o X no Word — figura que o julgador não vê, contada como presente.

Corrigido: exige-se referência **e** existência do alvo.

### A `FAIXAS` era catraca decorativa

A "densidade calibrada por extensão" que o Igor exigiu na auditoria de 30/07 —
peça de 4 páginas e de 31 não podem ter a mesma régua — estava **inerte**. A
única rota viva chamava `avaliar(destino, None, tipo)`, então toda peça era
medida contra a faixa neutra de 10 páginas. A constante existia, estava
documentada, elogiada em comentário, e nunca era consultada com valor real.

**A saída óbvia era estimar a extensão pelo tamanho do texto, e ela foi
rejeitada por medição.** Calibrei o estimador contra **269 pares DOCX/PDF reais
do acervo** — âncora externa, não o meu próprio gate. O melhor candidato
(caracteres ÷ 3.800) acerta a faixa de densidade em **60%** dos casos. Numa régua
de quatro faixas, errar 40% faria o gate exigir quatro figuras de uma peça de
seis páginas: exatamente o falso positivo que travaria peça com prazo, que é o
risco que adiou a ativação do bloqueio.

Continuar mexendo na heurística até a taxa agradar seria a autovalidação que esta
frente existe para quebrar. O que ficou: usa-se a contagem física quando há PDF
ao lado do DOCX, e declara-se `densidadeCalibrada: false` quando não há. Régua
neutra com aviso é honesta; régua estimada com aparência de precisão não é.
**Hoje 66% do acervo é medido contra a extensão real.**

---

## 2. A cobertura era achado real ou artefato da definição? — **Real.**

Censo sobre os 356 DOCX do acervo, antes e depois das duas correções:

| | conformes | reprovados |
|---|---|---|
| gate antigo | 74 (20%) | 282 |
| gate corrigido | 74 (20%) | 282 |

A correção mudou **um** documento de 356 (VIS-03 foi de 277 para 278 achados). O
número não dependia da definição defeituosa. A pobreza visual do acervo é fato
medido, e sobreviveu à correção do instrumento que a mediu.

---

## 3. Limite de moldagem — **há uma hipótese ainda não exercitada.**

O ataque do item 1 está fechado. O canário executado nesta onda removeu elementos
de uma peça aprovada e confirmou que o gate reprova a destruição. Ele ainda não
testou o ataque inverso: adicionar duas tabelas vazias com barra lateral grossa e
um diagrama sem conteúdo. Portanto, isso permanece uma **hipótese de limite**, não
um resultado medido.

O limite provável decorre de o gate contar **estrutura**, e estrutura se fabrica;
se confirmado, não será resolvido por um limiar estrutural isolado. Até lá, não se
deve declarar robustez nem tratar a hipótese como defeito demonstrado.
`conforme: true` no F8-S significa **"os elementos existem"**, nunca "os elementos
dizem algo". O que os elementos afirmam é guardado em outro lugar: o brief F7.5,
a fidelidade textual de 100% e o olho humano. A ordem de 30/07 — *figura
fabricada é pior que figura ausente, porque parece prova* — continua sendo a
regra que nenhum contador de OOXML substitui.

---

## 4. O gate ainda sabe reprovar? — **Sim, e agora há prova permanente.**

`test_forja_assinatura_antimoldagem.py`, na régua. Pega a peça aprovada pelo dono
(Cafelana V8, 30/07) e a destrói no OOXML, um elemento por vez, exigindo que o
gate acuse a família certa: figura, paleta, timbre, destaque, negrito, tabela.
Seis destruições, seis acusações. Se o gate aprovar peça destruída, a suíte falha
mesmo com todo o resto verde.

Foi esse canário que encontrou o falso negativo B, minutos depois de instalado.

---

## 5. O achado que vale mais que tudo acima

Medi o raio de explosão de tornar o F8-S bloqueante. O resultado desmonta a
própria pergunta:

**A rota canônica de produção visual rodou UMA vez na história.** Existe um único
`VISUAL_BUILD.json` no acervo inteiro. E das 12 entregas mais recentes, **11
foram produzidas fora dela**.

Tornar o F8-S bloqueante hoje travaria uma peça — que já está conforme. O gate
guarda uma porta que quase ninguém atravessa.

Isto é a **terceira** aparição do mesmo padrão, e ele já está escrito no
`CLAUDE.md` desde 03/08: *"gate instalado na rota que ninguém percorre é gate
nenhum — o elo 4-B era sério e rodou em 3 casos na história."* A lição foi
registrada e a fábrica seguiu produzindo por fora.

**Consequência para a decisão:** o dilema "ligar ou não o bloqueio" é quase vazio.
A pergunta real é por que a rota canônica não é usada — se falta comodidade, se o
caminho manual é mais rápido, ou se ninguém sabe que ela existe. Ligar o gate sem
responder isso produz a sensação de rigor sem o rigor.

---

## Estado

| Item | Estado |
|---|---|
| Falso negativo A (figura órfã) | corrigido |
| Falso negativo B (referência quebrada) | corrigido |
| `FAIXAS` inerte | viva em 66% do acervo; declarada quando não |
| Estimador de páginas | **rejeitado por medição** (60% de acerto de faixa) |
| Canário anti-moldagem do F8-S | instalado na régua, 6/6 |
| Régua completa | APROVADO, 127,7 s |
| Limite honesto do gate | documentado no item 3 |
| Bloqueio (tarefa #9) | **não ligado** — depende de ordem do Igor, e o item 5 sugere que a pergunta certa é outra |
