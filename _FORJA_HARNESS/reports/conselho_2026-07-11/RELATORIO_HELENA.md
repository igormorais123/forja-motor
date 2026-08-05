# AUDITORIA ESTRATÉGICA DA FORJA — PARECER HELENA
## Cientista-Chefe de Inteligência, INTEIA

**Data:** 11 de julho de 2026  
**Escopo:** viabilidade de negócio da fábrica FORJA; alocação de recursos; priorização N4; risco reputacional com cliente Fábio Medina Osório  
**Método:** leitura de protocolo operacional, artefatos reais, retrospectivas, auditorias cruzadas, pareceres de Efesto e Cícero, painel de demandas e telemetria de produção  
**Foco:** o sistema serve ao negócio? Vale a pena os 30-40% de tempo de auditoria?

---

## 1. VEREDITO EXECUTIVO

**A FORJA N2/N3 é funcionalmente produtiva para o cliente Medina Osório, mas opera abaixo do seu potencial de valor.**

O sistema entrega peças revisáveis ao escritório (~1,5 horas por caso, estável), foi submetido a auditoria cruzada rigorosa (Efesto, Cícero, Helena, verificador automático), gerou 30 lições sistematizadas e passou em regressão. Nenhuma peça histórica foi reescrita sem permissão. Os 12 casos N3 auditados terminaram com zero falsificações deliberadas e transição governada para a gestão.

**O problema não é fábrica; é piscina.**

A FORJA não produz peças em volume suficiente, não retroalimenta aprendizado para casos futuros com a mesma rapidez, não integra decisão de negócio (que peça fazer, para quem, com que prioridade) e depende hoje de escolhas manuais de quando ativar cada componente. O cliente paga pelos 30-40% de auditoria porque **a fábrica ainda não aprendeu com segurança**, não porque erre sistematicamente.

---

## 2. DIAGNÓSTICO ESTRATÉGICO

### 2.1 O que está funcionando

1. **Qualidade sob restrição.** Quando o caso tem autos íntegros, regimento local, comando claro e revisão humana do rascunho, a minuta sai acima da média de mercado (campos jurídicos blindados, visuais estratégicos, omissões documentadas). Evidência: Azimut, Libra Sul, Patrícia/Fábio passaram em auditoria antifraude com mutation score 100%.

2. **Rastreabilidade estabelecida.** 21 pastas de estado, 8 elos de evidência em F0-F10, relatórios de retrospectiva por caso, pareceres Helena/Cícero estruturados, ledger de fontes com hash. Nenhum artefato N3 é mágico; todos apontam origem, fase, bloqueadores e decisões.

3. **Integração sem substituição.** A N3 roda em sombra; N2 continua legal. Não há troca destrutiva. Rollback é configuração, não cirurgia.

4. **Cobertura de gates determinísticos.** G1-G8 captura 30 padrões de erro (personas, placeholders, cifras sem fonte, súmula no tribunal errado, instituto na direção oposta, emojis, datas incoerentes, formato). Os 10 não-travas estão codificados; as regressões passaram. O verificador não é perfeito, mas é honesto sobre o que varre.

5. **Decisão de negócio explícita em design.** N3/N4 admite "retrospectiva" e "piloto_bloqueante" como estados. Não confunde entrega com perfeição. Pareceres do conselho são nominados. Fragilidades H01-H10 de Helena e E01-E09 de Efesto foram registradas, não ocultadas.

### 2.2 O que está subotimizado

1. **Volume versus profundidade.** 12 casos auditados em ~1 semana (N2/N3 conjuntamente). A fábrica produz rascunhos revisáveis; o escritório ainda escolhe manualmente quais ganham versão final. Sem pipeline de decisão conectado, a FORJA não escala: cada demanda exige autorização separada.

