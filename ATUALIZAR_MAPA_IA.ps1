[CmdletBinding()]
param(
    [switch]$Quiet
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Generator = Join-Path $Root "00_IA_NAVIGACAO\scripts\atualizar_mapa_ia.py"

if (-not (Test-Path -LiteralPath $Generator)) {
    throw "Gerador nao encontrado: $Generator"
}

$Python = (Get-Command python -ErrorAction SilentlyContinue | Select-Object -First 1).Source
if (-not $Python) {
    throw "Python nao encontrado no PATH."
}

$ArgsList = @($Generator)
if ($Quiet) {
    $ArgsList += "--quiet"
}

& $Python @ArgsList
exit $LASTEXITCODE
