# Reforma do diagnóstico e do design da FORJA — van Aken e The McKinsey Mind

**Documento:** 39
**Data:** 2026-07-30
**Autor:** sessão Claude (primeira passada em Opus 5; revisão crítica na mesma sessão após troca para Fable 5 — ver §12)
**Status:** estudo + plano de reforma. Não altera código nem contratos até decisão do Igor.
**Escopo:** fases de exploração do problema (F2/F2A), pesquisa prévia (F3) e design da solução (F4/F5).

## Fontes estudadas

| Fonte | Como foi lida | Verificação |
|---|---|---|
| Van Aken & Berends, *Problem Solving in Organizations*, 3. ed., Cambridge, 2018 | OCR integral local, leitura verbatim dos cap. 4, 5, 6 e 12 | SHA-256 `12d0f7ef…c167e`, idêntico ao registrado no doc 14 — mesma edição |
| Rasiel & Friga, *The McKinsey Mind* | NotebookLM `b565f70b`, fonte `the mckinsey mind.pdf`, duas consultas dirigidas com exigência de capítulo/página | Citações de página vêm do NotebookLM e **não foram conferidas no PDF**; ver §8 |
| Artefatos reais da FORJA | 7 casos com `FORJA-F2A-100-v1`, contratos de fase, `forja_pso_pet.py` | Medição própria, reproduzível |

O notebook `3003e19d` (só o livro van Aken) não foi consultado: o OCR local é fonte superior, permite leitura verbatim e tem hash conferido.

---

## 1. Síntese executiva

Três conclusões, em ordem de importância.

**Primeira: a FORJA já tinha van Aken e o perdeu.** Em 11/07/2026 o método foi estudado a fundo e virou o perfil PSO-Pet 1.0 — doc 14 (489 linhas), roteiro `templates/F4_METODO_SOLUCAO_PROBLEMA_PETICAO.md`, validador `forja_pso_pet.py`, schemas em `pso_schemas/`. Nada disso rodou uma única vez: não há um só `PSO_CASE.json` nos 51 casos de `state/`, e `forja_pso_pet.py` não é referenciado por nenhum contrato de fase, gate ou runner — só por seu próprio teste. Foi declarado *shadow-only*, sem elo bloqueante e sem dono. **Na FORJA, o que não tem contrato de fase e gate não acontece.** Essa é a lição de arquitetura que condiciona todo o resto deste plano.

**Segunda: as 100 perguntas degeneraram em formulário, e a causa é o formato, não a execução.** Medição nos 7 casos que rodaram o protocolo:

| Campo | Valores distintos entre as 100 perguntas |
|---|---|
| `caseAnchor` | 1 (em 6 dos 7 casos) |
| `whyItMatters` | 10 — um texto por ótica, copiado dez vezes |
| `unansweredConsequence` | **1** — a mesma frase nas 100 |
| `downstreamTargets` | 1 — `[F3,F4,F5,F6,F7]` em todas |
| Palavras por resposta | 23 a 59 |

Em 6 dos 7 casos, **100 de 100 perguntas saíram `answered` e nenhuma bloqueada**. Nos dois casos Melissa, 100 respondidas com 34 `supportIds`. O protocolo manda "não responder por memória ou para fechar 100" e manda reescrever cada pergunta com nomes de atos e datas do caso; nenhuma das duas regras sobreviveu ao contato com a cota. No CASO-04 as perguntas ficaram genéricas — "Que evento criou a necessidade da peça atual?", "Que pedido pode parecer excessivo?".

O mecanismo é identificável no código: o gate se chama `exploration_100_complete`. Ele premia completude numérica. Uma meta numérica vira alvo, e o alvo é atingido pelo caminho mais barato — preencher. Nenhum ajuste de conteúdo dentro do formato corrige isso, porque o incentivo está no formato.

**Terceira: os dois livros convergem contra o desenho atual e divergem entre si de um modo aproveitável.** Ambos dizem que exploração termina por **suficiência decisória**, nunca por contagem — van Aken pela saturação (nada de novo aparece), McKinsey pelo "E daí?" (o achado não muda recomendação nenhuma). E divergem no ponto certo: van Aken é *diagnosis-first* (não desenhe solução antes de validar o problema e suas causas), McKinsey é *hypothesis-first* (parta da conclusão mais provável e tente matá-la). Essa tensão não deve ser resolvida escolhendo um lado: petição tem uma parte que é diagnóstico factual-processual (van Aken manda) e uma parte que é escolha de tese sob prazo (McKinsey manda). O plano abaixo aloca cada método onde ele é superior.

**Recomendação central:** substituir a cota de 100 perguntas por uma **árvore de questões decisórias com poda**, sob hipótese explícita, com plano de trabalho por folha e parada por saturação. Estimo redução material do preenchimento vazio e — mais importante — antecipação da morte de teses inviáveis para antes da redação, que é onde está o retrabalho de 30-40% documentado no CLAUDE.md.

---

## 2. Por que o PSO-Pet morreu (e o que isso impõe a esta proposta)

Quatro causas, todas verificáveis:

1. **Sem elo bloqueante.** Declarado "em sombra; não promove N4 nem cria bloqueio automático" (doc 14, cabeçalho). O F2A-100 nasceu com validador *e* ordem inviolável no CLAUDE.md *e* gate no contrato F2 — e rodou em 7 casos.
2. **Sem invocação.** `forja_pso_pet.py` existe e tem teste, mas nenhum runner o chama. Código órfão.
3. **Artefato paralelo.** O doc 14 §14 mapeia corretamente o método sobre os JSONs existentes, mas o produto por caso era um roteiro Markdown novo, fora do pipeline N4. Artefato que não é consumido por fase seguinte não é produzido.
4. **Gates de promoção inalcançáveis por construção.** O §16 exigia três casos-piloto prospectivos — mas nada agendava esses pilotos.

**Consequência para este plano:** qualquer técnica adotada aqui entra como (a) campo obrigatório em artefato JSON já consumido a jusante, (b) checagem em validador executável, (c) gate nomeado no contrato de fase. O que não couber nas três, não entra — fica registrado como rejeitado, não como "futuro".

