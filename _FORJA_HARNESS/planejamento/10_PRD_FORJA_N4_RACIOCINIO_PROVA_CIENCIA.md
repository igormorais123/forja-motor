# PRD — FORJA N4: Raciocínio, Prova e Ciência

**Produto:** FORJA, harness de elaboração, revisão e entrega assistida de petições  
**Versão proposta:** N4.0  
**Data:** 2026-07-10  
**Status:** versão final do planejamento N4; candidata não vigente  
**Revisão do documento:** final-r2, após auditoria cruzada de 2026-07-10  
**Base vigente:** `../FORJA_SPEC_MANIFEST.json`  
**Base incremental:** `08_PLANO_FORJA_N3_INTEGRIDADE_VISUAL_E_GESTAO.md` e `09_AUDITORIA_ADVERSARIAL_PONTOS_DECISIVOS.md`  
**TDD:** `11_TDD_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`  
**Roadmap:** `12_ROADMAP_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`  
**Diagramas:** `13_DIAGRAMAS_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`

> Este documento planeja uma evolução incremental. Ele não altera o `FORJA_SPEC_MANIFEST.json`, não promove N3 ou N4 e não muda o comportamento atual. A ativação depende dos gates do roadmap e de atualização futura e coerente do conjunto normativo.

---

## 1. Decisão de produto

A N4 não será uma nova fábrica nem uma troca do motor de redação. Será uma camada adicional de **raciocínio verificável** sobre a FORJA existente.

O objetivo é fazer com que a qualidade que hoje pode aparecer na peça final exista também como estrutura interna auditável:

1. cada questão relevante deve ser identificada antes da redação;
2. cada afirmação decisiva deve estar ligada ao que a sustenta, limita ou contradiz;
3. cada pedido, alegação, omissão e resposta deve ter cobertura comprovável;
4. cada tese deve indicar sua maturidade, risco e posição na estratégia;
5. cada peça deve possuir testes próprios, definidos antes do texto final;
6. inconsistências globais de terminologia, tempo, cálculo e sentido devem ser detectadas;
7. quando houver tema não jurídico relevante, a FORJA poderá acrescentar **Lastro Científico Interdisciplinar — LCI**, com pesquisa acadêmica séria e linguagem calibrada;
8. toda correção humana estrutural deve poder virar aprendizado testável, sem reescrever silenciosamente casos passados.

A unidade mínima deixa de ser apenas “parágrafo bem escrito” e passa a ser:

**questão → afirmação → fonte → relação lógica → teste → decisão → redação → auditoria.**

---

## 2. Linha de base que a N4 deve respeitar

### 2.1 Capacidades já existentes e preservadas

A N4 parte das capacidades atuais, sem duplicá-las:

- fluxo persistente F0–F10;
- manifest, estado, eventos, hashes e pacote de revisão;
- índice documental, cobertura, fatos, proposições e proveniência por bloco planejados na N3;
- fonte oficial e taxonomia de falhas de citação;
- regimento do tribunal e leis gerais como gates;
- auditoria adversarial A1 em F3, F4 e F7;
- pareceres obrigatórios de Helena e Cícero, com decisões registradas;
- redação sobre template Medina Osório;
- fidelidade Markdown → DOCX → PDF;
- QA visual página a página e controle de diagramas;
- integração file-first com a gestão do escritório;
- fechamento apenas com evidência real de entrega;
- diff pós-entrega e retrospectiva.

### 2.2 Restrição operacional constatada

No levantamento de 2026-07-10, a pasta `state/` continha 21 diretórios de caso, mas ainda não apresentava os novos artefatos canônicos esperados para a promoção plena da N3, como `n3_artifacts`, `F3_FACT_LEDGER.json`, `CONTEXT_VALIDATION.json` ou auditorias A1 materializadas nesses estados.

Consequência de produto:

- a N4 pode ser especificada e construída em sombra;
- a N4 **não pode ser promovida antes de existir uma linha de base N3 comprovada em casos reais**;
- primeiro se prova que o alicerce existente funciona; depois se torna obrigatória a nova camada.

### 2.3 Lições da auditoria de 2026-07-10 incorporadas como requisito

A auditoria de artefatos reais do ciclo N3, registrada em `../reports/AUDITORIA_ULTRACODE_2026-07-10.md`, trouxe cinco lições que a N4 deve transformar em gate ou fixture:

1. **Metadados contaminados em todos os documentos do ciclo auditado:** a verificação precisa ocorrer no arquivo final, depois do render e de qualquer regeneração.
2. **Defeitos visuais que só apareceram em inspeção ampliada:** títulos de cards ultrapassaram bordas apesar do QA anterior; o corpus deve conter esses casos reais.
3. **Registro de hashes dessincronizado do disco:** oito registros ficaram defasados depois de sanitização ou novo render; toda alteração física invalida hash e pacote dependente.
4. **Versão divergente entregue ao revisor humano:** no caso Patrícia/Fábio, a cópia de revisão não correspondia à versão auditada; a seleção do anexo deve estar vinculada ao pacote aprovado.
5. **O próprio verificador pode errar:** a regra do art. 343-A do RISTJ estava invertida e foi corrigida após conferência oficial; gates determinísticos também precisam de hard negatives e fonte canônica.

