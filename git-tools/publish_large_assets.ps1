[CmdletBinding()]
param([string]$RepositoryRoot)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
if ([string]::IsNullOrWhiteSpace($RepositoryRoot)) {
    $RepositoryRoot = Split-Path -Parent $scriptDirectory
}

$manifestPath = Join-Path $scriptDirectory 'large-assets-manifest.json'
if (-not (Test-Path -LiteralPath $manifestPath)) {
    throw "Manifesto ausente: $manifestPath"
}

$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$repo = $manifest.repository
$tag = $manifest.releaseTag

$savedPreference = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
& gh release view $tag -R $repo --json tagName 2>$null | Out-Null
$releaseViewExitCode = $LASTEXITCODE
$ErrorActionPreference = $savedPreference
if ($releaseViewExitCode -ne 0) {
    & gh release create $tag -R $repo --target main --title 'Arquivos grandes do backup privado' --notes 'Assets privados acima do limite normal do Git. Gerenciados por git-tools/large-assets-manifest.json.'
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar a release de arquivos grandes.' }
}

$existing = @(& gh release view $tag -R $repo --json assets --jq '.assets[].name')
$records = [System.Collections.Generic.List[object]]::new()
foreach ($file in $manifest.files) { $records.Add($file) }
foreach ($assembled in $manifest.assembledFiles) {
    foreach ($part in $assembled.parts) { $records.Add($part) }
}

$uploadDirectory = Join-Path $env:TEMP 'fabricas-peticoes-release-assets'
[System.IO.Directory]::CreateDirectory($uploadDirectory) | Out-Null

foreach ($record in $records) {
    if ($existing -contains $record.assetName) { continue }

    $sourcePath = Join-Path $RepositoryRoot ($record.localPath.Replace('/', '\'))
    if (-not (Test-Path -LiteralPath $sourcePath)) { throw "Asset local ausente: $sourcePath" }

    $actualHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualHash -ne $record.sha256) { throw "SHA-256 divergente: $sourcePath" }

    $uploadPath = Join-Path $uploadDirectory $record.assetName
    if (Test-Path -LiteralPath $uploadPath) { Remove-Item -LiteralPath $uploadPath -Force }
    New-Item -ItemType HardLink -Path $uploadPath -Target $sourcePath | Out-Null
    try {
        & gh release upload $tag $uploadPath -R $repo
        if ($LASTEXITCODE -ne 0) { throw "Falha ao enviar o asset: $($record.assetName)" }
    }
    finally {
        Remove-Item -LiteralPath $uploadPath -Force -ErrorAction SilentlyContinue
    }
}

Write-Output 'Assets grandes conferidos na release privada.'