---

## 3. Destilação — van Aken

Marco o que o doc 14 já capturou e o que ficou de fora. O que ficou de fora é onde está o ganho.

### 3.1 Já capturado no doc 14 (manter, sem retrabalho)

Ciclo P0–P8; fórmula canônica da definição do problema; distinção resultado direto × intermediário × final; quatro categorias de requisitos; matriz qualitativa de alternativas sem probabilidade numérica; validação invertida (da solução para os requisitos); regra do "sem surpresa"; CIMO para aprendizado; especificação mínima; triangulação.

### 3.2 Não capturado — as sete técnicas que faltam

**(A) Problema real × problema de percepção × problema de meta** (Monhemius, 1984 — cap. 5.3, "Validating the Business Problem"). Antes de diagnosticar causas, é preciso decidir se o problema *existe*. Problema de percepção: o dono do problema tem leitura inexata do sistema. Problema de meta: a meta é irreal para o padrão do setor. Só o problema real merece projeto. Van Aken exige **norma e evidência** para classificar — sem norma, não se pode afirmar que há problema.

Tradução jurídica, e é a técnica de maior valor deste documento: o comando do escritório pode ser (i) problema real — há omissão, erro de premissa, nulidade; (ii) problema de percepção — o acórdão de fato enfrentou a questão, e o que existe é inconformismo; (iii) problema de meta — pretende-se de um recurso efeito que sua cognição não comporta (rediscutir prova em REsp, por exemplo). A FORJA hoje trata os três como se fossem o mesmo, e produz embargos de declaração para inconformismo — que é exatamente o vício que o Alessandro combate nas 8 diretrizes já citadas no CLAUDE.md. A norma aqui é o regimento, a cognição do veículo e o texto da decisão; a evidência é o cotejo verbatim entre o que se alegou e o que o acórdão decidiu.

**(B) Saturação como critério de parada** (cap. 5.3, citando Glaser & Strauss). A exploração termina quando novas entrevistas, novos incidentes ou novos documentos deixam de produzir informação nova — não quando se atinge um número. É a resposta direta e literária ao problema das 100 perguntas.

**(C) Causas acionáveis e condições de contorno** (cap. 5.1 e 5.5). Causas fora do alcance do principal viram *condição*, não objeto de intervenção. No exemplo EcoLogic, o estudante descartou "pressão ambiental" porque estava fora da responsabilidade do principal, e descartou "falta de visão de expertise" porque já havia solução em curso. Tradução: fato desfavorável consolidado, preclusão operada e matéria fora da cognição do veículo são *condições de contorno da peça*, e gastar argumento nelas é desperdício — a peça deve atacar o elo que ela pode mover.

**(D) Posição do problema na árvore causa-efeito determina o trade-off relevância × viabilidade** (cap. 4.3). À direita (sintoma final) o problema é mais relevante e menos viável; à esquerda (causa raiz distante) é mais viável e menos relevante. Escolhe-se um nó intermediário. Tradução: escolher o nível certo do pedido — pedir a reforma integral do acórdão é relevante e inviável; atacar um vício pontual sem consequência é viável e irrelevante.

**(E) A história diagnóstica como teste de maturidade** (cap. 5.6). Não é lista de defeitos: é explicação integrada, em poucas frases, de como os fatores se produzem e se realimentam. O exemplo do hospital (pacientes com DPOC) mostra o ciclo vicioso: alta sem treino de inalação → deterioração → internação de emergência → pressão sobre leitos → alta sem treino. Van Aken é categórico: **se a história não pode ser contada de forma coerente, o diagnóstico ainda não está pronto** e um redesenho coerente é impossível. Isso é um gate barato e potente, e o doc 14 o menciona (§6.2) sem torná-lo verificável.

**(F) Triangulação com limite inferior conservador** (Box 5.2). Três fontes sobre a mesma questão deram 5%, 11% e 4%; o estudante concluiu "em ao menos 4% dos casos". Tradução direta para peça: quando as fontes divergem sobre quantum, data ou extensão, afirmar o **limite que todas sustentam**, não a média nem o número mais favorável. Isso ataca de frente o erro recorrente nº 2 do CLAUDE.md (premissa não declarada) e a lição registrada na memória de que achado forte gera excesso na redação.

**(G) Loop B — renegociar requisitos** (cap. 12.4). Quando muitas iterações síntese-avaliação não convergem, não se insiste: renegocia-se o requisito com o principal, para cima ou para baixo, e registra-se. Hoje a FORJA trava ou entrega abaixo do requisito sem dizer. Loop B dá o caminho legítimo: escrever que o requisito foi rebaixado, por quê, e com autorização de quem.

### 3.3 Um achado conceitual que muda como pensar a peça

Van Aken distingue **primeiro redesenho** (o sistema formal projetado pelo agente de mudança) e **segundo redesenho** (a apropriação pelos atores, que sempre adaptam à sua circunstância). E: em sistema social, **sobre-especificar é danoso** — ao contrário do domínio material, onde só desperdiça.

Aplicado à petição: a peça é o primeiro redesenho; o segundo é o que o relator e o gabinete fazem com ela. A decisão nunca é determinada pela peça — é reconstruída pelo leitor. Isso tem consequência prática imediata sobre a diagramação: o excesso de estrutura, de marcação e de conclusão pré-mastigada não aumenta controle, reduz apropriação. A regra já existente na fábrica — "se o elemento não reduz esforço cognitivo do julgador, sai da peça" — ganha aqui fundamento teórico e um critério: preservar espaço para o julgador chegar à conclusão, ancorando poucos pontos decisórios com força, em vez de fechar todos.

---

## 4. Destilação — The McKinsey Mind

### 4.1 As técnicas que valem

