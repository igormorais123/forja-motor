# Execução diária do vigia de comunicações processuais (DJEN/CNJ).
# Registrado como tarefa agendada FORJA-Monitor-DJEN. Silencioso quando não há
# novidade; quando há, deixa um arquivo visível na raiz do harness, porque log
# que ninguém abre não avisa ninguém.

$ErrorActionPreference = 'Stop'
# O agendador nao herda o ambiente da sessao: sem isto o Python escreve na code
# page do console e todo acento chega corrompido ao log e a flag.
$env:PYTHONIOENCODING = 'utf-8'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$harness = Split-Path -Parent $MyInvocation.MyCommand.Path
$logDir  = Join-Path $harness 'telemetria\monitor_djen'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log     = Join-Path $logDir 'execucoes.log'
$flag    = Join-Path $harness 'NOVIDADE_PROCESSUAL.md'
$carimbo = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

Push-Location $harness
try {
    $saida = & python forja_monitor_djen.py 2>&1 | Out-String
    $codigo = $LASTEXITCODE
} finally {
    Pop-Location
}

Add-Content -Path $log -Value "==== $carimbo (exit=$codigo)`n$saida" -Encoding UTF8

if ($codigo -eq 10) {
    $urgente = if ($saida -match 'URGENTE') { " — HÁ ITEM QUE PEDE LEITURA IMEDIATA" } else { "" }
    $texto = @"
# Comunicação processual nova$urgente — $carimbo

O vigia do Diário de Justiça Eletrônico Nacional encontrou comunicação nova em
processo acompanhado.

$saida

Confira no processo antes de tratar como definitivo, e apague este arquivo depois
de dar o encaminhamento. Detalhe por processo em ``telemetria\monitor_djen\``.
"@
    Set-Content -Path $flag -Value $texto -Encoding UTF8
} elseif ($codigo -eq 2) {
    Add-Content -Path $log -Value "  -- sem alvo: o acervo nao esta nesta maquina" -Encoding UTF8
} elseif ($codigo -eq 1) {
    Add-Content -Path $log -Value "  !! erro na verificacao — conferir manualmente" -Encoding UTF8
}

exit 0
