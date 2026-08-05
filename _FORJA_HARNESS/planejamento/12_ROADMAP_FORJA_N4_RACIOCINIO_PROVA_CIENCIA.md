# ROADMAP — FORJA N4: Raciocínio, Prova e Ciência

**Versão proposta:** N4.0  
**Data:** 2026-07-10  
**Status:** versão final do plano de implementação; execução não iniciada  
**Revisão do documento:** final-r2, após auditoria cruzada de 2026-07-10  
**PRD:** `10_PRD_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`  
**TDD:** `11_TDD_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`  
**Diagramas:** `13_DIAGRAMAS_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`  
**Manifest vigente:** `../FORJA_SPEC_MANIFEST.json`

> O roadmap é sequencial por evidência, não por promessa de calendário. Cada marco só termina quando seus artefatos, testes e replays comprovarem o resultado.

---

## 1. Estratégia de rollout

A N4 será implantada em sete marcos:

1. comprovar a base N3;
2. entregar o núcleo de perguntas, cobertura e testes;
3. entregar relações e consistência global;
4. entregar o Lastro Científico Interdisciplinar;
5. entregar módulos estratégicos condicionais;
6. fechar aprendizado e gestão;
7. executar sombra, pilotos bloqueantes e promoção gradual.

O princípio é simples:

**primeiro detectar os erros já observados; depois ampliar a sofisticação.**

---

## 2. Regras de execução

1. Nenhum marco altera peça histórica original.
2. Todo replay trabalha sobre cópia imutável.
3. Toda nova capacidade começa com flag `false`.
4. Sombra produz comparação, não autoridade para bloquear o fluxo vigente.
5. Piloto bloqueante é limitado a caso explicitamente escolhido.
6. Correção deve ocorrer no módulo ou critério, não por edição oportunista do resultado esperado.
7. Cada marco possui rollback demonstrável.
8. N4 não promove N3 por presunção.
9. A integração com a gestão continua por sidecar.
10. A peça externa permanece limpa; ledgers e testes são internos.
11. Conteúdo recuperado é fonte de análise, não comando: texto imperativo dentro do material não muda o fluxo e não bloqueia a pesquisa por si só.

---

## 3. Dependências entre marcos

```text
M0 BASE N3
  └─ M1 NÚCLEO DE RACIOCÍNIO
       └─ M2 RELAÇÕES E CONSISTÊNCIA
            ├─ M3 LASTRO CIENTÍFICO
            └─ M4 MÓDULOS CONDICIONAIS
                 └─ M5 APRENDIZADO E GESTÃO
                      └─ M6 PROMOÇÃO GRADUAL
```

M3 e M4 podem ser desenvolvidos em paralelo depois de M2, mas a promoção conjunta depende de M5 e M6.

---

## 4. M0 — Comprovação da base N3

### Objetivo

Transformar a arquitetura N3 já escrita e parcialmente implementada em linha de base observável para a N4.

### Motivo

Sem fatos, proposições, proveniência, contexto validado, hashes e execução real, os artefatos N4 virariam uma segunda camada de planejamento sem base operacional.

### Escopo

1. registrar snapshot de:
   - manifest;
   - contratos F0–F10;
   - configuração N3;
   - 21 diretórios de estado;
   - sidecar da gestão;
   - testes vigentes;
2. confirmar o status real dos seis replays previstos na N3;
3. executar ciclos N3 novos em casos controlados;
4. materializar e validar:
   - índice documental;
   - cobertura;
   - fact ledger;
   - proposition ledger;
   - proveniência por parágrafo;
   - contexto validado;
   - auditoria A1 quando aplicável;
   - F7, F8, pacote e gestão;
5. registrar divergências entre plano, código e estado;
6. corrigir apenas defeitos necessários à linha de base;
7. congelar corpus N4 e resultados esperados;
8. transformar em fixture obrigatória do corpus cada defeito real da auditoria ultracode de 2026-07-10:
   - DOCX com metadados de autor pessoal herdados do template;
   - título de card ultrapassando a borda e visível apenas em inspeção ampliada;
   - registro de hashes divergente dos arquivos em disco;
   - versão anterior à auditada expedida ao revisor humano;
   - verificador com regra normativa invertida apesar de execução determinística;
