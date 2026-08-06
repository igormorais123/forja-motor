# Índice FORJA — 1 tela

**Portas de entrada:** `README.md` para começar; `DOCUMENTACAO_TECNICA.md` para o mapa completo; `docs/` para arquitetura, configuração, desenvolvimento e testes.

| Preciso de... | Vá para |
|---|---|
| Contrato de distribuição do motor genérico | `..\MOTOR_DISTRIBUICAO.md` |
| Separação física e acervo privado desta instalação | `SEPARACAO_MOTOR_ACERVO_2026-08-05.md` + `..\GITHUB_BACKUP_README.md` |
| Visão geral e começo rápido | `README.md` + `docs/GETTING-STARTED.md` |
| Arquitetura e fluxo de dados | `docs/ARCHITECTURE.md` |
| Configuração, flags e autenticação | `docs/CONFIGURATION.md` |
| Alterar o código com segurança | `docs/DEVELOPMENT.md` |
| Testes, régua e critérios de aceite | `docs/TESTING.md` |
| Regras normativas (fases, milestones) | `FORJA_SPEC_MANIFEST.json` |
| Estado da implementação N3 | `reports/IMPLEMENTACAO_FORJA_N3_2026-07-10.md` |
| Estado final auditado da implementação N4 | `reports/CONSELHO_SINTESE_IMPLEMENTACAO_FORJA_N4_2026-07-11.md` |
| Pareceres Efesto, Helena, Cícero e Diabob | `reports/CONSELHO_*_FORJA_N4_2026-07-11.md` |
| Aprendizados consolidados do Conselho | `APRENDIZADOS_CONSELHO_N4_2026-07-11.md` |
| Runbook completo de validação N4 | `RUNBOOK_VALIDACAO_CONSELHO_N4.md` |
| PRD, TDD, Roadmap e Diagramas N4 | `planejamento/10_*.md` a `planejamento/13_*.md` |
| Método PSO-Pet para definição, diagnóstico e desenho da petição | `planejamento/14_METODO_VAN_AKEN_APLICADO_A_PETICOES.md` |
| Roteiro preenchível PSO-Pet por caso | `templates/F4_METODO_SOLUCAO_PROBLEMA_PETICAO.md` |
| Exploração inicial obrigatória em 100 perguntas | `templates/F2A_EXPLORACAO_100_PERGUNTAS.md` + `planejamento/20_F2A_EXPLORACAO_100_PERGUNTAS.md` |
| Gerar/validar a árvore F2-A | `forja_exploracao_100.py` + `test_forja_exploracao_100.py` |
| Validador e indicadores PSO-Pet | `forja_pso_pet.py` + `test_forja_pso_pet.py` |
| Fila priorizada em operação (próximas peças, prontidão, score) | `python forja_fila.py` (`--proxima` consome o topo; `--dry` inspeciona; flag `filaPriorizadaV1`; regressão `test_forja_fila.py`) |
| FORJA FILA (priorização painel→FORJA, R1.1 Helena): PRD, TDD, Diagramas e Mapa de implementação | `planejamento/15_PRD_FILA_PRIORIZADA.md` a `planejamento/18_MAPA_IMPLEMENTACAO_FILA_PRIORIZADA.md` |
| Conselho quadripartite do sistema (11/07) e decisões acatadas/rejeitadas | `reports/conselho_2026-07-11/` (4 relatórios + `DECISOES_CONSELHO.md`) |
| Benchmark real e relatório PSO-Pet | `reports/PSO_PET_BENCHMARK_REAL_2026-07-11.json` + `reports/RELATORIO_PSO_PET_SOLUCAO_PROBLEMAS_E_METRICAS_2026-07-11.md` |
| Explicação visual da FORJA para advogados | `reports/FORJA_EXPLICADA_PARA_ADVOGADOS.html` (41 diagramas navegáveis, em linguagem simples; atualizado em 12/07/2026) |
| Edição visual Blender 2D e auditoria comparativa (ARQUIVADAS em 16/07/2026) | `C:\Users\IgorPC\.claude\projects\Forja visual 3d\reports_atlas_blender\` (movidas para fora do harness junto com o projeto 3D eliminado; ver LEIA-ME.md de lá) |
| Validar um caso N4 | `python forja_n4_validate.py <caseId>` |
| Contratos e artefatos N4 | `n4_schemas/` + `phase_contracts_n4/` |
| Pesquisa científica interdisciplinar | `forja_science.py` |
| Busca jurídica integrada (TeiaJus + STJ) | `forja_legal_search.py` + `FORJA_SEARCH_CONFIG.json` (`search`, `case`, `stj-health`, `stj-catalog`, `stj-search`, `stj-daily`, `stj-datajud`, `stj-collect`; telemetria em `telemetria/legal_search/`) |
| Integridade da entrega N4 | `forja_delivery_integrity.py` |
| Plano N3 de integridade, contexto, visual e gestão | `planejamento/08_PLANO_FORJA_N3_INTEGRIDADE_VISUAL_E_GESTAO.md` |
| Auditoria de peça adversária, má-fé e pontos decisivos | `planejamento/09_AUDITORIA_ADVERSARIAL_PONTOS_DECISIVOS.md` + `forja_adversarial_audit.py` |
| Validação completa N3 | `python validate_forja_n3.py --real-word --run-replay` |
| Replay dos 21 estados e seis casos representativos | `reports/N3_SHADOW_REPLAY_2026-07-09.md` |
| Eventos e estado N3 | `forja_state_machine.py` + `forja_run.py` + `phase_contracts/` |
| Contexto e fidelidade semântica | `forja_context.py` + `forja_fidelity.py` |
| Pacote e encerramento canônico | `forja_package.py` + `forja_close_cycle.py` |
| Sincronização com a gestão | `forja_management_bridge.py` + `..\gestao_escritorio\scripts\sync_forja_gestao.py` |
| Lições acumuladas (91) | `RETROSPECTIVAS.md` |
| Anti-autocertificação E2E | `forja_n4_e2e_adversarial.py` + `reports/N4_E2E_ANTI_SELF_CERTIFICATION_2026-07-11.json` |
| Métricas mecânicas antifraude | `forja_n4_anti_fraud_audit.py` + `reports/N4_ANTI_FRAUD_AUDIT_RESULT.json` |
| Gates automáticos de qualidade | `forja_verificador.py` (+ `test_forja_verificador.py` — rodar após qualquer mudança) |
| Escrita humana em peças e e-mails, sem vícios de IA | `PROTOCOLO_ESCRITA_HUMANA_FORJA.md` + `forja_estilo_humano.py` (+ `test_forja_estilo_humano.py`; bloqueia F6/F7/F9, render, pacote e rascunho; o corpo do e-mail é vinculado por hash) |
| **Revisão e escrita final (F7-B)** — modelo editorial padrão `claude-opus-5` desde 25/07/2026 | `PROTOCOLO_EDITORIAL_ESCRITA_FINAL.md` + `planejamento/21_F7B_FABLE5_REVISAO_ESCRITA_FINAL.md` + `forja_editorial.py` (shim legado: `forja_fable5.py`) + `forja_editorial_model.py` (allowlist) + `forja_editorial_fidelity.py` + `test_forja_editorial.py` (F7-B obrigatório; `final_markdown` é o cânone de F8) |
| Executar F7-B | `python forja_editorial.py <caseId> <attempt-dir> --source audited_markdown.md --f7-gate f7_gate_result.json`; incorporar `EDITORIAL_RESULT.json` (nome legado `FABLE5_RESULT.json`) ao `PHASE_RESULT.json` integral antes de promover |
| **Blindagem contra lastro aparente (L1-L8)** — transcrição verbatim como prova de leitura | `PROTOCOLO_LASTRO_DOCUMENTAL.md` + `forja_lastro.py` + `test_forja_lastro.py`; bloqueia em F7 (`fact_grounding_verbatim`) e na entrega (elo 9-B) |
| Calibrar a detecção de material econômico | `python forja_calibra_monetario.py --saida CALIBRACAO_MONETARIA.json` — mede a incidência da regra ampla × estreita sobre o acervo e amostra os falsos positivos (citação de lei lida como dinheiro). Evidência REEXECUTÁVEL da calibração dos gates L9-L13 |
| **Fonte prevalente e valor monetário (L9-L13) — IMPLEMENTADO em 04/08/2026** | Extensão FORJA-LASTRO-v2 DENTRO de `forja_lastro.py` (o v1 ancorava proposição, não número). Origem: incidente CASO-04 02/08/2026. **L9, L10, L12 e L13 bloqueiam; o L11 está em P1 por calibração** — conferir o módulo antes de citar severidade. Plano: `planejamento\41_...md`; catálogo: § U13 de `planejamento\06_GATES_QUALIDADE_FORJA.md`; evidência ao cliente: `RELATORIO_EVIDENCIA_GATE_DOCUMENTAL_2026-08.md` |
| Calibrar os gates econômicos L9-L13 contra o acervo | `python forja_calibra_gates_economicos.py` — mede incidência, separação citado × calculado e o teto de reprovação, e **nomeia** os casos limítrofes em `CALIBRACAO_GATES_ECONOMICOS.json`. Foi esta medição que rebaixou o L11 a P1; a promoção a P0 exige rodá-la de novo, não impressão |
| Rodar o gate de lastro sobre um artefato | `python forja_lastro.py <peca.md> [--ledger fact_ledger.json] [--base-dir DIR] [--revisao revisao.json] [--exigir-criterio]` |
| Auditar atualidade dos regimentos arquivados (E11) | `python forja_regimentos.py` (+ `RUNBOOK_AUDITORIA_REGIMENTOS.md`, `test_forja_regimentos.py`); exit 1 com bloqueio |
| Incidente que originou a blindagem (lastro aparente, CASO-23) | `INCIDENTE_VALE_TRADING_LASTRO_APARENTE_2026-07-26.md` |
| **Bancada de modelos (6 modelos, mesma peça real, juízes cegos)** — protocolo, peças e conclusões | `bancada_cafelana_v7/LEIA-ME.md` + `RELATORIO_BANCADA_V7.md`; rodar com `bancada_dossie.py` → `bancada_executar.py` → `bancada_avaliar.py` → `bancada_juizes.py` → `bancada_relatorio.py` |
| Números brutos da bancada (telemetria, canários, votos por critério, âncoras, auto-preferência) | `bancada_cafelana_v7/RESULTADOS_DETALHADOS_BANCADA_V7.md` — regerar com `python bancada_registro.py` |
| **Identidade de modelo e captura multi-turno** (apelido ≠ modelo; `json` devolve só o último turno) | `test_forja_identidade_modelo.py` — rodar após mexer em `forja_headless.py`, `forja_editorial.py` ou `forja_editorial_model.py` |
| Roteamento de modelo por fase, com perfis medidos | `planejamento/37_PLANO_HARNESS_MULTIMODELO.md` § 7 + `forja_modelos.py` (campo `forte_em`) |
| **Baseline de testes — porta de entrada única** (não rodar pytest direto: regressões standalone não são coletadas pelo pytest) | `python forja_baseline.py [--json CAMINHO] [--quiet]` — fotografia corrente: 83/83 suítes, 545 testes pytest, 60 subtestes e 41 scripts standalone (05/08/2026) |
| Contratos F7-B/F8 | `phase_contracts/F7.json` + `phase_contracts/F8.json` e extensões em `phase_contracts_n4/` |
| Regressão do passe editorial | `python -m unittest -v test_forja_editorial.py test_forja_estilo_humano.py test_forja_n3_runner.py test_forja_n3_package.py test_forja_n3_headless.py` |
| Evidência da execução viva Fable 5 | `reports/fable5_live_validation_20260715/` |
| Regressão histórica de compatibilidade do render inline/extrator de citações/cache F7/kit visual | `test_licao41.py` (somente compatibilidade de acervo; a produção atual não usa render; rodar após mexer em `forja_render_docx.py`, `forja_citations.py`, `forja_metricas_f7.py` ou `medina_visual_kit.py`) |
| Bateria REAL com telemetria (pipeline completa sobre artefatos de produção) | `test_real_telemetria_licao41.py` (JSON em `telemetria/`; rodar antes de declarar manutenção concluída) |
| Compatibilidade histórica (não usar na produção) | `forja_render_docx.py` materializa MD → DOCX/PDF para acervo legado; não faz parte da rota canônica atual e não deve ser usado para novas peças. |
| **Edição VISUAL LAW — ENTRADA ÚNICA DE PRODUÇÃO (desde 03/08/2026)** | `forja_visual_build.py`: gates F7 → brief `F7_5_BRIEF_VISUAL.json` → mapa automático (`forja_visual_mapa_gen.py`) → figuras (`forja_visual_figuras.py` + geradores em `medina_svg_kit.py`) → `forja_visual.compor()` → `forja_svg_docx.inserir_svgs()` → QA estrutural estática (`forja_visual_qa_structural.py` e lint SVG) → gate F8-S (`forja_assinatura_visual.py`). Sem EMF, Word COM, PDF, PNG ou renderizador. ~7s por peça. Mapa manual `compor_<caso>_mapa.py` vira refinamento opcional, não pré-requisito. Linguagem visual: skill `padrao-visual-medina`. **`--tipo peca|estudo` declara o produto** em vez de deduzi-lo por palavra-chave nas primeiras linhas: relatório ao cliente que não diga "relatório" na abertura era classificado como peça e cobrado por endereçamento e assinatura com OAB que não deve ter. **O DOCX desta rota é para os gates, não para enviar** enquanto a Lição 211 estiver aberta: o Word recusa abri-lo. O entregável sai por `montar_visual.montar()` (SVG→EMF + Word COM), que também gera o PDF e as imagens do QA de página |
| Brief visual F7.5 (contrato) | `templates/F7_5_BRIEF_VISUAL.md` — o autor declara âncoras da capa, cadeia argumentativa e cronologia. Sem ele só saem as figuras estruturalmente seguras, e peça longa não fecha o piso |
| Conselho e revisão cruzada do gate visual (03/08/2026) | `planejamento/25_CONSELHO_GATE_VISUAL_2026-08-03.md` (parecer dos 4, COM nota de superação parcial) + estado atual no topo do `planejamento/24_...md`. Revisão cruzada Codex achou defeito material no gate; lições 93-95 em `RETROSPECTIVAS.md` |
| Gate de desenho do SVG (SVGC) | `_FERRAMENTAS\medina_svg_colisao.py` — **bloqueante** na inserção SVG nativa (`forja_svg_docx.inserir_svgs`). SVGC-01 texto ocluído por forma opaca posterior; SVGC-02 texto sobre texto; SVGC-04 cor inválida (`fill="ffffff"` sem `#`); avisos SVGC-03 (traço cruzando texto) e SVGC-05 (contraste < 2,0:1). Pega o defeito que o F8-S não vê por verificar presença e não corretude do desenho. Regressão: `test_medina_svg_colisao.py` |
| Gate F8-S — assinatura visual | `forja_assinatura_visual.py` (verificação AFIRMATIVA de presença; taxonomia VIS-02/03/04/05/06/11). Figura é contada por **referência + existência do alvo**, nunca por arquivo em `word/media/`. A densidade usa páginas reais apenas quando há PDF irmão já existente, lido sem renderização; sem ele o laudo sai com `densidadeCalibrada: false`. Hoje em **modo observação**: grava `F8S_ASSINATURA_VISUAL.json` e não bloqueia. Regressão: `test_forja_assinatura_visual.py` (mutação) e `test_forja_assinatura_antimoldagem.py` (anti-moldagem, 6 destruições da peça aprovada) |
| Rodar fase de IA headless (OAuth) | N2: `python forja_headless.py <caso> <FASE> "<prompt>"`; N3: iniciar tentativa em `forja_run.py` e informar `--attempt-dir` |
| Fontes oficiais verbatim | `cache/fontes_oficiais/` (brutos em `raw/`) |
| Artefatos de um caso | `state/case-<id>/producao/` |
| Planejamento N2 (PRD/TDD/roadmap/diagramas/gates) | `planejamento/01..06_*.md` |
| Plano de upgrade × estado da arte 2026 (U1-U11, adotados/rejeitados) | `planejamento/07_PLANO_UPGRADE_ESTADO_DA_ARTE_2026.md` |
| Scan anti-injeção de prompt em PDFs (F1) | `python forja_injection_scan.py <pasta-ou-pdfs>` (+ `test_forja_injection.py`) |
| Regressão de alucinação de citação (6 modos) | `python test_forja_citacoes.py` (taxonomia em `planejamento/06_GATES...md`) |
| Diff pós-entrega (protocolada × nossa) | `python forja_diff_docx.py <nossa.docx> <protocolada.docx> [saida.md]` |
| Peças-modelo aprovadas por tipo (ler INTEIRA antes de redigir) | `..\_MODELOS\LEIA-ME.md` |
| Protocolos da fábrica (regimento, padrão Word, feedback humano) | `..\CLAUDE.md` e `..\APRENDIZADOS_FEEDBACK_HUMANO.md` |
| QA de páginas: densidade/branco/corte (M4.2) | `python forja_qa_paginas.py <pasta-pngs>` (+ `test_forja_qa_paginas.py`) |
| Mutação semântica S1-S6 (M3.1, critério 3 N4) | `python forja_mutation_semantic.py <caso>` (+ `test_forja_mutation_semantic.py`) |
| Ledger de citações materiais (M3.2, lição 52) | `python forja_ledger_material.py <caso>` (+ `test_forja_ledger_material.py`) |
| Coerência F2 tribunal×CNJ e perfil PSO (M4.3) | `forja_f2_check.py` (+ `test_forja_f2_check.py`) |
| Executor N3 — suíte dedicada (M4.1) | `test_forja_run.py` |
| Alertas P0 no painel (M1.1) | `forja_alertas.py` (+ `test_forja_alertas.py`) |
| Resumo da fila ao abrir sessão (M1.2) | `forja_local_context.py` (hook em `.claude/settings.json`) |
| Métricas de gates e tempo por fase (M1.3) | `python forja_metricas_gates.py` → `reports/METRICAS_GATES.json` |
| Ordem parecer→redação (M2.1) | `parecer_antes_da_redacao` em `forja_delivery.py` (+ `test_forja_ordem_parecer.py`) |
| Ciclos prospectivos N4 (M3.3) | `RUNBOOK_CICLO_PROSPECTIVO.md` |
| Plano de instalação de melhorias (M1-M4) | `planejamento/19_PLANO_INSTALACAO_MELHORIAS_FORJA_2026-07-12.md` |
| Painel de demandas | `..\gestao_escritorio\` (HTML gerado por `render_dashboard.py` — nunca editar direto) |
| **APRENDIZADO DO RETORNO HUMANO** — captura da peça protocolada, comparação, gate de comparabilidade, adoção e aplicação da regra | `forja_post_protocol.py` + `forja_aprendizado.py` (+ `test_forja_aprendizado.py`) |
| Varredura do Gmail (consulta derivada da allowlist de remetentes, não de `has:attachment`) | `python forja_post_protocol.py scan-gmail [--shadow]` |
| Gate de comparabilidade: a peça humana é revisão da nossa, ou outro documento? | `PP-NOT-A-REVISION` — piso de 0,30 de texto em comum (`_e_revisao`) |
| Correção que veio no corpo do e-mail, sem anexo a comparar | `PP-NO-RETURN-ATTACHMENT` → `state/<caso>/n4_artifacts/F10_RETORNO_SEM_ANEXO.json` |
| O que se repete no retorno do titular (ordenado por casos distintos) | `python forja_aprendizado.py padroes` |
| Ler o texto real das correções de uma classe (do cofre local; não grava) | `python forja_aprendizado.py amostra <camada:causa>` |
| Promover classe a regra, aplicar no destino e conferir | `python forja_aprendizado.py adotar/aplicar/conferir` |
| A evidência de cada regra adotada ainda existe? | `python forja_aprendizado.py revalidar` |
| Regras aprendidas em vigor (7) | `learning_registry/REGRAS_APRENDIDAS.json` |
| Gate S6 — ato citado na peça não declarado neste trabalho | `atos` em `F2_IDENTIDADE_PROCESSUAL.json` → `forja_identidade_processual.gate_s6_identidade_do_ato` |
| Gate S7 — tema sustentado fora do objeto devolvido | `objeto` em `F2_IDENTIDADE_PROCESSUAL.json` → `gate_s7_objeto_devolvido` |
| E-mail de agradecimento e estímulo à crítica (escrito por pessoa, nunca disparado) | `templates/F10_EMAIL_RETORNO_E_AGRADECIMENTO.md` |
| **AUTO-RESEARCH (ciclo AR)** — PRD/TDD v1.1 pós-review adversarial Codex | `planejamento/22_PRD_AUTORESEARCH_FORJA.md` + `planejamento/23_TDD_AUTORESEARCH_FORJA.md` |
| Candidata AR — materialidade de pendências e entrega sem espera artificial (`estudo_descritivo`, não promovida) | `autoresearch/candidates/materialidade-pendencias-v1/` |
| Propriedade intelectual da FORJA (registro INPI, marca, segredo de negócio; patente descartada) | `planejamento/24_ANALISE_PROPRIEDADE_INTELECTUAL_FORJA.md` |
| **PARECER FINAL E CONSOLIDAÇÃO DO CONSELHO (25/07/2026)** — decisões de Helena e Cícero, migração Fable 5 → Opus 5 com revisão cruzada entre famílias, P0 do `art. 343-A`, reconciliação de cânone e ordem de execução | `planejamento/36_CONSOLIDACAO_CONSELHO_E_PARECER_FINAL.md` |
| **CÂNONE DE EXECUÇÃO — PRD, TDD e roadmap (`FORJA-ASSINATURA-LITE-v1`)** | `planejamento/33_PRD_FORJA_ASSINATURA_LITE_COCRIACAO_PRECEDENTES.md` + `34_TDD_...md` + `35_ROADMAP_EXECUCAO_FORJA_ASSINATURA_LITE.md` |
| Anexos a fundir no cânone (tarefa 0 da Onda 0): conchas do catálogo N4, registro de decisão, 13 testes negativos, registro de escopo | `planejamento/ANEXO_A_...md`, `ANEXO_B_...md`, `ANEXO_C_...md` |
| Pareceres do conselho sobre o plano | `planejamento/pareceres/HELENA_FORJA_COCRIACAO_2026-07-25.md` + `CICERO_FORJA_COCRIACAO_2026-07-25.md` |
| Consolidações de arquitetura (histórico e insumo) | `planejamento/31_PLANO_UNICO_CONSOLIDADO_2026-07-25.md` + `32_PLANO_UNICO_CONSOLIDADO_V2_2026-07-25.md` |
| Requisitos declarados pelo titular (entrevista Fábio Medina Osório, 25/07/2026) — fluxo desejado, 19 lacunas, padrões de pensamento e linguagem | `planejamento/29_REQUISITOS_ENTREVISTA_FABIO_MEDINA_OSORIO.md` |
| Arquitetura dos 3 eixos (fonte do plano 31) — dialética, identidade Medina Osório e sistema de precedentes sobre o TeiaJus | `planejamento/30_ARQUITETURA_DIALETICA_IDENTIDADE_E_PRECEDENTES.md` |
| Corpus AR (split HMAC por linhagem; sealed fora do workspace) | `python forja_ar_corpus.py --scan/--check/--report` → `autoresearch/AR_CORPUS.json` |
| Painel de indicadores AR (I1–I10; null motivado; máscara pareada) | `python forja_ar_indicadores.py --md <peca> [--ledgers <dir>] / --comparar <a> <b>` |
| Canários de falha única (públicos + camada secreta externa) | `python forja_ar_canarios.py --verificar [--secreto]` (kill por sensor; controles benignos vivos) |
| Execução pareada vigente×variante | `forja_ar_runpair.py` (`--freeze/--register/--validate`) |
| Julgamento cego pairwise (swap, 2 famílias, consolidação por hash) | `forja_ar_blind.py` (`--prepare/--consolidate`; mapping HMAC fora do workspace) |
| Ciclo AR e gate de promoção (3 estados; log encadeado por hash) | `forja_ar_ciclo.py` (`snapshot/promotion/independent-review/human-approve/relatorio`) |
| Regressão AR (23 testes, 12 sabotagens nominais — na Régua) | `python -m pytest test_forja_autoresearch.py -q` |
| Relatório do ciclo AR-0 (piloto descritivo, σ por indicador) | `autoresearch/ciclos/ciclo-0/AR_CICLO_0_RELATORIO.md` |

Fluxo padrão de um caso: RETROSPECTIVAS → scan anti-injeção nos PDFs (F1) → leitura da peça-modelo do tipo (`_MODELOS`) → **auditoria de regimento do tribunal (`forja_regimentos.py`)** → **perfil PSO-Pet proporcional em F2-F4** → **se houver peça adversária, auditoria A1 em F3/F4/F7** → pareceres obrigatórios de Helena e Cícero antes da redação → verificação independente de fatos/citações → **lastro verbatim no `fact_ledger` (L1-L8)** → auditoria F7 com zero P0 → **F7-B controlada: o modelo editorial revisa e escreve `final_markdown`; o resultado é incorporado ao resultado integral e o orquestrador recompõe hashes/invariantes** → triagem humana das dúvidas → materialização estática OOXML/SVG → QA estrutural e conferência humana → rascunho Gmail (nunca enviar) → painel → retrospectiva.
| Camada evolutiva Karpathy (gerações, winners, convergência) | `forja_ar_evolucao.py` (`init/nova-geracao/selecionar/convergencia`) → `autoresearch/evolucao/<experimento>/` |
| Ciclo AR-1 real (geração 0 do prompt-mestre; 2 rounds de juiz invalidados + 1 válido) | `autoresearch/ciclos/ciclo-1/AR_CICLO_1_RELATORIO.md` + `AR_PARECER_INDEPENDENTE_varB.md` |
| Diagrama canônico do ciclo AR (archify workflow: raias por ator, anulações reais, gate humano) | `autoresearch/ciclos/ciclo-1/AR_CICLO_HUMANO.html` (fonte: `ar-ciclo-humano.workflow.json`) |
| Ciclo AR-2 real (gen-1 hybrid perdeu; cegamento vazado pego e anulado; 2º gap v1) | `autoresearch/ciclos/ciclo-2/AR_CICLO_2_RELATORIO.md` + `AR_PROMOTION_NOTA.md` |
| Protocolo canônico do juiz cego do ciclo AR (obrigatório em toda bancada) | `templates/AR_JUIZ_PROTOCOLO.md` |

## GATES COMPUTADOS — fim da autovalidação (04/08/2026)

Até 04/08/2026, 42 dos 73 gates declarados nos contratos eram escritos pelo próprio agente da fase: ele recebia `requiredGates` no `RUN_CONTEXT` e devolvia `pass` no `PHASE_RESULT`. Nenhum código conferia. Hoje os 73 são computados.

| O que fazer | Comando |
|---|---|
| Quem decide cada gate | `python forja_gate_liveness.py` |
| O gate dispara em caso real? | `python forja_recomputo_censo.py` |
| **O gate sabe dizer não?** | `python forja_canario_mutacao.py` |
| **O leitor alcança o artefato na forma em que ele existe?** | `python forja_forma_artefatos.py` |
| Vocabulário dos artefatos e deriva | `python forja_artefatos.py` |
| **A catraca sabe reprovar?** | `python forja_canario_catraca.py` |
| **O que a casa APROVOU continua sendo lido igual?** | `python forja_baseline_aprovado.py` |
| **O gate de assinatura visual ainda sabe reprovar?** | `python test_forja_assinatura_antimoldagem.py` |
| **A rota que tem os gates está sendo percorrida?** | `python forja_adocao_rota.py` (05/08/2026: **1 de 40 obras**, desduplicado por conteúdo) |
| **A mutação semântica mata o mutante?** | `python forja_mutation_lote.py` (05/08/2026: **0,147**, alvo 0,80 — S2 e S4 em **zero**) |
| **A campanha de melhoria saiu dos trilhos?** | `python forja_lapidacao_governanca.py --invariantes` |
| **Duas melhorias disputam o mesmo arquivo?** | `python forja_lapidacao_governanca.py --propriedade melhorias.json` |
| **Toda peça atravessa o verificador, venha por onde vier?** | `python test_forja_porta_unica.py` |
| Catracas (não deixam piorar) | `test_forja_gate_liveness.py`, `test_forja_recomputo_censo.py`, `test_forja_canario_mutacao.py`, `test_forja_forma_artefatos.py`, `test_forja_artefatos.py`, `test_forja_canario_catraca.py` |

Os quatro medidores respondem perguntas diferentes e nenhum substitui o outro. O **liveness** diz quem decide; o **censo** diz se o produtor roda sobre material real; o **canário** destrói o artefato aprovado e exige que o veredito mude — é o único que distingue "esteira limpa" de "gate cego"; o **censo de formas** pega a falha que não gera erro nenhum, o gate que lê `x.json` quando o artefato é `x.md` e devolve um `warn` educado que o operador entende como "conferido". Cinco gates caíram nessa em 04/08/2026.

O **canário de catraca** fecha o círculo por cima: os outros quatro medidores são guardados por constantes de catraca, e nenhuma delas jamais tinha sido vista falhando. Ele aperta cada uma ao impossível e cobra a reprovação — 18 catracas, todas reprovaram —, e imprime em toda execução a lista dos valores vigentes, para que **afrouxar uma catraca seja decisão visível e não acidente**. Foi assim que apareceu, nesta leva, uma catraca afrouxada de 3 para 4 por uma sessão paralela: legítima, porque o acervo cresceu, e agora rastreável.

Triagem nominal das reprovações reais, com o que é defeito de caso e o que era defeito do gate: `TRIAGEM_REPROVACOES_CENSO_2026-08-04.md`. O que há dentro dos gates que nunca produziram veredito — e por que os dezesseis da F8 ainda não conheceram uma peça real: `LACUNA_GATES_SEM_VEREDITO_2026-08-04.md`.

| Quem sai do padrão Word do escritório | `python forja_varredura_tipografica.py` (catraca: `test_forja_varredura_tipografica.py`) |

A primeira execução dos gates visuais contra peças reais, com os falsos positivos que barravam o padrão da casa: `F8_PRIMEIRA_EXECUCAO_REAL_2026-08-04.md`. A varredura tipográfica do acervo inteiro, com a medição refeita pelo leitor de herança de estilos e o descarte de versões superadas — 4 de 122 entregáveis abaixo de 50% de justificação: `VARREDURA_TIPOGRAFICA_ACERVO_2026-08-04.md`.

O **baseline do padrão aprovado** é a peça que faltava, e ela responde a um defeito estrutural: a fábrica tinha 73 gates que sabem reprovar e **nenhuma memória conferível do que está certo**. O padrão aprovado vivia como regra escrita em protocolo, e regra escrita não se confere contra artefato — foi assim que, em 04/08/2026, quatro gates reprovaram o padrão do dono no mesmo dia. `BASELINE_APROVADO.json` congela três âncoras reais com o **veredito medido na data da aprovação**, e não com "zero achados", porque congelar perfeição seria mentira: o template tem uma linha de exemplo não justificada. Divergência aqui não diz que o gate está errado; diz que alguém precisa decidir, por escrito, qual dos dois lados mudou. Do outro lado, `test_forja_layout_antimoldagem.py` estraga de propósito uma peça aprovada e exige que o gate acuse — porque quatro afrouxamentos seguidos e um verde perfeito no fim são, pelo resultado, indistinguíveis de um gate moldado até aprovar. O parecer do conselho que diagnosticou isso: `CONSELHO_O_QUE_FALTA_2026-08-04.md`.

A mesma prova foi estendida ao **gate de assinatura visual** em 05/08/2026, e ali ela derrubou o instrumento duas vezes antes de sustentá-lo: o F8-S contava figura por arquivo no pacote (copiar quatro EMF órfãos para dentro do zip virava peça reprovada em CONFORME) e, depois de corrigido, contava referência sem conferir se o alvo existia (figura quebrada valia como figura). A `FAIXAS` de densidade estava inerte desde sempre, e a tentação de ressuscitá-la por estimativa foi **rejeitada por medição** — 60% de acerto de faixa contra 269 pares DOCX/PDF reais não sustenta uma catraca de quatro faixas. O relatório completo, com as quatro perguntas do Diabob respondidas por número, está em `F8S_ANTICIRCULARIDADE_2026-08-04.md`. A adoção continua sendo o risco operacional dominante: a medição mais recente encontrou apenas **1 de 40 entregas recentes (2%)** pela rota canônica; a porta única bloqueia o desvio quando o artefato passa por `PecaVisual.salvar()`, mas isso não substitui elevar a adoção na produção.

A rota canônica de produção tem regressão com **material real**: `test_forja_visual_build_peca_longa.py` compõe o markdown auditado do CASO-04 (18 seções, 2 figuras). Existe porque o teste sintético de um parágrafo não achava dois defeitos que quebravam a produção — numeral romano com teto em XV e `Path` não serializável no laudo de colisão SVG, este último com o pior formato de falha possível: peça sem figura passava, peça com figura quebrava. O inventário da divergência entre `AGENTS.md` e `CLAUDE.md`, para a decisão de reconciliação: `DIVERGENCIA_AGENTS_CLAUDE_2026-08-04.md`.

**Cuidado com os dois lugares.** O censo mede; quem roda na promoção de uma fase é `forja_run._validate_result`. Já aconteceu de a correção entrar só no medidor: `test_forja_rota_forma.py` guarda a fiação da rota de produção contra essa reincidência.

Produtores, por fase: `forja_ingestao` e `forja_injection_scan` (F1) · `forja_exploracao_100.gates_da_exploracao` e `forja_produto` (F2) · `forja_regimento_gate` e `forja_adversarial_gate` (F3) · `forja_conselho` (F4) · `forja_fontes_oficiais` (F5) · `forja_paragrafos` e `forja_redacao` (F6) · `forja_lastro`, `forja_citations`, `forja_replay`, `forja_contexto`, `forja_red_team`, `forja_p0` (F7) · `forja_f8_contract` (F8) · `forja_entrega` (F0/F9) · `forja_f10_contract` (F10).

Vocabulário canônico dos artefatos em `forja_artefatos.DIALETOS`, fonte única dos mapas de sinônimo. Detalhe e critérios: `planejamento/06_GATES_QUALIDADE_FORJA.md`, seção "Levas 12 a 17".

**Não decore o estado.** Os números envelhecem; rode os dois medidores antes de afirmar qualquer coisa sobre a cobertura da esteira.

## LAPIDACAO AO RIGOR DO SQLITE TEST HARNESS (05/08/2026)

Campanha de três ondas, 18 agentes, governada por `GOVERNANCA_LAPIDACAO_2026-08-05.md`
(envelope da Helena) e por `forja_lapidacao_governanca.py` (invariantes executáveis do
Efesto — os sete critérios de parada conferidos contra o estado vivo, cada um visto
reprovando uma sabotagem em `test_forja_lapidacao_governanca.py`).

**O número que a campanha existiu para produzir**, medido nos dois lados com os mesmos
6 casos e 102 mutantes:

| | Congelada `3866e1c16` | Aperfeiçoada |
|---|---|---|
| Escore geral | 0,1078 (11/102) | **0,1471 (15/102)** |
| S5 sobreabstração | 0/23 | **4/23** |
| S1, S2, S3, S4, S6 | — | idênticas |

O ganho é **inteiramente** de uma família. **S2 (troca de parte, 0/23) e S4 (troca de
pedido, 0/12) continuam em zero nas duas versões**: inverter o pedido da própria cliente
sai protocolável. Alvo do harness: 0,80. O relato completo, incluindo o gate revertido por
reprovar 2 das 3 âncoras aprovadas, está em `LAPIDACAO_ONDA2_RESULTADO_2026-08-05.md`; a
medição da onda 1 em `LAPIDACAO_ONDA1_MEDICAO_2026-08-05.md`.

Antes desta campanha o harness de mutação semântica havia rodado em **2 dos 53 casos** na
história do sistema. Lições 195-204 em `RETROSPECTIVAS.md`.

**Por que S2 e S4 continuam em zero — leia antes de tentar fechá-las.**
`DIAGNOSTICO_S2S4_2026-08-05.md`. A campanha prescrita pelo veredito ("comparar contra o que
o caso registra em `FORJA_CASE_MANIFEST.json`") **não é executável**: o manifesto não declara
parte nem pedido em nenhum dos 27 casos. Falta um **fato**, não um gate — nenhuma verificação
confere coerência contra verdade que o sistema nunca gravou. Fechar as duas famílias exige
primeiro criar a declaração de cliente, papel processual e direção do pedido, lastreada em
fonte **externa à redação** (comando do caso ou decisão impugnada), porque artefato derivado
do texto da peça seria mutado junto. Isso muda o protocolo de entrada de caso e é decisão do
Igor com Helena e Cícero, não reparo de engenharia.

**Quem commita sozinho.** `DIAGNOSTICO_AUTOCOMMIT_2026-08-05.md`. É
`git-tools/sync_github.ps1`, diário: faz `commit` no branch **corrente** mas `push` sempre em
`main`, e o push **falha desde 31/07** por objetos acima do limite de 100 MB do GitHub —
`main` local está 26 commits à frente do remoto. Consequência prática para quem trabalha
aqui: branch de trabalho nesta pasta pode receber commit de sincronização, e o GitHub não é
cópia de segurança atual do acervo.

## FRONTEIRA MOTOR / ACERVO (06/08/2026)

A FORJA vive em dois repositórios fisicamente separados no PC e uma zona que
não é versionada. `forja-motor` é o produto genérico, indistinguível e
compartilhável por qualquer escritório; `forja-auditoria` é privado e recebe
informação do escritório, identidade, configuração, casos e evidência
operacional. A divisão é também de pasta:

```text
%USERPROFILE%\repos\
├── forja-motor
└── forja-auditoria
```

Quem decide de que lado está cada arquivo é **uma função**, e não uma lista:
o sincronizador e o gate consomem a mesma política.

| recurso | o que faz |
|---|---|
| `forja_fronteira.py` | `classificar(caminho)` devolve MOTOR/ACERVO/LOCAL com o motivo; `varrer()` reprova nome de cliente, CNJ, CPF, CNPJ e OAB no motor; `--mapa` escreve `FRONTEIRA_DO_DISCO.md` na raiz; `--classificar` responde por um caminho |
| `test_forja_fronteira.py` | 46 casos: classificação, detecção real, vocabulário que NÃO pode acusar, valor sintético, máscara da casa, degradação sem o acervo |
| `forja_acervo.py` | a **única porta** pela qual o motor pede algo ao acervo: `caminho()`, `caso()`, `valor()`, `disponivel()`, `autos_disponiveis()` |
| `forja_anonimizar.py` | troca nome de cliente por pseudônimo estável e mascara CNJ/OAB preservando ano, segmento e tribunal |
| `git-tools/sync_forja_repos.py` | publica os dois repositórios; **roda a fronteira antes e não publica se ela reprovar** |
| `git-tools/montar_forja.py` | clona os dois, sobrepõe e **roda o baseline** — montagem que não termina em prova é promessa |

Registros que vivem no acervo e fazem o motor funcionar sem carregar cliente:
`ACERVO_CASOS.json` (rótulo → caseId), `ACERVO_FIXTURES.json` (chave → caminho),
`ACERVO_VALORES.json` (chave → valor esperado), `BASELINE_ANCORAS.json` (peças
aprovadas) e a família `FRONTEIRA_*` (nomes protegidos, curadoria, pseudônimos).

Estado medido em 05/08/2026: motor com 531 arquivos e **zero sinal de cliente**
conferido em modo nominal contra o clone publicado; árvore montada a partir dos
dois repositórios roda **91/91 suítes**. As pastas de caso continuam na raiz por
decisão medida — ver Lição 223.

## VIGIAS — o que roda sozinho, e por que cada um existe (06/08/2026)

Três tarefas agendadas no Windows. Nenhuma delas peticiona, envia mensagem ou
decide qualquer coisa: todas apenas **olham** e, quando encontram algo, deixam um
arquivo visível na raiz do harness — log que ninguém abre não avisa ninguém.

| tarefa | módulo · wrapper | quando | o que faz | flag que levanta |
|---|---|---|---|---|
| `FORJA-Monitor-STF` | `forja_monitor_stf.py` · `monitor_stf_diario.ps1` | 09:00 | raspa a aba de andamentos de um processo do Supremo | `NOVIDADE_STF.md` |
| `FORJA-Monitor-DJEN` | `forja_monitor_djen.py` · `monitor_djen_diario.ps1` | 09:15 | consulta a base nacional de comunicações, que cobre todos os tribunais e devolve o **teor** de cada ato; marca como urgente o que fala em pauta, sustentação, julgamento, acórdão, sentença, prazo ou destaque | `NOVIDADE_PROCESSUAL.md` |
| `FORJA-Fios-Abertos` | `forja_fios_abertos.py` · `fios_abertos_diario.ps1` | 09:30 | lista os fios de e-mail em que a última palavra **não** é minha | `FIO_SEM_RESPOSTA.md` |

Códigos de saída, iguais nos três: `0` sem novidade, `10` com novidade, `1` em
erro, `2` sem alvo configurado.

**Nenhum deles carrega dado de cliente.** Número de processo, nome de parte e
endereço de escritório moram no acervo, sob `monitor_djen_vigiados` e
`fios_remetentes_casa` em `ACERVO_VALORES.json`. Sem o acervo, os módulos rodam
sem alvo e **dizem** que rodaram assim, em vez de rodar em silêncio.

Regressões: `test_forja_monitor_djen.py` (9 casos) e `test_forja_fios_abertos.py`
(6 casos), ambos com o defeito real que motivou o vigia como fixture — a
intimação de pauta vista por acaso três semanas depois, e o retorno do escritório
sobre peça já entregue.

**Armadilha registrada (Lição 235):** as tarefas invocam `powershell.exe`, que é
o Windows PowerShell 5.1 e lê `.ps1` **sem BOM** como ANSI — todo acento vira
erro de parse e o script morre antes da primeira linha. Os três wrappers estavam
assim até 06/08. Wrapper com acento nasce com BOM UTF-8, e canário de tarefa
agendada se roda com o comando literal de
`(Get-ScheduledTask <nome>).Actions[0]`, nunca no shell da sessão.

Estado medido em 06/08/2026: fronteira **aprovada** com 575 arquivos no motor;
baseline **104/104 suítes verdes**, 647 testes pytest, 66 subtests e 46
regressões em script, com `test_real_telemetria_licao41.py` em quarentena
declarada.
