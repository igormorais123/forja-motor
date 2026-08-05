# Lapidação da FORJA — veredito final

**Data:** 2026-08-05. **Branch:** `forja/lapidacao-sqlite-grade-20260805`, 10 commits sobre
`forja-congelada-20260805` = `3866e1c16`.
**Custo:** 18 agentes em três ondas, ~1,57 milhão de tokens de subagente.
**Governança:** `GOVERNANCA_LAPIDACAO_2026-08-05.md` (Helena) + `forja_lapidacao_governanca.py` (Efesto).

---

## Resposta direta às duas condições de parada que o dono fixou

O pedido era não parar até que **(a)** o avaliador prefira a FORJA aperfeiçoada em
comparação direta contra a congelada, e **(b)** se confirme que o resultado atingiu a
disciplina do *SQLite test harness*.

**(a) Atingida.** **(b) NÃO atingida, e não é atingível por iteração desta campanha.**

Continuar iterando até que alguém diga "sim" à segunda condição seria fabricar a resposta —
exatamente o comportamento resistente-a-Goodhart que o pedido mandava evitar. O relatório
honesto vale mais que a conclusão desejada.

---

## (a) A comparação direta

Mesma bateria nos dois lados: 6 casos, 102 mutantes, operadores determinísticos.

| Família | Congelada | Aperfeiçoada |
|---|---|---|
| S1 inversão de tese | 0/2 | 0/2 |
| **S2 troca de parte** | **0/23** | **0/23** |
| S3 valor ou data | 2/30 | 2/30 |
| **S4 troca de pedido** | **0/12** | **0/12** |
| S5 sobreabstração | 0/23 | **4/23** |
| S6 deturpação de precedente | 9/12 | 9/12 |
| **Geral** | **0,1078** | **0,1471** |

Dois verificadores de contexto novo, que não participaram da construção:

- **Verificador independente: prefere a APERFEIÇOADA.** "+4 detecções reais sem dano",
  zero regressão nas outras cinco famílias.
- **Avaliador de disciplina: rotulou CONGELADA** — mas não apresentou **nenhuma** evidência
  de que a congelada seja melhor. Sua medição confirma o ganho de +4 com zero regressão. O
  que ele de fato rejeita é a **alegação de paridade com o SQLite**, e nisso está certo. O
  rótulo contradiz os próprios dados dele e não sobrevive à leitura; a rejeição da paridade
  sobrevive inteira, e está acatada abaixo.

Uma refutação dele foi conferida e não procede: alegou não localizar as checagens
`N4-Q-100-DIVERSITY` e `N4-Q-100-NO-GAP`. Elas estão em `forja_exploracao_100.py`,
commitadas em `2aaf90801`, e acusam 14/14 e 9/14 árvores reais. Ele leu o arquivo enquanto
um processo externo havia trocado a branch (lição 200).

## (b) A disciplina do SQLite, medida

| Dimensão | SQLite | FORJA | Distância |
|---|---|---|---|
| Razão teste : produção | ~590x | **0,42x** | ~1.400x |
| Escore de mutação | — | **0,147** (alvo próprio: 0,80) | 18% do alvo |
| Gates com contraprova de sabotagem | regra | ~12 testes nominados | minoria |
| Corpus de regressão | centenas | 6 casos canônicos de 53 | 11% |

**Não é rigor de SQLite test harness, e a diferença é de ordem de grandeza, não de ajuste.**

O que faltaria, concretamente: matar ~67 mutantes a mais dos 102, o que exige fechar
S2 (23) e S4 (12) — as duas famílias em zero **nas duas versões**. Traduzindo para o risco
real: **inverter o pedido da própria cliente, ou trocar agravante por agravado, sai
protocolável hoje.** A única tentativa de fechá-las nesta campanha produziu um gate que
reprovava duas das três peças aprovadas pelo escritório, e foi revertido.

---

## O que a campanha entregou, então

**1. O número passou a existir.** `forja_mutation_semantic.py` havia rodado em **2 dos 53
casos** na história do sistema. Agora há painel em lote e o escore é rastreável. Antes de
hoje ninguém sabia que era 0,11.

**2. Três falsos progressos foram impedidos** — e num sistema de alta confiança isso conta
tanto quanto o que se constrói:

- *Um gate que travaria a produção inteira.* `forja_coerencia_processual` reprovava
  `cafelana-v8` e `cafelana-v4`, emitia P0 dentro do `verificar()` que a porta única chama
  em toda peça, e engolia exceção com `except: pass`. Erro de conceito: nas Impugnações ao
  Agravo Interno a cliente pede o *desprovimento* do agravo alheio e a peça cita
  "provimento" ao referir o pedido adversário; numa delas o gate apontou a União — a parte
  adversa — como cliente.
- *Um conserto para problema inexistente.* "Ativar L9–L13 dormentes" foi aprovado pelo
  avaliador da onda 1 com arquivo e linha. Executado: são fail-closed por construção.
- *Uma catraca afrouxada com boa redação.* O canário caiu para 39/34 e acusou cegueira; o
  gate que sumiu tinha acabado de **enxergar**. Corrigiu-se a medida, não o piso.

**3. Governança executável.** Os sete critérios de parada viraram função que confere o
estado vivo, cada um visto reprovando uma sabotagem.

**4. Achados de segurança.** 5.691 arquivos de caso e 759 binários (159,8 MB) versionados
no repositório do engine, com nomes de cliente e números CNJ.

**5. Seis lições** (195–200), das quais três nasceram de defeitos no código escrito **nesta
campanha**, todos pegos por medição e não por revisão.

## Estado de validação

- Baseline **APROVADO**: 89/89 suítes, 569 testes, 60 subtestes, 43 regressões em script
  (congelada: 83, 545, 41).
- Régua **APROVADO em 142,3 s**, rebaseline de 4 arquivos com motivo no histórico.
- Âncoras aprovadas intactas. Fail-closed preservado: Cafelana travado, revision 177.
- Invariantes: 7 de 8 verdes. O oitavo é o repositório, e é decisão do Igor.

## A campanha seguinte, se houver

Em ordem de risco jurídico evitado:

1. **Fechar S2 e S4 sem repetir o erro do gate revertido.** O caminho não é ler o texto da
   peça isoladamente: é comparar o papel e o pedido declarados contra o que o **próprio
   caso** registra em `FORJA_CASE_MANIFEST.json`. Coerência interna do texto não distingue
   citação do adversário de pedido contra si; coerência texto-versus-caso distingue.
2. **Produzir uma árvore F2A de exploração genuína** para servir de âncora positiva. Sem
   ela, promover as checagens de diversidade a P0 é arbitrário.
3. **Decidir o repositório** — separar o engine do acervo, ou aceitar formalmente o estado.
4. **Elevar a razão teste:produção**, hoje em 0,42x. Não a 590x, que é fantasia para este
   contexto, mas a contraprova de sabotagem deixando de ser minoria.