A mesma auditoria derrubou como **falso positivo** a crítica às margens 2,5/5,4 cm das peças visual law: elas pertenciam ao perfil visual aprovado. Portanto, a N4 deve conferir o arquivo contra o `layoutProfileId` selecionado para a peça — padrão Word ordinário ou variante visual law aprovada — e nunca forçar um único conjunto de margens sobre todos os produtos.

---

## 3. Problemas que a N4 resolve

### P1 — Cobertura aparente

Uma peça pode parecer completa e ainda deixar sem resposta um pedido, fundamento, documento, evento ou possível omissão.

### P2 — Coerência temática sem identidade processual

O texto pode preservar a tese geral e, ao mesmo tempo, alternar indevidamente entre “não conhecimento”, “improcedência”, “rejeição” e “extinção”, ou modificar a qualificação de um mesmo evento em seções diferentes.

### P3 — Lastro genérico

Expressões como “segundo o material do escritório” indicam uma origem ampla, mas não permitem confirmar a afirmação exata, seu local, seu alcance ou sua condição de validade.

### P4 — Comparação documental incompleta

Em peças responsivas ou sucessivas, a tese de repetição, omissão, inovação ou contradição pode ser formulada sem uma matriz que compare:

- alegação anterior;
- resposta judicial ou adversária;
- nova alegação;
- diferença material;
- consequência processual.

### P5 — Tese correta, mas superdimensionada

Um precedente ou estudo pode apoiar apenas parte do raciocínio e ser usado como se resolvesse toda a controvérsia.

### P6 — Plano sem critérios de falsificação

Uma peça pode ser revisada por impressão geral, sem perguntas literais que permitam declarar objetivamente se cumpriu ou não o que o caso exigia.

### P7 — Consenso artificial

Agentes diferentes podem repetir a mesma premissa, inclusive quando ela veio do comando inicial e não dos autos. Quantidade de concordâncias não substitui verificação independente.

### P8 — Conhecimento interdisciplinar usado como ornamento

Temas de psicologia, saúde, contabilidade, economia, engenharia ou políticas públicas podem ser importantes para a tese, mas são frequentemente tratados por generalizações, referências vagas ou autoridade acadêmica sem conexão precisa com a proposição defendida.

### P9 — Aprendizado sem causa

Uma correção humana pode ser registrada apenas como texto “antes/depois”, sem indicar se a causa foi erro factual, fonte inadequada, falha de recuperação, estratégia, terminologia, visual, estilo ou preferência.

---

## 4. Objetivos

1. Obter cobertura explícita de todas as questões e pedidos materiais.
2. Tornar afirmações decisivas rastreáveis até fonte, localizador e condição de uso.
3. Detectar contradições de evento, termo, data, cálculo e conclusão no documento inteiro.
4. Distinguir tese principal, subsidiária, de reserva e ainda imatura.
5. Impedir que o critério de aceite seja relaxado para aprovar uma peça defeituosa.
6. Fortalecer peças responsivas com comparação documental e auditoria A1 integradas.
7. Acrescentar fundamentos acadêmicos de outras áreas quando realmente pertinentes.
8. Separar evidência científica geral de prova individual do caso.
9. Capturar correções humanas como dados de melhoria e testes de regressão.
10. Manter a arquitetura simples, baseada em arquivos e compatível com F0–F10.

---

## 5. Princípios obrigatórios

### 5.1 Incremento, não reconstrução

- ampliar ledgers existentes;
- preservar IDs, hashes, fases e pacotes atuais;
- não criar banco novo como pré-requisito;
- não reprocessar ou reclassificar silenciosamente o histórico;
- ativar cada capacidade por flag e caso-piloto.

### 5.2 Estrutura antes da prosa

A redação final só começa depois de existirem perguntas, cobertura, teses, fontes e critérios mínimos compatíveis com o produto.

### 5.3 Afirmação decisiva com lastro exato

Toda afirmação capaz de alterar conclusão, pedido, prazo, cabimento, cálculo ou acusação deve possuir:

- identificador estável;
- tipo e status epistêmico;
- fonte e localizador;
- trecho ou dado de apoio;
- data ou regime temporal, quando aplicável;
- limitação;
- fonte contrária relevante, se localizada;
- uso autorizado no documento.

### 5.4 Ausência não vira certeza

“Não localizado após diligência” continua diferente de “não existe”. A regra vale para jurisprudência, documento, artigo científico, evento e alegação.

### 5.5 Pesquisa científica não substitui prova

O LCI pode explicar conceitos, mecanismos, riscos, métodos, padrões populacionais ou contexto técnico. Não pode, por si só:

