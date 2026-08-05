# FORJA — Auditoria adversarial e pontos decisivos

**Versão:** A1  
**Data:** 10/07/2026  
**Aplicação:** toda peça que responda, confronte ou dependa de alegações formuladas por parte adversária.

## 1. Finalidade

Acrescentar à FORJA uma investigação específica da peça adversária antes da definição da resposta. O objetivo não é multiplicar acusações, mas localizar erros raros e materialmente relevantes que possam alterar admissibilidade, prova, credibilidade, ônus, preclusão, competência, pedido ou resultado.

O protocolo procura, em especial:

1. julgados, temas, súmulas, normas ou trechos citados de modo inexistente, inexato ou descontextualizado;
2. contradições entre narrativa, pedidos, documentos, datas, valores e posições anteriores;
3. omissões que escondam fato ou documento capaz de alterar a solução;
4. indícios objetivos de alteração da verdade ou uso abusivo do processo;
5. pontos decisivos que, se confirmados, exijam mudança concreta da estratégia ou providência processual.

## 2. Regra de prudência

Resultado negativo de pesquisa não prova inexistência. A classificação correta é **“não localizado após diligência”**, acompanhada das consultas realizadas. A expressão “jurisprudência inexistente”, a imputação de falsidade e o pedido de sanção só podem aparecer em texto externo quando houver prova positiva ou diligência robusta, materialidade, base jurídica e autorização expressa de Cícero ou do revisor humano.

Perda anterior, tese rejeitada, recurso cabível ou interpretação jurídica discutível não constituem, isoladamente, má-fé. A auditoria deve testar a melhor explicação inocente e o risco de a acusação se voltar contra a própria peça.

### 2.1 Taxonomia jurídica de triagem

Nos processos sujeitos ao CPC, o indício deve ser relacionado, sem antecipar conclusão, a uma das hipóteses do art. 80:

| Hipótese a testar | Evidência mínima procurada |
|---|---|
| pretensão ou defesa contra texto expresso de lei ou fato incontroverso | norma ou fato incontroverso exato e demonstração de que a parte não apenas os interpretou de outro modo |
| alteração da verdade dos fatos | versões incompatíveis, fonte de cada versão, materialidade e elemento que afaste erro justificável |
| uso do processo para objetivo ilegal | finalidade concreta, nexo com o ato processual e vantagem ilícita pretendida |
| resistência injustificada ao andamento | ordem, ciência, possibilidade de cumprimento, atraso e ausência de justificativa |
| atuação temerária | risco processual conscientemente assumido ou culpa grave demonstrável, não simples tese malsucedida |
| incidente manifestamente infundado | ausência objetiva de fundamento e contexto que demonstre o caráter manifesto |
| recurso manifestamente protelatório | inadequação ou repetição, contexto temporal e elementos que revelem propósito de atraso |

A classificação interna sempre registra: `legalHypothesis`, conduta objetiva, materialidade, referências dos autos, hipótese inocente rival e tratamento recomendado. O art. 81 só entra na estratégia externa depois de Cícero confirmar cabimento, proporcionalidade e pedido adequado ao caso.

## 3. Funcionamento em três passagens

### F3 — Inventário e verificação

Artefato: `adversarial_audit`.

- confirmar leitura integral e mapear os pedidos adversários;
- inventariar todas as autoridades citadas, inclusive número, tribunal, relator, data, trecho, proposição atribuída e localização na peça;
- conferir existência, identidade, literalidade, contexto, vigência e aderência da proposição em fonte oficial;
- para “não localizado”, registrar ao menos dois canais oficiais distintos, consulta, data, endereço e resultado;
- confrontar fatos, datas, valores, anexos, pedidos e posições anteriores;
- registrar cada contradição pelos dois polos, fontes exatas e consequência possível;
- separar erro material, interpretação discutível, omissão estratégica, distorção objetiva e indício potencialmente sancionável.

### F4 — Decisão estratégica

Artefato: `adversarial_strategy`.

Cada achado recebe uma decisão registrada:

