# Parecer do Conselho Quadripartite: Gate Visual F8-S da FORJA

> ## ✔ DECISÃO DO IGOR — 03/08/2026, posterior a este parecer e à nota abaixo
>
> **O Igor decidiu, e a decisão prevalece sobre o cronograma deste parecer.** Ele
> acatou a recomendação apresentada: **ligar depois do prazo de 05/08, não antes,
> e em duas etapas** —
>
> 1. **primeiro fechar a rota simples**, que é o que de fato produz peça pobre
>    (corresponde ao Passo 2 abaixo);
> 2. **só depois tornar o F8-S bloqueante** (Passo 5), com a etapa 1 já estável.
>
> **Motivo do adiamento, nas palavras dele:** o risco concreto é uma peça com
> prazo travar num falso positivo do gate e alguém ter que destravar sob pressão.
> Ele ofereceu ligar imediatamente se fosse a recomendação; a recomendação foi
> esperar, e ele a acatou.
>
> Isso **confirma o sequenciamento** dos Passos 2 e 5 e **descarta a data única
> de 06/08** da seção 1: as duas etapas são separadas no tempo, e a segunda não
> tem data fixa — depende da primeira estar estável. As cinco condições de
> ativação continuam valendo, com a correção técnica da condição nº 1 feita na
> nota abaixo (a entrada é `forja_visual_build.build()`, não integração dentro do
> render).
>
> **A ordem permanente de 30/07 não depende disto:** peça sem elementos visuais
> completos não sai, bloqueie o gate ou não.
>
> Rastreio das tarefas: #7 (etapa 1) e #9 (etapa 2, bloqueada por #7).

> ## ⚠ NOTA DE SUPERAÇÃO PARCIAL — 03/08/2026, mesma data, posterior a este parecer
>
> Este parecer foi emitido ANTES da revisão cruzada com a família Codex, e três
> pontos dele não se sustentam:
>
> **1. A condição de ativação nº 1 está tecnicamente errada.** Ela manda
> `forja_render_docx.py` importar `forja_visual_build.build_visual()`. A função
> se chama `build()`, e — mais importante — integrar a composição dentro do
> render é a arquitetura **analisada e rejeitada** na Onda 2: construiria a peça
> duas vezes, uma pobre e uma rica, deixando dois DOCX parecidos na mesma pasta.
> É o modo de falha do caso Patrícia (Lição 48). A arquitetura correta é a
> entrada única `forja_visual_build.build()`, com o render rebaixado a prévia.
>
> **2. A data de 06/08/2026 não se sustenta.** A revisão cruzada encontrou um
> defeito material no próprio gate: a contagem de caixas casava células do
> quadro zebrado, mascarando a ausência total de destaque (521 caixas fantasmas
> no Aditamento CORSAN). Ligar o bloqueio com esse defeito seria pior que não
> ligar — deixaria passar peça pobre com muitas tabelas e reprovaria peça boa
> sem elas. Corrigido em 03/08, mas o instrumento acumulou três defeitos
> materiais em três dias e não deve barrar peça com prazo processual antes de
> um período sem defeito novo.
>
> **3. A cobertura citada (5%) estava errada** por causa do mesmo defeito. O
> número correto é 9%.
>
> **O que este parecer mantém de válido:** a exigência do brief F7.5 para peça
> longa; o fechamento da rota simples; a conferência humana como condição; e a
> tese de que a fábrica não deve parar durante a integração.
>
> **Lição registrada (93):** o conselho leu o dossiê escrito pelo construtor do
> sistema e não detectou a circularidade que o Diabob apontou — só a leitura
> independente do código a encontrou. Comitê não substitui revisão de código.
> Ver `RETROSPECTIVAS.md`, lições 93 a 95, e a seção de estado no documento 24.

**Data**: 03/08/2026  
**Assunto**: Decisão sobre ligação do bloqueador visual F8-S em produção  
**Secretário**: Efesto (na função)  
**Conselheiros**: Efesto (engenharia), Helena (estratégia), Cícero (jurídico), Diabob (red team)

---

## 1. DECISÃO

**Gate F8-S bloqueante**: SIM. Entra em produção como bloqueador irrevogável em **06/08/2026** (quarta), condicionado às cinco observáveis abaixo. Todas devem ser verdadeiras simultaneamente; falta qualquer uma = adiamento automático.