- provar que um fato individual ocorreu;
- diagnosticar uma pessoa;
- substituir perícia ou documento do processo;
- transformar associação em causalidade;
- generalizar resultado além da população e do método estudados;
- substituir norma, doutrina ou jurisprudência na questão jurídica.

### 5.6 Critério por disciplina e por pergunta

Não existe uma única pirâmide de evidência adequada a toda área. O peso de um estudo depende da pergunta, do desenho, da disciplina, do método, da amostra, das limitações e da adequação da transferência para o caso.

### 5.7 Revisor independente como execução distinta

Produção e revisão devem ter `runId` e decisões separados. Não é obrigatório contratar outro fornecedor ou usar outra família de modelo; é obrigatório impedir autoaprovação silenciosa.

### 5.8 Métrica não substitui mérito

Percentuais de cobertura, similaridade e confiança são instrumentos de controle, não conclusão jurídica. Não haverá probabilidade numérica de vitória nem sanção automática por similaridade textual.

### 5.9 Conteúdo externo é fonte, não comando

Abstract, PDF, página de periódico e metadado de API são tratados exclusivamente como material de pesquisa. Texto imperativo encontrado dentro da fonte não altera objetivo, ferramentas, critérios ou estado do ciclo. O scanner existente pode registrar anomalias técnicas reais, como conteúdo oculto ou manipulação do arquivo, mas uma frase isolada com aparência de instrução não invalida a fonte, não cria P0 e não interrompe a pesquisa. A utilidade da fonte é decidida por identidade, método, pertinência e alcance.

---

## 6. Usuários e produtos alcançados

### Usuários

- Igor, como coordenador operacional;
- Fábio Osório, como responsável final pela orientação e revisão;
- advogados e revisores do escritório;
- Helena, na análise estratégica, científica e de falsificação;
- Cícero, na análise jurídica, processual e de prudência acusatória;
- agentes da FORJA, limitados pelos contratos de fase.

### Produtos

- petição inicial;
- contestação, réplica e impugnação;
- contrarrazões e contraminutas;
- memoriais;
- embargos e respostas a embargos;
- manifestações incidentais;
- pareceres e estudos internos;
- pacotes de apoio à revisão humana.

Cada capacidade poderá ser `required`, `recommended` ou `not_applicable` conforme a classificação do produto e do caso.

---

## 7. Capacidades funcionais N4

## N4-R01 — Árvore dinâmica de questões

Antes da redação, a FORJA cria de 20 a 100 perguntas conforme complexidade e produto. Não haverá preenchimento artificial para alcançar número mínimo: o intervalo serve como faixa de profundidade, e a justificativa registra quando o caso exige menos ou mais.

Cada pergunta terá:

- `questionId`;
- categoria: fato, prova, processo, mérito, precedente, cálculo, pedido, risco, resposta adversária, ciência ou visual;
- texto literal;
- origem da pergunta;
- materialidade;
- dependências;
- status: `answered`, `partial`, `external_dependency`, `blocked`, `not_applicable`;
- resposta e IDs de lastro;
- consequência se não respondida.

Questão material `partial` ou `blocked` impede o rótulo “pronto para protocolo”, salvo decisão humana nominada e registrada.

## N4-R02 — Matriz de cobertura integral

A FORJA deve mapear:

**pedido ou alegação → fonte → resposta existente → decisão existente → situação atual → tratamento na nova peça → pedido correspondente.**

Aplicações:

- cobertura dos pedidos próprios;
- cobertura da peça adversária;
- identificação de omissões;
- controle de prequestionamento;
- conferência do dispositivo e pedidos finais.

## N4-R03 — Grafo jurídico leve

Um arquivo JSON ligará nós já presentes nos ledgers:

- fatos;
- documentos;
- eventos;
- alegações;
- proposições jurídicas;
- precedentes;
- estudos acadêmicos;
- teses;
- pedidos;
- decisões;
- contradições.

Relações mínimas (enumeração canônica, fechada por versão de schema):

- `supports`;
- `contradicts`;
- `qualifies`;
- `depends_on`;
- `responds_to`;
- `ignored_by`;
- `distinguishes`;
- `quantifies`;
- `limits`;
- `records` — documento registra fato ou evento;
- `justifies` — tese fundamenta pedido;
- `tested_by` — pedido ou tese é verificado por teste do caso;
- `resolves` — decisão anterior resolve alegação ou questão.

Toda relação de sustentação (`supports`, `justifies`) carrega atributo `scope` (`full` ou `partial`): "sustenta parcialmente" é `supports` com `scope: partial`, nunca uma relação nova inventada fora da enumeração. Relação fora da enumeração reprova o grafo na validação.

Não será implantado banco de grafos na N4 inicial. O JSON é derivado dos ledgers e validado por referências.

## N4-R04 — Matriz de maturidade e contaminação de teses

Cada tese receberá:

