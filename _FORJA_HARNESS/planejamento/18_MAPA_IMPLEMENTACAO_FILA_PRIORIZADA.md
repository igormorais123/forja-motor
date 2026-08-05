# Mapa de implementação — FORJA FILA

Roadmap executável da R1.1 (Helena, 16h estimadas). Cada marco tem gate de saída objetivo; nenhum marco seguinte começa com gate anterior aberto. Tudo aditivo e reversível por flag — padrão N2/N3 da casa.

## Visão geral

| Marco | Entrega | Esforço | Gate de saída |
|---|---|---|---|
| M0 | Flag + schema + fixtures | 2h | Schema validado contra os 23 casos reais em modo leitura |
| M1 | Motor `forja_fila.py` + regressão | 6h | Suíte 14 casos verde + rodada sombra real revisada por humano |
| M2 | Seção no painel | 3h | QA visual + painel idêntico com flag off / arquivo ausente |
| M3 | `--proxima` + encadeamento F0 + régua | 2h | Dry-run ponta a ponta; falha da fila não derruba F0 |
| M4 | 1 semana de operação assistida + calibração | 3h | Métrica da Helena atingida; flag default `true`; lição registrada |

Total: 16h. M1 é o caminho crítico; M2 e M3 podem andar em paralelo após M1.

---

## M0 — Fundação (2h)

1. Adicionar `filaPriorizadaV1: false` em `FORJA_N3_CONFIG.json`.
2. Escrever o schema de `FILA_PRIORIZADA.json` (TDD §3) como constante documentada no módulo.
3. Rodar protótipo de leitura contra os 23 casos reais (só leitura, sem gravar em `gestao_escritorio/`): imprime classificação de prontidão proposta.
4. **Gate M0:** revisão humana da classificação proposta dos 23 reais — se ≥3 demandas caírem em categoria obviamente errada, revisar o léxico/regras ANTES de codificar o motor (barato corrigir aqui, caro depois).

Risco tratado: o léxico de `bloqueada_decisao_cliente` (regra 7) é a parte mais frágil — validado contra dados reais antes de virar código de produção.

## M1 — Motor + regressão (6h)

1. `forja_fila.py`: funções puras (`classificar_prontidao`, `pontuar`, `ordenar`, `montar_fila`) + `main()` com os 3 artefatos (R4), escrita atômica.
2. `test_forja_fila.py`: os 14 casos do TDD §7 (7 DEVE_PEGAR + 7 NÃO_PODE_TRAVAR), fixtures sintéticas, `hoje` injetado.
3. Relatório humano `reports/FILA_<data>.md` com decomposição de score por fator (auditável de relance).
4. **Gate M1:** (a) suíte verde; (b) suítes existentes verdes (`test_forja_regua`, `test_forja_verificador`, `test_forja_citacoes`, `test_forja_conselho_1107`); (c) rodada sombra com dados reais gera fila que Igor/Efesto reconhecem como sensata — divergência vira ajuste de peso documentado, não gambiarra; (d) diff de `demandas.json` vazio (R1).

## M2 — Painel (3h) [paralelo com M3]

1. `secao_fila()` em `render_dashboard.py` lendo `data/forja_fila.json` com degradação limpa (R5): arquivo ausente/malformado/flag off → painel byte-idêntico ao atual.
2. Top 5 + resumo de bloqueadas por motivo + badge 48h (R7) + badge prazo vencido + aviso de frescor (hash de origem ≠ demandas.json atual).
3. **Gate M2:** QA visual do painel (gate obrigatório da casa — nunca declarar pronto sem olhar o render); teste A/B: renderizar sem `forja_fila.json` e comparar com o painel atual (nenhuma diferença).

Fronteira: `render_dashboard.py` é o ÚNICO escritor do HTML (memória do projeto). Nenhum CSS novo — só classes existentes.

## M3 — Consumo e encadeamento (2h) [paralelo com M2]

1. `forja_fila.py --proxima`: regenera e imprime o caso do topo; exit 3 se fila vazia (TDD §6).
2. Chamada opcional no fim de `forja_reconcile.main()` sob flag, com try/except — falha da fila NUNCA derruba o F0 (TDD §5).
3. Adicionar `forja_fila.py` ao manifesto da régua (`forja_regua.py`) e rodar a régua.
4. Documentar operação em `DOCUMENTACAO_TECNICA.md` (tabela "quero mudar X"): mudar pesos → PRD §5 + constante do módulo + teste; mudar léxico → constante + gate M0 re-rodado.
5. Encadeamento adicional (executado em 12/07): `update_dashboard_local.ps1` regenera a fila antes do
   `render_dashboard.py` — o ciclo do botão "Atualizar" mantém a fila fresca sem intervenção manual
   (elimina o selo "fila desatualizada" no uso normal). Mesmo isolamento: falha não derruba o ciclo.
6. **Gate M3:** dry-run ponta a ponta com flag on: reconcile → fila → painel → `--proxima` → caso correto; matar a fila no meio (arquivo travado) → F0 completa normalmente com aviso em stderr.

## M4 — Operação assistida e promoção (3h ao longo de 1 semana)

1. Ligar `filaPriorizadaV1: true`; rodar reconcile+fila no ciclo normal da semana.
2. A cada peça iniciada na semana, registrar: a fila apontou o caso certo? Alguma urgência real ficou fora do top 5? (anotação de 1 linha por evento, no próprio relatório da fila do dia — sem burocracia nova).
3. Recalibrar pesos se necessário (mudança = editar constante + atualizar PRD §5 + caso de teste novo).
4. **Gate M4 (critério de sucesso da Helena):** Igor responde "quais as próximas 5 peças?" olhando um único lugar, sem abrir pasta; nenhuma urgência manual `alta` fora do topo; zero regressão nos gates existentes na semana.
5. Fechar: lição na `RETROSPECTIVAS.md`, atualizar `INDICE_FORJA.md` e `planejamento/MAPA_IA.md`, registrar no painel de memória do projeto.

**Critério de reversão (rollback é configuração, não cirurgia):** se na semana de M4 a fila induzir UMA escolha errada de prioridade com consequência real (peça urgente atrasada), desligar a flag, registrar o caso como fixture de regressão e só religar com o teste passando.

---

## Dependências e pré-condições

- F0 (`forja_reconcile.py`) funcionando — já operacional.
- Nenhuma dependência Python nova (stdlib apenas, padrão da casa).
- Não depende de N4, não toca no pipeline F1-F10, não altera `demandas.json`.

## O que fica explicitamente para depois (não entra nestes 16h)

- **R1.2 da Helena** (telemetria de feedback com classe de erro, ~8h + 2 semanas de coleta) — próximo candidato após M4, decisão do Igor.
- **Disparo automático de produção** — anti-requisito do PRD §6; só reavaliá-lo com evidência de M4 + decisão expressa do Igor (risco de negócio).
- Cron/agendamento da fila — opcional; o ciclo manual+reconcile cobre a semana de validação.
