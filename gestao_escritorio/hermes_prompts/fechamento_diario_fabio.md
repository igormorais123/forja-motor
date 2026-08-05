Tarefa recorrente de fechamento diário para Igor: registrar somente pendências reais e a primeira ação do dia seguinte.

Gate obrigatório: execute `/root/.hermes/bin/office-demand-panel priorities --json --limit 20`. Esse retrato, quando atual, prevalece sobre inferências do WhatsApp, e-mails antigos e estados internos da FORJA. Somente itens retornados em `priorities` podem ser cobrados.

Se `ok=false` ou `stale=true`, não liste demandas antigas; reporte apenas falha de sincronização se isso exigir ação. Demanda cumprida com evidência não reabre porque ainda há revisão, protocolo, recibo ou estado técnico bloqueado. A responsabilidade de Igor termina no envio da peça final ao escritório; protocolo e recibo são do responsável pelo protocolo.

Leia em modo somente leitura as mensagens do dia no banco `/root/.hermes/state/whatsapp-personal/messages.sqlite`, conversa `60855441973370@lid`. Use mensagens novas apenas para identificar evento novo; não transcreva conteúdo bruto e não envie nada por Igor.

Formato, apenas quando houver pendência real:
- o que ficou aberto no painel canônico;
- o que mudou hoje;
- uma ação que não pode dormir;
- primeiro bloco recomendado para amanhã;
- rascunho curto de resposta, se necessário.

Não repita o mesmo conjunto se `notificationFingerprint` estiver inalterado e não houver nova mensagem relevante. Se nada mudou, produza saída vazia.

Estado conhecido em 14/07/2026: o Agravo Interno completo da Cafelana já foi recebido no Gmail 19f6175e2aaf87eb; não cobrar sua obtenção. O acesso e checklist Natura já foram confirmados pelo Gmail 19f5e0a996739f26; não cobrar novamente.
