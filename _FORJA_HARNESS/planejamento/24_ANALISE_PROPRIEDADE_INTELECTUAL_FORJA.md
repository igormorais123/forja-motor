# 24 — Análise de propriedade intelectual da FORJA e plano de registro

- **Data:** 23/07/2026
- **Autor da análise:** Claude Fable 5 (sessão com Igor), a pedido do Igor
- **Natureza:** análise interna orientativa — não é parecer formal; validar com agente da propriedade industrial antes de protocolar no INPI
- **Classificação:** `internal_working` — não circular fora da operação
- **Premissa de titularidade (declaração do Igor, 23/07/2026):** o contrato com o escritório contém cláusula expressa, exigida pelo Igor como condição de entrada, atribuindo a ele a titularidade de tudo que ele cria e opera. Exceção única: a marca e identidade do escritório (Medina Osório). Em caso de saída, Igor leva o sistema. [DECLARAÇÃO — conferir o texto da cláusula antes de cada depósito e arquivar cópia junto a este documento]

---

## 1. Conclusão executiva

| Via | Viável? | O que cobre | Prioridade |
|---|---|---|---|
| **Patente (BR/EUA)** | ❌ Não recomendada | Nada que importe — método de negócio e software "em si" são excluídos (LPI art. 10, II, III e V; EUA: doutrina *Alice*) | Não fazer |
| **Registro de programa de computador — INPI (Lei 9.609/98)** | ✅ Sim | Todo o código-fonte da esteira (scripts `forja_*.py`, kits visuais, testes) | **Alta** |
| **Direito autoral (Lei 9.610/98)** | ✅ Automático; registro facultativo na Biblioteca Nacional | Documentação, protocolos, templates, PRDs/TDDs, material didático — a **expressão**, não o método | Média |
| **Marca "FORJA" — INPI (LPI)** | ✅ Sim, se houver plano de produto/serviço | Nome e identidade comercial do sistema | Média-alta se virar produto |
| **Segredo de negócio (LPI art. 195)** | ✅ Já vigente de fato | Prompts calibrados, gates, taxonomia de falhas, corpus de lições, ciclo AR | **Máxima — é a proteção mais forte** |

## 2. Por que patente não

1. **LPI art. 10, II e III** — métodos, planos e esquemas de negócio e regras abstratas não são invenção. O núcleo da FORJA (esteira F1→F10, gates de qualidade, conselho obrigatório Helena+Cícero, red team de 9 perguntas, F2-A de 100 perguntas, ciclo AR de auto-pesquisa) é método de organização de trabalho intelectual.
2. **LPI art. 10, V** — programa de computador "em si" não é patenteável. Os ~80 módulos Python não passam por essa porta.
3. A brecha das "invenções implementadas por computador" exige **problema técnico com efeito técnico** (padrão do exame do INPI). A FORJA resolve problema de qualidade e confiabilidade de produção jurídica — problema de negócio e informação, não técnico no sentido do exame.
4. EUA: *Alice Corp. v. CLS Bank* (2014) — ideia abstrata executada em computador é inelegível (35 U.S.C. §101). Mesmo destino provável.
5. **Custo estratégico**: pedido de patente é publicado após 18 meses — publicaria o funcionamento interno, destruindo a camada de segredo de negócio que hoje é o diferencial real.

## 3. O que registrar e como

### 3.1 Registro de programa de computador no INPI — prioridade 1

- Base: Lei 9.609/98 + Lei 9.610/98. Vigência: 50 anos. Sigiloso (o código não é publicado — deposita-se resumo de hash).
- Procedimento (2026): 100% eletrônico via e-Software/INPI com gov.br. Gera-se o **resumo digital hash (SHA-512) do código-fonte** e declara-se em formulário; o depósito sai em dias. Custo na casa de centenas de reais (GRU).
- **Escopo do depósito**: snapshot consolidado do código do harness — `forja_*.py`, `test_forja_*.py`, kits (`medina_visual_kit.py`, `medina_svg_kit.py`, `montar_visual.py`, `forja_visual.py`), contratos de fase (`phase_contracts/`, `n4_schemas/`) e módulos AR. **EXCLUIR obrigatoriamente**: tudo de `state/` (material sigiloso de clientes), `cache/`, credenciais, `.env`, telemetria de casos reais.
- O que dá: prova de anterioridade e autoria oponível a terceiros (inclusive ex-colaborador que copie o código). O que NÃO dá: exclusividade sobre a ideia ou o método — reimplementação independente com código próprio é lícita.
- Boa norma: novo depósito (ou aditamento) a cada versão majoritária do sistema.

### 3.2 Direito autoral sobre a documentação — automático; registro facultativo

