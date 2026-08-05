[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Source,

    [Parameter(Mandatory = $true)]
    [string]$DestinationDirectory,

    [long]$PartSizeBytes = 1900MB
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$sourcePath = [System.IO.Path]::GetFullPath($Source)
$destinationPath = [System.IO.Path]::GetFullPath($DestinationDirectory)

if (-not [System.IO.File]::Exists($sourcePath)) {
    throw "Arquivo de origem não encontrado: $sourcePath"
}

if ($PartSizeBytes -le 0 -or $PartSizeBytes -ge 2GB) {
    throw 'O tamanho de cada parte deve ser maior que zero e menor que 2 GiB.'
}

[System.IO.Directory]::CreateDirectory($destinationPath) | Out-Null

$sourceInfo = Get-Item -LiteralPath $sourcePath
$sourceHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
$manifestPath = Join-Path $destinationPath 'manifest.json'

if (Test-Path -LiteralPath $manifestPath) {
    try {
        $current = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $partsPresent = @($current.parts | ForEach-Object {
            Test-Path -LiteralPath (Join-Path $destinationPath $_.name)
        }) -notcontains $false

        if ($current.sourceSha256 -eq $sourceHash -and
            [long]$current.sourceBytes -eq $sourceInfo.Length -and
            $partsPresent) {
            Write-Output 'A cópia dividida já está atualizada.'
            exit 0
        }
    }
    catch {
        Write-Warning 'Manifesto anterior inválido; as partes serão refeitas.'
    }
}

Get-ChildItem -LiteralPath $destinationPath -File -Filter '*.part???' -ErrorAction SilentlyContinue |
    Remove-Item -Force

$buffer = New-Object byte[] (8MB)
$input = [System.IO.File]::Open($sourcePath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::Read)
$partNumber = 0
$parts = [System.Collections.Generic.List[object]]::new()

try {
    while ($input.Position -lt $input.Length) {
        $partNumber++
        $partName = '{0}.part{1:D3}' -f $sourceInfo.Name, $partNumber
        $partPath = Join-Path $destinationPath $partName
        $output = [System.IO.File]::Open($partPath, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
        $written = 0L

        try {
            while ($written -lt $PartSizeBytes -and $input.Position -lt $input.Length) {
                $remaining = [Math]::Min($buffer.Length, $PartSizeBytes - $written)
                $read = $input.Read($buffer, 0, [int]$remaining)
                if ($read -le 0) { break }
                $output.Write($buffer, 0, $read)
                $written += $read
            }
        }
        finally {
            $output.Dispose()
        }

        $partHash = (Get-FileHash -LiteralPath $partPath -Algorithm SHA256).Hash.ToLowerInvariant()
        $parts.Add([ordered]@{
            name = $partName
            bytes = $written
            sha256 = $partHash
        })
    }
}
finally {
    $input.Dispose()
}

$manifest = [ordered]@{
    schema = 1
    sourceName = $sourceInfo.Name
    sourceBytes = $sourceInfo.Length
    sourceSha256 = $sourceHash
    partSizeBytes = $PartSizeBytes
    parts = $parts
}

$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding UTF8
Write-Output ("Arquivo preservado em {0} parte(s). SHA-256: {1}" -f $parts.Count, $sourceHash)

