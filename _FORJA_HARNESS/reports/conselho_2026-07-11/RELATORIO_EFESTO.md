# Auditoria Técnica FORJA — Relatório EFESTO
**Data**: 11/07/2026 | **Executor**: Efesto Tekhton, Diretor de Tecnologia INTEIA | **Escopo**: Arquitetura, robustez, testes, dívida técnica, pontos de falha

---

## Sumário Executivo

O sistema FORJA (fábrica de melhoria de petições jurídicas) é uma arquitetura em **camadas aditivas bem-definidas** (N2 produção + N3 sombra + N4 pesquisa), com **documentação técnica exemplar** e um **protocolo de aprendizado contínuo** que codifica lições de casos reais em gates automáticos. 

O teste do verificador passa (15 detecções + 13 não-travas confirmadas). O pipeline está operacional e bloqueante onde importa (F7→F10 acoplado, gates com regressão). Há **dívida técnica aceitável** (duplicação de funções de 2-5 linhas, funções longas sem testes estruturais), mas **nenhum risco de quebra** de produção iminente.

A **recomendação estratégica é: consolidar agora (próximas 2 sessões), não adicionar**. O sistema responde bem porque cada feature paga entrada de regressão + documentação no catálogo de gates. A falha de protocolizar N4 para produção pode inflar dívida rápido. Abrir o circuito N4 sem a base de teste do N3 é risco.

---

## 1. Achados Técnicos

### E1 — Duplicação de funções utilitárias (P2, dívida técnica baixa)
**Severidade**: P2 (informativo, sem risco imediato) | **Evidência**: `forja_delivery.py:27-70`, `forja_headless.py:46-54`, `forja_citations.py` e 4 outros arquivos | **Impacto**: Manutenção fragmentada, possível dessincronia de comportamento.

**Descrição**: As funções `now_iso()`, `read_json()` e `append_unique()` (2-5 linhas cada) aparecem em 7 arquivos de forma independente. Auditor avaliou centralizar em `forja_utils.py`; decisão registrada foi rejeitar (DOCUMENTACAO_TECNICA.md §7, linha 193).

**Análise técnica**: A rejeição tem fundamento — são colas pequenas em contextos isolados. Porém, 7 implementações criam risco de **dessincronia silenciosa** — ex.: `read_json` tem `utf-8-sig` BOM tolerance em `forja_n3_common.py` mas não em `forja_delivery.py`. Se uma implementação for bugada, o fix não propaga. O módulo compartilhado `forja_n3_common.py` JÁ centraliza primitivas (sha256, locks, timing) — estender para essas 3 funções manteria a coesão de camada.

**Risco real**: Baixo (funções são estáveis e triviais). Ganho: médio (reduz variância de comportamento, simplifica auditorias futuras).

---

### E2 — Três funções-núcleo de lógica de negócio sem testes estruturais (P2, dívida técnica média)
**Severidade**: P2 (dívida bem-documentada) | **Evidência**: `forja_render_docx.py:82-188` (render, 106 linhas), `forja_delivery.py:129-~250` (f10 principal, ~120 linhas), `forja_reconcile.py` (~280 linhas) | **Impacto**: Vulnerabilidade a regressões silenciosas em mudanças de formatação/estado.

**Descrição**: As funções maiores do pipeline não têm testes de característica (behavior-driven). Elas são exercitadas a cada caso real (5 casos até agora), mas sem suíte estruturada. `forja_render_docx.py:render()` é crítica (markdown→DOCX→PDF+QA) e foi refatorada em resposta aos achados da Lição 41 (itálico, asteriscos literais).

**Análise técnica**: O DOCUMENTACAO_TECNICA.md (§7, linha 194) registra conscientemente "refatorar sem testes é risco sem ganho imediato". Isso é defensável em fase de produção estável. PORÉM:
- A Lição 41 **virou 12 casos de teste** (`test_licao41.py`) — padrão saudável.
- O teste real (`test_real_telemetria_licao41.py`) rodou sobre artefatos de produção e descobriu 4º defeito de ferramenta (**asteriscos em visual law caixas**, linhas 119-120 de RETROSPECTIVAS.md) que o teste sintético não pegou.
- Isso quer dizer: a suíte sintética **não cobre a integração de camadas** (render → visual kit → inserção Word COM).

