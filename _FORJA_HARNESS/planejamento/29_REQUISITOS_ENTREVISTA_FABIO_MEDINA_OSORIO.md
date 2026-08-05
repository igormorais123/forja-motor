# 25 — Requisitos da FORJA extraídos da entrevista de Fábio Medina Osório

**Fonte:** transcrição de áudio de entrevista conduzida por Igor Morais Vasconcelos (Participante 1) com Fábio Medina Osório (Participante 2), ~48 minutos, recebida em 25/07/2026.
**Natureza deste documento:** fonte canônica de requisitos declarados pelo titular. Substitui inferência sobre "o que o escritório quer" nos pontos aqui cobertos.
**Estado:** análise concluída; requisitos mapeados contra o harness real; plano de instalação proposto, não executado.

> **Revisão de 25/07/2026 (pós-parecer do Codex).** Duas afirmações originais deste documento foram corrigidas por erro material: (i) precedente vinculante **não** se "rebaixa" por baixa aderência fática — vinculação é regime jurídico, e o que a aderência governa é a *operação* (aplicar, distinguir, delimitar alcance, sustentar superação), não a força; (ii) "mínimo de teses por classe" foi substituído por **cobertura de famílias de tese examinadas**, porque a contagem incentiva produção artificial. O desenho corrigido, o detalhamento dos três eixos e o mapeamento sobre o TeiaJus estão em `planejamento/26_ARQUITETURA_DIALETICA_IDENTIDADE_E_PRECEDENTES.md`.

## 0. Advertência de método (obrigatória antes de citar este documento)

A transcrição é automática e contém erros de reconhecimento de fala. Este documento usa três marcações:

- **[literal]** — trecho fiel, conferido no contexto da transcrição;
- **[corrigido]** — erro evidente de ASR restaurado (`julietria`→jurimetria; `rácio decidente`→ratio decidendi; `escorpo`→escopo; `ferir`→aferir; `presidente`→precedente; `stej`→STJ; `redras`→regras; `12:00logante`→dialogante; `nique lá`→aniquilar; `desruptiva`→disruptiva);
- **[incerto]** — passagem que não pode ser reconstruída com segurança e **não deve** fundamentar requisito.

Passagens marcadas `[incerto]` neste documento: "teorias concessionais" (provavelmente "processuais" ou "constitucionais"); "não escrevemos um trabalho sobre soberania cognitiva" (provavelmente "nós escrevemos"); "os tribunais originários sempre proporcionam decidio jurisprudencial". Nenhuma delas sustenta requisito isolado — todas têm apoio redundante em outro trecho.

Regra de extração derivada do próprio modo de falar dele (ver §4): **quando ele formula a mesma ideia três vezes, a última formulação é a canônica.** Ele pensa por aproximação sucessiva e aperta o enunciado a cada repetição.

---

## 1. O que ele efetivamente pediu

### 1.1 A tese central, dita por ele

> **[literal]** "o dever de fundamentação, auditabilidade das tomadas de decisões, a explicabilidade... são vetores que regem a atuação da IA e regem a atuação dos operadores jurídicos como um todo, tanto dos advogados, dos magistrados, dos membros do Ministério Público"

Este é o centro doutrinário da entrevista inteira, e é um **transporte dogmático**: ele pega o dever de motivação do ato de autoridade pública (art. 93, IX, CF; art. 489, CPC; art. 50 da Lei 9.784/1999) e o impõe à IA como se a IA fosse órgão. Não é metáfora. Tudo que ele pede depois decorre disso.

Consequência de engenharia, e é a mais importante do documento: **artefato de fase não é log — é ato motivado endereçado a um humano.** Um JSON de auditoria que só um depurador lê não cumpre o requisito. O documento `forja_medina_osorio_arquitetura.md` acertou nesta formulação e ela deve ser adotada.

### 1.2 A ordem de trabalho que ele descreveu

Ele descreveu um procedimento, e a ordem importa:

1. **Pedido endereçado governa o trabalho.** [literal] "a principal tarefa que ela deve realizar, portanto, é olhar o pedido endereçado a ela, para que seja a tarefa que ela deve realizar em cima da documentação que acompanha esse pedido". Os documentos são lidos *sob* o pedido, não ao lado dele.
2. **Checagem documental integral.** [literal] "o primeiro grande trabalho de uma IA qualificada é a checagem documental... um checklist completo de todo esse corpo documental, do início ao fim, e detalhadamente rastrear todos os documentos que ela recebeu". Note "íntegra documental" — ele usa "íntegra" duas vezes na entrevista, aqui e nos precedentes. É palavra portante: texto inteiro, nunca resumo.
3. **Auditoria da qualidade do próprio pedido.** [literal] "depois ela deve analisar se esse pedido formulado a ela é um pedido bem estruturado ou não... diante daquele conjunto documental que lhe foi apresentado". Segunda premissa explícita, e é a que ninguém implementa.
4. **Pedido de esclarecimentos ao remetente, antes de começar.** [literal] "ela faria uma espécie de pedido de esclarecimentos ao remetente da demanda, para que ele esclareça melhor o objeto". E, decisivo: [literal] "não há problema no fato de a IA ter dúvidas — **ela deve ter dúvidas, ela deve suscitar dúvidas antes de iniciar o trabalho**". Ele escala de permissão para dever em uma frase. E impõe o dever recíproco: [literal] "cabe a quem endereçou essa demanda responder os questionamentos da IA". Rodadas múltiplas autorizadas: [literal] "não há problema algum em suscitar novos questionamentos também".
5. **Requerimento motivado de complementação documental, emitido cedo e em paralelo.** [literal] "ela tem que fundamentar também esse pedido de complementação documental — **não basta ir simplesmente**". E o requerimento tem função dupla: [literal] "ela tem que mostrar a razão pela qual está solicitando aquelas diligências, **mostrar que compreendeu** o escopo do seu trabalho". O pedido de diligências é o exame de compreensão da IA.
6. **Fixação de escopo, metodologia e objetivo.** [literal] "a metodologia é: antes de iniciar o trabalho, delimitar de forma muito clara o escopo desse trabalho... saber delimitar o escopo, saber delimitar a metodologia, saber delimitar onde o postulante quer chegar, onde o remetente do pedido quer, com os objetivos". **Três objetos, não um.**
7. **Interação dialogante para alargar teses.** [literal] "ela pode tentar alargar o campo de cognição sobre teses a serem desenvolvidas... olha, eu tenho essas teses aqui que eu pretendo desenvolver, esse primeiro leque aqui... ela pode colher a opinião do interlocutor... a IA pode suscitar no interlocutor outras teses que o interlocutor tenha, suscitar insights no interlocutor". E fecha: [literal] "só isso já é a programação do próprio trabalho a ser desenvolvido".
8. **Pesquisa roteada pela topologia decisória** (§1.4).
9. **Redação sob as três premissas de estilo** (§1.5).
10. **Supervisão humana com palavra final.** [literal] "ele terá que supervisionar, terá que dialogar, e terá que ter a palavra final sobre isso".