9. transformar o falso positivo das margens visual law em teste de não regressão: perfil visual aprovado não pode ser reprovado pelo padrão Word ordinário.

### Casos mínimos

- um caso responsivo;
- um caso com visual law complexo;
- um caso com documentos extensos;
- um caso em que a integração com a gestão tenha evidência de entrega.

### Entregáveis

- `N4_M0_BASELINE_INVENTORY.json`;
- `N4_M0_N3_REAL_CYCLES.md`;
- corpus imutável de fixtures;
- mapa de lacunas N3;
- plano de rollback;
- lista de defeitos que a N4 deve capturar.

### Testes

- replay reproduzível;
- zero alteração em originais;
- hashes coerentes;
- sidecar idempotente;
- A1 aplicável materializada;
- F7/F8 invalidados quando o arquivo muda;
- links por `artifactId` abrindo no painel.

### Critério de pronto

- a base N3 necessária à N4 existe em artefatos reais;
- lacunas restantes estão explicitamente aceitas ou bloqueadas;
- o corpus tem resultados esperados verificáveis;
- nenhum novo módulo N4 precisa inventar uma fonte de verdade ausente.

### Rollback

Nenhuma mudança de comportamento deve existir. Remover os relatórios de comparação do caminho do runner restaura o estado anterior; os snapshots permanecem como evidência.

---

## 5. M1 — Núcleo de raciocínio: questões, cobertura e TDD jurídico

### Objetivo

Criar a menor versão útil da N4: saber o que precisa ser respondido, provar que foi respondido e testar a peça pelos critérios do próprio caso.

### Escopo

1. criar schemas de:
   - classificação N4;
   - árvore de questões;
   - matriz de cobertura;
   - testes do caso;
   - resultados dos testes;
2. implementar `forja_reasoning.py` para perguntas e cobertura;
3. implementar `forja_case_tests.py`;
4. integrar F2, F4, F6 e F7 em sombra;
5. gerar 20–100 perguntas conforme complexidade, sem preenchimento artificial;
6. ligar pedidos, alegações, omissões e decisões a parágrafos da minuta;
7. congelar 10–25 testes antes da versão final;
8. impedir alteração silenciosa do teste;
9. registrar bloqueios materiais no sidecar temporário.

### Primeiras classes de perguntas

- identidade do processo, partes e tribunal;
- prazo e regime;
- fatos comprovados, declarados e inferidos;
- eventos processuais;
- pedidos próprios e adversários;
- resposta judicial anterior;
- precedentes decisivos;
- cálculo;
- objeção mais forte;
- fontes faltantes;
- visual necessário;
- LCI potencial.

### Entregáveis

- schemas JSON v1;
- módulos e validadores;
- contratos F2/F4/F7 candidatos v2, sem substituir os vigentes;
- fixtures positivas e negativas;
- relatório sombra por caso;
- documentação de versionamento dos testes.

### Testes essenciais

- pedido material sem resposta;
- questão material classificada como irrelevante sem justificativa;
- parágrafo sem item de cobertura;
- teste alterado após falha;
- hash da peça alterado depois dos testes;
- questão retirada sem histórico;
- caso simples sem inflar perguntas.

### Critério de pronto

1. toda questão material do piloto possui estado;
2. toda alegação/pedido material possui tratamento;
3. todos os testes bloqueantes são reproduzíveis;
4. mudança de critério invalida o resultado;
5. sombra encontra pelo menos os defeitos conhecidos do corpus;
6. casos simples não sofrem regressão de fluxo.

### Rollback

Desligar `n4QuestionTreeV1`, `n4CoverageMatrixV1` e `n4CaseTestsV1`. Os artefatos ficam fora do caminho vigente.

---

## 6. M2 — Relações, identidade e consistência global

### Objetivo

Impedir perda de sentido entre documentos, fases e versões da peça.

### Escopo