**(A) Hipótese inicial + Quick and Dirty Test** (cap. 1, p. 15-23). Formula-se a conclusão mais provável antes da coleta massiva; para cada hipótese pergunta-se *"quais premissas precisam ser verdadeiras para isto se sustentar?"*, e se **qualquer premissa pode ser refutada em minutos, a hipótese morre imediatamente**. No exemplo Acme Widgets, duas das três ideias morreram no QDT (fornecedores monopolizados; fábrica já a mais produtiva do setor) antes de qualquer análise.

Tradução jurídica — e este é o item de maior retorno imediato: o QDT jurídico mata teses natimortas antes da redação. Premissas que se refutam em minutos: intempestividade, ausência de prequestionamento, matéria de prova barrada pela Súmula 7/279, preclusão consumada, incompetência do órgão, ausência de interesse recursal. Hoje a FORJA descobre isso tarde — ou não descobre, e a auditoria F7 gasta o dobro. O QDT é barato: são consultas curtas a fontes que a fábrica já tem.

**(B) Issue tree terminando em sim/não, com poda** (cap. 1, p. 16 e 23-28). Hipótese no topo; desdobramento em questões de nível superior; subdivisão até chegar a perguntas respondíveis por sim ou não. **Um "não" elimina todo o ramo.** O erro que previne é nomeado no livro: o desejo de ser "uniformemente completo", isto é, investigar tudo com a mesma profundidade — exatamente o que as 10 óticas × 10 perguntas fazem hoje.

**(C) MECE com dois testes explícitos** (cap. 1, p. 3-6 e 11-14). Teste 1, mutuamente exclusivo: algum item do ramo A também pertence ao B? Teste 2, coletivamente exaustivo: somados, os ramos cobrem todos os cenários? Van Aken também adota MECE para causas (cap. 5.3, citando Baaij) — os dois livros concordam aqui.

**(D) Work plan de sete colunas** (cap. 2, p. 42-46). Para cada folha da árvore: (1) questão e sua hipótese; (2) análise a realizar; (3) dado necessário; (4) fonte do dado; (5) formato do produto; (6) responsável; (7) prazo. É a ponte executável entre exploração e pesquisa, e é precisamente o que falta hoje entre F2A e F3: `downstreamTargets` com `[F3,F4,F5,F6,F7]` em todas as 100 perguntas não roteia nada.

**(E) Duplo teste de parada: "E daí?" e sanity check** (cap. 2, p. 33-42; cap. 4, p. 85-93). Cada achado passa por "isto aponta para alguma recomendação?" e por "o quão errados precisaríamos estar para mudar de conclusão?". O exemplo do Conseco encerra ramos inteiros com uma pergunta de escala.

**(F) Não aceitar o diagnóstico do cliente** (cap. 1, p. 16 e 20-21). O consultor desconfia como o médico desconfia da autoavaliação do paciente. No caso Falkowski, o "problema" apresentado era o CFO; a análise mostrou que era o próprio CEO. Convergente com van Aken §4.3 (problema pré-definido pelo principal) e com a 9ª pergunta anti-bajulação do red team já instalada (upgrade U4).

**(G) Matar a própria hipótese sem apego** (cap. 4, p. 85-99). "Não faça os fatos se encaixarem na sua solução." Quando os dados refutam, muda a hipótese, não os fatos. Suprimir dado divergente para salvar recomendação elegante destrói a honestidade intelectual do processo.

**(H) Pirâmide, teste do elevador e regra de três** (cap. 4, p. 94-99; cap. 5, p. 104-114). Conclusão primeiro, seguida de três razões de suporte. O teste do elevador — explicar a solução em 30 segundos — é um **critério de aceitação** para a síntese executiva que o Prof. Fábio já exige em toda peça: hoje a exigência existe sem teste de qualidade.

**(I) Prewire** (cap. 5, p. 116-123). Discutir conclusões com os decisores antes da apresentação formal. Van Aken diz o mesmo com outro nome ("no surprises", cap. 6.5). Na FORJA isso já existe como conselho Helena + Cícero — o que falta é a regra de que **questão estratégica grave não pode aparecer pela primeira vez no pacote final**.

### 4.2 O que rejeitar do McKinsey, e por quê

| Técnica | Motivo da rejeição |
|---|---|
| "Ordem de grandeza" e precisão direcional ("estar aproximadamente certo em vez de precisamente errado") | Aceitável para alocar esforço analítico; **inaceitável para o que se afirma na peça**. Data, valor, citação e autoridade exigem exatidão verificável. Aplicar 80/20 ao esforço, nunca à asserção. |
| Omitir detalhes analíticos "que não ajudam a contar a história" | Colide com lealdade processual e com o gate de lastro. Seleção honesta de ênfase é legítima; supressão de fato desfavorável conhecido não é. |
| Tática Columbo, contornar o "sandbagger", abordagem indireta | Técnicas de consultoria adversarial aplicadas ao próprio cliente. Impróprias na relação com o titular e com a equipe do escritório. |
| Entrevista em duplas, guia enviado com antecedência, nota de agradecimento | Não rejeitado por mérito — simplesmente fora do escopo desta reforma. Pode servir à entrevista do titular (doc 29), que é outro assunto. |
| Priorizar "quick wins" | Em petição, o argumento mais fácil de verificar não é o mais decisivo. Priorizar por **impacto na pergunta jurisdicional**, não por facilidade. |

---

## 5. Onde os dois métodos se contradizem — e como alocar

| Dimensão | Van Aken | McKinsey | Alocação proposta na FORJA |
|---|---|---|---|
| Ponto de partida | Diagnóstico antes de solução; solução prematura é o erro típico | Hipótese primeiro; diagnóstico exaustivo é paralisia | **Ambos, em sequência**: hipótese explícita + QDT para *podar* cedo (McKinsey); diagnóstico validado para *sustentar* o que sobreviveu (van Aken). O QDT é barato e mata muito; o diagnóstico é caro e só se aplica ao que passou. |
| Exaustividade | Diagnóstico deve ser completo e integrado | "Don't boil the ocean"; podar impiedosamente | Exaustividade obrigatória na **admissibilidade e nos fatos materiais**; poda agressiva no **mérito acessório**. |
| Papel do número | Desconfia de critério composto ponderado; recomenda comparar *Gestalts* holísticos | 80/20, ordem de grandeza | Van Aken vence: **nada de score único ou probabilidade de vitória** — o doc 14 já decidiu assim e a decisão se confirma. |
| Parada | Saturação | "E daí?" + sanity check | Os dois, cumulativos: para quando satura **e** cada nó sobrevivente muda alguma decisão. |
| Cliente | Problema é escolha negociada com o principal | Desconfie do diagnóstico do cliente | Compatíveis: negociar a definição **depois** de validar independentemente. |

