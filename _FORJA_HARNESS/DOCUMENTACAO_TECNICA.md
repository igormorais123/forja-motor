# FORJA — Documentação técnica e mapa do código

> Escrito para OUTRAS IAs (e humanos) acharem qualquer parte do sistema, ajustarem com segurança e não recriarem o que já existe. Atualizado em **26/07/2026**, com a blindagem de lastro documental (§ 20) e a auditoria de regimentos (§ 21). Estado consolidado do sistema na § 22.
> Regra de ouro deste harness: **detecção agressiva, bloqueio conservador** — o verificador avisa muito (P1) e trava pouco (P0). Nunca transformar aviso em trava sem passar pela regressão (`test_forja_verificador.py`).

## 0. Estado real em 15/07/2026 — N3 implementada, promoção ainda controlada

A FORJA N3.0-r2 está implementada como camada aditiva. A N2 continua sendo a especificação vigente para os casos existentes; nenhuma peça histórica foi reescrita. O sidecar da gestão e a ponte de atualização estão ativos. Máquina de estados, executor, contexto, fidelidade, QA visual e fechamento canônico permanecem sob feature flags até os replays bloqueados serem corrigidos e três ciclos novos terminarem estáveis.

| Capacidade N3 | Módulo | Estado |
|---|---|---|
| eventos atômicos, revisão e reabertura formal | `forja_state_machine.py` | implementado em sombra |
| contratos F0-F10 e promoção isolada | `forja_run.py` + `phase_contracts/` | implementado em sombra |
| F2-A: 100 perguntas, 10 óticas, respostas e handoff | `forja_exploracao_100.py` + `F2_QUESTION_TREE.json` | **obrigatório em novos ciclos F2** |
| F7-B: revisão editorial e escrita final | `forja_editorial.py` (era `forja_fable5.py`) + `forja_editorial_fidelity.py` | **obrigatório antes de F8 em novas tentativas F7**; modelo padrão `claude-opus-5` desde 25/07/2026 |
| lastro documental verbatim (L1-L8) | `forja_lastro.py` | **bloqueante em F7 e na entrega** desde 26/07/2026 |
| atualidade dos regimentos arquivados | `forja_regimentos.py` | ativo; acervo em 16/16 desde 26/07/2026 |
| índice, cobertura, fatos, proposições e proveniência | `forja_context.py` | implementado em sombra |
| fidelidade Markdown→DOCX→PDF | `forja_fidelity.py` | implementado e obrigatório no pacote N3 |
| lint SVG, DOCX e PDF com revisor independente | `forja_visual_qa.py` + `medina_visual_lint.py` | implementado em sombra |
| pacote, draft, entrega e F10 por IDs/hashes | `forja_package.py` + `forja_close_cycle.py` | implementado em sombra |
| painel sem alterar `demandas.json` | `sync_forja_gestao.py` + `forja_status.json` | **ativo** |
| atualização após evento N3 canônico | `forja_management_bridge.py` | **ativa somente para caso diretamente em `state/`** |
| validação consolidada | `validate_forja_n3.py` | última execução completa publicada em 10/07: 11/11 grupos; reexecutar após mudanças |

Evidência atual: `reports/N3_SHADOW_REPLAY_2026-07-09.md` reproduziu 21/21 estados e preservou 21/21 hashes. Seis casos abriram bloqueio real: Plano de Saúde por regressão e fonte pendente; CASO-02, CASO-07, CASO-16, CASO-17 e CASO-19/Fábio por diagramas que o gate V2 rejeitou. O gate visual não foi ativado globalmente por essa razão.

Validação canônica:

```powershell
python validate_forja_n3.py --real-word --run-replay
```

O relatório fica em `reports/N3_VALIDATION_2026-07-10.json`. O teste real converte três produtos e 60 páginas em Word/PDF; a conversão agora ocorre em processo isolado, com limite de tempo, uma retomada e promoção atômica do PDF.

Regra de isolamento: eventos criados em diretório temporário, teste ou replay não podem atualizar o painel. A ponte valida que o caso está diretamente em `_FORJA_HARNESS/state/`. Se o sidecar contiver uma entrada N3 sem `FORJA_N3_STATE.json` canônico correspondente, `sync_forja_gestao.py --legacy --apply` restaura o estado N2 real. Essa regra possui regressão automatizada em `test_forja_n3_management.py`.

Rollback: desligar `managementSidecarV1` e `forjaManagementBridge` em `FORJA_N3_CONFIG.json`. Isso faz o painel ignorar novas sincronizações N3 sem apagar eventos, pacotes ou o sidecar e sem alterar `demandas.json`.

## 1. O que o FORJA é, em um parágrafo

Esteira que transforma um e-mail do escritório Medina Osório em minuta de peça jurídica revisável: baixa o comando e os anexos, lê os autos, planeja com conselho adversarial, redige, audita fatos e direito, entrega o texto auditado ao Claude Fable 5 para a revisão e escrita final, recompõe os gates de fidelidade, gera DOCX+PDF com QA visual página a página e deixa um RASCUNHO (nunca envia) no thread original do Gmail para o Igor revisar e encaminhar. Motor de IA: Claude Code com a assinatura OAuth do Igor (sem API paga). Tudo em "modo sombra": artefatos só em `_FORJA_HARNESS\state\<caseId>\`.

## 2. Mapa do pipeline de um caso (Mermaid)

```mermaid
flowchart TD
    A["E-mail do caso<br/>(pasta com COMANDO_DO_EMAIL.md + Anexos)"] --> B["forja_reconcile.py (F0)<br/>fila, pastas, evidências"]
    B --> B2["F2-A: forja_exploracao_100.py<br/>100 perguntas × 10 óticas<br/>respostas, lacunas e soluções"]
    B2 --> C["forja_sources.py (F3)<br/>tribunal + regimento + leis gerais"]
    C --> D["Workflow ultracode por caso<br/>(leitores de autos em paralelo → conselho de personas<br/>→ blueprint → redator → 4 auditores → revisão)"]
    D --> E["VERIFICAÇÃO INDEPENDENTE fora do workflow<br/>fatos vs PDFs (grep) + forja_citations.py (F5)<br/>+ cache/fontes_oficiais (verbatim)"]
    E --> FB["F7-B: forja_fable5.py<br/>Claude Fable 5 revisa e escreve o texto final<br/>hashes + fidelidade determinística"]
    FB --> F["forja_render_docx.py (F8)<br/>final_markdown → DOCX timbrado → PDF Word COM<br/>→ páginas PNG → contact sheet"]
    F --> G["forja_verificador.py (G1-G8)<br/>roda DENTRO do render — gates automáticos"]
    G --> H{"P0 não justificado?"}
    H -- sim --> E2["Corrigir a peça e re-render"] --> F
    H -- não --> I["QA visual página a página<br/>(inspeção humana/IA das PNGs)"]
    I --> J["gws gmail +reply --draft<br/>DOCX+PDF no thread original (NUNCA envia)"]
    J --> K["Painel: POST /api/comment<br/>+ retrospectiva em RETROSPECTIVAS.md"]
    K --> L["forja_delivery.py (F10)<br/>trilha de evidência de 8 elos"]
```

## 3. Mapa dos módulos e dependências (Mermaid)

```mermaid
flowchart LR
    subgraph FORJA["_FORJA_HARNESS (código)"]
        R[forja_reconcile.py<br/>F0 fila/auditoria]
        X[forja_exploracao_100.py<br/>F2-A perguntas/respostas/handoff]
        S[forja_sources.py<br/>F3 tribunal/regimento]
        C[forja_citations.py<br/>F5 citações]
        H[forja_headless.py<br/>claude -p OAuth]
        FB[forja_fable5.py<br/>F7-B Claude Fable 5]
        EF[forja_editorial_fidelity.py<br/>hashes + invariantes]
        RD[forja_render_docx.py<br/>F6/F8 render+QA]
        V[forja_verificador.py<br/>gates G1-G8]
        T[test_forja_verificador.py<br/>regressão]
        P[forja_pilot_m4.py<br/>piloto histórico M4]
        D[forja_delivery.py<br/>F10 trilha]
    end
    subgraph DADOS["dados e artefatos"]
        ST[("state/case-*/<br/>FORJA_STATE.json + producao/")]
        CF[("cache/fontes_oficiais/<br/>verbatim + raw/")]
        MAN[("FORJA_SPEC_MANIFEST.json<br/>fonte normativa")]
        RETRO[("RETROSPECTIVAS.md<br/>70 lições")]
    end
    subgraph EXTERNO["fora do harness"]
        TPL[("_FERRAMENTAS/TEMPLATE_MEDINA_OSORIO_PETICAO.docx")]
        WVP[word_visual_pipeline.py<br/>_FERRAMENTAS]
        GES[("gestao_escritorio/data/*.json<br/>painel — só leitura")]
        GMAIL[gws CLI → Gmail drafts]
    end
    R --> ST
    X --> ST
    R -.lê.-> GES
    S --> ST
    C --> ST
    C -.consulta.-> CF
    H --> ST
    FB --> EF
    EF --> ST
    RD --> ST
    RD -.usa.-> TPL
    RD -.importa.-> WVP
    RD ==chama==> V
    T ==testa==> V
    P -.usa.-> TPL
    D --> ST
    ST -.anexos.-> GMAIL
```

### 3-A. Camada N4 implantada

```mermaid
flowchart LR
    F2["F2-A: classificação + 100 perguntas<br/>10 óticas, respostas e soluções"] --> F3["F3: eventos, comparação e grafo"]
    F3 --> F4["F4: cobertura, teses, testes e cenários"]
    F4 --> F5["F5: fontes jurídicas e ciência interdisciplinar"]
    F5 --> F7["F7: testes, metacognição e consistência global"]
    F7 --> F7B["F7-B: Fable 5 + gates editoriais"]
    F7B --> F8["F8: fidelidade semântica e QA visual"]
    F8 --> F9["F9: arquivo selecionado = hash do pacote"]
    F9 --> F10["F10: evidência da entrega e aprendizado"]
    F10 --> Gestão["Sidecar e painel do escritório"]