1. implementar grafo jurídico leve sobre IDs existentes;
2. criar identidade canônica de eventos e termos;
3. comparar documentos sucessivos por unidade argumentativa;
4. mapear alcance e limite de precedentes diretos/analógicos;
5. implementar verificador intertemporal;
6. implementar cenários objetivos de quantificação;
7. criar auditoria global F7;
8. integrar texto, quadros, diagramas, pedidos, relatório e e-mail;
9. criar hard negatives:
   - termo próximo, mas processualmente diferente;
   - precedente semanticamente próximo, mas juridicamente insuficiente;
   - DOI real de artigo incorreto;
   - argumento repetido com novidade material;
   - valor correto com data-base errada.

### Entregáveis

- `forja_consistency.py`;
- schema do grafo;
- schema da identidade de eventos;
- schema de comparação;
- schema intertemporal;
- schema de quantificação;
- F7 global consistency report;
- corpus de hard negatives.

### Pilotos indicados

- embargos sucessivos;
- peça em que “não conhecimento” e “rejeição” apareçam como risco;
- caso com precedente por analogia;
- caso com transição CPC/lei/regimento;
- caso com proveito econômico ou cálculo.

### Testes essenciais

- evento idêntico com labels incompatíveis;
- data divergente entre cronologia e pedido;
- tese subsidiária contradiz principal sem condição;
- precedente sustenta apenas uma subproposição;
- similaridade elevada tratada como triagem, não sanção;
- cálculo com variável sem fonte;
- ressalva perdida em tabela ou diagrama;
- e-mail declara “tudo conferido” com P0.

### Critério de pronto

1. zero referência órfã no grafo;
2. zero conflito terminológico material não explicado;
3. comparação documental separa repetição, novidade e possível prequestionamento;
4. precedentes têm alcance e limites registrados;
5. intertemporalidade usa ato e data comprovados;
6. quantificação é reproduzível ou declara impossibilidade;
7. consistência global detecta divergências entre todos os formatos.

### Rollback

Desligar flags de grafo, terminologia, comparação, temporalidade e quantificação. Nenhum ledger N3 é alterado.

---

## 7. M3 — Lastro Científico Interdisciplinar

### Objetivo

Permitir que a FORJA use conhecimento acadêmico de outras áreas como apoio sério, verificável e proporcional às teses jurídicas.

### Escopo

1. criar classificação `not_applicable | rapid | strict`;
2. implementar protocolo de busca;
3. criar adaptadores iniciais:
   - Crossref;
   - OpenAlex, quando houver chave/acesso disponível;
   - NCBI E-utilities/PubMed/PMC;
4. permitir busca manual registrada e encadeamento de referências;
5. deduplicar por DOI, PMID, título, autoria e ano;
6. verificar versão, revisão por pares e estado editorial;
7. criar ficha de estudo;
8. avaliar método por disciplina e proposição;
9. buscar evidência contrária;
10. criar síntese e mapa claim→evidência;
11. integrar citações científicas à proveniência do parágrafo;
12. auditar gráficos, tabelas e linguagem causal;
13. produzir relatório interno e citação externa limpa.

### Princípios de implementação

- metadado não prova conteúdo;
- artigo existente não significa pertinente;
- revisão sistemática ruim não recebe prioridade automática;
- estudo populacional não prova fato individual;
- associação não vira causalidade;
- ausência em uma base não prova inexistência;
- evidência contrária deve aparecer na síntese;
- PRISMA é referência de transparência no modo estrito, não ritual obrigatório no modo rápido.

### Primeiros domínios-piloto

1. psicologia/saúde comportamental;
2. medicina/saúde;
3. contabilidade/economia;
4. políticas públicas ou organização, se houver caso adequado.

### Entregáveis

- `forja_science.py`;
- adaptadores e cache bibliográfico;
- schemas F5C;
- fixtures de fontes válidas, divergentes, corrigidas e retratadas;
- modelo de síntese rápida;
- modelo estrito;
- gate científico F7;
- integração visual para tabelas/gráficos científicos.

### Testes essenciais

- DOI real para artigo errado;
- título semelhante com autores diferentes;
- preprint tratado como versão publicada;
- artigo retratado;
- correção relevante não considerada;
- estudo observacional com linguagem causal;
- amostra incompatível;
- resultado estatístico sem relevância prática;
- gráfico com eixo ou unidade alterados;
- evidência mista apresentada como consenso;
- ausência em OpenAlex tratada indevidamente como inexistência;
- base indisponível tratada como resultado negativo;
- artigo que estuda prompt injection contém texto imperativo e é falsamente bloqueado em vez de ser analisado como fonte.

