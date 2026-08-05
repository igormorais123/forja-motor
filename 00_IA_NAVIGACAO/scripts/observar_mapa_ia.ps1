[CmdletBinding()]
param(
    [int]$DebounceSeconds = 8
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$UpdateScript = Join-Path $Root "ATUALIZAR_MAPA_IA.ps1"
$LogDir = Join-Path $Root "00_IA_NAVIGACAO\logs"
$LogFile = Join-Path $LogDir "observador_mapa_ia.log"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Write-MapaLog {
    param([string]$Message)
    $line = "{0} {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
    Add-Content -LiteralPath $LogFile -Value $line -Encoding UTF8
    Write-Host $line
}

function Test-IgnorePath {
    param([string]$Path)
    if ([string]::IsNullOrWhiteSpace($Path)) { return $true }
    $normalized = $Path.Replace("/", "\")
    if ($normalized -like "*\00_IA_NAVIGACAO\*") { return $true }
    if ([IO.Path]::GetFileName($normalized) -eq "MAPA_IA.md") { return $true }
    if ([IO.Path]::GetExtension($normalized) -in @(".tmp", ".swp")) { return $true }
    return $false
}

Write-MapaLog "Iniciando observador em $Root"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $UpdateScript -Quiet
Write-MapaLog "Mapa inicial atualizado."

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $Root.Path
$watcher.Filter = "*"
$watcher.IncludeSubdirectories = $true
$watcher.NotifyFilter = [IO.NotifyFilters]'FileName, DirectoryName, LastWrite, Size'
$watcher.EnableRaisingEvents = $true

$eventNames = @("Created", "Changed", "Deleted", "Renamed")
foreach ($eventName in $eventNames) {
    Register-ObjectEvent -InputObject $watcher -EventName $eventName -SourceIdentifier "MapaIA.$eventName" | Out-Null
}

$pending = $false
$lastChange = Get-Date

try {
    while ($true) {
        $event = Wait-Event -Timeout 2
        if ($event) {
            $events = @($event) + @(Get-Event | Where-Object { $_.SourceIdentifier -like "MapaIA.*" })
            foreach ($item in $events) {
                $path = $item.SourceEventArgs.FullPath
                Remove-Event -EventIdentifier $item.EventIdentifier -ErrorAction SilentlyContinue
                if (-not (Test-IgnorePath -Path $path)) {
                    $pending = $true
                    $lastChange = Get-Date
                }
            }
        }

        if ($pending -and ((Get-Date) - $lastChange).TotalSeconds -ge $DebounceSeconds) {
            Write-MapaLog "Mudancas detectadas. Atualizando mapas."
            & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $UpdateScript -Quiet
            if ($LASTEXITCODE -eq 0) {
                Write-MapaLog "Mapas atualizados."
            } else {
                Write-MapaLog "Atualizacao retornou codigo $LASTEXITCODE."
            }
            $pending = $false
        }
    }
}
finally {
    foreach ($eventName in $eventNames) {
        Unregister-Event -SourceIdentifier "MapaIA.$eventName" -ErrorAction SilentlyContinue
    }
    $watcher.Dispose()
    Write-MapaLog "Observador encerrado."
}
