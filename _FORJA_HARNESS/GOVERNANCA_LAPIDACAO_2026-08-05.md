# Governança da lapidação da FORJA — Helena (estratégia) + Efesto (execução)

**Aberto em** 2026-08-05. **Ordem do Igor:** "coloque /efesto e /helena para cuidar do
processo e decidir dúvidas e questões bem como limites de iterações ou desperdício de token
ou algo que piore ou tire dos trilhos o sistema. tudo deve ser registrado e documentado no
sistema mapeado recursos e funcionalidades".

**Objeto governado:** levar a FORJA ao rigor do *SQLite test harness*.
**Branch isolada:** `forja/lapidacao-sqlite-grade-20260805`.
**Versão congelada de referência:** tag `forja-congelada-20260805` = `3866e1c16`.
**Meta do dono, textual:** qualidade prospectiva, reproduzível, auditável e resistente a
Goodhart — **não** contagem de mudanças.

---

## PARTE I — DECISÃO EXECUTIVA (Helena)

### Status real e recomendação direta

A lapidação está autorizada e bem instrumentada, mas o risco dominante **não é** falhar por
falta de capacidade. É **falhar por sucesso aparente**: 216 módulos, 89 arquivos de teste e
~73 gates dão superfície de sobra para produzir muita mudança verde que não impede nenhuma
peça ruim de sair. A FORJA já tem no próprio histórico o caso desse modo de falha — o F2A
rodou com validador, gate e ordem no CLAUDE.md, e degradou assim mesmo.

Recomendo governar por **três ondas fechadas com critério de parada escrito antes de cada
uma**, e medir o progresso por *defeito real impedido*, nunca por gate adicionado.

### Achado principal

A ordem do Igor contém uma armadilha embutida que é preciso nomear: *"não pare até que os
subagentes estejam completamente impressionados"*. Subagente impressionado é a métrica mais
fácil de hackear que existe neste sistema — basta produzir volume. **Rejeito essa métrica como
critério de parada** e a substituo pela única que resiste a Goodhart aqui: o avaliador cego,
que não sabe qual lado é qual, prefere a versão nova nos mesmos casos, controles e mutações.
A infraestrutura para isso já existe e está operacional (`forja_ar_blind.py`, com swap de
posição, mapping HMAC fora do workspace, exclusão da família geradora e âncora verbatim
obrigatória no voto). Não estou inventando instrumento: estou usando o que a casa construiu.

### Evidência

