[CmdletBinding()]
param([string]$RepositoryRoot)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
if ([string]::IsNullOrWhiteSpace($RepositoryRoot)) {
    $RepositoryRoot = Split-Path -Parent $scriptDirectory
}

function Get-RelativeForwardPath {
    param([string]$Root, [string]$Path)
    $rootWithSlash = [System.IO.Path]::GetFullPath($Root).TrimEnd('\') + '\'
    $rootUri = [System.Uri]::new($rootWithSlash)
    $pathUri = [System.Uri]::new([System.IO.Path]::GetFullPath($Path))
    return [System.Uri]::UnescapeDataString($rootUri.MakeRelativeUri($pathUri).ToString())
}

function Get-AssetRecord {
    param(
        [string]$Root,
        [string]$LocalPath,
        [string]$TargetPath,
        [string]$AssetPrefix
    )

    $item = Get-Item -LiteralPath $LocalPath
    $hash = (Get-FileHash -LiteralPath $LocalPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $extension = $item.Extension.ToLowerInvariant()
    return [ordered]@{
        assetName = ('{0}-{1}{2}' -f $AssetPrefix, $hash.Substring(0, 12), $extension)
        localPath = (Get-RelativeForwardPath -Root $Root -Path $item.FullName)
        targetPath = $TargetPath
        bytes = $item.Length
        sha256 = $hash
    }
}

$root = [System.IO.Path]::GetFullPath($RepositoryRoot)
$caseRelative = 'Assunto Laudo Pericial Contábil – Atualização de Valores – Proc. 9000001-00.1997.4.01.0000'
$caseFolder = Join-Path $root $caseRelative
$zipPath = Join-Path $caseFolder 'docs laudo pericia.zip'
$partsFolder = Join-Path $caseFolder '_github_lfs_docs_laudo_pericia_zip'
$pdfPath = Join-Path $caseFolder '8 - novo laudo técnico e-fls 1139 a 2699 (975-2515) (1).pdf'
$sqliteRelative = 'Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/_nivel_sol_work/private_whatsapp/messages-current.sqlite'
$sqlitePath = Join-Path $root ($sqliteRelative.Replace('/', '\'))

& (Join-Path $scriptDirectory 'split_oversized_file.ps1') -Source $zipPath -DestinationDirectory $partsFolder

$zipInfo = Get-Item -LiteralPath $zipPath
$zipHash = (Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()
$partItems = @(Get-ChildItem -LiteralPath $partsFolder -File -Filter '*.part???' | Sort-Object Name)
if ($partItems.Count -eq 0) { throw 'Nenhuma parte do ZIP foi encontrada.' }

$parts = [System.Collections.Generic.List[object]]::new()
for ($index = 0; $index -lt $partItems.Count; $index++) {
    $part = $partItems[$index]
    $partHash = (Get-FileHash -LiteralPath $part.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    $parts.Add([ordered]@{
        assetName = ('docs-laudo-pericia-{0}.part{1:D3}' -f $zipHash.Substring(0, 12), ($index + 1))
        localPath = (Get-RelativeForwardPath -Root $root -Path $part.FullName)
        bytes = $part.Length
        sha256 = $partHash
    })
}

$manifest = [ordered]@{
    schema = 1
    repository = 'igormorais123/fabricas-de-melhoria-de-peticoes'
    releaseTag = 'large-files'
    files = @(
        Get-AssetRecord -Root $root -LocalPath $pdfPath -TargetPath "$caseRelative/8 - novo laudo técnico e-fls 1139 a 2699 (975-2515) (1).pdf" -AssetPrefix 'laudo-tecnico-e-fls-1139-2699'
        Get-AssetRecord -Root $root -LocalPath $sqlitePath -TargetPath $sqliteRelative -AssetPrefix 'messages-current'
    )
    assembledFiles = @(
        [ordered]@{
            targetPath = "$caseRelative/docs laudo pericia.zip"
            bytes = $zipInfo.Length
            sha256 = $zipHash
            parts = $parts
        }
    )
}

$manifestPath = Join-Path $scriptDirectory 'large-assets-manifest.json'
$json = $manifest | ConvertTo-Json -Depth 8
$current = if (Test-Path -LiteralPath $manifestPath) { Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 } else { '' }
if ($current.TrimEnd() -ne $json.TrimEnd()) {
    Set-Content -LiteralPath $manifestPath -Value $json -Encoding UTF8
    Write-Output 'Manifesto de arquivos grandes atualizado.'
}
else {
    Write-Output 'Manifesto de arquivos grandes já está atualizado.'
}
