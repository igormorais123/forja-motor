# 31 — Plano único consolidado: FORJA-ASSINATURA Lite + requisitos do titular

**Data:** 25/07/2026. **Estado:** planejamento consolidado. **Nenhuma linha de código foi alterada.**

**Substitui como roteiro de execução:** `26_PLANO_IMPLEMENTACAO_FORJA_ASSINATURA.md`, `27_PRD_FORJA_ASSINATURA.md` e `28_TDD_FORJA_ASSINATURA.md`, que passam a valer como **visão longa e backlog experimental** — não como plano imediato. O veredito adversarial Fable 5 de 24/07 (GO-COM-CONDIÇÕES) permanece válido quanto à tese; o que muda é a superfície.

**Consolida:** `29_REQUISITOS_ENTREVISTA_FABIO_MEDINA_OSORIO.md` (requisitos declarados pelo titular), `30_ARQUITETURA_DIALETICA_IDENTIDADE_E_PRECEDENTES.md` (os três eixos), `25_GOSTO_JURIDICO_AUTONOMO_EDGE.md` (protocolo EDGE já implementado) e a crítica de enxugamento de 25/07.

**Regra que governa este documento:** a FORJA já é grande. Toda capacidade nova precisa provar que **não existe** em outra nomenclatura, e precisa entrar como extensão do que existe, não como sistema paralelo.

---

## 1. A descoberta que dispensa metade da obra

Os dois planos — FORJA-ASSINATURA e os três eixos do documento 30 — convergiram para **o mesmo artefato**, por caminhos independentes. Um veio de teoria de seleção editorial; o outro, da fala do titular. Postos lado a lado:

| Campo do `F4_SIGNATURE_BRIEF` | O mesmo objeto, nos três eixos |
|---|---|
| questão decisiva | já existe: gate `jurisdictional_question_defined` em F4 |
| **versão óbvia rejeitada** | é o *"teses que descartei e por quê"* — o item que faz um sócio sênior engajar |
| **exatamente três rotas** | é o *"leque de teses"* que o titular pediu para mostrar ao advogado |
| rota escolhida e razão concreta | a decisão estratégica |
| frase-mãe | a expressão mais comprimida da identidade |
| **IDs das âncoras decisivas** | `fact_ledger` + os precedentes-âncora (Eixo 3) |
| melhor contra-argumento e resposta | o *distinguishing* antecipado + o red team de F7 |
| **consequência já demonstrada** | o **motor Medina**: nomear a consequência para quem decide |
| conteúdo obrigatório | preservação, já verificada por `forja_editorial_fidelity` |

E a tabela EDGE do documento 25 fecha a mesma equivalência por um terceiro caminho:

- **Exacting** — rejeitar a versão óbvia entre alternativas → as três rotas;
- **Differentiated** — *"o fio decisivo que só existe neste processo"* → **exige saber quem decide** (§3.1);
- **Grounded** — ledgers, hashes, replay → a âncora de precedente (§3.2);
- **Emotional**, que a FORJA já traduziu como **saliência decisória** — *"fazer o julgador perceber a consequência que os autos já provam"* → é **literalmente** o terceiro tempo do movimento argumentativo do titular: estabelecer o que a autoridade já decidiu, mostrar que decidir diferente rompe isonomia, **nomear a consequência para quem decide**.

Duas análises independentes, uma partindo de um vídeo sobre *synthetic sameness* e outra da transcrição de Fábio Medina Osório, chegaram ao mesmo mecanismo. Isso é a evidência mais forte de que o desenho está certo — e é a razão pela qual **não se constroem dois sistemas: constrói-se um.**

## 2. A dependência que a versão Lite não enxergou

A crítica está certa no princípio: *a inteligência fica na qualidade da escolha prévia, não no volume de versões*. Um único draft, precedido de uma escolha boa, vence três drafts precedidos de escolha genérica.

Falta responder: **o que torna a escolha boa?**

