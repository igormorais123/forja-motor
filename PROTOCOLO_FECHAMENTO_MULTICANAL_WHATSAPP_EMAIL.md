# Protocolo de fechamento multicanal — WhatsApp, e-mail e painel

Versão: `1.0`  
Data: 22/07/2026  
Classificação: controle operacional interno  
Escopo: demandas do escritório recebidas ou complementadas por WhatsApp/Hermes e e-mail

## 1. Finalidade

Impedir que uma demanda seja considerada concluída quando apenas parte do pedido foi lida,
executada ou comunicada. O painel é um quadro de comando; o fechamento depende da conciliação das
fontes vivas e das evidências arquivadas.

Este protocolo não autoriza envio externo. Gmail e WhatsApp permanecem em leitura e triagem, salvo
autorização específica para a mensagem e o destinatário.

## 2. Definições que não podem ser confundidas

| Estado | O que prova | O que não prova |
|---|---|---|
| `identificada` | existe pedido concreto e titular definido | que todos os insumos chegaram |
| `insumos_parciais` | parte do material foi lida | que mídia apenas registrada foi recuperada |
| `em_execucao` | há trabalho efetivo em curso | que existe produto entregável |
| `entregue_para_revisao` | o escritório recebeu produto identificável | que todas as fontes críticas foram lidas ou que houve protocolo |
| `respondida` | houve comunicação de retorno | que a obrigação material foi cumprida |
| `cumprida` | todos os gates aplicáveis abaixo passaram | que o cliente ou tribunal recebeu, salvo se isso era o pedido expresso |
| `bloqueada` | falta insumo material, decisão ou acesso necessário | fracasso da execução; o bloqueador deve ser nominado |

No schema atual do painel, apenas `aberta` e `cumprida` são estados finais reconhecidos pela interface.
Assim, `insumos_parciais`, `em_execucao`, `entregue_para_revisao` e `bloqueada` devem permanecer com
`status=aberta` e ser registradas em `etapaOperacional`, comentário manual ou próxima ação até a
evolução do schema.

`respondidoComConteudo=true` e `status=cumprida` são decisões independentes. Uma mensagem pode
responder sem entregar; uma peça entregue ao escritório pode encerrar a responsabilidade interna sem
provar protocolo judicial.

## 3. Ledger sanitizado obrigatório por demanda

Antes de executar, criar ou atualizar um registro interno que contenha somente metadados necessários:

- identificador da mensagem ou e-mail;
- data e hora com fuso;
- direção (`recebida` ou `enviada`);
- canal e remetente operacional;
- tipo (`texto`, `áudio`, `PDF`, `DOCX`, imagem ou link);
- classificação (`pedido`, `complemento`, `correção`, `aprovação`, `entrega` ou `contexto`);
- estado de materialização (`acessível`, `ausente`, `corrompido` ou `não aplicável`);
- artefato ou demanda vinculada;
- tratamento dado e evidência.

Não copiar conversa bruta para o painel, relatório público ou chat. O conteúdo necessário deve ser
resumido de forma fiel, preservando números, datas, condicionantes e perguntas.

## 4. Gates de fechamento

### G1 — cobertura do pedido

- Enumerar cada pedido, pergunta, correção e entrega mencionada pelo Fábio.
- Ligar cada item a um artefato, resposta ou bloqueador.
- Pergunta sem resposta e correção sem tratamento impedem `cumprida`.

### G2 — materialização de mídia e anexos

- Evento `has_media=true` não significa conteúdo lido.
- Confirmar que o arquivo existe, abre e corresponde ao evento.
- Áudio qualificado como essencial, fundamental ou necessário permanece bloqueador enquanto o arquivo
  não estiver acessível e transcrito/revisado.
- É proibido inferir o teor de áudio ausente pelo texto adjacente.
- Se a recuperação falhar, registrar o identificador do evento, pedir reenvio pelo canal autorizado e
  manter a demanda aberta ou `entregue_para_revisao` com ressalva material.

### G3 — integridade jurídica e factual do produto

- Vincular as proposições materiais às fontes efetivamente lidas.
- Separar melhoria editorial de validação jurídica: documento mais curto ou visualmente superior não é,
  por isso, “juridicamente corrigido”.
- Tese nova ou fortalecida exige lastro e decisão autoral registrada.
- Bloqueador material não pode ser apagado por confiança de estilo ou por aprovação visual.

### G4 — cronologia do envio ao cliente

