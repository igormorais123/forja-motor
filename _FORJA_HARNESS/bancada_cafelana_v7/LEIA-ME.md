# Bancada Cafelana V7 — teste independente de modelos

Teste encomendado pelo titular em 27/07/2026. Seis modelos de fronteira recebem o mesmo caso real e escrevem, cada um, a sua versão da mesma peça. Depois são avaliados por regra e por juízes cegos.

Isto **não é** um ciclo da FORJA. É uma bancada isolada, em pasta própria, que reaproveita os gates da fábrica como instrumento de medida. Nenhuma peça produzida aqui entra em caso, em estado ou em entrega.

## O que se está medindo

Potencial bruto de trabalho jurídico: dado o mesmo material de um caso vivo e a mesma tarefa, quanto cada modelo entrega de peça protocolável — e, sobretudo, quanto inventa pelo caminho.

## A tarefa

Escrever a **V7** da impugnação ao agravo interno no AREsp nº 2.698.443/DF (STJ, Primeira Turma, Rel. Min. Regina Helena Costa), a partir da V6 entregue em 27/07/2026.

O alvo foi escolhido por três razões: é trabalho real e corrente, tem V6 documentada com pendências declaradas por escrito, e tem determinações do titular registradas — o que permite medir obediência, e não só eloquência.

## Participantes

| id | família | rota | endereço |
|---|---|---|---|
| `opus-5` | anthropic | assinatura Claude Max | alias `opus` |
| `fable-5` | anthropic | assinatura Claude Max | alias `fable` |
| `sol-5.6` | openai | OpenRouter | `openai/gpt-5.6-sol` |
| `luna-5.6` | openai | OpenRouter | `openai/gpt-5.6-luna` |
| `grok-4.5` | xai | OpenRouter | `x-ai/grok-4.5` |
| `kimi-k3` | moonshot | OpenRouter | `moonshotai/kimi-k3` |

Assinatura tem prioridade sobre API paga, conforme a regra da casa: os dois modelos Anthropic rodam pelo Claude Code autenticado, sem chave e sem custo marginal. Os quatro restantes não existem na assinatura e vão por OpenRouter.

**Ressalva sobre o `kimi-k3`:** ele foi retirado do registro de produção da FORJA em 26/07/2026, por decisão do titular, após reprovar a bancada jurídica. Participa aqui a pedido, para efeito comparativo. O resultado desta bancada, por si só, não reabre aquela decisão.

**Ressalva sobre a família K2:** permanece vedada por ordem expressa. O bloqueio é executável, não documental — `modelo_remoto_proibido()` recusa qualquer variante, inclusive sufixos que ainda não existiam quando a lista foi escrita.

## Blindagens contra trapaça

O risco de um teste assim não é o modelo mentir: é o teste medir outra coisa.

**No insumo.** O dossiê é congelado, hasheado e idêntico para todos. Nenhum participante recebeu um documento a mais. O SHA-256 do prompt efetivo fica no `META.json` de cada execução, e `bancada_dossie.py --verificar` reconfere a integridade a qualquer momento.

**No isolamento.** A rota de assinatura roda com `--tools ""`. Sem isso, o Claude leria o disco, acharia a V6 no acervo — e acharia as peças dos rivais. Cada execução escreve apenas na própria pasta; em nenhum momento um participante vê saída de outro.

**Na identidade.** Quem consumiu tokens é lido do envelope, não da promessa: `modelUsage` na assinatura, campo `model` na resposta HTTP. Provedor que entrega modelo diferente do pedido fica marcado como divergência.

**No truncamento.** `finish_reason` diferente de `stop` marca a peça como incompleta. Resposta cortada não pode ser lida como concisão.

### Duas falhas que estas blindagens pegaram na primeira execução

Nenhuma das duas foi falha de modelo. As duas teriam produzido um relatório errado.

**O alias `opus` não é o Opus 5.** A primeira execução do participante `opus-5` usou `--model opus`, e o envelope reportou `claude-opus-4-8`. O gate de identidade acusou a divergência e a execução foi descartada — está preservada em `execucao_descartadas/`, porque a peça não era ruim, apenas não era do modelo que a bancada se propôs a medir. O endereço correto, confirmado por sonda, é o id canônico `claude-opus-5`; `opusplan` resolve para `claude-sonnet-4-6` e `opus-5` não é reconhecido. Alias curto é conveniência de sessão interativa e não serve para medição.

**O `--output-format json` devolve só o último turno.** Uma peça longa atravessa mais de um turno do Claude Code, e o campo `result` traz apenas o final: a segunda execução do `opus-5` produziu 36 mil tokens de saída e devolveu 10 KB começando no meio de uma palavra. Medir isso seria medir o harness. A rota de assinatura passou a capturar por `--output-format stream-json`, concatenando todos os blocos de texto na ordem. Os dois participantes de assinatura foram reexecutados com o mesmo método, para que a comparação entre eles não dependesse de qual teve sorte de caber em um turno.

**Na avaliação.** Ver abaixo: o que é regra é medido por código, e o que é ofício é julgado às cegas, com controle de posição e âncora conferida.

