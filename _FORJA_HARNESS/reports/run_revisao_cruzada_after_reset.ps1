$ErrorActionPreference = "Stop"

$promptPath = Join-Path $PSScriptRoot "revisao_cruzada_lote_20260729_prompt.md"
$rawOutputPath = Join-Path $PSScriptRoot "revisao_cruzada_lote_20260729_raw.json"
$statusPath = Join-Path $PSScriptRoot "revisao_cruzada_lote_20260729_status.json"
$target = [datetime]::Today.AddHours(21).AddMinutes(1)
$now = Get-Date

if ($now -lt $target) {
    Start-Sleep -Seconds ([int][math]::Ceiling(($target - $now).TotalSeconds))
}

$startedAt = (Get-Date).ToString("o")
$prompt = Get-Content -LiteralPath $promptPath -Raw -Encoding UTF8
$output = & claude -p $prompt --model claude-opus-5 --output-format json 2>&1
$exitCode = $LASTEXITCODE
$outputText = ($output | Out-String).Trim()

[System.IO.File]::WriteAllText($rawOutputPath, $outputText, [System.Text.UTF8Encoding]::new($false))

$status = [ordered]@{
    startedAt = $startedAt
    finishedAt = (Get-Date).ToString("o")
    exitCode = $exitCode
    modelRequested = "claude-opus-5"
    rawOutputPath = $rawOutputPath
}
$statusJson = $status | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText($statusPath, $statusJson, [System.Text.UTF8Encoding]::new($false))

