# Plano do loop pós-protocolo e de autoaperfeiçoamento arquitetural da FORJA

**Versão:** 2.1, implementada, endurecida após três revisões adversariais no Claude Code Opus 5 e auditada em operação  
**Data:** 29/07/2026  
**Status:** implementação concluída; operação automática condicionada aos gates descritos neste documento  
**Escopo:** captura da peça humana final recebida por e-mail, prova de protocolo, comparação com a versão exata da FORJA, aprendizado controlado e aperfeiçoamento contínuo da arquitetura.

## 1. Resultado pretendido

Toda peça produzida com participação da FORJA deverá encerrar o ciclo com um pacote pós-protocolo verificável:

```text
<pasta do caso>/
└── PEÇA PROTOCOLADA — <NOME CANÔNICO DA PEÇA>/
    ├── PEÇA PROTOCOLADA — <NOME CANÔNICO DA PEÇA>.<docx|pdf>
    ├── ORIGINAL_RECEBIDO__<nome original>.<ext>
    ├── MUDANÇAS_IA_VS_PEÇA_PROTOCOLADA.md
    ├── DOCUMENT_COMPARISON_PRIVATE.json
    ├── PROVENIÊNCIA_E_PROTOCOLO.json
    └── sha256sums.json
```

Essa pasta local é privada e excluída do Git por regra testada. O arquivo original recebido fica imutável. O nome canônico facilita a navegação humana. O manifesto liga a cópia canônica ao anexo, à mensagem, ao caso, ao processo, ao hash e à versão exata da FORJA que foi enviada ao escritório.

O `F10_HUMAN_DIFF_CLASSIFICATION.json` permanece em `state/<caseId>/n4_artifacts/` como ledger sanitizado, sem texto integral. Ele referencia o diff privado por ID e hash.

O loop será automático em cinco tarefas: detectar, baixar, parear, comparar e propor aprendizado. A promoção de uma mudança para regra de futuras peças continuará controlada. Alteração humana isolada não se transforma silenciosamente em verdade jurídica, preferência universal ou mudança de arquitetura.

## 2. Premissas e decisões

1. **Não criar F11 nem renumerar a esteira.** O subsistema entra em `F10_ENTREGA_EVIDENCIA_APRENDIZADO`, que já possui `delivery_integrity`, `human_diff_classification` e `feedbackAssimilation`.
2. **“Final humana” e “protocolada” são estados diferentes.** Um anexo pode ser a versão final do escritório sem haver prova de protocolo.
3. **O comparando da IA não é “o arquivo mais novo”.** É o artefato selecionado em F9/F10 e entregue ao escritório, identificado por `artifactId` e SHA-256.
4. **O e-mail é origem e evidência operacional, não prova automática de conteúdo jurídico.**
5. **A edição humana não é infalível.** Mudança material só pode alimentar regra jurídica após validação contra autos, fontes oficiais e decisão humana registrada.
6. **Aprendizado começa no caso.** Ampliação para tipo de peça, tribunal, escritório ou global exige evidência crescente.
7. **Autoaperfeiçoamento de arquitetura gera candidatos, testes e ADRs.** Nunca altera produção por conta própria e não usa métricas de qualidade de petição como se medissem arquitetura.
8. **A implementação será aditiva.** Fachadas atuais continuam funcionando; não haverá reescrita ampla nem segundo repositório de verdade.
9. **O caminho atual ainda não foi provado com retorno real.** Os artefatos F10 humanos inspecionados estão sem conteúdo aplicável; a primeira execução será piloto controlado.

## 3. O que já existe e será reaproveitado

| Capacidade atual | Papel no novo loop | Limite atual a corrigir |
|---|---|---|
| `forja_diff_docx.py` | referência experimental e CLI manual durante a transição | não possui consumidor por import; entrada manual, alinhamento frágil, três classes excessivamente amplas, sem proveniência ou idempotência |
| `forja_learning.py` | gates de assimilação, autoria, escopo e promoção | valida payload pronto, mas não captura e não produz o payload |
| `F10_HUMAN_DIFF_CLASSIFICATION.json` | artefato estruturado do aprendizado | ainda não é produzido automaticamente a partir do retorno por e-mail |
| `forja_delivery_integrity.py` | liga pacote, artefato selecionado e entrega | precisa expor a versão-base exata ao comparador pós-protocolo |
| `forja_delivery.py` | fechamento F10 e evidência | hoje fecha entrega ao escritório; precisa registrar o ramo pós-protocolo sem confundi-lo com o limite de entrega do Igor |
| `APRENDIZADOS_FEEDBACK_HUMANO.md` | visão humana das lições promovidas | não deve receber colagem automática de achado ainda não revisado |
| `_MODELOS/LEIA-ME.md` | catálogo de melhores peças humanas | entrada ainda manual e sem score/proveniência uniforme |
| AutoResearch (`forja_ar_*`) | padrão de pré-registro, canários, revisão independente e aprovação humana | o manifesto atual é congelado e os indicadores medem peças; arquitetura exige linhagem separada |
| `FORJA_STATE.json` e eventos | trilha operacional por caso | faltam estados explícitos do pós-protocolo |
| painel do escritório | visão de demanda e evidência | faltam estados “versão humana retornou”, “protocolo verificado”, “diff pendente” e “lição promovida” |

## 4. Distinção obrigatória de estados

O sistema não poderá usar “protocolada” como rótulo genérico. O manifesto registrará:

