# Quadro de qualidade — fechamento multicanal

Atualizado em: 22/07/2026  
Escopo: auditoria das demandas recentes do Fábio e controles de não recorrência

| Item | Severidade | Estado | Evidência/limite | Controle aplicado | Próxima ação |
|---|---:|---|---|---|---|
| Deltan — áudio indicado como fundamental sem arquivo acessível | P1 | aberto/bloqueado | evento de áudio existe, mas não há mídia materializada no acervo consultado | `MC-01`, `MC-08`, G2 | obter reenvio/recuperação, transcrever e confrontar com o parecer |
| CASO-17 — mensagem de WhatsApp contraditória ao relatório e e-mail auditados | P1 | incidente registrado | comunicação posterior qualificou como fortalecimento teses antes apontadas como riscos | `MC-02`, `MC-03`, `MC-07`, G3–G5 | não reutilizar a mensagem; eventual correção externa depende de autorização específica |
| CASO-04 — quatro áudios históricos indisponíveis | P2 | limite de cobertura | perguntas textuais e documentos foram tratados; conteúdo dos quatro áudios não foi recuperado | `MC-01`, G2 | preservar ressalva e recuperar apenas se o conteúdo voltar a ser material |
| CASO-07 — documentos essenciais ausentes | P1 | aberto/bloqueado | faltam documentos nominados no controle da demanda | `MC-08`, G2/G3 | receber e ingerir os documentos antes de liberar conclusão |
| Exportação sanitizada contabilizava palavras-chave e áudios enviados como se fossem recebidos | P1 | encerrado | laço agora examina somente entradas e separa caminho registrado, arquivo acessível e ausência | `MC-01`, `MC-06`; parse PowerShell e teste remoto aprovados | monitorar o próximo ciclo automático |
| Estados `respondida`, `entregue` e `cumprida` sem contrato multicanal explícito | P1 | encerrado | protocolo incorporado à automação, skill e guia; servidor rejeita baixa com insumo pendente | `MC-04`, `MC-05`; teste HTTP retornou `409` sem alteração de estado | monitorar o próximo uso real do botão |
| Conteúdo recebido no chat podia ser confundido com autoria intelectual do remetente | P1 | encerrado | mensagens longas importadas coexistem com instruções autorais curtas no mesmo canal | `MC-10`; `feedbackAssimilation` e regressões N4 aprovadas | aplicar o ledger no próximo retorno humano de uma peça |
| Mensagens de uma mesma rajada podiam ser interpretadas isoladamente | P1 | encerrado | o histórico mostra pedidos desenvolvidos por complementos sucessivos e mídias | `MC-09`; unidades conversacionais sanitizadas e gate de sobreposição | monitorar a próxima triagem real |
| Lote CASO-04, Estre, ERM e CASO-07 liberado sem a camada visual obrigatória | P1 | corrigindo | ESTRE, ERM e os dois produtos CASO-07 foram reconstruídos, revisados em 100 páginas e reenviados em 31/07/2026; CASO-04 permanece em tratamento segmentado por ordem expressa do último e-mail, sem recomposição integral prematura | `MC-12`; `gestao_escritorio/logs/QA_VISUAL_EMAIL_LOTE_2026-07-31.json`; e-mails `19fb887ca4ec3c0c`, `19fb88820599754e` e `19fb88881b936800` | concluir a camada visual de CASO-04 somente quando o fluxo segmentado autorizar a recomposição integral |
| Recibo CASO-07 N5 declarou QA visual 57/57 sem correspondente no resultado bruto do revisor | P1 | encerrado | o recibo anterior foi substituído por revisão visual independente das 72 páginas correntes, com hashes reais, render fresco e inspeção página a página; a página 47 suspeita foi confirmada como continuação válida de tabela | `MC-13`; `gestao_escritorio/logs/QA_VISUAL_EMAIL_LOTE_2026-07-31.json`; envio verificado em `19fb88881b936800` | preservar separação entre auditoria jurídica, fidelidade e QA visual nos próximos recibos |

## Critério de saída deste quadro

Um item só muda para `encerrado` quando a correção está aplicada, o teste preventivo passa e a
evidência do caso foi reconciliada. Documento criado sem mudança de rotina permanece `corrigindo`.

## Validações desta revisão

- parser do PowerShell: aprovado;
- exportação remota sanitizada: aprovada, sem corpo de conversa;
- testes automatizados: 15/15 aprovados;
- render do painel: aprovado;
- inspeção visual do painel e do detalhe Deltan: aprovada;
- gate HTTP real: `409` para conclusão com mídia/anexo pendente, com hash do estado inalterado;
- servidor local reiniciado e saudável na porta 8765.
- atualização manual completa: aprovada em 22/07/2026 às 01:53, com 41 demandas, 2 abertas e 39 cumpridas; WhatsApp conectado, Hermes saudável e exportação sanitizada atualizada.