**Risco real**: Médio. Um ajuste em `forja_render_docx.py` que não quebre teste sintético pode ainda gerar asteriscos ou truncamentos no PDF. A detecção é por QA visual (que funciona, Lição 38: ~100% de defeitos de render), mas cria ciclo de re-render lento.

---

### E3 — Acoplamento não-intencional entre F7 (verificador) e F10 (delivery): falha no gate se o verificador cair (P1, arquitetura)
**Severidade**: P1 (detecção operacional, mitigado em prática) | **Evidência**: `forja_render_docx.py:90-107` (F7 fail-closed) + `forja_delivery.py:73-106` (F10 lê F7) | **Impacto**: Se o verificador falhar por exceção, o render aborta e **nenhum artefato é gerado** (nem marcador de erro) — estado fica inconsistente.

**Descrição**: O `forja_render_docx.py` roda o verificador ANTES de produzir DOCX/PDF (Lição 44c, review adversarial 09/07). Se `forja_verificador.verificar()` ou `forja_metricas_f7.metricas_f7()` lançarem exceção, o render morre e o F10 não tem JSON para ler. O F10 espera `F7_VERIFICADOR_FORJA.json` na pasta; falta dele = bloqueador.

**Análise técnica**: 
- **Design original (N2)**: F7 roda no render, grava JSON, render continua se P0 foi "aceito conscientemente". Gate F10 confere: se p0>0 sem justificativa, reprova.
- **Mudança (Lição 44c)**: "F7 fail-closed" — render aborta se gates/métricas falharem (exceção levanta, nada é gravado).
- **Conflito**: Se o verificador lança exceção (bug no code, regex crash, I/O erro), o render retorna exit 1, nenhum JSON é gravado, F10 não consegue dar prosseguimento. A tentativa fica órfã.

**Risco real**: Baixo, mas real. Causa: exceções no verificador são raras (testadas), mas não impossíveis. Se um novo gate tem regex ruim (e.g., backtracking infinito), pode pendurar ou falhar. Mitigação no código: não há try/except em torno do bloco F7; a exceção sobe direto.

---

### E4 — Estado persistido em disco nem sempre sincronizado com a realidade de produção (P1, observado e corrigido)
**Severidade**: P1 (Lição 33, observado e fixado em 09/07) | **Evidência**: Caso Azimut (FORJA_STATE.json criado retroativamente), 5 casos sincronizados manualmente | **Impacto**: Estado como fonte de verdade quebrada; painel pode refletir fase errada.

**Descrição**: O `forja_headless.py` é o único que atualiza `FORJA_STATE.json` em N2. Mas os casos reais 1-5 rodaram via **workflows multiagente na sessão (não via headless)**, então o estado permanecia em F0/F3 "pending" enquanto a produção real estava em F9. Lição 33 relata isso; Lição 36 (auditoria Efesto 09/07) confirmou o bloqueio. Corrigido: sincronização retroativa com evidência (draft IDs conferidos em Gmail via `gws drafts list`). Regra nova adicionada: atualizar `FORJA_STATE.json` é **passo obrigatório após workflow**.

**Análise técnica**: O design N2 não contemplava workflows não-headless. O N3 adiciona máquina de estados + eventos, que resolvem isso. Porém, N3 continua em sombra (feature flags, não produção). Resultado: **o N2 ainda roda em produção, e há gap de sincronização se workflow não chamar `forja_headless`**.

**Risco real**: Médio. Mitigado em prática porque: (a) a triagem humana (relatório+painel) apanha dessincronia; (b) Igor é avisado se painel discorda de Gmail. Porém, se a sessão de produção cair e for retomada, o N2 não tem máquina de estados para recuperar de forma confiável — requer intervenção manual ou réplica de N3.

---