---

## 6. A proposta — F2A-v2: divergência forçada + árvore de questões decisórias

**Correção de rumo pedida pelo Igor (30/07):** a primeira versão desta seção pulava direto para a árvore convergente e perdia o que as 100 perguntas tentavam garantir — a exploração do problema por todos os lados. O Igor está certo, e os dois livros o sustentam: van Aken separa a **orientação divergente** do *problem mess* (cap. 4.3 — só depois de mapear o emaranhado se escolhe o problema focal) do **diagnóstico convergente**; McKinsey põe o brainstorming de "sala branca" *antes* da issue tree. O desenho definitivo tem, portanto, **duas fases com contratos distintos**: primeiro diverge com amplitude verificada, depois converge com poda lastreada. O defeito do formato atual nunca foi exigir amplitude — foi medi-la por contagem, e contagem se satisfaz com cópia.

### 6.0 Fase D — divergência com amplitude medida, não contada

Substitui a cota "100 perguntas, 10 por ótica" por exigências que **só a exploração real satisfaz e a cópia não**:

1. **Especificidade por pergunta.** Pergunta só conta se estiver ancorada em um elemento concreto e próprio do caso — ato, documento, data, pedido, valor, sujeito ou tensão nomeada. "Que evento criou a necessidade da peça atual?" não conta; "a vista publicada em 26/06 para responder a Petição 654252/2026 reabre a discussão sobre X?" conta. Checagem determinística: o campo `caseAnchor` deve ter **alta cardinalidade entre as perguntas** (o oposto do medido hoje: 1 valor em 100), e cada pergunta deve conter ao menos um identificador do inventário do caso.
2. **Geração congelada antes da resposta.** As perguntas são produzidas primeiro, gravadas e seladas por `contentHash`; só então se respondem. É a defesa estrutural contra o formulário: quem escreve pergunta e resposta no mesmo fôlego escreve as duas para se encaixarem. A separação obriga a pergunta a nascer da leitura dos autos, não da resposta que já se pretendia dar.
3. **Dissimilaridade entre perguntas.** Verificação determinística de sobreposição de tokens entre pares; pares acima do limiar são enchimento e não contam para a amplitude. Calibrar o limiar nos 7 casos degenerados, que são o corpus perfeito do antipadrão.
4. **As 10 óticas como pauta de varredura, com saturação por ótica.** Em cada ótica, gerar perguntas até declarar saturação — e a declaração exige dizer **qual foi a última pergunta gerada que nada acrescentou**. Ótica vazia é declarada vazia com motivo. Se o Igor quiser manter um piso numérico global (as 100) como garantia psicológica de esforço, ele pode ficar — a diferença é que **pergunta genérica, duplicada ou sem âncora não conta para o piso**, então o piso só é atingível explorando de verdade. O número deixa de ser o alvo e vira subproduto.
5. **Cota de perspectiva, não de volume.** Herdada do McKinsey e do red team já instalado: entre as perguntas válidas deve haver, obrigatoriamente, perguntas formuladas **do ponto de vista do adversário** e **do ponto de vista do julgador que quer negar** — não como ótica decorativa, mas com o teste do §6.3(3): o revisor pergunta "que pergunta o adversário faria que não está aqui?".

### 6.0-bis Fase C — convergência

Toda pergunta válida da Fase D tem exatamente três destinos, e nenhum é silencioso: (a) entra como nó ou evidência de um ramo da árvore MECE sob a pergunta jurisdicional; (b) é podada com motivo + lastro (e relida pelo red team de F7); (c) vira bloqueio com consequência e rota de diligência. Pergunta sem destino é P0 do validador. A partir daí valem os elementos 1–9 do §6.1: QDT, poda por "não" de admissibilidade, work plan de sete colunas, história diagnóstica, rival, parada por saturação.

O ganho sobre o desenho atual: hoje as 100 perguntas terminam em si mesmas (`downstreamTargets` genérico); no híbrido, cada pergunta ou muda uma decisão, ou morre com registro, ou bloqueia a peça. E o ganho sobre a minha v1: a amplitude que o Igor queria forçar continua forçada — agora por especificidade, dissimilaridade e saturação por ótica, que não se falsificam por cópia.

### 6.1 Os nove elementos obrigatórios da convergência

Substituir `FORJA-F2A-100-v1` por `FORJA-F2A-TREE-v2` com as duas fases acima. Elementos da Fase C:

1. **Pergunta jurisdicional única**, em uma frase — o que o órgão precisa decidir. Já é gate no catálogo; passa a ser a raiz da árvore.
2. **Classificação do problema**: real, percepção ou meta, com a **norma** invocada e a **evidência** do cotejo. Problema de percepção ou de meta **bloqueia a produção da peça naquele veículo** e devolve ao titular com a alternativa cabível.
3. **Hipótese inicial explícita** — a tese que provavelmente vence — declarada antes da pesquisa ampla.
4. **QDT por tese**: lista das premissas necessárias, cada uma com veredicto refutada / sustentada / a verificar em minutos. Tese com premissa refutada morre aqui e o registro do óbito permanece.
5. **Árvore MECE**, profundidade livre, folhas obrigatoriamente respondíveis por sim/não. Ramo com "não" em nó de admissibilidade é podado inteiro, com o motivo gravado.
6. **Work plan de sete colunas por folha material** — questão, análise, dado, fonte, produto, responsável, prazo. É o que F3 consome.
7. **História diagnóstica** em até dez linhas, contando causa, encadeamento e elo atacável. Se não puder ser escrita, F4 não abre.
8. **Explicação rival elaborada** — pelo menos uma leitura alternativa dos fatos ou do direito desenvolvida de verdade, com a evidência que discriminaria entre as duas.
9. **Registro de parada**: por que a exploração terminou — saturação declarada, com os últimos nós que nada acrescentaram.