## Como a avaliação funciona

### Camada 1 — determinística (`bancada_avaliar.py`)

Roda em código. Nenhum participante tem influência sobre ela.

- **Integridade (40 pontos)** — toda autoridade citada é confrontada com o ledger fechado do dossiê. Ausente e marcada `[A CONFERIR]` é honestidade; ausente e afirmada como verificada é o pecado capital.
- **Obediência (20)** — cinco canários. Cada um é um erro **real** que a V6 encontrou e corrigiu: tratar de prevenção, pedir conhecimento parcial, citar o precedente autoderrotante, apoiar-se no fundamento superado pela Corte Especial, citar fala de desembargador sem ata. Não são armadilhas inventadas para reprovar — são as pedras onde já se tropeçou neste caso. Quem tropeça de novo não leu o dossiê.
- **Retenção (20)** — as seis conquistas da V6 sobreviveram? Perder o que já estava resolvido é regressão, ainda que a prosa melhore.
- **Pendências (12)** — as cinco pendências declaradas foram fechadas ou explicadas?
- **Ofício (8)** — `forja_lastro`, `forja_estilo_humano` e `forja_verificador` sem adaptação, mais a entrega do relatório contratado.

**Tetos.** Média ponderada perdoa o imperdoável, então há teto: peça que afirma autoridade fora do dossiê não passa de 60; canário grave acionado limita a 65; ausência do relatório contratado limita a 80. Escrever bem o resto não compensa inventar precedente.

**Exceção documentada.** O placeholder da data do protocolo é legítimo em revisão interna — a própria V6 o tem. Penalizá-lo seria punir a peça por não inventar a data de um ato que ainda não ocorreu.

### Camada 2 — julgamento cego (`bancada_juizes.py`)

Três famílias julgam: `opus-5` (anthropic), `sol-5.6` (openai), `grok-4.5` (xai). Seis critérios de 0 a 10, ranking completo e escolha da única peça que o juiz protocolaria hoje.

- As peças viram `P1..Pn` em ordem sorteada; o mapa vai para **fora do workspace**, em `~/.forja_ar_secrets/`.
- Antes de cegar, uma varredura procura peça que se identifique. Cegamento sobre texto que se denuncia é teatro.
- Cada juiz julga **duas vezes**, com a ordem de apresentação invertida. Ranking que muda ao inverter mede viés de posição, e isso vira número no relatório.
- O juiz precisa **transcrever** um trecho literal da peça que elegeu. Se o trecho não existe naquela peça, o voto é anulado — é o teste de que o juiz leu o que julgou.
- **Auto-preferência é medida, não presumida.** Todo juiz aqui também é participante; o relatório registra quanto cada família favorece a si mesma.

## Como rodar

```powershell
python bancada_dossie.py                    # congela o insumo e extrai o ledger fechado
python bancada_dossie.py --verificar        # reconfere a integridade do dossiê
python bancada_executar.py --todos          # despacha a tarefa
python bancada_avaliar.py                   # camada determinística
python bancada_juizes.py --cegar --julgar --consolidar
```

## Estrutura

```
protocolo/     PROMPT_V7.md, DOSSIE.md (congelado), DOSSIE_LEDGER.json
execucao/<id>/ SAIDA.md + META.json (hashes, custo, identidade, truncamento)
execucao_descartadas/  execuções inválidas, preservadas com o motivo
cego/          P1..Pn.md + CEGAMENTO.json (o mapa NÃO está aqui)
avaliacao/     DETERMINISTICA.json, juizes/, JUIZES_CONSOLIDADO.json, QUADRO_FINAL.json
RELATORIO_BANCADA_V7.md              leitura de conjunto e conclusões
RESULTADOS_DETALHADOS_BANCADA_V7.md  todos os números, gerados dos artefatos
```

## Os dois documentos de saída

`RELATORIO_BANCADA_V7.md` é a **narrativa**: o que o teste mostrou, o que decidiu a comparação, o que fazer com isso.

`RESULTADOS_DETALHADOS_BANCADA_V7.md` é a **prova**: telemetria de cada execução, canários e retenção item a item, os seis votos brutos com nota por critério, âncoras, auto-preferência, estabilidade de posição e as suítes do harness na mesma rodada. É emitido por `bancada_registro.py` a partir dos artefatos — nenhum número é transcrito à mão, porque duzentos números copiados criam uma segunda fonte da verdade que diverge da primeira na próxima reexecução.

Regerar depois de qualquer etapa: `python bancada_registro.py`.

## Limites deste teste

Uma peça por modelo é **amostra de tamanho um**. Diferença pequena entre dois participantes não distingue modelo de sorte de execução; diferença grande, sobretudo em invenção de autoridade, distingue.

Os gates medem o que é verificável por regra. Nenhum deles julga se um precedente realmente sustenta a tese que lhe atribuíram — isso continua exigindo leitura jurídica humana, aqui como na produção.

E nenhuma peça desta bancada é protocolável. São exercícios de comparação, produzidos sem acesso aos autos e sem revisão humana.