### 1.3 O argumento econômico dele, que precisa ser respeitado literalmente

Ele antecipa a objeção óbvia — diálogo é atrito, atrito é lentidão — e a rejeita quatro vezes em quarenta segundos: [literal] "já pode abreviar inclusive o tempo, então ela ganha velocidade com isso, ela ganha **enorme** velocidade nesse trabalho"; "isso significa um ganho de escala, ganho de velocidade na produção do trabalho".

E diz **como** isso acelera: [literal] "independentemente de ter capacidade de prosseguir no aprofundamento do estudo da matéria, enfim, mas ela já lança um checklist documental preliminar". Ou seja: **a diligência é emitida cedo e o trabalho cognitivo continua em paralelo.** O pedido de documentos não suspende a cognição.

Isto tem consequência direta e é onde a proposta externa e o harness atual convergem por caminhos diferentes: o bloqueio correto não é do trabalho, é do **produto protocolável**. O F2-A já implementa exatamente isso (`draftRelease: blocked` enquanto houver questão material bloqueada, sem parar F3/F5). Está certo e deve ser preservado contra qualquer proposta de "portão humano que suspende o pipeline".

### 1.4 Topologia decisória — o algoritmo que ele ditou

Este é o trecho mais operacional da entrevista e o mais ausente do harness. Reproduzido quase integral:

> **[corrigido]** "quando já tem um órgão julgador prevento num determinado tribunal superior, numa determinada turma, então obviamente se tem um relator prevento, aí ela vai direcionar pesquisas para o relator prevento, para os componentes da turma preventa; ela vai também para outra turma que compõe a mesma seção; ela vai direcionando... ela vai para a Corte Especial no STJ, porque ela tem precedentes que têm uma força superior; e ela vai buscar matéria constitucional por prequestionamento futuro, para subir para o STF"

É uma **ordem de busca nominal**: relator prevento → integrantes da turma preventa → outra turma da mesma seção → Corte Especial → matéria constitucional a prequestionar. Não se pesquisa jurisprudência em abstrato; pesquisa-se **para um destinatário identificado**.

Requisitos de precedente que ele enunciou em torno disso:
- graduação hierárquica; precedente qualificado; precedente vinculante;
- atualidade: [literal] "o precedente tem que estar atualizado; quanto mais recente, melhor";
- [corrigido] "a leitura integral, ou pelo menos... o rastreamento da íntegra, **mas principalmente o uso adequado dos precedentes e a seleção correta**";
- [corrigido] "capacitada na identificação da **ratio decidendi**";
- [literal] "o que é muito relevante é a **aderência fático-probatória** da matéria discutida, debatida, objeto da decisão a que se busca num caso concreto, com o precedente a ser utilizado";
- e de novo: [literal] "a busca, a identificação, o mapeamento, e **principalmente a identificação da aderência de cada precedente ao caso concreto**";
- extensão ao contencioso administrativo: [corrigido] "serve nos processos judiciais e nos processos administrativos, por conta da teoria dos precedentes".

**"Principalmente" é o marcador de prioridade dele.** Ele usa duas vezes, e as duas apontam para o mesmo lugar: **uso adequado e aderência**. É a evidência textual mais forte de onde investir.

### 1.5 Estilo — três premissas declaradas, nesta ordem

1. **Correção do idioma, sem tolerância.** [corrigido] "há regras que devem ser seguidas... tem que seguir rigorosamente as regras do idioma; esse é o primeiro ponto, premissa fundamental".
2. **Poder de síntese.** [literal] "a segunda premissa é o poder de síntese, a objetividade, a ausência de redundâncias, a ausência de repetição, ou seja, ir direto ao ponto sempre". Justificada por um modelo de leitor, que ele constrói com imagem própria: [literal] "não se pode mais pensar que nesse universo nós estamos escrevendo uma obra literária para alguém, por seu deleite, ler e trabalhar aquela petição com prazer, bebendo uma taça de vinho. Não. Ele está tentando resolver um problema ali, **atordoado com milhares de processos**, com problemas de outras pessoas também **na fila** para resolver."
3. **Acessibilidade.** [literal] "de modo muito direto, objetivo, acessível, **sem rebuscamento**". E ele fecha o requisito com um argumento moral, não estético: [literal] "quanto mais transparente for a comunicação, melhor o **acesso à justiça** para a pessoa que é representada pelo advogado; então a comunicação tem que ser íntegra, transparente, objetiva".

