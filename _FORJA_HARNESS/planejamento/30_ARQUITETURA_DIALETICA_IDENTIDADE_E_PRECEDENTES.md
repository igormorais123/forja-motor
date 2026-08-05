# 26 — Arquitetura de três eixos: dialética com o advogado, identidade Medina Osório e sistema de precedentes

**Estado:** pesquisa, diagnóstico e planejamento. **Nenhuma linha de código foi alterada.**
**Fonte de requisitos:** `planejamento/25_REQUISITOS_ENTREVISTA_FABIO_MEDINA_OSORIO.md` (entrevista de 25/07/2026).
**Insumos críticos incorporados:** três documentos de IA externa (`forja_medina_osorio_arquitetura.md`, `gates_e_validadores.md`, `identidade_medina_osorio.md`) e o parecer do Codex de 25/07/2026.
**Sistemas inspecionados:** `_FORJA_HARNESS` (contratos F0–F10 e módulos de produção) e `Sistema de Busca Jurídica\teiajus` (README, matriz de capacidades, documentação de operação do STJ, conectores).

---

## 0. Resolução de uma divergência entre os pareceres

O Codex registrou, com correção metodológica, que a transcrição que recebeu estava truncada: continha 00:00–03:34, saltava "[321 lines hidden]" e retornava em 45:19–47:58. Por isso marcou como `[Não verificado]` tudo que os documentos de IA citavam do trecho central.

**A transcrição integral foi recebida nesta análise.** Os trechos centrais estão conferidos e reproduzidos em `planejamento/25`, §1.4 a §1.6. A ressalva do Codex fica levantada quanto ao conteúdo; permanece válida quanto à prosódia, que nenhuma transcrição entrega.

A consequência não é acadêmica. O terço que faltou ao Codex é justamente onde estão os requisitos mais pesados e mais ausentes do harness:

- o algoritmo de busca por topologia decisória (relator prevento → turma → seção → Corte Especial → prequestionamento);
- os dois marcadores "principalmente", ambos apontando para **uso adequado e aderência do precedente**;
- ratio decidendi nomeada expressamente;
- as duas aplicações de jurimetria;
- as três premissas de estilo, o modelo do julgador atordoado na fila e a imagem da taça de vinho;
- os conceitos operativos de **desmoralização** e **constrangimento**.

Os seis traços de pensamento que o Codex extraiu dos 3,5 minutos iniciais estão corretos e foram incorporados. Eles são, porém, o começo da fala — e o titular gasta o meio da entrevista dando especificação técnica, não filosofia.

### 0.1 Correções do Codex que este documento adota — e que corrigem o documento 25

Quatro são materiais e uma delas é um erro jurídico que eu havia reproduzido do documento de identidade externo:

**(a) Precedente vinculante não se "rebaixa" por baixa aderência fática.** Estava errado em `25`, §2.2, G9. Vinculação é regime jurídico, não nota de similaridade. Diante de precedente vinculante com moldura fática diversa, as operações corretas são: **delimitar o alcance** da ratio, **distinguir** (art. 489, §1º, VI, e art. 927, §1º, do CPC) ou sustentar **superação** (art. 927, §§2º a 4º). O que a aderência governa é a *operação*, não a *força*. Corrigido no documento 25 e refeito no §3 abaixo.

**(b) Hierarquia de fontes com texto normativo em último lugar confunde ordem de exposição com autoridade.** A lei não é a fonte mais fraca. O documento de identidade externo listou uma ordem de *exposição na peça* e a rotulou como hierarquia de autoridade. Não adotar.

**(c) Nota numérica de aderência é pseudoprecisão.** Um precedente não tem "aderência 7,3". Substituída por matriz qualitativa estruturada com decisão humana nominal (§3.3).

**(d) "Mínimo de teses por classe" incentiva produção artificial de teses.** É Goodhart puro, e o titular pediu plausibilidade forte, não volume. Substituído por **cobertura de famílias de tese examinadas**, com não aplicabilidade justificada (§1.5).

Adoto também, sem reserva: a granularidade de lacunas em quatro níveis; o alerta de que segundo agente não é automaticamente revisor independente; a exigência de política de retenção e minimização no dossiê; a proibição de ativar em produção a matriz doutrinária inferida de trajetória pública; e a reformulação do teste cego (§2.6).

---

# PARTE I — A dialética: o sistema como parceiro intelectual antes de escrever

## 1.1 O que precisa ficar claro antes de projetar

O modelo que o titular descreve **não é** "o advogado manda o caso e a IA entrega pronto". Também **não é** um chatbot que conversa. É um terceiro modelo, e ele o nomeou em vocabulário processual: **"uma espécie de pedido de esclarecimentos ao remetente da demanda"**.