- força documental;
- força jurídica;
- lacunas;
- melhor objeção;
- risco de enfraquecer tese superior;
- posição: principal, subsidiária, reserva ou não usar;
- gatilho de ativação;
- veículo processual adequado;
- decisão de Helena;
- decisão de Cícero;
- decisão humana final quando houver divergência material.

## N4-R05 — TDD jurídico do caso

Cada peça terá 10 a 25 testes literais definidos antes da versão final, além dos gates gerais da FORJA.

Exemplos:

- “O texto distingue não conhecimento de improcedência em todas as ocorrências?”
- “Cada pedido adversário material recebeu resposta e consequência?”
- “O precedente sustenta a proposição usada, e não apenas tema próximo?”
- “A data do ato que define o regime intertemporal está comprovada?”

É proibido modificar o teste apenas para transformar falha em aprovação. Se o teste estiver incorreto, a correção exige justificativa, nova versão e reexecução.

## N4-R06 — Auditoria metacognitiva e anti-concordância

A revisão registrará:

- quais premissas vieram do usuário, e-mail ou comando;
- quais foram confirmadas nos autos;
- quais permaneceram apenas como declaração;
- onde múltiplos agentes repetiram uma premissa sem verificação independente;
- qual recomendação mudou por fato novo, erro identificado ou preferência explícita;
- quais métricas poderiam estar sendo otimizadas sem ganho jurídico real.

## N4-R07 — Ledger longitudinal de condutas

Em casos com histórico sucessivo, a FORJA poderá organizar condutas alegadas ou verificadas em dois polos e no tempo.

Cada item será `verified`, `partial`, `not_verified` ou `contradicted`, com fonte exata, correção posterior e formulação externa permitida. O ledger não cria narrativa acusatória por acúmulo; a materialidade e a prudência continuam submetidas à A1 e a Cícero.

## N4-R08 — Mapa de fatores decisórios

Decisões anteriores do próprio caso serão decompostas em:

- requisito explícito;
- prova considerada suficiente ou insuficiente;
- cautela do julgador;
- questão deixada em aberto;
- efeito sobre a próxima peça.

O produto é um mapa de critérios demonstrados nas decisões, não perfil psicológico nem imitação retórica do julgador.

## N4-R09 — Estratégia condicional de composição

Quando aplicável, a FORJA poderá registrar:

- interesses;
- limites não negociáveis;
- concessões possíveis;
- condições de ativação;
- alternativa sem acordo;
- zona qualitativa de possível composição;
- efeito processual e probatório.

Não serão inventadas probabilidades de sucesso, valores sem base ou suposta intenção da parte contrária.

## N4-R10 — Identidade terminológica e de eventos

A FORJA cria um vocabulário canônico do caso e compara o documento inteiro. Alternâncias como “não conhecimento”, “improcedência”, “rejeição” e “extinção” serão bloqueadas quando descrevem o mesmo evento sem distinção expressa e fonte correspondente.

## N4-R11 — Comparação estruturada entre documentos

Para peças responsivas, sucessivas ou integrativas, a FORJA comparará unidades argumentativas, não apenas porcentagem de texto.

Saída mínima:

- argumento anterior;
- resposta já dada;
- argumento atual;
- conteúdo novo ou repetido;
- documento e localizador;
- consequência possível;
- ressalva sobre prequestionamento ou justificativa legítima.

Similaridade é sinal de triagem, nunca prova automática de má-fé ou caráter protelatório.

## N4-R12 — Validador intertemporal

Quando houver mudança normativa relevante, o sistema identificará:

- norma ou regime em disputa;
- ato juridicamente relevante;
- data comprovada do ato;
- regra de transição;
- fonte vigente;
- conclusão e incerteza residual.

## N4-R13 — Cenários objetivos de quantificação

Quando a tese envolver valor, proveito econômico, atualização, dano, custo ou impacto mensurável, a FORJA poderá produzir:

- fórmula;
- entradas conhecidas e fontes;
- entradas controvertidas;
- faixa mínima, máxima e incontroversa, quando calculável;
- sensibilidade a variáveis;
- limitações;
- ponto que depende de perícia ou liquidação.

Sem fórmula e dados reais, o artefato registra impossibilidade de quantificação; não cria simulação decorativa.

## N4-R14 — Lastro Científico Interdisciplinar — LCI

A F2 classifica a pesquisa científica como:

- `not_applicable`;
- `rapid`;
- `strict`.

O LCI é acionado quando uma proposição não jurídica material pode ser esclarecida por psicologia, saúde, contabilidade, economia, engenharia, educação, políticas públicas ou outra área correlata.

O produto interno deve conter pergunta de pesquisa, protocolo, fontes verificadas, qualidade metodológica, evidências contrárias, limites de transferência e mapa entre estudo e proposição jurídica.

## N4-R15 — Alcance real de precedentes e analogias

Cada autoridade decisiva deve registrar:

- proposição efetivamente sustentada;
- trecho ou razão relevante;
- semelhanças com o caso;
- distinções;
- limite do uso;
- caráter direto ou analógico;
- vigência e situação atual.