### Critério de pronto

1. todas as referências-piloto têm identidade confirmada;
2. todas as frases científicas apontam para estudo e trecho/resultado adequado;
3. limites e evidência contrária estão registrados;
4. modo `not_applicable` funciona sem custo adicional;
5. modo `rapid` é reproduzível;
6. modo `strict` registra seleção e exclusões;
7. nenhum P0 científico do corpus passa;
8. falha de API degrada explicitamente sem falsa conclusão;
9. texto imperativo em fonte acadêmica não altera o fluxo nem produz falso bloqueio; anomalia técnica real continua registrada pelo scanner existente.

### Rollback

Desligar `n4ScienceEvidenceV1`; remover claims científicos candidatos da entrada F6; manter protocolo e ledger para auditoria.

---

## 8. M4 — Módulos estratégicos condicionais

### Objetivo

Integrar técnicas aprovadas que aumentam visão estratégica sem obrigar todos os casos a carregar a mesma complexidade.

### Módulos

#### 4A — Maturidade e contaminação de teses

- papel principal/subsidiário/reserva;
- força documental e jurídica separadas;
- melhor objeção;
- risco de contaminar tese superior;
- gatilho e veículo.

#### 4B — Ledger longitudinal de condutas

- dois polos;
- linha do tempo;
- `verified | partial | not_verified | contradicted`;
- correção posterior;
- frase externa autorizada;
- integração A1 e aprovação de Cícero para acusações.

#### 4C — Mapa de fatores decisórios

- requisito expresso em decisão;
- prova aceita/recusada;
- cautela;
- questão em aberto;
- consequência para a próxima peça.

#### 4D — Composição condicional

- interesses;
- não negociáveis;
- concessões;
- gatilhos;
- alternativa sem acordo;
- faixa qualitativa, sem probabilidade inventada.

### Entregáveis

- schemas e validadores;
- regras de aplicabilidade;
- integração aos pareceres Helena/Cícero;
- fixtures de tese forte contaminada por tese fraca;
- fixtures de conduta não confirmada;
- fixtures de decisão com critério explícito;
- fixtures de composição não aplicável.

### Critério de pronto

1. módulos não aplicáveis geram apenas justificativa mínima;
2. tese fraca não é promovida por retórica;
3. conduta não verificada não é externalizada como fato;
4. mapa decisório cita decisão e localizador;
5. composição não inventa vontade, número ou probabilidade;
6. Helena e Cícero registram decisões materiais e divergências.

### Rollback

Desligar `n4ConditionalStrategyV1`; blueprint N3 permanece válido.

---

## 9. M5 — Metacognição, aprendizado e gestão

### Objetivo

Fechar o ciclo entre produção, revisão humana, correção estrutural e painel do escritório.

### Escopo

1. implementar auditoria metacognitiva;
2. registrar origem das premissas;
3. medir independência real das fontes de concordância;
4. registrar por que uma recomendação mudou;
5. detectar manipulação de métricas;
6. classificar diff humano por causa;
7. criar fila de propostas de regressão;
8. exigir aprovação antes de transformar proposta em gate;
9. estender telemetria;
10. estender sidecar N4;
11. mostrar no painel:
   - N4 desligada/sombra/piloto;
   - cobertura material;
   - testes pendentes;
   - modo e estado LCI;
   - bloqueios;
   - próximo passo;
   - artefatos;
12. preservar regra de que rascunho não conclui demanda;
13. implementar a seleção pré-envio e a confirmação pós-entrega nos dois modos previstos pelo canal.

### Entregáveis

- `forja_metacognition.py`;
- `forja_learning.py`;
- classificação do diff;
- fila de testes propostos;
- extensão de métricas;
- extensão idempotente do sidecar;
- `F9_DELIVERY_SELECTION.json` e `F10_DELIVERY_INTEGRITY.json`;
- componentes do painel e links por `artifactId`;
- runbook de reabertura e aprendizado.

