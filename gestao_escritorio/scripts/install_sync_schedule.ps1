param(
  [int]$IntervalMinutes = 30
)

$ErrorActionPreference = "Stop"
$TaskName = "Medina Osorio - Gestao Escritorio Sync"
$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Update = Join-Path $Root "gestao_escritorio\scripts\update_dashboard_local.ps1"
$Launcher = "C:\Users\IgorPC\.runbooks\focus-safe-launcher.pyw"
$Pythonw = "C:\Python314\pythonw.exe"
$PowerShell = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"

if (-not (Test-Path -LiteralPath $Update)) { throw "Atualizador não encontrado: $Update" }
if (-not (Test-Path -LiteralPath $Launcher)) { throw "Inicializador sem foco não encontrado: $Launcher" }
if (-not (Test-Path -LiteralPath $Pythonw)) { throw "pythonw.exe não encontrado: $Pythonw" }

$arguments = '"{0}" "{1}" -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "{2}" -Mode Automation' -f $Launcher, $PowerShell, $Update
$action = New-ScheduledTaskAction -Execute $Pythonw -Argument $arguments -WorkingDirectory $Root
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2) -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RestartCount 2 -RestartInterval (New-TimeSpan -Minutes 3) -ExecutionTimeLimit (New-TimeSpan -Minutes 20) -MultipleInstances IgnoreNew

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Description "Atualiza Gmail, entregas, WhatsApp sanitizado, FORJA, Hermes VPS e painel Medina Osorio sem roubar foco." -User $env:USERNAME -RunLevel Limited -Force | Out-Null
Write-Output "OK: $TaskName a cada $IntervalMinutes minutos"
