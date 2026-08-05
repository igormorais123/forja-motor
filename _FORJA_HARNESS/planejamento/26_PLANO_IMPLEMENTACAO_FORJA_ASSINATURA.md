# Plano de implementação — FORJA‑ASSINATURA

> **RECLASSIFICADO EM 25/07/2026 — visão longa e backlog experimental, não roteiro de execução.**
> A tese deste plano permanece correta e o veredito adversarial Fable 5 de 24/07 (GO-COM-CONDIÇÕES) segue válido quanto a ela. O que foi retirado é a superfície: cinco a sete geometrias, três microbriefs, múltiplos drafts em produção, N-way, Condorcet, recall, memória decisória, pacote e CLI próprios, sete schemas e quinze ondas.
> **O roteiro vigente é `planejamento/35_ROADMAP_EXECUCAO_FORJA_ASSINATURA_LITE.md`**, derivado da arquitetura consolidada no documento 32. O PRD canônico é o documento 33 e o TDD canônico é o documento 34. Os documentos 27 e 28 permanecem como visão experimental de longo prazo.

**Protocolo proposto:** `FORJA-ASSINATURA-v1`  
**Data:** 24/07/2026  
**Estado:** plano revisado adversarialmente; `GO-COM-CONDIÇÕES`; não implementado  
**Predecessor:** `planejamento/25_GOSTO_JURIDICO_AUTONOMO_EDGE.md`  
**Pesquisa de base:** `C:\Users\IgorPC\Documents\FORJA_Valor_Unico_Memoravel_Research_20260724\FORJA_VALOR_UNICO_MEMORAVEL.md`  
**Revisão adversarial:** `reports/REVISAO_ADVERSARIAL_FABLE5_FORJA_ASSINATURA_2026-07-24.md`  
**Especificações de execução vigentes:** `planejamento/33_PRD_FORJA_ASSINATURA_LITE_COCRIACAO_PRECEDENTES.md` e `planejamento/34_TDD_FORJA_ASSINATURA_LITE_COCRIACAO_PRECEDENTES.md`  
**Regra de implantação:** aditiva, por ondas, sem renumerar F0–F10 e sem alterar o cânone jurídico por inferência editorial.

## 1. Decisão executiva

A FORJA‑ASSINATURA será uma camada de **busca, comparação e seleção argumentativa** anterior à auditoria factual final. Não será um prompt mais eloquente, um detector de “texto humano” nem uma licença para tornar a peça excêntrica.

O sistema deve:

1. reconstruir a identidade decisória do caso;
2. explicitar a solução mediana que deve ser superada;
3. gerar geometrias argumentativas ortogonais;
4. materializar o incumbente e desafiantes sob o mesmo snapshot;
5. eliminar qualquer candidato juridicamente inferior;
6. escolher, às cegas, somente quando houver superioridade demonstrada;
7. conservar o incumbente quando não houver vencedor;
8. registrar por que cada alternativa venceu, perdeu ou foi bloqueada;
9. registrar decisões calibradas sem realimentar os geradores em produção na v1;
10. entregar à F7 apenas um `draft_markdown` canônico.

Princípio central:

> **Divergir antes da redação; convergir somente depois da prova.**

Resultado esperado:

> A peça deve parecer a formulação necessária daquele processo, e não uma boa peça genérica da mesma categoria.

## 2. Autoridade, precedência e limites

Este plano não substitui:

- `FORJA_SPEC_MANIFEST.json`;
- os contratos em `phase_contracts/` e `phase_contracts_n4/`;
- `planejamento/05_FORJA_NIVEL_2_ANALISE_E_PLANO_CORRIGIDO.md`;
- `planejamento/22_PRD_AUTORESEARCH_FORJA.md`;
- `planejamento/23_TDD_AUTORESEARCH_FORJA.md`;
- `PROTOCOLO_FABLE5_ESCRITA_FINAL.md`;
- `RUNBOOK_LIBERACAO_JURIDICA_ESTRITA.md`;
- a ordem arquitetural de `00_MAPA_ARQUITETURA_IA/ANALISE_ARQUITETURAL_E_PROPOSTAS.md`.

Em caso de conflito, prevalecem:

1. invariantes jurídicos e de segurança;
2. manifesto e contrato de fase vigente;
3. decisões arquiteturais aceitas;
4. este plano;
5. prompts e documentação operacional derivada.

A autonomia proposta é de **produção e seleção textual**. Ela não converte a IA em fonte, advogado responsável ou autoridade de protocolo. A liberação jurídica externa continua obedecendo ao contrato vigente.

## 3. Diagnóstico de partida

### 3.1 O que já existe e deve ser reutilizado

| Necessidade | Componente existente | Uso autorizado |
|---|---|---|
| Contratos de fase | `forja_phase_contracts.load_contract()` | carregar contratos versionados e falhar fechado |
| Tentativa e promoção | `forja_run.prepare_attempt()` e `promote_attempt()` | manter tentativa isolada, hash e promoção canônica |
| Editor pós-F7 | `forja_fable5.run_editorial_pass()` | copiar o seam `invoke=` e manter F7‑B |
| Fidelidade editorial | `forja_editorial_fidelity.validate_editorial_bundle()` | preservar fatos, números, autoridades, pedidos e polaridade |
| Sinais de texto artificial | `forja_estilo_humano.analisar()` e `relatorio()` | sentinela negativa, nunca medida de excelência |
| Cegamento | `forja_ar_blind.canonicalize()`, `leak_scan()` e protocolo HMAC | reutilizar princípios, não a limitação binária |
| Não inferioridade | `forja_ar_indicadores.computar_indicadores()` e `comparar()` | vetor jurídico sem média compensatória |
| Execução pareada | `forja_ar_runpair.freeze_input()`, `register_manifest()` e `validate_pair()` | congelar input, ledgers, parâmetros e custo |
| Promoção experimental | `forja_ar_ciclo.snapshot()` e `promotion()` | endurecer antes de promover assinatura |
| Testes do caso | `forja_case_tests.validate_suite()`, `run_suite()` e `validate_results()` | congelar expectativas antes da redação |
| Mutação semântica | `forja_mutation_semantic.rodar()` | provar que gates percebem mudança material |
| Recibos humanos | validadores públicos de `forja_human_review.py` | criar recibo dedicado, sem reutilização imprópria |
| Memória sanitizada | disciplina de `forja_learning.py` | aprender decisões, não copiar peças privadas |

### 3.2 Lacunas comprovadas

1. As “três direções” do Fable existem apenas como declaração da mesma sessão.
2. Só um texto é materializado; alternativas não possuem artefato nem hash.
3. O próprio redator escolhe a própria versão.
4. F7‑B entra tarde demais para corrigir arquitetura argumentativa.
5. O gate de estilo mede ausência de vícios, não presença de qualidade.
6. A bancada cega atual aceita apenas dois lados.
7. I9 permanece desconectado do painel de indicadores.
8. `forja_ar_evolucao.py` pode desempatar aprovados pelo menor SHA, o que não mede qualidade.
9. `gostoJuridico` não é recomposto por `validate_editorial_bundle()`, promoção ou pacote.
10. Os artefatos de AUTO‑RESEARCH ainda não formam uma cadeia integralmente hash-bound.
11. O corpus possui 43 itens inventariados, mas somente sete artefatos pontuáveis.
12. O painel histórico não possui dados para I1, I3, I7, I8, I9 e I10.
13. Não existe schema dedicado a frase-mãe, geometrias, micropeças, independência, julgamento de assinatura ou decisão de seleção.
14. A Régua protege hashes, mas não executa toda a superfície comportamental relevante.

