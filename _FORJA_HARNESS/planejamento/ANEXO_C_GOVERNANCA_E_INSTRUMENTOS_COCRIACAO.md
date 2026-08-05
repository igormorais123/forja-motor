# 35 — Roteiro, portões e instrumentos de operação

**Protocolo:** `FORJA-COCRIACAO-v1`
**Data:** 25/07/2026. **Estado:** roteiro para aprovação. **Não autoriza implementação.**
**Rege-se pelo PRD `33` e pelo TDD `34`.**

---

## 1. Quatro ondas

Cada onda tem saída verificável e portão de passagem. Nenhuma onda começa sem o portão da anterior fechado. As ondas 1A e 1B correm em paralelo.

### Onda 0 — Contratos, proveniência e baseline
**Sem qualquer mudança de saída. Sem código de produção.**

Entregas:
1. Semântica dos estados epistêmicos fixada: `record_evidence`, `office_declaration`, `inference`, `unknown`.
2. Classe de silêncio e efeito definidos por tipo de pergunta, na forma de RF-2.4.
3. Matriz de produtores e consumidores dos artefatos a estender, com os sete consumidores do TDD §5.6.
4. Schemas, versões e plano de migração aditiva.
5. Fonte adequada por campo do mapa do destinatário.
6. **Inventário real do bridge TeiaJus**: separar capacidades anunciadas pelo agente, ações permitidas por `FORJA_SEARCH_CONFIG.json`, comandos já expostos e fontes não integradas.
7. Plano de corpus e regras de atribuição, reaproveitando `forja_learning.py`.

**Portão 0 — bloqueante:**
- [ ] Régua verde, **ou** desvio classificado e aceito como baseline conhecido. Rebaseline automático permanece proibido.
- [ ] Nenhuma afirmação de capacidade existente sustentada apenas por semelhança de nome. Cada "já existe" tem arquivo, linha ou artefato real.
- [ ] Os 22 shells do catálogo que este plano não usa permanecem sem alteração.

### Onda 1A — Cocriação em sombra

Entregas: seleção de perguntas materiais; minuta de consulta; ledger de decisão; replay sobre casos históricos com resposta conhecida; teste de rodadas múltiplas e de silêncio material.

**Portão 1A:**
- [ ] Zero pergunta emitida que estivesse respondida no acervo — métrica de emissão igual a zero.
- [ ] Zero fato material convertido em premissa por silêncio.
- [ ] Zero envio externo. A consulta existe como minuta interna.
- [ ] Resposta parcial mantém a pendência aberta, provado em teste.

### Onda 1B — Destinatário e precedentes em sombra

Entregas: mapa do destinatário com fonte por campo; pesquisa topológica pertinente ao tribunal do caso; brief e cobertura de famílias; verificação de três a seis âncoras; reabertura de F4 quando a âncora cai.

**Portão 1B:**
- [ ] Composição, prevenção, ratio e vigência conferidas conforme a natureza de cada dado.
- [ ] Nenhuma âncora com ratio sustentada apenas por ementa.
- [ ] Todo precedente-âncora com operação declarada.
- [ ] Campos não apurados presentes e motivados, em vez de ausentes.
- [ ] `F6` inalterada.

### Onda 2 — Identidade e variante de redação

Entregas: `IDENTITY_CORPUS_MANIFEST.jsonl` com atribuição e confiança; separação entre escrita, edição, feedback e fala; padrões candidatos extraídos; **um único** draft variante que consome brief e padrões; comparação cega no AUTO-RESEARCH, com o prompt atual como incumbente.

**Portão 2:**
- [ ] Não inferioridade jurídica confirmada antes de qualquer preferência editorial.
- [ ] Preferência cega estável após troca de posição.
- [ ] Ganho não explicado por tamanho nem por corte de conteúdo obrigatório.
- [ ] Nenhum padrão de identidade ativado com origem apenas em hipótese sobre trajetória pública.
- [ ] Se não houver ganho, a decisão correta é sombra ou desligamento — e isso não é fracasso do projeto.

### Onda 3 — Piloto controlado

Entregas: ativação por `pilotCases`; uma peça por caso; consulta enviada por pessoa autorizada; mapa e brief ativos; F7 e F7-B recompondo rota, âncoras e conteúdo obrigatório; revisão humana final obrigatória.

**Portão 3, para ampliar:**
- [ ] Ganho prospectivo estável.
- [ ] Zero regressão jurídica ou factual.
- [ ] Rastreabilidade completa do brief até o texto final.
- [ ] Custo e latência dentro do teto.
- [ ] Rollback exercitado de fato, não apenas descrito.

As oito condições de `default_on` da revisão adversarial Fable 5 de 24/07 permanecem integralmente aplicáveis e não são reabertas aqui.

### Trilha condicional, fora das ondas centrais

Conectores de jurisprudência administrativa — TCU, CGU e CRG, CADE, CVM, CNJ, CNMP — por demanda real. Módulo J-B de jurimetria comportamental somente após autorização expressa, parecer do Cícero e desenho estatístico válido. Nenhum dos dois bloqueia as ondas centrais.

---

## 2. Instrumento de governança: registro de escopo

Preenchido a cada onda. Existe para impedir recrescimento silencioso da superfície.