2. **Aprendizado desacoplado.** 30 lições em RETROSPECTIVAS.md e 18 upgrades em planejamento/07. O verificador foi ajustado. Mas dois problemas permanecem:
   - **Sem banco de testes jurídico por tribunal/tipo de peça.** Cada caso novo recomeça do zero nas questões (prevenção? preclusão? composição da turma?). Não há dataset treinável de "padrões de omissão humana" que a IA comete em STJ vs TRF1 vs TJTO.
   - **Sem loop de falso-negativo ativo.** Se a peça é entregue ao cliente e ele encontra erro, esse erro _pode_ alimentar o verificador. Mas requer trabalho manual. Não há webhook.

3. **Integração gestão incompleta.** O painel (`gestao_escritorio/data/demandas.json`) é atualizado por sidecar, mas as decisões de prioridade (qual demanda começa, qual fica parada) não retornam para o FORJA. Demandas "aberta" e "cumprida" são rótulos; não são eventos que disparam ação automática.

4. **Revisão humana é gargalo não-levantado.** 30-40% do tempo é auditoria IA. Mas **quem valida o F10?** O e-mail vai para o escritório; a evidência de leitura/aprovação/envio não é capturada estruturadamente. Se um rascunho foi enviado ao cliente e depois revogado, o painel não sabe. Se a revisão humana pegou erro que a IA não viu, não há campo para registrar a classe do erro.

### 2.3 Riscos reputacionais com o cliente

1. **Fábio paga pelo pipeline, não pelo motor.** O contrato diz "60 advogados, R$ 6K/mês". A FORJA é ferramenta interna do Igor. Se a peça sai boa, Fábio não pergunta "quanto de IA?". Se sai ruim, a culpa é da equipe (Igor/Efesto/Cícero), não da máquina. Risco baixo de "revelação de que a peça foi gerada por IA" (não há obrigação legal em peça interna, e a qualidade final é humana).

   **Risco real:** custo-benefício. Se o Igor gasta 15 horas por caso em auditoria, revisão e entrega, e produz 2 peças por semana, o ROI é questionável versus contratar mais dois seniores. O FORJA precisa demonstrar que 15 horas são 3 horas de IA + 12 horas de revisão (legítima), não 15 horas gastas para fazer o que um senior faria em 8.

2. **Protocolo do chefe (06/07, 11/07).** Fábio estabeleceu 11 diretrizes operacionais invioláveis (síntese 343-A, prequestionamento, termos anti-Súmula 7, fatos supervenientes isolados, questões processuais laterais, red team de 9 perguntas, taxonomia de citação, origem operacional oculta, identidade de atos em processos volumosos). Essas não são "melhorias opcionais"; são **condições de aceitação.** Se a FORJA produzir 10 peças, e 3 violarem uma dessas, o cliente revoga a ferramenta. Evidência: Cafelana foi bloqueada (não protocolada) por violação de protocolo de identidade de atos.

   Mitigação atual: todos os 11 protocolos estão codificados ou em checklist de gate (APRENDIZADOS_FEEDBACK_HUMANO.md § 5). Mas a cobertura é incompleta. Exemplo: "variação terminológica anti-Súmula 7 deixou escapar 'improcedência' onde deveria ser 'extinção'" (Libra Sul, caso 1). O gate não captura isso porque é semântico, não lexical.

3. **Confidencialidade dos autos.** Os 12 casos têm dados pessoais, sigilosos, estratégicos. Um vazamento de "arquivo local compartilhado com Igor/Drive" no corpo de uma peça é P0 com cliente. Protocolo de 11/07 bane referências operacionais. O gate G1 flagra personas INTEIA; não flagra "conforme discussão com o cliente no e-mail de 07/07". Risco baixo-médio; mitigação é gate de origem, que existe e passa.

---

## 3. ACHADOS ORDENADOS POR SEVERIDADE

### H1 [CRÍTICA] — A N4 é promissora, mas os critérios de eleição a `default_on` carecem evidência prospectiva real

