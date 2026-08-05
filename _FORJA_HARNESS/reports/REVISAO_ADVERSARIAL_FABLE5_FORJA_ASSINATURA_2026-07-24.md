# Revisão adversarial Fable 5 — FORJA-ASSINATURA

**Data:** 24/07/2026  
**Protocolo avaliado:** `FORJA-ASSINATURA-v1`  
**Objeto:** `planejamento/26_PLANO_IMPLEMENTACAO_FORJA_ASSINATURA.md`  
**Modelo confirmado pelo envelope do Claude Code:** `claude-fable-5`  
**Sessões:** `3237d49a-314c-4082-8ebd-b1ed03c70129` e
`af68cd8b-3ccd-422c-a82f-b2d17852346a`  
**Modo:** duas leituras adversariais, sem ferramentas: arquitetura/contratos e
testes/rollout/promoção.

## 1. Veredito

**GO-COM-CONDIÇÕES.**

A tese do plano é correta: a FORJA não alcançará texto excepcional adicionando
adjetivos de estilo ao último prompt. Ela precisa criar divergência estrutural
antes da prosa, materializar alternativas, compará-las cegamente e preservar o
incumbente quando a melhora não for demonstrada.

O plano original, porém, não era executável sem decisões adicionais. Quatro
lacunas permitiam autonomia apenas nominal:

1. o `candidate_0` era um fluxo abstrato, não um texto comparável;
2. a bancada exigia famílias distintas que podem não existir no ambiente real;
3. o recall podia apenas copiar a síntese executiva obrigatória;
4. os gates de piloto, custo, memória e promoção ainda continham critérios
   narrativos ou indecidíveis.

As correções foram incorporadas ao Plano 26 e formalizadas no PRD 27 e TDD 28.

## 2. Julgamento do plano original

| Dimensão | Nota original | Nota após revisão | Fundamentação |
|---|---:|---:|---|
| Tese de produto | 5/5 | 5/5 | ataca mediania pela arquitetura, não por cosmética |
| Segurança jurídica | 4/5 | 5/5 | vetos permanecem acima de qualquer preferência editorial |
| Executabilidade | 2/5 | 4/5 | baseline, piloto e modo degradado agora têm semântica |
| Resistência a Goodhart | 3/5 | 4/5 | memória isolada, recall descontaminado e promoção por ganho |
| Compatibilidade | 4/5 | 5/5 | F0–F10 e `final_markdown` permanecem canônicos |
| Custo e operação | 2/5 | 4/5 | perfil numérico passa a ser obrigatório antes de gerar |
| Evidência de eficácia | 3/5 | 4/5 | regra sequencial e ganho sobre incumbente tornam-se gates |

O ponto ainda não pontuável como 5/5 é empírico: não existe, nesta etapa de
planejamento, uma rodada prospectiva que demonstre ganho real.

## 3. Evidências confirmadas no código vivo

1. `forja_ar_blind.py` prepara apenas os lados `vigente` e `variante`; o
   protocolo atual é binário.
2. `forja_ar_evolucao.py` ainda desempata dois aprovados pelo menor SHA-256. A
   FORJA-ASSINATURA não pode herdar essa regra.
3. `forja_n4_validate.FLAG_FILES` é global por feature, mas
   `forja_n4_validate._effective_mode()` já rebaixa casos fora de `pilotCases`
   para sombra. A assinatura deve reutilizar esse padrão.
4. `phase_contracts/F6.json` recebe `blueprint` e ledgers e publica um único
   `draft_markdown`; não há `optionalInputs` ou `conditionalInputs`.
5. `forja_editorial_fidelity.validate_editorial_bundle()` recompõe hashes,
   modelo e fidelidade, mas o recibo `gostoJuridico` continua validado dentro de
   `forja_fable5.py`, fora da recomputação final.
6. `forja_run.py` e `FORJA_SPEC_MANIFEST.json` já tratam `final_markdown` como
   cânone consumido por F8. O plano deve preservar essa interface.

## 4. Achados consolidados e decisão