Isso importa para o desenho. Um pedido de esclarecimentos é um **ato**: tem endereçado, objeto, motivação e produz dever de resposta. Não tem histórico de conversa, não tem turnos, não tem "digite sua dúvida". A interação é assíncrona, documental e motivada — que é exatamente como um escritório funciona e exatamente o que sobrevive a e-mail.

E há uma restrição econômica que ele mesmo impôs, quatro vezes: **perguntar tem que acelerar, não atrasar.** Qualquer desenho em que o pipeline fica parado esperando resposta viola o requisito. O que ele descreveu foi o oposto — emitir o checklist cedo e seguir trabalhando: *"independentemente de ter capacidade de prosseguir no aprofundamento do estudo da matéria... mas ela já lança um checklist documental preliminar"*.

## 1.2 O instrumento: CONSULTA AO ADVOGADO RESPONSÁVEL

Documento único, enviado por e-mail, com cinco blocos. Não é formulário; é peça endereçada.

**Bloco 1 — Compreensão declarada.**
"Isto é o que entendi que se pede. Isto é o que li. Isto é o que ainda não li, e por quê."

Não é cortesia. É o que o titular chamou de **"mostrar que compreendeu o escopo do seu trabalho"**, e é o mecanismo mais barato de detecção de erro que existe: se entendemos errado, ele descobre em trinta segundos de leitura, e não depois de uma petição inteira. Dois parágrafos no máximo, mais a lista do acervo com o que está ilegível, truncado, sem assinatura ou com páginas faltando.

**Bloco 2 — Perguntas decisórias.**
Lote único, ordenado por impacto no escopo. Cada pergunta carrega quatro campos, e o quarto é o que resolve o problema da velocidade:

| Campo | Função |
|---|---|
| A pergunta | direta, respondível em uma linha |
| Por que preciso saber | vincula à tese, ao fato ou ao ato que depende dela |
| O que muda em cada resposta possível | mostra que a pergunta é decisória, não burocrática |
| **O que farei se não houver resposta** | **premissa declarada sob a qual sigo trabalhando** |

O quarto campo é o coração do desenho. **Nenhuma pergunta paralisa.** Cada uma vem com uma premissa de trabalho declarada; o silêncio não trava nada, apenas faz a premissa entrar na peça como premissa visível e rastreável. Isso honra literalmente o argumento de velocidade dele e, ao mesmo tempo, a regra da fábrica de que premissa sem prova vira `[VERIFICAR]` com bloqueador nominado.

**Bloco 3 — Diligências documentais motivadas.**
Cada item com: documento pretendido, a tese ou o fato que depende dele, a fundamentação, e a consequência concreta da ausência. *"Não basta ir simplesmente"* — lista sem motivação é rejeitada pelo validador, não pelo revisor.

**Bloco 4 — Leque de teses, para provocação.**
Este é o bloco que o titular descreveu com mais entusiasmo e que nenhum concorrente faz. Apresentar:
- as teses que vejo, com a natureza de cada uma (processual, prejudicial, mérito, subsidiária, constitucional a prequestionar);
- **as teses que descartei e por quê** — e este é o item que faz um sócio sênior parar e ler, porque revela julgamento e não catálogo;
- a pergunta final: *"o que o senhor vê aqui que não está nesta lista?"*

O propósito real, dito por ele: *"a IA pode suscitar no interlocutor outras teses que o interlocutor tenha... e aí ele reflita"*. É elicitação de conhecimento tácito. O ativo mais valioso do escritório está na cabeça dos sócios e só sai quando provocado por uma lista concreta e errável.

**Bloco 5 — Decisões que são dele.**
Bifurcações em que a resposta é de negócio, de cliente ou de estratégia, e não técnica: apetite de risco, relação com a parte contrária, disposição para acordo, tratamento de fato superveniente, se haverá pedido de sustentação oral. O sistema não escolhe, e diz que não escolhe.

## 1.3 A regra que protege a confiança

Uma pergunta só entra na consulta se passar nos quatro filtros. O terceiro e o quarto decidem se ele responde ou para de ler.

1. **É material** — essencial ao produto, ou essencial a uma afirmação decisiva. Os níveis "útil" e "irrelevante" não perguntam: viram nota interna.
2. **Está bloqueada** — não há resposta no acervo nem em fonte oficial.
3. **Não é respondível pelo acervo já inventariado.** Perguntar o que está nos autos destrói a confiança mais rápido do que qualquer erro técnico. Validador obrigatório: toda pergunta é submetida a busca no índice documental antes de ser emitida; havendo correspondência, a pergunta é rejeitada.
4. **Não é respondível por pesquisa.** Se o TeiaJus, o regimento ou a fonte oficial resolvem, **o trabalho é nosso, não dele.** Terceirizar ao advogado o que o sistema deveria encontrar é a forma mais rápida de provar que o sistema não serve.