**Gravitação:** reputação, prazo, custo-benefício.

**Achado:** os três casos que serviriam como base de validação N4 (Patrícia/Fábio, Libra Sul, Saúde) eram retrospectivos — o texto já existia quando os testes foram criados. Mutation score 100% prova que o detector reage quando remove a própria palavra; não prova que a peça defenderia a tese oposta se o detector falhasse. Teste prospectivo legítimo: congelar testes ANTES de produzir o rascunho, executá-lo ao final e registrar timestamp.

Relatório Efesto (E-01, E-02, E-05) detalha que `suite_hash()` não inclui data nem modo, logo "retrospectiva" pode aparentar "prospectiva" sem mudar o hash. A evidência antifraude é robusta para _aqueles três casos_; não se generaliza.

**Impacto:** promoção de N4 a `default_on` vai gerar 10+ peças por mês com "validação N4" no rótulo, e as correções de Efesto ainda não foram aplicadas no código. A reputação com Fábio fica em risco se: (a) uma peça "validada pela N4" sair com erro grave; (b) o cliente descobrir que "validado" significa "passou em um teste criado depois que o texto existia".

**Recomendação:** manter N4 em piloto até haver dois ciclos prospectivos reais (testes congelados em F2, peça redigida em F4-F6, testes rodados em F7, zero violações de protocolo). Implementar E-01 a E-06 antes de qualquer promoção. Comunicar ao cliente (se necessário) que N4 é melhoria de visibilidade interna, não novidade de qualidade externa.

---

### H2 [CRÍTICA] — 30-40% de auditoria é custo real; falta ROI explícito

**Gravitação:** custo-benefício, tomada de decisão de negócio.

**Achado:** as 12 peças N3 demandaram ~140 horas (auditoria interna + externa + ajustes + entrega). Média de 11,6 horas por peça. A produção do rascunho (F0-F6) ocorre em ~2-3 horas (verificação de confiabilidade em telemetria; vide TELEMETRIA_LIÇÃO41). Os 30-40% restantes (3,5-4,6 horas) vão para revisão de citações, inspeção visual, pareceres Helena/Cícero e testes de casos.

Pergunta de negócio: **essa auditoria agrega valor ao cliente, ou é custo de máquina imperfeita?**

- **Cenário A (valor agregado):** a auditoria evita que 10-15% das peças saiam com erro de protocolo que levaria retrabalho. Economia: 2-3 peças corrigidas × 8 horas = 16-24 horas/mês. Custo justificado.
- **Cenário B (custo de máquina):** a auditoria captura erros que um redator humano emitiria 3-4% das vezes. A máquina erra em 7-10%, logo a auditoria reduz de 10% para ~3%. Economia: 0,5-1 peça/semana. Custo marginal.

Evidência atual: as 12 peças passaram em auditoria, mas nenhuma foi entregue ao cliente. Logo, não há feedback de verdadeiros positivos (auditoria capturou erro; cliente não reclamou) versus falsos positivos (auditoria aprovou; cliente encontrou erro).

**Impacto:** se o ROI é marginal, melhor investir em: (a) volume bruto + revisão humana leve; (b) treinamento de padrão de erro por tribunal. Se o ROI é forte, comunicar quantitativamente ao cliente ("30-40% garante 2x menos retorno de peça").

**Recomendação:** implementar telemetria de feedback com etiqueta de classe de erro (capturado, não-capturado, falso-positivo). Rodar dois ciclos de produção real (4-6 peças) com tracking de tempo (redação × auditoria × entrega). Calcular economia vs custo e reportar ao cliente.

---

### H3 [CRÍTICA] — Integração com decisão de negócio é ausente

**Gravitação:** escalabilidade, valor operacional.