### 6.2 Como fica o gate

`exploration_100_complete` sai. Entram:

- `problem_validated` — classificação real/percepção/meta com norma e evidência;
- `hypotheses_qdt_done` — toda tese viva passou pelo QDT;
- `tree_mece_verified` — dois testes MECE por nível; folhas em sim/não;
- `workplan_bound` — folha material sem análise, dado, fonte e responsável é P0;
- `diagnostic_story_present` — história escrita e coerente;
- `rival_explanation_present`;
- `stop_justified` — saturação declarada, não contagem.

O validador `forja_exploracao_100.py` é substituído por `forja_arvore_questoes.py`, invocado pelo mesmo ponto do pipeline. O contrato F2 troca o gate e mantém `question_tree` como nome de output, **mas com `protocolVersion` novo e rejeição ativa do antigo**: todo consumidor a jusante deve falhar alto ao encontrar `FORJA-F2A-100-v1` depois do corte, em vez de aceitar o schema velho em silêncio. Migração silenciosa de schema sob o mesmo nome de arquivo é exatamente o tipo de deriva que a fábrica já pagou para aprender a evitar.

### 6.3 Anti-degeneração: por que estes gates não viram a próxima cota

Autocrítica obrigatória: metade dos gates acima é de *presença* (`diagnostic_story_present`, `rival_explanation_present`, `stop_justified`), e gate de presença degenera pelo mesmo mecanismo da cota — o modelo escreve *uma* história boilerplate, *uma* rival de palha, *uma* frase de saturação, e passa. O plano que diagnostica Goodhart nas 100 perguntas não pode entregar gates Goodhart-vulneráveis sem defesa. Quatro defesas, todas exigidas do validador e do contrato:

1. **Veredicto sem lastro não é veredicto.** Cada QDT (`refutada`/`sustentada`), cada poda de ramo e cada classificação real/percepção/meta exige `supportIds` apontando para fonte verificável (autos, regimento, cache de fontes oficiais) — mesma disciplina do `forja_lastro.py`. "Refutada porque sim" é P0. Em especial, **ramo podado é o esconderijo natural de questão incômoda**: a poda grava motivo + fonte, e o red team de F7 relê os ramos podados — mesma lição da memória "objeção externa rejeitada deve ser relida a cada versão".
2. **As métricas que detectaram a degeneração viram canário permanente.** A medição que expôs o formulário (§1) — valores distintos de campos por artefato, razão de cópia entre respostas, distribuição de tamanho — entra em `forja_arvore_questoes.py` como checagem determinística: campos-chave com diversidade abaixo de piso calibrado nos 7 casos degenerados = P1 automático. O detector do problema passa a ser o guarda do sucessor.
3. **Revisor independente com pergunta certa.** O contrato F2 já tem `reviewerRole` (`forja-product-auditor`). A revisão da árvore não pergunta "está completa?" — pergunta **"que questão material do caso não está na árvore?"** e **"qual poda você reverteria?"**. Uma ausência apontada reabre a exploração. É o teste CE feito por adversário, não por autor.
4. **Qualidade de texto não é mensurável por regex — e o plano assume isso.** A história diagnóstica e a explicação rival só têm avaliação real no julgamento cego do ciclo AR e na revisão cruzada entre famílias. O validador determinístico checa estrutura, lastro e diversidade; coerência é papel do revisor. Prometer menos aqui é a lição do `anti-trapaca-evaluator`.

### 6.4 As 10 óticas não morrem — mudam de função

Erro da primeira versão deste plano: descartar as óticas junto com a cota. As 10 óticas canônicas (mandato, fatos, prova, processo, direito, adversário, riscos, alternativas, quantificação, comunicação) são um bom checklist de *cobertura* — o problema nunca foram elas, foi a cota de 10 respostas por ótica. Na v2 elas viram o **teste "coletivamente exaustivo" do MECE**: ao fechar a árvore, verificar ótica por ótica se existe questão material daquela lente que não está em nenhum ramo. Ótica sem questão material é declarada vazia *com uma frase de motivo* — não recebe 10 perguntas de enchimento. Isso preserva o investimento do F2A-100, facilita a migração mental e dá ao revisor do §6.3(3) uma pauta concreta.

### 6.5 Perfil por complexidade — seleção que não pode ser jogada

Van Aken §13 já previa três perfis e nunca foram usados porque nada os selecionava. Aqui o perfil é escolhido em F2 e determina o gate — mas **a seleção não pode ficar a critério do produtor**, porque o produtor sempre terá incentivo a escolher "leve" para reduzir trabalho. Critérios determinísticos, computáveis a partir do manifest e do inventário:

| Perfil | Critério objetivo (qualquer um dispara o nível) | Exigência |
|---|---|---|
| Leve | produto não protocolável, OU peça de questão única sem parte adversa ativa | itens 1–4 e 9; árvore rasa; sem explicação rival |
| Completo | peça protocolável em processo contencioso; recurso; peça responsiva | itens 1–9 |
| Intensivo | mais de um recurso/ato impugnável vivo no processo, OU cálculo material, OU acervo acima do piso de volume, OU produto destinado a tribunal superior | 1–9 + grafo de atos + triangulação com limite inferior + conselho ampliado |

Rebaixar o perfil calculado é permitido **somente com motivo registrado e autorização humana** — o mesmo desenho do `familyAssurance`: a degradação é permitida, o silêncio não.

---

## 7. Reforma do design (F4/F5)

Cinco mudanças, todas de van Aken, todas já descritas no doc 14 e nenhuma operacionalizada.