### Testes essenciais

- três agentes com uma fonte comum;
- instrução do usuário tratada como fato sem fonte;
- correção de estilo promovida indevidamente a regra jurídica;
- P0 escondido por 100% de cobertura numérica;
- refresh do painel perde estado N4;
- link com espaço/acento;
- dois casos atualizam sidecar simultaneamente;
- canal sem acesso ao anexo pós-envio confirma a entrega pela cadeia alternativa sem falso bloqueio;
- erro estrutural vira teste e impede reincidência.

### Critério de pronto

1. premissas têm origem e status;
2. consenso artificial é detectado;
3. mudanças estratégicas têm causa;
4. correções humanas são classificadas;
5. nenhum aprendizado vira regra sem teste;
6. sidecar é idempotente;
7. painel mostra bloqueio acima do percentual;
8. gestão e estado canônico não divergem;
9. versão entregue está ligada ao pacote por uma das duas cadeias válidas de evidência.

### Rollback

Desligar flags metacognitiva, aprendizado, integridade de entrega e gestão N4. O sidecar N3 continua e as propostas ficam arquivadas.

---

## 10. M6 — Sombra, pilotos bloqueantes e promoção

### Objetivo

Provar que a N4 melhora o resultado real sem criar regressões, burocracia vazia ou falsa confiança.

### Etapa 6.1 — Replay offline

Executar o corpus completo em cópias:

- comparar N3 versus N4;
- medir defeitos adicionais encontrados;
- medir falsos positivos;
- verificar tempo e volume de artefatos;
- eliminar perguntas e campos que não gerem decisão útil;
- corrigir módulo, não a história do caso.

### Etapa 6.2 — Sombra em casos novos

N4 produz relatórios, mas o fluxo vigente decide. Revisores humanos registram:

- achado correto;
- falso positivo;
- omissão;
- impacto real na peça;
- custo de revisão;
- módulo responsável.

### Etapa 6.3 — Piloto bloqueante

Ativar inicialmente apenas:

1. questão material sem resposta;
2. cobertura de pedidos;
3. identidade terminológica;
4. testes do caso;
5. citação científica inválida, quando aplicável;
6. consistência global.

Módulos estratégicos permanecem consultivos até acumularem evidência.

### Etapa 6.4 — Promoção gradual

Ordem sugerida:

1. árvore de questões;
2. cobertura;
3. testes do caso;
4. terminologia e consistência;
5. comparação/intertemporal/quantificação;
6. LCI;
7. metacognição/aprendizado;
8. módulos estratégicos condicionais.

### Casos mínimos de promoção

- pelo menos um caso responsivo completo;
- pelo menos um caso com LCI;
- pelo menos um caso quantitativo;
- pelo menos um caso longo com visual complexo;
- ciclos novos suficientes para demonstrar estabilidade, além dos replays.

O número final deve ser definido no relatório M6 com base na variedade e nos defeitos observados, sem reduzir o piso de três ciclos novos estáveis já exigido pelo manifest para a candidata N3.

### Critérios de promoção

1. zero P0 conhecido escapando no corpus;
2. zero regressão material em peça antes aprovada;
3. falsos positivos bloqueantes dentro do limite aprovado pelos revisores;
4. rollback comprovado;
5. todos os artefatos e hashes coerentes;
6. sidecar e painel idempotentes;
7. ganho demonstrado em cobertura, coerência ou detecção;
8. nenhum módulo obrigatório sem utilidade comprovada;
9. documentação e contratos correspondem ao código;
10. gate de expedição comprovado: hash do arquivo selecionado igual ao pacote auditado e registro reconciliado; após o envio, hash real quando o canal o fornecer ou `artifactId` + hash pré-envio + evidência externa nos demais canais;
11. promoção aprovada e manifest atualizado em operação única.

### Rollback

- desligar módulo ou N4 inteira;
- recalcular visão do painel;
- preservar eventos e artefatos;
- retomar N3/N2;
- abrir retrospectiva do defeito;
- nenhuma limpeza destrutiva.

---

## 11. Matriz consolidada de entregas

