# PRD — FORJA FILA: priorização automática painel → FORJA

**Origem:** recomendação R1.1 (achado H3, crítico) do parecer Helena de 11/07/2026 (`reports/conselho_2026-07-11/RELATORIO_HELENA.md`), autorizada pelo Igor em 12/07/2026.
**Objetivo de negócio:** dobrar a vazão da fábrica (4 → 8 peças/semana viáveis) eliminando o gargalo de priorização manual — hoje cada demanda exige que alguém abra 17 pastas e decida "qual é a próxima".
**Métrica de sucesso (Helena):** Igor consegue dizer "próximas 5 peças a fazer" sem abrir nenhuma pasta, em um único lugar, com o porquê da ordem explicado.

---

## 1. Problema

O painel (`gestao_escritorio/data/demandas.json`) registra as demandas com status, prazo e urgência, e a FORJA reporta estado para o painel (ponte FORJA→painel via `forja_management_bridge.py`/`sync_forja_gestao.py`). **O caminho de volta não existe**: nenhuma etiqueta do painel dispara ou ordena trabalho na FORJA. Consequências medidas na auditoria de 11/07:

- Fila fantasma (H7): 17 demandas "abertas" no papel, só ~5-7 prontas de fato — as demais têm bloqueador não visível (anexo externo pendente, decisão do Fábio, comando ausente).
- Capacidade prática ~4 peças/semana; cada peça acima disso exige decisão por WhatsApp/reunião.
- Zero transparência de fila para o Fábio ("o que vem agora e por quê").

## 2. Solução em uma frase

Um motor determinístico (`forja_fila.py`) que lê o painel + os estados F0 da FORJA, classifica cada demanda aberta em **pronta / bloqueada (com motivo) / em produção**, calcula um **score de prioridade explicável** e grava a fila ordenada em três lugares: JSON para máquinas, relatório para humanos e seção no painel HTML.

**A fila propõe; o humano dispara.** O ganho de vazão vem de eliminar a decisão manual de priorização e a caça a bloqueadores — não de disparar produção sozinha.

## 3. Requisitos funcionais

| ID | Requisito | Critério de aceite |
|---|---|---|
| FILA-R1 | Ler `demandas.json`, `intervencoes_manuais.json` e `state/case-*/FORJA_STATE.json` em modo leitura. **Nunca escrever em `demandas.json`** (quadro de comando é humano/Hermes — protocolo da fábrica) | Diff de `demandas.json` antes/depois de rodar a fila é vazio, sempre |
| FILA-R2 | Classificar prontidão de cada demanda não-cumprida: `pronta`, `bloqueada_acesso` (anexos externos/Drive pendentes), `bloqueada_comando` (sem `COMANDO_*.md`), `bloqueada_decisao_cliente` (próxima ação depende do Fábio), `bloqueada_pasta` (P0 de pasta no F0), `em_producao` (F1-F9 em andamento), `aguardando_revisao_humana` (status painel `pronta_para_revisao` — peça feita, gargalo é gente; descoberto no gate M0 de 12/07), `aguardando_evidencia` | Cada demanda aparece em exatamente uma categoria, com o motivo textual do bloqueio |
| FILA-R3 | Score de prioridade **determinístico e explicável** (§5). Proibido LLM/heurística opaca no cálculo | Mesmo input → mesmo score, coberto por regressão; relatório mostra a decomposição em pontos por fator |
| FILA-R4 | Gravar: (a) `state/FILA_PRIORIZADA.json` (canônico, máquina); (b) `reports/FILA_<data>.md` (humano, com decomposição do score e lista de bloqueadores); (c) `gestao_escritorio/data/forja_fila.json` (consumo do painel, escrita atômica) | Os três artefatos existem e batem entre si após cada execução |
| FILA-R5 | Seção "Próximas peças (FORJA)" no painel HTML gerado por `render_dashboard.py`, com top 5 prontas + contagem de bloqueadas por motivo | Painel renderiza a seção; **na ausência de `forja_fila.json` o painel renderiza normalmente sem a seção** (degradação limpa) |
| FILA-R6 | Comando de consumo: `python forja_fila.py --proxima` imprime o caso do topo (caseId, pasta, comando, score, motivo) pronto para disparar a produção | Dry-run ponta a ponta: fila → `--proxima` → caso correto do topo |
| FILA-R7 | Sinalização de espera de decisão (SLA informativo, não punitivo): demanda `bloqueada_decisao_cliente` há mais de 48h ganha destaque no relatório e no painel ("aguardando decisão há N dias") | Fixture com espera simulada gera o destaque; sem espera, não gera |
| FILA-R8 | Anti-inanição: demanda antiga sem urgência sobe gradualmente (§5), nunca fica invisível para sempre | Fixture: demanda de baixa prioridade com 30 dias aparece no top 10 |
| FILA-R9 | Feature flag `filaPriorizadaV1` no `FORJA_N3_CONFIG.json`; desligada, nada muda no comportamento atual (aditivo, padrão da casa N2/N3) | Flag off → painel e pipeline idênticos ao estado atual |