Se F4 inventa três rotas sem saber quem julga, a escolha é abstrata — e produz exatamente a mediania que o plano quer matar: um brief bem formado que escolheu a rota óbvia por falta de informação sobre o destinatário. "Differentiated" — o fio que só existe neste processo — não é um desejo estilístico; é uma consequência de conhecer **este relator, esta turma, o que já decidiram, onde está a divergência**.

Por isso o plano único acrescenta **um** insumo ao brief, e só um: o mapa do destinatário. Não é enfeite, é o que impede a rota diferenciada de ser uma aspiração.

**Ordem consolidada:**

```
F3-B  mapa do destinatário   → quem decide, o que já decidiu, onde diverge
F4    signature brief        → três rotas informadas, uma escolhida, âncoras declaradas
F5    verificação            → confirma as âncoras que o brief declarou
F6    um único draft         → segue a rota, consome as âncoras
F7/F7-B  preservam            → gostoJuridico recompõe brief e rota
```

Aresta de realimentação, reaproveitando a máquina de invalidação já prevista: **âncora que não sobrevive à verificação em F5 invalida a rota e reabre F4.** É mais barato que descobrir na auditoria.

---

## 3. Superfície técnica única

### 3.1 Artefatos novos — dois, e não sete

**(1) `F3_MAPA_DESTINATARIO.json`** — pequeno, cerca de dez campos, todos preenchidos ou marcados como não apurados com motivo:

órgão competente; prevenção (existe, de quem, origem, fundamento regimental); **composição atual do órgão com data de conferência obrigatória**; posição do relator prevento sobre a questão; posição da turma, da outra turma da mesma seção, da seção e da Corte Especial; divergência conhecida entre fracionários; via recursal projetada; matéria a prequestionar.

Alimentado pelo TeiaJus, que **já tem o dado**: espelhos mensais dos dez órgãos julgadores do STJ com o campo relator, Diário com íntegras e `textSha256`, DataJud com `orgaoJulgador`. Nenhuma coleta nova.

Fecha a lacuna G6 do documento 29 — a mesma falha que o escritório já apontou uma vez no caso Cafelana e que segue sem artefato.

**(2) `F4_SIGNATURE_BRIEF.json`** — exatamente como a crítica desenhou, com os nove campos do §1, produzido **dentro da execução F4 atual**, depois dos pareceres Helena e Cícero. Sem chamada adicional. Absorve o leque de teses: não há dois lugares onde rotas nascem.

### 3.2 Extensões de artefatos existentes — três, sem schema novo

**(3) `verified_source_ledger` (F7) + campos de precedente.** `ratio` com trecho literal e localização; `obiterConfundivel`; `molduraFaticaDeterminante`; `confronto` elemento a elemento; `operacao` — aplicar, distinguir, delimitar alcance, sustentar superação; `regime`; `vigenciaConferidaEm`.

**Restrição que evita o overcode:** aplicado **apenas aos precedentes-âncora declarados no brief** — tipicamente três a seis por peça, não trinta. É a diferença entre um instrumento e uma burocracia. E é fiel ao titular, que falou de *"seleção correta"* e *"uso adequado"*, não de fichar tudo.

**(4) `source_ledger` (F5) + dois campos.** `parametrosBusca` (termos, órgãos, recorte, bases consultadas e não consultadas com motivo) e **`resultadosNegativos`** — o que foi procurado e não foi encontrado.

O resultado negativo é a única informação genuinamente nova aqui, e é estratégica de primeira ordem: **a ausência de precedente favorável no órgão prevento muda a peça inteira.** Hoje se perde. Não precisa de documento próprio: precisa de um campo.

**(5) Recibo `gostoJuridico` + dois campos.** `signatureBriefSha256` e `selectedRouteId`, recompostos no validador final por `forja_editorial_fidelity`, corrigindo o achado 5 da revisão adversarial (o recibo hoje é validado dentro de `forja_fable5.py`, fora da recomposição final).

### 3.3 Sem schema novo — um seletor e um renderizador

**(6) Consulta ao advogado responsável.** É **projeção** do que já existe, não motor novo: seletor sobre as cem perguntas do F2-A + renderizador em prosa endereçada + rastreador de resposta. Os quatro filtros de admissão e o campo *"o que farei se não houver resposta"* estão no documento 30, §1.2 e §1.3.

