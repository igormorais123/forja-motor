# Execução diária do varredor de fios de e-mail sem resposta minha.
# Registrado como tarefa agendada FORJA-Fios-Abertos. Silencioso quando não há
# fio aberto; quando há, deixa arquivo visível na raiz do harness, porque log
# que ninguém abre não avisa ninguém.

$ErrorActionPreference = 'Stop'
$harness = Split-Path -Parent $MyInvocation.MyCommand.Path
$logDir  = Join-Path $harness 'telemetria\fios_abertos'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log     = Join-Path $logDir 'execucoes.log'
$flag    = Join-Path $harness 'FIO_SEM_RESPOSTA.md'
$carimbo = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

Push-Location $harness
try {
    $saida = & python forja_fios_abertos.py 2>&1 | Out-String
    $codigo = $LASTEXITCODE
} finally {
    Pop-Location
}

Add-Content -Path $log -Value "==== $carimbo (exit=$codigo)`n$saida" -Encoding UTF8

if ($codigo -eq 10) {
    $nunca = if ($saida -match 'NUNCA RESPONDI') { " — HÁ FIO NUNCA RESPONDIDO" } else { "" }
    $texto = @"
# Fio de e-mail sem resposta$nunca — $carimbo

Há mensagem do escritório posterior à última resposta minha. Entrega feita não
fecha o fio: o retorno sobre uma peça já entregue abre trabalho novo que o
painel de demandas registra como o mesmo item já cumprido.

$saida

Responda ou anote a decisão, e apague este arquivo depois de dar o
encaminhamento.
"@
    Set-Content -Path $flag -Value $texto -Encoding UTF8
} elseif ($codigo -eq 2) {
    Add-Content -Path $log -Value "  -- sem alvo: o acervo nao esta nesta maquina" -Encoding UTF8
} elseif ($codigo -eq 1) {
    Add-Content -Path $log -Value "  !! erro na varredura — conferir manualmente" -Encoding UTF8
}

exit 0