**Condições de ativação** (objetivas, verificáveis):
1. Onda 2 (geradores de cronologia, tese, matriz em `medina_svg_kit.py`) integrada ao pipeline padrão de produção — `forja_render_docx.py` importa `forja_visual_build.build_visual()` e a chamada é executada após F7 passar (evidência: `grep "build_visual" forja_render_docx.py` retorna match).
2. Integração testada em zero P0 de F7 jurídico sobre cinco peças reais de tipos distintos (peça protocolável, memorial, produto interno), ponta a ponta.
3. Rota simples (`forja_render_docx.render()` sem `compor()`) rebaixada para prévia não liberável — `forja_package.py` rejeita saída em `*_PREVIEW_NAOLIBRAVEL.docx` (não empacotável, não entregável).
4. Igor confere visualmente os cinco PDFs gerados em 06/08 (timbre, síntese, diagrama, caixa, pull quote, paleta Medina, legibilidade ≥8pt impresso) — conferência toma 15–20 minutos — e assina relatório de aprovação explícita por tipo de peça.
5. Brief F7.5 obrigatório para peça > 25 páginas codificado no contrato F7 (`phase_contracts/F7.json`) — redator escreve 1–2 minutos (JSON estruturado: cronologia, cadeia argumentativa, elementos visuais projetados) ou gate VIS-03 bloqueia entrega. Sem brief = não há saída.

**Rota simples fecha** no mesmo dia (06/08/2026): `forja_render_docx.render()` continua existindo para QA interna, mas `forja_delivery.py` e `gestao_escritorio` recusam qualquer DOCX que não seja `*_VISUAL_LAW.docx`.

**Cronograma**: Onda 2 integrada + testada 04–05/08 (~5–7 horas, paralelo com produção normal). Conferência Igor 06/08 (~20 minutos). Gate ativo 06/08 noite. **Fábrica não para durante integração.**

---

## 2. COMO SE CHEGOU AQUI

**Ponto crítico trazido por Efesto**: Integração técnica (acoplamento em `forja_render_docx`, chamada viva no pipeline) é separada de construir Onda 2 (algoritmos de gerador). Ligar gate sem integração em produção = travamento garantido. Essa linha não cede.

**Sequência validada por Cícero**: Capabilidade → enforcement, não enforcement → capabilidade. Figura em peça protocolada é prova; figura fabricada sem ancoragem semântica (Brief F7.5 ausente) cria risco legal maior que figura ausente (Lição 90, dados reais Cafelana V7). Conferência visual humana em amostra real é auditoria obrigatória de responsabilidade profissional, não atalho.

**Helena convergiu** de "ligar AGORA sem integração" para "APÓS integração + conferência Igor", cedendo no timing técnico realista. Mantém inviolável: visual é padrão de saída, não opção; consistência Medina Osório é direito de cliente e ordem do dono do escritório.

**Diabob realista**: Bloqueio entra quando funciona ponta a ponta em produção real, não quando promete. Cedeu em Brief F7.5 ser obrigatório estruturalmente (não refinamento futuro). Convergiu na data fixa 06/08 em vez de observação permanente indefinida.

**Quatro observáveis** garantem pronto: (1) grep em `forja_render_docx.py` confirma acoplamento vivo; (2) zero P0 de F7 sobre 5 casos reais; (3) `forja_package` rejeita PREVIEW no código; (4) Igor assina conferência visual em amostra real. Sem esses, gate não entra.

---

## 3. DIVERGÊNCIAS QUE PERMANECERAM

**Uma divergência nominalmente registrada, não bloqueadora:**

**Diabob** recusa conferência visual manual do Igor como gate de entrada. Posição: "Validação cruzada automática (forja_verificador rodando sobre os 5 casos) confirma 100% passam. Gate é instrumentação suficiente; reduz dependência humana e mantém fábrica não travada."

**Posição majoritária** (Efesto, Helena, Cícero): Conferência visual do Igor em amostra real (5 peças, 15–20 minutos) é obrigatória. Razão: responsabilidade jurídica, Lição 90 (figura fabricada sem lastro é pior que ausente), inviolabilidade da ordem do dono do escritório sobre padrão visual. Efesto: "Igor abre PDF no Adobe, aprova/rejeita por tipo explicitamente". Cícero: "Sem conferência prévia, máquina rejeita, cliente contesta, responsabilidade é nossa".

**Consenso final**: Conferência visual de Igor permanece como **G5 de ativação do gate**. Diabob fica registrado em discordância nominal mas não bloqueia execução. A validação automática (`forja_verificador`) roda em paralelo como instrumento de suporte.

---

## 4. O QUE FOI DERRUBADO

**Teses refutadas (não reabrir):**