Duas fusões que eliminam duplicidade:
- o bloco de teses da consulta **é** o conjunto de rotas do brief, renderizado para fora;
- **a resposta do advogado é o aceite de escopo.** Não existe subfase separada de fixação de escopo: a consulta respondida cumpre a função, com proveniência `office_declaration`.

Quando enviar: sempre a consulta de escopo (curta); a consulta de rotas apenas em classe complexa ou estratégica, porque é renderização de artefato que F4 produz de qualquer modo — custo marginal próximo de zero.

### 3.4 Configuração e prova

Flag única `off | shadow | pilot`, reaproveitando `forja_n4_validate._effective_mode()` e `pilotCases`, que a revisão adversarial já identificou como padrão correto. Teto simples de custo com a telemetria existente. Sem pacote novo, sem CLI própria, sem máquina de estados nova.

---

## 4. O que sai — de ambos os planos

### 4.1 Cortes no FORJA-ASSINATURA (endosso a crítica, com um acréscimo)

Retirados: cinco a sete geometrias; três microbriefs isolados; dois ou três drafts por petição; N-way e Condorcet; terceiro juiz; famílias distintas obrigatórias em produção; memória decisória na v1; topologia estrutural sofisticada; pacote `forja/signature/` com treze módulos; CLI própria; subfases F4-S, F5-S, F6-A, F6-B e F6-C; sete schemas; rollout de quinze ondas; budget complexo por estágio; `default_on` desenhado antes do piloto.

**Acréscimo meu, que a crítica não flagrou: cortar `F6_SIGNATURE_RECALL.json` e não repor.** Recall em duas sessões não é apenas caro — mede a coisa errada para este destinatário. O modelo de leitor do titular é o **julgador atordoado, com uma fila**. A métrica que importa é **esforço de decisão reduzido**, não memorabilidade. Recall é métrica de publicidade, não de adjudicação, e otimizá-la produz exatamente o texto calculado que a própria crítica teme.

### 4.2 Cortes no meu plano (documento 30)

Sou obrigado à mesma disciplina:

- **Caderno de pesquisa como artefato próprio** → cortado. Vira dois campos no `source_ledger` (§3.2, item 4). A informação nova é o resultado negativo; o resto já está na telemetria.
- **Ficha de precedente como dossiê de dez blocos para todo precedente** → cortada. Vira extensão do `verified_source_ledger` e **só para as âncoras do brief**. Era o maior risco de overcode do meu plano.
- **Subfase F2-C de fixação de escopo** → cortada. A consulta respondida é o aceite.
- **Jurimetria de comportamento (J-B)** → sai do roteiro e vai para backlog declarado. A jurimetria de **seleção** (J-A) — buscar o que o relator prevento e a turma já decidiram — permanece, porque é consulta ao TeiaJus, não inferência estatística, e é o que alimenta o mapa do destinatário.
- **Precedente administrativo** (TCU, CNJ, CGU, CADE, CVM) → mantido: é tabela em `forja_authorities.py`, superfície quase nula, e é o terreno real do escritório.

### 4.3 Placar da consolidação

| | Plano ASSINATURA original | Meu plano isolado | **Plano único** |
|---|---:|---:|---:|
| Artefatos novos | 6 | 4 | **2** |
| Extensões de artefato existente | 1 | 2 | **3** |
| Subfases novas | 5 | 6 | **1** (F3-B) |
| Módulos novos | ~13 | — | **0 pacotes; validadores nos módulos existentes** |
| Ondas | 15 | 3 blocos | **3** |
| Drafts por petição | 3+ | 1 | **1** |

---

## 5. Separação que a crítica embaçou: nem tudo é hipótese de A/B

A crítica manda provar tudo no AUTO-RESEARCH. Correto para uma das três coisas, e categoria errada para as outras duas.