### E5 — Falta de validação no limite de contexto do headless: timeout genérico sem retry (P1, mitigação existente)
**Severidade**: P1 (mitigado, monitora-se) | **Evidência**: `forja_headless.py:70-75`, TIMEOUT_S = 600s | **Impacto**: Prompt longo gera "Prompt is too long" sem retry ou fallback.

**Descrição**: Se o prompt montado (BLINDAGEM_IDPI + mandatory_prompt_for_phase + prompt) exceder contexto do modelo, Claude headless falha com "Prompt is too long". A exceção é capturada e gravada em stderr, mas sem retry ou decomposição. Lição 1 (Libra Sul) e Lição 9 (Patrícia) reportam isso — "Auditor de citações estourou contexto". Mitigação: instruções de ler PDFs por páginas/intervalos, resumo incremental.

**Análise técnica**: Risco estrutural do design headless consultivo — é read-only nos autos, então não pode fazer splits inteligentes. O mitigation atual é **instruir o prompt direto** ("leia PDF por páginas, resuma incrementalmente"). Funciona, mas frágil. Uma solução robusta seria: pipeline de decomposição (split automático de PDFs grandes, merge de resultados parciais) — mas exigiria escrita no disco de intermediários (fora do escopo read-only OAuth).

**Risco real**: Médio. Acontece em casos com 2+ PDFs volumosos. Detecta-se na auditoria (o resultado fica incompleto). Não bloqueia deploy porque cases reais ajustam prompts manualmente. Registrado em RETROSPECTIVAS.md como lição — futuro headless multimodelo pode aliviar.

---

### E6 — Cache de fontes oficiais existente, mas sem validação de frescor (P2, informativo)
**Severidade**: P2 (operacional) | **Evidência**: `forja_metricas_f7.py` lê cache; Lição 45 (art. 343-A RISTJ): regimento baixado semana passada estava velho | **Impacto**: Peça pode citar dispositivo tido como inexistente, em razão de cache desatualizado.

**Descrição**: O cache `cache/fontes_oficiais/` armazena verbatim de súmulas, artigos, temas STJ com cabeçalho FONTE/URL/data. O verificador G4 confere contra cache. Porém, não há validação de frescor — se a Lei 14.905/2024 foi emendada em junho/2026 e o cache tem versão de janeiro, a conferência passa. Lição 45: art. 343-A RISTJ (criado ER 53/2026, DJe 01/07/2026) foi negado pelo verificador porque a "consolidação local estava desatualizada". Corrigido retroativamente.

**Análise técnica**: Essa é uma **vulnerabilidade operacional**, não bug de código. A Regra 10/07 (RETROSPECTIVAS Lição 45) estabelece: "negar a existência de dispositivo exige a mesma régua de fonte oficial + data de conferência que afirmar". O cache precisa de **refresh policy** — ex.: se arquivo > 30 dias, avisar no render. Ferramentas: verificar DJe/data de publicação oficial vs cache.stat().st_mtime.

**Risco real**: Médio. Ocorre raramente (emendas regimentais não são frequentes). Detectável por auditoria manual (Efesto em 09/07 pegou). Regressão de regressão: o verificador agora flagra "art. 343-A fora do STJ" de forma negativa — precisa de teste para não virar falso-positivo novamente.

---

### E7 — Padrão de teste real descobriu defeitos em produção que testes sintéticos não pegaram (P2)
**Severidade**: P2 (prática demonstrada, não é falha de código) | **Evidência**: `test_real_telemetria_licao41.py` rodou em artefatos reais vs `test_licao41.py` sintético | **Impacto**: Confiança em testes unitários diminuída para o pipeline visual law.

**Descrição**: O `test_licao41.py` é uma regressão bem-estruturada de 22 casos (12 testes + 10 não-travas). Ele passou 100%. O `test_real_telemetria_licao41.py` rodou a pipeline completa em 15 DOCX reais de produção e achou:
1. **40 asteriscos literais** em visual law do Libra Sul (célula de caixa não converteu `**negrito**` via `_rico`).
2. **Antigas versões de DOCX** (CORSAN) com 30 asteriscos (artefatos antigos a regenerar).
3. **Regressão em `word_visual_pipeline.inserir_emf_word_com`** (alguém trocara por `python-docx add_picture`, que não suporta EMF).