| Estado | Significado | Pode usar o nome `PEÇA PROTOCOLADA`? |
|---|---|---|
| `human_final_received` | versão final humana recebida, sem afirmação de protocolo | não |
| `protocol_claimed` | mensagem humana afirma que a peça foi protocolada | somente com aviso `PROTOCOLO DECLARADO, NÃO VERIFICADO` |
| `protocol_verified` | há elo verificável entre processo, protocolo e conteúdo do arquivo submetido | sim |
| `identity_ambiguous` | há mais de uma peça/caso/versão plausível | não; quarentena |
| `not_a_petition` | anexo é minuta, relatório, comprovante ou material de apoio | não |

Para cumprir a nomenclatura desejada sem mentir, a pasta só recebe o nome definitivo depois de `protocol_verified`. Antes disso, usa:

```text
VERSÃO HUMANA FINAL — <NOME DA PEÇA>/
```

Quando a prova chega, a promoção de nome é atômica e preserva no manifesto todos os nomes anteriores.

## 5. Arquitetura proposta

### 5.1. Componentes

```text
Gmail em modo leitura
        |
        v
Adaptador Gmail existente, endurecido
        |
        v
ReturnCandidateDetector -----> Quarentena de ambiguidade
        |
        v
CaseAndArtifactResolver ------> F9/F10 + FORJA_STATE + demandas.json
        |
        v
ImmutableArtifactVault ------> original + hash + proveniência
        |
        v
ProtocolEvidenceVerifier ----> final recebida / protocolo alegado / verificado
        |
        v
DocumentComparisonService ---> diff estrutural, textual, jurídico e visual
        |
        v
LearningCandidateBuilder ----> MD humano + JSON estruturado
        |
        +------> Case Learning Ledger
        |
        +------> Learning Promotion Gate
                         |
                         +--> APRENDIZADOS_FEEDBACK_HUMANO.md
                         +--> fixtures/testes/gates/prompts
                         +--> _MODELOS/LEIA-ME.md
                         +--> Architecture Improvement Queue
                                      |
                                      v
                    AR-Architecture separado + ADR candidata
                                      |
                     shadow -> canário -> revisão independente
                                      |
                              aprovação humana
                                      |
                         promoção gradual / rollback
```

### 5.2. Direção de dependência

O núcleo de domínio não acessará Gmail, Word, disco ou painel diretamente.

```text
adapters/email, adapters/office, adapters/storage
                    |
                    v
application/post_protocol
                    |
                    v
domain/feedback + domain/protocol_evidence
                    |
                    v
contracts/schemas
```

Durante a migração, `forja_learning.py` e `forja_delivery.py` permanecem fachadas compatíveis. `forja_diff_docx.py` não tem consumidor por import: seu CLI manual permanece temporariamente por reversibilidade, mas será aposentado depois que o comparador novo provar equivalência nos pilotos. Novos módulos não importarão as fachadas de volta.

### 5.3. Pré-requisito arquitetural

Antes de iniciar a migração física deste subsistema, concluir ou estabilizar a onda W0 já priorizada em `00_MAPA_ARQUITETURA_IA/ANALISE_ARQUITETURAL_E_PROPOSTAS.md`: romper a dependência circular entre package e validação. O loop pós-protocolo não deve ampliar esse ciclo.

## 6. Fluxo operacional completo

### PP0. Descoberta do retorno

O adaptador consulta apenas mensagens elegíveis:

- remetentes e domínios autorizados do escritório;
- threads ligadas a demanda/caso existente;
- mensagens posteriores ao envio da versão da FORJA;
- anexos `.docx`, `.pdf`, `.odt` ou comprovantes de protocolo;
- marcadores semânticos como “versão final”, “protocolada”, “protocolo”, “peça ajustada”, usados somente como sinais, nunca como prova isolada.

Cada anexo gera duas chaves:

```text
contentKey  = sha256(caseId + attachmentSha256)
evidenceKey = sha256(accountId + threadId + messageId + attachmentId)
```

`contentKey` impede que o mesmo documento reenviado em nova mensagem ou thread gere cópia, diff ou aprendizado duplicado. `evidenceKey` preserva todas as mensagens que provaram a origem.

### PP1. Resolução de caso e identidade

O resolvedor não será um segundo matcher. Ele endurece e reutiliza as rotas existentes de Gmail/gestão, eliminando resolução conclusiva por termos de assunto. Usa, nesta ordem:

1. vínculo existente entre thread Gmail e `demandId/caseId`;
2. número CNJ completo;
3. `deliveryEvidence` e assunto da entrega;
4. tipo da peça, cliente e tribunal;
5. intervenção manual já registrada.

Resultado com menos de uma correspondência inequívoca vai para quarentena. Nome parecido nunca basta para vincular casos ou processos.

O falso positivo histórico Jalusa/WhatsApp será canário obrigatório: o retorno deve cair no caso correto ou em quarentena, nunca ser “resolvido” por semelhança textual.

### PP2. Seleção da versão-base da FORJA

O sistema lê `F9_DELIVERY_SELECTION.json`, `F10_DELIVERY_INTEGRITY.json`, package manifest e recibo de entrega. A base precisa satisfazer:

- artefato selecionado existe;
- hash recalculado coincide com o hash selecionado;
- evidência mostra que esse artefato, e não outro, foi entregue ao escritório;
- o tipo documental é comparável;
- entre múltiplas entregas, vale a última entrega comprovada anterior à mensagem de retorno;
- empate, versões concorrentes ou entrega sem hash produzem `ai_baseline_unresolved`;
- nenhuma versão posterior da IA é usada por conveniência.

Falha produz `ai_baseline_unresolved` e bloqueia o diff. O anexo humano ainda é preservado.

### PP3. Captura imutável e nomenclatura

