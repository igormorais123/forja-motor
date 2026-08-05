# Gestão do Escritório Medina Osório

Central local de demandas da fábrica de petições. A fonte de verdade é `data/demandas.json`; os HTMLs são retratos regeneráveis.

## Abrir

- Entrada principal: `..\ABRIR_GESTAO_ESCRITORIO.html`.
- Inicializador seguro: `iniciar_painel_gestao_escritorio.ps1`.
- Painel vivo: `http://127.0.0.1:8765/`.
- Retrato offline: `painel_gestao_escritorio.html`.
- Retrato externo, somente leitura: `PAINEL_ESCRITORIO_MEDINA_OSORIO.html`.

O inicializador chama `scripts/ensure_server.ps1`, valida `/api/health`, inicia o servidor com o caminho corretamente escapado e instala a tarefa de usuário `Medina Osorio - Gestao Escritorio Watchdog`. A tarefa roda no logon e a cada dez minutos; se o processo cair, restaura o serviço sem abrir janela.

## Arquitetura

1. `data/demandas.json`: fila operacional canônica.
2. `data/intervencoes_manuais.json`: comentários, correções e overrides com evidência.
3. `data/forja_status.json`: sidecar que vincula cada demanda ao estado, gates, bloqueios, QA, artefatos e evidência da FORJA.
4. `scripts/sync_forja_gestao.py`: reconciliação aditiva entre estados FORJA, auditorias manuais e cumprimento comprovado na gestão.
5. `scripts/update_dashboard_local.ps1`: ciclo Gmail, entregas, WhatsApp sanitizado, Hermes, FORJA, alertas e render.
6. `scripts/dashboard_enrichment.py`: campos derivados de interface, links Gmail, datas a conferir, qualidade da fila e conflitos Gestão × FORJA.
7. `templates/dashboard.html`: interface das vistas Hoje, Prazos, Demandas, Integrações e Entregas.
8. `scripts/render_dashboard.py`: injeta o retrato nos HTMLs autocontidos.
9. `scripts/server.py`: API local, atualização assíncrona e ações manuais.

Persistência crítica usa troca atômica por `scripts/office_io.py`. Uma interrupção durante a gravação preserva o último JSON ou HTML completo.

## Atualização e observabilidade

- `POST /api/update`: inicia um ciclo em segundo plano e responde imediatamente.
- `GET /api/update-status`: estado e histórico dos últimos 30 ciclos.
- `GET /api/health`: diagnóstico leve, sem alterar arquivos.
- `GET /api/data`: retrato completo, também somente leitura.
- `data/runtime_status.json`: processo e ciclo atual.
- `data/update_history.json`: duração, resultado e resumo dos ciclos.

Uma segunda atualização recebe HTTP `409` enquanto a primeira estiver rodando. O painel consulta o estado até o encerramento e continua utilizável durante a varredura.

## Integração FORJA

- A gestão é autoridade para existência da demanda, prioridade, prazo e evidência concreta de entrega.
- A FORJA é autoridade para fase produtiva, gates, bloqueios, artefatos, hashes e QA visual.
- O sidecar faz a junção por `demandId`; não altera `demandas.json` nem os estados históricos da FORJA.
- Uma demanda cumprida com evidência pode ser encerrada como `fulfilled_by_reconciliation` mesmo quando não exigiu produção de petição. Isso não afirma que a FORJA executou um ciclo inexistente.
- Produto pronto ou bloqueado não recebe evidência de envio sem mensagem, arquivo entregue ou protocolo próprio.
- Artefatos do sidecar só abrem após validação de caminho dentro do workspace e conferência do SHA-256 registrado.
- A rotina diária mede cobertura, divergências de estado e arquivos ausentes. A situação saudável é `vínculos = total`, `divergências = 0` e `arquivos ausentes = 0`.
- A aba Integrações e a visão Hoje exibem esses indicadores; cada demanda mostra fase, bloqueios, QA e arquivos no bloco `Ciclo FORJA`.

## Modos degradados

- Gmail sem autenticação: a fila local permanece disponível e a vista Integrações oferece reconexão.
- WhatsApp/Hermes indisponível: o último retrato sanitizado válido é preservado; uma falha não zera candidatos anteriores.
- WhatsApp aguardando QR: a vista Integrações oferece `Parear WhatsApp` e abre a tela segura de pareamento, sem transportar conversa para o painel.
- Ponte VPS indisponível: o painel local continua operando e registra o erro de sincronização.
- Servidor desligado: o launcher tenta reconectar e oferece o retrato offline.
- Porta 8765 ocupada por outro processo: o inicializador não mata o processo; reporta o conflito.

## Contratos de segurança

- Gmail e WhatsApp são somente leitura por padrão.
- O sistema não envia, arquiva, apaga ou rotula e-mail.
- O sistema não envia WhatsApp.
- WhatsApp é transportado apenas como resumo sanitizado; conversa bruta não entra no painel.
- Uma demanda só pode ser marcada como cumprida com tipo e descrição concreta da evidência.
- Alertas no celular só são disparados para demandas abertas vencidas ou com prazo formal em até 48 horas.

## Testes

```powershell
C:\Python314\python.exe -m unittest discover -s gestao_escritorio\tests -v
```

O conjunto cobre persistência atômica, leitura sem efeitos colaterais, extração conservadora de prazo, qualidade dos vínculos, contrato de saúde e presença das cinco vistas. A validação visual deve ser feita em desktop e celular após mudanças no template.
