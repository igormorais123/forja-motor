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

function Add-MonitorLog {
    param([Parameter(Mandatory = $true)][string]$Value)

    # Duas execuções podem se sobrepor (Agendador + canário manual), e o
    # antivírus/indexador também pode abrir o arquivo por instantes. A
    # telemetria não pode derrubar um ciclo que já concluiu a consulta.
    $mutex = [Threading.Mutex]::new($false, 'Local\FORJA-Monitor-TPU-Log')
    $locked = $false
    try {
        $locked = $mutex.WaitOne([TimeSpan]::FromSeconds(15))
        if (-not $locked) { throw 'timeout aguardando o log do monitor TPU' }
        $ultimoErro = $null
        for ($tentativa = 0; $tentativa -lt 6; $tentativa++) {
            try {
                [IO.File]::AppendAllText(
                    $log,
                    $Value + [Environment]::NewLine,
                    [Text.UTF8Encoding]::new($false)
                )
                return
            } catch [IO.IOException] {
                $ultimoErro = $_.Exception
                Start-Sleep -Milliseconds (150 * ($tentativa + 1))
            }
        }
        throw $ultimoErro
    } finally {
        if ($locked) { $mutex.ReleaseMutex() }
        $mutex.Dispose()
    }
}

Push-Location $harness
try {
    $saida = & python forja_monitor_tpu.py 2>&1 | Out-String
    $codigo = $LASTEXITCODE
} finally {
    Pop-Location
}

Add-MonitorLog -Value "==== $carimbo (exit=$codigo)`n$saida"

if ($codigo -eq 1) {
    Add-MonitorLog -Value "  !! erro na verificação — conferir manualmente"
}

# O módulo usa 10 para novidade; para o Agendador, execução concluída continua
# sendo sucesso. O detalhe permanece no log e na caixa interna de avisos.
exit 0