O anexo é salvo primeiro com seu nome original e SHA-256. A cópia canônica recebe:

```text
PEÇA PROTOCOLADA — <TIPO> — <PROCESSO OU IDENTIFICADOR CURTO> — <DATA>.<ext>
```

Regras:

- não sobrescrever;
- conteúdo idêntico gera referência ao mesmo blob, não duplicação;
- mesmo nome com hash diferente gera `v02`, `v03`;
- nomes são sanitizados para Windows sem perder legibilidade;
- original, cópia canônica e manifestos têm hashes separados;
- a pasta inteira e o JSON privado são ignorados pelo Git;
- um teste reprova se vault, anexo ou diff integral aparecerem em `git ls-files`;
- anexos e conteúdo não entram no Graphify nem em telemetria.

### PP4. Verificação do protocolo

O verificador classifica a evidência:

- comprovante de protocolo com identificador externo, data, processo e identidade do arquivo;
- PDF com marca/rodapé de protocolo cujo conteúdo visível normalizado coincide com a final humana;
- mensagem explícita do advogado responsável, classificada como declaração;
- ausência ou conflito.

`protocol_verified` exige elo de arquivo: hash/tamanho/nome no comprovante ou igualdade do fingerprint textual-estrutural entre a final humana e a versão carimbada pelo tribunal. Processo, tipo e data apenas corroboram; não resolvem sozinhos. Sem elo de arquivo, o teto é `protocol_claimed`. Não será criada assinatura criptográfica nova apenas para dar aparência de rigor.

### PP5. Extração e normalização

O comparador produzirá duas representações:

1. **visível**, correspondente ao que o leitor vê;
2. **estrutural**, com headings, parágrafos, tabelas, notas, rodapés, imagens, campos, numeração, referências e revisões controladas quando existentes.

Para DOCX:

- ler Open XML, não apenas `python-docx`;
- detectar `track changes`, comentários, campos e texto em caixas;
- usar como cânone visível a versão com alterações aceitas; preservar a camada de revisão separadamente;
- comentários ficam no vault, mas não viram lição sem decisão humana explícita;
- preservar localizadores estáveis;
- renderizar por Word COM quando houver diferença visual relevante.

Para PDF:

- extrair texto com coordenadas;
- usar OCR apenas quando necessário;
- registrar confiança e páginas;
- bloquear classificação material quando o OCR não permitir comparação confiável.

Para comparação DOCX × PDF protocolado:

- remover da camada comparável carimbo, cabeçalho de tribunal e fólio adicionados externamente;
- alinhar por headings, numeração e fingerprint de blocos, não por página;
- suprimir conclusões de layout quando os formatos de origem forem diferentes;
- exigir golden específico antes de habilitar em caso real.

### PP6. Diff multicamada

Cada mudança preserva o campo canônico `cause` de `forja_learning.py` e recebe uma ou mais camadas ortogonais. Isso evita desligar silenciosamente gates existentes como `style_preference`.

| `layer` | Exemplos | `cause` provável |
|---|---|---|
| `format_layout` | fonte, espaçamento, paginação, fólio, tabela, figura | `visual` |
| `copy_style_voice` | concisão, ordem, cadência, vocabulário, tom | `style_preference` ou `terminology` |
| `fact` | data, nome, valor, evento, documento | `fact` |
| `procedural_identity` | processo, recurso, classe, órgão, cronologia | `fact` ou `reasoning` |
| `legal_rule` | norma, dispositivo, regime jurídico | `legal_rule` |
| `authority_citation` | precedente, trecho, ratio, pincite, tribunal | `citation_scope` ou `source_retrieval` |
| `reasoning` | premissa, inferência, nexo, objeção, distinção | `reasoning` |
| `request_relief` | pedido, subsidiariedade, extensão, efeito | `reasoning` |
| `evidence_annex` | anexo citado, localização, suficiência da prova | `missing_input` ou `source_retrieval` |
| `calculation` | fórmula, base, índice, período, quantum | `calculation` |
| `signature_protocol` | assinatura, OAB, data, metadado de protocolo | `delivery` |
| `unknown` | mudança ainda não classificável com segurança | `other`, bloqueada |

Classe ou `cause` desconhecida falha fechada. Teste de cobertura exige que toda nova `layer` tenha mapeamento explícito, inclusive para o gate anti-preferência-isolada.

Cada registro deve conter:

- `before` e `after` integrais no JSON privado;
- resumo sanitizado no Markdown;
- localizador nos dois documentos;
- classe, impacto `material|não_material|incerto` e confiança;
- fonte/lastro quando a mudança é material;
- origem intelectual com default `unknown`; mudança adicionada ou fortalecida não sobe acima do caso até a origem ser resolvida;
- `[INFERÊNCIA]` para intenção presumida;
- escopo máximo inicialmente permitido;
- sugestão de teste, gate, prompt ou nenhum ajuste;
- decisão do revisor.

O relatório não atribui intenção ao advogado a partir da edição. “Alterou porque preferiu X” é inferência até haver feedback explícito.

### PP7. Relatório humano

`MUDANÇAS_IA_VS_PEÇA_PROTOCOLADA.md` terá:

1. identidade dos dois artefatos e respectivos hashes;
2. grau da evidência de protocolo;
3. resumo executivo das alterações;
4. mudanças materiais primeiro;
5. fatos, autoridades, pedidos e cálculos alterados;
6. mudanças de estrutura, voz e visual;
7. itens mantidos pelo humano, para evitar aprender apenas com correções;
8. riscos e divergências que exigem revisão;
9. lições candidatas, com escopo e confiança;
10. decisões de promoção/rejeição e testes associados.