### 3.3 Estado de verificação em 24/07/2026

Foi executada a linha de base:

```powershell
python -m pytest -q `
  test_forja_fable5.py `
  test_forja_estilo_humano.py `
  test_forja_autoresearch.py `
  test_forja_run.py `
  test_forja_n4.py
```

Resultado observado: `131 passed, 3 subtests passed`.

A Régua, entretanto, está atualmente reprovada por alterações já existentes e ainda não rebaselinadas em arquivos de EDGE/Fable/estilo. A implementação da FORJA‑ASSINATURA não deve começar sobre esse baseline ambíguo.

## 4. Definição operacional de gosto jurídico

Gosto jurídico funcional é a capacidade de:

1. distinguir texto juridicamente correto de texto juridicamente correto e decisivamente superior;
2. explicar a escolha com âncoras verificáveis;
3. repetir o julgamento sob troca de posição e anonimização;
4. manter a preferência fora dos casos usados na calibração;
5. abster-se quando não houver diferença demonstrável;
6. aprender com rejeições sem sacrificar correção.

Não é:

- imitação de um autor;
- aumento de adjetivos;
- dramatização;
- novidade pela novidade;
- uniformidade estética;
- “probabilidade de ter sido escrito por IA”;
- média numérica capaz de esconder erro material.

### 4.1 Assinatura do caso

Cada caso deve possuir uma identidade decisória composta por:

```text
questão determinante
  + fato/prova que muda o resultado
  + regra ou limite aplicável
  + consequência processual
  + providência pedida
```

A “frase-mãe” deve responder:

> Por que este processo deve terminar desta maneira, diante desta prova e deste limite jurídico?

### 4.2 Memorabilidade juridicamente segura

Memorabilidade será medida como **recuperabilidade decisória fiel**, não como efeito retórico:

- qual questão deve ser decidida;
- qual âncora sustenta a resposta;
- qual regra ou limite governa;
- qual consequência decorre;
- qual providência é pedida.

Qualquer recordação falsa ou exagerada bloqueia o candidato.

## 5. Encaixe arquitetural

### 5.1 A tupla F0–F10 permanece intacta

Não criar `F6.5`, não renumerar fases e não introduzir nova fase canônica.

A camada será embutida em fronteiras existentes:

```text
F4 Blueprint estratégico
  └─ F4-S · identidade decisória e divergência estrutural
       ├─ frase-mãe
       ├─ mapa da versão óbvia
       └─ 5–7 geometrias
             ↓
F5 Pesquisa oficial
  └─ F5-S · grounding e seleção estratégica
       ├─ confirmação de lastro das geometrias
       ├─ 3 microbriefs estruturais independentes
       └─ shortlist de 2 estratégias
             ↓
F6 Redação
  ├─ F6-A · 2 drafts completos independentes
  │          └─ 3º draft somente em ambiguidade pré-registrada
  ├─ F6-B · seleção textual cega N-way
  └─ F6-C · promoção de um único draft
             ↓
draft_markdown + paragraph_provenance
             ↓
F7 Auditoria factual/jurídica
             ↓
F7-B edição local conservadora
             ↓
final_markdown → F8
```

### 5.2 Fronteiras de autoridade

| Camada | Pode | Não pode |
|---|---|---|
| F4‑S | formular estruturas com claims/ issues existentes | inventar tese, fato, fonte ou pedido |
| F5 | confirmar ou bloquear lastro | escolher estilo ou redigir peça completa |
| F5‑S | materializar microbriefs e selecionar estratégias lastreadas | transformar microbrief em petição |
| F6‑A | redigir candidatos completos | ver candidatos irmãos ou julgamentos |
| F6‑B | comparar candidatos cegos | criar conteúdo novo ou “corrigir” candidato |
| F6‑C | promover um único draft | levar variantes rejeitadas a F7 |
| F7 | auditar e corrigir juridicamente | escolher por beleza |
| F7‑B | editar localmente forma | reabrir frase-mãe, ordem das teses ou pedidos |
| F8 | materializar e validar visualmente | selecionar conteúdo |

### 5.3 Estrutura física-alvo

Para não acrescentar outro módulo monolítico à raiz:

```text
forja/
  signature/
    __init__.py
    contracts.py
    divergence.py
    candidates.py
    blind.py
    selection.py
    recall.py
    memory.py
    service.py
    adapters/
      model.py
      storage.py
forja_signature.py                 # fachada CLI fina e compatível
n4_schemas/
  f4_signature_map.schema.json
  f4_signature_geometries.schema.json
  f5_signature_shortlist.schema.json
  f6_signature_candidates.schema.json
  f6_signature_judgment.schema.json
  f6_signature_selection.schema.json
  f6_signature_recall.schema.json