| Marco | Resultado principal | Bloqueia produção vigente? | Dependência | Esforço relativo |
|---|---|---:|---|---|
| M0 | baseline N3 real | não | manifest/N3 | M — depende do estado real dos 21 casos |
| M1 | perguntas, cobertura e testes | não, em sombra | M0 | G — núcleo da N4 |
| M2 | relações e consistência | não, em sombra | M1 | G — maior superfície de validação |
| M3 | LCI | não, em sombra | M2 | G — adaptadores externos e validação científica |
| M4 | estratégia condicional | não, em sombra | M2 | M — schemas e regras de aplicabilidade |
| M5 | metacognição, aprendizado e gestão | não, em sombra | M3/M4 | M — integra o que já existe |
| M6 | piloto e promoção | apenas casos escolhidos | M0–M5 | M — execução e medição, pouco código novo |

Esforço relativo (P/M/G) orienta priorização, não calendário: o roadmap continua sequencial por evidência.

---

## 12. Critérios de parada

Uma frente deve ser pausada quando:

- duplica artefato N3 sem ganho;
- cria mais revisão manual do que defeitos reais detectados;
- depende de dado que a FORJA não possui;
- produz falso positivo bloqueante recorrente;
- não possui fixture reproduzível;
- exige infraestrutura nova sem benefício demonstrado;
- altera fonte canônica para fazer o teste passar;
- enfraquece visual, prazo ou gestão já estáveis.

Pausa não cancela o roadmap inteiro. Isola-se o módulo e preserva-se o núcleo útil.

---

## 13. Backlog posterior à N4

Somente depois da promoção e de dados reais:

- busca científica monitorada por tema;
- banco local de fontes acadêmicas validadas;
- expansão para bases disciplinares específicas;
- recomendação automática de novos hard negatives;
- avaliações comparativas de modelos por tarefa;
- eventual indexação semântica local;
- eventual treinamento comportamental sobre corpus classificado;
- geração assistida de revisão sistemática formal.

Nenhum desses itens é requisito para a N4.

---

## 14. Definition of Done geral

A N4 estará implementada, e não apenas documentada, quando:

- a linha de base N3 estiver comprovada;
- os módulos existirem com schemas, flags e testes;
- os casos-piloto produzirem artefatos reais;
- defeitos conhecidos forem detectados;
- a pesquisa científica for verificável e calibrada;
- a consistência global alcançar peça, visual, relatório e e-mail;
- o painel refletir a realidade;
- rollback funcionar;
- a promoção atualizar todo o conjunto normativo;
- a revisão humana encontrar menos erros materiais sem receber burocracia inútil.

Até lá, o status correto é **candidata em planejamento, desenvolvimento ou sombra**, nunca “N4 implantada”.

---

## 15. Fechamento dos marcos em 11/07/2026

| Marco | Estado | Evidência |
|---|---|---|
| M0 | concluído | 21 estados inventariados sem alteração destrutiva; `N4_M0_BASELINE_20260711T000646.json` |
| M1 | concluído em sombra | perguntas, cobertura, testes congelados e regressões automatizadas |
| M2 | concluído em sombra | grafo, terminologia, comparação, intertemporal, quantificação e consistência global |
| M3 | concluído em sombra | piloto real Crossref + PubMed/PMC; OpenAlex degrada sem falso bloqueio quando indisponível |
| M4 | concluído em sombra | condutas, maturidade de teses, decisão, solução consensual e limites de uso externo |
| M5 | concluído | metacognição, classificação de correção humana, sidecar, painel e abertura de artefatos |
| M6.1 | concluído | corpus 11/11 e telemetria real com Word e documentos de produção |
| M6.2 | concluído como baseline | três casos reais com 24/24, zero P0/P1, QA integral e mutation score 100% |
| M6.3 | concluído com correção | CASO-19/Fábio, CASO-16 e Saúde validados retrospectivamente; CASO-04 revogada e bloqueada |
| M6.4 | pendente de ciclos prospectivos | os três textos antecedem os testes e, por isso, `promotionEligible=false`; `default_on` não promovido |