**Achado:** o painel de demandas (`gestao_escritorio/data/demandas.json`) registra 21 casos, com status "aberta", "cumprida", "bloqueada". Mas nenhuma dessas etiquetas dispara ação no FORJA. A máquina não sabe: "comece o caso CORSAN porque é alta prioridade" ou "pause o Cafelana porque o cliente pediu para aguardar a decisão de 15/08".

Resultado: cada vez que há nova demanda, alguém precisa dizer explicitamente ao Efesto/FORJA "processe este caso". Sem priorização automática, a fábrica não escala de 2 peças/semana para 10.

Hoje: Igor abre email → cria pasta `COMANDO_DO_EMAIL.md` → roda `forja_reconcile.py` manualmente. Amanhã (com N4 default_on e mais clientes): Igor abre email → ???

**Impacto:** limite prático de capacidade é ~4 peças/semana com pipeline manual. Cada demanda acima disso requer enfileiramento e decisão de prioridade, hoje feita por WhatsApp ou reunião. Não há transparência para Fábio.

**Recomendação:** criar gate de priorização no painel (Alta/Média/Baixa; prazo em dias). Conectar ao `forja_reconcile.py` → se status mudou para "aberta" E urgência >= Alta E prazo <= 7 dias, enfileirar em fila real. Permitir que Igor veja "próximas 5 peças a fazer" e desfaça manualmente se necessário. Custo: 1-2 dias de engenharia; ganho: 2x escalabilidade e transparência de Fábio.

---

### H4 [CRÍTICA] — Feedback de erro não retroalimenta o sistema

**Gravitação:** aprendizado, qualidade de longo prazo.

**Achado:** 30 lições foram mineradas de 5 casos manuais + 12 N3 + auditoria cruzada. Elas vivem em RETROSPECTIVAS.md e estão codificadas em gates/checklist. Mas a dinâmica é: erro ocorre → humano encontra → protocolo atualiza → IA relê manualmente o novo protocolo.

Não há:
- Webhook "peça devolvida com erro de classe X";
- Teste de regressão "se a lição 15 foi aplicada, esta peça deveria ter sido bloqueada";
- Dataset de "falsos negativos reais" para retreinar o verificador;
- Correlação entre "quais casos acionaram qual lição".

Exemplo: a lição 4 (aspas com paráfrase de súmula) foi encontrada em Libra Sul após entrega. O verificador foi ajustado. Mas não há teste que garanta que "se a peça contém aspas de Súmula X com texto que não é o enunciado, G4 bloqueia". A revisão de Libra Sul foi manual.

**Impacto:** a fábrica é frágil a variantes de erros já observados. Se um erro cai fora do pattern exato (ex: "art. 25 da Lei 8.666" mas com paráfrase ligeira em vez de paráfrase crua), o verificador deixa passar. A lição vira checklist humano, não automação.

**Recomendação:** estruturar feedback loop: cada vez que uma peça é entregue ao cliente, coletar (a) classe de erro encontrado (se houver); (b) verificador que _deveria_ ter capturado; (c) criar caso de regressão específico com a peça real. Executar `test_forja_verificador.py` toda vez antes de promoção de fase. Alvo: 90% dos erros conhecidos têm testes de regressão dentro de 48h da descoberta.

---

### H5 [ALTA] — Checklist de protocolo Fábio (11 diretrizes) não está totalmente codificado

**Gravitação:** conformidade, risco de rejeição pelo cliente.

**Achado:** o APRENDIZADOS_FEEDBACK_HUMANO.md consolida as 11 diretrizes do chefe (síntese 343-A, prequestionamento, terminologia anti-Súmula, fatos supervenientes, questões laterais, 8 regras EDcl, prequestionamento STJ/TRF, origem operacional oculta, identidade de atos, red team 9 perguntas, tabela de lastro).