Mais duas regras de conteúdo textual:
- **Concretude:** [literal] "ela tem que ser muito concreta, aderente à realidade, **mostrar a realidade para quem decide**". Mostrar, não qualificar — é a raiz da proibição de adjetivação valorativa.
- **Não abrir mão das fontes:** [literal] "ela não vai poder abrir mão do uso dos precedentes, ou da doutrina, ou da referência aos textos normativos".

E o teste final, na negativa: [literal] "não adianta um trabalho volumoso, rebuscado, com um idioma erudito, que fica dificultando o trabalho daquela pessoa que decide, que tem uma fila enorme e gigantesca de problemas de outras pessoas também para serem decididos".

**Nota importante sobre a "armadilha" da identidade textual.** Ele diz [literal] "não há mais uma preocupação com a identidade do texto do autor... eu não sou um grande escritor". Lido isolado, isso dispensaria um perfil de identidade. Lido inteiro, não: ele opõe **literatura** a **trabalho profissional de persuasão** — [literal] "se eu fosse escritor da área de literatura, talvez eu tivesse essa identidade; mas quando nós estamos falando de um trabalho profissional na advocacia... é um trabalho de persuasão". O que ele dispensa é o ornamento, não a identidade. A identidade dele é **arquitetural** (moldura doutrinária, hierarquia de fontes, ordem do raciocínio, o que se recusa a fazer), não lexical. O documento `identidade_medina_osorio.md` acertou esta leitura e ela deve ser adotada.

### 1.6 Jurimetria — o pedido de maior valor e maior risco

Ele pediu duas aplicações concretas, ambas com a mesma mecânica.

**(a) Comportamento decisório.** [corrigido] "se ela consegue aproximar um histórico estatístico maior de precedentes de um determinado julgador e mostrar que, de repente, é uma variação, um viés, uma modificação **que não se justifica**, só por conta de um determinado escritório, ou por conta de um escritório que é justamente o seu adversário — quando ele muda de posição, **veja o constrangimento que sugere**, se você detecta e faz esse diagnóstico... de repente isso é flagrado e revelado nos autos". Enquadramento dele: [literal] "combate ao desvio de finalidade, do desvio de poder... estrangulando esse mercado de abuso de poder, ou de favorecimentos, ou de arbitrariedades", contra o [literal] "subjetivismo desenfreado das autoridades — não apenas judiciárias, mas as administrativas também".

**(b) Benchmarking de acordos.** [corrigido] "quando você tem a capacidade de rastrear outros acordos em situações absolutamente idênticas... olha, em tantas situações análogas o acordo foi formado num cenário de deságio de 30%; aqui nesse caso concreto nós estamos oferecendo 40, 50% — a vantajosidade para o poder público é ainda muito maior; e se houver uma recusa, vejam, de repente o gestor público pode ser responsabilizado perante o Tribunal de Contas da União, de repente pode estar causando dano ao erário".

Observação: (b) é um **produto autônomo** e tem aplicação imediata no caso CASO-07/CASO-07 que já está na fila. Comercialmente pode valer mais do que a fábrica de petições.

Ele **não** pediu contenção. A contenção é imposta pela arquitetura, e a proposta externa está correta em impor: relatório interno, metodologia e universo amostral declarados, nunca composição automática de peça, decisão nominal do titular para usar. Acrescento duas exigências que a proposta não tem: **parecer do Cícero por uso** (exposição do art. 34 do EAOAB — imputação; litigância de má-fé; art. 41 da LOMAN) e **proibição de afirmar conduta de pessoa identificada** — o achado descreve série estatística, não intenção de juiz.

### 1.7 Limites e postura que ele impôs sobre si

- **Nunca comparação depreciativa.** Ele recusa a pergunta do diferencial quatro vezes: [literal] "eu não vou nunca me comparar com outro advogado... cada um tem a sua singularidade... eu não sou o melhor do Brasil nem do mundo"; e [literal] "muitas vezes indico vários outros colegas igualmente qualificados". Requisito: **a peça ataca a tese, nunca desqualifica o advogado adversário.**
- **Trabalho em rede é premissa.** [literal] "o ser humano evoluiu sempre em grupo... eu não resolvo nada sozinho, eu resolvo no coletivo, em grupo, com uma rede de outros colegas igualmente qualificados... e a IA é mais uma colaboradora... a IA trabalha em grupo, ela não vai sozinha resolvendo nunca nada, como eu também não resolvo sozinho".
- **Recusa explícita do modelo "IA programada de cima".** À pergunta "você é o Deus que vai programar o coração dela", respondeu: [literal] "eu não gostaria de pensar dessa forma... eu penso de uma forma dialogante, não de uma forma divina, de uma criatura perfeita que nasce pronta. Eu penso que seríamos parceiros, que **cresceríamos juntos**, e eu acredito que não vai ter outro jeito". Isto é uma afirmação de projeto, não filosofia: **o único modelo de autoria que ele aceita é co-evolução com registro do que o revisor humano mudou.**

---

## 2. Mapa de requisitos contra o harness real

Verificado em 25/07/2026 nos contratos `phase_contracts/F0..F10.json`, em `forja_estilo_humano.py`, `forja_authorities.py`, `forja_citations.py`, `forja_exploracao_100.py`, `templates/F2A_EXPLORACAO_100_PERGUNTAS.md` e por varredura léxica no código de produção.

### 2.1 O que já existe e atende (não reconstruir)

