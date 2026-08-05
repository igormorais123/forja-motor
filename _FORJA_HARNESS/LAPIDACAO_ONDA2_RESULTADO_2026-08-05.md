# Lapidação da FORJA — Onda 2: o que ficou, o que foi revertido, o que continua aberto

**Data:** 2026-08-05. **Branch:** `forja/lapidacao-sqlite-grade-20260805`.
**Congelada:** `forja-congelada-20260805` = `3866e1c16`.
**Custo:** 8 agentes, 707.137 tokens, 261 chamadas, 20 minutos. Acumulado da campanha:
16 agentes, ~1,38 milhão de tokens.

---

## A comparação direta, que é a única coisa que decide

Mesma bateria, mesmos 6 casos, mesmos 102 mutantes, rodada nos dois lados:

| Família | Congelada | Aperfeiçoada | Δ |
|---|---|---|---|
| S1 inversão de tese | 0/2 | 0/2 | — |
| **S2 troca de parte** | **0/23** | **0/23** | — |
| S3 valor ou data | 2/30 | 2/30 | — |
| **S4 troca de pedido** | **0/12** | **0/12** | — |
| S5 sobreabstração | 0/23 | **4/23** | **+4** |
| S6 deturpação de precedente | 9/12 | 9/12 | — |
| **Geral** | **0,1078 (11/102)** | **0,1471 (15/102)** | **+4** |

**O ganho é inteiramente de uma família.** Cinco das seis estão idênticas. E as duas mais
graves continuam em zero nas duas versões: **inverter o pedido da própria cliente
(`provimento` → `desprovimento`) passa 12 de 12 vezes, e trocar as partes passa 23 de 23.**

O alvo declarado pelo próprio harness é 0,80. Estamos em 0,147. Quem ler este documento
procurando uma vitória não vai encontrá-la aqui.

## O que a campanha de fato entregou

Não foi escore de mutação. Foi outra coisa, e vale nomear com precisão:

1. **O número passou a existir.** O harness de mutação semântica havia rodado em 2 dos 53
   casos na história do sistema. Agora há `forja_mutation_lote.py`, o painel roda em lote e
   o número é rastreável. Antes da campanha ninguém sabia que o escore era 0,11.
2. **Dois falsos progressos foram barrados antes de virar código.**
3. **Um gate que bloquearia a produção inteira foi revertido antes de sair da branch.**
4. **Uma catraca que media a coisa errada foi corrigida sem ser afrouxada.**

---

## Ficam

**`gate_s5_sobreabstracao`** (`forja_verificador.py`). Afirmação de jurisprudência
consolidada — "é pacífico", "as Cortes Superiores firmaram" — sem citação nominal
conferível na mesma frase ou no parágrafo seguinte. É o modo de falha "tese deturpada" da
taxonomia da casa, e o mais perigoso numa peça, porque afirma autoridade que o julgador não
tem como conferir. **P1**, calibrado: 0 falsos positivos em 19 casos reais, 7/7 sabotagens
pegas, âncoras aprovadas intactas.

**Rastreabilidade de proveniência** (`forja_context.py`). Os 184 achados
`unknown_provenance_reference` passam a carregar `gateCode` e `anchor` com bloco, linha e
trecho. Aditivo, com teste de compatibilidade para leitor que não conhece o campo.

**Guardas de vacuidade** em `forja_axi.py`.

**`forja_mutation_lote.py`**, o painel em lote descrito acima.

---

## Revertido: `forja_coerencia_processual`

Era a melhoria mais importante da onda — o gate que deveria fechar S2 e S4. Foi apagado no
mesmo dia, por execução contra as âncoras de `BASELINE_APROVADO.json`:

```
cafelana-v8   approved=False   p0_count=1
cafelana-v4   approved=False   p0_count=2
template-casa approved=True    p0_count=0
```

**Duas das três peças aprovadas pelo dono seriam bloqueadas.** A regra da casa é anterior a
qualquer gate: se a trava reprova o padrão aprovado, quem está errado é a trava.