| Tese | Refutação | Quem trouxe | Refutador |
|------|-----------|-------------|-----------|
| Ligar gate hoje (30/07) | Onda 2 não integrada; travaria 100% das entregas. Evidência técnica inconteste. | Helena R1 | Efesto+diagnóstico |
| Brief F7.5 é refinamento futuro | Risco jurídico (Lição 90: figura fabricada > figura ausente). Cicero com dados reais Cafelana V7. | Efesto R1 | Cicero+exemplos |
| Observação silenciosa indefinida é segura | Fábrica fica em limbo. "Vamos ver se funciona por dois meses" é enganação. | Cicero R1 original | Efesto+Diabob R2 |
| Fechar rota simples antes de Onda 2 | Travamento. Sem alternativa ativa, paralisa. | Efesto R1 | Todos convergem |
| Visual é opção do agente | Visual é direito de saída, ordem inviolável do dono. Padrão Medina Osório é DNA da fábrica. | Diabob R1 | Helena+Cicero |
| Onda 1+2 rodam em paralelo com bloqueio ligado | Sequência: capabilidade → enforcement. Ligar bloqueio sem capabilidade viva = armadilha. | Helena R1 | Efesto+Cicero |

**Três ideias que caíram na rodada 1 e não reapareceram:**
- Onda 2 leva 25–30 horas (Efesto R1 pessimista) → Corrigido para 5–7 horas (Cicero R2 validou).
- Brief F7.5 obrigatório acima de 12 páginas → Corrigido para 25 páginas (Helena+Cicero convergem).
- Gate automático dispensa auditoria humana → Refutado. Cicero com Lição 90: figura em peça protocolada é prova; figura sem ancoragem semântica é risco legal. Conferência Igor é obrigatória.

---

## 5. PLANO DE EXECUÇÃO

Cinco passos sequenciados, paralelo onde possível. Responsável em parênteses.

### Passo 1: Integração Onda 2 (Efesto, engenharia) — 04–05/08, ~5–7 horas

**1A — Completar geradores de diagrama** (48h antes da integração)
- Arquivo: `_FERRAMENTAS\medina_svg_kit.py`
- Construir três geradores compostos: cronologia de atos, encadeamento de tese, matriz comparativa.
- Aceitar: Composição roda em zero P0 de testes existentes (gates de legibilidade ≥8pt impresso e validação de overflow de viewBox já codificados).
- Critério de pronto: `python -m pytest medina_svg_kit_test.py` passa 100%.

**1B — Acoplamento ao pipeline padrão**
- Arquivo: `_FORJA_HARNESS\forja_render_docx.py`
- Refactor: `from forja_visual_build import build_visual`. Chamada integrada após F7 passar, antes de empacotamento.
- Integração: `render()` invoca `build_visual(md_path, out_dir)` → gera mapa automático se não existir, chama `compor()`, roda `montar()`, retorna destino visual.
- Aceitar: Nenhuma dependência nova; tempo de composição <7 segundos por peça (já medido).
- Critério de pronto: `grep "build_visual" forja_render_docx.py` retorna match; método `render()` testa integração; zero P0 de F7.

**1C — Teste em cinco peças reais**
- Arquivo: `_FORJA_HARNESS\test_onda2_integracao.py`
- Rodar pipeline completo em cinco peças de produção recente (tipos: protocolável, memorial, produto interno).
- Medir tempo de processamento agregado (alvo: <30 minutos para 5).
- Aceitar: Zero erro; tempo de composição não degrada latência de entrega urgente.
- Critério de pronto: Log de processamento mostra `success: True` em 5/5 casos; tempo agregado ≤30min.

### Passo 2: Rebaixamento rota simples (Efesto + Diabob, código) — 05–06/08, ~1 hora

**2 — Rejeição de saída não-visual em produção**
- Arquivo: `_FORJA_HARNESS\forja_package.py`
- Modificação: Validação de entrada rejeitando saída de `forja_render_docx.render()` sem `compor()` como entregável.
- Implementação: `forja_package.validate_input()` verifica assinatura digital em `F8S_ASSINATURA_VISUAL.json`. Sem assinatura = recusa.
- Rota simples marcada: Output em `*_PREVIEW_NAOLIBRAVEL.docx` (para QA interna, não empacotável).
- Aceitar: Refactorização zero-breaking de pipeline existente; QA interna intacta.
- Critério de pronto: `forja_package.test_rejects_preview_nonlibravel()` passa; `forja_delivery.py` retorna erro explicito ("Assinatura visual obrigatória") ao tentar empacotar PREVIEW.

### Passo 3: Conferência visual Igor (Igor, decisão executiva) — 06/08, ~20 minutos

**3 — Inspeção visual de cinco PDFs em amostra real**
- Arquivo (entrada): Cinco PDFs gerados por Passo 1B integrado.
- Checklist por tipo de peça:

| Elemento | Crítico | Paleta | Legibilidade |
|----------|---------|--------|--------------|
| Timbre (cabeçalho 1ª pág) | SIM | N/A | Visual |
| Síntese executiva | SIM | Fundo terracota (#D9926A) | ≥8pt |
| Diagrama (cronologia/tese) | SIM | Traços petróleo (#395C60) | ≥8pt |
| Caixa de síntese | Condicional (peça longa) | Fundo cinza leve | ≥7pt |
| Pull quote (fragmento literário) | Condicional | Tipografia itálica | ≥9pt |
| Negrito institucional | Condicional | N/A | Visual |
| Rodapé institucional | SIM | Tipografia Times New Roman | ≥8pt |
| Sem placeholder [VERIFICAR] | SIM | N/A | Grep literal |

- Decisão: Aprovação (S) / Rejeição (N) por tipo de peça em relatório estruturado.
- Arquivo (saída): `_FORJA_HARNESS\state\CONFERENCIA_VISUAL_IGOR_2026-08-06.md` com assinatura digital Ed25519.
- Critério de pronto: Relatório assinado com 5/5 aprovações OU reprovações com plano de remissão (rework Onda 2 ou Brief F7.5 adicional). Se aprovado: prosseguir Passo 4. Se reprovado (>50%): escalar a Efesto + Cicero, gate não entra em produção.

### Passo 4: Formalização contratual Brief F7.5 (Cicero, jurídico) — concomitante 04–06/08

**4 — Atualização do contrato de fase F7**
- Arquivo: `_FORJA_HARNESS\phase_contracts\F7.json`
- Campo novo: `"visual_brief_f75_declarado"` com obrigatoriedade condicional: `"obrigatorio_se": {"paginas": {">": 25}}`.
- Schema: `{cronologia_declarada: string, cadeia_argumentativa_declarada: string, elementos_visuais_projetados: [enum]}`
- Assinatura: Contrato F7 assinado digitalmente (Ed25519); `forja_run.py` valida assinatura antes de F8 rodar.
- Aceitar: Sem brief válido para peça >25pp, F8 bloqueado em gate VIS-03 (diagnóstico explícito: "Brief F7.5 obrigatório para peça > 25 páginas").
- Critério de pronto: `forja_run.py --validate phase_contracts/F7.json` retorna `signature_valid: True`; teste de rejeição passa (peça >25pp sem brief → VIS-03 bloqueia).

### Passo 5: Ligação do bloqueador F8-S (Efesto, código) — 06/08 noite, ~30 minutos

**5 — Ativação do gate em modo irrevogável**
- Arquivo: `_FORJA_HARNESS\forja_verificador.py`
- Modificação: Seção `F8-S` (hoje em `if DEBUG_MODE_OBSERVACAO:`) ativada em modo production check. Gate retorna bloqueador P0 em peça sem assinatura visual válida.
- Diagnósticos: VIS-03 (brief ausente), VIS-04 (elemento gráfico ausente), VIS-05 (legibilidade abaixo de 8pt), VIS-06 (overflow de viewBox).
- Critério de pronto: Passo 3 (conferência Igor) passou com aprovação em 5/5. Zero waiver pós-06/08. Qualquer peça que chegue a F8 sem assinatura visual válida é rejeitada em estado P0_BLOCKED automaticamente.

**Precedência de validação**: Passos 1, 2, 3, 4 devem estar VERDES antes do Passo 5 rodar. Se qualquer um falha, Passo 5 é adiado indefinidamente até reparação.

---

## 6. O QUE O IGOR PRECISA FAZER

**Uma única ação**: Em 06/08/2026 (à tarde, após Passo 1 integrado), abrir cinco PDFs gerados pela Onda 2 integrada no Adobe Reader ou Word, conferir o checklist visual de timbre / síntese / diagrama / caixa / pull quote / paleta / legibilidade (15–20 minutos totais), e assinar o relatório de aprovação (SIM/NÃO por tipo de peça) em `_FORJA_HARNESS\state\CONFERENCIA_VISUAL_IGOR_2026-08-06.md` com chave Ed25519.

Sem essa conferência assinada, gate não entra em produção. Com aprovação explícita, Passo 5 roda automaticamente à noite.

---

**Registrado e consolidado pelo Conselho em 03/08/2026.**


## Decisão do Igor em 04/08/2026 — a etapa 1 sai do plano

O plano acima previa duas etapas: primeiro fechar a rota simples (fazer `forja_render_docx` produzir prévia não liberável) e só depois tornar o gate F8-S bloqueante. **O Igor descartou a etapa 1: o render não faz sentido como rota e não será tratado.**

Consequência: o gate F8-S deixa de depender dela. A única condição que resta para ligá-lo é o prazo de 05/08. A ordem permanente de 30/07 — peça sem elementos visuais completos não sai — continua valendo independentemente do modo do gate, como sempre valeu.

Não reabrir a etapa 1 sem fato novo.