## 4. Requisitos não-funcionais

- **Determinismo total**: sem rede, sem LLM, sem relógio no score além de datas dos próprios dados (a data "hoje" entra como parâmetro injetável para teste).
- **Regenerável**: a fila é artefato derivado; apagar e rodar de novo reconstrói idêntico. Ninguém edita a fila à mão.
- **Execução**: manual ou ao fim do `forja_reconcile.py` (mesmo ciclo do F0). Sem daemon/watcher — rejeitado como complexidade sem necessidade.
- **Compatível com a régua**: `forja_fila.py` entra no manifesto da régua (`forja_regua.py`) como arquivo protegido.

## 5. Fórmula de prioridade (normativa)

Score 0–100, somente demandas `pronta` competem pela fila de produção (bloqueadas ficam em lista própria, ordenadas pelo mesmo score, para orientar o desbloqueio):

| Fator | Pontos | Fonte |
|---|---|---|
| Urgência manual `alta` | +40 | `urgenciaManual` (painel) |
| Urgência manual `media` ou ausente | +20 | idem |
| Urgência manual `baixa` | +0 | idem |
| Prazo ≤ 3 dias | +40 | `prazo` |
| Prazo ≤ 7 dias | +30 | idem |
| Prazo ≤ 14 dias | +20 | idem |
| Prazo ≤ 30 dias | +10 | idem |
| Sem prazo estruturado | +0 | idem (e o F0 já flagra `SEM_PRAZO_TRIAGEM`) |
| Tag `alto valor` | +10 | `tags` |
| Idade: +1 ponto por dia desde `recebidoEm`, teto +10 | +0..10 | `recebidoEm` |

Desempate, nesta ordem: prazo mais próximo → `recebidoEm` mais antigo → `id` lexicográfico. Prazo vencido conta como "≤ 3 dias" e ganha marcador `PRAZO_VENCIDO` no relatório (nunca some da fila).

**Regra de ouro:** o score ordena, não decide. `urgenciaManual: alta` colocada pelo Igor/Hermes domina o topo por construção (+40). Se a ordem parecer errada, o humano ajusta a urgência no painel — a fila obedece na próxima execução. Não há override dentro da fila.

## 6. Fora de escopo (anti-requisitos — não reabrir sem fato novo)

1. **Disparo automático de produção** (fila iniciando F1-F10 sozinha): risco de negócio — peça errada produzida no momento errado consome as horas que a fila deveria economizar. O disparo continua sendo comando explícito (humano ou agente sob comando).
2. **Escrita em `demandas.json`** pelo motor de fila (inclusive preencher `prioridade`): quadro de comando é do humano.
3. **LLM no score** ou qualquer fator não-reprodutível.
4. **Daemon/watcher de arquivo**: rodar junto do reconcile e sob demanda basta; cron é opcional futuro.
5. **SLA punitivo / escalonamento automático de cobrança ao cliente**: só sinalização visual de espera (FILA-R7).

## 7. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Score mal calibrado deixa peça urgente para trás | `urgenciaManual` domina por construção; relatório decompõe os pontos (auditável de relance); M4 do mapa recalibra pesos com 1 semana de uso real |
| Fila vira segunda fonte de verdade e diverge do painel | Fila é derivada e regenerável; carrega `geradoEm` + hash do `demandas.json` de origem; painel mostra "fila de <timestamp>" |
| Seção nova quebra o painel existente | Renderização isolada com degradação limpa (FILA-R5); QA visual do painel no gate do M2 |
| Demanda classificada `pronta` mas na verdade bloqueada | Prontidão deriva dos findings do F0 (`forja_reconcile.py`), que já é a autoridade de bloqueio; caso o F0 não pegue, a lição vira finding novo no F0, não gambiarra na fila |

## 8. Dependências

- `forja_reconcile.py` (F0) — fonte dos findings de bloqueio; a fila roda DEPOIS do reconcile (ou o chama).
- `render_dashboard.py` — único escritor do painel HTML (memória do projeto: nunca editar o HTML direto).
- `forja_n3_common.py` — `atomic_write_json`, `feature_enabled`, `now_iso`.