| Requisito dele | Implementação existente |
|---|---|
| Checagem documental rastreada, íntegra | F1: `document_index`, `coverage_ledger`, gates `critical_documents_indexed` + `coverage_declared`; `forja_injection_scan.py` |
| A IA deve ter dúvidas antes de trabalhar | **F2-A, 100 perguntas** (`forja_exploracao_100.py`, 10 óticas, `blocked` com consequência e rota de diligência) — é a implementação mais forte do harness e antecede a entrevista |
| Pendência material não deixa sair peça, mas não trava a cognição | `draftRelease: blocked` em F2-A + F6 bloqueado, com F3/F5 seguindo |
| Fonte idônea, íntegra, jamais citar o inexistente | `cache/fontes_oficiais/` verbatim com data de conferência; F7 gates `live_official_source_replayed`, `source_excerpt_hash_match`, `citation_coverage_complete`; taxonomia U1 de 6 modos de falha; regressão `test_forja_citacoes.py` |
| Matriz fato→prova com âncora | F3: `fact_ledger`, `chronology`, `contradictions`, gate `critical_facts_sourced`; matriz de segurança factual em 5 colunas, >30% não verificado bloqueia redação |
| Descarte fundamentado, nada desaparece em silêncio | F4: `council_decisions` (acatada/rejeitada/por quê); `forja_ledger_material.py` nomina P1, nunca silencia |
| Trabalho em rede, nunca sozinho | Conselho obrigatório Helena + Cícero; separação produtor/revisor (`producer_reviewer_separation`); auditoria adversarial |
| Supervisão humana com palavra final, auditável | `forja_human_review.py` + trust store externo + recibo assinado em F7 e F8; o F15 da proposta externa **já existe** |
| Co-evolução com registro do que o humano mudou | `APRENDIZADOS_FEEDBACK_HUMANO.md` + `forja_diff_docx.py` (protocolada × nossa) + ciclo AR |
| Dossiê de auditabilidade | F9/F10: `package_manifest`, hashes, `run_metrics`, `retrospective`; `RETROSPECTIVAS.md` (80 lições) |
| Síntese executiva na abertura | Já obrigatória por determinação do próprio Fábio (07/07/2026), estilo art. 343-A do RISTJ |
| "Se não reduz esforço cognitivo do julgador, sai da peça" | Já é regra escrita de visual law da fábrica — **é literalmente o teste final de estilo dele**, adotado antes da entrevista |
| Ausência de redundância | `_redundancia()` em `forja_estilo_humano.py` (similaridade entre parágrafos) |

Duas conclusões desta tabela. Primeira: **o harness já honra a espinha dorsal da fala dele** — dúvida antes do trabalho, lastro de fonte, nada silencioso, palavra final humana registrada, co-evolução. Segunda: as três propostas externas subestimam gravemente o que existe (falam em "adaptação, não construção" apenas para F8–F10). Elas foram escritas sem ler o harness.

### 2.2 Lacunas confirmadas por varredura

Termos ausentes de todo o código de produção: `aderência`, `ratio`, `prevento`/`prevenção`, `jurimetria`, `estatística`, `composição da turma`, `legibilidade`, `síntese`/`concisão`, `diligência` (como artefato contratado).

| # | Lacuna | Evidência da falta | Gravidade |
|---|---|---|---|
| **G1** | Pedido endereçado como ato governante + auditoria da adequação do pedido | F0 exige o arquivo `commandFile`, não a sua suficiência; nenhum artefato diz "o comando está mal estruturado diante do acervo, por isto" | Alta |
| **G2** | Pedido de esclarecimentos **ao remetente**, em lote motivado, com dever recíproco de resposta | F2-A é autorrespondida pela própria IA; nada sai endereçado ao Fábio | **Crítica** — é o que ele mais detalhou |
| **G3** | Requerimento motivado de complementação documental como saída contratada, cada item vinculado à tese/fato dependente | Existe só ad hoc em scripts de caso (`build_f3_verifact.py`), nunca como contrato com gate | Alta |
| **G4** | Fixação versionada de **escopo, metodologia e objetivo** com aceite nominal do remetente | F2 fixa produto/risco/audiência/release, autodeclarados; sem `aceite {por, em}`, sem versionamento de mudança de escopo | Alta |
| **G5** | Consulta de preferência doutrinária ao interlocutor; hierarquia de doutrina por matéria | Ausente | Média |
| **G6** | **Topologia decisória**: prevenção, relator prevento, composição **atual** do órgão, posição da turma e da seção, divergência entre fracionários, via recursal projetada, matéria a prequestionar | Ausente. E o `CLAUDE.md` já registra esta falha como lição do caso CASO-04 ("a peça da IA não tratou prevenção/preclusão") | **Crítica — falha conhecida e não corrigida** |
| **G7** | Roteamento **nominal** da pesquisa pela topologia (buscar pelo relator e pelos integrantes) | `forja_legal_search.py` busca por matéria, não por decisor | Alta |
| **G8** | Extração de **ratio decidendi** separada de obiter dictum | Existe apenas como item de checklist na taxonomia U1 ("tese deturpada"), não como artefato | Alta |
| **G9** | **Aderência fático-probatória**: identificação da ratio, moldura fática determinante do paradigma, confronto elemento a elemento, **operação declarada** (aplicar, distinguir, delimitar alcance ou sustentar superação), distinção possível pelo adversário e resposta antecipada | Ausente | **Crítica — é o "principalmente" dele, duas vezes** |
| **G10** | Por precedente: grau de vinculação + situação de vigência (superação, modulação, afetação posterior por tema repetitivo ou de repercussão) | Parcial: detectamos súmula vinculante e tema, e conferimos fonte com data; não há campo de vigência verificado por precedente | Alta |
| **G11** | Geração divergente com mínimo por classe + poda com pontuação por critério e reconciliação (aprovadas + descartadas = total gerado) | Parcial: blueprint, `proposition_ledger` e conselho existem; falta o ledger de teses com contagem fechada | Média |
| **G12** | Precedente **administrativo** na hierarquia (TCU, CNJ, CGU/CRG, CADE, CVM) | `forja_authorities.py` só conhece CNJ/STJ/STF/súmula/tema. Ele estendeu a teoria dos precedentes ao contencioso administrativo — que é o terreno dele | Alta |
| **G13** | Gates de estilo **positivos**: densidade, extensão máxima por classe de peça, voz passiva, subordinação encaixada, latinismo decorativo, adjetivação valorativa sobre conduta de terceiro, argumento em nota de rodapé, distância alegação↔âncora, "cada seção justifica sua existência" | `forja_estilo_humano.py` detecta cheiro de IA e redundância; não mede síntese, acessibilidade nem extensão | Alta |
| **G14** | Proibição de desqualificar o advogado adversário, como gate | Existe como cultura, não como validador | Média |
| **G15** | **Módulo de jurimetria** (comportamento decisório; benchmarking de deságio) | Ausente | Alta em valor, alta em risco |
| **G16** | Memória institucional estruturada: teses reaproveitáveis, precedentes qualificados por matéria, padrões de aderência por órgão, corpus vivo das alterações do revisor | Parcial: `RETROSPECTIVAS.md`, `_MODELOS`, ciclo AR. Falta a memória indexada por matéria e por órgão | Média |
| **G17** | **Perfil de identidade calibrado por corpus** das peças assinadas por ele | Ausente. Dependência externa, não de engenharia | Alta |
| ~~**G18**~~ | ~~Triagem de conflito de interesses, sigilo, segredo de justiça e perímetro~~ | **REJEITADO em 04/08/2026 por ordem do Igor.** Nenhum dos quatro é padrão computável, e o próprio quadro registrava que **o Fábio não pediu**: a lacuna era inferida pela análise, não relatada pelo escritório. Conflito e sigilo são juízo humano sobre o caso, não gate. | — |
| **G19** | Métrica de sucesso acordada com ele | Temos `run_metrics` e `METRICAS_GATES.json` internos; nenhuma métrica de negócio pactuada | Média |

