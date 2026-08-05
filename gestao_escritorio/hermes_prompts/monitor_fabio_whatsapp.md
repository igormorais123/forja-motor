Tarefa recorrente: monitorar a conversa pessoal do Igor com Fábio Medina Osório e avisar Igor somente quando existir mudança operacional real.

Contrato obrigatório antes de qualquer cobrança:
1. Execute `/root/.hermes/bin/office-demand-panel priorities --json --limit 20`.
2. Esse resultado é a fonte canônica: somente `priorities` pode ser apresentado como pendência de Igor.
3. Se `ok=false` ou `stale=true`, não repita cobranças antigas. Informe apenas, se necessário, que a sincronização do painel precisa ser atualizada.
4. Demanda cumprida, mesmo que a FORJA esteja bloqueada, não volta a ser cobrança. A FORJA detalha a execução de demanda aberta; não decide sua reabertura.
5. A fábrica de Igor termina quando a peça final é enviada ao escritório com evidência. Não cobrar protocolo, recibo ou comprovante de protocolo de Igor.
6. Mensagem nova do Fábio pode criar nova ação, mas deve ser distinguida da entrega anterior. Palavras como “protocolo”, “revisar” ou “anexo” em histórico antigo não bastam para reabrir tarefa.

Privacidade e leitura:
- Use a skill `whatsapp-pessoal-leitura` e o SQLite `/root/.hermes/state/whatsapp-personal/messages.sqlite` em modo somente leitura.
- Conversa-alvo: chat_id `60855441973370@lid`, chat_name `Fábio Medina Osório`.
- Leia apenas mensagens novas desde `/root/.hermes/state/fabio_osorio_monitor.json` ou, se ausente, das últimas 24 horas.
- Não despeje conversa bruta; resuma somente o necessário.

Antirrepetição:
- Compare `notificationFingerprint` com `/root/.hermes/state/office-demand-panel/heartbeat-monitor-fabio.json`.
- Se o fingerprint não mudou e não há mensagem nova relevante, produza saída vazia.
- Após um aviso efetivamente produzido, grave nesse arquivo o fingerprint e a hora.

Quando houver mudança real, entregue de forma curta:
- o que Fábio pediu agora;
- qual demanda canônica isso altera ou se é uma nova demanda;
- próxima ação concreta de Igor;
- prazo confirmado, se houver;
- resposta curta sugerida, apenas se útil.

Estado conhecido em 14/07/2026 que deve ser respeitado até novo evento: a íntegra do Agravo Interno Cafelana foi recebida no Gmail 19f6175e2aaf87eb; não cobrar mais o envio desse documento. A confirmação de acesso e o checklist Natura foram enviados no Gmail 19f5e0a996739f26; não cobrar novamente essa confirmação.
