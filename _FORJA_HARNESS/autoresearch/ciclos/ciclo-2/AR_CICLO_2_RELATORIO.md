# Ciclo AR-2 — Geração 1 (hybrid) REAL: a variante perdeu e nada foi promovido (23/07/2026)

> Segundo ciclo real de trabalho e auto-aperfeiçoamento do experimento `prompt-mestre-v2`.
> Resultado científico honesto: o hybrid NÃO superou o vigente. O anti-trapaça pegou um
> vazamento de cegamento causado pelo próprio orquestrador e anulou uma rodada inteira.

## Resultado

**Geração 1 fechada SEM winner.** A variante `varH` (estratégia hybrid: parent varB/compress +
recomendações 1–4 do parecer independente do ciclo-1) passou a não-inferioridade nas duas
tarefas, mas no julgamento cego válido **perdeu t1 para o VIGENTE por unanimidade (kappa 1.0,
vencedor por hash `fad08dc6…` = e3/vigente)** e **empatou t2 (kappa 0.0, sem vencedor)**.
`forja_ar_evolucao.py selecionar` → `winner: null`; convergência: 1 geração seguida sem ganho (limite: 3).
O prompt vigente permanece baseline. Nenhum recibo humano foi necessário — não houve candidata.

## O experimento (pré-registrado; log encadeado verde no fechamento)

- **Mutação (autoria Codex GPT-5.5):** `gen-1/varH_hybrid.md` (19,4 KB vs parent 17,8 KB) — os 4 reforços do parecer AR-1 escritos como obrigações bloqueantes (cobertura do ato impugnado → `internal_working`; Helena não-eletiva; fidelity do Fable; risco crítico bloqueia liberação). Conferidos nominalmente no texto antes do registro.
- **Tarefas train (2 linhagens distintas — lição L5 do ciclo-1):** t1 = plano de saúde/TJDFT (rascunho F6, 36 KB) e t2 = Azimut/STJ (memorial, 10 KB). Limitação documentada: a peça-base t2 é a mesma dos canários públicos (corpus train pontuável tem só 3 linhagens; a terceira, Natura com 177 KB, foi descartada por custo).
- **Execuções pareadas:** rodada 1 = 4 execuções (1,4M tokens) DESCARTADAS por vazamento (abaixo); rodada 2 = 4 execuções válidas com nomes opacos e1–e4 (2,18M tokens; paridade validada nos dois pares). Assimetria notável: executar o vigente custou 507k/1.635k tokens vs 126k/94k do varH — o prompt comprimido é 4–13× mais barato de executar.
- **Canários A2:** 8/8 (6 públicos + 2 secretos) antes de qualquer medição.

## O que o anti-trapaça pegou neste ciclo (tudo real)

1. **Round 1 ANULADO — cegamento comprometido pelo orquestrador.** Dois vazamentos nos bundles: (a) o executor ecoou o nome do arquivo de saída ("OUT_T2_VIGENTE") como título da peça; (b) o cabeçalho de mutação `<!-- mutacao: hybrid … parecer AR-1 … -->` entrou no prompt de execução e o executor escreveu referências ao "parecer AR-1" DENTRO das peças do varH — um juiz identificou a variante por isso. Correção: nomes de saída opacos (e1–e4) + remoção de cabeçalhos HTML na montagem + varredura anti-vazamento nos outputs e nos bundles antes de julgar. Trilha: `judgments/round1_invalidado/INVALIDACAO.md`.
2. **Round 2 ANULADO — viés posicional em 3 de 4 juízes** (mesma posição nas duas ordens = artefatos diferentes) e 1 âncora não literal. Correção de protocolo: instruir explicitamente que o voto segue o TEXTO através do swap (mesma âncora nas duas ordens, posição espelhada) — o que o juiz válido do ciclo-1 tinha feito naturalmente.
3. **Round 3 VÁLIDO** — t1b: 2 juízes × 2 ordens, âncoras literais verificadas, kappa 1.0 (um juiz da bancada original caiu por âncora não literal — fail-closed — e foi substituído por contexto novo). t2b: válido, empate 1×1, kappa 0.0.
4. **Gap v1 nº 2 descoberto em uso real:** `promotion` emitiu `technical_candidate_passed` sem conferir que o vencedor por hash é a VARIANTE (era o vigente). A camada evolutiva recusou. Corrigir na v1.1 junto com o gap nº 1 (sealed debita sem avaliar). Nota formal: `AR_PROMOTION_NOTA.md`.
5. **Sentinela I5 em ação (e seu limite):** na rodada 1, o varH tinha P0 de ritmo robótico em t2 e o vigente não; na rodada 2, o padrão se inverteu em t1 (delta +1.0 pró-varH). Sensor de execução única é ruidoso — papel `sentinela` (alerta sem veto) mostrou-se o desenho certo, mas a variância entre execuções precisa entrar no relatório de qualquer ciclo.