---

## 3. Avaliação dos três documentos externos

Aproveitáveis, com três correções materiais.

**Adotar:**
- "Explicação não é log, é peça endereçada a um humano" — formulação melhor do que a nossa.
- A tabela de rastreabilidade requisito→fase, como instrumento de apresentação ao titular. Demonstra que a arquitetura decorre da fala dele.
- O antipadrão do lote de perguntas: **nunca perguntar o que já consta do acervo inventariado**. Deve ser validador com bloqueio. É a observação mais útil dos três documentos.
- Perguntas em **lote único ordenado por impacto**, não em conversa, com teto de rodadas por classe. É a única forma de honrar o ganho de velocidade que ele prometeu.
- "Descarte silencioso é exatamente o que a auditabilidade existe para impedir", com reconciliação de contagem.
- Leitura de que a identidade dele é arquitetural e não lexical; e a precedência final: camada lexical nunca prevalece sobre correção substantiva.
- Protocolo de calibração por corpus, inclusive a exigência de duas ou três peças que **ele considere ruins** — o contraste ensina mais que o exemplo.
- Validação cega com dois sócios que não participaram do projeto.
- Contenção do módulo de jurimetria.

**Corrigir:**

1. **Não renumerar as fases.** A proposta cria dezesseis fases novas. Isso invalidaria os 11 contratos, cerca de 40 suítes de teste, o `FORJA_SPEC_MANIFEST.json`, a máquina de estados e os 49 casos já em `state/`. Os requisitos dele cabem como **subfases** dentro de F0–F10, no padrão que já usamos e que já funcionou duas vezes (F2-A da exploração em 100 perguntas, F7-B do Fable 5). Mapeamento proposto: F1-B recepção e adequação do pedido; F2-B lote de esclarecimentos e diligências; F2-C fixação de escopo com aceite; F3-B topologia decisória; F5-B ratio e aderência; F6-B contrato estilístico. O custo de integração cai de "reescrever o harness" para "seis artefatos e seis gates".

2. **A tensão "recall contra precisão" não está na fala dele.** A proposta afirma que ele quer objetivos opostos e que "a premissa precisa ser recalibrada". Ele próprio ordena as duas exigências: pede quantidade superior de teses e, na frase seguinte, [literal] "por outro lado, ela parte de uma previsão de que as teses jurídicas a serem articuladas precisam ter forte plausibilidade... as teses precisam ter uma conectividade lógica". Ele também rejeita expressamente o modelo de máquina autônoma. Levar essa "recalibração de expectativa" para a reunião seria corrigir algo que ele não errou.

3. **"Consequência institucional" não é a oitava seção da peça — é o motor.** A proposta a coloca em penúltimo lugar na arquitetura argumentativa. Ver §4.3: o movimento de constrangimento por incoerência é o que organiza a peça dele inteira.

**Ajustes menores:** reutilizar `_redundancia()` de `forja_estilo_humano.py` em vez de construir similaridade semântica nova; voz passiva como aviso P2, não gate duro, porque em português jurídico há uso legítimo; e o módulo de jurimetria exige parecer do Cícero por uso, não só autorização do titular.

---

## 4. Padrões de pensamento e de linguagem dele

Extraídos da fala. Separo o que é **oral** — e que não deve ser imitado em peça escrita — do que é **cognitivo**, que é o que deve ser codificado.

