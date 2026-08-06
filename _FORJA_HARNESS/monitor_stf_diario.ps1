# Execução diária do vigia de andamentos do STF.
# Registrado como tarefa agendada FORJA-Monitor-STF. Silencioso quando não há
# novidade; quando há, deixa um arquivo visível na raiz do harness, porque log
# que ninguém abre não avisa ninguém.

$ErrorActionPreference = 'Stop'
$harness = Split-Path -Parent $MyInvocation.MyCommand.Path
$logDir  = Join-Path $harness 'telemetria\monitor_stf'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log     = Join-Path $logDir 'execucoes.log'
$flag    = Join-Path $harness 'NOVIDADE_STF.md'
$carimbo = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

Push-Location $harness
try {
    $saida = & python forja_monitor_stf.py 2>&1 | Out-String
    $codigo = $LASTEXITCODE
} finally {
    Pop-Location
}

Add-Content -Path $log -Value "==== $carimbo (exit=$codigo)`n$saida" -Encoding UTF8

if ($codigo -eq 10) {
    $texto = @"
# Movimento novo no STF — $carimbo

O vigia de andamentos encontrou movimentação nova em processo acompanhado.

$saida

Confira o processo antes de tratar como definitivo, e apague este arquivo depois
de dar o encaminhamento. Detalhe por caso em ``telemetria\monitor_stf\``.
"@
    Set-Content -Path $flag -Value $texto -Encoding UTF8
} elseif ($codigo -eq 1) {
    Add-Content -Path $log -Value "  !! erro na verificacao — conferir manualmente" -Encoding UTF8
}

exit 0
