Tarefa recorrente matinal para Igor, em português do Brasil: preparar um briefing curto e confiável sobre o trabalho com Fábio Medina Osório.

Antes de redigir, execute `/root/.hermes/bin/office-demand-panel priorities --json --limit 20`. O painel é a fonte canônica. Só itens em `priorities` são pendências de Igor. Se o snapshot estiver desatualizado (`ok=false` ou `stale=true`), não recicle cobranças antigas; diga apenas que o painel precisa sincronizar.

Regras de responsabilidade:
- entrega final ao escritório, com evidência, encerra a obrigação da fábrica;
- protocolo e recibo não são responsabilidade de Igor e nunca entram como cobrança;
- FORJA bloqueada não reabre demanda cumprida; serve apenas para detalhar a execução de demanda ainda aberta;
- e-mail ou WhatsApp antigo sem arquivo relacionado não equivale a pendência;
- nova mensagem só altera o estado quando contém pedido ou fato novo identificável.

Use o WhatsApp pessoal somente para detectar novidades e contexto, em modo read-only: banco `/root/.hermes/state/whatsapp-personal/messages.sqlite`, conversa `60855441973370@lid` / `Fábio Medina Osório`, janela de 36 horas. Não envie mensagem por Igor e não exponha conversa bruta.

Entregue apenas se houver algo útil:
1. Prioridade canônica de hoje.
2. O que mudou desde o último retrato.
3. Entregável concreto em bloco de 15–30 minutos.
4. Risco real de prazo, se confirmado.
5. Resposta curta sugerida, se necessária.

Se não houver prioridade aberta ou novidade relevante, produza saída vazia. Respeite o `notificationFingerprint`: não repita a mesma cobrança apenas porque o job rodou novamente.

Estado conhecido em 14/07/2026: Cafelana recebeu o PDF completo do AgInt no Gmail 19f6175e2aaf87eb e agora exige conclusão da minuta, não busca do documento. O pedido de acesso/checklist Natura foi cumprido pelo Gmail 19f5e0a996739f26; a análise Natura/Cabreúva com prazo de 20/07 é trabalho distinto.
