[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$TaskName = "MapaIA_FabricaPeticoes"
$StartupFile = Join-Path ([Environment]::GetFolderPath("Startup")) "MapaIA_FabricaPeticoes.cmd"
$StartupLink = Join-Path ([Environment]::GetFolderPath("Startup")) "MapaIA_FabricaPeticoes.lnk"

$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Tarefa agendada removida: $TaskName"
} else {
    Write-Host "Tarefa agendada nao encontrada: $TaskName"
}

if (Test-Path -LiteralPath $StartupFile) {
    Remove-Item -LiteralPath $StartupFile -Force
    Write-Host "Inicializador Startup removido: $StartupFile"
}

if (Test-Path -LiteralPath $StartupLink) {
    Remove-Item -LiteralPath $StartupLink -Force
    Write-Host "Atalho Startup removido: $StartupLink"
}