### 4.1 Padrões de fala (não transportar para o texto)

- **Tríades.** "a dedicação, a seriedade, a ética"; "escopo, metodologia, objetivo"; "qualidade, rapidez, velocidade"; "acesso, resolutividade, capacidade". É o ritmo dele. Na escrita isso vira enumeração, e só quando cada item faz trabalho próprio.
- **Aproximação sucessiva.** Reformula com "quer dizer", "ou seja", "portanto", apertando o enunciado a cada volta. **A última formulação é sempre a mais precisa** — daí a regra de extração do §0.
- **Hedge epistêmico sistemático.** "eu acho que", "eu penso que", "ao nosso ver", "no meu modo de ver", "talvez". Ele marca opinião como opinião, de forma consistente. Coincide com a exigência de rotular `[Inferência]` e `[Não verificado]` que já usamos: ele faz isso naturalmente e vai reconhecer as marcações como suas.
- **Concessão antecipada.** "obviamente", "óbvio que" — concede a objeção provável do interlocutor antes de avançar.
- **Pergunta retórica seguida de resposta.** "O que é que eu espero, por exemplo? Eu espero..."; "Daqui você quer exatamente o quê?"
- **Encenação.** Ele argumenta pondo a cena em fala direta: "olha, em tantas situações análogas o acordo foi de 30%..."; "eu analisei toda essa documentação, você está me pedindo isso, o seu pedido não está claro". Na peça isto reaparece como "veja-se" e "vejam" — ele usa os dois: "veja o constrangimento que sugere", "vejam aí".
- **Autodepreciação como credibilidade.** "eu não sou um grande escritor", "mero mortal", "não sou o melhor do Brasil nem do mundo". Nunca sobre competência — só sobre comparação.

### 4.2 Léxico dele (vocabulário positivo, extraído literalmente)

íntegra; corpo documental; checklist; rastrear; lastro; aderência fático-probatória; ratio decidendi; precedente qualificado; precedente vinculante; graduação hierárquica; prevento; órgão fracionário; seção; Corte Especial; prequestionamento; multiplicação de teses; conectividade lógica; plausibilidade; hermenêutica; retórica; argumentação; integridade e coerência; isonomia; força coercitiva; **constrangimento**; **desmoralização**; desvio de finalidade; desvio de poder; subjetivismo desenfreado; auditabilidade; explicabilidade; rastreabilidade; dever de fundamentação; parametrização do risco jurídico; jurimetria; resolutividade; descongestionamento; **espaço público não estatal**; **soberania cognitiva**; **IA artesanal**; **IA dialogante**; poder de síntese; acessibilidade; transparência; concretude; agenda de desenvolvimento.

Usados por ele como pejorativos: **rebuscado, erudito, volumoso, aleatoriamente, desenfreado, inauditável**. São candidatos diretos à lista de proibições do contrato estilístico.

### 4.3 Padrões cognitivos (estes são para codificar)

**a) Analogia estruturante como porta de entrada.** Abre definindo o objeto por um corpo: [literal] "cada processo é como se fosse um corpo único, anatomia de um corpo". Depois sustenta o primeiro terço inteiro na analogia advogado↔IA, e **deriva deveres da analogia**. Consequência prática e barata: ele pensa em **atos**, e nossos artefatos têm nomes de etapa de engenharia (`F2_CLASSIFICACAO_PRODUTO_RISCO`). Nomear cada artefato pelo ato correspondente — termo de recebimento, pedido de esclarecimentos, requerimento de diligências, fixação de escopo, dossiê — torna o harness legível para ele a custo quase zero.

**b) Transporte dogmático — a assinatura intelectual dele.** Pega uma garantia consolidada num campo e exige seu transporte para outro: motivação do ato público → IA; teoria dos precedentes judicial → contencioso administrativo; garantias do direito punitivo → direito administrativo sancionador. **Se quisermos que uma peça soe como ele, o movimento estrutural é este:** identificar a garantia que já existe em outro lugar e exigir sua aplicação aqui.

**c) Constrangimento por incoerência — o motor da peça.** Aparece três vezes na entrevista, sempre com a mesma forma:
1. estabelecer o que a autoridade decidiu antes, ou em casos análogos;
2. mostrar que decidir diferente agora rompe isonomia e coerência;
3. nomear a **consequência para quem decide** — desmoralização, e possível responsabilização.

Instâncias: precedente ([literal] "uma autoridade, se ela não segue um precedente, ela de alguma forma se desmoraliza por falta de coerência... haverá uma quebra de isonomia"); jurimetria ("veja o constrangimento que sugere"); deságio ("o gestor público pode ser responsabilizado perante o Tribunal de Contas da União"). O terceiro passo é mais duro do que "consequência institucional" sugere: ele **nomeia o risco pessoal do decisor**.

**d) "Desmoralização" como conceito operativo de dano.** Usa a mesma palavra para o juiz que rompe o próprio precedente e para a IA que erra a pesquisa: [literal] "sempre que uma pesquisa se revelar falsa ou errada, o inauditável sempre vai causar desmoralização daquele que usa a IA como ferramenta... a IA ela própria se desmoraliza como ferramenta e desmoraliza o seu usuário". É o elo mais profundo da entrevista: **citação falsa faz ao advogado exatamente o que a quebra de precedente faz ao juiz.** Por isso ele trata alucinação como problema existencial, não técnico — e por isso o bloqueio duro de precedente não verificado é doutrina, não paranoia de engenharia.

**e) Enquadramento institucional, nunca conflitual.** Sempre alarga: caso concreto → órgão → instituição → agenda de desenvolvimento do país. O caso é episódio de um sistema.