O Markdown é derivado do JSON privado e pode ser regenerado. O ledger F10 sanitizado contém apenas IDs, sínteses, classificações e hashes.

### PP8. Encerramento e painel

Os estados são eventos append-only com `expected_revision` e `idempotency_key`. `FORJA_STATE.json` recebe apenas a projeção derivada; o job de inbox nunca reescreve o estado inteiro.

```json
{
  "type": "post_protocol_diff_ready",
  "expectedRevision": 17,
  "idempotencyKey": "<contentKey>:diff:v1",
  "payload": {
    "humanArtifactId": "…",
    "aiBaselineArtifactId": "…",
    "protocolEvidenceId": "…",
    "diffArtifactId": "…",
    "openReasonCodes": []
  }
}
```

Eventos previstos: `candidate_detected`, `identity_ambiguous`, `captured`, `protocol_claimed`, `protocol_verified`, `ai_baseline_unresolved`, `diff_ready`, `review_pending`, `learning_proposed`, `learning_promoted` e `complete`.

O painel exibirá apenas:

- retorno humano detectado;
- protocolo não verificado/verificado;
- diff pronto;
- revisão pendente;
- lição promovida;
- código fechado de bloqueio e próxima ação.

Conteúdo da peça, trechos de e-mail, prosa livre de bloqueio e diferenças jurídicas não aparecem no painel.

## 7. Modelo de aprendizado

### 7.1. Ciclo, escopo e estágio de promoção

Não se criará um enum concorrente. O campo `status` mantém o contrato atual:

```text
observed | proposed | promoted | rejected
```

O alcance permanece em `scope`:

```text
case | product_type | tribunal | office | global
```

E a maturidade técnica fica em campo ortogonal:

```text
case_only
  -> evidence_repeated
  -> fixture_added
  -> test_passed
  -> independently_reviewed
  -> human_approved
  -> monitored
  -> retained | rolled_back
```

Regras:

- `scope=case` e `promotionStage=case_only`: automático e restrito ao caso;
- `scope=product_type|tribunal`: exige classificação humana ou duas ocorrências independentes;
- `scope=office`: exige no mínimo dois casos independentes, aprovação, fixture e teste;
- `global`: excepcional, com evidência em famílias distintas de casos e decisão explícita;
- preferência de estilo isolada nunca vira gate global;
- inferência implícita nunca se autopromove;
- mudança material precisa de fonte e decisão jurídica;
- conteúdo de origem desconhecida ou mista não pode ser atribuído como criação humana; mudança adicionada/fortalecida chega como `origin=unknown` e fica no caso até resolução;
- rejeições são registradas para impedir reapresentação cíclica sem evidência nova.

### 7.2. Quatro destinos possíveis

Uma lição confirmada deve ir ao destino mínimo correto:

| Tipo de lição | Destino |
|---|---|
| cautela jurídica recorrente | `APRENDIZADOS_FEEDBACK_HUMANO.md` + fixture + gate |
| padrão de peça de alta qualidade | `_MODELOS/LEIA-ME.md` + referência imutável |
| correção de comparador/processo | teste e módulo responsável |
| deficiência estrutural recorrente | fila de melhoria arquitetural + ADR candidata |

Não se deve transformar toda edição em prompt. Muitas correções pertencem a dado do caso, fonte, validador, template, integração ou arquitetura.

### 7.3. Métricas úteis

- cobertura de retornos: peças entregues com retorno detectado;
- percentual com identidade inequívoca;
- percentual com protocolo verificado;
- diffs ligados ao artefato exato entregue;
- mudanças materiais por classe;
- falso positivo/falso negativo do classificador, medido em amostra humana;
- tempo entre retorno e relatório;
- lições propostas, promovidas, rejeitadas e revertidas;
- redução de recorrência da falha em casos prospectivos;
- mudanças preservadas pelo humano, mas somente quando houver evidência de revisão, e não mera ausência de edição;
- danos evitados: pedido/fato/citação/processo corrigido antes de nova entrega.

Não usar como métrica primária “quantidade de parágrafos mudados” nem a queda bruta do percentual de mudanças. Menos mudança pode significar melhora, conformismo ou comparação defeituosa.

## 8. Loop de aperfeiçoamento da arquitetura

### 8.1. Geração de candidato

Um candidato arquitetural nasce quando:

- a mesma causa aparece em pelo menos dois casos independentes;
- há falha operacional com impacto material mesmo em ocorrência única;
- a correção exige coordenação entre três ou mais componentes;
- a solução local criaria duplicação, dependência circular ou estado concorrente;
- a telemetria sanitizada mostra retry, bloqueio ou intervenção manual recorrente.

O candidato registra:

- problema observável;
- evidências e casos, somente por IDs/hashes;
- componente responsável;
- hipótese de causa;
- alternativas;
- menor mudança coerente;
- contratos afetados;
- risco técnico/jurídico e rollback;
- critérios de sucesso e de rejeição.

### 8.2. Experimentação

O AutoResearch de peças não será modificado nem terá seu manifesto congelado reescrito. Uma linhagem separada, `AR-Architecture`, reutiliza somente os mecanismos genéricos que forem extraíveis sem alterar ciclos vigentes. Seu manifesto próprio mede arquitetura com indicadores determinísticos:

- SCC/ciclos de import;
- consumidores quebrados;
- contratos e suítes verdes;
- identidade de artefatos antes/depois;
- tempo e retries;
- capacidade de rollback.

Fluxo:

1. congelar baseline e manifesto;
2. criar patch ou configuração candidata em worktree;
3. rodar testes de contrato, regressões jurídicas e canários;
4. comparar artefatos antes/depois;
5. executar shadow replay em corpus permitido;
6. medir não inferioridade arquitetural com indicadores próprios;
7. produzir no máximo `estudo_descritivo` enquanto não houver sealed prospectivo próprio;
8. colher parecer independente de família diferente da geradora;
9. exigir aprovação humana vinculada ao hash;
10. manter qualquer promoção como decisão humana externa ao AR até o sealed existir; depois, promover gradualmente com flag e rollback.

### 8.3. Tipos de mudança e autoridade

| Mudança | Automação permitida |
|---|---|
| documentação derivada, painel e relatório | regenerar automaticamente após fontes canônicas mudarem |
| teste/fixture candidato | gerar e executar em isolamento |
| prompt/configuração | experimentar em shadow; promover só após gates |
| schema/contrato/API | proposta + compatibilidade + testes de consumidores |
| regra jurídica, liberação ou fonte | nunca promover sem revisão jurídica humana |
| mudança de arquitetura | worktree, ADR, benchmark, revisão independente e aprovação |
| remoção de fachada/dado | somente após inventário de consumidores, backup e rollback validado |

### 8.4. Monitoramento e rollback

Toda promoção registra versão, hash, casos de evidência, testes, aprovador, data e janela de observação. O rollback é automático somente para falhas técnicas objetivas previamente definidas; regressão jurídica bloqueia e exige decisão humana.

## 9. Contratos e artefatos novos ou alterados

### 9.1. Novos contratos

- `post_protocol_return.schema.json`
- `protocol_evidence.schema.json`
- `document_comparison.schema.json`
- `learning_candidate.schema.json`
- `architecture_candidate.schema.json`, pertencente à linhagem AR-Architecture

Todos nascem com envelope N4: produtor, revisor diferente, hashes, status, issues e política de promoção.

### 9.2. Extensões compatíveis

- `f10_delivery_integrity.schema.json`: expor o artefato-base exato;
- `f10_human_diff_classification.schema.json`: locadores, impacto, confiança, protocolo, versões e decisão;
- `phase_contracts_n4/F10.json`: tornar obrigatório o ramo pós-protocolo quando houver retorno elegível, sem bloquear o fechamento anterior do limite de entrega do Igor;
- event store: novos eventos `post_protocol_*`; `FORJA_STATE.json` recebe projeção;
- `FORJA_SPEC_MANIFEST.json`: registrar componentes, contratos e política de promoção;
- `AR_ARCH_MANIFEST.json`: manifesto separado, budgets e gates arquiteturais próprios; `AR_MANIFEST.json` vigente não é alterado.

Disciplina de geração: alterar primeiro `ARTIFACT_SPECS`, depois `ARTIFACT_CATALOG.json`, então `generate_n4_contracts.py`, schemas gerados, registry/validador e testes de igualdade do catálogo. Nenhum schema novo é editado isoladamente.

Os gates entram primeiro em `shadow`. Só bloqueiam quando o grupo for explicitamente promovido para `pilot_blocking`, com código incluído na lista bloqueante e teste que demonstre a transição.

### 9.3. Regra temporal importante

O fechamento da demanda por entrega ao escritório continua válido. O ramo pós-protocolo é uma obrigação de aprendizado posterior e possui estado próprio. A ausência de retorno humano não reabre artificialmente o trabalho já entregue por Igor, mas permanece visível como `postProtocol.not_detected`.

## 10. Controles operacionais concretos

1. Gmail será somente leitura; o loop não envia mensagens.
2. Anexos e diffs integrais ficam em pasta local ignorada pelo Git; teste objetivo impede rastreamento acidental.
3. Logs guardam IDs, hashes, contagens e reason codes, não trechos.
4. Documento recebido é tratado como dado, nunca como instrução.
5. Arquivos malformados, macros, links e conteúdo oculto passam por triagem.
6. Extração não modifica o original.
7. Conflito de identidade bloqueia; não usa similaridade de nome para resolver sozinho.
8. OCR de baixa confiança não sustenta classificação jurídica.
9. Mudança humana que cria ou altera fato, autoridade, valor, pedido ou identidade processual exige conferência na fonte.
10. O sistema nunca envia, assina ou protocola a peça.

## 11. Modos de falha e recuperação

| Código | Falha | Sinal | Recuperação |
|---|---|---|---|
| PP-01 | e-mail falso positivo | anexo sem vínculo inequívoco | quarentena; nenhuma renomeação |
| PP-02 | versão-base errada | hash não coincide com entrega | bloquear diff e reconstruir F9/F10 |
| PP-03 | declaração confundida com prova | só há frase “protocolada” | manter `protocol_claimed` |
| PP-04 | duplicação | mesma chave/hash reaparece | idempotência; apontar para registro existente |
| PP-05 | arquivo sobrescrito | nome igual, hash diferente | versionar e alertar conflito |
| PP-06 | extração incompleta | track changes, caixa, nota ou OCR ausente | trocar extractor; revisão humana |
| PP-07 | alinhamento semântico errado | parágrafos pareados sem relação | marcar `unknown`; não aprender |
| PP-08 | mudança material tratada como estilo | fato/pedido/citação alterado | classificadores determinísticos prioritários |
| PP-09 | autoria humana falsa | material importado/indeterminado atribuído ao advogado | novo gate de diff documental: `origin=unknown` por padrão e bloqueio acima do caso |
| PP-10 | preferência isolada vira regra | uma ocorrência promove gate | rejeitar promoção ampla |
| PP-11 | painel expõe conteúdo | trecho jurídico ou e-mail no JSON/HTML | sanitizar e falhar CI |
| PP-12 | arquitetura se autoedita | candidato escreve produção | worktree read/write isolada, produção read-only |
| PP-13 | promoção piora casos | canário/replay ou produção regressa | rollback e congelamento da linhagem |
| PP-14 | ausência de retorno trava demanda concluída | ramo pós-protocolo acoplado a `cumprida` | estados independentes |
| PP-15 | peça humana juridicamente pior | alteração sem lastro é assimilada | validar fonte; rejeitar ou limitar ao caso |