test_forja_assinatura.py
```

Regras:

- módulos de domínio não leem rede, subprocesso, Word ou estado diretamente;
- adapters dependem do domínio, nunca o inverso;
- a fachada de raiz apenas traduz CLI e chama `service`;
- APIs privadas de Fable/runner não se tornam dependências;
- schemas entram no catálogo existente; não criar registry paralelo;
- se a proposta arquitetural P‑J01 ainda estiver pendente, concluí-la antes desta fatia ou registrar formalmente a dependência.

Registros vivos que precisam mudar de forma coerente:

- `forja_n4_common.ARTIFACT_SPECS`;
- `generate_n4_contracts.EXTENSIONS`;
- `generate_n4_contracts.SCHEMA_OVERRIDES`;
- `forja_n4_validate.VALIDATORS`;
- `forja_n4_validate.FLAG_FILES`;
- `forja_n4_invalidation.py`;
- `phase_contracts_n4/`;
- `n4_schemas/ARTIFACT_CATALOG.json`;
- `FORJA_N3_CONFIG.json`.

Catálogo, schemas e contratos N4 devem ser regenerados pelo gerador canônico, não editados como fontes paralelas.

### 5.4 Compatibilidade do rollout

O runner atual resolve apenas `requiredInputs`; não há contrato genérico de
`optionalInputs` ou `conditionalInputs`. O rollout terá três etapas:

1. **Sombra:** `forja_signature.py` opera como sidecar com caminhos explícitos,
   produz envelopes N4 em F4/F5 e não altera o `RUN_CONTEXT` de F6.
2. **Piloto bloqueante:** somente casos listados em `signature.pilotCases`
   exigem os artefatos de assinatura por `FLAG_FILES`/validação N4; o executor
   reutiliza a semântica condicional já implementada por
   `forja_n4_validate._effective_mode()` e prepara a tentativa F6 com a
   shortlist por caminho e hash explícitos. Casos fora da lista permanecem em
   sombra e não podem ser bloqueados pela feature.
3. **Default-on:** somente depois da prova prospectiva, `signature_shortlist`
   torna-se `requiredInput` formal de F6 para novas tentativas. Bundles históricos
   permanecem legíveis, mas não são tratados como evidência de assinatura.

Não adicionar imediatamente `signature_shortlist` ao contrato-base de F6, pois isso
eliminaria o rollout progressivo e quebraria novas tentativas ainda em sombra.

## 6. Contrato dos artefatos

Todos os artefatos devem conter:

- `schemaVersion`;
- `protocolVersion`;
- `caseId`;
- `attemptId`;
- `generatedAt`;
- `producerRunId`;
- hashes de entradas;
- versão do prompt/rubrica;
- identidade/família real do executor quando verificável;
- `releasePolicy: internal_working`, salvo o único `draft_markdown` promovido;
- `reasonCodes`;
- status explícito.

### 6.1 `F4_SIGNATURE_MAP.json`

Campos mínimos:

```json
{
  "schemaVersion": "FORJA-ASSINATURA-v1",
  "caseId": "...",
  "inputHashes": {
    "blueprint": "...",
    "factLedger": "...",
    "propositionLedger": "...",
    "issueLedger": "..."
  },
  "audience": {
    "decisionMaker": "...",
    "proceduralMoment": "...",
    "cognitionLimits": ["..."]
  },
  "motherSentence": {
    "text": "...",
    "claimIds": ["..."],
    "factIds": ["..."],
    "authorityIds": ["..."],
    "issueIds": ["..."],
    "requestedActionIds": ["..."]
  },
  "defaultMap": {
    "expectedGenericOpening": "...",
    "expectedGenericArc": ["..."],
    "transplantableRisks": ["..."]
  },
  "nonNegotiables": ["..."],
  "knownGaps": ["..."]
}
```

Gate:

- toda referência deve existir no ledger congelado;
- `knownGaps` nunca é convertido em afirmação;
- ausência de questão, âncora, consequência ou providência bloqueia F4‑S.

### 6.2 `F4_SIGNATURE_GEOMETRIES.json`

Deve conter de cinco a sete geometrias.

Eixos iniciais:

- causalidade factual;
- limiar ou condição processual;
- distribuição de ônus;
- cronologia e preclusão;
- coerência/contradição;
- aderência entre ratio e caso;
- proporcionalidade do remédio;
- consequência institucional;
- outro eixo, permitido apenas em sombra e com justificativa.

Cada geometria deve declarar:

- `geometryId`;
- `primaryAxis`;
- `coreQuestion`;
- `openingMove`;
- `argumentOrder`;
- `claimIds`;
- `factIds`;
- `authorityIds`;
- `issueIds`;
- `counterargument`;
- `response`;
- `decisionalConsequence`;
- `whyNotDefault`;
- `groundingStatus`;
- `rejectionReason`, se eliminada.

Diversidade válida exige eixos primários diferentes e ordens argumentativas materialmente distintas. Sinônimos ou novas metáforas não contam.

### 6.3 `F6_SIGNATURE_CANDIDATES.json`

Manifesto de candidatos:

```json
{
  "candidates": [
    {
      "candidateId": "candidate_0",
      "candidateRole": "incumbent|challenger",
      "stage": "full_draft",
      "geometryId": "...",
      "generationMode": "incumbent_pipeline|signature_challenger",
      "artifactPath": "...",
      "artifactSha256": "...",
      "inputSnapshotSha256": "...",
      "promptSha256": "...",
      "executor": {
        "family": "...",
        "model": "...",
        "sessionId": "...",
        "assurance": "envelope_verified|orchestrator_attested|self_declared"
      },
      "siblingAccess": false,
      "legalVectorPath": "...",
      "status": "generated|blocked|eligible|rejected|selected"
    }
  ]
}
```

O `candidate_0` é sempre a saída materializada do fluxo incumbente, executada
antes da comparação com o mesmo snapshot jurídico congelado, em sessão isolada
e sem artefatos de assinatura no prompt. Ele possui texto, caminho e hash; não é
o nome abstrato de um fluxo. Por padrão, o segundo draft é o melhor desafiante.
O terceiro draft só materializa o segundo desafiante quando o critério de
ambiguidade pré-registrado da shortlist é satisfeito.

Independência mínima:

- sessão nova por candidato;
- prompt sem texto de candidato irmão;
- mesmo snapshot jurídico;
- parâmetros registrados;
- família/modelo e nível de garantia registrados; `self_declared` nunca basta
  para gate bloqueante;
- `orchestrator_attested` exige que o orquestrador comprove sessões distintas e
  grave o hash de cada prompt sem texto irmão;
- retries corretivos não contam como candidatos.

Se só houver uma família disponível, registrar `correlatedCandidates=true`; o fluxo pode operar, mas não pode alegar independência entre famílias.

### 6.3-A `F5_SIGNATURE_SHORTLIST.json`

Artefato de transição entre estratégia e redação:

- hashes de `F4_SIGNATURE_MAP.json`, geometrias e `source_ledger`;
- três microbriefs independentes referidos por hash;
- vetor de grounding de cada microbrief;
- duas estratégias selecionadas para redação;
- rejeições e reason codes;
- abstenção quando nenhuma desafiante supera o incumbente; nesse caso, o
  artefato continua válido com `strategies: []` e
  `fallback: "candidate_0"`;
- hash da rubrica congelada;
- `supersedes`, quando houver revisão.

Microbrief é estrutura, não peça. Deve conter somente abertura, frase-mãe, ordem,
âncoras, contra-argumento e consequência. Não deve simular redação integral dentro
da fase de pesquisa.

### 6.4 `F6_SIGNATURE_JUDGMENT.json`

Cada voto deve conter:

- juiz, família e nível de garantia (`envelope_verified`,
  `orchestrator_attested` ou `self_declared`);
- `judgeIndependenceMode` efetivo:
  `cross_family|cross_session_same_family|unverified`;
- arquivos efetivamente lidos;
- declaração de isolamento;
- ordem apresentada;
- hashes dos bundles;
- candidato vencedor por hash;
- trecho-âncora literal;
- avaliação estruturada por dimensão;
- confiança;
- motivo de abstenção, se houver;
- flags de viés, vazamento ou conflito.

Dimensões:

1. `legalNonInferiority`;
2. `caseIdentity`;
3. `decisionalClarity`;
4. `groundedSpecificity`;
5. `counterargumentStrength`;
6. `faithfulRecall`;
7. `economy`;
8. `editorialHumanity`.

Uma dimensão estética nunca supera falha jurídica.

### 6.5 `F6_SIGNATURE_RECALL.json`

O teste será um gargalo de informação em duas execuções isoladas:

1. o **leitor** recebe apenas o corpo do candidato, após remoção determinística
   da síntese executiva, e produz cartão de até 80 palavras;
2. o **verificador** recebe apenas o cartão e o `F4_SIGNATURE_MAP.json`.

O cartão deve recuperar:

- questão;
- prova/âncora;
- regra/limite;
- consequência;
- providência.

O leitor não recebe o mapa dourado nem a síntese executiva. O verificador não
recebe a peça. A remoção usa marcador estrutural validado; se não for possível
identificar a síntese com segurança, o teste é inválido, não uma nota baixa.
Isso mede recuperabilidade do corpo, não memória humana real.

Gates:

- elemento falso: P0;
- providência ou questão ausente: candidato não pode vencer;
- cópia extensa ou cartão acima do limite: teste inválido;
- nomes e detalhes irrelevantes não compensam omissão decisória.

### 6.6 `F6_SIGNATURE_SELECTION.json`

Campos:

- snapshot e hashes dos candidatos;
- candidatos bloqueados e reason codes;
- matriz jurídica;
- matriz de comparações;
- swaps;
- consistência por juiz;
- vencedor estrutural;
- recall;
- decisão final;
- `winnerArtifactSha256`;
- identidade, snapshot e hash do `candidate_0`;
- `incumbentPreserved`;
- `abstained`;
- cadeia de evidências;
- hash anterior da memória decisória.

Estados:

```text
generated
→ legally_eligible
→ blind_preferred
→ selected_for_f7
→ audited_in_f7
→ finalized_in_f7b
```

“Vencedor na bancada”, “selecionado para F7”, “promovido como política” e “liberado juridicamente” são estados distintos.

### 6.7 Invalidação e reabertura

A decisão de assinatura é append-only. Nunca sobrescrever a anterior.

| Mudança observada | Invalida | Ação |
|---|---|---|
| `blueprint`, questão ou pedido | mapa, geometrias, shortlist e drafts | reabrir em F4‑S |
| `fact_ledger` ou `proposition_ledger` | toda a cadeia dependente | reabrir F4‑S |
| `source_ledger` ou autoridade | shortlist, drafts e seleção | reabrir F5 |
| decisão Helena/Cícero | geometria atingida e descendentes | reabrir F4‑S |
| rubrica/prompt/modelo | comparação e julgamento | nova tentativa, sem reaproveitar voto |
| candidato | recall, voto e seleção daquele hash | recomputar |
| alteração jurídica em F7 | conformidade com assinatura | classificar o diff e revalidar invariantes |
| alteração estrutural em F7‑B | bundle final | rejeitar F7‑B |

Para F7/F7-B, a detecção deve recompor invariantes determinísticos: frase-mãe,
sequência de `claimIds` por seção, teses, pedidos e polaridade. Mudança jurídica
corretiva é permitida, mas, se mudar eixo, ordem argumentativa ou providência,
invalida a seleção anterior e exige nova decisão; edição local insensível a
fronteiras de frase não invalida.

Usar eventos e revisão otimista de `forja_state_machine.py`; a memória armazena
`previousDecisionId`, `supersedes` e motivo, preservando as decisões antigas como
evidência histórica.

## 7. Algoritmo de seleção

### 7.1 Vetos jurídicos e preferência holística estável

O sistema não usa média única nem ordem lexicográfica sobre notas qualitativas
ruidosas.

```text
VETOS
1. Integridade jurídica e factual
2. Cobertura e cognoscibilidade
3. Segurança, proveniência e origem operacional