1. **Conceito de solução antes do texto.** Escolher e validar a arquitetura — veículo + tese principal + ordem decisória + mapa de prova — como artefato próprio, aprovado antes de redigir. Van Aken (cap. 6.3) é explícito: iterar a partir do *outline* custa uma fração de iterar a partir do detalhe. É o ataque mais direto ao retrabalho de 30-40% documentado.
2. **Alternativa obrigatória.** A pergunta literal do livro: *"se este design não puder ser usado, o que eu faria?"* Uma alternativa real por caso completo, com o gatilho que faria trocar.
3. **Requisitos com fronteira dura.** Condição de contorno (lei, prazo, competência, cognição, prova disponível, instrução do titular) é inegociável; restrição de design (extensão, profundidade subsidiária, quantidade de visual) é negociável. Proibido relaxar condição para a solução caber.
4. **Loop B com registro.** Quando as iterações não convergem, rebaixar requisito negociável **com motivo e autorização escritos** — em vez de travar ou entregar abaixo em silêncio.
5. **Especificação mínima com folga de apropriação.** O blueprint diz ao redator o necessário e não cada frase; a peça ancora poucos pontos decisórios com força e deixa o julgador percorrer o resto. Fundamento em §3.3.

Da parte McKinsey, apenas dois itens entram no design: o **teste do elevador como critério de aceitação da síntese executiva** e a **regra de três** para as razões de suporte.

---

## 8. Ressalvas honestas

- **As páginas do McKinsey Mind não foram conferidas na fonte.** Vêm do NotebookLM, que cita mas pode errar pincite — exatamente o modo de falha nº 4 da taxonomia de citação do upgrade U1. Antes de qualquer uso das páginas em documento que circule fora da fábrica, conferir no PDF. O **conteúdo** das técnicas é consistente entre as duas consultas e com o que o livro notoriamente sustenta; a **localização** é que está não verificada.
- **Van Aken foi lido verbatim** no OCR com hash conferido; as citações de capítulo e seção deste documento são seguras.
- **Os ganhos do §9 são estimativas [Inferência]**, ancoradas nos erros reais de `RETROSPECTIVAS.md` e do CLAUDE.md, não em medição prospectiva. O ciclo AR existe exatamente para isso e nenhuma dessas mudanças deveria ser declarada "melhoria" sem passar por ele.
- **Nenhuma dessas técnicas ataca o modo de falha dominante da fábrica**, que é alucinação de citação e premissa não declarada. Elas atacam o desperdício e a tese natimorta. O gate de lastro e a conferência de citação continuam sendo a defesa principal e não são substituídos por nada aqui.
- **Risco de a reforma repetir o destino do PSO-Pet:** é real, e a única mitigação é o §2 — contrato, validador e gate, ou nada.
- **Risco de a reforma repetir o destino do F2A-100:** também real, e mais insidioso — os gates novos podem degenerar em boilerplate como a cota degenerou em preenchimento. As defesas estão no §6.3 (lastro por veredicto, canários de diversidade, revisor adversarial, honestidade sobre o que regex não mede); sem elas, a v2 seria só uma cota com outro formato.
- **A Etapa 2 tem bloqueador de governança:** a ordem inviolável de 14/07 só pode ser superada por determinação expressa do Igor (ver §10). Este documento propõe; não revoga.

---

## 9. Seleção final — o que aplicar, onde e o ganho esperado

Ordenado por retorno sobre esforço.

| # | Técnica | Fonte | Onde | O que substitui | Ganho esperado | Custo |
|---|---|---|---|---|---|---|
| 1 | QDT jurídico por tese | McKinsey c.1 | F2A | nada — é novo | mata tese inviável antes da redação; ataca a raiz do retrabalho | baixo |
| 2 | Problema real × percepção × meta | van Aken 5.3 | F2A | aceitação tácita do comando | impede EDcl para inconformismo e pedido fora da cognição | baixo |
| 3 | Árvore com poda em vez de cota | McKinsey c.1 + van Aken 4.3 | F2A | as 100 perguntas | fim do preenchimento; esforço concentrado no decisivo | médio |
| 4 | Work plan de 7 colunas | McKinsey c.2 | F2A→F3 | `downstreamTargets` genérico | pesquisa deixa de ser difusa; cada questão tem dono e fonte | baixo |
| 5 | Parada por saturação + "E daí?" | van Aken 5.3 + McKinsey c.2 | F2A | `exploration_100_complete` | remove o incentivo que produziu a degeneração | baixo |
| 6 | História diagnóstica como gate | van Aken 5.6 | F2A→F4 | menção não verificável no doc 14 | detecta diagnóstico imaturo antes do blueprint | baixo |
| 7 | Conceito de solução antes do texto | van Aken 6.3 | F4 | blueprint que já desce ao texto | iteração barata em vez de cara | médio |
| 8 | Alternativa obrigatória | van Aken 6.4/12.4 | F4 | matriz preenchida *post hoc* | evita primeira ideia por ser a primeira | baixo |
| 9 | Triangulação com limite inferior | van Aken Box 5.2 | F3/F6 | número mais favorável | ataca excesso na redação e premissa não declarada | baixo |
| 10 | Explicação rival elaborada | van Aken 5.4 | F2A/F4 | red team só no fim | objeção entra cedo, quando ainda é barata | médio |
| 11 | Condição de contorno × restrição | van Aken 6.3 | F4 | requisitos indiferenciados | impede relaxar o inegociável | baixo |
| 12 | Loop B com registro | van Aken 12.4 | F4/F7 | travar em silêncio | degradação explícita, como no `familyAssurance` | baixo |
| 13 | Elevator test na síntese executiva | McKinsey c.4 | F6/F7 | síntese sem critério | dá teste de aceitação a exigência que já existe | baixo |
| 14 | Especificação mínima com folga | van Aken 12.5/12.6 | F4/F6 | sobre-estruturação | fundamenta a poda de visual supérfluo | baixo |
| 15 | Causas acionáveis / condições | van Aken 5.1 | F2A/F4 | tratar tudo como atacável | não gasta argumento no que a peça não move | baixo |