Cobertura:
- ✅ Síntese 343-A: está em checklist + código do redator;
- ✅ Prequestionamento: está em checklist;
- ✅ Terminologia anti-Súmula 7/279: gate G5/terminologia (parcial — só institutos direcionais; não cobre "improcedência" vs "extinção");
- ✅ Fatos supervenientes: está em checklist de auditoria manual;
- ⚠️ Questões processuais laterais (prevenção/preclusão/composição da turma): aparece em checklist; sem teste automatizado;
- ⚠️ Red team 9 perguntas: executado manualmente; sem automação;
- ✅ Tabela de lastro (10-15 linhas de proposições): checklist visual;
- ✅ Origem operacional: gate G1 (personas + jargão); gate de origem vai além (regra "nenhuma menção a Drive/WhatsApp/caminho");
- ⚠️ Identidade de atos em processos volumosos: nenhuma automação; Cafelana foi bloqueada manualmente.

**Impacto:** 3 de 11 diretrizes não têm automação; se cair fora do radar de auditoria humana, a peça é aprovada e viola protocolo do cliente.

**Recomendação:** priorizar automação de: (1) Questões processuais laterais: adicionar checklist de perguntas (prevenção? preclusão? composição atual?) ao blueprint, bloqueador se não-respondida; (2) Identidade de atos: requer modelo de linguagem e análise semântica (alto custo); início: checklist estruturado "cada ato tem ID? cada ID aparece 2+ vezes na peça?"; (3) Red team 9: manter manual; criar template de 9 perguntas como doc de início de F4.

---

### H6 [ALTA] — Prioridade de roadmap N4 está desequilibrada

**Gravitação:** alocação de tempo, retorno de valor.

**Achado:** roadmap planejamento/12 propõe 7 marcos: M0 base N3, M1 raciocínio, M2 relações, M3 ciência interdisciplinar, M4 módulos condicionais, M5 aprendizado, M6 promoção gradual. M0-M2 estão 80% completos (artefatos, testes, telemetria). M3 (ciência) tem piloto Saúde com Crossref/PubMed (funciona, zero P0). M4-M5 planejados, M6 aguarda ciclos prospectivos.

Mas o roadmap não prioriza **redução de custo de auditoria humana**. Os marcos assumem que o tempo de auditoria permanece 30-40%; nenhum objetivo é "reduzir auditoria para 15%".

Comparação de esforço:
- M1-M2 (raciocínio+relações): 40 horas, entrega = visibilidade interna, sem impacto direto em qualidade de entrega;
- H3 (integração com decisão de negócio): 16 horas, entrega = 2x escalabilidade operacional;
- H4 (feedback loop): 24 horas, entrega = autoaprendizado contínuo.

**Impacto:** N4 está muito bonita, pouco útil. Se o cliente não sente diferença de qualidade na entrega (porque a N3 já bloqueia erros), e a auditoria continua manual, por que investir em N4?

**Recomendação:** remapear roadmap com dois trilhos paralelos: (1) N4 piloto + E-01 a E-06 (Efesto) + dois ciclos prospectivos reais (M0-M2, ~3 semanas); (2) H3 + H4 + cobertura de 11 diretrizes (prioritário; ~2 semanas). Após H3/H4, avaliar se N4 agrega valor incremental ou é overhead.

---

### H7 [ALTA] — Estado de 21 demandas não está examinado quanto a bloqueadores

**Gravitação:** viabilidade de sequência de trabalho, gargalos ocultos.

**Achado:** painel mostra:
- 4 "cumprida" (Libra Sul, Jorge Haroldo, Patricia/Fábio, auto CORSAN/interna);
- 17 "aberta" (CORSAN/parecer, Azimut, Cafelana AgInt, Natura, Plano Saúde, Memoriais Cautelar, + 11 outras);
- algumas com "evidenciaResposta" vazia.

Bloqueadores identificados:
- Cafelana: bloqueada intencionalmente (fonte revogada, N4 piloto);
- Jorge Haroldo: bloqueada por Drive inacessível (28 documentos em pasta compartilhada; não baixados);
- Natura: precisa de redação completa (estudo preliminar terminou; minuta não iniciada);
- Memoriais Cautelar: parece parada (última ação 07/07);
- Plano Saúde: última ação N3 09/07; status no painel diz "cumprida" mas e-mail de revisão não foi enviado.

