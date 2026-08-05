# Round 1 do ciclo AR-2 — INVALIDADO (cegamento comprometido)

Data: 2026-07-23. Decisão da bancada: fail-closed, nenhum voto consolidado.

## Evidência (verificada por busca exata na fonte)

1. `OUT_t1_varH.md` (2×) e `OUT_t2_varH.md` (3×) contêm referências a "parecer AR-1" — o cabeçalho
   `<!-- mutacao: hybrid | eixo: ... parecer AR-1 | parent: gen-0/varB -->` de `varH_hybrid.md`
   entrou no EXECPROMPT e o executor ecoou o metadado do experimento dentro da peça.
   O juiz 2 do par t1 citou exatamente esse trecho como âncora — a variante era identificável.
2. `OUT_t2_vigente.md` contém o próprio nome "OUT_T2_VIGENTE" ecoado como título pelo executor
   (o caminho de saída com o lado nomeado estava visível no prompt). O juiz do par t2 escreveu
   "L tem título OUT_T2_VIGENTE" — o lado vazou no bundle.

## Causa raiz

Falha de montagem do harness (não dos juízes): (a) caminhos de saída nomeando o lado;
(b) cabeçalho de mutação embutido nas instruções de trabalho. A canonicalização da bancada
não remove conteúdo ecoado pelo executor.

## Correção aplicada (rodada 2)

- Nomes de saída opacos (OUT_e1..e4) sem correlação com lado/tarefa.
- Cabeçalho HTML de mutação removido do texto da variante antes da montagem do prompt.
- Novas execuções pareadas completas; nenhuma edição manual dos outputs antigos.

Votos brutos desta rodada preservados nesta pasta apenas como trilha.
