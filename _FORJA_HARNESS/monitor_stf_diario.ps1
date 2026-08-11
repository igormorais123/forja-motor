# Execução diária do vigia de andamentos do STF.
# Registrado como tarefa agendada FORJA-Monitor-STF. Silencioso quando não há
# novidade; quando há, deixa um arquivo visível em `reports\`, porque log que
# ninguém abre não avisa ninguém.
#
# O aviso nomeia o processo e o cliente, então não pode nascer na raiz do
# harness: ali é motor, e o gate de fronteira reprova a publicação inteira por
# causa dele. `reports\` já é acervo e já é o destino de escrita de outros
# módulos, de modo que o aviso continua à vista sem atravessar a fronteira.

$ErrorActionPreference = 'Stop'
# O agendador nao herda o ambiente da sessao: sem isto o Python escreve na code
# page do console e todo acento chega corrompido ao log e a flag.
$env:PYTHONIOENCODING = 'utf-8'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$harness = Split-Path -Parent $MyInvocation.MyCommand.Path
$logDir  = Join-Path $harness 'telemetria\monitor_stf'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log     = Join-Path $logDir 'execucoes.log'
$flag    = Join-Path $harness 'reports\NOVIDADE_STF.md'
New-Item -ItemType Directory -Force -Path (Join-Path $harness 'reports') | Out-Null
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

Este arquivo é acervo: nomeia processo e cliente e não acompanha o motor.
"@
    Set-Content -Path $flag -Value $texto -Encoding UTF8
} elseif ($codigo -eq 0 -and (Test-Path -LiteralPath $flag)) {
    # Sem movimento novo, a flag anterior só pode sair se o aviso persistente
    # já recebeu ciência nominal. Assim não apagamos novidade esquecida e não
    # deixamos alerta visual depois do encaminhamento comprovado.
    try {
        Push-Location $harness
        $pendentes = (& python forja_avisos.py --json 2>$null | Out-String) | ConvertFrom-Json
        if (-not @($pendentes | Where-Object { $_.origem -eq 'monitor_stf' }).Count) {
            Remove-Item -LiteralPath $flag -Force
        }
    } finally {
        Pop-Location
    }
} elseif ($codigo -eq 1) {
    Add-Content -Path $log -Value "  !! erro na verificacao — conferir manualmente" -Encoding UTF8
}

exit 0