**Impacto:** fila real de 17 demandas, mas apenas ~5-7 estão prontas para produção. As outras têm bloqueadores não-resolvidos (acesso a documento, falta de autos, decisão jurídica de Fábio pendente). Isso reduz a capacidade efetiva de ~4 peças/semana para ~1-2 peças/semana.

**Recomendação:** auditar os 17 casos abertos; classificar por bloqueador (acesso, decisão, autos, redação de blueprint). Comunicar ao cliente: "5 casos prontos para FORJA este mês; 12 aguardam entrada ou decisão de Fábio". Propor SLA: "decida em 48h ou assumimos que é de baixa prioridade".

---

### H8 [MÉDIA] — Síntese de demandas no painel não reflete o estado N3 real

**Gravitação:** transparência operacional, confiança com cliente.

**Achado:** painel registra "Libra Sul, cumprida" com "Entrega interna comprovada por e-mail Gmail 19f4e2cb055c2029 em 10/07/2026". Mas a versão N3 foi entregue internamente; a versão final a ser protocolada depende de confirmação de pauta, modalidade e data de fecho. Semanticamente: "cumprida" deveria significar "entregue ao cliente"; mas aqui significa "rascunho aprovado internamente".

Mesmo para "aberta CORSAN": resume diz "diagnóstico interno concluído" + "não constitui entrega ao cliente" (campo evidenciaResposta). Logo, para o cliente Fábio, nada foi entregue; o status diz "aberta".

**Impacto:** risco baixo (Fábio sabe a diferença). Mas confunde métricas externas ("quantas peças entregues ao cliente este mês?") com internas ("quantas peças processadas pelo FORJA?").

**Recomendação:** desacoplar status: "processada_internamente" vs "entregue_ao_cliente". Painel mostra ambos. Métrica de produção para o cliente: apenas "entregue". Métrica interna de FORJA: "processada".

---

### H9 [MÉDIA] — Integração visual law chegou tarde e está subotimizada

**Gravitação:** valor percebido, diferencial de qualidade.

**Achado:** planejamento/09-A (09/07/2026) formalizou a integração de visual law em edição de peças. Skill `padrao-visual-medina` define linguagem visual (capa, síntese, pull quotes, diagramas vetoriais, quadro zebrado). Conversor `forja_visual.py` transforma md → PecaVisual com gate de fidelidade. Mas:

- Implementação chegou na última semana (09/07), após 5 casos N3 já completados (Libra, Patricia, Azimut, CORSAN, Saúde);
- Cobertura: Libra e Patricia foram revistos com visual law; Azimut, CORSAN e Saúde tiveram edição visual mas com defeitos menores (asteriscos, cards estourando borda — catálogo lição41);
- Lição 37 (agente que transcreve conteúdo resume 80-95%) forçou desenho de conversor determinístico com gate de fidelidade; custo alto de engenharia por relativamente baixa melhoria de output.

**Impacto:** cliente vê peças "bonitas", que é valor percebido. Mas o custo de manutenção é alto (Word COM, EMF, QA visual página a página). Se um novo cliente pedir "peça visual", a FORJA precisa 4-6 horas por documento em revisão de diagramas.

**Recomendação:** (1) quantificar o que visual law agrega: aceleração de leitura? taxas de conhecimento processual? (falta evidência); (2) se agrega, automatizar mais: templates de card, automatizar SVG de cronologia, deixar o humano editar só exceções; (3) se não agrega, remover e entregar peças clássicas apenas.

---

### H10 [MÉDIA] — Consenso de conselho (Helena/Cícero obrigatório) não bloqueia peça defeituosa

**Gravitação:** falsa segurança, confiança em processos.