Antes de redigir e-mail ou WhatsApp, confirmar o último evento relevante:

- `ainda não enviado`: orientar revisão anterior ao envio;
- `já enviado`: registrar análise posterior e indicar correção, complemento ou risco residual;
- `não verificado`: não afirmar nenhuma das duas situações.

Depois de o Fábio informar que já enviou o documento, é proibido escrever “antes de enviar ao
cliente”. O texto deve refletir a cronologia real.

### G5 — consistência entre canais

Montar uma matriz curta antes de qualquer retorno:

| Tema material | Relatório auditado | E-mail | WhatsApp | Resultado |
|---|---|---|---|---|
| tese, risco ou pendência | posição e lastro | posição comunicada | posição comunicada | `coerente`, `divergente` ou `não tratado` |

Uma mensagem posterior não pode inverter risco ou conclusão registrados no relatório/e-mail sem nova
fonte e decisão expressa. Divergência detectada bloqueia o fechamento, exige registro de incidente e,
se houver autorização, correção objetiva no mesmo canal.

### G6 — evidência de entrega

Registrar:

- ID do e-mail ou mensagem de entrega;
- nomes e hashes dos anexos, quando aplicável;
- destinatário interno autorizado;
- data e hora;
- classificação da versão (`internal_review_only`, `protocolável` ou `externa`);
- pendências declaradas.

Não exigir recibo judicial quando a responsabilidade de Igor termina com a entrega ao escritório.

### G7 — releitura de alta d'água

Imediatamente antes do fechamento:

1. atualizar Gmail e WhatsApp;
2. comparar a última entrada com o retrato usado no início;
3. incorporar nova mensagem ou reabrir a triagem;
4. conferir que nenhuma mídia recebida permanece sem materialização;
5. só então atualizar o painel.

Contagem de mensagens não substitui leitura de cada evento relevante.

## 5. Critério lógico de `cumprida`

Uma demanda só pode receber `status=cumprida` quando:

`cobertura do pedido` **e** `insumos críticos acessíveis` **e** `produto verificado` **e**
`comunicação coerente` **e** `evidência de entrega` **e** `releitura final dos canais` forem verdadeiros.

Se qualquer termo for falso ou não verificado, manter `status=aberta`, registrar a etapa intermediária
ou `bloqueada` e nomear a única ação que libera o próximo passo.

O servidor local aplica um escudo mínimo determinístico: a rota de conclusão rejeita a baixa quando
`externosPendentes=true`, quando o número de anexos diretos materializados é inferior ao esperado ou
quando `etapaOperacional` indica insumos parciais, entrega para revisão ou bloqueio. Esse escudo não
substitui os gates semânticos de cobertura, cronologia e consistência entre canais.

## 6. Aplicação imediata aos incidentes auditados em 21–22/07/2026

- CASO-08: produto entregue ao escritório, mas áudio indicado como fundamental não está materializado;
  manter aberto até recuperação/reenvio e confronto do conteúdo com o parecer.
- CASO-04: perguntas textuais e documentos foram tratados; quatro eventos antigos de áudio não estão
  recuperáveis no acervo atual. Registrar limite de cobertura, sem afirmar leitura integral dos áudios.
- CASO-17: relatório e e-mail apontaram riscos jurídicos, mas mensagem posterior de WhatsApp
  qualificou como fortalecimento algumas das mesmas teses. Registrar divergência, impedir que o padrão
  seja reutilizado e só comunicar correção com autorização específica.
- CASO-07: manter bloqueada por documentos materiais ausentes; estilo ou pesquisa não suprem o acervo.

## 7. Checklist de encerramento

- [ ] Todos os pedidos e complementos foram enumerados?
- [ ] Toda mídia relevante existe e foi efetivamente aberta?
- [ ] Áudios relevantes foram transcritos e confrontados com a tarefa?
- [ ] O produto passou pelos gates jurídico, factual e visual aplicáveis?
- [ ] A cronologia distingue análise anterior e posterior ao envio ao cliente?
- [ ] E-mail, WhatsApp, relatório e painel comunicam a mesma conclusão?
- [ ] A entrega interna possui ID e anexos identificáveis?
- [ ] Gmail e WhatsApp foram relidos imediatamente antes da baixa?
- [ ] `respondida`, `entregue` e `cumprida` foram usadas sem equivalência automática?
- [ ] O bloqueador residual está explícito e acionável?