PREFERÊNCIA HOLÍSTICA ENTRE ELEGÍVEIS
4. Identidade do caso
5. Clareza decisória
6. Recuperabilidade fiel
7. Resistência ao melhor contra-argumento
8. Economia condicionada à cobertura
9. Qualidade editorial

ESTABILIDADE
10. Consistência sob swap, juízes e margem mínima
```

Falha em veto elimina o candidato; pontuação posterior não compensa. Entre
elegíveis, o juiz emite preferência holística acompanhada de âncora e dimensões
diagnósticas. Diferença abaixo da margem congelada, inconsistência sob swap ou
desacordo sem resolução pré-registrada produz abstenção.

### 7.2 Incumbente como candidato zero

O `candidate_0` é o texto integral produzido pelo fluxo vigente sob o mesmo
snapshot jurídico, materializado e hasheado antes do cegamento.

Regra:

- desafiante só substitui o incumbente se for não inferior em todas as dimensões jurídicas e superior de forma estável;
- empate, ciclo de preferência ou baixa confiança preserva o incumbente;
- ausência de vencedor não bloqueia a redação, salvo se todos os candidatos violarem gate jurídico;
- nunca escolher pelo menor hash.

### 7.3 Seleção N-way

A bancada atual A/B não será forçada a aceitar três lados.

Implementar protocolo N-way:

1. candidatos anonimizados e canonicalizados;
2. mapping HMAC fora do workspace;
3. permutações balanceadas;
4. preferencialmente dois juízes de famílias distintas, excluída a família
   geradora;
5. comparação por pares;
6. vencedor de Condorcet único;
7. ciclo ou desacordo relevante gera abstenção;
8. terceiro juiz somente sob regra pré-registrada;
9. razão e âncora persistidas por candidato.

Quando só uma família estiver disponível, o protocolo pode operar em
`cross_session_same_family` apenas com sessões novas, prompts de juiz disjuntos,
swap obrigatório e atestação do orquestrador. Esse modo é correlação declarada,
não independência entre famílias. O próprio gerador, a mesma sessão ou
`self_declared` geram abstenção obrigatória em modos bloqueantes.

No fluxo de custo reduzido:

- três micropeças disputam a shortlist;
- o incumbente e a melhor desafiante geram os dois drafts padrão;
- a segunda desafiante só gera o terceiro draft se a margem da shortlist ficar
  abaixo do limiar pré-registrado antes da redação.

## 8. Questões essenciais que o sistema deve responder

Antes de redigir:

1. Qual é a questão que realmente decide o caso?
2. Qual fato ou prova muda o resultado?
3. Qual é o limite jurídico que impede a solução contrária?
4. O que o julgador pode considerar neste momento processual?
5. Qual providência concreta decorre da cadeia?
6. Qual seria a redação óbvia e intercambiável?
7. Que trecho sobreviveria se nomes, datas e números fossem trocados?
8. Qual é o melhor argumento contrário?
9. Qual consequência humana, institucional ou processual já está provada?
10. Que conteúdo é obrigatório e não pode ser sacrificado por concisão?

Depois de redigir:

11. O primeiro movimento da peça revela a fricção real ou começa com prefácio genérico?
12. Cada seção decisiva liga proposição, âncora e consequência?
13. A hierarquia textual corresponde ao peso jurídico das teses?
14. A versão vencedora permanece vencedora com posição invertida?
15. O cartão de recuperação reconstrói o caso sem inventar?
16. O ganho veio da estrutura ou de comprimento/adjetivação?
17. A F7‑B preservou a geometria selecionada?

## 9. Ondas de implementação

Cada onda é uma entrega independente. Nenhuma onda posterior começa com testes ou contratos da anterior em vermelho.

### Onda 0 — Estabilizar a linha de base

**Objetivo:** tornar o ponto de partida reproduzível.

Implementar:

1. revisar as alterações EDGE/Fable/estilo já presentes;
2. decidir quais são legítimas;
3. executar as suítes vivas;
4. rebaselinear a Régua somente após revisão;
5. registrar hash do baseline;
6. corrigir a contagem documental de testes, sem hardcode de quantidade;
7. confirmar o estado de P‑J01 da arquitetura.

Arquivos:

- `REGUA_MANIFEST.json`;
- `DOCUMENTACAO_TECNICA.md`;
- `docs/TESTING.md`;
- relatório novo em `reports/`.

Aceite:

- suíte atual verde;
- Régua verde ou desvio explicitamente bloqueante;
- lista exata de arquivos alterados;
- nenhum caso real modificado;
- baseline hash-bound.

Rollback:

- não há mudança de produção;
- rebaseline sem revisão é proibido.

### Onda 1 — Contratos, schemas e tipos puros

**Objetivo:** definir o idioma executável da assinatura antes de qualquer chamada a modelo.

Implementar:

- pacote `forja/signature/`;
- schemas da seção 6;
- validadores públicos;
- catálogo de artefatos com owner, fase, validator e política;
- reason codes versionados;
- `FORJA_SIGNATURE_CONFIG` com modos `off|shadow|pilot_blocking|default_on`;
- fachada `forja_signature.py`.

Não alterar ainda F4/F6.

Testes:

- schema válido/inválido;
- referências inexistentes;
- hash divergente;
- geometria duplicada;
- contagem fora de 5–7;
- decisão sem evidência;
- tentativa de autopromoção;
- `candidate_0` sem texto, snapshot ou hash;
- booleano `verified` usado como prova;
- caso fora do piloto bloqueado por artefato de assinatura ausente;
- caso dentro do piloto aceito sem artefato obrigatório;
- perfil de orçamento sem limites numéricos congelados.

Aceite:

- todos os contratos falham fechados;
- nenhum booleano de modelo vale como prova;
- módulos de domínio sem I/O;
- APIs públicas documentadas;
- nenhum registry paralelo;
- modo efetivo por caso reutiliza a semântica de `pilotCases` do N4;
- memória de produção está contratualmente `write_only`;
- perfil de orçamento contém limites numéricos antes da primeira geração.

### Onda 2 — F4‑S: mapa decisório e divergência

**Objetivo:** produzir arquitetura antes da prosa.

Implementar:

- geração de `F4_SIGNATURE_MAP.json`;
- taxonomia de eixos;
- geração de 5–7 geometrias;
- diversidade computável por `primaryAxis` e distância mínima pré-registrada
  entre as sequências de `claimIds`/`argumentOrder`;
- filtro determinístico de referências;
- teste de transplante diagnóstico;
- registro da versão óbvia.

Integração inicial:

- modo sombra;
- artefatos não alteram o `blueprint`;
- sem efeito em F6.

Testes:

- mesmos inputs geram envelope reproduzível;
- geometria não pode referenciar ID ausente;
- paráfrases da mesma arquitetura não contam como diversidade;
- `knownGaps` não aparece como fato;
- conteúdo injetado nos autos não vira instrução.

Aceite:

- pelo menos cinco geometrias materializadas;
- todas possuem eixos/ordens identificáveis e diversidade computável;
- zero tese ou autoridade nova;
- todos os artefatos vinculados por hash ao blueprint e aos ledgers.

Checkpoint antes da Onda 3:

- executar F4-S em sombra sobre corpus congelado de casos reais já entregues;
- aplicar regra amostral pré-registrada por linhagem e produto;
- medir mudança material de arquitetura, não apenas de léxico;
- não avançar se as geometrias forem predominantemente paráfrases.

A avaliação humana calibra a política e o corpus histórico; ela não é requisito
por petição quando o sistema chegar a `default_on`.

### Onda 3 — F5: filtro de lastro

**Objetivo:** impedir que uma geometria elegante avance sem fonte.

Implementar:

- ligação entre geometrias e `source_ledger`;
- status `grounded|partially_grounded|blocked`;
- retorno controlado a F4‑S quando fonte decisiva falhar;
- checklist de autoridades por geometria.

F5 continua pesquisa. Não redige e não escolhe por estilo.

Testes:

- fonte removida bloqueia geometria dependente;
- fonte substituída altera hash e invalida shortlist;
- citação não confirmada não pode virar mero aviso;
- distinção entre “não localizado” e “não existe”.

Aceite:

- nenhum candidato F6 nasce de geometria bloqueada;
- source ledger permanece canônico;
- nenhuma consulta externa é feita pelo domínio.

### Onda 4 — F5‑S: microbriefs e shortlist estratégica

**Objetivo:** materializar três estratégias curtas, já lastreadas, antes de pagar o custo de drafts completos.

Cada micropeça deve conter:

- abertura;
- frase-mãe;
- ordem dos capítulos;
- parágrafo decisivo;
- melhor objeção;
- resposta;
- pedido/consequência;
- IDs de lastro.

Implementar:

- uma sessão por micropeça;
- isolamento entre candidatas;
- manifest de execução;
- custo e tokens;
- filtro jurídico preliminar;
- shortlist N-way;
- margem da shortlist calculada sob regra congelada;
- `F5_SIGNATURE_SHORTLIST.json`;
- envelope N4 atribuído a F5;
- sidecar explícito no modo sombra.

Testes:

- sessão repetida não conta como independência;
- candidato com acesso a irmão é inválido;
- retry não vira novo candidato;
- modelo/família não verificados reduzem confiança;
- rótulos ou nomes de variante no texto causam leak.

Aceite:

- três artefatos independentes;
- mesmo snapshot jurídico;
- todos os IDs resolvidos;
- shortlist reproduzível por hash;
- somente a melhor desafiante segue por padrão; a segunda fica elegível apenas
  quando o critério objetivo de ambiguidade for satisfeito;
- abstenção gera fallback válido para `candidate_0`;
- F5 não produz petição completa.

### Onda 5 — F6‑A: drafts completos

**Objetivo:** redigir somente as arquiteturas com chance real de vencer.

Implementar:

- dois drafts completos por padrão: `candidate_0` e melhor desafiante;
- terceiro somente quando a margem da shortlist estiver abaixo do limiar
  congelado antes da geração;
- `paragraph_provenance` por candidato;
- execução dos gates jurídicos e de estilo em cada candidato;
- preservação do candidato zero.

Testes:

- remoção de conteúdo obrigatório elimina candidato;
- adição de autoridade não prevista elimina candidato;
- aumento de certeza elimina candidato;
- vazamento operacional elimina candidato;
- draft irmão não pode aparecer no prompt;
- P1 de estilo é registrado; P0 bloqueia.

Aceite:

- nenhum draft com P0 jurídico ou veto preliminar chega à comparação editorial;
- custo registrado por candidato;
- candidato zero sempre recuperável, com texto, snapshot e hash próprios.

### Onda 6 — F6‑B: cegamento e preferência preliminar

**Objetivo:** formar a matriz cega e a preferência preliminar sem conhecer
autor, família ou ordem original. Ainda não promover `draft_markdown`.

Implementar:

- mapping externo HMAC;
- canonicalização N-way;
- permutações balanceadas;
- voto estruturado;
- validação de família;
- registro do `judgeIndependenceMode` efetivo;
- Condorcet/abstenção;
- `F6_SIGNATURE_JUDGMENT.json`;
- estado máximo `blind_preferred`, condicionado aos gates da Onda 7.

Endurecer antes:

- ligar julgamento, candidatos, runpair e snapshot por hash;
- recomputar hashes no momento da decisão;
- não confiar em `judgeFamily` declaratório quando envelope real existir;
- impedir que `exit 0` seja interpretado como promoção;
- impedir `selected_for_f7` antes de recall e steelman;
- degradar com transparência para `cross_session_same_family` quando não houver
  segunda família, sem alegar independência entre famílias.

Testes de sabotagem:

- troca de rótulo;
- troca de posição;
- mapping adulterado;
- mapping vazado;
- juiz gerador;
- mesma sessão gerando e julgando;
- `self_declared` usado em gate bloqueante;
- família falsa;
- arquivo não declarado;
- âncora inexistente;
- bundle modificado;
- ciclo A>B>C>A;
- dois aprovados;
- tentativa de desempate por SHA;
- juiz fora do schema;
- decisão sem snapshot.

Aceite:

- preferência preliminar somente por hash;
- empate/ciclo marca abstenção preliminar;
- nenhuma candidata rejeitada chega a F7;
- razões das rejeições persistidas;
- nenhum `draft_markdown` promovido nesta onda.

### Onda 7 — Recuperabilidade, steelman e F6‑C

**Objetivo:** medir se a peça torna a decisão cognitivamente disponível sem
falsear e, somente então, emitir a seleção final.

Implementar:

- leitor isolado;
- remoção determinística da síntese executiva;
- cartão de 80 palavras;
- verificador contra mapa decisório;
- melhor contra-argumento;
- teste de resposta;
- canários contra stuffing;
- `F6_SIGNATURE_RECALL.json`;
- `F6_SIGNATURE_SELECTION.json`;
- promoção de exatamente um hash elegível para `draft_markdown`.

Testes:

- cartão copia mais do que o limite;
- questão ausente;
- providência errada;
- âncora falsa;
- regra trocada;
- nomes corretos com relação causal errada;
- repetição de palavras-chave sem nexo;
- texto longo não ganha por volume;
- síntese executiva ainda presente no input;
- síntese não identificável com segurança.

Aceite:

- zero elemento falso;
- questão e providência recuperadas;
- resultado ligado ao hash do candidato;
- métrica declarada como proxy, não memória humana comprovada;
- desafiante só alcança `selected_for_f7` depois de recall/steelman;
- falha, empate ou baixa margem promovem exatamente `candidate_0`.

### Onda 8 — F7 e F7‑B conservadora

**Objetivo:** preservar a arquitetura vencedora durante auditoria e edição final.

Implementar:

1. F7 recebe somente `draft_markdown` vencedor.
2. F7 registra mudanças jurídicas separadamente.
3. F7‑B deixa de escolher direção retórica.
4. F7‑B edita frase, transição, concisão e vocabulário.
5. Reordenação estrutural, fusão ampla e nova geometria tornam-se bloqueadas.
6. `validate_editorial_bundle()` passa a validar recibo público de assinatura.
7. promoção e package recompõem frase-mãe, seleção, hashes e fidelidade.
8. o validador recompõe topologia por teses, frase-mãe, `claimIds`, ordem das
   seções e pedidos; fusão local de frases, por si só, não reprova.

Promover `_taste_receipt_findings()` a API pública ou substituir por validador em `forja.signature.contracts`; não importar função privada.

Testes:

- F7‑B altera ordem de teses;
- F7‑B troca frase-mãe;
- F7‑B seleciona geometria diferente;
- F7‑B remove âncora decisiva;
- F7‑B mantém forma local e passa;
- bundle histórico continua legível;
- bundle novo sem assinatura não é liberável.

Aceite:

- estratégia hash-bound preservada até `final_markdown`;
- todos os gates recompostos em promoção;
- F8 continua recebendo um único cânone.

### Onda 9 — AUTO‑RESEARCH e memória decisória

**Objetivo:** aprender com comparações sem autopromover preferência.

Implementar:

- indicadores novos separados, sem média:
  - identidade do caso;
  - clareza decisória;
  - recuperação fiel;
  - resistência ao contra-argumento;
  - economia condicionada à cobertura;
- conexão real de I9 ao julgamento cego;
- memória estruturada de selecionados e rejeitados;
- memória decisória `write_only` para a esteira de produção v1;
- leitura da memória e do corpus de contrastes restrita ao ciclo AR offline;
- `reasonCodes` por decisão;
- comparação por produto, tribunal e fase processual;
- corpus de contrastes `excepcional × apenas correto`;
- feedback sanitizado e autoria intelectual.

Corrigir antes da promoção:

- `promotion()` recompõe hashes de código, sensores e corpus;
- comparison/canary/judgment ficam vinculados ao snapshot;
- sealed exige rubrica, hashes e recibo;
- revisão independente valida identidade real da família;
- `human_approve()` exige estado anterior correto;
- recibo Ed25519 específico para promoção AR;
- transições persistidas atomicamente;
- `forja_ar_evolucao` não grava winner promovido antes da cadeia completa.

Testes:

- feedback sem fonte não promove;
- rejeição é aprendida sem copiar texto privado;
- alteração de rubrica invalida comparação;
- candidato selecionado não equivale a política promovida;
- decisão histórica pré-correção é stale;
- metadata-only não conta como corpus de qualidade;
- novo null bloqueia;
- prompt de F4-S/F6-A que contenha memória decisória bloqueia.

Aceite:

- cadeia candidato → eval → blind → recall → decisão → memória inteiramente hash-bound;
- nenhuma preferência altera regra jurídica;
- memória registra derrotas, não apenas vencedores;
- nenhum gerador de produção lê decisões pretéritas na v1.

### Onda 10 — Calibração humana inicial

**Objetivo:** ensinar a distinção entre excepcional e apenas fluente.

Construir pares cegos com:

- versão original;
- versão final revisada;
- candidato rejeitado;
- motivo concreto da rejeição;
- alterações aceitas;
- produto e fase processual;
- força da preferência;
- âncoras;
- limites.

Rubrica humana:

```text
juridicamente inferior
correto, mas mediano
forte
excepcional
abstenção
```

Não usar nome do autor como sinal. Não atribuir tese ao remetente sem ledger de contribuição.

Piso inicial de engenharia, a ser pré-registrado antes de ver resultados:

- mais de uma linhagem;
- mais de um produto jurídico;
- comparação cega;
- razões obrigatórias;
- amostra prospectiva;
- revisão de casos em que IA e humano discordam;
- regra sequencial de parada com precisão, estabilidade, missingness e mínimos
  por linhagem/produto definidos antes da primeira observação;
- métrica de concordância, estabilidade sob swap e força mínima de preferência.

Não declarar eficácia a partir de contagem mínima nem escolher o ponto de parada
depois de observar um resultado conveniente. O tamanho final pode ser
sequencial, mas a função de parada é imutável e hash-bound.

Aceite:

- julgadores calibrados contra pares humanos;
- falsa preferência por verbosidade medida;
- posição invertida;
- desacordos preservados;
- nenhum dado privado entra em prompt público.

### Onda 11 — Piloto sombra

**Objetivo:** observar sem afetar a peça produzida.

Modo:

```json
{"signature": {"mode": "shadow"}}
```

O incumbente segue para F7. A FORJA‑ASSINATURA executa em paralelo e registra:

- candidato que escolheria;
- divergência contra incumbente;
- custo;
- legal noninferiority;
- recall;
- preferência humana quando disponível;
- falhas.

Critérios para sair da sombra:

- denominador mínimo pré-registrado por linhagem e produto atingido;
- zero regressão jurídica detectada no ramo sombra;
- detector de alteração material executado e sem falso negativo conhecido no
  conjunto de canários;
- cadeia hash-bound íntegra;
- swaps consistentes;
- casos prospectivos de mais de uma linhagem;
- ganho não explicado apenas por tamanho;
- revisão explícita dos desacordos.

Rollback:

- `mode=off`;
- nenhuma migração de artefato canônico;
- sidecars permanecem auditáveis.

### Onda 12 — `pilot_blocking`

**Objetivo:** tornar a seleção obrigatória em escopo controlado.

Regras:

- somente produtos/tribunais expressamente habilitados;
- candidato zero disponível;
- ausência de vencedor preserva incumbente;
- falha de integridade bloqueia;
- falha apenas de superioridade não bloqueia;
- toda decisão entra no log.

Não confundir com `default_on`.

Aceite:

- ciclos prospectivos completos;
- nenhum bypass;
- regressões de package/F8 ausentes;
- revisão independente;
- promoção humana da política, não da redação de cada caso.

### Onda 13 — `default_on`

**Objetivo:** executar autonomamente em novos casos elegíveis.

Pré-condições:

- `pilot_blocking` estável;
- sealed prospectivo;
- human promotion receipt dedicado;
- métricas e custos dentro do orçamento;
- famílias independentes disponíveis ou limitação registrada;
- ganho prospectivo sobre `candidate_0` conforme regra de preferência
  pré-registrada, sem regressão jurídica;
- documentação, mapas e rollback testados.

Autonomia:

- F4‑S, F6‑A/B/C e seleção são automáticos;
- F7/F7‑B continuam fail-closed;
- protocolo externo continua dependente da liberação jurídica vigente.

Rollback:

- alterar para `pilot_blocking` ou `shadow`;
- preservar todos os hashes;
- não apagar decisões;
- reprocessar somente casos sem pacote liberado.

### Onda 14 — Documentação e arquitetura

Após mudança estrutural:

1. atualizar `FORJA_SPEC_MANIFEST.json`;
2. atualizar contratos F4/F6/F7;
3. atualizar documentação técnica e protocolos;
4. atualizar catálogo;
5. regenerar Graphify e Archify;
6. renderizar e validar todos os HTMLs;
7. atualizar hashes;
8. executar consultas de grafo sobre os novos símbolos;
9. registrar relatório antes/depois.

Comandos-base:

```powershell
python "C:\Users\IgorPC\.claude\projects\00_MAPA_ARQUITETURA_IA\REGENERAR_MAPAS_ARQUITETURA.py"
python "C:\Users\IgorPC\.claude\projects\00_MAPA_ARQUITETURA_IA\APROFUNDAR_MAPAS_ARQUITETURA.py"
graphify update .
graphify query "FORJA ASSINATURA F4-S F6 seleção F7 F7-B" `
  --graph "00_MAPA_ARQUITETURA_IA\graphify-out\graph.json"
```