Aplicados sobre as 100 perguntas do F2-A, esses filtros devem produzir tipicamente **entre 5 e 12 perguntas**. Se produzirem 40, o problema está na leitura do caso e não no lote — e isso vira sinal de qualidade próprio.

## 1.4 Por que isto é barato: o motor já existe

O F2-A já produz, por caso, cem perguntas adaptadas, com classificação epistemológica, `blocked` motivado, consequência declarada e rota de diligência. **Não é preciso construir um motor de perguntas.** O que falta é uma projeção do F2-A sobre o humano:

- um **seletor** que aplique os quatro filtros e ordene por impacto;
- um **renderizador** que produza a consulta em prosa endereçada, no padrão do escritório, sem marcadores internos de auditoria (o protocolo de 11/07 já proíbe vazar `[FONTE: arquivo]` e proveniência operacional);
- um **rastreador** que receba a resposta, vincule cada resposta ao nó correspondente da árvore, mude o status de `blocked` para `answered` com proveniência `office_declaration` e conte a rodada.

Ponto de epistemologia que já é regra nossa e precisa ser mantido: **a resposta dele é declaração do escritório, não fato dos autos.** Vale como premissa de trabalho e como autorização; não vira prova. Isso já está no F2-A e é o que impede que uma troca por e-mail contamine a matriz factual.

## 1.5 Teses: cobertura, não contagem

O titular pediu quantidade superior de teses e, na frase seguinte, plausibilidade forte e conectividade lógica. Um mínimo numérico transforma o primeiro pedido em produção de lixo argumentativo e viola o segundo.

Desenho correto: **cobertura declarada de famílias de tese**, não contagem de teses. Para cada família — competência, admissibilidade, prejudiciais, prescrição e decadência, nulidades, mérito principal, mérito subsidiário, matéria constitucional a prequestionar, consequência institucional — o sistema declara: **examinei e proponho / examinei e descartei, com motivo / não se aplica, com motivo**. Nada desaparece em silêncio, e nada é inventado para bater meta.

## 1.6 Onde isto mora no harness

Subfase **F2-B**, entre a exploração das 100 perguntas e a fixação de escopo. Não é fase nova: é o padrão já usado duas vezes com sucesso (F2-A da exploração, F7-B do Fable 5). Consome `F2_QUESTION_TREE.json` e o `document_index` do F1; produz o documento que sai por e-mail e o ledger que fica auditável. Alimenta a subfase F2-C, que fixa escopo, metodologia e objetivo com aceite nominal.

Regra de bloqueio, com a granularidade que o Codex propôs e que corrige o desenho anterior: **a ausência de resposta não bloqueia a recepção, o inventário, a triagem, a pesquisa nem a cognição.** Bloqueia apenas a afirmação específica que dependia dela, e bloqueia o produto protocolável quando a lacuna é essencial ao produto. É o comportamento que o `draftRelease: blocked` já implementa.

---

# PARTE II — Identidade Medina Osório: método antes de vocabulário

## 2.1 O diagnóstico honesto do corpus

Verificado hoje: **`_MODELOS` está vazio** — contém apenas `LEIA-ME.md` e `MAPA_IA.md`. Todos os `.docx` do acervo da fábrica são produção nossa, não peças assinadas por ele. A calibração de identidade que os documentos externos propõem, a partir de vinte a trinta peças dele, **não pode começar hoje**.

Mas o inventário não é zero. Existem três corpora que ninguém contabilizou, e o segundo é o mais valioso de todos:

**Corpus A — texto autoral direto (temos, pouco).**
Os quesitos redigidos por ele no caso Cabreúva; os e-mails de demanda arquivados em `gestao_escritorio\entregas_fabio_osorio\` (dezenas de threads); esta entrevista. Registro: formulação de encomenda e escrita técnica, não peça.

**Corpus B — as revisões dele sobre a nossa produção (temos, e é o de maior sinal).**
`APRENDIZADOS_FEEDBACK_HUMANO.md` (27 KB) e o diff entre a versão protocolada e a nossa, que o `forja_diff_docx.py` já produz. **Cada alteração que ele fez é uma regra dele, observada em ato.** É um corpus que cresce a cada entrega, que ninguém precisa pedir, e que responde à pergunta certa: não "como ele escreveria", mas "o que ele aceita assinar". O Codex nomeou isto como "padrão recorrente nas revisões" e está correto em dar-lhe peso.

**Corpus C — obra pública (não temos localmente).**
Ele é autor consolidado em Direito Administrativo Sancionador. Ressalva importante: **registro acadêmico não é registro de petição.** O Corpus C serve à camada doutrinária e ao vocabulário técnico; não serve à arquitetura da peça, e usá-lo para isso produziria exatamente o texto erudito e volumoso que ele condenou.

**Ausente:** peças assinadas. É o único item que depende de pedido a ele.

## 2.2 Três níveis de confiança, e só dois são ativáveis

Adotado do Codex, com a granularidade que o caso exige:

| Nível | O que é | Uso |
|---|---|---|
| **N1 — confirmado** | regra enunciada por ele em fonte direta: entrevista, e-mail, determinação registrada | ativável em produção, como gate |
| **N2 — recorrente** | padrão observado no Corpus B, com pelo menos três ocorrências independentes | ativável com marcação e revisão humana |
| **N3 — hipótese** | inferido de trajetória pública ou de estilo presumido | **não ativável**; fica registrado como pergunta a fazer |

A matriz doutrinária que o documento de identidade externo atribuiu a ele — princípios operantes em ordem de invocação, ângulo característico — é **N3 inteira**. Não entra em produção. Entra na pauta da reunião como pergunta.

## 2.3 O que já é N1 hoje, sem pedir nada a ele

Da entrevista e das determinações registradas do escritório, já são regra confirmada:

1. Síntese executiva no início de toda peça, em qualquer tribunal (determinação de 07/07/2026, no estilo do art. 343-A do RISTJ).
2. Correção do idioma como premissa primeira, sem tolerância.
3. Poder de síntese: objetividade, ausência de redundância e de repetição, ir direto ao ponto.
4. Acessibilidade: direto, objetivo, sem rebuscamento, sem erudição decorativa.
5. Concretude: **mostrar a realidade a quem decide**, não qualificar conduta alheia.
6. Não abrir mão de precedente, doutrina e texto normativo.
7. Nunca desqualificar o advogado adversário; atacar a tese.
8. Prequestionamento expresso, com dispositivos legais e constitucionais carimbados.
9. Terminologia blindada contra as Súmulas 7 do STJ e 279 do STF.
10. Teste final de cada elemento: **reduz ou aumenta o esforço de quem decide?** Aumentou, sai. Já é regra escrita de visual law da fábrica, e é literalmente o critério dele.

Os pejorativos dele, extraídos da própria fala, entram diretamente na lista de proibições: **rebuscado, erudito, volumoso, aleatoriamente, desenfreado, inauditável.**

## 2.4 A identidade que importa é o motor argumentativo

O documento de identidade externo acertou ao dizer que a identidade dele é arquitetural, não lexical. Mas localizou o motor no lugar errado — pôs "consequência institucional" como oitava seção da peça. Não é seção. É o que organiza a peça inteira.

**O movimento Medina Osório, em três tempos**, observado três vezes na entrevista em contextos distintos:

1. **Estabelecer o que a autoridade já decidiu** — no próprio caso, no próprio órgão, ou em casos análogos.
2. **Mostrar que decidir diferente agora rompe isonomia e coerência** — não que a decisão é errada, mas que é *incoerente com ela mesma*.
3. **Nomear a consequência para quem decide** — desmoralização por falta de coerência e, no limite, responsabilização.

As três instâncias, na fala dele: precedente (*"uma autoridade, se ela não segue um precedente, ela de alguma forma se desmoraliza por falta de coerência... haverá uma quebra de isonomia"*); jurimetria (*"veja o constrangimento que sugere"*); acordo e deságio (*"o gestor público pode ser responsabilizado perante o Tribunal de Contas da União"*).

**Consequência para a dimensão persuasiva**, que é o que foi pedido:

| Recurso | Como ele usa | Como a FORJA deve usar |
|---|---|---|
| Ethos | credibilidade por lastro; nunca afirma além do que prova; liga auditabilidade a autoridade moral | a peça constrói autoridade **mostrando a fonte**, não adjetivando a própria tese |
| Pathos | mínimo, e sempre institucional: dignidade, acesso à justiça, isonomia | nunca indignação pessoal contra o adversário; nunca dramatização do fato |
| Logos | precedente ancorado, com a armadilha da coerência | o argumento decisivo é a incoerência do próprio órgão, não o erro em abstrato |

A formulação proibida é *"a decisão é absurda"*. A formulação dele é *"a decisão contraria o que este mesmo órgão decidiu em X, e mantê-la rompe a isonomia entre jurisdicionados em situação idêntica"*.

**O segundo movimento característico é o transporte dogmático**: identificar a garantia já consolidada em outro campo e exigir sua aplicação aqui. Ele fez isso na própria entrevista, ao impor à IA o dever de motivação do ato de autoridade pública. É a assinatura intelectual dele e é replicável como técnica de redação.

## 2.5 O que extrair, em que ordem, e o que não extrair

Ordem por retorno, do maior para o menor — inversa à que os sistemas costumam tentar:

**Nível 1 — arquitetura da peça** (Corpus B; começa hoje). Do diff protocolada × nossa: o que ele **cortou**, que revela o que considera peso morto; o que ele **moveu**, que revela a ordem que ele quer; o que ele **acrescentou**, que revela o que julgamos dispensável e ele não. Ordem das seções, posição do pedido, posição da síntese, tratamento dos fatos, densidade de citação por seção.

**Nível 2 — movimento argumentativo** (Corpus A e B). Onde entra a coerência do órgão; como antecipa a tese adversa; como formula pedido subsidiário.

**Nível 3 — fontes** (Corpus B e C). Precedentes e autores recorrentes, por matéria. Alimenta a preferência doutrinária que ele ofereceu responder.

**Nível 4 — lexical** (por último, e com cautela). Conectores, verbos de sustentação, comprimento de frase e de parágrafo, modo de transcrever precedente, termos que ele nunca usa.

**O que não extrair, sob nenhuma hipótese:** os padrões *orais*. Tríades enumerativas, hesitação, reformulação com "quer dizer", hedge constante ("eu acho que", "ao nosso ver"), encenação em fala direta, autodepreciação. São traços de fala inteligente e viram texto ruim. O Codex é explícito e está certo: traduzir a arquitetura mental, jamais o ritmo da voz.

## 2.6 Validação: o alvo correto

O documento externo propôs teste cego para verificar se a peça calibrada passa por autoria dele. **Alvo errado, e o Codex acertou ao corrigir.**

O alvo correto é **aderência ao padrão que o escritório aceita assinar**. Ele assina a peça: ela precisa ser aceitável para ele, não indistinguível dele. Perseguir indistinguibilidade é tecnicamente um alvo falso — não há corpus para tanto — e eticamente ruim, porque transforma o produto em imitação de pessoa em vez de instrumento de escritório.

Protocolo: três peças curtas sobre casos encerrados, submetidas a dois revisores do escritório que não participaram do projeto, com a pergunta **"o senhor assinaria isto? o que mudaria?"**. O que eles mudarem alimenta o Corpus B. É o mesmo ciclo de co-evolução que ele descreveu — *"cresceríamos juntos"* — e que a FORJA já opera pelo `APRENDIZADOS_FEEDBACK_HUMANO.md` e pelo ciclo AR.

---

# PARTE III — O sistema de precedentes: onde a FORJA está mais aquém

É a parte em que o titular concentrou os dois marcadores de prioridade — *"mas principalmente o uso adequado dos precedentes e a seleção correta"* e *"principalmente a identificação da aderência de cada precedente ao caso concreto"* — e é onde a varredura confirmou ausência total: `aderência`, `ratio`, `prevento` e `jurimetria` não aparecem em nenhum módulo de produção.

## 3.1 O achado que muda o custo do projeto

Inspecionei o TeiaJus. **O substrato de dados que faltava já existe e foi construído por você.**

| Capacidade já operacional no TeiaJus | Serve a |
|---|---|
| Espelhos oficiais mensais dos **10 órgãos julgadores do STJ**, com ementa, decisão, órgão, **relator**, classe e referências | topologia decisória; seleção por destinatário |
| Diário oficial diário, com metadados JSON e **íntegras em ZIP com `textSha256`** | a exigência dele de rastreamento da íntegra, não da ementa |
| DataJud `api_publica_stj` com `orgaoJulgador` e movimentos processuais | prevenção, tramitação, composição |
| Corpus canônico de 33.591 casos, 8.477 partes e 2.155 documentos com SHA-256 e linhagem verificável | jurimetria; base de análogos |
| Espelho CGU com 32.619 registros (CEIS, CNEP, CEPIM, CEAF, leniência) | precedente e sanção administrativa |
| Pipeline de evidência com **revisor nominal, hash e âncora literal**, com zero promoção automática | a auditabilidade que o titular exigiu |
| API JSON com 31 ações allowlisted, envelope v1, já integrada à FORJA na F5 | acoplamento sem obra nova |
| Política declarada de que espelho, ementa, metadado do DataJud e resultado web não substituem a íntegra do ato | é a doutrina dele, já escrita em código |

O TeiaJus, inclusive, já enuncia como princípio o que o titular disse na entrevista: **"descoberta não é prova"** e **"documento, identidade do ato, hash e trecho literal são controles distintos"**.

Portanto o trabalho não é coletar dados. São **três camadas de leitura sobre o que já existe**.

## 3.2 Camada 1 — Topologia decisória (subfase F3-B)

Artefato canônico: **MAPA DO DESTINATÁRIO**. Responde a uma pergunta que a FORJA hoje não faz: *para quem, nominalmente, esta peça está sendo escrita?*

Campos, todos preenchidos ou expressamente marcados como não apurados **com motivo**:

- **Órgão competente**, derivado do CNJ e conferido no regimento já presente na pasta do caso.
- **Prevenção**: existe? de quem? qual a origem — distribuição por dependência, relator de recurso anterior no mesmo processo, conexão? Com fundamento regimental citado (arts. 71 e 78 do RISTJ; art. 930, parágrafo único, do CPC). Pista pelo DataJud; **confirmação só na íntegra dos autos**.
- **Composição atual do órgão.** Armadilha já registrada pelo próprio escritório no `CLAUDE.md` a propósito do TJTO: composição muda, e um espelho de 2024 não prova a turma de hoje. Campo com **data de conferência obrigatória** e fonte oficial.
- **Posição do relator prevento** sobre a questão jurídica, agregada dos espelhos.
- **Posição da turma**, da **outra turma da mesma seção**, da **seção** e da **Corte Especial**.
- **Divergência conhecida entre órgãos fracionários** — gatilho de embargos de divergência e de uniformização, que hoje se perde.
- **Via recursal projetada** e **matéria constitucional a prequestionar desde já**.

Comandos do TeiaJus que alimentam o mapa, já existentes:

```
python forja_legal_search.py stj-search "<questão>" --orgao primeira_turma --orgao segunda_turma --artifact-dir <attempt>
python forja_legal_search.py stj-daily "<classe>" --days N --include-text --artifact-dir <attempt>
python forja_legal_search.py stj-datajud --limit N --artifact-dir <attempt>
```

Regra: o mapa **precede e roteia** a pesquisa. Não se pesquisa jurisprudência em abstrato — pesquisa-se para um destinatário identificado. É a frase dele, virada em ordem de execução.

## 3.3 Camada 2 — A ficha de precedente (subfase F5-B)

Substitui a nota numérica de aderência, que é pseudoprecisão. O objeto correto é um **dossiê por precedente**, espelhando o que o art. 489, §1º, incisos V e VI, do CPC exige do juiz — e voltando essa exigência para nós mesmos.

**Bloco de identidade do ato:** classe, número, órgão, **relator**, data de julgamento, data de publicação, colegiada ou monocrática.

**Bloco de regime jurídico** — aqui está a correção legal em relação ao documento 25:

| Regime | Efeito | Base |
|---|---|---|
| Vinculante | observância obrigatória | art. 927, I a V, do CPC: súmula vinculante; controle concentrado; repetitivos, IRDR e IAC; súmulas do STF em matéria constitucional e do STJ em infraconstitucional; orientação do plenário ou do órgão especial |
| Persuasivo qualificado | ônus argumentativo elevado para superar | acórdão de órgão superior, colegiado, recente, sobre a mesma questão |
| Persuasivo | vale pela razão que apresenta | monocrática, órgão diverso, antigo |

**Bloco de vigência:** superado, modulado, afetado por tema posterior, sobrestado? Com fonte e **data da conferência**. Precedente vigente ontem pode não estar vigente hoje.

**Bloco de íntegra:** obtida com hash, ou apenas ementa e espelho. **Regra dura: tese jurídica não se extrai de ementa.** Ementa é pista de localização. É a política já escrita do TeiaJus e é a exigência literal dele — *"o rastreamento da íntegra"*.

**Bloco de ratio decidendi:** o enunciado em uma frase, **com o trecho literal da íntegra que o sustenta e sua localização**, mais a identificação dos *obiter dicta* que poderiam ser confundidos com a ratio. Este bloco é a defesa contra o quarto modo de falha da nossa taxonomia de citação — tese deturpada, ratio contra dictum —, que hoje existe como item de checklist e não como artefato.

**Bloco de moldura fática:** os fatos que foram **determinantes** para aquela ratio. Não todos os fatos do paradigma: os determinantes. É essa restrição que torna o confronto útil.

**Bloco de confronto:** elemento a elemento contra o nosso caso — coincide, difere, ou não apurado —, com âncora dos dois lados: documento e página do nosso, trecho e localização do paradigma.

**Bloco de operação** — é aqui que a aderência produz efeito, sem tocar na força:

| Situação | Operação correta |
|---|---|
| Moldura coincide, precedente favorável | **aplicar**, demonstrando a coincidência |
| Moldura difere em elemento determinante, precedente contrário | **distinguir** (art. 489, §1º, VI, e art. 927, §1º) |
| Precedente vinculante contrário, moldura coincide | **delimitar o alcance** da ratio, ou sustentar **superação** (art. 927, §§2º a 4º); jamais ignorar |
| Precedente favorável de baixa autoridade, moldura coincide | usar como reforço, nunca como fundamento único |
| Sem operação declarada | **não citar** |

**Bloco adversarial:** o distinguishing que o adversário pode invocar contra o nosso próprio precedente, e a resposta antecipada.

**Bloco de decisão humana:** usar ou não usar, por quem, quando. O sistema entrega a matriz; a decisão é do advogado. É o que o titular exigiu e é coerente com a nossa doutrina antiautocertificação.

## 3.4 Camada 2-B — Seleção estratégica: a jurimetria que dá para fazer já

Aqui está a distinção que desbloqueia a maior parte do valor sem carregar o risco. O titular descreveu duas coisas diferentes sob o mesmo guarda-chuva estatístico, e elas têm perfis de risco opostos.

**J-A — Jurimetria de seleção.** Buscar o que o **destinatário identificado** já decidiu sobre a questão, para citá-lo. É técnica recursal ordinária, praticada por qualquer advogado sênior, e é exatamente o algoritmo que ele ditou. Risco reputacional: **nenhum**. Valor imediato: alto. **Fazer já.**

Ordem de busca, literal da fala dele:

1. o **próprio relator prevento** — o que ele já decidiu sobre a questão; é o mais constrangedor, pelo movimento do §2.4;
2. os **integrantes atuais da turma preventa**, individualmente;
3. a **turma**, como colegiado;
4. a **outra turma da mesma seção**;
5. a **seção**;
6. a **Corte Especial**;
7. **divergência aproveitável** entre órgãos fracionários;
8. **matéria constitucional a prequestionar** para o STF.

Os espelhos do STJ por órgão, com o campo relator, sustentam os itens 1 a 6 diretamente. É consulta, não inferência.

**J-B — Jurimetria de comportamento.** Série temporal de um julgador, para detectar variação de entendimento correlacionada a escritório ou parte; e comparação de deságios em acordos análogos, para aferir vantajosidade e risco de responsabilização do gestor. É o pedido de maior valor econômico e de maior risco reputacional do conjunto inteiro.

Contenção — por engenharia, não por opinião, porque ele não pediu contenção:
- fora do fluxo padrão, com acionamento manual exclusivo;
- produz **relatório interno** com metodologia, universo amostral, recorte temporal e limitações explícitas;
- **jamais compõe saída automática de peça**;
- a decisão de usar em peça é do titular, **registrada nominalmente**;
- **parecer prévio do Cícero por uso**, pela exposição do art. 34 do Estatuto da OAB, da litigância de má-fé e do art. 41 da LOMAN;
- **proibição de afirmar conduta ou intenção de pessoa identificada**: o achado descreve série, não motivação.

A aplicação do deságio em acordos com o poder público é um **produto autônomo** e tem aplicação imediata ao caso CORSAN/AGERST que já está na fila. Comercialmente pode valer mais do que a fábrica de petições.

## 3.5 Camada 3 — Auditabilidade da própria pesquisa

Ele foi específico: *"ela precisa ter explicabilidade nas suas buscas, nos seus rastreamentos, nos seus parâmetros, nas suas pesquisas; ela própria precisa estar sujeita à rastreabilidade"*. E ligou isso ao risco existencial: *"sempre que uma pesquisa se revelar falsa ou errada, o inauditável sempre vai causar desmoralização daquele que usa a IA"*.

Hoje arquivamos **resultados**. Não arquivamos o **raciocínio da busca**.

Artefato: **CADERNO DE PESQUISA**, por questão de pesquisa:
- a pergunta de pesquisa, em uma frase;
- os parâmetros usados: termos, órgãos, recorte temporal, bases;
- as bases consultadas **e as não consultadas, com motivo** — custo, indisponibilidade, sigilo, cota;
- o que foi encontrado;
- **o que foi procurado e não foi encontrado.** O resultado negativo hoje se perde e é informação estratégica de primeira ordem: a ausência de precedente favorável no órgão prevento muda a estratégia da peça inteira;
- o que foi descartado e por quê.

A telemetria do TeiaJus já grava em `telemetria/legal_search/`. O que falta é o ato motivado escrito por cima — e vale a regra reitora do §1.1 do documento 25: **isso não é log, é peça endereçada a quem revisa.**

## 3.6 Precedente administrativo

Ele estendeu expressamente a teoria dos precedentes ao contencioso administrativo, que é o terreno dele. O `forja_authorities.py` só reconhece CNJ, STJ, STF, súmula e tema.

Falta a camada de **TCU** (acórdãos e súmulas), **CNJ e CNMP**, **CGU e CRG** — que o TeiaJus já espelha com 32.619 registros —, **CADE** e **CVM**. Barato de acrescentar, de alto valor para a carteira real do escritório, e diretamente ligado à aplicação de deságio da jurimetria.

## 3.7 Gates novos que decorrem, e o que eles impedem

| Gate | Impede |
|---|---|
| Tese nunca extraída de ementa sem íntegra com hash | o modo de falha "tese deturpada" da nossa taxonomia |
| Todo precedente citado tem operação declarada: aplicar, distinguir, delimitar ou superar | citação decorativa, que não sustenta proposição |
| Todo precedente citado tem confronto de moldura fática registrado | precedente aparentemente forte e faticamente inaplicável |
| Vigência conferida com data | citar precedente superado ou modulado |
| Destinatário declarado por precedente | pesquisa em abstrato, que o titular rejeitou |
| Resultado negativo registrado | a ilusão de cobertura, que é o pior erro de pesquisa |
| Campos de prevenção preenchidos ou não apurados com motivo | a falha já cometida no caso Cafelana |

Os quatro primeiros são bloqueadores P0. O quinto e o sexto são exigência de completude do artefato. O sétimo fecha uma lição que o escritório já nos deu uma vez.

---

# PARTE IV — Sequenciamento e o que depende dele

## 4.1 Ordem proposta

**Bloco 1 — precedentes e topologia.** É o "principalmente" dele, é onde estamos mais aquém, e o substrato do TeiaJus já existe. Camada 1, o mapa do destinatário, antes da Camada 2, a ficha de precedente, porque a primeira roteia a segunda. J-A junto, porque é consulta e não inferência.

**Bloco 2 — dialética.** F2-B e F2-C. Barato, porque o motor de perguntas já existe no F2-A; faltam seletor, renderizador e rastreador. É também o que ele mais detalhou e o que o impressiona primeiro.

**Bloco 3 — identidade.** Começa hoje pelo Corpus B, a extração dos diffs de revisão, que não depende de pedido nenhum. Corpus de peças assinadas e preferência doutrinária dependem dele.

**Bloco 4 — caderno de pesquisa e precedente administrativo.**

**Bloco 5 — J-B, a jurimetria de comportamento.** Por último, com toda a contenção do §3.4.

## 4.2 O que só ele pode dar

- Vinte a trinta peças assinadas, estratificadas por tipo, incluindo duas ou três que ele considere ruins.
- Preferência doutrinária por matéria — ele ofereceu responder isso na própria entrevista.
- Parâmetros por classe de caso: teto de rodadas de consulta, extensão máxima por tipo de peça, nível de revisão exigido, disponibilidade do módulo J-B.
- Autorização e limites do módulo J-B.
- Os textos dele sobre soberania cognitiva e espaço público não estatal.

## 4.3 Como apresentar

Três coisas, e a segunda é a que fecha pelo critério dele:

1. A tabela de rastreabilidade requisito → fase de `planejamento/25`, §6. Demonstra que a arquitetura decorre da fala dele, e não do gosto do fornecedor.
2. **Uma demonstração ao vivo de recusa**: o sistema bloqueando a citação de um precedente cuja íntegra não conseguiu obter. O critério de compra dele não é velocidade — ele não mencionou custo, prazo nem tecnologia uma única vez. É confiabilidade auditável, e ele disse por quê: pesquisa falsa desmoraliza quem a usa.
3. A tabela de parâmetros por classe **vazia**, para preencher com ele. Ele recusou expressamente o papel de especificador de cima — *"não de uma forma divina, de uma criatura perfeita que nasce pronta; seríamos parceiros, cresceríamos juntos"*. Chegar com especificação fechada contraria o que ele acabou de dizer.

## 4.4 Riscos deste plano, declarados

- **Goodhart nas métricas de estilo e de tese.** Já mitigado no desenho, com cobertura em vez de contagem, mas qualquer limiar novo precisa passar pelo ciclo AR antes de virar gate, com canário de falha única.
- **Composição de órgão é dado perecível.** Um mapa do destinatário desatualizado é pior que nenhum, porque tem aparência de autoridade. Data de conferência obrigatória e prazo de validade curto.
- **Espelho não é íntegra.** O risco maior do Bloco 1 é a tentação de extrair ratio da ementa, porque a ementa está disponível e a íntegra dá trabalho. É exatamente o modo de falha que desmoraliza. O gate precisa ser duro desde o primeiro dia.
- **O Corpus B é pequeno e enviesado** — reflete os casos que fizemos, não a obra dele. Um padrão observado três vezes em três casos do mesmo tipo não é regra de escritório. Marcar o N2 com o tipo de peça em que foi observado.
- **O J-B pode vazar para dentro de uma peça por acidente.** É evento de custo assimétrico. A contenção precisa ser estrutural, não procedimental.