## Verificação realizada

- Paridade runpair: válida nos 2 pares da rodada 2 (`runpair-t1b`, `runpair-t2b`).
- Não-inferioridade: aprovada nas 2 tarefas (t1: deltas 0.0 + I5 +1.0; t2: todos 0.0).
- Julgamentos: `AR_JUDGMENT_ciclo2-t1b.json` (valid, kappa 1.0, winner=vigente) e `AR_JUDGMENT_ciclo2-t2b.json` (valid, kappa 0.0, sem winner).
- `verify-log`: cadeia de hashes íntegra após todos os eventos do ciclo.
- Orçamento de julgamentos consumido no gate: 4/200.

## Aprendizados minerados (novos)

- **L6.** O vazamento de cegamento mais provável não vem do juiz — vem do ORQUESTRADOR: nomes de arquivo com o lado e metadados de mutação embutidos no prompt são ecoados pelo executor dentro do produto. Toda montagem de execução pareada usa nomes opacos e remove cabeçalhos; toda bancada roda varredura anti-vazamento nos bundles antes de convocar juízes.
- **L7.** Juiz LLM não rastreia artefato através do swap sem instrução explícita: dizer "vote em cada ordem" produz viés posicional em massa (3/4). O protocolo agora diz: escolha o TEXTO, use a MESMA âncora nas duas ordens, posição espelhada, e mesma-posição-nas-duas-ordens anula.
- **L8.** Promotion gate precisa conferir `winner == variante` (gap v1 nº 2); enquanto isso, a seleção evolutiva é o gate efetivo.
- **L9.** Resultado negativo é resultado: reforçar obrigações (hybrid) não melhorou a peça aos olhos de juízes cegos — o vigente venceu t1. Hipóteses para gen-2: (a) os 4 reforços agem em fases que as tarefas train não exercitam (F7-B/F8, liberação final); (b) o benefício do compress do gen-0 não sobreviveu à adição de texto normativo. Próxima mutação deve mudar o EIXO (ex.: pivot sobre instruções de redação/estrutura da peça, que é o que os juízes efetivamente avaliam) ou trocar a métrica-alvo para incluir custo (varH executa 4–13× mais barato — ganho real que o julgamento cego não captura).
- **L10.** Custo de execução deveria ser indicador operacional formal do painel (I10 ou novo): 2 dos maiores achados do ciclo (tokens 13×, variância do I5) não estavam no desenho original.

## Fechamento das pendências (23/07/2026, noite — v1.1/v1.2)

Todas as pendências técnicas deste relatório foram implementadas e estão na Régua (APROVADA, 32/32
na suíte AR): gap 1 (sealed exige avaliação real antes do débito; teto `estudo_descritivo` sem
sealed), gap 2 (`promotion --variant-sha` bloqueia `vencedor_nao_e_variante`), L6 (`leak_scan`
bloqueante no prepare + `sanitize_instructions`), L7 (`templates/AR_JUIZ_PROTOCOLO.md`), L10
(`custoPareado` no validate_pair + I11 pré-registrado), e o desentrelaçamento canário×avaliação
(base migrada para a Impugnação Cafelana V4, fora do corpus; 8/8 kills reverificados).

## Próxima ação

Gen-2 só com decisão sobre o eixo (pivot de redação vs métrica de custo I11) — decisão do Igor,
sem pressa: convergência está em 1/3 e o vigente segue baseline.