- Já protegidos desde a criação, sem formalidade: `DOCUMENTACAO_TECNICA.md`, os documentos `planejamento/01–23`, `RETROSPECTIVAS.md` (80 lições), protocolos (escrita humana, Fable 5, tratamento de acervo), templates de fase, `FORJA_EXPLICADA_PARA_ADVOGADOS.html`.
- Registro facultativo na **Biblioteca Nacional (EDA)** serve como prova de data e autoria. Fazer para o corpus documental consolidado se ou quando a FORJA virar produto ou objeto de disputa potencial.
- **Limite estrutural (Lei 9.610, art. 8º, I e II)**: protege o texto, não o método descrito. Quem reescrever o processo com palavras próprias não infringe direito autoral — por isso o segredo de negócio (§ 3.4) é a camada decisiva.

### 3.3 Marca "FORJA" no INPI

- Registrar se houver intenção de oferta como produto ou serviço (SaaS jurídico, licenciamento a escritórios). Classes de Nice indicativas: **9** (software), **42** (SaaS/desenvolvimento), **45** (serviços jurídicos) — definir com o procurador.
- "Forja" é palavra de uso comum → risco de colidência e baixa distintividade nominativa. Fazer **busca de anterioridade** no INPI antes; considerar marca **mista** (nome + logo) ou nome composto (ex.: "FORJA INTEIA").
- A marca é independente do escritório: registrável em nome do Igor ou da INTEIA. A marca e identidade **Medina Osório** (logo, timbre) permanece do escritório — nunca incluir em depósito próprio.

### 3.4 Segredo de negócio — a proteção principal (não se registra; vive na conduta)

O valor competitivo real está no que um concorrente não reconstrói lendo uma descrição: prompts calibrados por 80 lições reais, catálogo de gates minerado de erros de produção, taxonomia de 6 modos de falha de citação, corpus de feedback humano (`APRENDIZADOS_FEEDBACK_HUMANO.md`), canários e segredos do ciclo AR. Proteção: **LPI art. 195, XI e XII** (concorrência desleal por divulgação ou exploração de conhecimento confidencial). Condição de eficácia: comportar-se como segredo —

1. repositório privado, acesso restrito e registrado;
2. ~~NDA e cláusula de confidencialidade com quem acesse a esteira~~ — **removido em 04/08/2026 (Igor).** Gestão de pessoal do escritório, não requisito do harness;
3. os segredos do AR já ficam fora do workspace (`%USERPROFILE%\.forja_ar_secrets\`) — manter a disciplina;
4. jamais publicar prompts, gates ou o funcionamento interno em material de marketing, artigo ou pedido de patente;
5. material de cliente (`state/`) tem camada adicional: sigilo profissional OAB — nunca entra em nenhum depósito, demo ou dataset.

## 4. Ressalva de autoria com IA

Parte do código e dos textos foi gerada com IA (Claude/Codex) sob direção do Igor. Obra **puramente** gerada por IA não tem autor humano e tem proteção autoral duvidosa (posição firme do US Copyright Office; doutrina majoritária no Brasil na mesma linha). A proteção se sustenta na **contribuição criativa humana substancial**: arquitetura, direção, seleção, curadoria, revisão e as decisões documentadas (retrospectivas, decisões de conselho, feedback humano). Essa trilha documental já existe na FORJA e deve ser preservada — é a prova da autoria humana se o registro for contestado. No formulário do INPI, o autor e titular declarado é o Igor (pessoa física) ou a pessoa jurídica dele, conforme orientação do procurador.

## 5. Plano de ação (ordem recomendada)

| # | Ação | Órgão | Urgência |
|---|---|---|---|
| 1 | Arquivar cópia da cláusula contratual de titularidade junto a este documento | interno | imediata |
| 2 | Preparar snapshot limpo do código (sem `state/`, `cache/`, segredos) + hash SHA-512 e depositar registro de programa | INPI (e-Software) | alta — semanas |
| 3 | Formalizar regime de segredo: NDA padrão + inventário do que é confidencial | interno | alta |
| 4 | Busca de anterioridade da marca; decidir nome definitivo; depositar se houver plano de produto | INPI (e-Marcas) | condicionada à decisão de produto |
| 5 | Registro facultativo do corpus documental | Biblioteca Nacional (EDA) | baixa — quando virar produto ou surgir risco |
| 6 | **Não** iniciar pedido de patente | — | decisão registrada; não reabrir sem fato novo (ex.: componente com efeito técnico genuíno) |

## 6. Decisões registradas

- **Patente: descartada** (fundamentos no § 2). Reabrir apenas com fato novo técnico.
- **Estratégia adotada**: segredo de negócio como camada principal + registro de software no INPI como prova de anterioridade + marca se houver produto.
- Este documento deve ser atualizado a cada mudança material (depósito realizado, mudança contratual, decisão de comercializar).