| Decisão | Quando usar |
|---|---|
| eixo central | o achado é provado, material e altera a solução |
| argumento subsidiário | o achado reforça, mas não sustenta sozinho, a resposta |
| pedir esclarecimento ou prova | falta elemento que a parte ou o juízo pode apresentar |
| preservar | o uso imediato prejudica oportunidade processual melhor |
| descartar | falso positivo, irrelevância ou risco maior que benefício |
| revisão humana obrigatória | possível acusação, sanção, fraude, falsidade ou risco ético |

Um “ponto decisivo” só existe quando contém: achado de origem rastreável, consequência jurídica, providência recomendada, forma de preservação, melhor explicação inocente e risco de reação. Helena avalia impacto, prioridade e efeito persuasivo. Cícero avalia juridicidade, prova, cabimento, ética e linguagem externa.

### F7 — Rechecagem adversarial

Artefato: `adversarial_recheck`.

O revisor tenta derrubar os próprios achados:

1. o precedente pode existir com outra grafia, classe, numeração ou base de pesquisa?
2. a frase é paráfrase mal sinalizada, e não citação inventada?
3. o trecho completo muda o sentido alegado?
4. a contradição admite conciliação razoável?
5. o fato atribuído à parte está realmente no documento indicado?
6. há nexo entre o erro e o pedido formulado?
7. a providência é proporcional e processualmente útil?
8. a linguagem externa foi autorizada quando acusatória?

Achado que não sobreviver à rechecagem é rebaixado ou removido.

## 4. Estados da verificação jurisprudencial

| Estado interno | Significado |
|---|---|
| `confirmed` | autoridade e proposição confirmadas em fonte oficial |
| `not_located_after_exhaustive_search` | não localizada após diligência documentada; não equivale a inexistência provada |
| `identifier_mismatch` | número, classe, tribunal, relator ou data não correspondem |
| `quote_mismatch` | texto entre aspas diverge da fonte |
| `proposition_mismatch` | fonte existe, mas não sustenta a proposição atribuída |
| `context_distortion` | recorte omite contexto que altera o sentido |
| `superseded_or_overruled` | autoridade superada, modificada ou sem vigência atual |
| `ambiguous` | resultado inconclusivo; não usar como acusação |

## 5. Escada de reação

1. corrigir silenciosamente a premissa na resposta;
2. demonstrar a inconsistência com fonte oficial;
3. pedir esclarecimento, juntada, desentranhamento ou valoração adequada, conforme cabimento;
4. explorar a perda de credibilidade apenas na medida necessária ao mérito;
5. formular pedido de sanção somente com tipicidade processual, materialidade, nexo, proporcionalidade e aprovação humana.

A FORJA não transforma automaticamente um indício interno em acusação protocolável.

## 6. Gates bloqueantes

- peça de resposta sem classificação de aplicabilidade;
- leitura integral ou pedidos adversários não confirmados;
- citação inventariada ainda pendente;
- divergência sem fonte oficial;
- “não localizado” sem dois canais oficiais documentados;
- contradição ou ponto decisivo sem fontes dos dois polos;
- estratégia sem decisão por achado;
- linguagem acusatória ou pedido sancionatório sem autorização humana/Cícero;
- F7 sem tentativa documentada de falso positivo;
- artefatos F3, F4 e F7 produzidos sobre versões diferentes da peça adversária.

## 7. Implementação

- módulo e comando: `forja_adversarial_audit.py`;
- prompt obrigatório: injetado por `forja_headless.py` em F3, F4 e F7;
- contratos: `phase_contracts/F3.json`, `F4.json` e `F7.json`;
- promoção de fase: validada por `forja_run.py`;
- pacote N3: validado e vinculado por hashes em `forja_package.py`;
- fechamento N2: `forja_delivery.py` exige `F3_AUDITORIA_PECA_ADVERSARIA.json` nas novas peças reconhecidas como responsivas;
- regressão: `test_forja_adversarial_audit.py` e caso específico em `test_forja_n3_package.py`.

Peças que não respondem manifestação adversária também geram classificação explícita `applicable: false`, com justificativa concreta. Peças históricas não são alteradas automaticamente.

## 8. Resultado esperado no trabalho jurídico

A resposta deixa de apenas rebater argumentos aparentes e passa a testar a confiabilidade estrutural da peça adversária. Quando existir um achado realmente decisivo, a FORJA deve entregá-lo com prova, consequência e providência. Quando não existir, deve registrar a investigação sem fabricar gravidade.