## 10. Configuração proposta

```json
{
  "signature": {
    "protocolVersion": "FORJA-ASSINATURA-v1",
    "mode": "off",
    "minGeometries": 5,
    "maxGeometries": 7,
    "microbriefCandidates": 3,
    "fullDraftCandidates": 2,
    "expandToThirdDraftOnAmbiguity": true,
    "ambiguityRuleId": "signature-shortlist-margin-v1",
    "recallCardMaxWords": 80,
    "recallInputPolicy": "body_without_executive_summary",
    "requireBlindSwap": true,
    "judgeIndependencePolicy": "prefer_cross_family",
    "allowedDegradedJudgeMode": "cross_session_same_family",
    "rejectSelfJudge": true,
    "allowCorrelatedGeneratorsInShadow": true,
    "allowCorrelatedGeneratorsInBlocking": true,
    "productionMemoryReadPolicy": "deny",
    "budgetProfileId": "signature-pilot-v1",
    "preserveIncumbentOnTie": true,
    "newPaidApiAllowed": false
  }
}
```

`signature-pilot-v1` deve resolver para limites numéricos de chamadas, tokens de
entrada/saída, tempo total, número de juízes e comparações. A Onda 0 mede a
linha de base; a Onda 1 congela o perfil antes de W2. Parâmetros, budgets,
função de parada e gatilhos devem ser hash-bound. Alteração depois de observar
resultados invalida o ciclo.

