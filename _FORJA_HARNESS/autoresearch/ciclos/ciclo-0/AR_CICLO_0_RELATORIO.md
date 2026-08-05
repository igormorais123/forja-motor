# Ciclo AR-0 — Relatório do estudo piloto descritivo (2026-07-23)

> Declaração metodológica obrigatória (PRD §9.8): este ciclo é DESCRITIVO. Nenhuma
> alegação de eficácia é feita; nenhuma variante foi promovida. Promoção real exige
> sealed prospectivo acumulado e a cadeia de três estados do PRD §7/A6.

## Resultado

O subsistema FORJA AUTO-RESEARCH foi implementado, testado e calibrado com material real.
Painel de indicadores operante; canários de falha única com discriminação 7/7; corpus real
registrado com split HMAC por linhagem; suíte de 23 testes (12 sabotagens nominais) verde.

## Verificação realizada

1. **Suíte**: `python -m pytest test_forja_autoresearch.py -q` → 23 passed (execuções
   independentes do executor Codex e do auditor Fable 5).
2. **Corpus real** (`forja_ar_corpus.py --scan`, chave HMAC externa real): 49 diretórios
   → 43 elegíveis; 28 train / 7 holdout / 8 sealed (sealed registrado só fora do
   workspace); 7 artefatos pontuáveis; `--check` sem erros (hashes e linhagens íntegros).
3. **Canários** (`--verificar --secreto`): 5 classes públicas reais (base: peça auditada
   Azimut, split train) + exemplo sintético + 2 classes secretas na pasta externa —
   kill 7/7 pelo sensor-alvo, zero contaminação de outros sensores, controles benignos vivos.
   Classes: placeholder, origem operacional, estilo IA, súmula×tribunal trocada, citação
   obrigatória removida (com ledger congelado); secretas: origem parafraseada (Drive),
   placeholder sutil no meio do texto.
4. **Painel descritivo** (22 peças reais: 5 do corpus pontuável + 17 do experimento
   fabrica-peticoes-v1):

   | Indicador | n | missing | média | σ | leitura |
   |---|---|---|---|---|---|
   | I2 integridade jurídica | 22 | 0 | 0.909 | 0.288 | 2 peças históricas com violação |
   | I4 placeholders | 22 | 0 | 0.227 | 0.419 | maioria dos rascunhos internos tem marcadores — esperado em `internal_working` |
   | I5 estilo humano | 22 | 0 | 0.227 | 0.419 | sensor v2 é posterior às peças antigas; mostra a evolução da fábrica |
   | I6 origem operacional | 22 | 0 | 0.682 | 0.466 | 7 flags auditados manualmente: 7/7 verdadeiros positivos (caminho local vazado) |
   | I1/I3/I7 (ledger) | 0 | 22 | — | — | ledgers só existem prospectivamente; missingness declarada, nunca zero silencioso |
   | I8 QA visual | 0 | 22 | — | — | exige recibo Ed25519; histórico sem contexto materializado |
   | I9/I10 | 0 | 22 | — | — | julgamento cego e pós-entrega são por ciclo, não por peça isolada |

## Decisões de calibração (congeladas no `AR_MANIFEST.json` v1.0-piloto-descritivo)

- Papéis mantidos: I2/I4/I6/I8 vetos; I5 sentinela; I1/I3/I7/I9 alvos; I10 operacional.
- Vetos e sentinelas concentram a discriminação observada no corpus real (σ 0.29–0.47) —
  cumprindo a regra "≥70% do poder em dimensões discriminantes" pela via de veto absoluto.
- Alvos de ledger ficam com margem de ruído 0.0 (qualquer regressão bloqueia) até haver
  série prospectiva que justifique margem maior — decisão conservadora pré-registrada.
- Nenhum indicador removido: os sem dado histórico provaram discriminação nos canários
  (I1) ou dependem de infraestrutura já existente e obrigatória (I8/recibo Ed25519).

## Risco e pendência real

- Sem casos sealed CONSUMÍVEIS ainda (orçamento vitalício 3 consultas, intocado) — o
  subsistema permanece `estudo_descritivo`; nenhuma variante pode ser promovida.
- Ledgers de claims/autoridades precisam nascer no A0/runpair dos próximos casos reais
  para I1/I3/I7 saírem do missingness.
- A camada secreta de canários deve ser rotacionada após cada uso em decisão.

## Próxima ação

Primeiro ciclo comparativo real (A0–A6) quando houver variante candidata de artefato de
fase — por exemplo, evolução do template `templates/F4_METODO_SOLUCAO_PROBLEMA_PETICAO.md`
— com execução pareada, julgamento cego (Claude × Codex) e gate de promoção completo.
