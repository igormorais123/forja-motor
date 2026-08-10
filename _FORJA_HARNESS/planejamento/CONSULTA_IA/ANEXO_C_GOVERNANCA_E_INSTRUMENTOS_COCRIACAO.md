# Consulta IA — 35 — Roteiro, portões e instrumentos de operação

> Cópia de consulta derivada. O documento canônico permanece no caminho de origem indicado abaixo.

## Metadados e rastreabilidade

- **Documento de origem:** `ANEXO_C_GOVERNANCA_E_INSTRUMENTOS_COCRIACAO.md`
- **Tipo:** Anexo
- **SHA-256 da origem:** `caa3236fb1ce89e885b525e80020c50e97f817cc7767c2f3c98b72959cd87281`
- **Linhas da origem:** 178
- **Blocos integralmente indexados:** 14
- **Geração:** 2026-08-10T13:53:35-03:00
- **Cobertura:** 100% das linhas e do texto da origem, sem omissão.
- **Links relativos normalizados:** 0 destino(s), apenas para preservar a navegação na cópia.

## Roteiro de consulta para IA

**Síntese de localização:** Protocolo: FORJA-COCRIACAO-v1 Data: 25/07/2026. Estado: roteiro para aprovação. Não autoriza implementação. Rege-se pelo PRD 33 e pelo TDD 34.

**Termos de recuperação:** não, onda, instrumento, pergunta, revisão, mapa, cada, portão, operação, ondas, destinatário, consulta.

Use o índice abaixo para localizar o bloco pertinente. Cada entrada informa as linhas exatas no documento de origem. Para afirmações materiais, leia o bloco integral e confira o arquivo canônico pelo SHA-256.

## Índice detalhado e cobertura integral

