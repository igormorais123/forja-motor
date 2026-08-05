[CmdletBinding()]
param(
    [int]$IntervalMinutes = 15
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$UpdateScript = Join-Path $Root "ATUALIZAR_MAPA_IA.ps1"
$WatchScript = Join-Path $Root "00_IA_NAVIGACAO\scripts\observar_mapa_ia.ps1"
$TaskName = "MapaIA_FabricaPeticoes"

if (-not (Test-Path -LiteralPath $UpdateScript)) {
    throw "Script de atualizacao nao encontrado: $UpdateScript"
}

function Install-StartupFallback {
    $StartupDir = [Environment]::GetFolderPath("Startup")
    $StartupFile = Join-Path $StartupDir "MapaIA_FabricaPeticoes.cmd"
    $StartupLink = Join-Path $StartupDir "MapaIA_FabricaPeticoes.lnk"
    if (Test-Path -LiteralPath $StartupFile) {
        Remove-Item -LiteralPath $StartupFile -Force
    }

    $Shell = New-Object -ComObject WScript.Shell
    $Shortcut = $Shell.CreateShortcut($StartupLink)
    $Shortcut.TargetPath = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
    $Shortcut.Arguments = "-WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -File `"$WatchScript`""
    $Shortcut.WorkingDirectory = $Root.Path
    $Shortcut.Description = "Observador vivo do Mapa IA da fabrica de peticoes"
    $Shortcut.Save()

    $StartArgs = "-WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -File `"$WatchScript`""
    Start-Process -FilePath "powershell.exe" -WindowStyle Hidden -WorkingDirectory $Root.Path -ArgumentList $StartArgs
    Write-Host "Fallback instalado na pasta Startup: $StartupLink"
    Write-Host "Observador vivo iniciado em segundo plano."
}

$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$UpdateScript`" -Quiet"

$TriggerLogon = New-ScheduledTaskTrigger -AtLogOn
$TriggerRepeat = New-ScheduledTaskTrigger `
    -Once `
    -At (Get-Date).AddMinutes(2) `
    -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes) `
    -RepetitionDuration (New-TimeSpan -Days 3650)

$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew

try {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger @($TriggerLogon, $TriggerRepeat) `
        -Settings $Settings `
        -Description "Atualiza os MAPA_IA.md da fabrica de peticoes automaticamente." `
        -Force | Out-Null

    Start-ScheduledTask -TaskName $TaskName
    Write-Host "Tarefa agendada instalada: $TaskName"
    Write-Host "Intervalo: $IntervalMinutes minutos"
}
catch {
    Write-Warning "Tarefa agendada indisponivel: $($_.Exception.Message)"
    Install-StartupFallback
}