Agravantes: emitia **P0** dentro de `verificar()`, que é o que a porta única chama em toda
peça — teria travado a produção inteira. E engolia exceção com `except: pass`, o fallback
silencioso expressamente proibido.

**O erro era de conceito, não de calibragem.** As duas âncoras são Impugnações ao Agravo
Interno: a cliente pede o *desprovimento* do agravo alheio, e a peça naturalmente escreve
"provimento" ao referir o pedido da parte contrária. O gate lia a coexistência dos dois
termos como incoerência. Em cafelana-v4 chegou a identificar a **União** — a parte adversa —
como cliente. Distinguir "a peça cita o pedido do adversário" de "a peça pede contra si
mesma" é exatamente a capacidade semântica que ele afirmava ter.

**O buraco de S2 e S4 permanece aberto e medido.** Buraco conhecido é dívida; gate que
bloqueia trabalho legítimo é dano, e vira waiver diário que contamina a confiança em todos
os outros gates do arquivo.

Nota sobre o julgamento: o juiz da onda 2 refutou parcialmente o ataque de falso positivo
alegando não ter reproduzido os 36,4% de bloqueio. Ele testou markdown, não os DOCX das
âncoras. A reprodução acima é do orquestrador, por execução.

---

## O canário: quando a catraca acusa rigor e chama de cegueira

O canário de mutação caiu de 40/35 para 39/34 e acusou *"algum gate ficou cego"*. Duas
causas, e só uma era defeito.

**Causa real, e minha.** A checagem de diversidade do F2A usava `json.dumps` direto; um
artefato destruído carregava valor não serializável, `TypeError` subia, e o validador
inteiro saía da contagem. O gate ficava cego exatamente no caso em que deveria acusar.
Corrigido com `_chave_comparavel`, que nunca levanta. *A lição é geral: a serialização
auxiliar de uma checagem jamais pode ser capaz de derrubar a checagem.*

**Causa de medida.** O `exploration_100_complete` saiu do censo porque **passou a
enxergar** — as 14 árvores reais são formulário, o veredito-base virou `warn`, e o canário
só muta gate cujo base é `pass`. A catraca acusava cegueira onde havia rigor novo.

A saída fácil era baixar o piso de 40/35 para 39/34. É precisamente assim que uma campanha
de melhoria destrói a proteção que deveria reforçar: um número por vez, sempre com bom
motivo. Em vez disso corrigiu-se a **medida**: `coberturaViva` e `provaDeQueSabeDizerNao`
passam a contar também o gate que reprova o artefato **real**, que é evidência mais forte
que reprovar o destruído.

Isso não afrouxa, e a razão é verificável: gate cego não reprova mutação nem reprova o
artefato real, logo não entra em nenhum dos dois conjuntos. Os pisos numéricos ficaram em
40 e 35, e há contraprova da medida nova dentro do próprio teste.

---

## Estado de validação

- **Baseline: APROVADO.** 89/89 suítes, 569 testes pytest, 60 subtestes, 43 regressões em
  script. Congelada: 83 suítes, 545 testes, 41 scripts.
- **Régua: APROVADO em 120,8 s**, após rebaseline de 4 arquivos com motivo escrito.
- **Âncoras aprovadas: intactas.**
- **Fail-closed preservado:** o caso Cafelana continua travado, revision 177.

## O que continua aberto, sem eufemismo

1. **S2 e S4 em zero.** Inverter o pedido ou trocar as partes sai protocolável. É o maior
   risco jurídico medido nesta campanha e ele não foi resolvido — a tentativa de resolvê-lo
   produziu um gate pior que o problema.
2. **Escore 0,147 contra alvo 0,80.**
3. **5.691 arquivos de caso e 759 binários versionados** no repositório do engine.
4. **F2A:** as duas checagens novas são P1 porque não existe no acervo uma única árvore de
   exploração genuína para servir de âncora de calibração. Sem esse exemplo positivo,
   qualquer promoção a P0 é arbitrária.