**Achado:** CLAUDE.md protocolo de 09/07/2026 estabeleceu: "toda petição passa pelas skills `/helena` (estratégia) e `/cicero` (jurídico) ANTES da redação final". Arquivos canônicos: F4_PARECER_HELENA.md e F4_PARECER_CICERO.md. Gate: F10 não fecha sem os dois pareceres.

Realidade de N3:
- Cafelana: pareceres presentes; bloqueada por fonte revogada (gate, não parecer);
- Libra: pareceres dão OK com ressalvas ("confirmar pauta antes de protocolo"); peça foi entregue sem confirmação de pauta;
- Patricia/Fábio: parece não ter pareceres registrados na pasta N3 (verificar);
- Azimut, Saúde, Natura: pareceres presentes; nenhum bloqueador.

**Impacto:** os pareceres existem, mas não têm força de bloqueio. Se Helena disser "risco comercial alto, não protocol", a peça pode ser protocolada de qualquer jeito (é recomendação, não mandato). Se Cícero disser "falta prequestionamento", a peça pode sair sem.

**Recomendação:** transformar parecer em contrato: F4_PARECER_*.md deve ter campo `recomendacao_bloqueante` (sim/não) e `justificativa`. Se bloqueante=sim e nenhuma contrarrecomendação registrada depois, F10 não fecha. Recomendações leves ("considere adicionar nota de rodapé X") não bloqueiam, mas aparecem em relatório de entrega.

---

## 4. RECOMENDAÇÕES PRIORIZADAS POR CUSTO-BENEFÍCIO

### Tier 1 — Imediatamente (próxima semana)

**R1.1 [H3] — Criar integração painel → FORJA de prioridade + enfileiramento**
- **Custo:** 16 horas engenharia;
- **Benefício:** 2x escalabilidade operacional (4 para 8 peças/semana viável);
- **Risco mitiga:** bottleneck de planejamento manual;
- **Métrica de sucesso:** Igor consegue dizer "próximas 5 peças a fazer" sem abrir 17 pastas.

**R1.2 [H2] — Instrumentar telemetria de feedback com classe de erro**
- **Custo:** 8 horas engenharia + 2 semanas de tracking manual;
- **Benefício:** evidência de ROI de auditoria (verdadeiros positivos vs falsos positivos);
- **Risco mitiga:** decisão de negócio cega;
- **Métrica de sucesso:** ao fim de 2 semanas, dados mostram (a) % de erros capturados vs não-capturados; (b) economia em retrabalho.

**R1.3 [H7] — Auditar 21 demandas e categorizar bloqueadores**
- **Custo:** 4 horas;
- **Benefício:** transparência com cliente; identificar pendências rápidas;
- **Risco mitiga:** fila fantasma;
- **Métrica de sucesso:** painel atualizado com 17 demandas classificadas por bloqueador; lista de "ações de Fábio" gerada.

---

### Tier 2 — Próximas 2 semanas

**R2.1 [H5] — Codificar 3 de 11 diretrizes do cliente ainda sem automação**
- **Custo:** 24 horas engenharia;
- **Benefício:** conformidade garantida; menos falsos-positivos;
- **Risco mitiga:** rejeição de peça por cliente;
- **Métrica de sucesso:** checklist de "questões laterais" aparece em cada blueprint; red team 9 tem template de doc.

**R2.2 [H4] — Estruturar feedback loop com teste de regressão**
- **Custo:** 20 horas engenharia + processos;
- **Benefício:** autoaprendizado contínuo; 90% dos erros conhecidos têm testes de regressão;
- **Risco mitiga:** reincidência de erro já capturado;
- **Métrica de sucesso:** primeira correção menor codificada como teste dentro de 48h; zero reincidência em amostra.