- [SRC-S001 · L1–L8 · 35 — Roteiro, portões e instrumentos de operação](#src-s001)
  - Assuntos: roteiro, portões, instrumentos, operação, pelo, protocolo, forja-cocriacao-v1, data
  - Trecho-guia: Protocolo: FORJA-COCRIACAO-v1 Data: 25/07/2026. Estado: roteiro para aprovação. Não autoriza implementação. Rege-se pelo PRD 33 e pelo TDD 34.
  - SHA-256 do bloco: `d25f2137bf1126e01c0410d09a963de9b77cda35ebc9d45fe5455d50106f56ab`
  - [SRC-S002 · L9–L12 · 1. Quatro ondas](#src-s002)
    - Caminho: 35 — Roteiro, portões e instrumentos de operação > 1. Quatro ondas
    - Assuntos: ondas, quatro, onda, portão, cada, tem, saída, verificável
    - Trecho-guia: Cada onda tem saída verificável e portão de passagem. Nenhuma onda começa sem o portão da anterior fechado. As ondas 1A e 1B correm em paralelo.
    - SHA-256 do bloco: `04a343e64bfc3bfc88ab94f13ce553b5c2f917d13e220f19fda2eace8ca35f74`
    - [SRC-S003 · L13–L29 · Onda 0 — Contratos, proveniência e baseline](#src-s003)
      - Caminho: 35 — Roteiro, portões e instrumentos de operação > 1. Quatro ondas > Onda 0 — Contratos, proveniência e baseline
      - Assuntos: baseline, plano, onda, contratos, proveniência, consumidores, real, não
      - Trecho-guia: Sem qualquer mudança de saída. Sem código de produção.
      - SHA-256 do bloco: `5d36164543b7cda3cbd295dd7f61e4b92c9c7df3b885b2a9ca76593a3d8cb9e6`
    - [SRC-S004 · L30–L39 · Onda 1A — Cocriação em sombra](#src-s004)
      - Caminho: 35 — Roteiro, portões e instrumentos de operação > 1. Quatro ondas > Onda 1A — Cocriação em sombra
      - Assuntos: zero, onda, cocriação, sombra, minuta, consulta, resposta, teste
      - Trecho-guia: Entregas: seleção de perguntas materiais; minuta de consulta; ledger de decisão; replay sobre casos históricos com resposta conhecida; teste de rodadas múltiplas e de silêncio material.
      - SHA-256 do bloco: `ab8a933148dffea82726fa6576806b5c9a1f6a8c35373848b20890643d2fe83a`
    - [SRC-S005 · L40–L50 · Onda 1B — Destinatário e precedentes em sombra](#src-s005)
      - Caminho: 35 — Roteiro, portões e instrumentos de operação > 1. Quatro ondas > Onda 1B — Destinatário e precedentes em sombra
      - Assuntos: destinatário, onda, precedentes, sombra, âncora, ratio, entregas, mapa
      - Trecho-guia: Entregas: mapa do destinatário com fonte por campo; pesquisa topológica pertinente ao tribunal do caso; brief e cobertura de famílias; verificação de três a seis âncoras; reabertura de F4 quando a âncora cai.
      - SHA-256 do bloco: `17454e3436dfad4bb368385a2ffb63ee6609a07ce53876b9c367b31eff6961e4`
    - [SRC-S006 · L51–L61 · Onda 2 — Identidade e variante de redação](#src-s006)
      - Caminho: 35 — Roteiro, portões e instrumentos de operação > 1. Quatro ondas > Onda 2 — Identidade e variante de redação
      - Assuntos: não, identidade, variante, onda, redação, padrões, cega, preferência
      - Trecho-guia: Entregas: IDENTITYCORPUSMANIFEST.jsonl com atribuição e confiança; separação entre escrita, edição, feedback e fala; padrões candidatos extraídos; um único draft variante que consome brief e padrões; comparação cega no AUTO-RESEARCH, com o prompt atual como incumbente.
      - SHA-256 do bloco: `153510179944f075a61a2d7dda4e696811239464dded8c1006504f4160f9fa82`
    - [SRC-S007 · L62–L74 · Onda 3 — Piloto controlado](#src-s007)
      - Caminho: 35 — Roteiro, portões e instrumentos de operação > 1. Quatro ondas > Onda 3 — Piloto controlado
      - Assuntos: onda, piloto, controlado, brief, revisão, final, não, entregas
      - Trecho-guia: Entregas: ativação por pilotCases; uma peça por caso; consulta enviada por pessoa autorizada; mapa e brief ativos; F7 e F7-B recompondo rota, âncoras e conteúdo obrigatório; revisão humana final obrigatória.
      - SHA-256 do bloco: `34f81f4e30b52db88933eb6a7f5c01c485e9537a1fbff7ad18d722dadcd8b2dc`
    - [SRC-S008 · L75–L80 · Trilha condicional, fora das ondas centrais](#src-s008)
      - Caminho: 35 — Roteiro, portões e instrumentos de operação > 1. Quatro ondas > Trilha condicional, fora das ondas centrais
      - Assuntos: ondas, centrais, trilha, condicional, fora, conectores, jurisprudência, administrativa
      - Trecho-guia: Conectores de jurisprudência administrativa — TCU, CGU e CRG, CADE, CVM, CNJ, CNMP — por demanda real. Módulo J-B de jurimetria comportamental somente após autorização expressa, parecer do Cícero e desenho estatístico válido. Nenhum dos dois bloqueia as ondas centrais.
      - SHA-256 do bloco: `b75d8f1466d946e4d338911d1e6896ca1e626dc0721288476c05b50b1d3db241`
  - [SRC-S009 · L81–L98 · 2. Instrumento de governança: registro de escopo](#src-s009)
    - Caminho: 35 — Roteiro, portões e instrumentos de operação > 2. Instrumento de governança: registro de escopo
    - Assuntos: valor, novos, instrumento, governança, registro, escopo, onda, aprovado
    - Trecho-guia: Preenchido a cada onda. Existe para impedir recrescimento silencioso da superfície.
    - SHA-256 do bloco: `65f86079c83494ae9da86cae0f46df03f24748d071c5ca5dd6ee99f8b67277b9`
  - [SRC-S010 · L99–L117 · 3. Instrumento de operação: gabarito da consulta](#src-s010)
    - Caminho: 35 — Roteiro, portões e instrumentos de operação > 3. Instrumento de operação: gabarito da consulta
    - Assuntos: pergunta, não, fato, instrumento, operação, gabarito, consulta, texto
    - Trecho-guia: Estrutura fixa da minuta que sai para o advogado responsável. Não é modelo de texto: é lista de verificação de completude antes da revisão humana.
    - SHA-256 do bloco: `0571a14a2bbbca8647aa5ba424f3656ea56c62e646ddb4ef124c8e52af3503fc`
  - [SRC-S011 · L118–L133 · 4. Instrumento de decisão: tabela de parâmetros por classe](#src-s011)
    - Caminho: 35 — Roteiro, portões e instrumentos de operação > 4. Instrumento de decisão: tabela de parâmetros por classe
    - Assuntos: instrumento, decisão, tabela, parâmetros, classe, mediante, autorização, deliberadamente
    - Trecho-guia: Deliberadamente vazia. Preencher com o titular, na reunião. Chegar com ela preenchida contraria o que ele disse — recusou o papel de especificador de cima e pediu que cresçamos juntos.
    - SHA-256 do bloco: `ae56129358d83c4cf0e11c93c36a520dbc28553eb2d5abcc721b4a928d82fd7c`
  - [SRC-S012 · L134–L143 · 5. Instrumento de apresentação ao titular](#src-s012)
    - Caminho: 35 — Roteiro, portões e instrumentos de operação > 5. Instrumento de apresentação ao titular
    - Assuntos: dele, não, ele, instrumento, apresentação, titular, critério, tabela
    - Trecho-guia: Três peças, e a segunda é a que decide pelo critério dele.
    - SHA-256 do bloco: `b0507ba998db3c431a847740fc383c8231c252198986432f5e800b0be2af6363`
  - [SRC-S013 · L144–L163 · 6. Instrumento de revisão: perguntas de aceite do plano](#src-s013)
    - Caminho: 35 — Roteiro, portões e instrumentos de operação > 6. Instrumento de revisão: perguntas de aceite do plano
    - Assuntos: aceite, têm, não, instrumento, revisão, perguntas, plano, está
    - Trecho-guia: Marcar antes de autorizar implementação.
    - SHA-256 do bloco: `ed155457fdaed274f0000cd824bff940048f3d2f1255b4b786f1e3b4ee992c09`
  - [SRC-S014 · L164–L178 · 7. Mapa da cadeia documental](#src-s014)
    - Caminho: 35 — Roteiro, portões e instrumentos de operação > 7. Mapa da cadeia documental
    - Assuntos: vigente, mapa, cadeia, documental, requisitos, fonte, consolidação, trinca
    - Trecho-guia: Em conflito operacional entre 31, 32 e a trinca 33–35, prevalece a trinca.
    - SHA-256 do bloco: `efeee8a1d3a4435ed52bef7e97692fcc9928cbee36a1a20173c69ed3aa6fc90b`

## Conteúdo integral indexado

Os marcadores HTML abaixo são apenas âncoras de navegação. O texto reproduz integralmente a origem normalizada em UTF-8; somente destinos de links relativos podem ter sido recalculados para apontar ao mesmo arquivo a partir desta pasta.

<a id="src-s001"></a>

# 35 — Roteiro, portões e instrumentos de operação

**Protocolo:** `FORJA-COCRIACAO-v1`
**Data:** 25/07/2026. **Estado:** roteiro para aprovação. **Não autoriza implementação.**
**Rege-se pelo PRD `33` e pelo TDD `34`.**

---


<a id="src-s002"></a>

## 1. Quatro ondas

Cada onda tem saída verificável e portão de passagem. Nenhuma onda começa sem o portão da anterior fechado. As ondas 1A e 1B correm em paralelo.


<a id="src-s003"></a>

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


<a id="src-s004"></a>

### Onda 1A — Cocriação em sombra

Entregas: seleção de perguntas materiais; minuta de consulta; ledger de decisão; replay sobre casos históricos com resposta conhecida; teste de rodadas múltiplas e de silêncio material.

**Portão 1A:**
- [ ] Zero pergunta emitida que estivesse respondida no acervo — métrica de emissão igual a zero.
- [ ] Zero fato material convertido em premissa por silêncio.
- [ ] Zero envio externo. A consulta existe como minuta interna.
- [ ] Resposta parcial mantém a pendência aberta, provado em teste.


<a id="src-s005"></a>

### Onda 1B — Destinatário e precedentes em sombra

Entregas: mapa do destinatário com fonte por campo; pesquisa topológica pertinente ao tribunal do caso; brief e cobertura de famílias; verificação de três a seis âncoras; reabertura de F4 quando a âncora cai.

**Portão 1B:**
- [ ] Composição, prevenção, ratio e vigência conferidas conforme a natureza de cada dado.
- [ ] Nenhuma âncora com ratio sustentada apenas por ementa.
- [ ] Todo precedente-âncora com operação declarada.
- [ ] Campos não apurados presentes e motivados, em vez de ausentes.
- [ ] `F6` inalterada.


<a id="src-s006"></a>

### Onda 2 — Identidade e variante de redação

Entregas: `IDENTITY_CORPUS_MANIFEST.jsonl` com atribuição e confiança; separação entre escrita, edição, feedback e fala; padrões candidatos extraídos; **um único** draft variante que consome brief e padrões; comparação cega no AUTO-RESEARCH, com o prompt atual como incumbente.

**Portão 2:**
- [ ] Não inferioridade jurídica confirmada antes de qualquer preferência editorial.
- [ ] Preferência cega estável após troca de posição.
- [ ] Ganho não explicado por tamanho nem por corte de conteúdo obrigatório.
- [ ] Nenhum padrão de identidade ativado com origem apenas em hipótese sobre trajetória pública.
- [ ] Se não houver ganho, a decisão correta é sombra ou desligamento — e isso não é fracasso do projeto.


<a id="src-s007"></a>

### Onda 3 — Piloto controlado

Entregas: ativação por `pilotCases`; uma peça por caso; consulta enviada por pessoa autorizada; mapa e brief ativos; F7 e F7-B recompondo rota, âncoras e conteúdo obrigatório; revisão humana final obrigatória.

**Portão 3, para ampliar:**
- [ ] Ganho prospectivo estável.
- [ ] Zero regressão jurídica ou factual.
- [ ] Rastreabilidade completa do brief até o texto final.
- [ ] Custo e latência dentro do teto.
- [ ] Rollback exercitado de fato, não apenas descrito.

As oito condições de `default_on` da revisão adversarial Fable 5 de 24/07 permanecem integralmente aplicáveis e não são reabertas aqui.


<a id="src-s008"></a>

### Trilha condicional, fora das ondas centrais

Conectores de jurisprudência administrativa — TCU, CGU e CRG, CADE, CVM, CNJ, CNMP — por demanda real. Módulo J-B de jurimetria comportamental somente após autorização expressa, parecer do Cícero e desenho estatístico válido. Nenhum dos dois bloqueia as ondas centrais.

---


<a id="src-s009"></a>

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


<a id="src-s010"></a>

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


<a id="src-s011"></a>

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


<a id="src-s012"></a>

## 5. Instrumento de apresentação ao titular

Três peças, e a segunda é a que decide pelo critério dele.

1. **Rastreabilidade requisito para fase** — a tabela do documento `29`, §6. Demonstra que a arquitetura decorre da fala dele, e não do gosto do fornecedor.
2. **Demonstração ao vivo de recusa** — o sistema bloqueando a citação de um precedente cuja íntegra não conseguiu obter. Ele não mencionou custo, prazo nem tecnologia uma única vez na entrevista; o critério dele é confiabilidade auditável, e ele disse por quê: pesquisa falsa desmoraliza quem a usa.
3. **A tabela do §4, vazia**, para preencher com ele.

---


<a id="src-s013"></a>

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


<a id="src-s014"></a>

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
