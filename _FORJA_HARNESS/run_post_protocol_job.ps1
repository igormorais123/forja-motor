param(
    [string]$Query = "in:anywhere newer_than:120d has:attachment -in:sent -in:trash -in:spam",
    [int]$MaxResults = 150
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$entrypoint = Join-Path $root "forja_post_protocol.py"

if (-not (Test-Path -LiteralPath $entrypoint -PathType Leaf)) {
    throw "Entrypoint pós-protocolo não localizado."
}

Push-Location $root
try {
    & python $entrypoint scan-gmail --query $Query --max-results $MaxResults
    if ($LASTEXITCODE -ne 0) {
        throw "Job pós-protocolo terminou com código $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}