**f) Consequencialismo centrado no leitor.** Nenhuma regra de estilo dele é estética. Cada uma é derivada de consequência para uma pessoa: o julgador atordoado na fila; a pessoa representada; o acesso à justiça. O contrato estilístico deve trazer a justificativa por consequência junto de cada regra — é assim que ele aceita regra.

**g) Simetria de direitos e deveres.** Confere direitos à IA (receber pedido endereçado, ter dúvidas, pedir esclarecimento) e no mesmo movimento impõe deveres a ela e o dever recíproco ao humano ("cabe a quem endereçou responder"). Ele modela tudo como **relação jurídica**. Isto legitima o bloqueio duro: recusar-se a começar sem pedido adequado é exercício de um direito que ele concedeu, não insubordinação.

**h) Velocidade por antecipação, nunca por atalho.** Todo o argumento de velocidade é: perguntar cedo, pedir documento cedo, paralelizar. Em nenhum momento é "pular a conferência".

**i) Ampliar e depois podar.** Faz isso com teses (leque amplo → forte plausibilidade) e retoricamente (lista possibilidades → "mas principalmente...").

**j) "Principalmente" como marcador de prioridade.** Duas ocorrências, ambas sobre precedente: **uso adequado** e **aderência ao caso concreto**. É o sinal mais confiável de onde ele quer investimento.

### 4.4 Entrelinhas — o que ele quis dizer sem dizer

1. **A dúvida da IA é o produto, não o defeito.** Ele gasta cinco minutos defendendo o direito de perguntar e antecipa quatro vezes a objeção de lentidão. Isto só se explica se ele já viu ferramentas que fingem entender e entregam trabalho errado. Ele está pedindo uma IA que **admite não saber** — e prometendo, em troca, responder.
2. **O lote de teses serve para extrair o que ele nunca escreveu.** [literal] "a IA pode suscitar no interlocutor outras teses que o interlocutor tenha... e aí ele reflita". Não é cortesia: é elicitação de conhecimento tácito. Ele sabe que o ativo mais valioso do escritório está na cabeça dos sócios e que só sai se provocado por uma lista concreta. Por isso as teses devem ser mostradas **antes** da pesquisa, e a origem de cada uma precisa ser marcada.
3. **O requerimento de diligências é o exame de admissão da IA.** [literal] "mostrar que compreendeu o escopo do seu trabalho". A primeira coisa que ele vai avaliar em qualquer entrega não é a peça — é se o pedido de documentos revelou compreensão do caso. É o nosso primeiro teste real com ele.
4. **Ele recusou o papel de especificador.** "não de uma forma divina, de uma criatura perfeita que nasce pronta... cresceríamos juntos". Uma proposta apresentada como especificação fechada vai contra o que ele acabou de dizer. Apresentar com a tabela de parâmetros por classe **em branco, para preencher com ele**, é a forma correta — e é a melhor recomendação dos três documentos externos.
5. **Ele quer ser multiplicador de método, não dono de ferramenta.** [literal] "ser um multiplicador dessa cultura... multiplicar uma cultura na qual eu acredito, que pode transformar para melhor a sociedade e as instituições". Há tensão a administrar com o plano de propriedade intelectual (`planejamento/24`): a titularidade é do Igor, e o desejo declarado dele é difundir o método. Não é conflito — publicar o método e licenciar a implementação são compatíveis — mas precisa ser conversado, não descoberto depois.
6. **Ele já tem texto escrito sobre "soberania cognitiva" e sobre "espaço público não estatal".** Ler antes da reunião. São as molduras conceituais em que ele vai encaixar a FORJA, e citá-las com precisão vale mais do que qualquer demonstração técnica.
7. **A jurimetria é a obra dele voltada para os decisores.** A carreira é improbidade e sancionador — controle de autoridade. Pedir estatística de comportamento judicial é aplicar o mesmo instrumento a quem julga. É por isso que ele não hesitou ao descrever, e é por isso que a contenção tem de ser da engenharia.
8. **Ele nunca mencionou custo, licença, prazo de projeto ou tecnologia.** Não é desinteresse: ele avalia por outro eixo — [literal] "sempre que uma pesquisa se revelar falsa ou errada... desmoraliza o seu usuário". **O critério de compra dele é confiabilidade auditável.** Uma demonstração de velocidade impressiona menos que uma demonstração de que o sistema se recusou a citar um precedente que não conseguiu verificar.

---

## 5. Plano de instalação proposto

Não construir tudo. Ordem por retorno sobre esforço, respeitando que os requisitos entram como **subfases** de F0–F10 (§3, correção 1).

**Onda 1 — o que ele mais detalhou, e a falha que o escritório já apontou uma vez**
1. **G6 + G7 — topologia decisória e roteamento nominal** (subfase F3-B). Falha conhecida do caso CASO-04, ainda sem artefato. Reaproveita `forja_legal_search.py` e `forja_f2_check.py`. Campos de prevenção preenchidos ou expressamente marcados como não apurados, com motivo.
2. **G1 + G2 + G3 — bloco de instrução** (subfases F1-B e F2-B). Barato porque o difícil já existe: o F2-A já produz pergunta bloqueada com consequência e rota de diligência. Falta rotear um subconjunto **para fora**, em lote ordenado por impacto, com razão da necessidade, e acrescentar o validador do antipadrão (não perguntar o que está no acervo).
3. **G4 — fixação de escopo, metodologia e objetivo com aceite nominal** (subfase F2-C). Reaproveita integralmente a máquina de recibo assinado e trust store externo que já opera em F7 e F8.
4. **G13 — contrato estilístico verificável** (subfase F6-B), estendendo `forja_estilo_humano.py`. É o que se demonstra mais rápido numa peça real.

