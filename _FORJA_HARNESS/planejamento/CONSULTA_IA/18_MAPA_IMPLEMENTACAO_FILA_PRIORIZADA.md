# Consulta IA — Mapa de implementação — FORJA FILA

> Cópia de consulta derivada. O documento canônico permanece no caminho de origem indicado abaixo.

## Metadados e rastreabilidade

- **Documento de origem:** `18_MAPA_IMPLEMENTACAO_FILA_PRIORIZADA.md`
- **Tipo:** Mapa
- **SHA-256 da origem:** `2e8657d9ace86e74cc343b909283fc98f5ab274b4fe13c7ef7e4e766c470f824`
- **Linhas da origem:** 76
- **Blocos integralmente indexados:** 9
- **Geração:** 2026-08-10T13:53:35-03:00
- **Cobertura:** 100% das linhas e do texto da origem, sem omissão.
- **Links relativos normalizados:** 0 destino(s), apenas para preservar a navegação na cópia.

## Roteiro de consulta para IA

**Síntese de localização:** Roadmap executável da R1.1 (Helena, 16h estimadas). Cada marco tem gate de saída objetivo; nenhum marco seguinte começa com gate anterior aberto. Tudo aditivo e reversível por flag — padrão N2/N3 da casa.

**Termos de recuperação:** fila, gate, painel, não, semana, flag, json, forja_fila, regressão, paralelo, reais, caso.

Use o índice abaixo para localizar o bloco pertinente. Cada entrada informa as linhas exatas no documento de origem. Para afirmações materiais, leia o bloco integral e confira o arquivo canônico pelo SHA-256.

## Índice detalhado e cobertura integral

