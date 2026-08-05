$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Ensure = Join-Path $Root "scripts\ensure_server.ps1"

& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Ensure -Open -InstallStartupTask
