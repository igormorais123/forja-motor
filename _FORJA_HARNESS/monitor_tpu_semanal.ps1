# Execução semanal do vigia das Tabelas Processuais Unificadas do CNJ.
# Registrado como tarefa agendada FORJA-Monitor-TPU. O módulo consulta fonte
# pública, grava o retrato e deposita aviso interno apenas quando há mudança.

$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$harness = Split-Path -Parent $MyInvocation.MyCommand.Path
$logDir  = Join-Path $harness 'telemetria\monitor_tpu'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log     = Join-Path $logDir 'execucoes.log'
$carimbo = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

Push-Location $harness
try {
    $saida = & python forja_monitor_tpu.py 2>&1 | Out-String
    $codigo = $LASTEXITCODE
} finally {
    Pop-Location
}

Add-Content -Path $log -Value "==== $carimbo (exit=$codigo)`n$saida" -Encoding UTF8

if ($codigo -eq 1) {
    Add-Content -Path $log -Value "  !! erro na verificação — conferir manualmente" -Encoding UTF8
}

# O módulo usa 10 para novidade; para o Agendador, execução concluída continua
# sendo sucesso. O detalhe permanece no log e na caixa interna de avisos.
exit 0
