# Ciclo AR-1 — Primeiro ciclo REAL de trabalho e auto-aperfeiçoamento (23/07/2026)

> Geração 0 do experimento evolutivo `prompt-mestre-v2` (modelo AutoResearch/Karpathy sobre os
> trilhos anti-trapaça do ciclo AR). Nada simulado: alvo real, tarefa real do split train,
> execuções reais, juízes reais, gates reais — incluindo duas rodadas de julgamento INVALIDADAS
> pelo próprio harness antes de uma válida.

## Resultado

**Vencedora da geração 0: variante `varB` (estratégia compress)** — venceu o julgamento cego
por unanimidade (kappa 1.0, swap-consistente por hash), passou a não-inferioridade em todos os
sensores e chegou a `technical_candidate_passed` → `independent_review_passed` (revisor de
família não-geradora: **APTA COM RESSALVAS**). **Nenhuma propagação foi feita**: o gate humano
(recibo Ed25519 do Igor) permanece pendente, e a decisão evolutiva registrada é incorporar as
ressalvas do revisor como mutação `hybrid` da geração 1 antes de qualquer adoção.

## O experimento (pré-registrado no snapshot A0, log encadeado)

- **Alvo real:** `PROMPT-FABRICA-MELHORIA-PETICAO.md` (prompt-mestre da fábrica — mesmo alvo do experimento manual fabrica-peticoes-v1).
- **Mutações (geração 0, autoria Codex GPT-5.5):** varA `expand` (29,2k — incorpora diretrizes 6–24) e varB `compress` (17,8k vs baseline 17,9k — mesma força normativa, gates consolidados).
- **Tarefa real (split train):** rascunho F6 do caso `case-email-auto-19f3f25cb64df962` (36k, plano de saúde/TJDFT), input congelado com hash.
- **Execuções pareadas (Codex, mesmos parâmetros):** 3 entregas completas reais — vigente 79k / varA 84k / varB 60k chars (766k tokens no total); paridade validada pelo harness.
- **Juízes cegos:** 2 juízes Claude de contexto independente (família NÃO-geradora; Gemini indisponível no ambiente — limitação pré-registrada no manifest antes do snapshot).

## O que o anti-trapaça pegou (em produção real)

1. **Round 1 INVALIDADO** — âncoras dos juízes não eram citações literais dos bundles (paráfrases). A bancada recusou 8/8 votos (`ancora_invalida`). Nenhum conserto manual: reexecução.
2. **Round 2 INVALIDADO** — o debug das âncoras provou que, com 8 arquivos parecidos numa mesma sessão, os juízes trocaram rótulos de posição/par: em 5 de 8 votos a citação elogiada pertencia a OUTRO texto que não o votado. Correção de protocolo derivada: **um par por sessão de juiz**.
3. **Round 3 VÁLIDO (protocolo corrigido)** — par varB: 2 juízes × 2 ordens, todos no mesmo artefato por hash, kappa 1.0. Par varA: devolutiva de um juiz caiu de novo por âncora (fail-closed); o voto válido remanescente preferiu o VIGENTE — varA não comprovou superioridade e perdeu a geração.

## Verificação realizada

- Canários A2: 8/8 (públicos + secretos) antes do ciclo.
- Paridade runpair: válida nos dois pares (mesmo inputHash/modelo/família/parâmetros).
- Não-inferioridade: aprovada para varA e varB (deltas 0.0 em I2/I4/I5/I6 — as três execuções passam limpas nos sensores determinísticos; a decisão recaiu no juiz cego, como desenhado).
- Promotion gate: `technical_candidate_passed` com orçamento consumido 4/200 julgamentos; **sealed não consultado** (sem promoção de produção; ver gap abaixo).
- Log `AR_LOG.jsonl`: cadeia de hashes íntegra (`verify-log` verde).
- Seleção evolutiva: `winners/gen-0.md` = varB; convergência: 1 geração fechada com ganho.

## Parecer independente (família claude ≠ geradora codex)

APTA COM RESSALVAS: 25 de 28 obrigações materiais PRESERVADAS; 3 ENFRAQUECIDAS na compressão
(bloqueio de cobertura do ato impugnado; obrigatoriedade da simulação de Helena; elo risco
crítico→liberação); 6 recomendações numeradas. Arquivo: `AR_PARECER_INDEPENDENTE_varB.md`.

## Aprendizados minerados (novos, deste ciclo)

- **L1.** Âncora literal é o detector mais barato de julgamento desatento: derrubou 2 rounds inteiros. Manter sempre.
- **L2.** Sessão de juiz deve conter UM par (4 arquivos); 8 arquivos similares induzem troca de rótulos mesmo em juízes competentes.
- **L3.** Compressão de prompt vence julgamento cego (menos redundância → melhor peça), mas o revisor adversarial acha o custo escondido: perda de clareza dos BLOQUEADORES. Julgamento cego + revisão de equivalência normativa são complementares, nunca substitutos.
- **L4.** Gap real de v1: `promotion --no-sealed` alcança `technical_candidate_passed` sem sealed, e `consume_sealed` debita sem avaliar de fato no conjunto selado. Corrigir em v1.1: avaliação sealed real antes do débito; sem sealed, teto explícito.
- **L5.** Tarefa 1 única no train: suficiente para provar o rito, insuficiente para generalizar — gen-1 deve usar ≥2 tarefas de linhagens distintas.

## Diagrama canônico

`AR_CICLO_HUMANO.html` (archify, modo workflow — raias por ator, fases Preparar/Competir/Julgar/Decidir,
raia de exceção com os 3 rounds reais, gate humano do Igor e trilha/cofre; fonte declarativa em
`ar-ciclo-humano.workflow.json`; validado com 0 erros pelo checker da skill e QA visual no navegador).
O `AR_CICLO_ARQUITETURA.html` anterior (modo architecture) permanece como histórico.

## Próxima ação

Geração 1: mutação `hybrid` (varB + recomendações 1–4 do parecer) contra o vigente, com ≥2
tarefas train, juízes um-par-por-sessão; propagação só com recibo Ed25519 do Igor.
