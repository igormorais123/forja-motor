[CmdletBinding()]
param([string]$RepositoryRoot)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
if ([string]::IsNullOrWhiteSpace($RepositoryRoot)) {
    $RepositoryRoot = Split-Path -Parent $scriptDirectory
}

$caseFolder = Join-Path $RepositoryRoot 'Assunto Laudo Pericial Contábil – Atualização de Valores – Proc. 0003453-28.1997.4.01.3400'
$partsFolder = Join-Path $caseFolder '_github_lfs_docs_laudo_pericia_zip'
$manifestPath = Join-Path $partsFolder 'manifest.json'

if (-not (Test-Path -LiteralPath $manifestPath)) {
    throw "Manifesto não encontrado: $manifestPath"
}

$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$outputPath = Join-Path $caseFolder $manifest.sourceName
$temporaryPath = "$outputPath.restoring"

$output = [System.IO.File]::Open($temporaryPath, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
try {
    foreach ($part in $manifest.parts) {
        $partPath = Join-Path $partsFolder $part.name
        if (-not (Test-Path -LiteralPath $partPath)) {
            throw "Parte ausente: $partPath"
        }

        $actualPartHash = (Get-FileHash -LiteralPath $partPath -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actualPartHash -ne $part.sha256) {
            throw "SHA-256 inválido na parte: $partPath"
        }

        $input = [System.IO.File]::OpenRead($partPath)
        try { $input.CopyTo($output) } finally { $input.Dispose() }
    }
}
finally {
    $output.Dispose()
}

$restoredHash = (Get-FileHash -LiteralPath $temporaryPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($restoredHash -ne $manifest.sourceSha256) {
    Remove-Item -LiteralPath $temporaryPath -Force
    throw 'O SHA-256 do arquivo restaurado não confere com o manifesto.'
}

Move-Item -LiteralPath $temporaryPath -Destination $outputPath -Force
Write-Output "Arquivo restaurado e validado: $outputPath"
