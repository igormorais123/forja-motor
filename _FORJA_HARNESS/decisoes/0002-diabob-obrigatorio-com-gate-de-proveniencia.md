# 0002 — Diabob obrigatório no conselho, aferido por proveniência e não por prosa

- Status: Aceita — promovida a exigência dura do contrato em 07/08/2026
- Data: 06-07/08/2026
- Quem decidiu: Igor

## Contexto

O conselho obrigatório da fábrica tinha duas vozes desde 09/07/2026: Helena e Cícero.
Em 06/08/2026 o Igor determinou uma terceira: o **Diabob**.

Havia um problema imediato, declarado na mesma sessão: `forja_conselho.py` valida os
pareceres de Helena e Cícero, e a obrigatoriedade do Diabob era **só texto**. A regra da
casa é explícita sobre esse estado — instrução escrita disputa atenção com o resto do
prompt e perde, e por isso a identidade dos atos recursais, inviolável desde 11/07, foi
violada em dois clientes antes de virar o gate S6. Regra escrita que não pega vira gate.

Havia também um erro de classificação meu a corrigir: o catálogo marcava `diabob` como
`status: preterida`, em favor da skill `forja-red-team`. Estava errado. A
`forja-red-team` conduz as nove perguntas **por dentro**, com o mesmo modelo que
escreveu; o Diabob traz o contraditório de **outra família**. O próprio executor explica
por quê: red team feito pelo mesmo modelo que produziu a análise repete os próprios
pontos cegos com voz mais dura.

## Decisão

**O que o gate afere é a proveniência da chamada, não o texto do parecer.** Prosa
dizendo "passou pelo Diabob" é exatamente o que não prova nada — e é o formato que uma
esteira apressada produz sozinha.

`forja_diabob.py --saida F4_PARECER_DIABOB.json` grava o **recibo** com modelo, família,
provedor, rota degradada, tempo e custo, ao lado do parecer. `forja_conselho.py` ganhou o
gate `diabob_present` (L-C4), chamado por `forja_run.py` em todo F4, que reprova:

| Situação | Veredito |
|---|---|
| recibo real, de outra família | `pass` |
| **não declarado** | `unknown` + P1 — a obrigatoriedade não fica comprovada |
| prosa em vez de recibo | `fail` — sem proveniência não se distingue contraditório de eco |
| família `anthropic`, a mesma que produz a peça | `fail` — isso é eco, não red team |
| recibo com parecer de casca | `fail` |
| rota degradada declarada | `pass` + P1 — rodar pela rota paga não invalida, mas não passa calado |

`unknown` **não é `pass`**: é a recusa de atestar o que não se viu. Foi escolhido em vez
de P0 para não reprovar retroativamente todo caso anterior à ordem — o mesmo critério
dos gates S2, S4, S6 e S7, onde caso sem declaração não recebe veredito.

## Consequências

- Passa a valer: todo F4 gera `F4_PARECER_DIABOB.json` pelo comando, não à mão.
- Fica proibido: atestar o contraditório por prosa, e usar a mesma família do produtor.
- O gate roda na rota real (`forja_run.py`), não numa rota lateral — a Lição 89 é que
  gate instalado onde ninguém passa é gate nenhum.
- Aceita-se perder: a reprovação dura de casos antigos. Eles ficam `unknown`, visíveis.
- A assinatura de `validar_conselho` ganhou `diabob=None` opcional, para não quebrar
  chamador antigo; a regressão cobre isso.

## Promoção a exigência dura do contrato (07/08/2026)

O Igor autorizou promover. `diabob_opinion` entrou em `requiredOutputs` e
`diabob_present` em `requiredGates`, nos dois contratos da fase — `phase_contracts/F4.json`
e `phase_contracts_n4/F4.json`.

**Correção de fato registrada aqui.** A versão anterior deste ADR dizia que a promoção
derrubaria "qualquer F4 em curso" e que até lá a ausência ficaria apenas visível como
`unknown`. **Estava errado sobre a rota real.** `forja_run._recompute_conselho` reprova
todo gate do conselho cujo valor recomputado não seja `pass` — e `unknown` não é `pass`.
Desde 06/08 a fase já parava; o que faltava era a mensagem dizer o que produzir. Antes:
`conselho obrigatório reprovado na recomputação (diabob_present)`. Agora a ausência é
barrada antes, em `saídas obrigatórias ausentes: diabob_opinion`.

O que a promoção muda de verdade, então, é **onde** e **como** o caso é barrado, não
**se**. `unknown` continua não sendo `pass`; a promoção é adicional, não troca.

Medido no acervo em 07/08/2026: **9 de 9 tentativas F4 históricas não têm o artefato.**
Nenhuma delas é revalidada — o contrato vale para promoção nova, e tentativa já promovida
não volta ao portão. Elas aparecem como `unknown` no censo de recomputação
(`forja_recomputo_censo.py`, que passou a procurar o recibo), que é o veredito honesto.

Também foram ligados dois pontos de entrada que conheciam Helena e Cícero e não o Diabob:
o censo acima e `forja_import_audited_cycle.py`, que agora reconhece o arquivo pelo nome.

**Kimi K3 não entrou na lista de proibidos.** Ele aparece na assinatura do Cursor
(`kimi-k3-high`) e foi retirado do registro da FORJA em 26/07/2026 por decisão do
titular, depois de reprovar a bancada jurídica. Em 07/08/2026 o Igor decidiu **não
bani-lo** — "pode ser útil". Ele segue fora do registro de modelos da FORJA e disponível
na conta; usá-lo em produção da esteira exigiria reinstalá-lo no registro, o que é
decisão nova e não está tomada.

## Critério de reabertura

Caso em que o gate reprove contraditório legítimo, ou evidência de que a verificação por
família deixa passar eco real — por exemplo, um provedor que reporte família errada.