```

Estado operacional após o Conselho de 11/07/2026: CASO-04, CASO-19/Fábio, CASO-16 e Saúde estão no piloto `pilot_blocking`. CASO-04 permanece bloqueada; os outros três são baselines retrospectivas mecanicamente reproduzidas, com zero P0, dois P1 de conselho por caso, `promotionEligible=false` e `legalReleaseStatus=human_review_required`. Os demais casos ficam em sombra. Relatório canônico: `reports/CONSELHO_SINTESE_IMPLEMENTACAO_FORJA_N4_2026-07-11.md`.

## 4. Índice — onde está cada coisa

| Caminho (relativo a `_FORJA_HARNESS\`) | O que é | Quando consultar |
|---|---|---|
| `forja_visual_build.py` | **Entrada única de produção visual** (gates F7 → brief → mapa → figuras → compor → montar → F8-S) | Toda entrega visual; nunca chamar `compor()` por fora |
| `forja_assinatura_visual.py` | Gate F8-S: verificação AFIRMATIVA de presença dos elementos no DOCX | Ao mexer em densidade, taxonomia VIS ou limiar de negrito |
| `..\_FERRAMENTAS\medina_svg_colisao.py` | Gate SVGC (bloqueante): oclusão, texto sobre texto, cor inválida, contraste | Ao alterar qualquer gerador de SVG ou investigar figura quebrada |
| `forja_calibra_monetario.py` | Calibração reexecutável da detecção de material econômico | Antes de tornar bloqueante qualquer gate econômico (plano 41) |
| `templates\F7_5_BRIEF_VISUAL.md` | Contrato do brief visual declarado pelo autor da peça | Toda peça com cronologia ou cadeia argumentativa |
| `FORJA_SPEC_MANIFEST.json` | Fonte normativa: fases F0-F10, milestones, componentes, regras | Antes de qualquer mudança de arquitetura |
| `RETROSPECTIVAS.md` | 103 lições numeradas, incluindo Conselho N4, anti-autocertificação e PSO-Pet | Antes de montar QUALQUER workflow novo |
| `APRENDIZADOS_CONSELHO_N4_2026-07-11.md` | Estado canônico, invariantes, pendências e métricas válidas da auditoria N4 | Antes de alterar ou promover a N4 |
| `RUNBOOK_VALIDACAO_CONSELHO_N4.md` | Comandos, critérios de aceite, interpretação e rollback | Depois de qualquer alteração N4 |
| `planejamento/14_METODO_VAN_AKEN_APLICADO_A_PETICOES.md` | Método completo de definição, diagnóstico, desenho, validação e aprendizado da petição | Antes do blueprint de casos completos ou intensivos |
| `templates/F4_METODO_SOLUCAO_PROBLEMA_PETICAO.md` | Roteiro interno preenchível do perfil PSO-Pet | Durante F2-F4 e nas reaberturas até F7 |
| `templates/F2A_EXPLORACAO_100_PERGUNTAS.md` | Contrato humano das 100 perguntas, respostas, hipóteses e handoff | Todo caso novo, após F1 e antes de F3/F4 |
| `forja_exploracao_100.py` | Andaime, CLI e validador determinístico F2-A | Inicializar e validar `F2_QUESTION_TREE.json` |
| `test_forja_exploracao_100.py` | Regressão de contagem, óticas, diversidade, lastro, bloqueio e rotas | Após qualquer mudança no protocolo F2-A |
| `planejamento/20_F2A_EXPLORACAO_100_PERGUNTAS.md` | Decisão arquitetural, posição no fluxo e compatibilidade | Antes de alterar contratos F2–F4 |
| `PROTOCOLO_EDITORIAL_ESCRITA_FINAL.md` | Runbook normativo da revisão e escrita final | Antes de executar ou alterar F7-B |
| `planejamento/21_F7B_FABLE5_REVISAO_ESCRITA_FINAL.md` | Decisão arquitetural, alternativas e compatibilidade de F7-B | Antes de alterar modelo, autenticação, retry ou invariantes |
| `docs/` | Guias de arquitetura, configuração, início, desenvolvimento e testes | Entrada técnica modular para manutenção |
| `forja_pso_pet.py` | Validador, indicadores vetoriais, auditoria de compatibilidade e benchmark PSO-Pet | Pilotos e auditoria de valor |
| `reports/RELATORIO_PSO_PET_SOLUCAO_PROBLEMAS_E_METRICAS_2026-07-11.md` | Resultado do benchmark real, métricas, limites e decisão de implantação | Antes de promover o perfil PSO-Pet |
| `reports/FORJA_EXPLICADA_PARA_ADVOGADOS.html` | Explicação navegável com 41 diagramas e linguagem voltada a advogados; o nome anterior permanece como endereço compatível | Compreender e apresentar a FORJA sem vocabulário de desenvolvimento |
| `C:\Users\IgorPC\.claude\projects\Forja visual 3d\reports_atlas_blender\` | Edição Blender 2D do atlas e auditoria comparativa V1/V2 — ARQUIVADAS fora do harness em 16/07/2026 (junto com o projeto 3D eliminado em 12/07) | Consultar apenas como histórico; a versão em uso é o atlas para advogados acima |
| `reports/ATLAS_VISUAL_FORJA_ATUAL_E_PSO_PET_2026-07-11.md` | Fonte Mermaid integral do atlas visual | Auditar ou atualizar os diagramas |
| `render_forja_atlas.py` | Render local e autocontido do Markdown/Mermaid para HTML, com zoom e navegação | Regenerar o atlas após mudança arquitetural |
| `DOCUMENTACAO_TECNICA.md` | Este arquivo — mapa e índices | Porta de entrada |
| `INDICE_FORJA.md` | Índice curto de 1 tela | Navegação rápida |
| `forja_verificador.py` | Gates G1-G8 (ver §6) | Ajustar detecção de erro |
| `test_forja_verificador.py` | Regressão do verificador (10 detecções + 8 não-travas) | OBRIGATÓRIO após mudar o verificador |
| `forja_render_docx.py` | Render md→DOCX+PDF+QA; chama o verificador | Ajustar formatação/QA |
| `forja_headless.py` | `claude -p` com OAuth (consultivo; orquestrador grava) | Rodar fase de IA sem workflow |
| `forja_fable5.py` | Passe F7-B pelo `claude-fable-5`, via assinatura OAuth, com prompt por stdin | Revisão editorial e escrita final do texto auditado |
| `forja_editorial_fidelity.py` | Recalcula hashes, evidência OAuth, títulos, retenção mínima e preservação de números, citações, pedidos, marcadores e ressalvas | Bloquear mudança material antes de F8 |
| `forja_reconcile.py` | F0 — audita fila de demandas em modo sombra | Reconciliar fila/painel |
| `forja_sources.py` | F3 — tribunal, regimento, leis gerais | Caso novo/pasta nova |
| `forja_citations.py` | F5 — extrai citações de DOCX/MD e confere no cache | Auditoria de citações |
| `forja_legal_search.py` + `FORJA_SEARCH_CONFIG.json` | Ponte JSON auditável para o TeiaJus: busca, processo, coleta, ranking, TJDFT/TRF1 e STJ (10 espelhos + Diário/íntegra + DataJud) | Pesquisa F5 e comando do Sistema de Busca Jurídica |
| `forja_delivery.py` | F10 — trilha de evidência de 8 elos + pacote de revisão | Fechar entrega |
| `forja_pilot_m4.py` | Piloto histórico do M4 (mantido como referência; produção usa o render) | Arqueologia |
| `cache/fontes_oficiais/*.txt` | Enunciados VERBATIM com fonte e data (súmulas STF/STJ, Tema 1368, art. 406 CC, Lei 14.905, Selic BCB) | Antes de citar qualquer fonte |
| `cache/fontes_oficiais/raw/` | Capturas brutas das páginas (auditoria da extração) | Conferir procedência |
| `state/case-<id>/producao/` | Peça .md, DOCX, PDF, páginas PNG, e-mail, relatório | Retomar/da revisar um caso |
| `state/case-<id>/FORJA_STATE.json` | Estado do caso (fases, gates, artefatos) | Diagnóstico de caso |
| `planejamento/01..06_*.md` | Spec N2 (PRD, TDD, roadmap, diagramas, análise, gates) | Comparar executado × planejado |
| `planejamento/10..13_*.md` | PRD, TDD, roadmap e diagramas finais da candidata N4 | Arquitetura de raciocínio, prova, ciência e entrega |
| `forja_n4_validate.py` | Validação agregada de schema, envelope, conteúdo e relações | Antes de promover fase ou fechar pacote N4 |
| `forja_reasoning.py` / `forja_consistency.py` | Questões, cobertura, grafo, terminologia, tempo, cálculo e consistência | Auditoria estrutural do caso |
| `forja_science.py` | Pesquisa e auditoria científica interdisciplinar | Quando a tese depende de conhecimento não jurídico |
| `forja_delivery_integrity.py` | Seleção F9 e confirmação F10 pelo hash | Antes e depois da entrega |
| `n4_schemas/` / `phase_contracts_n4/` | Contratos executáveis da N4 | Evolução sem substituir contratos N3 |
| `reports/` | Relatórios de reconciliação, implementação, Conselho e anti-autocertificação | Auditoria e histórico das decisões |

Fora do harness: template timbrado e pipeline visual em `..\_FERRAMENTAS\`; regimentos nas pastas dos casos; painel em `..\gestao_escritorio\` (HTML sempre gerado por `render_dashboard.py`, nunca editar direto); aprendizados de feedback humano em `..\APRENDIZADOS_FEEDBACK_HUMANO.md`.

### Integração com o Sistema de Busca Jurídica (TeiaJus)

- Diagnóstico: `python forja_legal_search.py capabilities` e `python forja_legal_search.py health`.
- Busca: `python forja_legal_search.py search "termos" --tribunal TJSP --limit 20 --artifact-dir <attempt-dir>`.
- Processo: `python forja_legal_search.py case <numero-cnj> --artifact-dir <attempt-dir>`.
- STJ: `stj-health`; `stj-catalog --include-resources`; `stj-search "termos" --orgao primeira_turma`; `stj-daily "REsp" --include-text`; `stj-datajud --source-timeout 5`.
- Coleta STJ mutável: `--db <banco> stj-collect --max N --allow-mutation`.
- Recursos mutáveis usam `execute <acao> --params '<json>' --allow-mutation`; sem a flag, a ponte falha fechada.
- Cada chamada grava telemetria em `telemetria/legal_search/`. Com `--artifact-dir`, grava `F5_TEIAJUS_SEARCH_<requestId>.json`, sempre `internal_working`.
- O resultado do TeiaJus não autocertifica citação: uso na peça continua bloqueado pelos gates de fonte oficial, literalidade, identidade do ato e atribuição da F5/F7. `textGaps` do STJ bloqueia alegação sobre a íntegra ausente.

## 5. "Quero ajustar X" → mexa em Y

| Quero... | Arquivo | Onde |
|---|---|---|
| Adicionar persona/jargão proibido | `forja_verificador.py` | listas `PERSONAS` / `JARGAO` |
| Aprovar novo marcador deliberado | `forja_verificador.py` | lista `PLACEHOLDER_OK` |
| Ensinar novo par súmula×tribunal | `forja_verificador.py` | sets `SUMULAS_STJ` / `SUMULAS_STF` |
| Adicionar dispositivo notório trocado | `forja_verificador.py` | lista `DISPOSITIVOS_ERRADOS` |
| Adicionar instituto direcional | `forja_verificador.py` | `INSTITUTOS_DIRECIONAIS` (+ negações em `NEGACOES_G5`) |
| Mudar severidade de um gate | `forja_verificador.py` | função `gate_gN` — e rodar a regressão! |
| Mudar fonte/margem/recuo do Word | `forja_render_docx.py` | função `render()` (Pt/Cm) |
| Mudar detecção de assinatura/título | `forja_render_docx.py` | `eh_assinatura()` |
| Trocar modelo/timeout do headless geral | `forja_headless.py` | constantes `MODELO` / `TIMEOUT_S` |
| Ajustar o passe final editorial (F7-B) | `forja_editorial.py` + `forja_editorial_fidelity.py` | prompt, timeout e invariantes F7-B; modelo dentro da allowlist de `forja_editorial_model.py` e sempre OAuth |
| Mudar gate de lastro documental | `forja_lastro.py` | gate novo exige falha real nomeada + caso de detecção **e** de não-trava (`test_forja_lastro.py`) |
| Auditar atualidade de regimento | `forja_regimentos.py` | `RUNBOOK_AUDITORIA_REGIMENTOS.md`; padrão de cabeçalho novo está lá |
| Acrescentar fonte oficial ao cache | `cache/fontes_oficiais/` | arquivo novo com cabeçalho FONTE/URL/data; bruto em `raw/` |
| Mudar regra de fase/gate normativo | `FORJA_SPEC_MANIFEST.json` | e refletir aqui e no CLAUDE.md da fábrica |
| Ligar/desligar módulo N4 ou escolher piloto | `FORJA_N3_CONFIG.json` | `features.n4*`, `n4.mode` e `n4.pilotCases` |
| Alterar schema/contrato N4 | `generate_n4_contracts.py` + `forja_n4_common.py` | regenerar e rodar `test_forja_n4.py` |
| Auditar autocertificação N4 | `forja_n4_e2e_adversarial.py` + `forja_n4_anti_fraud_audit.py` | rodar o runbook completo e conferir matriz de confusão |
| Interpretar baseline/conselho/promoção | `APRENDIZADOS_CONSELHO_N4_2026-07-11.md` | não confundir aprovação estrutural com liberação |
| Registrar lição nova | `RETROSPECTIVAS.md` | numerar sequencialmente; se determinística, virar gate + caso na regressão |
| Mudar pesos/fatores do score da fila | `forja_fila.py` | função `pontuar` + PRD `planejamento/15` §5 + caso novo em `test_forja_fila.py` |
| Ampliar léxico de decisão do cliente (fila) | `forja_fila.py` | constante `LEXICO_DECISAO_CLIENTE`; validar contra casos reais (`--dry`) |
| Ligar/desligar a fila priorizada | `FORJA_N3_CONFIG.json` | `features.filaPriorizadaV1` (off = painel e pipeline idênticos) |

## 6. Gates e política anti-trava

| Gate | Detecta | Severidade | Racional |
|---|---|---|---|
| G1 | personas internas (Helena, Efesto...) e jargão de processo | P0 / P1 (jargão) | nome interno em peça = vazamento certo |
| G2 | placeholders | P0 só p/ dado esquecido (`[NOME]`, `[OAB]`...) e `[BLOQUEADOR...]`; `[dia]` e marcadores deliberados = P1 | não travar o fluxo por marcador consciente |
| G3 | contagem agregada sem fonte/método | P1 | pode ser legítima; humano decide |
| G4 | súmula no tribunal errado; dispositivos notórios trocados | P0 | erro objetivo |
| G5 | instituto jurídico na direção errada (execução fiscal por particular etc.) | P0, com lista de negações (texto que NEGA o instituto passa) | erro conceitual grave |
| G6 | emojis (P0); separadores `---` no fonte (P1 — o render já os ignora); fecho "FIM DO DOCUMENTO" | P0/P1 | cara de IA |
| G7 | intervalo de datas declarado ≠ recalculado | P0 | aritmética objetiva |
| G8 | peça sem endereçamento/assinatura | P1 | aviso de formato |

Regras: (1) exit code 1 só com P0; (2) TODA mudança no verificador passa por `python test_forja_verificador.py` — a lista `NAO_PODE_TRAVAR` é tão importante quanto a `DEVE_PEGAR`; (3) P0 pode ser aceito conscientemente, mas a justificativa vai no relatório de entrega do caso.

## 7. Auditoria crítica de 09/07/2026 — achados e decisões

**Corrigido nesta rodada** (custo baixo, ganho real):
- `forja_citations.py`: import morto `unicodedata` removido.
- `forja_headless.py`: timeout e saída não-JSON agora produzem erro claro (antes: exceção crua sem contexto).
- `forja_render_docx.py` e `forja_pilot_m4.py`: guarda explícita se o template do escritório sumir (antes: erro críptico de zipfile).
- Render: separador `---` de markdown não vaza mais como texto no Word.
- Temporários de scraping removidos; capturas brutas movidas para `cache/fontes_oficiais/raw/`.

**Rejeitado conscientemente** (anti-excesso — reavaliar só se a dor aparecer):
- *Extrair `forja_utils.py`* com `now_iso`/`read_json`/`append_unique` (6 duplicatas): são funções de 2-5 linhas ("cola"); centralizar criaria acoplamento entre módulos hoje independentes e um ponto único de quebra. Duplicação aceita e documentada.
- *Refatorar as 3 funções longas* (`processar_caso`, `render`, `montar_piloto`): funcionam e foram validadas em 5 casos reais; refatorar sem suíte de testes é risco sem ganho imediato. Pré-condição para mexer: escrever testes de característica antes.
- *Suítes de teste para todos os módulos*: o ponto crítico (verificador) tem regressão; os demais são exercitados a cada caso real. Custo > benefício agora.

**Auditoria geral Efesto (09/07, madrugada)** — evidência executada, não opinião:
- Regressão do verificador verde (10 detecções + 8 não-travas); os 6 módulos importam sem erro.
- Os 5 rascunhos conferidos VIVOS no Gmail (`gws drafts list`) com thread ids corretos.
- Painel: JSONs válidos (BOM em `status_integracoes.json`/`whatsapp_candidates.json` é tolerado por design — todos os leitores usam `utf-8-sig`); HTML regenerado pela API a cada comentário.
- Cache de fontes: 15/15 arquivos com cabeçalho FONTE/URL/data. Manifest válido.
- **Corrigido**: 6 FORJA_STATE.json defasados sincronizados com a realidade (5 entregues → `draft_awaiting_review` com draftId; CASO-12 CASO-12 → `blocked`); estado do CASO-02 criado retroativamente (produção existia sem estado — P0) e o case duplicado `case-email-auto-19f3ed5bdbdcf159` marcado `superseded` apontando para o canônico.
- **Falso positivo do auditor-agente descartado**: "5 referências quebradas de planejamento" não existem (a doc usa o glob correto `01..06_*.md`) — ver Lição 34.
- **Tolerado**: case CASO-04 AgInt em F10 sem pasta `producao/` (entrega histórica está em `..\gestao_escritorio\entregas_fabio_osorio\`); sonda `drive_access_probe` do caso CASO-17 mantida como evidência de inacessibilidade do Drive.

**Aplicação da auditoria externa Efesto/5.5 (09/07, `reports/RELATORIO_EFESTO_AUDITORIA_FORJA_PETICOES_2026-07-09.md`)**:
- **Circuito F7→F10 FECHADO** (recomendação central do relatório): `forja_render_docx.py` persiste `F7_VERIFICADOR_FORJA.json` na pasta de produção; `forja_delivery.py` ganhou o elo 9 bloqueante (`p0 == 0`) — peça com P0 não fecha F10. Testado ponta a ponta com caso descartável.
- **P0 CASO-16 confirmado e corrigido**: rótulo estrutural "IDENTIFICAÇÃO DO PROCESSO" estava no DOCX entregue; removido, re-render limpo, rascunho substituído (r-2094364308504934560).
- **CASO-07**: todas as menções a "13 inquéritos" amarradas à origem (e-mail do escritório, item 16) + léxico de fonte do G3 ampliado; rascunho substituído (r-9065022275353955467).
- **Gates F3 defasados fechados por evidência**: o REGIMENTO_INTERNO_TJRJ.md JÁ EXISTIA na pasta do caso CASO-19/Fábio (gate não fora atualizado); CASO-17 classificado como produto consultivo (parecer/quesitos — sem tribunal de endereçamento; reabrir o gate se o parecer final identificar processo concreto).
- **Distinção de status (pedida pelo relatório)**: `fulfilled` em `F0_RECONCILIACAO_FILA` = cumprimento por reconciliação/`manual_override` de demanda histórica, NÃO esteira F0-F10 completa; `fulfilled` só significa peça auditada quando `currentPhase = F10...` com trilha. Não normalizar estados legados em massa.
- **F7 standalone**: casos entregues sem re-render nesta rodada (CASO-19/Fábio, CASO-17, CASO-02) receberam `F7_VERIFICADOR_FORJA.json` gerado avulso (0 P0; CASO-02 com o P1 `[dia]` deliberado — preencher no protocolo é item do checklist F9/F10).

**Pequenas inconsistências conhecidas e toleradas**: `merge_gates` existe só em `forja_sources.py` (citations usa `merge_by_id`) — comportamentos ligeiramente diferentes de deduplicação, sem efeito prático observado; `read_json` tem nomes de parâmetro diferentes entre módulos (`fallback` × `fb`).

## 8. Executado × planejado (spec N2)

| Plano (manifest/planejamento 01-06) | Executado | Δ |
|---|---|---|
| M0-M5 (reconcile → delivery) | Todos concluídos e registrados no manifest | ✔ conforme |
| Motor: headless OAuth consultivo por fase | Casos reais usaram **workflows ultracode multiagente** + verificação independente externa — mais forte que o previsto | evolução acima do plano; headless mantido para fases pontuais |
| F6 redação sobre template | `forja_render_docx.py` substituiu o piloto M4 (que fica como referência) | ✔ evolução prevista |
| Gates de qualidade (06_GATES) | Parte determinística virou CÓDIGO (`forja_verificador.py` G1-G8, integrado ao render) | acima do plano |
| Fontes oficiais | Cache verbatim com data + rotas mapeadas (BCB/Planalto diretos; SCON/STF via Chrome real) | acima do plano |
| Ingestão Gmail contínua em sombra | **NÃO implementada** — decisão: ingestão manual por caso enquanto o volume é baixo | pendência deliberada |
| Orquestrador automático da fila | **NÃO implementado** — loop é conduzido pela sessão (humano no circuito) | pendência deliberada |
| Verificação de citações 100% automática | Parcial: cache + forja_citations; SCON com desafio anti-bot exige navegador | limite externo conhecido |

## 9. Números da produção (lote 1, 08-09/07/2026)

5 casos entregues como rascunho no Gmail (CASO-16, CASO-19/Fábio, CASO-07, CASO-17, CASO-02), 1 bloqueado por documento externo (CASO-12 CASO-12). Padrão confirmado: nenhuma peça saiu protocolável direto do workflow — a verificação independente externa achou erro material em 5 de 5 casos (dois com achado que MUDOU a peça: Tema 1368 transitado e fatores Selic oficiais). É por isso que os gates existem e por isso a verificação em fonte oficial não é opcional.

## 9-A. Camada visual law (PADRÃO das entregas desde 09/07/2026 — ordem do Igor)

Toda peça/documento entregável sai na **edição visual law** do padrão `padrao-visual-medina` (skill em `~\.claude\skills\`). O fluxo:

1. **Conteúdo congelado**: o md auditado da pasta `producao/` NUNCA muda nesta fase.
2. **Mapa visual**: `producao/_visual/compor_<caso>_mapa.py` — dicionário `MAPA` declarativo (pull quotes, caixas, figuras, rótulos de síntese, linhas-síntese). Pode ser escrito por agente: as âncoras são validadas contra o md e o corpo é protegido pelo gate.
3. **Composição**: `forja_visual.py: compor(md, docx, MAPA)` — o texto entra por EXTRAÇÃO do md (fidelidade por construção); **gate de fidelidade embutido** aborta se 1 parágrafo faltar (Lição 37: agentes que transcrevem resumem — 5 de 5 reprovados na auditoria). O fólio áureo (identidade oculta do escritório) é aplicado automaticamente pelo kit; `tipo: "estudo"` no MAPA desliga o fólio (estudo/parecer interno não é peça protocolável) — implementado em 09/07/2026.
4. **Diagramas**: SVGs com `medina_svg_kit` (fontes ≥ 9px; números SEMPRE conferidos contra o md).
5. **Montagem**: `_FERRAMENTAS\montar_visual.py: montar(docx, figs)` — SVG→EMF (gate de legibilidade), inserção Word COM, PDF, páginas de QA; `anti_placeholder(pdf)` no final.
6. **QA visual página a página** (inegociável) e só então o rascunho no Gmail.
7. **Gate F10**: o `forja_delivery.py` tem elo bloqueante 4-B — sem um `*VISUAL_LAW*.docx` na pasta de produção (ou do caso), a demanda não fecha (adicionado 09/07/2026). Desde 11/07/2026 (conselho quadripartite, Lição 61) o elo exige também LASTRO: `forja_visual.py` grava `FIDELIDADE_VISUAL.json` (docxSha256/mdSha256) após o gate de fidelidade, e o elo 4-B recomputa o hash do DOCX — versão errada/alterada não fecha; composições pré-gate valem por evidência legada. Na mesma data: elo 2 valida que o F3 CITA o regimento do tribunal (lição CASO-16), e trilha reprovada grava `trilhaBloqueadores` no FORJA_STATE.json + exit code 2 (Lição 62). Regressão: `test_forja_conselho_1107.py`.

`forja_render_docx.py` permanece para render simples + gates (F7); o verificador roda sobre o MESMO md, então vale para as duas saídas.

## 10. Monitoramento vivo (painel de estágio)

O acompanhamento de estágio de cada demanda vive no painel do escritório, NÃO neste arquivo:

- **Fonte de dados**: `..\gestao_escritorio\data\demandas.json` (base) + `data\intervencoes_manuais.json` (comentários e overrides de status).
- **HTML**: `..\gestao_escritorio\PAINEL_ESCRITORIO_MEDINA_OSORIO.html` — gerado por `scripts\render_dashboard.py`; **nunca editar direto**.
- **Como atualizar estágio**: `POST http://127.0.0.1:8765/api/comment` com `{"id": "<demanda>", "text": "...", "autor": "FORJA/ONIR"}` — o servidor grava, aplica e re-renderiza o HTML automaticamente. Status: `POST /api/item-status` (`aberta`/`cumprida` — só marcar cumprida com evidência de entrega ao Fábio).
- **Convenção FORJA**: todo avanço de fase de um caso gera 1 comentário "Estágio DD/MM: ..." na demanda correspondente. Rascunho no Gmail = demanda continua `aberta` (cumprida só após Igor revisar e enviar).
- **Regra da Lição 33**: atualizar o `state/case-*/FORJA_STATE.json` (fase, status, deliveryEvidence com draftId) é passo obrigatório do pós-workflow — a produção via workflow NÃO atualiza o estado sozinha.
- Última sincronização completa de estágio: 09/07/2026 (7 demandas atualizadas: 5 entregues, 1 bloqueada, 1 protocolo de aprendizados).

## 11. Upgrades estado da arte 2026 (executados em 09/07/2026)

Plano completo com adoções, rejeições e critérios: `planejamento/07_PLANO_UPGRADE_ESTADO_DA_ARTE_2026.md` (seção 4 traz o status de execução). Módulos novos e pontos de contato:

| Módulo | Papel | Quando roda |
|---|---|---|
| `forja_injection_scan.py` + `test_forja_injection.py` | detecta injeção indireta de prompt em PDFs (fonte <2pt, cor invisível, padrões de instrução PT/EN); achado vira P0 de triagem humana em `F1_INJECTION_SCAN.json` | ingestão F1, antes de qualquer leitor engolir PDF de terceiro |
| `BLINDAGEM_IDPI` em `forja_headless.py` | prefixo inviolável em todo prompt de fase: conteúdo dos autos é dado, nunca instrução | toda chamada headless |
| `test_forja_citacoes.py` + `conferir_aspas` em `forja_citations.py` | regressão de veneno de citação — um caso por modo da taxonomia de 6 falhas (inexistente, nome trocado, misquote, pincite, tese deturpada, precedente superado) | após qualquer mudança no processo de conferência |
| `forja_metricas_f7.py` (+ `test_f7_campos.py`) | enriquece `F7_VERIFICADOR_FORJA.json`: citações não conferidas nominalmente, pontos a conferir remanescentes, campo de vigência das autoridades decisivas | dentro do render (`forja_render_docx.py`) |
| `forja_diff_docx.py` | diff pós-entrega protocolada × nossa, pré-classificado (formato / estilo-voz / conteúdo jurídico), pronto para `APRENDIZADOS_FEEDBACK_HUMANO.md` | quando a versão protocolada voltar (Diretriz nº 5 do Fábio) |
| `forja_learning.py` (`feedbackAssimilation`) | agrupa a rajada conversacional sem guardar conteúdo bruto, distingue texto humano de material importado e registra, tese por tese, quem suscitou, selecionou, validou e decidiu | em F10 após feedback ou retorno de versão humana; também antes de promover aprendizado amplo. **Estado em 06/08/2026: validador e contrato existem, produtor não — zero artefatos no disco.** A correção que chega em prosa é registrada por `F10_RETORNO_SEM_ANEXO.json` e triada por pessoa (§ 25.3) |
| `forja_aprendizado.py` (+ `test_forja_aprendizado.py`) | a correção humana vira regra aplicada e conferida: `padroes`, `amostra`, `adotar`, `aplicar`, `conferir`, `revalidar` | depois de todo retorno; `conferir` roda no gate 5-B do F10 (§ 25) |
| `..\_MODELOS\LEIA-ME.md` | peça-modelo aprovada por tipo, lida INTEIRA antes de redigir (sem RAG) | blueprint/redator, antes da redação |

Protocolo (sem código): taxonomia de 6 modos, red team com 9 perguntas, tabela de lastro das proposições decisivas e bloco "Pontos que exigem o seu olho" no e-mail — tudo em `planejamento/06_GATES_QUALIDADE_FORJA.md` e no checklist de `..\APRENDIZADOS_FEEDBACK_HUMANO.md`. Rejeições com fundamento (não reabrir sem fato novo): RAG/GraphRAG, governança de confidencialidade por IA, LLM-as-judge, RCT interno, firewall de saída dedicado, DataJud/Sinapses, rerankers de domínio.

O `feedbackAssimilation` é uma extensão compatível de `F10_HUMAN_DIFF_CLASSIFICATION.json`.
Ele contém apenas IDs e sínteses sanitizadas: `conversationUnits`, `signals`, `contributions` e
`workflowChanges`. Conteúdo bruto, transcrição ou citação literal de WhatsApp é P0. Inferência sobre
preferência ou personalidade nunca se autopromove; regra de escritório/global exige aprovação e duas
evidências independentes. Tese adicionada ou fortalecida só pode ser marcada `external_ready` com fonte
jurídica e decisão registrada, ainda que tenha origem humana.

## 12. Conselho obrigatório Helena + Cícero (ordem do Igor, 09/07/2026)

Toda peça (manual ou FORJA) exige, ANTES da redação final, parecer escrito das skills `/helena`
(estratégia: prioridade, riscos de negócio, alinhamento com o objetivo do cliente) e `/cicero`
(jurídico: cabimento, juridicidade, compliance OAB, blindagem recursal, ética), cada um com
recomendações numeradas e decisão registrada por recomendação (acatada/rejeitada/por quê).
Arquivos canônicos: `F4_PARECER_HELENA.md` e `F4_PARECER_CICERO.md` em `state/<caseId>/`.
Enforcement em três camadas: gate G5.7 (`planejamento/06_GATES_QUALIDADE_FORJA.md`), item do
checklist de `..\APRENDIZADOS_FEEDBACK_HUMANO.md` e elo 10 BLOQUEANTE do `forja_delivery.py`
(testado em 09/07 com caso descartável: sem pareceres reprova, com pareceres aprova o elo).
O relatório de melhorias da peça resume os dois pareceres e as decisões tomadas.

## 13. Auditoria adversarial e pontos decisivos — A1 (10/07/2026)

Peças que respondem manifestações adversárias têm uma trilha própria e bloqueante. O módulo `forja_adversarial_audit.py` inventaria e confere citações da parte contrária, cruza fatos e posições, registra contradições, qualifica indícios de má-fé e exige consequência concreta para qualquer ponto classificado como decisivo.

| Fase | Artefato | Conteúdo mínimo |
|---|---|---|
| F3 | `adversarial_audit` | leitura integral, pedidos, citações, fontes oficiais, contradições, indícios e pontos decisivos |
| F4 | `adversarial_strategy` | decisão por achado, contribuição de Helena/Cícero e autorização de linguagem sensível |
| F7 | `adversarial_recheck` | tentativa de falso positivo, hipótese inocente e revisão das alegações externas |

`forja_headless.py` acrescenta o protocolo a todo prompt F3/F4/F7; `forja_run.py` valida antes de promover; `forja_package.py` vincula os três registros por hash; `forja_delivery.py` acrescenta o elo 11 às novas peças reconhecidas como resposta. “Não localizado” exige dois canais oficiais documentados e jamais equivale automaticamente a “inexistente”. O protocolo completo está em `planejamento/09_AUDITORIA_ADVERSARIAL_PONTOS_DECISIVOS.md`; a regressão fica em `test_forja_adversarial_audit.py`.

## 14. FORJA FILA — priorização painel → FORJA (implementada em 12/07/2026)

R1.1 do parecer Helena (`reports/conselho_2026-07-11/RELATORIO_HELENA.md`), aprovada pelo Igor.
Motor: `forja_fila.py` (score determinístico e explicável; a fila PROPÕE, o humano dispara).
Artefatos: `state/FILA_PRIORIZADA.json` (canônico) + `reports/FILA_<data>.md` (humano) +
`gestao_escritorio/data/forja_fila.json` (painel; seção "Próximas peças (FORJA)" com degradação
limpa — sem o arquivo, o painel fica idêntico). Encadeada em DOIS pontos, ambos com isolamento de falha: fim do `forja_reconcile.py` (F0) e ciclo de
atualização do painel (`gestao_escritorio/scripts/update_dashboard_local.ps1`, antes do render —
o botão "Atualizar" sempre entrega fila fresca), sob a flag `filaPriorizadaV1`. Consumo: `python forja_fila.py --proxima`
(exit 3 se não houver demanda pronta). Regressão: `test_forja_fila.py` (21 casos). Planejamento:
`planejamento/15..18_*FILA_PRIORIZADA.md`. Anti-requisitos (não reabrir sem fato novo): disparo
automático de produção, escrita em `demandas.json`, LLM no score, daemon próprio.

**Política de calendário (feedback Igor, 12/07/2026 — INVIOLÁVEL):** marco interno de
engenharia/FORJA NUNCA vira evento ou alarme no Google Calendar do Igor — o calendário é dele,
para compromissos humanos reais (audiência, prazo processual, reunião). Pendência interna de
acompanhamento vive DENTRO da FORJA: `FORJA_N3_CONFIG.json -> fila.operacaoAssistidaAte` +
`pendencia_operacao_assistida()` no `forja_fila.py` — aparece no rodapé da seção do painel e no
relatório diário da fila; quando vence, vira selo âmbar persistente até o fechamento (sem push,
sem alarme). Para encerrar o acompanhamento: remover a chave `fila.operacaoAssistidaAte` do config.

## 15. Melhorias do plano 19 (implementadas em 12/07/2026)

Plano: `planejamento/19_PLANO_INSTALACAO_MELHORIAS_FORJA_2026-07-12.md` (M1-M4).
(O projeto irmão de visualização 3D foi eliminado por decisão do Igor em 12/07 — não reabrir.)

- **M1.1 Alertas P0** — `forja_alertas.py`: `notificar_p0()` publica comentário `forja-p0`
  na demanda do painel (`intervencoes_manuais.json`, com lock do office_io), log global em
  `reports/ALERTAS_P0.jsonl`, dedupe 6h por (caso, gate), fallback durável em
  `state/<caso>/ALERTAS_PENDENTES.jsonl` (drenar: `python forja_alertas.py --drenar <case_dir>`).
  Integrado no `forja_delivery.py` (reprovação da trilha) e `forja_verificador.py --case-dir`.
  Fail-open em todos os caminhos. Regressão: `test_forja_alertas.py` (9 casos).
- **M1.2 LocalContext** — `forja_local_context.py` (hook SessionStart em `.claude/settings.json`
  desta pasta): injeta resumo vivo da fila (ativos, fase, P0/P1, prazo, idade) ao abrir sessão.
- **M1.3 Métricas de gates** — `python forja_metricas_gates.py` →
  `reports/METRICAS_GATES.json` (ranking de gates, tempo médio por fase, P0 abertos);
  ranking de gates, tempo médio por fase e P0 abertos para consumo do painel.
- **M2.1 Ordem dos pareceres** — `parecer_antes_da_redacao()` no `forja_delivery.py`:
  parecer Helena/Cícero nascido DEPOIS do início do F6 reprova o elo 10 com
  `PARECER_POS_REDACAO` (ordem do Igor 09/07, lição 62). Corte: F6 iniciado antes de
  12/07/2026 segue a regra antiga. Regressão: `test_forja_ordem_parecer.py` (6 casos).
- **M3.3 Runbook prospectivo** — `RUNBOOK_CICLO_PROSPECTIVO.md`: checklist do ciclo com
  congelamento pré-redação; contagem de ciclos válidos (0/3 em 12/07).

### 15-b. M3 e M4 (implementados na tarde de 12/07/2026)

- **M3.1 Mutação semântica** — `python forja_mutation_semantic.py <caso>` →
  `n4_artifacts/F7_SEMANTIC_MUTATION.json`. Operadores S1-S6 determinísticos
  (inversão de tese, troca de parte, valor/data, pedido, sobreabstração,
  deturpação de precedente) + controles benignos que não podem morrer.
  Canais de morte: suíte de testes do caso + verificador (novo P0 vs baseline).
  GATE DE SANIDADE anti-autocertificação: suíte que reprova o ORIGINAL invalida
  o canal case_test (primeiro run real dava 24/24 falso com a minuta errada —
  o texto canônico é `n4_cycle_m6/CANONICAL_TEXT_FROM_FINAL_DOCX.txt`).
  Baselines 12/07: CASO-19 0.17, CASO-16 0.20, Saúde 0.0 (alvo 0.8 —
  famílias fracas nominadas no JSON dizem qual detector construir; o conserto
  da Súmula 362 no G4 já subiu S6 de CASO-19 de 0/2 para 2/2).
  Regressão: `test_forja_mutation_semantic.py` (10).
- **M3.2 Ledger material** — `python forja_ledger_material.py <caso>` →
  `F5_LEDGER_MATERIAL.json` (citações extraídas × cache oficial/fonte local/
  sourceLedger + tabela `producao/PROPOSICOES_DECISIVAS.md`, template gerado
  quando ausente). Sem fonte primária = P1 nominado, nunca silencioso.
  Regressão: `test_forja_ledger_material.py` (7).
- **M4.1** — `test_forja_run.py` (9): executor N3 coberto (fluxo feliz F0 com
  promoção real, autorrevisão, gates, excesso de tentativas, replay idempotente,
  bloqueio formal).
- **M4.3** — `forja_f2_check.py`: coerência tribunal×CNJ (J4→TRF, 8.27→TJTO,
  AREsp→STJ...), perfil PSO-Pet e complexidade em enum; achado = P1 nominado.
  Regressão: `test_forja_f2_check.py` (11).
- **G4 ampliado**: pares súmula×tribunal acrescidos (STJ: 43, 54, 227, 297,
  326, 362, 385; STF: 282, 356) — motivado pela sobrevivência do S6.

- **M4.2 QA de páginas** — `python forja_qa_paginas.py <pasta-de-pngs>`:
  densidade anômala por página (MAD, não desvio-padrão — o outlier infla o σ e
  se esconde), página em branco no meio do documento e conteúdo colado na borda
  inferior (1ª página isenta: o rodapé institucional do template encosta na
  borda POR PROJETO, densidade ~0.93 nos renders reais). Achado = P1 nominado;
  regenerar é decisão do agente. Validado em 37 páginas reais sem falso
  positivo. Regressão: `test_forja_qa_paginas.py` (8, com PNGs sintéticos).


Pendência restante do plano 19: `resolvedAt` nos bloqueadores (writer-side).
O hook LocalContext (M1.2) lê state/ diretamente e não depende de nenhum módulo externo.

## 16. Gate de escrita humana (15/07/2026)

Contrato editorial: `PROTOCOLO_ESCRITA_HUMANA_FORJA.md`. Implementação:
`forja_estilo_humano.py`; regressão: `test_forja_estilo_humano.py`.

O gate não atribui probabilidade de autoria por IA. Ele devolve sinais verificáveis com trecho,
contagem e ação corretiva: contraste formular, metadiscurso vazio, clichê, conectores em série,
travessões repetidos, absolutismo sem lastro, redundância consecutiva, ritmo robótico, simetria
estrutural e conclusão tautológica. Em e-mails, também bloqueia aberturas traduzidas, fórmulas
burocráticas, autonarração do esforço, fechos inflados e corpo com formato de relatório. `P0` é
recomputado sobre o texto real nas seguintes barreiras:

1. prompt obrigatório de F6/F7 para a peça e de F9 para o e-mail (`forja_headless.py`);
2. promoção de artefatos F6/F7 (`forja_run.py`);
3. render simples e composição visual (`forja_render_docx.py` e `forja_visual.py`);
4. validação hash-bound da peça e do corpo do e-mail no pacote (`forja_package.py`);
5. registro do rascunho somente com `bodySha256` idêntico ao e-mail aprovado (`forja_close_cycle.py`);
6. F10, pelo `F7_VERIFICADOR_FORJA.json` e pelo pacote canônico já existentes.

Assim, `p0=0`, `anti_ai_style_passed=pass` ou `email_human_style_passed=pass` declarados manualmente
não aprovam texto viciado, e uma edição no corpo depois do pacote invalida o registro do rascunho.

## 17. F7-B — revisão e escrita final pelo modelo editorial (15/07/2026)

> **Atualização de 25 e 26/07/2026.** O modelo editorial padrão passou a ser `claude-opus-5` por determinação do titular; o Fable 5 continua autorizado como legado, e a allowlist vive em `forja_editorial_model.py` — modelo fora dela não executa. O executor foi renomeado de `forja_fable5.py` para **`forja_editorial.py`** (o nome antigo permanece como shim com `DeprecationWarning`), e o protocolo, de `PROTOCOLO_FABLE5_ESCRITA_FINAL.md` para **`PROTOCOLO_EDITORIAL_ESCRITA_FINAL.md`**. Os leitores ainda aceitam os nomes antigos de artefato (`FABLE5_RESULT.json`, `fable5_usage`). A revisão cruzada entre famílias de modelo virou gate de produção: `familyAssurance` assume `cross_family`, `cross_session_same_family` ou `unverified`, é recomposto pelo orquestrador e nunca aceito por declaração. O texto abaixo descreve a mecânica, que não mudou.


F7-B é uma subfase bloqueante dentro de `F7_AUDITORIA_JURIDICA_FACTUAL`; ela não renumera F8–F10. O operador ou workflow a aciona depois de `f7_gate_result.json` comprovar zero P0:

```powershell
python forja_fable5.py <caso> <attempt-dir> --source audited_markdown.md --f7-gate f7_gate_result.json
```

`forja_run.py` não chama o Fable automaticamente. O executor envia o texto auditado integral por `stdin` ao Claude Code, com ferramentas desabilitadas, exige autenticação `claude.ai`/assinatura `max` e comprova no envelope o modelo `claude-fable-5`. Isso implica processamento remoto pela conta do Igor, embora não use API key nem cobrança de API.

O bundle produzido contém `final_markdown*.md`, `editorial_report*.json`, `editorial_diff*.patch`, `fable5_usage*.json`, `editorial_fidelity*.json` e o fragmento `FABLE5_RESULT*.json`. O fragmento não é um `PHASE_RESULT.json` completo: seus artefatos e quatro gates devem ser incorporados ao resultado F7, mantendo produtor `forja-auditor-juridico`, revisor `forja-gate-controller` e todos os demais requisitos da fase.

O executor isolado só comprova imediatamente a ausência de `p0 > 0` no arquivo de gate. A regra do workflow é mais forte: todos os gates F7 devem estar satisfeitos antes da integração e a promoção final volta a validá-los. Não tratar a ausência de P0, sozinha, como aprovação jurídica completa.

| Gate agregado | O que o runner recompõe |
|---|---|
| `fable5_oauth_confirmed` | conta Claude Max, sessão e modelo canônico |
| `editorial_source_hash_match` | SHA-256 real do `audited_markdown` |
| `editorial_fidelity_pass` | protocolo, hashes e sinais estruturais/lexicais preservados |
| `human_style_final_pass` | ausência de P0 do gate de escrita humana no texto final |

Os sinais determinísticos incluem multiconjuntos de números, datas/valores, marcadores processuais, autoridades, aspas duplas e marcadores de auditoria; títulos; retenção mínima de 90%; pedidos/fecho quando reconhecidos; e ausência de origem operacional. Eles não provam equivalência semântica universal nem cobrem toda mudança factual sem números, adição semanticamente nova, aspas simples ou pedido sem heading reconhecido. Por isso o diff e a revisão humana permanecem obrigatórios.

Uma chamada pode durar até 1.800 segundos. Há no máximo três candidatas editoriais internas no total — a inicial e até dois retries —, sempre a partir do `audited_markdown` original; isso não se confunde com as quatro tentativas de fase admitidas pelo contrato F7. Depois de três reprovações, a tentativa fica bloqueada. O suporte a documentos adicionais usa sufixo comum no bundle, mas o bundle-base permanece obrigatório e ainda falta regressão específica para multi-documento.

O campo `duvidas` do `editorial_report` não possui gate automático. Ele deve ser triado antes de F8: dúvida material sobre fato, estrutura, tese, pedido ou sentido volta à auditoria e bloqueia a composição; dúvida puramente editorial pode ser mantida com decisão humana registrada. O CLI direto `forja_editorial_fidelity.py <audited> <final> <report>` também não recebe `fable5_usage`; a recomposição completa da prova OAuth ocorre no executor, na promoção e no pacote.

Na promoção, `forja_run.py` recompõe os gates. F8 recebe `final_markdown` como cânone, e `forja_package.py` revalida o bundle do entregável selecionado. Pacotes históricos permanecem legíveis conforme o contrato de sua época; novas tentativas F7 não podem usar essa compatibilidade como atalho.

Evidências de 15/07/2026: regressão integrada com 42/42 testes e execução standalone real sobre aproximadamente 36 KB, aprovada na primeira tentativa. Essa execução comprova o passe editorial e seus gates; não comprova promoção, render e pacote E2E. Protocolo completo: `PROTOCOLO_EDITORIAL_ESCRITA_FINAL.md`; decisão: `planejamento/21_F7B_FABLE5_REVISAO_ESCRITA_FINAL.md`; artefatos sanitizados: `reports/fable5_live_validation_20260715/`.

## 18. Gate visual e jurisprudencial anti-trapaça (21/07/2026)

O incidente CASO-17 demonstrou que lint automático e `approved=true` não provam diagramação. O arquivo enviado tinha somente 20 de 245 parágrafos de corpo justificados. A correção passou a usar quatro provas independentes e reproduzíveis:

1. `forja_docx_layout.py`: inspeção OOXML do corpo (Times New Roman 12, justificado), consistência de tabelas, fólio lateral e assinatura de fidelidade textual antes/depois;
2. `forja_visual_review.py`: formulário inicialmente pendente, hashes exatos e oito checks obrigatórios em todas as páginas, sem preenchimento automático; em liberação estrita, `forja_human_review.py` exige recibo humano Ed25519 da inspeção visual integral;
3. `forja_visual_qa.py`: separação explícita entre lint automático e revisão visual independente;
4. `forja_package.py`/`forja_n4_validate.py`: recomputação do DOCX, rerender do PDF e replay do atestado, sem confiar no ledger produzido pela etapa.

Na F7, `forja_official_sources.py` faz replay HTTPS da página oficial e exige que identidade e trecho material existam tanto na captura arquivada quanto na resposta viva. `forja_package.py` exige cobertura de todas as citações extraídas e hash do trecho. `forja_human_review.py` rejeita o rótulo declaratório `type=human`: a aderência entre proposição e fonte só passa com recibo Ed25519 assinado por chave presente em `~/.hermes/trust/FORJA_HUMAN_REVIEW_TRUST.json`. O caminho não é substituível por variável do processo e o SHA-256 do trust store precisa coincidir com `FORJA_HUMAN_REVIEW_TRUST_PIN.json`, arquivo protegido pela régua. A FORJA não cria nem guarda a chave privada. HTTP 403, WAF, timeout, fonte sem verbatim, assinatura ausente, ambiguidade ou falta de revisor bloqueiam. O extrator também distingue processos CNJ estaduais: uma ADI `...8.26...` é TJSP e não pode ser promovida a ADI do STF.

A barreira é deliberadamente fail-closed. Ela prepara material íntegro para revisão humana; não pretende transformar validação técnica em aprovação jurídica. Regressão: `test_forja_anti_cheat.py`, além das suítes visual e de pacote. Registro do incidente: `INCIDENTE_NATURA_QA_VISUAL_2026-07-21.md`.

## 19. AUTO-RESEARCH — ciclo AR de auto-melhoria anti-trapaça (23/07/2026)

Subsistema que institucionaliza o loop de auto-melhoria da fábrica: mede a qualidade das
entregas com indicadores ancorados nas falhas reais mineradas, testa variantes de artefatos
da esteira contra material real e só permite promoção que sobreviva a canários adversariais,
holdout com orçamento e cadeia de aprovação em três estados. Normativa: `planejamento/22_PRD_AUTORESEARCH_FORJA.md`
e `planejamento/23_TDD_AUTORESEARCH_FORJA.md` (v1.1 — a v1.0 foi REPROVADA em review
adversarial do Codex GPT-5.5 com 13 P1; todas as recomendações foram incorporadas e a
triagem está no §14 do PRD).

Arquitetura em seis módulos determinísticos (LLM nunca é chamado pelo Python; passos de
modelo são explícitos, no padrão F7-B):

1. `forja_ar_corpus.py` — inventário do corpus real de `state/` com split train/holdout/sealed
   por HMAC de LINHAGEM (grupo do mesmo litígio nunca se separa), estratificado por
   produto×tribunal. O sealed não é listado no workspace: vive em
   `%USERPROFILE%\.forja_ar_secrets\sealed_registry.json` com orçamento VITALÍCIO de consultas.
2. `forja_ar_indicadores.py` — painel I1–I10 reutilizando os sensores vivos
   (`forja_verificador`, `forja_metricas_f7`, `forja_estilo_humano`, `forja_human_review`).
   Cobertura e correção separadas contra ledgers congelados pré-geração (anti-otimização
   por exclusão de conteúdo); sensor ausente vira `null` motivado, nunca zero; em comparação
   vigente×variante a máscara é pareada e novo `null` BLOQUEIA (nunca renormaliza).
3. `forja_ar_canarios.py` — canários de FALHA ÚNICA por mutação sobre peça-base real:
   o sensor-alvo deve matar a mutação, os demais não podem mudar (atribuição limpa) e o
   controle benigno deve sobreviver. Camada pública em `autoresearch/canarios/` + camada
   secreta rotativa fora do workspace.
4. `forja_ar_runpair.py` — execução pareada vigente×variante (mesmo input congelado,
   manifests de execução com modelo/parâmetros/hashes); paridade violada não chega ao juiz.
5. `forja_ar_blind.py` — julgamento cego pairwise com swap obrigatório (A/B e B/A),
   mapping HMAC fora do workspace, consolidação por `artifactSha256` (mesma POSIÇÃO
   vencendo nas duas ordens = viés posicional → par anulado), mínimo de 2 famílias de
   juiz e proibição de a família geradora julgar a própria variante.
6. `forja_ar_ciclo.py` — orquestrador com log encadeado por hash e gate de promoção em
   três estados: `technical_candidate_passed` → `independent_review_passed` (família
   distinta) → `human_promotion_approved` (recibo Ed25519 da trilha `forja_human_review`).
   Sem sealed elegível, o teto é `estudo_descritivo` e nenhuma variante é promovida.

Regressão: `test_forja_autoresearch.py` (23 testes, 12 sabotagens nominais: split-shopping,
mapping vazado, injeção contra o juiz, supressão de ledger, inflação de páginas, remoção de
citações, stuffing, edição de manifest pós-resultado, replay do sealed, linhagem separada,
pesos hardcoded, controle benigno morto). A suíte integra a Régua e os 13 arquivos AR são
protegidos por hash no `REGUA_MANIFEST.json`.

Calibração real (ciclo AR-0, 23/07/2026): painel sobre 22 peças reais (5 do corpus + 17 do
experimento `.autoresearch/fabrica-peticoes-v1`); σ 0.29–0.47 nos determinísticos; flags de
origem operacional auditados manualmente (7/7 verdadeiros positivos — caminho local vazado
em peças históricas); canários 7/7 com atribuição limpa. Relatório:
`autoresearch/ciclos/ciclo-0/AR_CICLO_0_RELATORIO.md`. Segredos (chave HMAC, sealed,
canários secretos) em `%USERPROFILE%\.forja_ar_secrets\` — nunca no repositório; testes
redirecionam via `FORJA_AR_SECRETS_DIR`.

### 19.1 Camada evolutiva Karpathy e primeiro ciclo real (23/07/2026, noite)

`forja_ar_evolucao.py` implementa o modelo AutoResearch/Karpathy da skill `autoresearch` sobre os
trilhos anti-trapaça do ciclo AR: experimentos com baseline congelado, gerações de variantes com
estratégia de mutação declarada (rephrase/expand/compress/pivot/hybrid) e eixo conceitual do diff,
seleção de vencedor SÓ com evidência de ciclo (julgamento cego válido + não-inferioridade),
snapshot em `autoresearch/evolucao/<exp>/winners/gen-N.md` e convergência por K gerações sem ganho.

Primeiro ciclo real (AR-1, geração 0 de `prompt-mestre-v2`): alvo = prompt-mestre da fábrica;
mutações autoradas pelo Codex; tarefa real do split train executada em paridade 3× (766k tokens);
2 rounds de julgamento INVALIDADOS pelo harness (âncoras + troca de rótulos) antes de um round
válido com kappa 1.0; vencedora varB (compress); revisão independente APTA COM RESSALVAS;
`independent_review_passed` alcançado; SEM propagação (gate humano Ed25519 pendente). Relatório:
`autoresearch/ciclos/ciclo-1/AR_CICLO_1_RELATORIO.md`. Protocolo de juiz corrigido: um par por
sessão; âncora literal exclusiva do vencedor, verificada antes da devolutiva.

## 20. Blindagem contra lastro aparente (26/07/2026)

Módulo `forja_lastro.py` (`FORJA-LASTRO-v1`). Protocolo completo em `PROTOCOLO_LASTRO_DOCUMENTAL.md`; incidente que o originou em `INCIDENTE_VALE_TRADING_LASTRO_APARENTE_2026-07-26.md`; catálogo em § U12 de `planejamento/06_GATES_QUALIDADE_FORJA.md`.

**O problema.** No caso CASO-23, três camadas de revisão — red team interno de 12 perguntas, gate F7 e dois revisores externos de famílias distintas — devolveram zero P0 sobre uma minuta que continha quatro P0. Todas examinaram o TEXTO. Os erros estavam na FONTE, e a fonte não fora aberta. O `fact_ledger` marcava F012 como `confirmed_document` com apoio em `E252-ANEXO-AI-p20-31`: a página existia, o documento existia, e o documento dizia o contrário.

**O eixo.** Citar o localizador não é ter lido o localizador. A única prova barata de leitura é a transcrição verbatim — um modelo obrigado a colar o trecho tem de abrir a fonte; um modelo que só precisa citar a página pode inventá-la com aparência perfeita.

**Os oito gates**, cada um com uma falha real desta execução como âncora (não há gate especulativo no módulo):

| Gate | Sev | Âncora |
|---|---|---|
| L1-lastro | P0 | status documental sem transcrição verbatim |
| L1-lastro-pendente | P1 | mesma falta, porém **declarada** (`groundingPending`) |
| L2-transcricao | P0 | transcrição que não existe na fonte apontada |
| L3-superlativo | P0/P1 | "confirmada em todas as instâncias" sobre REsp **não conhecido** |
| L4-denominador | P1 | "93% dessa distância" — denominador trocado no meio da frase |
| L5-identidade | P0 | "mesmas partes e a mesma liquidação" — eram liquidações distintas |
| L6-norma-por-ano | P0 | "normas de 2002, 2016 e 2018" — a de 2018 não existia |
| L7-criterio-vigente | P0 | base de cálculo recomendada contra critério já fixado nos autos |
| L8-objecao | P0 | objeção externa acatada sem reabrir a fonte, contra minuta correta |

**Acoplamento** (importável não é acoplado — a regressão verifica os quatro pontos): `fact_grounding_verbatim` nos `requiredGates` do `phase_contracts/F7.json`; elo bloqueante **9-B** no `forja_delivery.py` via `fatos_sem_lastro()`; gates lexicais na bateria do `forja_verificador.py`; e `test_forja_lastro.py` (37 casos) no `SUITES_SCRIPT` do baseline.

> ⚠ **Correção de 03/08/2026 — verificar a ligação não é verificar o cálculo.** Medido por busca de chamadores: `validar_lastro_fatos` (L1/L2), `exigir_criterio_vigente` (L7) e `validar_decisoes_revisao` (L8) **não têm chamador fora do teste**. Da produção sobrevivem `analisar_texto` (L3–L6, pelo verificador) e `fatos_sem_lastro` (elo 9-B). O ponto 1 é **declarativo**: `forja_run._validate_result` confere `requiredGates` lendo o campo `gates` do `PHASE_RESULT.json`, escrito pelo próprio agente da fase — de modo que `fact_grounding_verbatim` está no contrato e ninguém o calcula. **Acrescentar gate a contrato que ninguém computa aumenta a autoatestação.** Ligar isso é o passo 1 do plano 41. Lição 100.

**Duas regras de calibração que valem para todo gate futuro.** Pendência declarada é P1, não P0 — punir honestidade com a pena da invenção ensina o sistema a esconder lacuna. E negação nunca trava: o L5 chegou a bloquear "não se trata da mesma liquidação", que é a correção desejada; hoje há detector de negação por janela curta e as duas frases corrigidas reais estão fixadas como não-travas.

**Limite.** São escudos lexicais e estruturais: obrigam a colar o trecho e conferem que ele está no arquivo apontado; **não** julgam se o trecho sustenta a proposição. Isso continua sendo auditoria F7 e leitura humana.

## 21. Auditoria de atualidade dos regimentos (26/07/2026 — E11)

Módulo `forja_regimentos.py` (`FORJA-REGIMENTOS-v1`). Runbook operacional em `RUNBOOK_AUDITORIA_REGIMENTOS.md`.

Converte em checagem recorrente a exigência do protocolo da fábrica de que a peça reflita o regimento vigente **na data do protocolo**. Varre `REGIMENTO_INTERNO_*.md` na fábrica inteira e reporta, por arquivo: versão consolidada, data de verificação, URL oficial e presença da seção "Emendas posteriores". Exit 1 com qualquer bloqueio.

Códigos: `sem_versao` (P0), `sem_data_verificacao` (P0), `verificacao_vencida` (P1, padrão 30 dias), `sem_fonte` (P1), `sem_secao_emendas` (P1). Regra conservadora: na dúvida reporta desconhecido, nunca aprovado — ausência de data não é data recente; e verificação vencida é ressalva, porque o arquivo não está errado, está por conferir.

**O parser é a parte delicada e errou três vezes antes de acertar**: regex guloso truncando data em célula de tabela; frontmatter YAML ignorado; e leitura da primeira data da linha em vez da data depois do rótulo (a linha do TJRJ tem duas datas e devolvia 2024 para arquivo conferido em 2026). Dos 8 bloqueios da primeira execução, **7 eram defeito do auditor**. Por isso `test_forja_regimentos.py` fixa quatro cabeçalhos reais do acervo como não-travas.

Estado em 26/07/2026: **16 arquivos, 16 em ordem, 0 bloqueio, 0 ressalva**. Achado a carregar: **o TJSP tem os AR 594 e 595/2026 posteriores à compilação arquivada de 30/04/2026** — ressalva registrada dentro do arquivo. Dois arquivos do TRF4 parados no AR 35 receberam aviso expresso de desatualização, sem reescrita do corpo.

## 22. Estado consolidado em 26/07/2026

| Frente | Estado |
|---|---|
| Baseline (`forja_baseline.py`) | **41/41 suítes verdes** · 463 testes pytest (+44 subtests) · 7 regressões em script |
| Régua (`forja_regua.py`) | **APROVADA**, rebaselinada com motivo enumerado |
| Regimentos | 16/16 em ordem |
| Modelo editorial F7-B | `claude-opus-5` padrão; allowlist em `forja_editorial_model.py` |
| Revisão cruzada | `familyAssurance` é gate; `unverified` bloqueia em qualquer modo |
| Fontes oficiais | nove artigos do RISTJ arquivados verbatim, o que destravou a bateria REAL |

Duas manutenções silenciosas que explicam sintomas anteriores: um `.git/index.lock` obsoleto de três dias travava todo o git e fazia o sync diário parar em 22/07; e a bateria REAL vinha reprovando desde E9/E10 porque peças de produção citavam o RISTJ sem verbatim arquivado — resolvido pelo arquivamento das fontes, não por afrouxamento do gate.

Caso CASO-23: permanece `internal_working`, bloqueado em F7 pelos dois gates humanos (`human_claim_review_signed_receipt` e `external_human_trust_store_verified`), que nenhum modelo pode satisfazer. As diligências externas pendentes estão declaradas no incidente e nos artefatos do caso, nunca descartadas em silêncio.

## 23. Esteira visual reconstruída (30/07 a 03/08/2026)

**Ordem de origem (Igor, 30/07):** nenhuma peça sai da FORJA sem elementos visuais completos. Sem atalho, sem waiver, sem exceção para produto interno.

**Causa medida da regressão:** a edição visual não degradou, **parou em 10/07/2026**. O `compor()` funcionava, mas exigia um mapa escrito à mão por caso — cinco mapas manuais na semana em que o kit era novidade, nenhum depois. Cobertura em 03/08 nas 22 entregas recentes: 9%. A lição é de arquitetura, não de disciplina: **recurso que depende de esforço manual por caso não sobrevive ao volume.**

### 23.1 Entrada única de produção

`forja_visual_build.py` é a **única** rota de produção visual. Fluxo: gates F7 (fail-closed) → brief `F7_5_BRIEF_VISUAL.json` → mapa automático (`forja_visual_mapa_gen.py`) → figuras (`forja_visual_figuras.py` + geradores em `_FERRAMENTAS\medina_svg_kit.py`) → `forja_visual.compor()` → `montar_visual.py` (EMF/Word COM/PDF/QA) → gate F8-S. **7 a 15 segundos por peça, fidelidade textual 100%.**

**Decisão registrada, não reabrir sem fato novo:** NÃO integrar `compor()` dentro de `forja_render_docx.render()`. Constrói a peça duas vezes, uma pobre e uma rica, e deixa dois DOCX parecidos na mesma pasta — modo de falha do caso CASO-19 (Lição 48). O render simples é prévia; a produção passa pela entrada única.

### 23.2 Nunca inferir conteúdo semântico de figura

Foi tentado e reprovado: a cronologia inferida da prosa misturou data de documento com prazo interno e leu fragmento de CNJ como data; a cadeia de tese colocou a **tese da parte adversária** como elo do raciocínio da cliente. Cada frase era verbatim e o conjunto mentia. **Figura fabricada é pior que figura ausente, porque parece prova.** Daí o brief F7.5 declarado pelo autor da peça (`templates\F7_5_BRIEF_VISUAL.md`, 1 a 2 minutos); sem ele saem apenas as figuras estruturalmente seguras.

### 23.3 Os dois gates, e o que cada um vê

| Gate | Módulo | O que verifica | Estado |
|---|---|---|---|
| **F8-S** — assinatura visual | `forja_assinatura_visual.py` | **PRESENÇA** de elementos no DOCX final: timbre, síntese de abertura em tabela, figuras vetoriais e destaques por faixa de extensão, negrito entre 2% e 20% do corpo, paleta. Taxonomia VIS-02/03/04/05/06/11 | **observação** — grava `F8S_ASSINATURA_VISUAL.json`, não bloqueia |
| **SVGC** — desenho do SVG | `_FERRAMENTAS\medina_svg_colisao.py` | **CORRETUDE do desenho**: SVGC-01 texto ocluído por forma opaca posterior, SVGC-02 texto sobre texto, SVGC-04 cor inválida; avisos SVGC-03 (traço cruzando texto) e SVGC-05 (contraste < 2,0:1) | **bloqueante**, dentro de `svg_para_emf` |

O F8-S nasceu porque **gate que só procura defeito nunca detecta pobreza**: o `forja_visual_qa` procura markdown vazado, marcador literal e clipping — uma peça de texto corrido, sem um único destaque, passa limpa nele. O SVGC nasceu porque o F8-S conta presença e não vê um diagrama internamente quebrado (Lições 96 e 98).

Regressão: `test_forja_assinatura_visual.py` (mutação + teste-âncora) e `test_medina_svg_colisao.py` (10 casos, com o diagrama defeituoso real como fixture e a correção como contraprova).

### 23.4 Regras de calibração que custaram caro

1. **Nunca detectar identidade visual por valor de cor.** A arte do timbre usa `3a5c61`/`d9936a`, um dígito fora dos tokens `395C60`/`D9926A`; a prova correta é estrutural — desenho vetorial no cabeçalho. Um gate calibrado por cor quebraria no primeiro retoque da marca (Lição 94).
2. **Contraste em 2,0:1, não nos 3,0:1 da WCAG.** O rótulo terracota sobre painel terra da casa dá 2,3:1 e está aprovado desde 09/07; calibrar na norma reprovaria a paleta do escritório.
3. **Manter o teste-âncora contra a peça aprovada.** Gate que reprova o padrão aprovado pelo dono está errado, não a peça. Foi ele que pegou a regressão do item 1.
4. **Defeito só é defeito contra o padrão aprovado.** Os retângulos cinza da capa e o vazio inferior são identidade, não erro.
5. **Calibrar contra o acervo antes de bloquear.** O SVGC foi medido nos 228 SVGs existentes: 5 reprovações, **todas confirmadas por render como defeito real**, zero falso positivo sobrevivente. Os dois falsos positivos corrigidos no caminho: `!important` dentro de `style=` lido como parte da cor, e `<tspan>` sem `x` próprio tratado como começando no `x` do pai.
6. **Nenhuma rota é universal até que se prove.** `medina_svg_kit.salvar()` parecia cobrir tudo e não cobre o SVG desenhado à mão — por isso o gate mora em `svg_para_emf`. O mesmo erro reapareceu no plano 41 com `PecaVisual.salvar()`, que não cobre `forja_render_docx` (python-docx direto). Lição 101.

### 23.5 Comitê não substitui revisão de código

O conselho de quatro personas leu o dossiê do construtor e recomendou arquitetura já rejeitada, citando função inexistente. A circularidade de autovalidação — quem constrói escreve o gate, mede com ele e se aprova — só foi quebrada pela revisão cruzada com a outra família de modelo, lendo o XML. Achado material: a contagem de caixas casava qualquer célula sem borda superior, contando 521 fantasmas no CASO-07 e **mascarando ausência total de destaque** (Lição 93).

### 23.6 Calibração de material econômico

`forja_calibra_monetario.py` mede a incidência da detecção de conteúdo econômico sobre o acervo, para os gates L9–L13 planejados (plano 41). Existe porque a primeira medição foi feita por script não persistido e os números iriam ao cliente como evidência — **número em relatório de evidência sem meio de reexecução é atestação sem lastro**. Comando: `python forja_calibra_monetario.py --saida CALIBRACAO_MONETARIA.json`. Resultado de 03/08: a regra ampla tocaria 39,3% dos documentos contra 13,9% da estreita, e 29,7% das ocorrências com separador de milhar são citação normativa lida como dinheiro (Lição 102).

## 24. Vigias e o fio de e-mail como superfície de trabalho (06/08/2026)

### 24.1 O problema que os três vigias resolvem

Até 06/08/2026 a esteira só enxergava trabalho que alguém tivesse **pedido**. Dois
episódios no mesmo dia mostraram o custo disso.

O primeiro: uma varredura feita para outro fim revelou, por acaso, que dois
agravos do escritório estavam pautados para julgamento em duas semanas, com o
prazo de sustentação oral correndo. As intimações haviam sido divulgadas três
semanas antes. Achado que depende de acaso não se repete.

O segundo: a varredura de fim de trabalho deu tudo verde — baseline, fronteira,
painel de demandas, nenhuma flag — enquanto sete fios de e-mail do escritório
esperavam resposta, o mais antigo havia duas semanas, um deles com uma promessa
escrita minha e outro com uma **diretriz permanente** do escritório que não
constava de documento nenhum da fábrica. Nenhum gate viu, porque a demanda que
originou cada retorno já constava cumprida: a peça tinha sido entregue. O retorno
**sobre** a entrega abre trabalho novo que o painel registra como o mesmo item
fechado.

### 24.2 Arquitetura comum aos três

| camada | decisão | por quê |
|---|---|---|
| alvo | vive no acervo (`monitor_djen_vigiados`, `fios_remetentes_casa`), lido por `forja_acervo.valor()` | número de processo, nome de parte e endereço de escritório são dado de cliente; o motor é público e a fronteira reprova |
| ausência de acervo | sai com código `2` e diz que rodou sem alvo | vigia mudo é indistinguível de vigia sem trabalho |
| resposta inesperada da API | `RuntimeError`, não lista vazia | "não consegui ler" nunca pode virar "não há nada" |
| aviso | arquivo na raiz do harness, não linha em log | log que ninguém abre não avisa ninguém |
| ação | nenhuma — não peticiona, não envia, não decide | avisar continua sendo decisão de quem lê |

### 24.3 Fontes públicas que a esteira passou a usar

Duas rotas foram medidas em 05–06/08/2026 e dissolveram dependências que eu já
havia declarado ao cliente como sendo de terceiro:

- **Cadastro nacional de processos (DataJud/CNJ)** — `POST` em
  `api-publica.datajud.cnj.jus.br/api_publica_<alias>/_search` com o número de 20
  dígitos sem pontuação. **Não** indexa nome de parte, mas devolve classe,
  assunto, órgão julgador atual, grau e a lista completa de movimentos com data.
  Serve para confirmar órgão julgador e relatoria sem depender de informação de
  terceiro — o que torna operacionais os níveis 2, 5 e 8 da ordem de pesquisa
  jurisprudencial da casa.
- **Diário nacional (DJEN/Comunica)** —
  `comunicaapi.pje.jus.br/api/v1/comunicacao`. **Indexa nome de parte com polo** e
  devolve o **teor** integral de cada comunicação. O host `comunica.pje.jus.br`
  devolve HTML e não serve. Foi o teor, e não o cadastro, que respondeu perguntas
  de valor que eu havia dado como dependentes de acesso aos autos.

Lição derivada, registrada como 232: **campo ausente não é dado ausente** — o
dado pode estar no texto que o campo não indexa.

### 24.4 A armadilha do invólucro

As tarefas agendadas invocam `powershell.exe`, o Windows PowerShell 5.1, que lê
`.ps1` sem BOM como ANSI: todo acento vira erro de parse e o script morre antes
da primeira linha útil. Os três wrappers estavam assim, e o vigia do STF vinha
"rodando" desde a instalação sem nunca ter executado uma linha. Os testes não
apanham porque exercitam o módulo Python, que está correto — o defeito mora no
invólucro. E o canário não apanhou porque rodou no PowerShell 7 da sessão.

Duas regras ficaram: wrapper com acento nasce com **BOM UTF-8**; e canário de
tarefa agendada se executa com o comando literal de
`(Get-ScheduledTask <nome>).Actions[0]`. Detalhe da armadilha secundária: ao
simular novidade, remova só o item mais recente do retrato — zerar a lista vira
*primeira leitura* e o vigia calado está certo.


## 25. Aprendizado do retorno humano — da correção à mudança no sistema (06/08/2026)

O loop pós-protocolo existia e funcionava: capturava a peça que o titular
protocolou, comparava com a nossa e classificava cada mudança por camada, causa
e impacto. O que não existia era o que vem depois — e o que vinha antes.

### 25.1 O executor que faltava

Seis casos reais já haviam produzido **1.096 candidatos a lição**. Destes,
**1.095 parados e um promovido**. A causa não era desleixo: promover um
candidato exigia criar à mão uma fixture e um teste, mais um SHA-256 copiado a
dedo. Todos os 1.096 traziam um campo `destination` preenchido, e nenhuma linha
de código o consumia — o destino foi projetado, o executor nunca foi escrito.

`forja_aprendizado.py` fecha isso com quatro verbos e um princípio: **promover o
padrão, não a ocorrência**. `padroes` agrega por `camada:causa` e ordena por
recorrência entre **casos distintos** — um processo longo produz centenas de
mudanças sozinho e dominaria qualquer ranking por volume. `adotar` registra a
decisão humana guardando a evidência do momento. `aplicar` escreve a regra no
destino (item no contrato da fase, instrução no template, lição no protocolo),
de forma idempotente por bloco marcado. `conferir` verifica que ela continua lá
— é a diferença entre registrar uma lição e aplicá-la.

Um teste só, parametrizado pelo registro, confere cada regra contra o seu
destino: adotar a próxima não custa uma linha de código. Era esse custo marginal
que matava o desenho anterior.

O **gate 5-B do F10** verifica o inverso do reflexo natural: não exige que o caso
corrente já tenha aprendido — o retorno humano chega depois do protocolo, e isso
travaria toda entrega. Verifica que nenhuma regra adotada antes tenha saído do
seu destino.

### 25.2 O gate que faltava antes: isto é revisão da nossa peça?

Com o ciclo pronto, a leitura apontava `reasoning:reasoning` com 279 correções
materiais em 5 casos — o maior padrão, e o candidato natural a virar regra. Ao
abrir os textos, os pares comparados **não eram o mesmo trecho**.

O comparador alinhava tokens de dois documentos quaisquer. Sem origem comum, ele
casa parágrafos sem relação entre si e classifica cada par com confiança 0,98.
Medido:

| retorno | texto em comum com a nossa base | blocos preservados |
|---|---|---|
| três deles | 0,7% · 3,1% · 13,4% | 0 · 0 · 1 |
| dois deles | 49,9% · 66,8% | 35 · 19 |

Os três primeiros eram documento distinto, não revisão. Sozinhos produziram 496
das mudanças e 228 das materiais — mais que o dobro do que veio dos dois
retornos legítimos. **Agregado por classe, esse ruído tem a forma exata de um
padrão do escritório.**

`_e_revisao` mede a proporção de texto em comum (`sharedTokenRatio`, novo no
resumo da comparação) e barra abaixo de 0,30 com `PP-NOT-A-REVISION`, nos dois
caminhos que produzem comparação. O gate nasceu exigindo também um mínimo de
blocos preservados e a suíte reprovou nove testes na hora: **a contagem cresce
com o tamanho do documento e reprova peça curta por ser curta**. Ficou só a
proporção, que é adimensional.

`forja_aprendizado.py` refaz a pergunta na leitura, porque os candidatos de 2026
nasceram antes do gate, e devolve os descartes com o motivo — filtro silencioso
foi como o ruído passou por padrão na primeira vez.

`amostra <classe>` abre o par real de textos a partir do cofre local e mostra na
tela sem gravar nada. Sem ele foi possível olhar 279 correções materiais e não
ter como perceber o problema, porque o texto nunca aparecia. **Contar não é
ler.** Sanitização por hash protege o texto e, sem uma janela deliberada para
lê-lo na triagem, também cega quem decide.

`revalidar` compara a evidência registrada na adoção com a de hoje. Aplicado, ele
acusou a primeira regra da casa: adotada com "3 casos, 12 correções materiais",
lastro real de 1 e 1 depois do gate. A regra continuava sensata; a evidência,
não. Não apaga nem reescreve — devolve a divergência para decisão humana.

### 25.3 A cegueira ao e-mail, e a conta de 45 contra 5

A varredura do Gmail pedia `has:attachment` e descartava em silêncio toda
mensagem sem peça anexada. Uma correção escrita em prosa — *"tire aquele
argumento"*, *"o prazo é outro"*, *"não use esse precedente"* — nunca chegava a
ser lida. Havia até um esquema pronto para isso, `feedbackAssimilation`, com
validador, contrato e seis tipos de retorno: **validador escrito, produtor
nenhum, zero artefatos no disco**.

Tirar o filtro sozinho não resolveu: sem ele a consulta traz a caixa inteira e a
cota se esgota antes de chegar ao escritório — 60 de 60 mensagens vieram de
remetente não autorizado. `consulta_padrao` deriva a consulta da própria lista
de remetentes autorizados, que é a mesma que autoriza a ingestão. A rodada
seguinte trouxe **45 correções do escritório vinculadas a caso conhecido, contra
as 5 que a esteira via por anexo**: o loop enxergava cerca de um décimo do
retorno do titular.

Cada uma fica ancorada no caso em `F10_RETORNO_SEM_ANEXO.json`, idempotente por
mensagem; a de demanda reconhecida sem caso FORJA aberto vai para lista própria,
declarada como tal (10 com caso, 35 sem). Guarda-se localizador, assunto e data,
**nunca o corpo** — o conteúdo vive no e-mail e quem tria abre a mensagem. Não
há classificação automática de prosa: heurística sobre texto livre inventaria
padrão, que é o erro que o gate de comparabilidade acabou de fechar.

### 25.4 Regras aprendidas em vigor

Duas, em `learning_registry/REGRAS_APRENDIDAS.json`:

1. `evidence_annex:missing_input` → checklist do F1. Conferir que todo documento
   citado no comando existe antes de redigir; insumo ausente vira bloqueador
   nominado, nunca premissa. Lastro corrigido para 1 caso após o gate.
2. `reasoning:reasoning` → template do F4. **Declarar o cerco antes de sustentar
   a tese**: para cada capítulo, escrever o que a peça NÃO pede e NÃO reabre.
   Veio de ler o que o titular insere à mão nos dois retornos aproveitáveis —
   *"não se pretende a reabertura do mérito"*, *"sem alteração ou renúncia aos
   demais pedidos"*. Escrevemos a tese afirmativa e omitimos o cerco que bloqueia
   a leitura adversa. Lastro: 2 casos, 54 mudanças materiais.

O e-mail de agradecimento e estímulo à crítica está em
`templates/F10_EMAIL_RETORNO_E_AGRADECIMENTO.md`. É para escrever, não para
disparar: agradecimento com molde reconhecível deixa de ser lido na segunda vez.

Lições 237 a 249 em `RETROSPECTIVAS.md`.


## 26. S6 e S7 — identidade do ato e objeto devolvido (06/08/2026)

Com a varredura corrigida, 45 correções do titular ficaram legíveis. Cinco delas
foram lidas e produziram sete regras. Duas conclusões vieram junto e mudaram o
desenho.

### 26.1 Regra escrita que não pega

A identidade dos atos recursais é regra INVIOLÁVEL do protocolo desde
11/07/2026. Depois disso, o titular teve de corrigir à mão, em **dois clientes e
dois tribunais diferentes**, a citação de recursos do mesmo cliente estranhos
àquele trabalho e a transposição de dados de um processo paralelo para o
pautado. A síntese executiva estruturada, regra desde 07/07, teve o mesmo
destino.

Instrução escrita compete com todo o resto do prompt e perde. Por decisão do
Igor em 06/08, as duas viraram gate verificável.

### 26.2 Os dois gates

Ambos vivem em `forja_identidade_processual.py` e entram por
`forja_verificador.verificar`, no desenho já provado dos S2/S4: **lastro externo
declarado, e caso sem declaração não recebe veredito** — jamais P0 por ausência.
Os blocos são opcionais em `F2_IDENTIDADE_PROCESSUAL.json`:

| bloco | gate | o que reprova |
|---|---|---|
| `atos.{impugnado,proprios,relacionados}` | **S6_IDENTIDADE_DO_ATO** | identificador de processo ou recurso citado na peça e não declarado como deste trabalho |
| `objeto.{devolvido,excluidos}` | **S7_OBJETO_DEVOLVIDO** | tema declarado fora do objeto devolvido e ainda assim sustentado na peça |

S6 fecha um modo de falha que não deixa rastro lexical: **o recurso citado a
mais existe, é do mesmo cliente e está escrito corretamente.** Depois dele o
texto segue internamente coerente, e é por isso que nenhum gate de coerência
interna discorda — o mesmo diagnóstico que derrubou a primeira tentativa de gate
de identidade processual em 05/08. Só a lista externa separa um do outro.

S7 nasce da correção mais recorrente do titular: a peça trata de tudo o que é
verdadeiro sobre o caso em vez do que o tribunal pode decidir. A lista de
exclusões é **declarada por pessoa** — inferir escopo de prosa argumentativa é o
erro que a esteira já cometeu na figura de cronologia.

Detalhe de implementação que veio de falha: dois identificadores do mesmo ato
diferem no começo ou no fim (com e sem dígito verificador, com e sem sufixo do
tribunal), nunca no meio. A primeira versão absolvia por conteúdo em qualquer
posição, e um número curto contido por acaso dentro de um CNJ longo passava.

### 26.3 As sete regras em vigor

`learning_registry/REGRAS_APRENDIDAS.json`, todas com evidência medida:

| destino | regra |
|---|---|
| checklist F1 | conferir que todo documento citado no comando existe antes de redigir |
| checklist F1 | declarar o objeto devolvido e os temas fora dele antes de redigir |
| template F4 | declarar o cerco: o que a peça NÃO pede e NÃO reabre |
| template F4 | nomear e enfrentar a objeção HOJE mais forte contra o provimento |
| template F4 | separar o precedente DESTES autos (comando) do paralelo (espelho) |
| checklist F7 | recusar afirmação categórica onde o que decide é a ausência do fato |
| checklist F7 | documento já juntado não recebe ressalva de verificação |

As duas do F7 são complementares e precisam ser lidas juntas com a primeira do
F1: exigir lastro antes de escrever, e não hedgear o que já está provado.

Lições 250 a 254 em `RETROSPECTIVAS.md`.


## 27. Leitura integral das 49 correções (06/08/2026)

Com a varredura corrigida, as 49 mensagens do escritório vinculadas a caso
ficaram legíveis. Foram lidas todas: **35 com lição, 14 sem**. A triagem fica
registrada por mensagem (`triagem`, `triadaEm`) em `F10_RETORNO_SEM_ANEXO.json`,
de modo que a próxima leitura começa onde esta parou.

### 27.1 O padrão mais recorrente não estava na peça

A mesma cobrança apareceu em **cinco matérias distintas**, quatro delas no mesmo
dia: a esteira declarou "documento não localizado" sem dizer por quê. O titular
pediu a distinção de quatro situações — falta de habilitação nos autos,
restrição de permissão ou link, indisponibilidade na fonte, limitação da própria
ferramenta — e exigiu que as diligências fossem esgotadas e **registradas** antes
de considerar algo não localizado.

Nenhum diff de documento acharia isto: o padrão não deixa marca no texto da peça.

`forja_insumo_bloqueado.py` fecha o buraco com `F1_INSUMO_BLOQUEADO.json`:

| campo | exige |
|---|---|
| `causa` | vocabulário fechado com as quatro situações; "não localizado", "inacessível" e afins são recusados como sintoma |
| `diligencias` | onde, quando e resultado — sem elas, "indisponível na fonte" é indistinguível de "não procurei" |
| `consequencia` | o que da peça fica sem lastro |
| `rotaDeSolucao` | quem pode destravar e como |
| `recebidos` | inventário do que chegou e foi conferido, exigido sempre que há bloqueio |

O inventário veio da quinta matéria, onde a pergunta foi invertida: *"todo o
material foi encaminhado — a documentação não foi aberta?"*. Um bloqueio só
ganha sentido contra o que entrou: sem o inventário, "faltou tal peça" não
distingue documento que não veio de documento que veio e não foi aberto.

Elo **5-C** no F10. Caso sem bloqueio declarado passa sem o artefato — o gate
mede qualidade de diagnóstico, não cria burocracia.

### 27.2 O contrapeso que quase faltou

Horas depois de adotar "enfrentar a objeção mais forte da adversa", a leitura
trouxe a diretriz que a equilibra: **escrever da perspectiva do advogado da
parte, nunca da de quem julga.** Risco, objeção e precedente contrário são
identificados e enfrentados, inclusive por distinção tecnicamente sustentável,
mas jamais adotados nem antecipados como juízo desfavorável ao cliente.

Sozinha, a primeira regra empurraria a esteira mais fundo no modo juiz — que é
justamente o defeito que o titular vinha corrigindo. Duas regras verdadeiras
que, isoladas, se degradam. **Regra nova se lê contra as que já existem, e não
só contra a evidência que a motivou.**

### 27.3 A hierarquia de pesquisa que existia e a esteira não conhecia

Nove níveis, do pleno do STF à câmara do tribunal local, com o refinamento que
só quem litiga escreve: buscar **pelo relator e pelos integrantes da turma**
quando já há processo no tribunal ou prevenção; sem competência ou relatoria
conhecida, a busca fica genérica. Estava num e-mail de julho e nunca chegou a
artefato nenhum.

### 27.4 As 14 regras em vigor

`learning_registry/REGRAS_APRENDIDAS.json`. Por destino:

- **F1 (antes de redigir)** — conferir existência do insumo citado no comando;
  declarar o objeto devolvido e os temas fora dele; diagnosticar insumo
  bloqueado com causa, diligências, consequência e rota.
- **F4 (roteiro do redator)** — declarar o cerco; enfrentar a objeção mais forte;
  perspectiva do advogado e não do julgador; separar precedente destes autos do
  paralelo; ordem de busca jurisprudencial; alcance medido do fato favorável;
  premissa declarada por conclusão.
- **F7 (conferência)** — recusar afirmação categórica; não ressalvar o que já
  está nos autos; não colapsar categorias jurídicas no rótulo favorável;
  qualificar natureza e peso da fonte citada.

Lições 255 a 259 em `RETROSPECTIVAS.md`.

## 28. Repertório de skills por fase (06/08/2026)

Ordem do Igor. Havia 402 skills instaladas entre Claude (238), Hermes (132), Codex (26)
e projeto (6), e nenhuma ligação entre elas e as fases da esteira. Skill que o agente
não lembra que existe no ponto em que ela resolveria o problema é skill que não existe
— o mesmo modo de falha da Lição 89, o gate instalado na rota que ninguém percorre.

**O que foi criado.** `skills_repertorio/`, com um documento por fase — `F0.md` a
`F10.md`, mais `TRANSVERSAIS.md` e o cardápio mestre `LEIA-ME.md`. Cada documento traz
a fase em uma tela (produtor, revisor, entradas, saídas, gates, scripts da casa), uma
tabela de escolha em 30 segundos, as fichas das skills que servem ali, as combinações
que funcionam e **o que não usar naquela fase, com o motivo**.

**Natureza.** Cardápio, não contrato. Nenhuma skill do repertório é obrigatória, salvo
`helena` e `cicero` em F4, que já eram por ordem anterior. O contrato da fase e o
`CLAUDE.md` continuam prevalecendo.

**Gestão de contexto.** O agente lê **apenas** o documento da fase corrente. As fichas
se repetem em cada fase onde a skill serve — a redundância é deliberada, para que o
agente de F7 não precise abrir o documento de F1. Para consulta programática existe
`CATALOGO_SKILLS.json`, com `fases[]`, `alimenta[]` e os cinco eixos de modulação.

**Os cinco eixos de cada ficha.** Custo de contexto (baixo, médio, alto); dependência
externa (nenhuma, rede, login, crédito pago); risco de fabricação (nulo, baixo, alto);
reversibilidade (total, parcial, nenhuma); e **quem confere depois** — o gate, script
ou pessoa que valida a saída, nunca "ninguém". Nenhuma saída de skill entra na esteira
como conclusão; toda saída entra como insumo.

**As oito perguntas de decisão** estão no `LEIA-ME.md`. A primeira é a que mais corta:
qual artefato do contrato esta skill alimenta? Se o agente não sabe responder, não
invoca.

**Sete skills adaptadas**, em `..\.claude\skills\`: `forja-ingestao-autos`,
`forja-exploracao-problema`, `forja-campo-tribunais`, `forja-pesquisa-jurisprudencia`,
`forja-red-team`, `forja-revisao-cruzada` e `forja-saida-humana`. Elas **não substituem
nenhum script**: chamam `forja_injection_scan.py`, `forja_insumo_bloqueado.py`,
`forja_exploracao_100.py`, `forja_regimentos.py`, `forja_adversarial_audit.py`,
`forja_estilo_humano.py` e os demais, e acrescentam o que a versão genérica não sabe —
a ordem de pesquisa da Diretriz 28, o vocabulário fechado de causa de bloqueio, a
calibragem "advogado, não juiz", os dois passes de estilo de F7, e que
`familyAssurance` é recomposto pelo orquestrador e nunca aceito por declaração.

**Rejeições registradas** em `TRANSVERSAIS.md`, para não serem reabertas a cada rodada:
diagramação genérica (produz figura fora da identidade e sem os gates de legibilidade,
overflow e colisão), navegador redundante, jurídico duplicado, UI e frontend, a família
`gsd-*` inteira, segurança de sessão e as skills de coleta e campanha. Duas ficaram em
observação declarada: `proj-analise-juridica-preditiva` e `archify`.

## 29. Grok 4.5 pela assinatura do Cursor (06/08/2026)

Ordem do Igor. O Grok 4.5 já estava no registro de modelos desde 26/07, mas pelo
OpenRouter, que cobra por chamada — o que fazia do contraditório obrigatório uma
despesa por peça. O CLI do Cursor entrega o mesmo modelo pela assinatura já paga.

**A rota.** Provedor `cursor` em `forja_modelos.py`, modelo `grok-4.5-cursor`
(família `xai`, remoto **`cursor-grok-4.5-high`**). O despacho executa
`cursor-agent --print --output-format json --mode ask --trust --model cursor-grok-4.5-high`,
**com o prompt entregue por stdin**.

Três detalhes que custaram medição em 07/08/2026 e não são estilo:

1. **O ID no Cursor não é `grok-4.5`.** `cursor-agent --list-models` expõe
   `cursor-grok-4.5-{low,medium,high}` e as variantes `-fast`. Usamos `high`, porque
   contraditório se paga em raciocínio, não em latência. A mesma lista mostra
   `gpt-5.5-high` e `gpt-5.5-high-fast` disponíveis — e a trava de GPT-5.5 os reprova,
   conferido.
2. **O prompt vai por stdin, nunca por argumento.** O wrapper `.cmd` passa pelo
   cmd.exe, que **corta o argumento na primeira quebra de linha**. O modelo respondia
   sobre a primeira linha e devolvia texto plausível: o Diabob chegou a dizer "você só
   me nomeou, não há alvo" com o alvo dentro do prompt. Erro que não levanta exceção e
   produz parecer verossímil é o pior tipo desta casa, e por isso tem regressão própria.
3. **O CLI exige confiança no diretório de trabalho.** Em vez de confiar a pasta do
   caso — que tem autos, ledger e artefatos —, ele roda numa **pasta vazia dedicada**
   (`cache/cursor_sandbox`) com `--trust`. Nosso uso é texto que entra e texto que sai:
   o modelo não precisa de workspace, e pasta vazia não tem o que ser explorado.

**`--mode ask` não é detalhe:** sem ele o agente do Cursor tem ferramenta de escrita e
shell, e revisor externo não edita o caso.

O binário não entra no PATH na instalação padrão do Windows. A ordem de busca é
`FORJA_CURSOR_AGENT` → `%LOCALAPPDATA%\cursor-agent\cursor-agent.cmd` →
`shutil.which`. Foi criado também um atalho em `%USERPROFILE%\.local\bin\cursor-agent.cmd`,
que já está no PATH, para o uso manual no terminal.

**Custo declarado zero, e o motivo importa.** Não é grátis: é mensalidade. Não há preço
por chamada a registrar, e estimar centavos mentiria no ledger — que é o defeito que
este harness existe para não ter. Pelo mesmo motivo a contagem de tokens fica em zero:
o CLI não a expõe, e número estimado em ledger vira número citado depois. Quem precisar
medir consumo usa a rota OpenRouter. O ledger continua contando as **chamadas**, que é
o que permite ver volume.

**A assinatura OAuth é a única rota do Grok** (ordem do titular, 06/08/2026). A rota
`grok-4.5` do OpenRouter existe e cobra por chamada — por isso ela **não é automática**.
Se a assinatura falhar, `forja_diabob.py` e `forja_triagem_rapida.py` **falham alto**,
com a instrução de conserto (`cursor-agent login`), em vez de cair calados numa rota
paga. Gasto novo é decisão do titular, não consequência de um login vencido. A reserva
só entra com `--permitir-reserva`, e a queda fica declarada em `rotaDegradada`.

**Posto 1 — Diabob (F4 e F7), obrigatório.** `forja_diabob.py` usa `grok-4.5-cursor`.
Medido em 07/08/2026 com a rota já autenticada: 42 a 81 segundos por parecer, US$ 0,00,
`rotaDegradada: None`. Sobre a mesma frase de teste — "o prazo é de 15 dias porque o
cliente disse que foi intimado na sexta" — o Diabob separou o que a peça confundia:
a fala do cliente, se provada, funda o **início** da contagem, nunca a **duração** do
prazo.

**Posto 2 — triagem semântica da ingestão (F1).** `forja_triagem_rapida.py`, novo. Ele
existe porque o `forja_injection_scan.py` é lexical **e examina o PDF** — fonte abaixo
de 2pt, branco sobre branco, padrão de instrução conhecido; ele nem aceita `.txt` como
entrada. A triagem lê o **texto já extraído** atrás de sentido: instrução embutida em
prosa normal, documento fora do caso, incoerência interna, promessa de anexo sem lastro.
Os dois não veem o mesmo substrato, e é por isso que os dois rodam. É a Lição 267
aplicada: gate lexical só enxerga a forma que alguém já viu falhar.

As duas forças do modelo servem exatamente a este posto: **velocidade**, porque ingestão
tem volume e passada cara não roda em todo documento; e **perspectiva diferente**, porque
quem lê aqui não é o modelo que vai redigir a peça — leitor que já sabe a tese enxerga o
que confirma a tese.

Medição em fixture. Na primeira rodada, ainda sem a assinatura, ela caiu para o
`luna-5.6`: pegou a instrução embutida, a data impossível e os anexos prometidos, mas
**errou para mais**, apontando "conforme notas fiscais juntadas" num documento limpo.

Repetida em 07/08/2026 já no Grok pela assinatura, o resultado foi melhor: mesmos
achados verdadeiros, **zero falso positivo** no documento limpo, e as colunas de
verificação vieram no vocabulário fechado da casa ("não veio / veio e não foi aberto /
restrição"). Custou 45 a 48 segundos por documento, US$ 0,00.

**A melhoria que veio do próprio modelo.** Na primeira rodada com Grok ele declarou o
que lhe faltava: "sem o caso de destino da ingestão, não dá para dizer" se o documento
pertence ao caso — e, em vez de inventar, apontou o que precisaria ser cruzado. Foi
acrescentado o parâmetro `--contexto` (número CNJ, partes, órgão). Com ele, a categoria
"documento fora do caso" saiu de morta para viva: na repetição, cruzou número e partes
do documento contra o caso informado e acusou a divergência. Sem contexto, o prompt
manda explicitamente **não concluir** nada sobre pertencimento.

**Limites declarados no próprio artefato.** `F1_TRIAGEM_RAPIDA.json` carrega o campo
`natureza`: não é gate, não bloqueia, não substitui o scan lexical, e **ausência de
achado não é prova de documento limpo**. Texto acima de 24 mil caracteres é truncado, e
o laudo declara o corte — silêncio sobre corte vira cobertura falsa.

**Regressão:** `test_forja_cursor_grok.py`, 22 testes, nenhum dependente de rede ou
login. Protege o registro do modelo, o despacho, a leitura dos três formatos de saída do
CLI, a mensagem de erro útil, a queda declarada e o isolamento de falha por documento.
O último teste ancora a complementaridade: se o scan lexical um dia passar a aceitar
texto, a razão de existir da triagem precisa ser reavaliada, não presumida.

## 30. Diabob obrigatório vira gate de proveniência (07/08/2026)

A ordem de 06/08 pôs o Diabob no conselho obrigatório, ao lado de Helena e Cícero. No
mesmo dia ficou declarado o problema: a obrigatoriedade era **só texto**, porque o
`forja_conselho.py` validava apenas os dois pareceres. Pela regra da casa, regra escrita
que não pega vira gate — a identidade dos atos recursais foi violada em dois clientes
antes de virar o S6.

**O que o gate afere: a proveniência da chamada, não o texto.** Prosa dizendo "passou
pelo Diabob" é exatamente o que não prova nada, e é o formato que uma esteira apressada
produz sozinha. `forja_diabob.py --saida F4_PARECER_DIABOB.json` grava o **recibo** —
modelo, família, provedor, rota degradada, tempo, custo — junto com o parecer.

`forja_conselho.py` ganhou `diabob_present` (L-C4), chamado por `forja_run.py` em todo
F4. Comportamento medido em 07/08/2026 contra o artefato real e três fraudes plausíveis:

| Situação | Veredito |
|---|---|
| recibo real, família `xai` | `pass` |
| não declarado | `unknown` + P1 |
| prosa em vez de recibo | `fail` |
| família `anthropic` — a mesma que produz a peça | `fail`, nomeando o eco |
| recibo com parecer de casca (2 bytes) | `fail` |
| rota degradada declarada | `pass` + P1 |

`unknown` não é `pass`: é a recusa de atestar o que não se viu. Escolhido em vez de P0
para não reprovar retroativamente todo caso anterior à ordem — mesmo critério dos gates
S2, S4, S6 e S7.

**O teste legado me corrigiu no caminho.** `test_forja_conselho.py` afirmava que "o
conselho completo e bem formado" passa em todos os gates, e passou a falhar — porque a
definição de conselho completo mudou. A correção certa era a fixture, não o gate: ela
agora inclui o recibo do Diabob, e ganhou duas verificações novas — ausência fica
`unknown`, e contraditório da mesma família reprova. São 15 verificações, todas verdes.

**Prova em caso real.** Rodado sobre um blueprint de teste com o vício plantado ("o
prazo é de 15 dias porque o cliente disse que foi intimado na sexta"), o Diabob devolveu
3.780 bytes em 66 segundos, US$ 0,00, e foi ao ponto: *"está contando prazo sobre boato
do cliente e chamando isso de pergunta jurisdicional"*, exigindo o localizador nos autos
— publicação, portal, DJEN ou certidão — antes de qualquer contagem.

**O que não foi feito, e por quê.** `diabob_opinion` **não** entrou em `requiredOutputs`
de `F4.json`: entraria como exigência dura e derrubaria qualquer F4 em curso. O gate já
roda na rota real e já expõe a ausência. Promover a saída a obrigatória é o passo
seguinte, depois que os casos vivos passarem a produzir o artefato — decisão consciente,
registrada na ficha `decisoes/0002`.

**Kimi K3 não foi banido.** Aparece na assinatura do Cursor (`kimi-k3-high`) e foi
retirado do registro da FORJA em 26/07 após reprovar a bancada jurídica. Em 07/08 o Igor
decidiu não bani-lo. Ele segue fora do registro de modelos e disponível na conta; usá-lo
na esteira exigiria reinstalá-lo, o que é decisão nova e não está tomada.