## 11. Orçamento e eficiência

O sistema não deve gerar sete peças completas.

Funil:

```text
5–7 geometrias baratas
→ 3 micropeças
→ 2 drafts completos
→ 3º draft apenas sob ambiguidade
→ 1 vencedor
```

Controles:

- orçamento por caso;
- tokens/tempo por candidato;
- limite numérico de chamadas e comparações por estágio;
- cache apenas de artefatos hash-identical;
- early exit jurídico;
- nenhum novo custo de API sem autorização;
- preferência por assinaturas/OAuth existentes;
- custo registrado como métrica operacional, nunca qualidade;
- estouro de budget preserva `candidate_0` com reason code; jamais pula gate
  jurídico.

## 12. Matriz de testes

### 12.1 Unidade

- schemas;
- reason codes;
- resolução de IDs;
- diversidade por eixo e distância de ordem;
- canonicalização;
- permutações;
- Condorcet;
- abstenção;
- recall card;
- remoção segura da síntese executiva;
- topologia estrutural insensível a edição local;
- transições de estado;
- hash chain.

### 12.2 Contrato

- F4 histórico;
- F4 novo com sidecars;
- F6 histórico com um draft;
- F6 novo com candidatos internos e um output canônico;
- F7 com assinatura;
- F7 histórico legível;
- F8 sem alteração de interface;
- package recompõe gates.