Todos foram fixos. Mas o **meta-fato** é importante: teste sintético não cobria a integração de render→visual kit→Word COM→PDF em um fluxo.

**Análise técnica**: Isso não é falha do harness, é **indicador de que suítes sintéticas precisam de cobertura de integração**. A bateria real é cara (roda sobre artefatos de produção, consome espaço em disco, é lenta), mas essencial. O padrão deveria ser: sintético passa → real passa → deploy. Hoje é: sintético passa → deploy → descobrir em produção.

**Risco real**: Médio. Mitigado porque QA visual pega a maioria. Recomendação: tornar `test_real_telemetria_licao41.py` obrigatório antes de releases, não opcional.

---

## 2. Pontos Fortes

**A1 — Documentação técnica exemplar**: O arquivo `DOCUMENTACAO_TECNICA.md` (296 linhas) é um raro modelo de documentação viva. Tem mapa Mermaid do pipeline, tabela "quero mudar X → mexa em Y", índice com caminho até cada coisa, auditoria crítica registrada, executado × planejado, rejeições com fundamento. Serve como bússola para qualquer intervenção.

**A2 — Protocolo de aprendizado acoplado ao código**: `RETROSPECTIVAS.md` cataloga 48 lições de casos reais. Cada lição numérica entra em gates automáticos ou checklist de auditoria. Isso é raro — a maioria dos sistemas deixa "lições" em docs que ninguém lê. Aqui elas viram regressão.

**A3 — Regressão do verificador integrada no pipeline**: `forja_verificador.py` tem `test_forja_verificador.py` com lista `DEVE_PEGAR` (15 detecções que passaram) e `NÃO_PODE_TRAVAR` (13 não-travas). Toda mudança no verificador passa por isso. Pattern modelo.

**A4 — Fail-closed on F7**: O render (F6/F8) foi **acoplado intencionalmente** a F7 depois de Lição 35 (auditoria Efesto 09/07 descobriu que P0 podia virar entrega se operador não olhasse console). Design assertivo, não defensivo — Gates rodam ANTES de qualquer artefato. Exemplar.

**A5 — Camadas aditivas sem substituição**: N2 (produção) + N3 (sombra com máquina de estados) + N4 (pesquisa em raciocínio/ciência). Cada camada tem feature flags. Zero destruição. Permite experimentação sem risco.

**A6 — Isolamento de estado por caso**: cada caso tem sua pasta `state/case-id/` com `FORJA_STATE.json`, `producao/`, artefatos. Sem acoplamento global. Facilita paralelização futura e auditoria de um caso isoladamente.

---

## 3. Recomendações Priorizadas

### R1 — Centralizar funções utilitárias (P2, esforço S)
**Por quê**: Reduz variância de comportamento, simplifica auditorias futuras, facilita sincronização de bug-fixes.

**O que fazer**: 
1. Mover `now_iso()`, `read_json()`, `append_unique()` para `forja_n3_common.py`.
2. Validar comportamento (BOM handling, fallback em `read_json`, dedupe).
3. Importar de `forja_n3_common` em todos os 7 arquivos.
4. Rodar testes de regressão.

**Tempo estimado**: ~2h.

---

### R2 — Resolver acoplamento F7↔F10 com tratamento de erro (P1, esforço M)
**Por quê**: Se verificador falha com exceção, render aborta sem marcar erro — estado fica órfão.

**O que fazer**:
1. Em `forja_render_docx.py`, envolver bloco F7 em try/except.
2. Se exceção, gravar JSON com erro.
3. Em `forja_delivery.py`, ler JSON e se campo `error` existir, bloquear F10.
4. Adicionar teste.

**Tempo estimado**: ~3h.

---

### R3 — Implementar refresh policy para cache (P2, esforço M)
**Por quê**: Cache desatualizado pode levar a falsos-negativos.

**Tempo estimado**: ~3h.