**Onda 2 — o ativo durável**
5. **G8 + G9 + G10 — ratio e obiter, aderência fático-probatória, vigência por precedente** (subfase F5-B). É o "principalmente" dele. É também o que separa o sistema de um buscador, e o que nenhum concorrente tem.
6. **G11 — ledger de teses com geração e poda reconciliadas.**
7. **G12 — camada de precedente administrativo** em `forja_authorities.py`.
8. **G14 — gate de não desqualificação do adversário.**

**Onda 3**
10. **G16 + G17 — memória institucional indexada e calibração de identidade por corpus.** Depende de insumo dele.
11. **G19 — métricas pactuadas.**
12. **G15 — módulo de jurimetria**, por último, com contenção e parecer do Cícero por uso.

**Insumos que só ele pode dar — pedir na reunião**
- 20 a 30 peças assinadas, estratificadas por tipo, incluindo duas ou três que ele considere ruins.
- Preferência doutrinária por matéria (autores de referência).
- Preenchimento da tabela de parâmetros por classe de caso: teto de rodadas de esclarecimento, mínimo de teses, limiar de nota de aderência, extensão máxima da peça, nível de revisão exigido, disponibilidade do módulo de jurimetria.
- Autorização e limites do módulo de jurimetria.
- Os textos dele sobre soberania cognitiva e espaço público não estatal.

**Como apresentar.** Tabela requisito→fase (demonstra que a arquitetura decorre da fala dele); demonstração ao vivo de um bloqueio — o sistema recusando citar precedente não verificado, porque é o critério de compra dele (§4.4.8); e a tabela de parâmetros **vazia**, para preencher com ele, porque ele recusou o papel de especificador (§4.4.4).

---

## 6. Registro de rastreabilidade

| Requisito declarado | Formulação na entrevista | Onde entra no harness | Estado |
|---|---|---|---|
| Pedido endereçado governa | "olhar o pedido endereçado a ela... em cima da documentação" | F0/F1-B | G1, falta |
| Checagem documental integral | "checklist completo... do início ao fim... rastrear todos" | F1 | existe |
| Auditoria da adequação do pedido | "se esse pedido é bem estruturado ou não" | F1-B | G1, falta |
| Direito e dever de duvidar | "ela deve ter dúvidas, deve suscitar dúvidas antes de iniciar" | F2-A | existe, interno |
| Esclarecimentos ao remetente | "pedido de esclarecimentos ao remetente da demanda" | F2-B | G2, falta |
| Diligência documental motivada | "não basta ir simplesmente... mostrar que compreendeu" | F2-B | G3, falta |
| Escopo, metodologia e objetivo fixados | "delimitar o escopo, a metodologia, onde o remetente quer chegar" | F2-C | G4, falta |
| Diligência não bloqueia cognição | "independentemente de prosseguir no aprofundamento" | F2-A | existe |
| Diálogo que colhe teses | "colher a opinião do interlocutor... suscitar insights" | F4 | G5 e G11, parcial |
| Multiplicação de teses | "articular uma quantidade superior" | F4 | G11, parcial |
| Plausibilidade e conectividade lógica | "forte plausibilidade... conectividade lógica" | F4 | G11, parcial |
| Topologia e prevenção | "relator prevento, turma, seção, Corte Especial" | F3-B | **G6, falta** |
| Hierarquia e qualificação de precedente | "graduação hierárquica, qualificados, vinculantes" | F5 | G10 e G12, parcial |
| Íntegra e fonte idônea | "rastreamento da íntegra... fontes idôneas" | F5 e F7 | existe |
| Uso adequado e seleção correta | "mas principalmente o uso adequado" | F5-B | **G9, falta** |
| Ratio decidendi | "identificação da ratio decidendi" | F5-B | **G8, falta** |
| Aderência fático-probatória | "a aderência fático-probatória... com o precedente a ser utilizado" | F5-B | **G9, falta** |
| Prequestionamento | "matéria constitucional por prequestionamento futuro" | F3-B e F4 | parcial (existe como diretriz do escritório) |
| Correção do idioma | "seguir rigorosamente as regras do idioma" | F6-B | parcial |
| Síntese, objetividade, sem redundância | "o poder de síntese... ausência de redundâncias" | F6-B | G13, parcial |
| Acessibilidade sem rebuscamento | "muito direto, objetivo, acessível, sem rebuscamento" | F6-B | G13, falta |
| Concretude | "muito concreta, aderente à realidade, mostrar a realidade" | F6-B | G13, falta |
| Não desqualificar o adversário | "nunca me comparar... cada um tem sua singularidade" | F6-B | G14, falta |
| Crítica adversarial | "melhor objeção... caminho mais estreito para negar" | F7 | existe |
| Supervisão humana com palavra final | "terá que ter a palavra final" | F7 e F8 | existe |
| Auditabilidade das próprias buscas | "explicabilidade nas suas buscas, nos seus parâmetros" | F5 e F9 | parcial |
| Co-evolução com registro | "cresceríamos juntos" | F10 e ciclo AR | existe |
| Jurimetria de comportamento decisório | "análise estatística... o constrangimento que sugere" | Módulo J | **G15, falta** |
| Benchmarking de deságio em acordos | "em tantas situações análogas o acordo foi de 30%" | Módulo J | **G15, falta** |
| Conflito, sigilo, perímetro | não declarado pelo Fábio | — | **G18 rejeitado 04/08** — juízo humano, não gate |
| Identidade calibrada por corpus | não declarado | F6-B | G17, falta |