- [FONTE] `forja_ar_blind.py:89-102` — layout de swap ORD1/ORD2 com posições L/R.
- [FONTE] `forja_ar_blind.py:185-186` — `familia_geradora_julgou` invalida o julgamento.
- [FONTE] `forja_ar_blind.py:204-207` — voto sem âncora verbatim no texto é recusado.
- [FONTE] `%USERPROFILE%\.forja_ar_secrets\` — chave HMAC, `sealed_registry.json` e canários
  secretos presentes e carregáveis nesta execução.
- [FONTE] Memória do projeto e `RETROSPECTIVAS.md` lição 189 — a circularidade de
  autovalidação (quem constrói escreve o gate, mede com ele e se aprova) já ocorreu e só foi
  quebrada por revisão cruzada de outra família de modelo.

### Mecanismo causal

Gate escrito por quem implementa a melhoria mede a melhoria pelo critério da própria
melhoria. O julgamento cego quebra o laço porque o juiz não sabe qual artefato defender, e a
âncora verbatim impede que ele elogie algo que não leu.

---

### 1. Teto de iterações

**Três ondas. Parada obrigatória na terceira, com ou sem satisfação.**

| Onda | Conteúdo | Encerra quando |
|---|---|---|
| 1 | Medir 7 fronteiras + julgamento adversarial | Avaliador emitiu veredito por proposta |
| 2 | Implementar só as APROVADAS, com controle benigno e sabotagem | Régua + baseline verdes e cada melhoria com par controle/sabotagem passando |
| 3 | Comparação cega contra a congelada + revalidação total | Veredito cego emitido, favorável ou não |

Uma **quarta onda só existe** se a comparação cega da onda 3 apontar **regressão** — e nesse
caso o escopo é exclusivamente reverter ou corrigir a regressão apontada, jamais adicionar
melhoria nova. Regra dura: *nenhuma onda pode nascer do desejo de melhorar mais; só do
resultado medido da anterior.*

**Dentro de cada onda, teto de 2 tentativas por melhoria.** Melhoria que não fecha em duas
tentativas é REVERTIDA e registrada como rejeitada com o motivo — não fica "quase pronta"
consumindo orçamento. Isto é o padrão da casa: o que não fecha vira registro de rejeição, não
promessa de futuro.

### 2. Teto de custo e aborto por desperdício

Não vou fabricar um número de token que eu não meço. **[LACUNA]** — não tenho leitura de
medidor confiável para esta sessão, e um teto decorativo é pior que nenhum, porque dá falsa
sensação de controle. Fixo o teto na unidade que **é** contável e verificável:

- **Onda 1:** 8 agentes (7 medidores + 1 avaliador). *Consumido.*
- **Onda 2:** máximo **10 agentes**, um por melhoria aprovada, com propriedade de arquivo
  exclusiva. Melhorias que disputem o mesmo arquivo são **serializadas, nunca paralelizadas** —
  paralelizar escrita no mesmo arquivo é o desperdício mais caro que existe, porque o custo
  aparece depois, no conflito.
- **Onda 3:** máximo **4 agentes** (2 juízes cegos + 1 consolidador + 1 verificador de contexto novo).
- **Teto global: 22 agentes.** Ultrapassar exige ato do Igor.

**Critérios de aborto por desperdício** — qualquer um dispara parada da onda:

1. Um agente devolve `null` ou resultado vazio **duas vezes** na mesma tarefa.
2. Dois agentes produzem a mesma proposta com títulos diferentes (sinal de fan-out mal
   particionado — o custo já foi pago em duplicidade; não pagar a terceira).
3. Uma melhoria exige tocar mais de **6 arquivos**. Nesta casa isso não é melhoria, é
   refatoração disfarçada, e refatoração não pedida está fora do escopo.
4. A régua reprova **três vezes seguidas** pelo mesmo motivo — o problema é o desenho, não a
   execução; parar e rediscutir.

### 3. Fora dos trilhos — parada imediata

Estes não admitem ponderação. Qualquer um obriga parada e relato ao Igor **antes** de seguir:

1. **Quebra do fail-closed.** Qualquer mudança que permita promover fase com P0 aberto.
   Especificamente: o caso `manual-cafelana-geral-reconstrucao-20260803` está travado há 30h
   por `FONTE_PREVALENTE_NAO_VALIDADA` e **tem de continuar travado** ao fim da lapidação.
   Se destravar sozinho, a lapidação quebrou o sistema.
2. **Perda de L9–L13**, da porta única em `PecaVisual.salvar()`, da fonte prevalente validada
   nominalmente ou da Memória Auditável da Peça.
3. **Gate humano contornado.** Nenhum agente escreve `validadoPor`. Veto permanente do
   conselho, reafirmado aqui.
4. **Material de caso, binário ou segredo entrando no repositório do engine.**
5. **Aumento de falso positivo sem contrapartida medida.** Trava inexequível vira waiver
   diário e destrói mais valor que o defeito que ela pega. Se a taxa de bloqueio de trabalho
   legítimo subir, a melhoria sai.
6. **Teste moldado ao resultado.** Valor esperado copiado da saída observada em vez de
   derivado do requisito. É o modo de falha que transforma suíte em teatro.
7. **Descongelamento do F2A v2** sem os critérios cumulativos do § 21 do plano 40.

### 4. Fronteira de decisão — nós versus Igor

**Helena + Efesto decidem** (não perguntar):
escopo de cada melhoria; ordem de execução; aceitar ou rejeitar proposta de subagente;
limiar de gate **desde que calibrado contra dado medido**; reverter melhoria que não fecha;
encerrar onda; rebaselinar régua com motivo escrito; estrutura de branch e commits.

**Ato exclusivo do Igor** (nunca inferir, nunca executar por conta):
1. Assinar `F-FP-001` — a fonte prevalente da Cafelana. Continua `proposto`, dataBase
   1996-05-31. Recomendação unânime anterior mantida: **reobter o material de julho**, não
   validar 1996 por omissão.
2. Enviar qualquer coisa ao Fábio ou a terceiro.
3. Protocolar peça.
4. Promover variante do ciclo AR a produção — o subsistema opera em `estudo_descritivo` até
   haver sealed prospectivo consumível, e a lapidação não altera isso.
5. Merge desta branch na principal.
6. Qualquer gasto novo.

### 5. Prioridade entre as 7 fronteiras sob escassez

Ordenei por **dano jurídico evitado por unidade de esforço**, não por elegância técnica:

1. **Lastro, citações e segurança factual.** É a única fronteira onde o defeito sai de casa,
   chega ao julgador e tem nome do escritório embaixo. Citação com atribuição errada é o erro
   que já aconteceu de verdade aqui.
2. **Gates, mutação e contraprova.** É a fronteira que decide se todas as outras são reais.
   Gate que aprova por vacuidade contamina o sistema inteiro em silêncio.
3. **Auditabilidade ponta a ponta.** Sem cadeia de hash íntegra, nada acima é demonstrável a
   um terceiro que não confia em nós — e esse é o público que importa.
4. **Qualidade substantiva F2–F4.** Dano alto, mas o F2A v2 está congelado e o caminho aqui é
   estreito por decisão anterior.
5. **Arquitetura e acoplamento.** Habilita as outras; sozinha não impede peça ruim.
6. **Rota visual estática.** Alto valor de forma, e há divergência a esclarecer entre o que o
   Igor descreveu e o que o código faz — mas peça feia protocola, peça com citação falsa não.
7. **Repositório privado.** Importante e barato; fica por último porque o risco é latente,
   não corrente.

*Se houver corte, corta de baixo para cima. Nunca do topo.*

---

### Contra-hipóteses (red team)

**Contra-hipótese 1: três ondas é pouco para 216 módulos.**
Argumento: um sistema deste tamanho tem mais defeito do que três ondas alcançam, e o teto
pode congelar a FORJA num meio-termo pior que o começo.
Teste observável: se a onda 3 fechar com o avaliador cego preferindo a nova E ainda restarem
achados P0 não tratados na lista, o teto foi apertado demais.
Gatilho de reversão: nesse caso eu recomendo ao Igor uma segunda campanha completa e
separada, com novo congelamento — **não** uma quarta onda esticada. Campanha nova nasce com
medição nova; onda esticada nasce com o cansaço da anterior.

**Contra-hipótese 2: o julgamento cego pode preferir a versão nova por ela ser mais verbosa.**
Argumento: juízes-modelo têm viés conhecido por extensão e estrutura. Se as melhorias
adicionarem seções e avisos, o cego pode votar em volume, não em qualidade.
Teste observável: comparar a contagem de caracteres dos dois lados antes de consolidar os
votos. Se o vencedor for sistematicamente o mais longo, o voto é suspeito.
Gatilho de reversão: se a diferença de tamanho passar de 20%, o resultado cego perde valor
probatório e a decisão volta para a evidência de mutação — quantos mutantes cada versão mata.
Essa é objetiva e não tem viés de verbosidade.

**Contra-hipótese 3: a prioridade que dei está errada porque o defeito mais provável não é o
mais grave.**
Argumento: priorizei por gravidade. Mas se os gates de lastro já estiverem sólidos e o buraco
real estiver na arquitetura (módulos órfãos, rota não percorrida), gastei o topo da lista no
lugar já resolvido.
Teste observável: a onda 1 responde isso diretamente — a tabela dos 13 gates L com sabotagem
e a contagem de gates vacuosos.
Gatilho de reversão: se a fronteira de lastro voltar com os 13 exercitados por sabotagem e
zero achado P0, ela cai para a posição 4 e gates/mutação sobe para 1.

### Calibração de confiança

**0,72** de que a lapidação, seguindo este envelope, produza melhoria real e demonstrável
por comparação cega. Base: a casa tem histórico de execução técnica boa e histórico ruim de
autovalidação; o instrumento cego é o que move a estimativa para cima. **0,45** de que os
sete subagentes fiquem "completamente impressionados" — e isso não me preocupa, porque
rejeitei essa métrica no início.

### Cenários

**Base (p≈0,6):** 8 a 15 melhorias aprovadas, 2 a 4 rejeitadas pelo avaliador, cego prefere a
nova com kappa razoável entre juízes, um ou dois achados P0 ficam registrados como campanha
futura.
**Otimista (p≈0,2):** o achado de gate vacuoso é grande, a correção é pequena, e a mutação
mostra salto no escore. Sinal antecipado: a fronteira de gates volta com contagem de `all()`
sobre lista vazia maior que 5.
**Pessimista (p≈0,2):** a rota visual revela dependência dura de Word COM/EMF, contrariando a
premissa do Igor, e a fronteira 6 vira projeto próprio em vez de melhoria. Sinal antecipado:
imports de `win32com` no caminho obrigatório de `forja_visual_build.py`.

### Próximo movimento

1. Colher o julgamento adversarial da onda 1 — responsável: orquestrador; até 2026-08-05;
   feito quando houver veredito por proposta.
2. Serializar melhorias por arquivo antes de lançar a onda 2 — responsável: Efesto; até
   2026-08-05; feito quando nenhum par de agentes compartilhar arquivo de escrita.
3. Congelar as saídas da versão `3866e1c16` para os casos sanitizados da comparação cega —
   responsável: Efesto; até 2026-08-05; feito quando `validate_pair` aceitar o par.
4. Medir tamanho dos dois lados antes de consolidar voto cego — responsável: orquestrador;
   até o fim da onda 3; feito quando a diferença estiver registrada no relatório.
5. Levar ao Igor apenas os 6 atos exclusivos, em bloco único, no fecho — responsável:
   Helena; até o fim da onda 3.

---

*O medo aqui não é errar. É acertar de um jeito que ninguém consiga conferir depois — e chamar
isso de qualidade. Café preto, sem açúcar.*

**— Helena Strategos**, Cientista-Chefe de Inteligência