| Item | Valor aprovado | Valor observado | Desvio justificado por |
|---|---:|---:|---|
| Tipos novos de artefato | 1 | | |
| Shells do catálogo ativados | 2 | | |
| Extensões de artefato existente | 3 | | |
| Subfases novas | 2 | | |
| Módulos novos | 4 arquivos | | |
| Pacotes ou CLIs novos | 0 | | |
| Drafts por petição | 1 | | |

Qualquer valor observado acima do aprovado exige justificativa escrita e aceite antes de prosseguir. **Ausência de justificativa barra a onda.**

---

## 3. Instrumento de operação: gabarito da consulta

Estrutura fixa da minuta que sai para o advogado responsável. Não é modelo de texto: é lista de verificação de completude antes da revisão humana.

1. **Compreensão declarada** — o que entendi que se pede; o que li; o que não li e por quê; documentos ilegíveis, truncados, sem assinatura ou com páginas faltando.
2. **Perguntas decisórias**, ordenadas por impacto. Cada uma com: a pergunta; por que preciso saber; o que muda em cada resposta; **e o efeito da ausência de resposta, na classe correta**.
3. **Diligências documentais motivadas** — documento pretendido; tese ou fato que depende dele; fundamentação; consequência da ausência.
4. **Rotas, para provocação** — as rotas que vejo; **as que descartei e por quê**; e a pergunta final: o que o senhor vê aqui que não está nesta lista?
5. **Decisões reservadas ao senhor** — objetivo, apetite de risco, disposição para acordo, tratamento de fato superveniente, sustentação oral.

**Verificações antes de submeter à revisão humana**
- [ ] Nenhuma pergunta respondível pelo acervo inventariado.
- [ ] Nenhuma pergunta respondível por pesquisa que caiba a nós.
- [ ] Nenhum marcador interno de auditoria, caminho local ou proveniência operacional no texto.
- [ ] Toda pergunta de fato material declara bloqueio, e não premissa.
- [ ] Destinatário correto e canal registrado.

---

## 4. Instrumento de decisão: tabela de parâmetros por classe

**Deliberadamente vazia.** Preencher com o titular, na reunião. Chegar com ela preenchida contraria o que ele disse — recusou o papel de especificador de cima e pediu que cresçamos juntos.

| Parâmetro | Simples | Complexo | Estratégico |
|---|---|---|---|
| Teto de rodadas de consulta | | | |
| Faixa de rotas no brief | | | |
| Número de âncoras com ficha profunda | | | |
| Extensão máxima da peça | | | |
| Nível de revisão humana exigido | | | |
| Mapa do destinatário obrigatório | | | |
| Módulo J-B disponível | não | mediante autorização | mediante autorização |

---

## 5. Instrumento de apresentação ao titular

Três peças, e a segunda é a que decide pelo critério dele.

1. **Rastreabilidade requisito para fase** — a tabela do documento `29`, §6. Demonstra que a arquitetura decorre da fala dele, e não do gosto do fornecedor.
2. **Demonstração ao vivo de recusa** — o sistema bloqueando a citação de um precedente cuja íntegra não conseguiu obter. Ele não mencionou custo, prazo nem tecnologia uma única vez na entrevista; o critério dele é confiabilidade auditável, e ele disse por quê: pesquisa falsa desmoraliza quem a usa.
3. **A tabela do §4, vazia**, para preencher com ele.

---

## 6. Instrumento de revisão: perguntas de aceite do plano

Marcar antes de autorizar implementação.

- [ ] Os artefatos novos e estendidos têm dono, schema, consumidor e invalidador definidos.
- [ ] O efeito do silêncio está codificado por classe de pergunta.
- [ ] Resposta, aceite estratégico e prova factual estão separados.
- [ ] Cada campo do mapa tem fonte, política de frescor e comportamento de falha.
- [ ] O bridge TeiaJus necessário está distinguido das capacidades apenas anunciadas.
- [ ] Ratio decisiva exige conteúdo suficiente e localização verificável.
- [ ] O regime do precedente não foi reduzido a peso numérico.
- [ ] O corpus tem política de autoria e de contribuição intelectual.
- [ ] A/B, conferência factual e métrica de interação não estão confundidos.
- [ ] O envio externo permanece sujeito a autorização.
- [ ] Casos legados preservam compatibilidade.
- [ ] AH-01 a AH-08 permanecem fail-closed em `strict_protocol`.
- [ ] Os 22 shells não usados permanecem intocados.

---

## 7. Mapa da cadeia documental

| Documento | Papel | Estado |
|---|---|---|
| `25_GOSTO_JURIDICO_AUTONOMO_EDGE` | protocolo EDGE, já implementado em F6, F7-B e AUTO-RESEARCH | vigente |
| `26`, `27`, `28` — FORJA-ASSINATURA v1 | visão longa e backlog experimental | reclassificados |
| `29_REQUISITOS_ENTREVISTA` | requisitos declarados pelo titular | fonte |
| `30_ARQUITETURA_DIALETICA` | os três eixos, detalhados | fonte |
| `31_PLANO_UNICO` | consolidação v1 | histórico |
| `32_PLANO_UNICO_V2` | consolidação v2 do Codex | insumo, revisado no `33`, §1 |
| **`33_PRD`** | requisitos de produto | **vigente** |
| **`34_TDD`** | desenho técnico | **vigente** |
| **`35`** | roteiro, portões e instrumentos | **vigente** |

Em conflito operacional entre `31`, `32` e a trinca `33`–`35`, prevalece a trinca.
