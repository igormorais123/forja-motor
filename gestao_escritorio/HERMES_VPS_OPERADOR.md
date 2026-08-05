# Operador Hermes VPS - gestão de demandas do escritório

Este painel é a fonte operacional das demandas do escritório Fabio Medina Osório.

## Regra de privacidade

Usar somente resumo operacional. Não despejar conversa bruta de WhatsApp no painel, no chat ou em relatórios.

## Fonte de verdade e limite da fábrica

O PC local continua sendo a fonte principal. A VPS recebe um retrato sanitizado e envia mudanças por fila para o PC local importar.

- Só demandas com `status != cumprida` são acionáveis para cobrança.
- A FORJA detalha execução e bloqueios, mas não reabre demanda já baixada na gestão.
- A responsabilidade de Igor termina quando a peça final é enviada ao escritório com evidência. Protocolo e recibo não são pendência da fábrica.
- Snapshot com mais de 180 minutos é considerado desatualizado: o Hermes deve pedir sincronização e não repetir cobranças antigas.

## Comando na VPS

`/root/.hermes/bin/office-demand-panel`

## Consultar prioridades

`/root/.hermes/bin/office-demand-panel priorities --limit 5`

Usar quando Igor perguntar no WhatsApp coisas como:

- "quais demandas do escritório são prioridade?"
- "o que está urgente para o Fabio?"
- "o que preciso fazer primeiro?"

## Consultar estado geral

`/root/.hermes/bin/office-demand-panel status`

## Registrar comentário em uma demanda

`/root/.hermes/bin/office-demand-panel comment --id ID_DA_DEMANDA --text "comentario operacional"`

## Criar demanda recebida por áudio, WhatsApp ou orientação verbal

`/root/.hermes/bin/office-demand-panel add-task --title "titulo" --summary "resumo operacional" --urgency alta`

## Marcar mudança de status

`/root/.hermes/bin/office-demand-panel status-set --id ID_DA_DEMANDA --status cumprida --note "como foi cumprida"`

## Fila remota

`/root/.hermes/bin/office-demand-panel pending --json`

Se houver itens pendentes, aguardar o PC local sincronizar. Depois de importados, os itens são arquivados automaticamente.

## Atualização local

No PC local, o botão `Atualizar agora`, a rotina automática a cada 30 minutos e o script `gestao_escritorio\sincronizar_hermes.ps1` importam a fila da VPS e exportam as prioridades atualizadas. O instalador da rotina é `scripts\install_sync_schedule.ps1`.

## Continuidade e rollback (14/07/2026)

- A ponte PC→VPS usa o alias SSH `hermes` por Tailscale; acesso direto a `root@2.25.174.138:22` é bloqueado.
- O indexador da FORJA usa `index_project_folder` (manifesto de caminhos e tamanhos), evitando ZIP integral do acervo.
- Backups locais anteriores à correção: `C:\Users\IgorPC\.hermes\backups\office-sync-20260714`.
- Backups remotos anteriores à correção: `/root/.hermes/backups/office-sync-20260714`.
- Para rollback, restaurar os arquivos correspondentes desses diretórios e reinstalar a versão do operador com `scripts\hermes_bridge.py --ssh-alias hermes --install sync`.

## Painel web para celular (08/07/2026, atualizado: sem senha)

Retrato do painel em modo leitura publicado na VPS a cada sincronização (botão Atualizar agora, rotina das 9h ou `sincronizar_hermes.ps1`).

- URL (link secreto, sem senha): https://escritorio.2.25.174.138.nip.io/p-yjp3RHTnCnaMntEV/
- A raiz do site devolve 404; a proteção é o caminho não adivinhável. Se o link vazar para alguém indevido, trocar o token: renomear a pasta em `/var/www/escritorio-painel/`, ajustar `REMOTE_WEB_DIR` em `scripts/hermes_bridge.py` e o link no `ABRIR_GESTAO_ESCRITORIO.html`.
- Arquivo para enviar por WhatsApp: `gestao_escritorio\PAINEL_ESCRITORIO_MEDINA_OSORIO.html` (autônomo, com dados e logo embutidos; regenerado a cada atualização do painel).
- Publicação: `scripts/hermes_bridge.py` → `publish_remote_panel` envia o HTML para a VPS.
- Nginx: `/etc/nginx/sites-available/escritorio-painel.conf` (HTTPS Let's Encrypt, no-index).
- No celular só leitura; ações (comentar, concluir, criar tarefa) pelo painel do PC ou pelo Hermes no WhatsApp (`office-demand-panel`).
