$ErrorActionPreference = "Stop"

$promptPath = Join-Path $PSScriptRoot "revisao_cruzada_visual_lote_20260730_prompt.md"
$rawOutputPath = Join-Path $PSScriptRoot "revisao_cruzada_visual_lote_20260730_round6_raw.json"
$statusPath = Join-Path $PSScriptRoot "revisao_cruzada_visual_lote_20260730_round6_status.json"
$prompt = Get-Content -LiteralPath $promptPath -Raw -Encoding UTF8
$startedAt = (Get-Date).ToString("o")

$output = & claude -p $prompt --model claude-opus-5 --permission-mode bypassPermissions --safe-mode --output-format json 2>&1
$exitCode = $LASTEXITCODE
$outputText = ($output | Out-String).Trim()
[System.IO.File]::WriteAllText($rawOutputPath, $outputText, [System.Text.UTF8Encoding]::new($false))

$status = [ordered]@{
    startedAt = $startedAt
    finishedAt = (Get-Date).ToString("o")
    exitCode = $exitCode
    modelRequested = "claude-opus-5"
    promptSha256 = (Get-FileHash -LiteralPath $promptPath -Algorithm SHA256).Hash.ToLower()
    manifestSha256 = (Get-FileHash -LiteralPath (Join-Path $PSScriptRoot "manifest_visual_lote_20260730.json") -Algorithm SHA256).Hash.ToLower()
    rawOutputPath = $rawOutputPath
    rawOutputSha256 = (Get-FileHash -LiteralPath $rawOutputPath -Algorithm SHA256).Hash.ToLower()
}
[System.IO.File]::WriteAllText(
    $statusPath,
    ($status | ConvertTo-Json -Depth 5),
    [System.Text.UTF8Encoding]::new($false)
)

exit $exitCode