### 12.3 Metamórficos

- trocar posição;
- anonimizar autor;
- trocar nomes mantendo relações;
- retirar âncora;
- inserir autoridade irrelevante;
- aumentar comprimento;
- repetir termos da rubrica;
- inverter polaridade;
- alterar data/valor;
- preservar palavras e alterar nexo.

### 12.4 Adversariais

- prompt injection;
- mapping leak;
- family spoofing;
- self-judge;
- result JSON fora do schema;
- `approved=true` sem evidência;
- alteração pós-snapshot;
- sealed falso;
- salto de estado;
- downgrade silencioso para candidato único;
- feedback sem autoria;
- memória decisória vazando para prompt de geração;
- prova de independência baseada apenas em autodeclaração.

### 12.5 Regressão real

- artefatos sanitizados;
- casos históricos somente replay;
- pilotos prospectivos em sombra;
- comparação de hashes de package;
- F8 renderizado página a página.

### 12.6 Comandos mínimos

```powershell
python -m pytest -q -p no:cacheprovider `
  test_forja_assinatura.py `
  test_forja_autoresearch.py `
  test_forja_fable5.py `
  test_forja_estilo_humano.py `
  test_forja_run.py `
  test_forja_anti_hallucination_v2.py `
  test_forja_n4.py `
  test_forja_pso_pet.py `
  test_forja_mutation_semantic.py