- [SRC-S001 · L1–L4 · Mapa de implementação — FORJA FILA](#src-s001)
  - Assuntos: mapa, implementação, fila, marco, gate, roadmap, executável, helena
  - Trecho-guia: Roadmap executável da R1.1 (Helena, 16h estimadas). Cada marco tem gate de saída objetivo; nenhum marco seguinte começa com gate anterior aberto. Tudo aditivo e reversível por flag — padrão N2/N3 da casa.
  - SHA-256 do bloco: `ed702f9ddb17c5674bb1870073a08697270aaecb801c7978049686beb3f83110`
  - [SRC-S002 · L5–L18 · Visão geral](#src-s002)
    - Caminho: Mapa de implementação — FORJA FILA > Visão geral
    - Assuntos: flag, visão, geral, schema, casos, painel, ponta, marco
    - Trecho-guia: Total: 16h. M1 é o caminho crítico; M2 e M3 podem andar em paralelo após M1.
    - SHA-256 do bloco: `ad73209eb5c62ad101cdf83ace834c91b2c3e7796b16b6dd756a72aea16f867f`
  - [SRC-S003 · L19–L27 · M0 — Fundação (2h)](#src-s003)
    - Caminho: Mapa de implementação — FORJA FILA > M0 — Fundação (2h)
    - Assuntos: reais, fundação, json, leitura, contra, classificação, proposta, léxico
    - Trecho-guia: 1. Adicionar filaPriorizadaV1: false em FORJAN3CONFIG.json. 2. Escrever o schema de FILAPRIORIZADA.json (TDD §3) como constante documentada no módulo. 3. Rodar protótipo de leitura contra os 23 casos reais (só leitura, sem gravar em gestaoescritorio/): imprime classificação de pr
    - SHA-256 do bloco: `1ef0e56be7a51986c2c772f0162ee7a58ee0def667211bf7bbbb8f3bc343ae3f`
  - [SRC-S004 · L28–L34 · M1 — Motor + regressão (6h)](#src-s004)
    - Caminho: Mapa de implementação — FORJA FILA > M1 — Motor + regressão (6h)
    - Assuntos: motor, regressão, fila_, forja_fila, funções, puras, classificar_prontidao, pontuar
    - Trecho-guia: 1. forjafila.py: funções puras (classificarprontidao, pontuar, ordenar, montarfila) + main() com os 3 artefatos (R4), escrita atômica. 2. testforjafila.py: os 14 casos do TDD §7 (7 DEVEPEGAR + 7 NÃOPODETRAVAR), fixtures sintéticas, hoje injetado. 3. Relatório humano reports/FILAd
    - SHA-256 do bloco: `37ea01aa64b6b9fbd9c02d056737b8b7cac04e05edac2b74198502db0a0cff90`
  - [SRC-S005 · L35–L42 · M2 — Painel (3h) [paralelo com M3]](#src-s005)
    - Caminho: Mapa de implementação — FORJA FILA > M2 — Painel (3h) [paralelo com M3]
    - Assuntos: painel, json, atual, paralelo, render_dashboard, forja_fila, badge, gate
    - Trecho-guia: 1. secaofila() em renderdashboard.py lendo data/forjafila.json com degradação limpa (R5): arquivo ausente/malformado/flag off → painel byte-idêntico ao atual. 2. Top 5 + resumo de bloqueadas por motivo + badge 48h (R7) + badge prazo vencido + aviso de frescor (hash de origem ≠ de
    - SHA-256 do bloco: `5193220a293143a0ffb6a99c90f1b58391520741255acb8d7ea1411c5a240d0e`
  - [SRC-S006 · L43–L53 · M3 — Consumo e encadeamento (2h) [paralelo com M2]](#src-s006)
    - Caminho: Mapa de implementação — FORJA FILA > M3 — Consumo e encadeamento (2h) [paralelo com M2]
    - Assuntos: fila, encadeamento, mudar, consumo, paralelo, forja_fila, proxima, regenera
    - Trecho-guia: 1. forjafila.py --proxima: regenera e imprime o caso do topo; exit 3 se fila vazia (TDD §6). 2. Chamada opcional no fim de forjareconcile.main() sob flag, com try/except — falha da fila NUNCA derruba o F0 (TDD §5). 3. Adicionar forjafila.py ao manifesto da régua (forjaregua.py) e
    - SHA-256 do bloco: `64905ff6f5c050168690ead6b4e6b767cf81b8c74855173ec1b05ae1b598617b`
  - [SRC-S007 · L54–L65 · M4 — Operação assistida e promoção (3h ao longo de 1 semana)](#src-s007)
    - Caminho: Mapa de implementação — FORJA FILA > M4 — Operação assistida e promoção (3h ao longo de 1 semana)
    - Assuntos: semana, fila, registrar, caso, operação, assistida, promoção, longo
    - Trecho-guia: 1. Ligar filaPriorizadaV1: true; rodar reconcile+fila no ciclo normal da semana. 2. A cada peça iniciada na semana, registrar: a fila apontou o caso certo? Alguma urgência real ficou fora do top 5? (anotação de 1 linha por evento, no próprio relatório da fila do dia — sem burocra
    - SHA-256 do bloco: `751b5f8c0bee9a50f24a8109e3843fee055dec8ab85ce96439bc4570a691c1d3`
  - [SRC-S008 · L66–L71 · Dependências e pré-condições](#src-s008)
    - Caminho: Mapa de implementação — FORJA FILA > Dependências e pré-condições
    - Assuntos: não, dependências, pré-condições, forja_reconcile, funcionando, operacional, nenhuma, dependência
    - Trecho-guia: F0 (forjareconcile.py) funcionando — já operacional. Nenhuma dependência Python nova (stdlib apenas, padrão da casa). Não depende de N4, não toca no pipeline F1-F10, não altera demandas.json.
    - SHA-256 do bloco: `06291a79e82db83042100ac696911461249f99cde429e10affb8bb0568c25df6`
  - [SRC-S009 · L72–L76 · O que fica explicitamente para depois (não entra nestes 16h)](#src-s009)
    - Caminho: Mapa de implementação — FORJA FILA > O que fica explicitamente para depois (não entra nestes 16h)
    - Assuntos: fica, explicitamente, depois, não, entra, nestes, decisão, igor
    - Trecho-guia: R1.2 da Helena (telemetria de feedback com classe de erro, 8h + 2 semanas de coleta) — próximo candidato após M4, decisão do Igor. Disparo automático de produção — anti-requisito do PRD §6; só reavaliá-lo com evidência de M4 + decisão expressa do Igor (risco de negócio). Cron/age
    - SHA-256 do bloco: `fc6fcc6d5e2409ac1e723e5532c1785ae251b4a12d26f88556bd61c8902e22f9`

## Conteúdo integral indexado

Os marcadores HTML abaixo são apenas âncoras de navegação. O texto reproduz integralmente a origem normalizada em UTF-8; somente destinos de links relativos podem ter sido recalculados para apontar ao mesmo arquivo a partir desta pasta.

<a id="src-s001"></a>

# Mapa de implementação — FORJA FILA

Roadmap executável da R1.1 (Helena, 16h estimadas). Cada marco tem gate de saída objetivo; nenhum marco seguinte começa com gate anterior aberto. Tudo aditivo e reversível por flag — padrão N2/N3 da casa.


<a id="src-s002"></a>

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


<a id="src-s003"></a>

## M0 — Fundação (2h)

1. Adicionar `filaPriorizadaV1: false` em `FORJA_N3_CONFIG.json`.
2. Escrever o schema de `FILA_PRIORIZADA.json` (TDD §3) como constante documentada no módulo.
3. Rodar protótipo de leitura contra os 23 casos reais (só leitura, sem gravar em `gestao_escritorio/`): imprime classificação de prontidão proposta.
4. **Gate M0:** revisão humana da classificação proposta dos 23 reais — se ≥3 demandas caírem em categoria obviamente errada, revisar o léxico/regras ANTES de codificar o motor (barato corrigir aqui, caro depois).

Risco tratado: o léxico de `bloqueada_decisao_cliente` (regra 7) é a parte mais frágil — validado contra dados reais antes de virar código de produção.


<a id="src-s004"></a>

## M1 — Motor + regressão (6h)

1. `forja_fila.py`: funções puras (`classificar_prontidao`, `pontuar`, `ordenar`, `montar_fila`) + `main()` com os 3 artefatos (R4), escrita atômica.
2. `test_forja_fila.py`: os 14 casos do TDD §7 (7 DEVE_PEGAR + 7 NÃO_PODE_TRAVAR), fixtures sintéticas, `hoje` injetado.
3. Relatório humano `reports/FILA_<data>.md` com decomposição de score por fator (auditável de relance).
4. **Gate M1:** (a) suíte verde; (b) suítes existentes verdes (`test_forja_regua`, `test_forja_verificador`, `test_forja_citacoes`, `test_forja_conselho_1107`); (c) rodada sombra com dados reais gera fila que Igor/Efesto reconhecem como sensata — divergência vira ajuste de peso documentado, não gambiarra; (d) diff de `demandas.json` vazio (R1).


<a id="src-s005"></a>

## M2 — Painel (3h) [paralelo com M3]

1. `secao_fila()` em `render_dashboard.py` lendo `data/forja_fila.json` com degradação limpa (R5): arquivo ausente/malformado/flag off → painel byte-idêntico ao atual.
2. Top 5 + resumo de bloqueadas por motivo + badge 48h (R7) + badge prazo vencido + aviso de frescor (hash de origem ≠ demandas.json atual).
3. **Gate M2:** QA visual do painel (gate obrigatório da casa — nunca declarar pronto sem olhar o render); teste A/B: renderizar sem `forja_fila.json` e comparar com o painel atual (nenhuma diferença).

Fronteira: `render_dashboard.py` é o ÚNICO escritor do HTML (memória do projeto). Nenhum CSS novo — só classes existentes.


<a id="src-s006"></a>

## M3 — Consumo e encadeamento (2h) [paralelo com M2]

1. `forja_fila.py --proxima`: regenera e imprime o caso do topo; exit 3 se fila vazia (TDD §6).
2. Chamada opcional no fim de `forja_reconcile.main()` sob flag, com try/except — falha da fila NUNCA derruba o F0 (TDD §5).
3. Adicionar `forja_fila.py` ao manifesto da régua (`forja_regua.py`) e rodar a régua.
4. Documentar operação em `DOCUMENTACAO_TECNICA.md` (tabela "quero mudar X"): mudar pesos → PRD §5 + constante do módulo + teste; mudar léxico → constante + gate M0 re-rodado.
5. Encadeamento adicional (executado em 12/07): `update_dashboard_local.ps1` regenera a fila antes do
   `render_dashboard.py` — o ciclo do botão "Atualizar" mantém a fila fresca sem intervenção manual
   (elimina o selo "fila desatualizada" no uso normal). Mesmo isolamento: falha não derruba o ciclo.
6. **Gate M3:** dry-run ponta a ponta com flag on: reconcile → fila → painel → `--proxima` → caso correto; matar a fila no meio (arquivo travado) → F0 completa normalmente com aviso em stderr.


<a id="src-s007"></a>

## M4 — Operação assistida e promoção (3h ao longo de 1 semana)

1. Ligar `filaPriorizadaV1: true`; rodar reconcile+fila no ciclo normal da semana.
2. A cada peça iniciada na semana, registrar: a fila apontou o caso certo? Alguma urgência real ficou fora do top 5? (anotação de 1 linha por evento, no próprio relatório da fila do dia — sem burocracia nova).
3. Recalibrar pesos se necessário (mudança = editar constante + atualizar PRD §5 + caso de teste novo).
4. **Gate M4 (critério de sucesso da Helena):** Igor responde "quais as próximas 5 peças?" olhando um único lugar, sem abrir pasta; nenhuma urgência manual `alta` fora do topo; zero regressão nos gates existentes na semana.
5. Fechar: lição na `RETROSPECTIVAS.md`, atualizar `INDICE_FORJA.md` e `planejamento/MAPA_IA.md`, registrar no painel de memória do projeto.

**Critério de reversão (rollback é configuração, não cirurgia):** se na semana de M4 a fila induzir UMA escolha errada de prioridade com consequência real (peça urgente atrasada), desligar a flag, registrar o caso como fixture de regressão e só religar com o teste passando.

---


<a id="src-s008"></a>

## Dependências e pré-condições

- F0 (`forja_reconcile.py`) funcionando — já operacional.
- Nenhuma dependência Python nova (stdlib apenas, padrão da casa).
- Não depende de N4, não toca no pipeline F1-F10, não altera `demandas.json`.


<a id="src-s009"></a>

## O que fica explicitamente para depois (não entra nestes 16h)

- **R1.2 da Helena** (telemetria de feedback com classe de erro, ~8h + 2 semanas de coleta) — próximo candidato após M4, decisão do Igor.
- **Disparo automático de produção** — anti-requisito do PRD §6; só reavaliá-lo com evidência de M4 + decisão expressa do Igor (risco de negócio).
- Cron/agendamento da fila — opcional; o ciclo manual+reconcile cobre a semana de validação.