### Revisão M6.4 pelo Conselho - 11/07/2026
M6.4 continua pendente e ganhou critérios adicionais. Antes dos três ciclos prospectivos, o sistema deve provar: mutação semântica por famílias materiais; zero falsa aprovação P0 no corpus reservado; controles benignos com taxa de falso bloqueio publicada; pareceres Helena/Cícero específicos e anteriores ao produto final; regimento e citações materiais no ledger; e reexecução integral pelo agregador. Os três canários atuais possuem dois P1 de conselho cada e não servem como evidência de liberação jurídica.

Portanto, o estado final correto é **N4 implementada em modo piloto, com três baselines retrospectivas antifraude aprovadas, mas ainda sem os ciclos prospectivos exigidos para promoção geral**.

---

## 16. M6.5 — Piloto prospectivo do perfil PSO-Pet

### Objetivo

Testar se a definição explícita do problema, a história diagnóstica, a comparação de alternativas e a validação por requisitos reduzem erro e retrabalho sem burocratizar casos simples.

### Execução

1. selecionar três casos novos: um leve, um completo e um intensivo;
2. congelar o roteiro metodológico antes da redação final;
3. manter histórico das iterações e reaberturas;
4. comparar requisitos planejados com a peça e com as revisões humanas;
5. colher decisões separadas de Helena e Cícero;
6. registrar resultado direto e explicações rivais após entrega;
7. comparar retrabalho, perda de sentido e omissões com baselines anteriores.

### Critério de pronto

- três execuções prospectivas completas;
- zero falsa alegação de preenchimento anterior à redação;
- alternativa real examinada nos perfis completo e intensivo;
- utilidade reconhecida pelo conselho sem P0 novo causado pelo método;
- perfil leve sem aumento material injustificado de tempo;
- decisão documentada sobre manter em sombra, revisar ou promover itens específicos.

### Rollback

Remover a exigência do roteiro nos casos seguintes, preservando os três pilotos para análise. Nenhum artefato N2/N3/N4 existente é apagado ou reclassificado.

---

## 17. Trilha de compatibilidade obrigatória — F7-B vigente (adendo de 15/07/2026)

Este adendo não altera os sete marcos históricos nem afirma que a N4 foi promovida. Ele acrescenta uma condição de integração: qualquer marco que toque F7, F8, pacote ou replay deve preservar o F7-B implementado na base.

### Trabalho necessário em cada marco afetado

1. fixtures e replays devem produzir `audited_markdown`, passar F7 com zero P0 e então acionar `forja_fable5.py` explicitamente; não se deve pressupor chamada automática por `forja_run.py`;
2. a infraestrutura de teste deve comprovar Claude Code em OAuth Claude Max e modelo `claude-fable-5`, sem substituir a assinatura por API key;
3. gates N4 adicionais devem ser executados antes do editor e recompostos novamente quando dependerem do texto final; nenhum score N4 pode suplantar `editorial_fidelity` bloqueado;
4. `FABLE5_RESULT` deve ser mesclado ao `PHASE_RESULT` de F7 junto das saídas jurídicas, científicas e adversariais;
5. F8, F9, mutações e entrega devem selecionar `final_markdown` como cânone e manter `audited_markdown`, diff, relatório, uso e fidelidade como cadeia de auditoria;
6. o harness de retry deve testar separadamente três candidatas internas no total (inicial + até dois retries) desde a origem e até quatro tentativas externas da fase, comprovando que uma candidata rejeitada nunca vira base incremental;
7. testes negativos devem alterar, um por vez, fato, data, número, citação, autoridade, marcador, ressalva, título, pedido/fecho, origem operacional e hash, esperando bloqueio determinístico.

### Critério de pronto adicional

- zero promoção de fragmento isolado;
- zero pacote novo baseado apenas em `audited_markdown`;
- zero relaxamento dos limites semânticos pela N4;
- replays distinguem corretamente o contador editorial interno do contador da fase;
- falha de OAuth/modelo ou esgotamento das três candidatas bloqueia sem substituir a última versão válida.

### Rollback

Desligar funcionalidades candidatas N4 continua sendo o rollback da N4. O F7-B pertence à base vigente e não é removido por esse rollback; eventual retorno dele exige decisão normativa separada, mantendo os bundles já produzidos como evidência histórica.