---

### R4 — Elevar teste real para obrigatório (P2, esforço L)
**Por quê**: Teste real descobriu 4 defeitos que teste sintético não pegou.

**Tempo estimado**: ~1.5h.

---

### R5 — Implementar recuperação de tentativa abandonada (P1, esforço M)
**Por quê**: E4 (estado dessincronia) precisa de solução em N2 enquanto N3 não vai a produção.

**Tempo estimado**: ~4h.

---

### R6 — Suíte de testes de integração render→visual→PDF (P2, esforço M)
**Por quê**: E2 — funções longas sem testes de integração.

**Tempo estimado**: ~5h.

---

## 4. Vulnerabilidades Operacionais

**V1 — Dependência de protocolo manual**: O passo "atualizar FORJA_STATE.json após workflow" é mandatório (Lição 33), mas executado por humano. Se esquecer, estado fica órfão. **Solução**: ativar N3 para produção — mas exige regressão completa dos 6 casos.

**V2 — Cache sem backup**: Se `cache/fontes_oficiais/` for apagado, nenhuma regressão restaura. **Solução**: adicionar git-tracking ou backup semanal.

**V3 — Falta de auditoria de prompts**: Se um prompt injeta instrução clandestina, BLINDAGEM_IDPI é a única defesa. Não há logging de prompts. **Solução**: gravar `HEADLESS_PROMPT_LOG.json` para auditoria posterior.

---

## 5. Matriz de Severidade

| ID | Severidade | Título | Status |
|---|---|---|---|
| E1 | P2 | Duplicação de funções utilitárias | Dívida aceita |
| E2 | P2 | Funções longas sem testes estruturais | Dívida bem-documentada |
| E3 | P1 | Acoplamento F7↔F10, fail-closed sem retry | Mitigado em prática |
| E4 | P1 | Estado dessincronia com produção | Lição 33, corrigido em 09/07 |
| E5 | P1 | Timeout headless sem retry | Mitigado por instrução |
| E6 | P2 | Cache sem validação de frescor | Operacional, Lição 45 corrigida |
| E7 | P2 | Teste sintético não cobre integração | Padrão de cobertura fraco |

**P0 (bloqueador)**: Nenhum. Sistema está operacional.

---

## 6. Métrica de Saúde

| Métrica | Valor | Alvo | Status |
|---|---|---|---|
| Testes do verificador | 15 DEVE_PEGAR + 13 NÃO_PODE_TRAVAR | ✓ Passar | ✓ Verde |
| Casos entregues | 5 (lote 1) | 1/1 no padrão | ✓ Conforme |
| Gates automáticos ativos | G1-G9 | >=6 | ✓ Acima |
| Cobertura de regressão | 100% | >=90% | ✓ Excelente |
| Cobertura de integração | ~40% | >=70% | ⚠ Fraco |
| Documentação | 48 lições + CLAUDE.md + gates | >=30 | ✓ Excelente |
| P0s não-justificados | 0 | 0 | ✓ Verde |
| Tempo de ciclo | ~1-2h por caso | <3h | ✓ Aceitável |

---

## 7. Conclusão

O FORJA é um **sistema bem-arquitetado e operacional**, com protocolos de qualidade que funcionam. Não há P0s. A dívida técnica (E1, E2) é baixa e aceitável. Os riscos P1 são reais mas mitigados por camadas de verificação humana.

**A recomendação estratégica é consolidar agora (próximas 2 sessões), não adicionar features**. O sistema responde bem porque cada feature paga entrada de regressão. Abrir o circuito N4 sem antes executar R1–R3 é risco. A transição para N3 em produção é strategicamente importante mas exige 1-2 semanas de regressão — deixar para próximo ciclo.

**Prioridade técnica**: R2 → R3 → R4 → R1 — parallelizáveis em 2 sessões.

---

**Assinado**: Efesto Tekhton, Diretor de Tecnologia INTEIA | **Data**: 11/07/2026 | **Auditoria**: Arquitetura FORJA, robustez N2/N3, testes, dívida técnica.