## N4-R16 — Consistência global

A F7 executará verificação transversal de:

- partes, números, datas e valores;
- identidade dos eventos;
- termos processuais;
- tese principal e subsidiárias;
- dispositivo e pedidos;
- ressalvas;
- referências cruzadas;
- relação entre texto e elementos visuais;
- correspondência entre peça, relatório e e-mail de entrega;
- metadados do arquivo final (autor, empresa, template) conforme o padrão do escritório;
- layout do documento final conforme o `layoutProfileId` registrado no pacote, que pode apontar ao padrão Word ordinário ou a uma variante visual law aprovada;
- identidade da versão selecionada para entrega: o hash do arquivo escolhido coincide com o hash do pacote auditado;
- confirmação pós-entrega pelo hash real quando o canal expuser os bytes do anexo ou, nos demais canais, pelo `artifactId`, hash pré-envio e evidência externa correspondente.

## N4-R17 — Aprendizado por causa

O diff humano da F10 será classificado em:

- fato;
- direito;
- fonte;
- recuperação;
- planejamento;
- terminologia;
- cálculo;
- ciência;
- visual;
- estilo/voz;
- preferência;
- pacote/gestão.

Erro estrutural reproduzível gera proposta de teste. Preferência isolada não vira regra global automaticamente.

## N4-R18 — Evidência da própria execução

O pacote interno registrará:

- plano usado;
- artefatos de entrada e saída;
- chamadas de ferramentas;
- fontes recuperadas;
- verificações executadas;
- revisões rejeitadas ou aceitas;
- decisões humanas;
- hashes e `runId`;
- custo e duração apenas quando medidos.

Não se exige exposição de raciocínio interno irrestrito. Exige-se trilha operacional suficiente para localizar a origem de uma falha.

---

## 8. Produto LCI em detalhe

### 8.1 Modos

| Modo | Quando usar | Profundidade mínima |
|---|---|---|
| `not_applicable` | não há proposição não jurídica material | justificativa curta |
| `rapid` | apoio contextual ou técnico relevante, sem depender exclusivamente da ciência | pergunta precisa, duas rotas de descoberta quando disponíveis, estudos centrais e contraditórios, síntese calibrada |
| `strict` | proposição científica é central, contestável ou capaz de alterar pedido/resultado | protocolo ampliado, ao menos duas bases, critérios de seleção, avaliação metodológica, rastreio de exclusões e auditoria independente |

O modo `strict` não transforma toda petição em revisão sistemática. PRISMA será referência de transparência para revisões formais; no uso ordinário, a FORJA aplicará uma revisão rápida de evidências proporcional ao caso.

### 8.2 Rotas de pesquisa planejadas

- **Crossref:** metadados e DOI;
- **OpenAlex:** descoberta ampla e relações entre trabalhos, mediante acesso disponível;
- **PubMed/PMC via NCBI:** saúde, medicina e áreas biomédicas;
- bases disciplinares adicionais quando acessíveis e justificadas;
- busca manual e encadeamento de referências;
- Google Scholar apenas como descoberta manual complementar, sem dependência técnica obrigatória.

### 8.3 Ficha mínima de estudo

Cada estudo selecionado deve registrar:

- título, autores, ano e periódico;
- DOI, PMID, PMCID ou identificador equivalente;
- versão: preprint, manuscrito aceito ou versão publicada;
- revisão por pares conhecida;
- tipo de estudo;
- população, amostra e contexto;
- método, variáveis e resultados;
- tamanho de efeito ou medida reportada, se houver;
- limitações;
- financiamento e conflitos informados;
- correção, expressão de preocupação ou retratação;
- proposição que o estudo sustenta;
- proposição que o estudo **não** sustenta;
- aplicabilidade ao caso;
- evidência contrária relevante.

### 8.4 Estados de síntese

- `convergent` — fontes adequadas convergem;
- `mixed` — resultados relevantes divergem;
- `weak` — evidência insuficiente ou metodologicamente frágil;
- `absent` — não foi localizada evidência adequada;
- `not_transferable` — existe evidência, mas não pode ser transportada para a proposição do caso.

### 8.5 Uso permitido na peça

- `contextual_support`;
- `technical_definition`;
- `mechanism_support`;
- `risk_support`;
- `methodological_support`;
- `not_for_individual_fact`;
- `not_for_causal_claim`.

Linguagem final deve corresponder ao estado epistêmico: “indica”, “é compatível”, “há evidência mista” ou “não permite concluir”, conforme o caso. Fórmulas absolutas como “a ciência prova” são bloqueadas quando o corpus não sustentar essa força.

---

## 9. Jornada N4 dentro de F0–F10

