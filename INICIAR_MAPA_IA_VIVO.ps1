[CmdletBinding()]
param(
    [int]$DebounceSeconds = 8
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$WatcherScript = Join-Path $Root "00_IA_NAVIGACAO\scripts\observar_mapa_ia.ps1"

if (-not (Test-Path -LiteralPath $WatcherScript)) {
    throw "Observador nao encontrado: $WatcherScript"
}

& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $WatcherScript -DebounceSeconds $DebounceSeconds
exit $LASTEXITCODE