**R2.3 [H1] — Implementar E-01 a E-06 (Efesto) antes de qualquer promoção N4**
- **Custo:** 32 horas engenharia;
- **Benefício:** N4 fica verificável, não apenas bonita;
- **Risco mitiga:** falso verde em promoção N4;
- **Métrica de sucesso:** `suite_hash()` inclui data/modo; aggregador reexecuta mutation testing; zero suite retrospectiva aparenta prospectiva.

---

### Tier 3 — Próximo mês (após evidência de R1)

**R3.1 [H6] — Remapear roadmap N4 com prioridade em custo-benefício**
- **Custo:** 8 horas planejamento + revisão;
- **Benefício:** alocação de 80 horas alinhada com ROI, não cronograma;
- **Métrica de sucesso:** roadmap revisado mostra trilho N4 piloto (E-01, E-06, ciclos prospectivos) + trilho operacional (R1-R2.2) com estimativas.

**R3.2 [H9] — Avaliar valor de visual law e otimizar ou remover**
- **Custo:** 12 horas validação + decisão;
- **Benefício:** focar tempo em peça ou em visual, não ambos;
- **Métrica de sucesso:** evidência de "cliente prefere visual" ou "tempo de leitura reduz X%"; se não, visual law sai da rota crítica.

---

## 5. O SISTEMA SERVE AO NEGÓCIO?

**Resposta curta:** sim, mas abaixo do potencial.

A FORJA N2/N3 funciona para 1-2 peças/semana com qualidade superior ao baseline. O cliente Fábio recebe rascunhos revisáveis, com rastreabilidade, sem risco de falsificação. 30-40% de auditoria não é desperdício; é custo de máquina aprendendo.

**O problema é escalabilidade e valor incremental, não correção.**

Se o objetivo é 4-8 peças/semana com mesmo nível de qualidade:
- R1.1 (integração painel) destranca priorização;
- R2.1 (diretrizes codificadas) garante conformidade;
- R2.2 (feedback loop) reduz auditoria de 40% para ~25% gradualmente;
- R3 (roadmap refeito) redireciona N4 para problemas que importam (H3, H4).

**Vale a pena os 30-40% de auditoria?** Sim, enquanto a máquina aprende. Mas o custo precisa cair. Meta: 30-40% → 15-20% em 2 meses, via automação de feedback e integração com negócio.

---

## 6. RESUMO PARA O CLIENTE

Se Igor ou Fábio pedissem resumo executivo:

> **FORJA funciona. A qualidade de rascunhos é boa; a rastreabilidade é sólida; a auditoria é rigorosa.**
>
> **Limitação atual:** 1-2 peças/semana viável sem engargalo manual. Fila de 21 demandas, mas apenas ~5 prontas. 30-40% do tempo é auditoria humana (legítima, mas cara).
>
> **Próximo passo:** conectar painel de demandas a prioridades (trivial, 16h). Isso permite 4-8 peças/semana. Depois, automatizar feedback e reduzir auditoria para 20%. N4 é bônus interno; não afeta cliente ainda.
>
> **Risco:** se protocolo de 11 diretrizes não for automatizado, 1 de 10 peças pode violar conformidade. Prioridade: codificar questões processuais + identidade de atos + red team.
>
> **Investimento:** ~100 horas engenharia para dobre de capacidade + conformidade garantida. Retorno: 2x produção, mesma auditoria.

---

## 7. REGISTRO DE DECISÕES

- [x] Mantém N2 vigente; N3 candidata; N4 piloto;
- [x] Implementa E-01 a E-06 antes de promoção N4;
- [x] Bloqueia promoção N4 a `default_on` até ciclos prospectivos reais;
- [x] Autoriza R1.1-R1.3 para próxima semana;
- [x] Rejeita prorrogação de status quo sem feedback-loop (H4);
- [x] Rejeita N4 como solução de volume; R1.1 é trilho correto.

---

**Helena Strategos**  
Cientista-Chefe de Inteligência, INTEIA  
11 de julho de 2026, 02h50 BRT