## 12. Testes e verificação

### 12.1. Diagrama de cobertura

```text
mensagem elegível
  ├─ sem anexo -> integração
  ├─ anexo duplicado -> idempotência
  ├─ caso único -> contrato + integração
  ├─ casos ambíguos -> negativo/fail-closed
  ├─ protocolo apenas declarado -> estado
  ├─ protocolo comprovado -> evidência
  └─ comprovante conflitante -> negativo

artefatos pareados
  ├─ hash da IA correto -> integração F9/F10
  ├─ hash errado/ausente -> negativo
  ├─ DOCX simples -> golden
  ├─ DOCX com tabelas/notas/track changes -> golden
  ├─ PDF textual -> golden
  ├─ PDF escaneado confiável -> OCR
  └─ OCR ruim -> bloqueio

mudanças
  ├─ formato -> classificação
  ├─ estilo -> classificação
  ├─ fato/processo/citação/pedido/cálculo -> regressão jurídica
  ├─ autoria importada -> anti-fraude
  ├─ intenção incerta -> inferência
  └─ preferência isolada -> não promoção

promoção
  ├─ caso -> automática restrita
  ├─ escritório/global sem evidências -> bloqueio
  ├─ com evidências, fixture, teste e aprovação -> promoção
  ├─ candidato arquitetural -> shadow/canário
  └─ regressão -> rollback
```

### 12.2. Suítes mínimas

- testes unitários de nomenclatura, hashing, idempotência e resolução;
- testes de contrato de todos os schemas;
- golden jurídico de caso com origem ativa e golden estrutural de Siqueira Campos;
- CASO-04 somente como poison/estrutura, marcada como origem revogada, nunca como referência jurídica;
- testes de DOCX com estruturas difíceis;
- golden DOCX × PDF com carimbo, fólio e cabeçalho de tribunal;
- canário Jalusa para falso pareamento Gmail/demanda;
- corrida concorrente de dois eventos no mesmo caso, com falha por `expected_revision`;
- reenvio do mesmo anexo em nova mensagem/thread, sem nova captura;
- duas entregas possíveis antes do retorno, com bloqueio por ambiguidade;
- teste de PDF/OCR e confiança;
- mutações adversariais em processo, pedidos, valores e autoridades;
- teste de cobertura `layer -> cause` com default deny;
- teste que reprova vault/diff integral em `git ls-files`;
- teste que reprova prosa livre no painel;
- testes de promoção do `forja_learning.py`;
- testes da linhagem AR-Architecture, separados do AutoResearch de peças;
- replay dos casos existentes;
- `forja_baseline.py`;
- régua integral e validação de consumidores;
- regeneração Graphify/Archify e inspeção visual após implementação estrutural.

### 12.3. Critérios de aceite do produto

1. Em todos os retornos históricos localizáveis e canários de ambiguidade, nenhum anexo é ligado ao caso errado.
2. Reexecução não cria duplicata.
3. Todo relatório identifica hashes e artefato-base.
4. Nenhum caso usa `PEÇA PROTOCOLADA` sem estado de evidência compatível.
5. Mudanças em fatos, processos, citações, pedidos e cálculos são detectadas nos canários.
6. Anexo/diff integral não entra no Git e conteúdo bruto não aparece em painel, mapa ou telemetria.
7. Preferência isolada não vira regra ampla.
8. Promoção ampla exige aprovação, fixture, teste e duas evidências independentes.
9. Ramo pós-protocolo não altera o status da entrega já concluída.
10. Rollback restaura configuração, contrato e comportamento anterior.

## 13. Roadmap de implementação

### Pré-onda. Estabilizar W0 arquitetural

**Saída:** romper o ciclo package ↔ validator já priorizado na arquitetura viva.  
**Gate:** zero SCC, testes de package/N4 verdes e artefatos equivalentes.

### Onda 0. Vocabulário, contratos e pilotos

**Saídas:** ADR, `cause/layer/scope/promotionStage`, `ARTIFACT_SPECS`, catálogo, gerador, schemas, reason codes, nomenclatura, eventos e fixtures.  
**Gate:** catálogos coerentes, enums fail-closed, gates em shadow e golden jurídico sem origem revogada.

### Onda 1. Isolamento local, event store e idempotência

**Saídas:** exclusões Git, teste `git ls-files`, eventos `post_protocol_*`, projeção e chaves de conteúdo/evidência.  
**Gate:** nenhuma escrita inteira concorrente de `FORJA_STATE.json`; corrida falha por revisão.

### Onda 2. Matcher endurecido e captura em shadow

**Saídas:** matcher Gmail/gestão existente endurecido, vault imutável e manifestos.  
**Modo:** detecta e simula destino; não renomeia casos reais.  
**Gate:** todos os retornos históricos localizáveis + canário Jalusa, zero pareamento incorreto e zero duplicação.

### Onda 3. Evidência e nomenclatura

**Saídas:** verificador de protocolo, pasta canônica e transição atômica de nome.  
**Gate:** casos declarados, verificados, ambíguos e conflitantes cobertos.

