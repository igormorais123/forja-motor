[CmdletBinding()]
param([string]$RepositoryRoot)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
if ([string]::IsNullOrWhiteSpace($RepositoryRoot)) {
    $RepositoryRoot = Split-Path -Parent $scriptDirectory
}

$manifestPath = Join-Path $scriptDirectory 'large-assets-manifest.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$downloadDirectory = Join-Path $env:TEMP 'fabricas-peticoes-restore-assets'
[System.IO.Directory]::CreateDirectory($downloadDirectory) | Out-Null

function Get-VerifiedAsset {
    param([object]$Record)
    $downloadPath = Join-Path $downloadDirectory $Record.assetName
    if (-not (Test-Path -LiteralPath $downloadPath)) {
        & gh release download $manifest.releaseTag -R $manifest.repository --pattern $Record.assetName --dir $downloadDirectory
        if ($LASTEXITCODE -ne 0) { throw "Falha ao baixar: $($Record.assetName)" }
    }
    $hash = (Get-FileHash -LiteralPath $downloadPath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -ne $Record.sha256) { throw "SHA-256 inválido: $($Record.assetName)" }
    return $downloadPath
}

foreach ($file in $manifest.files) {
    $source = Get-VerifiedAsset -Record $file
    $target = Join-Path $RepositoryRoot ($file.targetPath.Replace('/', '\'))
    [System.IO.Directory]::CreateDirectory((Split-Path -Parent $target)) | Out-Null
    Copy-Item -LiteralPath $source -Destination $target -Force
}

foreach ($assembled in $manifest.assembledFiles) {
    $target = Join-Path $RepositoryRoot ($assembled.targetPath.Replace('/', '\'))
    [System.IO.Directory]::CreateDirectory((Split-Path -Parent $target)) | Out-Null
    $temporary = "$target.restoring"
    $output = [System.IO.File]::Open($temporary, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
    try {
        foreach ($part in $assembled.parts) {
            $partPath = Get-VerifiedAsset -Record $part
            $input = [System.IO.File]::OpenRead($partPath)
            try { $input.CopyTo($output) } finally { $input.Dispose() }
        }
    }
    finally { $output.Dispose() }

    $hash = (Get-FileHash -LiteralPath $temporary -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -ne $assembled.sha256) {
        Remove-Item -LiteralPath $temporary -Force
        throw "SHA-256 inválido no arquivo recomposto: $target"
    }
    Move-Item -LiteralPath $temporary -Destination $target -Force
}

Write-Output 'Todos os arquivos grandes foram restaurados e validados.'