| ID consolidado | Achados Fable | Severidade | Decisão | Correção incorporada |
|---|---|---:|---|---|
| R1 | A2, A11, B2 | P0 | aceita | `candidate_0` é texto integral, mesmo snapshot, hash próprio; abstenção aponta para ele |
| R2 | A1, B1, B10 | P0 | aceita com ajuste | preferência por famílias distintas; fallback declarado `cross_session_same_family`; self-judge bloqueia |
| R3 | A3, B6 | P0/P1 | aceita | recall recebe o corpo sem síntese executiva, removida deterministicamente |
| R4 | A4 | P0 | aceita | piloto reutiliza `pilotCases`; fora do escopo permanece sombra |
| R5 | A5 | P1 | aceita | `verified: true` vira enum de garantia; orquestrador atesta sessões e hashes |
| R6 | A6 | P1 | aceita | três vetos + preferência holística + estabilidade; sem lexicografia ruidosa |
| R7 | A7 | P1 | aceita | diversidade exige eixo distinto e distância estrutural computável |
| R8 | A9, B9 | P1 | aceita | topologia canônica por teses, frase-mãe, `claimIds`, ordem e pedidos |
| R9 | A10, B5 | P1 | aceita | budget profile numérico e hash-bound antes de W2; estouro preserva incumbente |
| R10 | A12, B3 | P0 | aceita | memória de produção `write_only`; leitura apenas no AR offline |
| R11 | B4, B8, B12 | P1 | aceita | regra sequencial, mínimos por estrato e concordância pré-registrados |
| R12 | B7 | P1 | aceita com ajuste | ganho prospectivo é requisito de política `default_on`, não revisão humana por peça |
| R13 | A8 | P1 | aceita com ajuste | checkpoint empírico após F4-S; humano calibra política, não participa do runtime |
| R14 | B11 | P2 | aceita | aceite passa de “inferior” subjetivo para P0/veto objetivo |

## 5. Ajustes deliberados ao parecer

### 5.1 Segunda família não vira dependência obrigatória

O Fable identificou corretamente a contradição, mas a solução não será comprar
API ou impedir todo piloto. O produto registra o grau real de independência:

- `cross_family`: garantia mais forte;
- `cross_session_same_family`: garantia degradada, permitida com swap, prompts
  disjuntos e sessões novas;
- `unverified`: não seleciona desafiante em modo bloqueante.

Isso evita tanto a falsa independência quanto um gasto novo não autorizado.

### 5.2 A autonomia pretendida permanece

A calibração humana inicial e a autorização de política não significam
intervenção na redação de cada petição. Depois da promoção:

- mapa, divergência, redação, comparação e seleção rodam automaticamente;
- gates jurídicos continuam fail-closed;
- empate ou dúvida preservam `candidate_0`;
- protocolo externo permanece fora do escopo desta camada.

### 5.3 “Memorabilidade” não é KPI isolado

Recall é diagnóstico secundário. Não pode:

- compensar regressão jurídica;
- decidir sozinho um vencedor;
- ser otimizado pela repetição da síntese;
- ser apresentado como prova de memória humana.

## 6. Condições bloqueantes antes de implementar geração

1. A Régua precisa estar verde ou o desvio precisa ser classificado e aceito
   como baseline conhecido; rebaseline automático permanece proibido.
2. Os schemas devem tornar `candidate_0`, assurance, modo de independência,
   budget e política de memória campos obrigatórios.
3. O perfil de orçamento deve conter números medidos e congelados.
4. Deve existir teste que prova a condicionalidade do piloto por caso.
5. Deve existir teste negativo que prova ausência de memória decisória nos
   prompts de F4-S e F6-A.

## 7. Condições para `default_on`

1. zero regressão jurídica detectada no conjunto prospectivo;
2. canários demonstram capacidade de detectar mudança material;
3. regra sequencial de amostra satisfeita por mais de uma linhagem e produto;
4. ganho prospectivo estável sobre `candidate_0`;
5. custo e latência dentro do perfil congelado;
6. rollback exercitado;
7. revisão independente e recibo humano autorizam a política;
8. nenhuma alegação de independência ou eficácia excede a evidência.

## 8. Risco residual

O risco principal deixa de ser arquitetural e passa a ser empírico: um sistema
pode gerar alternativas estruturalmente diferentes e ainda assim não produzir
peças melhores. Por isso W2 possui checkpoint go/no-go, e W13 exige ganho
prospectivo. Se a hipótese não se confirmar, a decisão correta é manter a
camada em sombra ou desligá-la, preservando toda a FORJA atual.
