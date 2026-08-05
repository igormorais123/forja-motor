$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent (Split-Path -Parent $here)
$promptPath = Join-Path $here "revisao_cruzada_corsan_n5_round7_prompt.md"
$rawPath = Join-Path $here "revisao_cruzada_corsan_n5_round7_raw.json"
$statusPath = Join-Path $here "revisao_cruzada_corsan_n5_round7_status.json"
$prompt = Get-Content -LiteralPath $promptPath -Raw -Encoding UTF8
$startedAt = (Get-Date).ToString("o")
Push-Location -LiteralPath $root
try {
    $output = & claude -p $prompt --model claude-opus-5 --permission-mode bypassPermissions --safe-mode --output-format json 2>&1
    $exitCode = $LASTEXITCODE
} finally {
    Pop-Location
}
$outputText = ($output | Out-String).Trim()
[System.IO.File]::WriteAllText($rawPath, $outputText, [System.Text.UTF8Encoding]::new($false))
$status = [ordered]@{
    startedAt = $startedAt
    finishedAt = (Get-Date).ToString("o")
    exitCode = $exitCode
    modelRequested = "claude-opus-5"
    promptSha256 = (Get-FileHash -LiteralPath $promptPath -Algorithm SHA256).Hash.ToLower()
    manifestSha256 = (Get-FileHash -LiteralPath (Join-Path $here "manifest_visual_lote_20260730.json") -Algorithm SHA256).Hash.ToLower()
    rawOutputPath = $rawPath
    rawOutputSha256 = (Get-FileHash -LiteralPath $rawPath -Algorithm SHA256).Hash.ToLower()
}
[System.IO.File]::WriteAllText($statusPath, ($status | ConvertTo-Json -Depth 5), [System.Text.UTF8Encoding]::new($false))
exit $exitCode