### Onda 4. Comparador multicamada

**Saídas:** extratores DOCX/PDF, alinhamento, JSON canônico e Markdown.  
**Gate:** DOCX×DOCX antes de DOCX×PDF; goldens com carimbo; OCR só na última subonda; mutações materiais e revisão humana de precisão/recall.

### Onda 5. Aprendizado controlado

**Saídas:** builder de candidatos, fila de revisão, atualização derivada de aprendizados e modelos.  
**Gate:** nenhuma autopromoção ampla; rejeição e proveniência preservadas.

### Onda 6. Painel e operação automática

**Saídas:** job recorrente, reason codes, estados sanitizados e alertas acionáveis.  
**Gate:** confirmar antes qual agendador e conta Gmail estão vivos; falha de Gmail degrada o ramo sem afetar a esteira principal.

### Onda 7. Loop arquitetural descritivo

**Saídas:** `architecture_candidate`, `AR_ARCH_MANIFEST.json`, ADR candidata, worktree, indicadores determinísticos, canários, revisão independente e rollback ensaiado.  
**Gate:** atingir `estudo_descritivo`; promoção permanece decisão humana fora do AR até existir sealed prospectivo próprio.

### Onda 8. Backfill seguro

**Saídas:** inventário de retornos históricos conhecidos.  
**Regra:** preservar nomes atuais; criar aliases/manifests, não reorganizar acervo em massa.  
**Gate:** cada item é `verificado`, `declarado` ou `ambíguo`; nenhum “protocolado” por inferência.

## 14. Ordem concreta de implementação por arquivo

1. Concluir W0 package ↔ validator.
2. Atualizar `ARTIFACT_SPECS`, catálogo, gerador, schemas, `FORJA_SPEC_MANIFEST.json` e contratos F10.
3. Isolar vault/diff do Git e criar testes de rastreamento.
4. Implementar eventos `post_protocol_*` com `expected_revision`.
5. Estender `forja_delivery_integrity.py` para expor a base exata.
6. Endurecer o matcher Gmail/gestão existente; não criar outro.
7. Criar captura/vault em shadow.
8. Substituir o domínio do comparador; manter apenas o CLI antigo até equivalência.
9. Integrar o produtor com `forja_learning.py` e os novos gates.
10. Integrar painel somente por reason codes.
11. Criar AR-Architecture separado.
12. Acrescentar fixtures, testes, baseline, runbook e documentação.
13. Regenerar mapas arquiteturais, validar HTMLs, consultar o grafo e atualizar hashes.

## 15. Fora do escopo

- protocolar ou assinar peças;
- enviar e-mail automaticamente;
- declarar que um anexo foi protocolado sem evidência;
- usar embeddings/RAG para substituir a leitura integral da peça-modelo;
- treinar modelo com acervo privado sem contrato específico;
- promover regra jurídica por votação de LLM;
- reorganizar todas as pastas antigas;
- remover fachadas atuais antes da migração e telemetria de consumidores;
- publicar peças, diffs ou anexos no GitHub;
- transformar estilo pessoal inferido em perfil psicológico.

## 16. Decisões autônomas registradas

| # | Decisão | Princípio | Alternativa rejeitada |
|---|---|---|---|
| 1 | incorporar em F10 | reutilizar contrato existente | criar F11 e renumerar a esteira |
| 2 | distinguir final humana de protocolada | evidência antes do rótulo | confiar no nome do arquivo |
| 3 | comparar com hash entregue | proveniência | escolher arquivo mais recente |
| 4 | preservar original e gerar cópia canônica | reversibilidade | renomear o único original |
| 5 | JSON canônico + Markdown derivado | auditabilidade e uso humano | somente relatório narrativo |
| 6 | caso primeiro, promoção gradual | menor autoridade necessária | aprender globalmente de uma peça |
| 7 | candidato arquitetural em worktree | isolamento e rollback | autoeditar produção |
| 8 | pós-protocolo não reabre entrega | separar limites operacionais | confundir Igor, escritório e tribunal |
| 9 | `layer` ortogonal a `cause` | preservar gates existentes | taxonomia nova que desarma validação |
| 10 | eventos com revisão esperada | concorrência segura | reescrever `FORJA_STATE.json` inteiro |
| 11 | AR-Architecture separado | medir a coisa certa | alterar o pré-registro do AutoResearch de peças |
| 12 | controle de conteúdo por Git ignore testado | evitar publicação acidental concreta | criar governança abstrata sem falha concreta |

### 16.1. Revisão adversarial independente

O plano v0.9 foi lido em modo somente leitura pelo Claude Code. O cliente confirmou o modelo canônico `claude-opus-5`, sessão `bc24f6f9-0c8b-4f29-80de-d2b10fc03c57`. O veredito foi `REPROVAR` a v0.9, preservando o eixo do produto.

Correções incorporadas:

- preservar `cause=style_preference` e separar `layer`;
- alinhar lifecycle, scope e estágio de promoção aos enums existentes;
- tratar origem de mudança documental como `unknown` por padrão;
- criar AR-Architecture separado;
- limitar o primeiro ciclo arquitetural a `estudo_descritivo`;
- usar event store com `expected_revision`;
- endurecer o matcher existente e incluir o canário Jalusa;
- normalizar DOCX × PDF carimbado;
- isolar vault/diff do Git com teste;
- corrigir idempotência, desempate de entregas, geração de schemas, track changes e reason codes;
- retirar CASO-04 do papel de golden jurídico.

Sugestões rejeitadas:

- criar recibo Ed25519 novo como requisito padrão de protocolo: substituído por elo de arquivo/fingerprint, mais simples e verificável;
- impor sanitização/autorização genérica à biblioteca interna `_MODELOS`: não houve falha concreta demonstrada e isso contrariaria a leitura integral hoje adotada;
- criar camadas genéricas sem falha concreta: mantidos apenas controles técnicos com teste reproduzível.

## GSTACK REVIEW REPORT

| Revisão | Revisor | Execuções | Estado | Achados |
|---|---|---:|---|---|
| Estratégia + engenharia | Claude Code Opus 5 | 1 | correções incorporadas | 6 críticos, 7 altos e 9 médios |
| Interface | escopo mínimo de painel | 0 | examinada no plano | estados, reason codes e ausência de conteúdo bruto especificados |

**Veredito final do plano:** v0.9 reprovada; v1.0 corrigida e pronta para decisão de implementação.

## 17. Critério final de “concluído”

O sistema estará realmente implantado quando uma peça real, recebida por e-mail após entrega da FORJA:

1. for detectada sem intervenção;
2. for ligada inequivocamente ao caso;
3. tiver original e cópia canônica preservados com hashes;
4. tiver o status de protocolo corretamente classificado;
5. for comparada à versão exata entregue pela FORJA;
6. gerar Markdown e JSON revisáveis;
7. produzir lições candidatas sem autopromoção indevida;
8. promover ao menos uma lição no menor escopo legítimo após teste e aprovação;
9. usar essa lição em nova peça e demonstrar, em ciclo prospectivo, que a falha não se repetiu;
10. gerar uma melhoria arquitetural candidata que percorra shadow, canário, revisão independente e rollback ensaiado, chegando a `estudo_descritivo`; promoção fica fora do AR até existir sealed prospectivo próprio.

## 18. Estado de implementação em 29/07/2026

Os dez critérios acima foram exercitados em execução real e prospectiva:

1. retorno real detectado no Gmail;
2. vínculo inequívoco com o caso;
3. original e cópia canônica preservados por hash;
4. estado corretamente mantido como `protocol_claimed`, pois não havia elo
   externo bastante para `protocol_verified`;
5. comparação feita contra o hash exato da versão entregue;
6. Markdown e JSON gerados;
7. candidatos produzidos sem autopromoção;
8. uma lição promovida no escopo `product_type`, após decisão, fixture e teste;
9. suíte prospectiva demonstrou aplicação da regra em nova peça compatível;
10. candidata arquitetural percorreu worktree isolado, shadow, canário, revisão
    independente e rollback, permanecendo no teto correto
    `estudo_descritivo`.

Evidências principais:

- `reports/POST_PROTOCOL_PROSPECTIVE_LEARNING_CANARY_20260729.json`;
- `reports/POST_PROTOCOL_CLAUDE_OPUS5_IMPLEMENTATION_REVIEW_20260729.md`;
- `reports/POST_PROTOCOL_CLAUDE_OPUS5_REREVIEW_20260729.md`;
- `reports/POST_PROTOCOL_CLAUDE_OPUS5_FINAL_APPROVAL_20260729.json`;
- `learning_registry/ACTIVE_RULES.json`;
- `ar_architecture/candidates/post-protocol-learning-loop-v1/ARCHITECTURE_CANDIDATE.json`.

A revisão adversarial inicial reprovou a implementação; a segunda confirmou a
correção dos críticos e encontrou a perda de decisões em reingestão; a terceira
aprovou sem achados críticos ou altos. Os achados médios e baixos remanescentes
também foram corrigidos antes do fechamento.

O caso real de Memoriais permanece deliberadamente como `protocol_claimed`.
Logo, sua pasta conserva o nome `VERSÃO HUMANA FINAL — ...`; o sistema não
inventa protocolo ausente. A automação horária executa o ciclo de forma
idempotente, preservando retornos sucessivos por `contentKey`.

**Veredito de implantação:** a FORJA possui loop pós-protocolo autoaperfeiçoável
controlado e loop arquitetural descritivo. Promoção de regra exige âncora humana
e teste prospectivo; promoção arquitetural continua fora do AR automático.

## 19. Fechamento operacional da execução

A auditoria final encontrou e corrigiu uma inconsistência de estado que não
afetava a regra ativa, mas enfraquecia sua representação: um candidato podia
estar `status=promoted` e `promotionStage=human_approved` enquanto conservava
`decision=pending`. O contrato agora exige e persiste:

```text
status=promoted  -> decision=approved
status=rejected  -> decision=rejected
```

A decisão é gravada em `F10_LEARNING_CANDIDATE.json` e na proposta correspondente
de `F10_HUMAN_DIFF_CLASSIFICATION.json`. Rebuilds normalizam promoções legadas
somente quando fixture e recibo verde continuam válidos; sem essas provas, o
candidato volta a `pending_revalidation`.

Verificações finais de 29/07/2026:

- caso real migrado com candidato e proposta `promoted/approved`;
- validadores do candidato e do human diff sem achados;
- regra `learn-b80a07dd026116a8` ativa para `memoriais de apelação`;
- suíte direcionada: 117 testes e 14 subtestes verdes;
- baseline canônico: 44 suítes, 517 testes, 60 subtestes e 7 regressões script,
  integralmente verdes;
- tarefa horária executada às 16:21:45, encerrou com código `0`, sem execução
  perdida e com próximo ciclo agendado para 17:21:44;
- camada v3 de interfaces regenerada sem falhas de parse, diagrama Archify
  validado sem erros ou alertas e hashes arquiteturais conferidos.