**Rejeitados com motivo** (§4.2): precisão direcional em asserção, omissão seletiva de detalhe, técnicas adversariais de entrevista, priorização por facilidade, score composto de vitória.

---

## 10. Sequência de implementação

Três etapas. Nenhuma delas começa sem decisão do Igor.

**Etapa 1 — o barato que não depende de schema.** Itens 1, 2, 6 e 9: QDT, classificação do problema, história diagnóstica e limite inferior. Entram como seções obrigatórias do artefato F2 atual e como checagens no validador existente. Não quebra nada a jusante. É onde está a maior parte do ganho.

**Etapa 2 — a troca de formato.** Itens 3, 4, 5: novo schema `FORJA-F2A-TREE-v2`, `forja_arvore_questoes.py`, troca dos gates no contrato F2, canários de diversidade (§6.3), migração dos consumidores de `question_tree` com rejeição ativa do schema antigo, e teste de regressão.

**Pré-condição de governança da Etapa 2 — sem ela nada anda:** o F2A-100 é **ordem inviolável do Igor de 14/07/2026**, gravada no CLAUDE.md do projeto ("deve usar `FORJA-F2A-100-v1`, conter exatamente 100 perguntas, 10 em cada ótica"). Nenhuma sessão pode revogá-la por conta própria — a substituição exige nova determinação expressa do Igor superando a anterior, nos moldes do precedente editorial de 25/07 que superou a ordem de 15/07 ("ambas registradas como invioláveis; prevalece a mais recente"). O pacote da Etapa 2 inclui, portanto, a atualização do CLAUDE.md e do AGENTS.md espelho com a nova determinação datada. Até essa determinação, o F2A-100 permanece obrigatório e a Etapa 1 roda *dentro* dele.

**Etapa 3 — o design.** Itens 7, 8, 10-15 em F4/F5, mais a reconciliação com o PSO-Pet: `forja_pso_pet.py` ou é integrado ao pipeline ou é removido do repositório. Manter código órfão com teste que ninguém chama é dívida que engana a próxima sessão.

Antes de declarar qualquer uma "melhoria", passar pelo ciclo AR — execução pareada, julgamento cego, canário. É a regra da própria fábrica.

---

## 11. Uma observação sobre a pergunta do Igor

O pedido foi "formas mais elegantes e sofisticadas e que seriam mais eficientes para explorar o problema". A resposta dos dois livros é a mesma e é o oposto de sofisticação: **explorar menos, mas com estrutura e com direito de matar cedo.** As 100 perguntas são o método mais elaborado e menos eficiente possível — cobram cem respostas e não obrigam nenhuma a mudar uma decisão. A árvore com poda cobra menos e decide mais.

O que o doutorado ensinou continua valendo integralmente; o que faltou nunca foi o método, foi o elo bloqueante que faz o método rodar.

---

## 12. Registro da segunda passada (revisão crítica na mesma sessão)

A pedido do Igor, o plano foi reanalisado adversarialmente após a primeira entrega. Quatro defeitos materiais encontrados e corrigidos — todos do mesmo tipo que o próprio plano censura nos outros:

1. **Gates Goodhart-vulneráveis.** A v1 propunha gates de *presença* (`diagnostic_story_present` etc.) sem defesa contra boilerplate — o mesmo mecanismo que degenerou a cota de 100. Corrigido no §6.3: lastro obrigatório por veredicto e por poda, canários de diversidade calibrados nos casos degenerados, revisor adversarial com pergunta invertida, e reconhecimento explícito do que validador determinístico não mede.
2. **Bloqueador de governança omitido.** A v1 propunha substituir o F2A-100 sem registrar que ele é ordem inviolável de 14/07 e que só determinação expressa do Igor a supera. Corrigido no §10 (pré-condição da Etapa 2) e §8.
3. **As 10 óticas descartadas por atacado.** A v1 jogou fora as óticas junto com a cota; elas são um bom teste de exaustividade coletiva. Corrigido no §6.4: mudam de função (de cota para checklist CE), não morrem.
4. **Seleção de perfil jogável e migração de schema silenciosa.** A v1 deixava o perfil a critério de quem produz (incentivo a escolher "leve") e mantinha o nome `question_tree` sem rejeição ativa do schema antigo. Corrigidos no §6.5 (critérios determinísticos + rebaixamento só com motivo e autorização) e §6.2 (fail-loud no `protocolVersion`).

**Terceira passada (mesma data, direção do Igor):** a v2 pura pulava a fase divergente e perdia o propósito legítimo das 100 perguntas — forçar a exploração do problema por todos os lados, que van Aken (orientação no *problem mess*, cap. 4.3) e McKinsey (brainstorming antes da issue tree) ambos prescrevem. Corrigido no §6.0: desenho híbrido em duas fases — divergência com amplitude **medida** (especificidade por âncora, geração congelada antes das respostas, dissimilaridade entre pares, saturação declarada por ótica, cota de perspectiva adversarial) e convergência com poda lastreada, onde cada pergunta válida tem destino obrigatório: ramo, poda registrada ou bloqueio. Piso numérico pode ser mantido como garantia de esforço, mas pergunta genérica, duplicada ou sem âncora não conta para ele — o número vira subproduto da exploração, não alvo.

Um alerta de método que fica para a etapa seguinte: **a segunda passada foi feita pela mesma sessão que escreveu a primeira** — vale como autocrítica, não como revisão cruzada. Antes de implementar, este documento deve passar pela revisão de outra família de modelo, conforme o gate `cross_model_review_verified` da própria fábrica.

---

## 13. Confronto com o estudo paralelo do GPT-5.6 Sol e consolidação

O Igor encomendou o mesmo estudo, em paralelo, ao GPT-5.6 Sol (`39_VAN_AKEN_MCKINSEY_DIAGNOSTICO_E_DESIGN_FORJA.md`, 30/07 13:25). Os dois documentos foram produzidos sem contato — o confronto abaixo funciona como a revisão cruzada entre famílias que o §12 pedia, e a implementação deve partir da síntese, não de qualquer um dos dois isolado.