| Fase | Acréscimo N4 |
|---|---|
| F0 | nenhuma mudança de fonte de verdade; apenas registrar versão/flags |
| F1 | preservar cobertura e documentos necessários às comparações |
| F2 | classificar árvore de questões, módulos condicionais e modo LCI |
| F3 | consolidar eventos, identidade terminológica, comparação documental, relações e condutas |
| F4 | fechar cobertura, maturidade de teses, testes do caso, fatores decisórios, temporalidade, quantificação e pareceres |
| F5 | manter pesquisa jurídica oficial e executar a via paralela F5C quando LCI aplicável |
| F6 | redigir somente com afirmações autorizadas e mapa parágrafo→lastro |
| F7 | executar testes do caso, consistência global, metacognição, auditoria científica e A1; após zero P0, preservar a subfase vigente F7-B |
| F8 | partir de `final_markdown` e confirmar que tabelas, gráficos e diagramas preservam sentido, fonte e legibilidade |
| F9 | empacotar peça limpa e cadernos internos correspondentes aos mesmos hashes |
| F10 | classificar diff humano, registrar aprendizado e sincronizar gestão sem alterar histórico |

Internamente, F5 passa a ter duas vias nomeadas: **F5J** (pesquisa jurídica oficial, comportamento vigente, inalterado) e **F5C** (Lastro Científico Interdisciplinar, condicional à classificação de F2). Os dois rótulos existem apenas dentro de F5 para fins de contrato, artefato e diagrama; o modelo público F0–F10 não será renumerado.

---

## 10. Gates de produto

### Gate N4-0 — Base operacional

N4 não pode ser promovida sem evidência de ciclos N3 reais, com ledgers, contexto, auditoria, visual e gestão coerentes.

### Gate N4-1 — Questões

Toda questão material está respondida, explicitamente bloqueada ou aceita por decisão humana nominada.

### Gate N4-2 — Cobertura

Todo pedido, alegação e ponto decisivo possui tratamento e consequência identificáveis.

### Gate N4-3 — Relações

Nenhum nó decisivo aponta para ID inexistente; fato, tese, fonte, pedido e decisão mantêm relações válidas.

### Gate N4-4 — Terminologia e tempo

Não existe alternância processual, data ou regime temporal material sem justificativa.

### Gate N4-5 — Testes do caso

Todos os testes bloqueantes da versão vigente passam. Mudança de critério exige versionamento e justificativa.

### Gate N4-6 — Ciência

Quando LCI é aplicável, nenhuma citação acadêmica entra na peça sem identidade confirmada, fonte lida no nível necessário, alcance delimitado e estado de correção/retratação consultado.

### Gate N4-7 — Metacognição

Premissas externas não confirmadas, consenso repetido e mudanças de recomendação estão explicitados no relatório interno.

### Gate N4-8 — Consistência global

Peça, pedidos, quadros, diagramas, relatório e e-mail não divergem sobre fatos, termos, valores, ressalvas ou pendências.

### Gate N4-9 — Aprendizado

Correção estrutural só vira regra após causa classificada, exemplo reproduzível e teste correspondente.

### Gate N4-10 — Expedição

Antes da entrega, o arquivo selecionado deve ter o mesmo hash do pacote auditado, metadados válidos e registro reconciliado com o disco. Depois da entrega, o hash do anexo é reconferido quando o canal disponibilizar o arquivo; quando não disponibilizar, valem o `artifactId`, o hash conferido antes do envio e a evidência externa de entrega. Divergência real bloqueia o fechamento e reabre F9. A mera indisponibilidade de hash pós-envio não bloqueia o sistema quando a cadeia alternativa estiver completa.

---

## 11. Critérios de aceitação

1. 100% das afirmações decisivas do piloto possuem lastro exato ou bloqueio.
2. 100% dos pedidos e alegações materiais possuem estado na matriz de cobertura.
3. Zero termo processual material conflitante sem justificativa.
4. Zero referência para nó, documento, fonte ou estudo inexistente.
5. Zero teste jurídico bloqueante relaxado sem nova versão e justificativa.
6. Zero citação científica fabricada, não identificada ou usada além do alcance verificado.
7. Toda síntese LCI registra limitações e busca de evidência contrária.
8. Comparação documental distingue repetição, inovação, resposta anterior e possível prequestionamento.
9. Quantificação usa fórmula e dados rastreáveis ou declara impossibilidade.
10. Produção e revisão possuem execuções separadas.
11. Peça, DOCX, PDF, relatório e pacote mantêm identidade por hash.
12. Gestão do escritório recebe fase, bloqueio, próximo passo e artefatos, sem concluir demanda por mera existência de rascunho.
13. N4 desligada reproduz o comportamento anterior sem apagar artefatos.
14. Nenhum caso histórico é reescrito durante replay.
15. Documento selecionado para entrega tem metadados válidos, layout conforme o perfil aprovado e hash idêntico ao pacote auditado; a evidência pós-entrega segue o contrato compatível com o canal.

---

## 12. Métricas

### Qualidade

