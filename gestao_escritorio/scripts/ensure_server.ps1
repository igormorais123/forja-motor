param(
  [switch]$Open,
  [switch]$InstallStartupTask,
  [switch]$Quiet
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$EnsureScript = $MyInvocation.MyCommand.Path
$ServerScript = Join-Path $Root "scripts\server.py"
$HealthUrl = "http://127.0.0.1:8765/api/health"
$PanelUrl = "http://127.0.0.1:8765/"
$TaskName = "Medina Osorio - Gestao Escritorio Watchdog"
$FocusSafeLauncher = "C:\Users\IgorPC\.runbooks\focus-safe-launcher.pyw"

function Get-PythonExecutable {
  $candidate = Get-Command python -ErrorAction SilentlyContinue
  if ($candidate) { return $candidate.Source }
  $known = "C:\Python314\python.exe"
  if (Test-Path -LiteralPath $known) { return $known }
  throw "Python nao encontrado. Instale o Python ou ajuste o PATH."
}

function Test-PanelHealth {
  try {
    $health = Invoke-RestMethod -Uri $HealthUrl -TimeoutSec 2
    return [bool]$health.ok
  } catch {
    return $false
  }
}

function Install-WatchdogTask {
  $powershell = (Get-Command powershell.exe).Source
  $python = Get-PythonExecutable
  $pythonw = Join-Path (Split-Path -Parent $python) "pythonw.exe"
  if (-not (Test-Path -LiteralPath $pythonw)) {
    throw "pythonw.exe nao encontrado ao lado de $python."
  }
  if (-not (Test-Path -LiteralPath $FocusSafeLauncher)) {
    throw "Inicializador sem console ausente: $FocusSafeLauncher"
  }
  $watchdogArguments = '-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "' + $EnsureScript + '" -Quiet'
  $arguments = '"' + $FocusSafeLauncher + '" "' + $powershell + '" ' + $watchdogArguments
  $action = New-ScheduledTaskAction -Execute $pythonw -Argument $arguments -WorkingDirectory $Root
  $logon = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
  $watchdog = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2) -RepetitionInterval (New-TimeSpan -Minutes 10)
  $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit (New-TimeSpan -Minutes 2) -MultipleInstances IgnoreNew
  Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger @($logon, $watchdog) -Settings $settings -Description "Mantem o painel local Medina Osorio disponivel em 127.0.0.1:8765." -User $env:USERNAME -RunLevel Limited -Force | Out-Null
}

$started = $false
if (-not (Test-PanelHealth)) {
  $listener = Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue
  if ($listener) {
    throw "A porta 8765 esta ocupada por outro processo e o painel nao respondeu ao diagnostico."
  }
  $python = Get-PythonExecutable
  $quotedScript = '"' + $ServerScript + '"'
  Start-Process -FilePath $python -ArgumentList $quotedScript -WorkingDirectory $Root -WindowStyle Hidden | Out-Null
  $started = $true
  $healthy = $false
  for ($attempt = 0; $attempt -lt 40; $attempt++) {
    if (Test-PanelHealth) {
      $healthy = $true
      break
    }
    Start-Sleep -Milliseconds 250
  }
  if (-not $healthy) {
    throw "O servidor foi iniciado, mas nao ficou saudavel em 10 segundos."
  }
}

$taskInstalled = $false
if ($InstallStartupTask) {
  try {
    Install-WatchdogTask
    $taskInstalled = $true
  } catch {
    if (-not $Quiet) { Write-Warning ("Painel ativo, mas o watchdog nao foi instalado: " + $_.Exception.Message) }
  }
}

if ($Open) {
  Start-Process $PanelUrl | Out-Null
}

if (-not $Quiet) {
  [pscustomobject]@{
    ok = $true
    url = $PanelUrl
    started = $started
    watchdogInstalled = $taskInstalled
  } | ConvertTo-Json
}