### 13.1 Convergência independente (adotar sem discussão)

As duas famílias chegaram sozinhas ao mesmo núcleo: problema como lacuna validada; pergunta decisiva governante; issue tree + hipótese inicial + rival + QDT com salvaguarda jurídica; work plan hipótese→teste→fonte; *diagnostic story* como gate F3→F4; requisitos congelados antes do design; alternativas comparadas e outline aprovado antes do detalhamento; parada por regra, não por contagem; 80/20 restrito à priorização de esforço; MECE defensável, não absoluto; prewire apenas interno. Mesma lista de rejeições. Convergência independente entre famílias é o sinal de robustez mais forte disponível antes de medição prospectiva.

### 13.2 O que o estudo do Sol tem de superior — incorporado a este plano

1. **Sementes como auditoria de omissão.** As 100 sementes viram banco canônico que roda ao final da convergência como detector de ramo omitido; omissão material reabre a árvore. Superior à minha redução das óticas a checklist CE: reusa as perguntas concretas, não só as lentes. Entra como camada 3 do desenho consolidado (§13.4).
2. **`diagnosticTree` tipado** — nós `symptom` / `candidate_cause` / `validated_cause` / `rival_explanation` / `mechanism` / `constraint`, relações com `relationType`, `supportIds`, `confidence`, `testId`, `status`. Leva a contrato o que este documento só descrevia em prosa.
3. **CIMO como justificativa de design** (`designRationaleCIMO`) em F4, além do CIMO de aprendizado em F10 — com a regra dele que merece virar gate: *solução sem mecanismo explícito não é design justificado; é preferência*.
4. **Auditoria dos schemas vivos** (§7 dele): `reasoning_graph` de F3 sem relações causais tipadas; artefatos F4 abertos demais. Complementa o que meu §7 não desceu a verificar.
5. **Fórmula de priorização de perguntas humanas** (materialidade × incerteza × poder de mudar a rota × irreversibilidade) para F2-B, e a tabela dele de indicadores mensuráveis por ganho (§10 dele) — adotar como base da medição do ciclo AR.
6. **Separação `presentedProblem` × `reframedProblem`** com justificativa lastreada do reenquadramento.

### 13.3 Onde o estudo do Sol falha — e este plano corrige

1. **Descreve a especificação, não audita a produção.** O §2.1 dele credita à F2A-100 virtudes ("impede lacunas silenciosas", "vincula respostas a supportIds") que os artefatos reais desmentem — a medição do §1 deste documento mostra a degeneração (100/100 `answered`, 1 valor distinto em campos-chave, 34/100 com lastro). A postura dele de "evolução aditiva preservando o que existe" preservaria também o comportamento degenerado.
2. **Recomenda o mecanismo que já matou o van Aken uma vez.** O §11 dele — "executar em sombra, sem substituir v1, três casos" — é o plano do doc 14 §16, que produziu zero execuções em 51 casos. Sombra sem elo bloqueante, agenda e dono não roda: isso é fato demonstrado nesta fábrica, não hipótese. O piloto correto é pareado e agendado via ciclo AR, com dono e prazo, ou não haverá piloto.
3. **Gates Goodhart-vulneráveis.** `diagnostic_story_accepted` e afins têm critérios sem mecanismo de imposição — degeneram como a cota degenerou. Falta tudo do §6.3 deste plano: lastro por veredicto e por poda, geração congelada antes das respostas, canários de diversidade, revisor adversarial com pergunta invertida.
4. **Ignora o bloqueador de governança** (ordem inviolável de 14/07, §10 deste plano) e mantém regime duplo v1/v2 sem fail-loud — o produtor poderia escolher v1 para sempre.
5. **A "exploração adaptativa" dele reduz a divergência forçada** (instancia perguntas só para ramos relevantes), na contramão da diretriz expressa do Igor de 30/07. O desenho dele é anterior à clarificação.
6. **Proveniência mais fraca:** o §13 dele admite páginas reconstruídas por notebook para os dois livros; aqui, o van Aken foi lido verbatim com hash conferido (a fraqueza compartilhada é só o McKinsey).

### 13.4 Desenho consolidado — três camadas

1. **Camada D — divergência forçada** (este plano, §6.0): varredura das 10 óticas com especificidade por âncora, geração congelada por hash antes das respostas, dissimilaridade entre pares, saturação declarada por ótica, cota de perspectiva adversarial. Piso numérico opcional em que só conta pergunta válida.
2. **Camada C — convergência estruturada** (síntese dos dois): `problemFrame` com lacuna e tipo (real/percepção/meta), `decisiveQuestion`, `hypothesisLedger` com QDT, `issueTree` + `diagnosticTree` tipado do Sol, `diagnosticWorkplan` de sete colunas, `diagnosticStory` como gate com as defesas anti-boilerplate do §6.3, destino obrigatório por pergunta (ramo / poda lastreada / bloqueio).
3. **Camada A — auditoria de omissão** (Sol): as 100 sementes rodam contra a árvore fechada; omissão material reabre a exploração; o resultado da varredura fica registrado no artefato.

Para F4, adotar do Sol `designRequirements`, `solutionConcepts` com alternativas, `designRationaleCIMO` e `outlineDesign` com gate `outline_approved_before_detailing` — somados ao Loop B com registro e à condição de contorno × restrição deste plano.

### 13.5 Efeito sobre a sequência do §10

A Etapa 1 ganha os campos `problemFrame`, `hypothesisLedger` (com QDT) e `diagnosticStory` no formato do Sol. A Etapa 2 incorpora o `diagnosticTree` tipado e a camada de auditoria de sementes, mantendo as pré-condições de governança e o fail-loud já registrados. A Etapa 3 absorve o §7.4 dele (artefatos e gates de F4). O piloto do §11 dele é substituído pelo ciclo AR pareado com agenda e dono. Este §13 constitui a revisão cruzada exigida pelo §12; a decisão de promover continua sendo do Igor.