- cobertura de questões materiais;
- cobertura de pedidos e alegações;
- afirmações decisivas com fonte exata;
- contradições globais detectadas antes da revisão humana;
- testes do caso aprovados/reprovados por versão;
- citações jurídicas e científicas verificadas;
- estudos com alcance e limitações preenchidos;
- correções humanas por causa;
- regressões evitadas por testes novos.

### Operação

- duração por fase e módulo;
- número de reaberturas e causa;
- artefatos produzidos e invalidados por hash;
- modo LCI usado;
- fontes consultadas e indisponíveis;
- sincronização com a gestão;
- diferença entre versão produzida e versão humana aprovada.

### Métricas proibidas como verdade de mérito

- probabilidade numérica de vitória;
- “confiança” sem calibração e sem base;
- similaridade textual como prova de má-fé;
- quantidade de artigos como substituto de qualidade;
- número de agentes concordantes como substituto de prova.

---

## 13. Fora do escopo N4 inicial

- troca generalizada do modelo-base;
- catálogo de fornecedores de IA;
- compra de GPU, servidor ou infraestrutura nova;
- fine-tuning, LoRA, QLoRA ou treinamento por reforço;
- banco vetorial, relacional ou de grafos como pré-requisito;
- busca científica autônoma ilimitada;
- revisão sistemática completa em toda petição;
- meta-análise sem dados compatíveis e protocolo próprio;
- protocolo judicial, assinatura ou envio automático;
- pontuação psicológica do julgador;
- percentuais especulativos de êxito;
- alteração retroativa de peças históricas para melhorar métricas.

Esses itens podem ser reavaliados no futuro apenas mediante problema concreto, ganho mensurável e novo planejamento.

---

## 14. Triagem da análise externa recebida

### Incorporado

- afirmação como unidade rastreável;
- coerência terminológica global;
- matriz de comparação entre peças sucessivas;
- alcance e limites de precedentes analógicos;
- cenários objetivos de quantificação;
- verificação intertemporal;
- trilha operacional por execução;
- baseline, regressão, sombra e promoção gradual;
- classificação causal das correções humanas;
- casos negativos difíceis para testes;
- auditoria científica de método, fonte e transferência.

### Incorporado com redução de escopo

- grafo de conhecimento vira JSON leve sobre os ledgers, sem banco novo;
- memória institucional vira arquivos, testes e retrospectivas versionadas;
- diversidade de revisão significa execução independente, não obrigação de fornecedor diferente;
- PRISMA inspira transparência no modo `strict`, mas não é imposto ao apoio científico ordinário;
- “uso de ferramentas” significa operações verificáveis já compatíveis com a FORJA, não autonomia irrestrita.

### Deferido ou rejeitado nesta versão

- portfólio de modelos e alegações comerciais não verificadas;
- substituição do motor por suposta geração mais nova;
- projeto de GPU/VRAM e modelos locais gigantes;
- fine-tuning antes de existir corpus classificado e avaliação estável;
- reconstrução da camada de dados;
- armazenamento de raciocínio interno irrestrito;
- votação entre modelos;
- números simulados para êxito processual;
- obrigação de revisão por fornecedor externo.

---

## 15. Entregáveis esperados após implementação

### Internos por caso

- árvore de questões;
- matriz de cobertura;
- grafo jurídico leve;
- identidade de eventos e termos;
- comparação documental, quando aplicável;
- maturidade de teses;
- testes próprios do caso;
- mapa intertemporal e cenários quantitativos, quando aplicáveis;
- protocolo e ledger científico, quando LCI aplicável;
- auditorias de consistência e metacognição;
- relatório de decisões Helena/Cícero;
- seleção da versão entregue e confirmação de integridade compatível com o canal;
- classificação do diff humano;
- métricas e trilha da execução.

### Externos

- petição limpa, sem marcações laboratoriais;
- quadro, tabela, gráfico ou diagrama apenas quando reduzir esforço cognitivo;
- fontes jurídicas e acadêmicas citadas com alcance calibrado;
- relatório de melhorias para o escritório;
- pacote de revisão com pendências reais e arquivos exatos.

---

## 16. Regra de promoção

A N4 só poderá tornar-se vigente quando:

1. a base N3 estiver comprovada nos termos do manifest atual;
2. os marcos do roadmap N4 tiverem evidência;
3. os testes em casos reais e replays não apresentarem regressão material;
4. as flags puderem ser desligadas sem corromper estado;
5. PRD, TDD, Roadmap, Diagramas, contratos, schemas, runbook e manifest forem atualizados na mesma promoção;
6. o sistema de gestão exibir corretamente os novos estados sem declarar cumprimento falso.

Até essa promoção, estes quatro documentos são o pacote de planejamento da candidata N4, e o manifest atual continua prevalecendo para execução.

---

## 17. Estado de execução em 11/07/2026