python forja_phase_contracts.py
python -m json.tool FORJA_SPEC_MANIFEST.json > $null
python validate_forja_n3.py --real-word --run-replay
python forja_regua.py
```

A contagem de testes deve vir da coleta viva, nunca de número escrito manualmente.

## 13. Gate de promoção

Uma política FORJA‑ASSINATURA só avança se:

1. schemas e contratos forem válidos;
2. code/sensor/corpus hashes forem recompostos;
3. canários públicos e secretos passarem;
4. nenhum alvo jurídico regredir;
5. nenhum veto for violado;
6. o julgamento estiver hash-bound;
7. houver swap estável;
8. o modo de independência real estiver permitido e registrado;
9. recall for fiel;
10. sealed prospectivo passar;
11. revisão independente passar;
12. recibo humano dedicado autorizar a política;
13. rollback estiver testado;
14. houver ganho prospectivo pré-registrado sobre `candidate_0`, sem regressão
    jurídica e sem explicação apenas por comprimento.

Resultado técnico máximo antes da aprovação:

```text
technical_candidate_passed
```

Depois:

```text
independent_review_passed
→ human_promotion_approved
→ pilot_blocking
→ default_on
```

## 14. Modos de falha e resgate

| Falha | Severidade | Detecção | Resgate |
|---|---:|---|---|
| Diversidade apenas declarada | P1 | hashes/artefatos ausentes | invalidar lote |
| Geometrias sinônimas | P1 | eixos/ordens duplicados | regenerar divergência |
| Candidato inventa lastro | P0 | ledger mismatch | bloquear |
| Mesmo redator/sessão escolhe própria peça | P0 em modo bloqueante | family/session graph | abster e preservar incumbente |
| Uma só família é apresentada como independência | P1 | `judgeIndependenceMode` | registrar correlação e aplicar modo degradado |
| Viés de posição | P1 | swap inconsistente | anular comparação |
| Novidade vazia vence | P1 | grounding + case identity | preservar incumbente |
| Verbosidade vence | P2 | length-controlled judge | normalizar e repetir |
| Recall inventa | P0 | confronto com map | eliminar candidato |
| Ciclo de preferência | P2 | matriz N-way | abster/preservar incumbente |
| F7‑B reabre estratégia | P0/P1 | topologia canônica | rejeitar F7‑B |
| Recibo narrativo substitui prova | P0 | recomputação | bloquear promoção |
| Corpus metadata-only infla N | P1 | `scoringEligible` | excluir da calibração |
| Hash antigo usado como atual | P1 | snapshot version | stale |
| Custo explode | P2 | budget | early exit/limite |
| Nova política se autopromove | P0 | state machine | exigir receipt |
| Texto elegante chamado “corrigido” | P0 | gate MC‑07 | separar editorial/jurídico |

## 15. Anti-padrões proibidos

- renumerar F0–F10;
- transformar F5 em redator;
- levar todos os candidatos a F7/F8;
- usar o Fable pós-F7 para refazer estratégia;
- chamar retries de diversidade;
- permitir que o gerador seja o julgador;
- selecionar pelo menor SHA;
- produzir média que compense erro jurídico;
- aceitar “sem P0” como excelência;
- aceitar exit code zero como promoção;
- gravar winner antes da cadeia completa;
- confiar em família declarada quando envelope verificável existe;
- usar corpus metadata-only para alegar calibração;
- treinar sobre vencedor sem registrar derrotas;
- expor memória decisória aos geradores de produção na v1;
- alegar independência entre famílias no modo `cross_session_same_family`;
- deixar feedback importado sem proveniência intelectual;
- rebaselinear Régua automaticamente;
- criar novo registry de schemas;
- introduzir API paga.

## 16. Critério de concluído

A implementação estará concluída somente quando:

1. F4‑S materializar frase-mãe, default e 5–7 geometrias;
2. F6 materializar `candidate_0` e desafiantes com nível de independência real,
   prompts, sessões, snapshot e hashes manifestados;
3. seleção N-way funcionar com cegamento e abstenção;
4. candidato zero for preservado em empate;
5. F7 receber um único cânone;
6. F7‑B não puder alterar a geometria;
7. promoção recompuser todos os hashes e gates;
8. memória registrar selecionados e rejeitados;
9. AUTO‑RESEARCH medir a camada em casos pontuáveis;
10. pilotos prospectivos passarem sem regressão;
11. `pilot_blocking` e rollback forem exercitados;
12. documentação, mapas, hashes e testes estiverem atualizados;
13. `default_on` tiver promoção humana da política;
14. nenhuma alegação de eficácia exceder a evidência;
15. memória decisória permanecer invisível aos geradores de produção v1;
16. ganho prospectivo sobre `candidate_0` satisfizer a regra de parada
    pré-registrada;
17. custo, latência e modo degradado estiverem dentro dos limites congelados.

## 17. Sequência recomendada de execução

```text
W0 baseline
→ W1 contratos
→ W2 F4-S
→ W3 grounding F5
→ W4 microbriefs/shortlist F5-S
→ W5 drafts F6-A
→ W6 cegamento F6-B
→ W7 recall/steelman/seleção F6-C
→ W8 F7/F7-B
→ W9 AUTO-RESEARCH/memória
→ W10 calibração
→ W11 shadow
→ W12 pilot_blocking
→ W13 default_on
→ W14 documentação/mapas
```

Não executar W2–W8 como uma única mudança. Cada onda deve produzir:

- diff pequeno;
- teste;
- relatório;
- gate;
- rollback;
- decisão explícita de avançar.

### Referências obrigatórias por onda

| Onda | Padrão a copiar, não reinventar |
|---|---|
| W0 | `test_forja_autoresearch.py`, `test_forja_fable5.py`, `REGUA_MANIFEST.json` |
| W1 | `forja_n4_common.py:22-180`, `generate_n4_contracts.py:108-202`, `forja_phase_contracts.py:10-46` |
| W2 | `forja_reasoning.py:18-191`, `phase_contracts/F4.json`, `phase_contracts_n4/F4.json` |
| W3 | `forja_citations.py`, `phase_contracts/F5.json`, artefatos F5C do catálogo |
| W4 | seam `invoke=` de `forja_fable5.py:290-432` e manifests de `forja_ar_runpair.py:36-150` |
| W5 | injeção de prompt de `forja_headless.py:27-120` e `forja_estilo_humano.py:152-158` |
| W6 | `forja_ar_blind.py:68-248`, sem herdar o limite binário; `forja_ar_evolucao.py:103-147`, sem desempate por SHA |
| W7 | `forja_case_tests.py:48-189` e `forja_mutation_semantic.py:179-246` |
| W8 | `forja_editorial_fidelity.py:134-310`, `forja_run.py:255-311`, `forja_package.py:470-619` |
| W9 | `forja_ar_ciclo.py:96-306`, `forja_learning.py:55-153`, `forja_state_machine.py:110-351` |
| W10 | `forja_human_review.py:174-273` e ledgers de contribuição intelectual |
| W11–W13 | `FORJA_N3_CONFIG.json`, `forja_n4_validate.FLAG_FILES`, eventos append-only |
| W14 | `00_MAPA_ARQUITETURA_IA/LEIA_PRIMEIRO.md` e scripts canônicos de regeneração |

## 18. Primeira entrega a executar

A primeira entrega de código deve conter apenas:

1. estabilização do baseline;
2. schemas;
3. validadores puros;
4. reason codes;
5. configuração `mode=off`;
6. perfil de orçamento numérico congelado;
7. contrato material de `candidate_0`;
8. política de memória `write_only`;
9. testes de contrato;
10. nenhuma chamada a modelo;
11. nenhuma alteração no output de F4–F8.

Esse recorte prova a nova linguagem do sistema sem colocar uma petição em risco. A geração começa somente na onda seguinte.
