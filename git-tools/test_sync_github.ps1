# Contraprova do sync_github.ps1, contra os defeitos que ele de fato teve.
#
# Não roda o script de produção contra o repositório real — cria um repositório
# git descartável e exercita ali as duas decisões que quebraram: agir fora de
# `main` e deixar arquivo grande entrar no commit. O terceiro defeito, a
# identidade, é conferido por leitura do commit produzido.
#
# Uso: pwsh -File test_sync_github.ps1   (exit 0 = ok)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$falhas = @()
$origem = Join-Path $PSScriptRoot 'sync_github.ps1'
$fonte = Get-Content -LiteralPath $origem -Raw

# --- 1. O script precisa recusar agir fora de main -------------------------
if ($fonte -notmatch "if \(\`$branch -ne 'main'\)") {
    $falhas += 'o script não confere o branch antes de commitar'
}
if ($fonte -match "push origin main" -and $fonte -notmatch "rev-parse --abbrev-ref HEAD") {
    $falhas += 'empurra main sem nunca conferir em que branch commitou'
}

# --- 2. O limite de tamanho precisa existir e ser aplicado ao ÍNDICE --------
if ($fonte -notmatch 'limiteBytes') { $falhas += 'não há limite de tamanho' }
if ($fonte -notmatch 'diff --cached --name-only') {
    $falhas += 'o limite não é medido sobre o que de fato entraria no commit'
}
if ($fonte -notmatch 'reset --quiet --') {
    $falhas += 'arquivo grande é detectado mas não é retirado do commit'
}

# --- 3. Identidade própria da automação ------------------------------------
if ($fonte -notmatch "user\.name='FORJA sync'") {
    $falhas += 'a automação ainda assinaria com a identidade pessoal'
}

# --- 4. A falha precisa aparecer fora do log -------------------------------
if ($fonte -notmatch 'Write-SyncStatus -Situacao ''FALHOU''') {
    $falhas += 'a falha continua visível só no log que ninguém abre'
}

# --- 5. Exercício real: arquivo grande é mesmo retirado do índice -----------
# Reproduz a mecânica do bloco de exclusão num repositório descartável, com um
# arquivo acima do limite. Se esta parte passar por acidente — porque o arquivo
# não chegou a ser grande —, o próprio teste acusa.
$temp = Join-Path ([System.IO.Path]::GetTempPath()) ('sync-test-' + [guid]::NewGuid().ToString('N').Substring(0, 8))
New-Item -ItemType Directory -Path $temp | Out-Null
try {
    & git -C $temp init --quiet -b main
    Set-Content -LiteralPath (Join-Path $temp 'pequeno.txt') -Value 'ok' -Encoding UTF8

    $grandePath = Join-Path $temp 'grande.bin'
    $fs = [System.IO.File]::Create($grandePath)
    try { $fs.SetLength(100MB) } finally { $fs.Dispose() }
    if ((Get-Item -LiteralPath $grandePath).Length -le 95MB) {
        $falhas += 'o arquivo de teste não ficou acima do limite — o exercício seria vazio'
    }

    & git -C $temp add -A
    $limiteBytes = 95MB
    $retirados = @()
    foreach ($relativo in @(& git -C $temp diff --cached --name-only --diff-filter=ACMR)) {
        if ([string]::IsNullOrWhiteSpace($relativo)) { continue }
        $absoluto = Join-Path $temp $relativo
        if (-not (Test-Path -LiteralPath $absoluto -PathType Leaf)) { continue }
        if ((Get-Item -LiteralPath $absoluto).Length -gt $limiteBytes) {
            & git -C $temp reset --quiet -- $relativo
            $retirados += $relativo
        }
    }

    $restantes = @(& git -C $temp diff --cached --name-only)
    if ($retirados -notcontains 'grande.bin') { $falhas += 'o arquivo grande não foi retirado' }
    if ($restantes -contains 'grande.bin') { $falhas += 'o arquivo grande continuou no commit' }
    # E o inverso, que é o que impede o remédio de virar doença: o arquivo
    # pequeno TEM de continuar. Um filtro que esvazia o commit também "resolve"
    # o push, e resolveria parando de sincronizar.
    if ($restantes -notcontains 'pequeno.txt') {
        $falhas += 'o arquivo pequeno foi retirado junto — o filtro esvaziaria o commit'
    }
}
finally {
    Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue
}

if ($falhas.Count -gt 0) {
    foreach ($f in $falhas) { Write-Output "  FALHOU: $f" }
    Write-Output "REGRESSÃO: $($falhas.Count) verificação(ões) do sync falharam"
    exit 1
}
Write-Output 'ok: sync só age em main, retira arquivo acima do limite sem esvaziar o commit, assina como automação e grita fora do log'
exit 0