A arquitetura deste PRD foi implementada como candidata `N4.0-candidate`, sem substituir por presunção a especificação vigente. Estão ativos por flags: árvore de questões, cobertura, grafo de raciocínio, testes do caso, identidade terminológica, comparação documental, direito intertemporal, quantificação, evidência científica, metacognição, estratégia condicional, aprendizado, integridade de entrega e visão de gestão.

Uma auditoria posterior revogou corretamente o antigo piloto Cafelana: ele derivava de minuta cuja própria origem registrava invalidação por confusão entre o AREsp de 2024 e o AgInt de 2026. Cafelana permanece com 24/24 artefatos, mas bloqueada por fonte revogada até a obtenção da íntegra do AgInt da União de 24/06/2026, e-STJ fls. 938/949.

Patrícia/Fábio, Libra Sul e Saúde foram validados como **baselines retrospectivas**, não como ciclos prospectivos. Cada baseline possui 24/24 artefatos, zero P0, dois P1 de conselho, 10/10 testes, cobertura de mutação literal de 100%, rastreabilidade física reproduzível e QA visual automática por página. Como os textos finais já existiam antes das suítes, os três relatórios registram `promotionEligible=false`.

### Adendo do Conselho - 11/07/2026
A auditoria independente corrigiu a expressão acima. As três baselines preservam 24/24 artefatos, zero P0, 10/10 testes e 10/10 mutações **literais**, mas possuem dois P1 jurídicos cada: Helena não emitiu aprovação específica suficiente para uso final e Cícero rejeitou a versão corrente. O QA por página é automático e independente da geração, não revisão humana. Assim:

- `approved=true` significa somente baseline estrutural reproduzida;
- `legalReleaseStatus=human_review_required`;
- `promotionEligible=false`;
- mutação literal não prova preservação de sentido;
- liberação exige pareceres específicos, regimento registrado, citações materiais verificadas e entrega aplicável confirmada.

A operação permanece limitada a `pilot_blocking` nesses três baselines e em Cafelana. Ativar `default_on` retroativamente bloquearia estados legados e, sobretudo, promoveria evidência retrospectiva como se fosse prospectiva. A promoção futura exige suíte congelada e datada antes da produção final de ciclos novos.

---

## 18. Extensão metodológica PSO-Pet — 11/07/2026

A FORJA incorpora, em sombra, o perfil metodológico descrito em `14_METODO_VAN_AKEN_APLICADO_A_PETICOES.md`. A extensão não cria nova fase nem promove a N4. Ela explicita a petição como intervenção jurídico-processual projetada e acrescenta o seguinte requisito funcional:

### N4-R19 — Definição, diagnóstico e desenho da intervenção

Antes da redação detalhada, casos classificados como completos ou intensivos devem produzir:

1. definição verificável do problema jurídico-processual, distinta do comando recebido;
2. resultado direto pretendido, distinto do resultado final multicausal;
3. história diagnóstica que relacione causas, sintomas, consequências e explicações rivais;
4. requisitos funcionais, do destinatário, condições jurídicas e restrições negociáveis;
5. ao menos uma alternativa estratégica viável à solução preferida;
6. síntese-avaliação iterativa até uma arquitetura robusta;
7. validação da solução contra os requisitos e a melhor objeção;
8. plano de protocolo, acompanhamento e avaliação formativa.

O perfil leve aplica somente o núcleo necessário e não pode atrasar demanda simples. Durante o piloto, o roteiro `../templates/F4_METODO_SOLUCAO_PROBLEMA_PETICAO.md` é artefato interno de apoio, não gate automático e não fonte jurídica.

---

## 19. Adendo de compatibilidade com a base vigente — F7-B (15/07/2026)

Este PRD N4 permanece candidato e não reinterpreta seu planejamento original. Contudo, qualquer implementação futura da N4 deve herdar a subfase F7-B já incorporada à base vigente:

- depois de todos os gates jurídicos, factuais, científicos e adversariais F7 chegarem a zero P0, `forja_fable5.py` pode ser acionado explicitamente; o runner não o invoca de forma automática;
- Claude Code deve comprovar `claude-fable-5` e autenticação OAuth Claude Max, sem API key;
- a edição limita-se à forma. Nenhum fato, data, número, valor, autoridade, citação, marcador, ressalva, tese, conclusão, pedido, fecho ou assinatura pode ser alterado;
- `forja_editorial_fidelity.py` recompõe os gates de origem/hash, fidelidade, estilo humano e OAuth/modelo. O editor não valida o próprio trabalho;
- até três candidatas editoriais internas podem ser tentadas, sempre a partir do texto auditado original; elas não alteram o limite de quatro tentativas da fase;
- `FABLE5_RESULT` é incorporado ao `PHASE_RESULT` completo de F7; isoladamente não autoriza promoção;
- `final_markdown` aprovado é o cânone de F8 e dos pacotes novos, enquanto `audited_markdown` conserva a origem auditada.

Os módulos N4 podem acrescentar invariantes científicas e de consistência, mas não relaxar os invariantes F7-B nem transformar a revisão editorial em nova oportunidade de mérito.
