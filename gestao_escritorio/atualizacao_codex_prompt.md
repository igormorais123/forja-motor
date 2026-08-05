# Automação diária - Gestão de Demandas do Escritório Medina Osório

Rode no workspace:

`C:\Users\IgorPC\.claude\projects\Escritório fabio osório\fabricas de melhoria de petições`

Objetivo: atualizar o painel `gestao_escritorio\painel_gestao_escritorio.html` com demandas do escritório vindas de Gmail e WhatsApp/Hermes, marcar respostas já enviadas com conteúdo, recalcular urgências e acionar alerta no celular quando houver prazo crítico.

Regras:

1. Não enviar, arquivar, apagar ou rotular e-mails.
2. Não enviar mensagens de WhatsApp.
3. Não imprimir conversa bruta de WhatsApp no chat ou em relatório público; o painel deve conter resumo operacional sanitizado.
4. Usar o Gmail conectado para:
   - recebidos: `from:(medinaosorio.adv.br) after:2026/06/01 -in:trash -in:spam`;
   - enviados: `in:sent to:(medinaosorio.adv.br) after:2026/06/01 -in:trash -in:spam`.
5. Para cada pedido novo de e-mail:
   - criar/atualizar entrada em `gestao_escritorio\data\demandas.json`;
   - preencher título, prazo, resumo, próxima ação, pasta, anexos, status e resposta;
   - se ainda não existir pasta de trabalho, criar uma pasta com nome claro no diretório raiz e criar `COMANDO_DO_EMAIL.md`.
6. Para respostas enviadas:
   - marcar `respondidoComConteudo=true` somente se houver e-mail enviado com conteúdo de entrega ou anexo de peça;
   - registrar o ID do e-mail enviado em `emailsResposta`;
   - quando a peça chegou ao escritório, mas ainda existe insumo crítico, divergência multicanal ou validação pendente, manter `status=aberta` e registrar `etapaOperacional=entregue_para_revisao` em campo, comentário ou próxima ação;
   - marcar `status=cumprida` somente quando cobertura do pedido, insumos críticos, produto verificado, consistência da comunicação, evidência de entrega e releitura final dos canais estiverem aprovados;
   - não confundir `respondidoComConteudo=true` com `status=cumprida`.
7. WhatsApp/Hermes:
   - verificar `C:\Users\IgorPC\.hermes\bin\hermes-whatsapp-personal-access.ps1 -Action status`;
   - usar o chat `60855441973370@lid` como Fábio Medina Osório;
   - usar `168032760508457@lid` como candidato de contexto Igor/Hermes até Igor confirmar o contato exato "Igor hermes 2 chip";
   - extrair apenas demandas operacionais em resumo sanitizado, sem transcrever conversa bruta;
   - contar palavras-chave e áudios de demanda apenas nas mensagens recebidas;
   - separar mídia registrada de mídia materializada; `has_media=true` sem arquivo acessível não prova leitura;
   - áudio essencial sem arquivo acessível bloqueia o fechamento e exige recuperação/reenvio;
   - reler a conversa imediatamente antes da baixa para incorporar novas mensagens e confirmar se o material já foi enviado ao cliente.
8. Conciliação multicanal obrigatória antes de qualquer baixa:
   - enumerar pedidos, perguntas, correções e complementos do Fábio;
   - confrontar relatório, e-mail e WhatsApp por tese, risco, pendência e recomendação;
   - se um canal contradizer outro, registrar incidente e manter a demanda aberta até tratamento;
   - usar a cronologia real: `ainda não enviado`, `já enviado` ou `não verificado`;
   - aplicar `PROTOCOLO_FECHAMENTO_MULTICANAL_WHATSAPP_EMAIL.md`.
9. Depois de atualizar o JSON, rodar:
   `powershell -NoProfile -ExecutionPolicy Bypass -File gestao_escritorio\scripts\update_dashboard_local.ps1 -Mode Automation`
10. Se houver demanda aberta vencida ou com prazo até 48h, o script local acionará MacroDroid pelo `codex-phone.ps1`.
11. Ao final, deixar um resumo curto no próprio job e não vazar conteúdo sensível. O resumo deve separar: concluídas com evidência, abertas já entregues para revisão, abertas bloqueadas e inconsistências detectadas.