| Capacidade | Natureza | Como se valida |
|---|---|---|
| **Brief → redação** | hipótese de qualidade de texto | **A/B cego no AUTO-RESEARCH.** Incumbente é o prompt atual; variante consome o brief. Se não vencer com estabilidade, fica em sombra ou sai. |
| **Mapa do destinatário** | correção factual de uma lacuna conhecida | **Conferência contra fonte oficial.** Não há hipótese a testar: ou os campos batem com o RISTJ, o DataJud e a composição publicada, ou estão errados. Testar isso em A/B seria confundir verdade com preferência. |
| **Consulta ao advogado** | interação pedida expressamente pelo titular | **Métricas de interação:** ele respondeu? as perguntas eram materiais? **alguma pergunta já estava respondida no acervo?** — essa última é falha grave. Submeter a A/B de qualidade textual seria erro de categoria. |

Isso importa porque impede duas coisas: gastar orçamento de AUTO-RESEARCH com o que não é hipótese, e bloquear em sombra uma capacidade que o titular pediu por escrito enquanto se espera um resultado estatístico que ela nunca produziria.

---

## 6. Três ondas

**Onda 1 — sombra, e nada muda na saída**
Régua verde primeiro, ou desvio classificado e aceito como baseline conhecido; rebaseline automático continua proibido. Schemas e validadores do mapa e do brief. F3-B produz o mapa; F4 produz o brief. **Nenhum output de F6 muda.** Verificação de completude e de grounding sobre casos históricos — Cafelana, Jalusa, Libra Sul e Natura, que já têm entrega e diff.

Critério de saída: os campos de prevenção e composição batem com a fonte oficial nos casos históricos; toda âncora declarada no brief existe nos ledgers.

**Onda 2 — variante A/B, e a consulta entra em operação**
F6 variante consome o brief; incumbente segue sendo o prompt atual; comparação cega no AUTO-RESEARCH existente. Produção intocada.

Em paralelo, e sem depender do A/B: **a consulta ao advogado entra em uso real**, porque sua validação é de interação, não de texto (§5). É o que o titular mais detalhou e o que ele avalia primeiro.

Começa também a extração do **Corpus B** — os diffs entre a versão protocolada e a nossa —, que não depende de pedido nenhum a ele e é o corpus de maior sinal para a identidade.

**Onda 3 — piloto controlado**
Poucos casos, uma peça por caso, via `pilotCases`. F7 e Fable recompõem o brief e preservam a rota. Rollback é desligar a flag. Só amplia com ganho prospectivo e sem regressão jurídica.

As oito condições de `default_on` da revisão adversarial de 24/07 permanecem integralmente aplicáveis e não são reabertas aqui.

---

## 7. Riscos que continuam de pé

- **Texto escrito para a rubrica.** O risco central da crítica não desaparece por enxugar: um brief com campos obrigatórios pode produzir peças que preenchem campos. Mitigação: o brief é **decisão**, não roteiro de redação; F6 não recebe o brief como sumário a expandir. E o gate de estilo humano já existente continua sendo o detector.
- **Mediania por seleção.** Sobrevive apenas no A/B, fora da produção, e com um único juiz por rodada. Não há comitê por petição.
- **Composição de órgão é dado perecível.** Mapa desatualizado é pior que ausente, porque tem aparência de autoridade. Data de conferência obrigatória e validade curta.
- **Espelho não é íntegra.** A tentação de extrair ratio da ementa porque a ementa está disponível é o modo de falha que desmoraliza — na palavra do próprio titular. Gate duro desde o primeiro dia.
- **Risco empírico, que a revisão adversarial já nomeou:** o sistema pode gerar escolha estruturalmente melhor e ainda assim não produzir peça melhor. Se não se confirmar, a decisão correta é sombra ou desligamento, preservando a FORJA atual.

---

## 8. O que continua dependendo dele

Sem mudança em relação ao documento 29, §5: vinte a trinta peças assinadas, incluindo duas ou três que ele considere ruins; preferência doutrinária por matéria; parâmetros por classe de caso, em tabela **vazia**, para preencher com ele; autorização e limites do módulo J-B; e os textos dele sobre soberania cognitiva e espaço público não estatal.
