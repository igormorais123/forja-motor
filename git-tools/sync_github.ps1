[CmdletBinding()]
param()

# ============================================================================
# APOSENTADO em 05/08/2026. NAO USE.
#
# Este script sincronizava o repositorio unico
# `igormorais123/fabricas-de-melhoria-de-peticoes`, que misturava o motor da
# FORJA com 17 GB de acervo processual. Ele parou de conseguir enviar em
# 31/07/2026 e o motivo nao tem conserto neste formato: o primeiro commit nao
# publicado sozinho tem 3,47 GB, e commit e atomico — nao ha fatiamento
# possivel. O erro ia para um log que ninguem abria, e por cinco dias o GitHub
# pareceu ser copia de seguranca sem ser.
#
# O substituto e `git-tools/sync_forja_repos.py`, agendado como
# "FORJA - Sync GitHub (motor + acervo)". Ele mantem DOIS repositorios:
#     forja-harness            motor, ~152 MB, sem dado de cliente
#     forja-acervo-auditoria   state/, modelos, painel, ~190 MB
#
# O acervo processual nao vai a nenhum dos dois: fica no disco, e a origem dele
# e o e-mail.
#
# O conteudo original segue abaixo, comentado, so como registro do que a rotina
# fazia — inclusive dos tres defeitos corrigidos em 05/08 antes de ela ser
# aposentada (commit no branch corrente com push sempre em main, ausencia de
# barreira de tamanho e identidade de commit indistinguivel da humana).
# ============================================================================

Write-Output 'sync_github.ps1 esta APOSENTADO. Use: python git-tools/sync_forja_repos.py'
Write-Output 'Detalhes no cabecalho deste arquivo e em _FORJA_HARNESS/CIRURGIA_COMMITS_2026-08-05.md'
exit 0

<#
--- conteudo original, preservado como registro ---

# Sincronização diária do repositório com o GitHub.
#
# Três defeitos consertados em 05/08/2026, depois de o push falhar em silêncio
# por cinco dias seguidos (main ficou 26 commits à frente do remoto):
#
#  1. Commitava no branch CORRENTE mas empurrava sempre `main`. As duas metades
#     discordavam, então o commit de sincronização caía em branch de trabalho e
#     o push não o levava a lugar nenhum. Agora a automação só age quando o
#     checkout está em `main`; em branch de trabalho ela sai sem tocar em nada,
#     porque varrer trabalho em curso para dentro de um commit é pior do que não
#     sincronizar naquele dia.
#
#  2. `add -A` empacotava arquivos acima do limite de 100 MB por arquivo do
#     GitHub, e o push morria na transferência — todo dia, com o erro indo para
#     um log que ninguém abre. Agora os arquivos grandes são descobertos por
#     tamanho e retirados do commit antes dele existir. O manifesto de assets
#     continuava sendo uma lista fixa de três arquivos escrita em 11/07, o que
#     não protege contra o arquivo grande que aparece amanhã.
#
#  3. Commitava com a identidade pessoal do Igor, tornando indistinguíveis no
#     histórico o commit humano, o de agente e o de automação. Agora a
#     automação assina com nome próprio.
#
# O que este script NÃO faz, por decisão: não reescreve histórico, não remove
# arquivo do disco e não decide o destino do acervo.

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$logDirectory = Join-Path $env:LOCALAPPDATA 'Codex\logs'
$logPath = Join-Path $logDirectory 'fabricas-peticoes-github-sync.log'
$statusPath = Join-Path $PSScriptRoot 'STATUS_SYNC.md'
$mutex = [System.Threading.Mutex]::new($false, 'Local\FabricasPeticoesGitHubSync')
$hasLock = $false

# GitHub recusa arquivo acima de 100 MB. A margem existe porque o limite é do
# objeto após compressão de transporte e não vale confiar no fio da navalha.
$limiteBytes = 95MB

# Declarado aqui, e não dentro do try, porque o bloco catch o consome: com
# Set-StrictMode, variável não inicializada faz o tratamento de erro estourar e
# engolir o erro original.
$grandes = @()

[System.IO.Directory]::CreateDirectory($logDirectory) | Out-Null

function Write-SyncLog {
    param([string]$Message)
    $line = '{0:u} {1}' -f (Get-Date), $Message
    Add-Content -LiteralPath $logPath -Value $line -Encoding UTF8
    Write-Output $line
}

function Write-SyncStatus {
    param([string]$Situacao, [string]$Detalhe, [string[]]$Grandes = @())
    # O log fica num diretório que ninguém visita. Este arquivo fica dentro do
    # repositório, ao lado do script, e é onde o operador de fato olha.
    $texto = @(
        '# Última sincronização com o GitHub',
        '',
        ('**{0}** — {1:yyyy-MM-dd HH:mm:ss}' -f $Situacao, (Get-Date)),
        '',
        $Detalhe
    )
    if ($Grandes.Count -gt 0) {
        $texto += @('', '## Arquivos deixados de fora por excederem o limite do GitHub', '')
        foreach ($g in $Grandes) { $texto += "- $g" }
        $texto += @(
            '',
            'Estes arquivos permanecem no disco e **não** foram versionados. Para levá-los',
            'ao GitHub use a rota de assets grandes (`publish_large_assets.ps1`,',
            '`split_oversized_file.ps1`), ou decida que eles não pertencem a este repositório.'
        )
    }
    Set-Content -LiteralPath $statusPath -Value ($texto -join "`n") -Encoding UTF8
}

try {
    $hasLock = $mutex.WaitOne(0)
    if (-not $hasLock) {
        Write-SyncLog 'Sincronização já está em execução; esta chamada foi ignorada.'
        exit 0
    }

    # (1) A automação só age em `main`.
    $branch = (& git -C $repositoryRoot rev-parse --abbrev-ref HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Não foi possível determinar o branch corrente.' }
    if ($branch -ne 'main') {
        $msg = "Checkout em '$branch', não em 'main'. Sincronização adiada para não varrer trabalho em curso."
        Write-SyncLog $msg
        Write-SyncStatus -Situacao 'ADIADA' -Detalhe $msg
        exit 0
    }

    & (Join-Path $PSScriptRoot 'refresh_large_assets_manifest.ps1') -RepositoryRoot $repositoryRoot

    & git -C $repositoryRoot add -A
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao preparar as alterações para o commit.' }

    # (2) Retirar do commit o que o GitHub recusaria. Feito DEPOIS do `add -A`
    # porque é o índice que diz o que de fato entraria, e não o disco.
    $preparados = @(& git -C $repositoryRoot diff --cached --name-only --diff-filter=ACMR)
    foreach ($relativo in $preparados) {
        if ([string]::IsNullOrWhiteSpace($relativo)) { continue }
        $absoluto = Join-Path $repositoryRoot $relativo
        if (-not (Test-Path -LiteralPath $absoluto -PathType Leaf)) { continue }
        $tamanho = (Get-Item -LiteralPath $absoluto).Length
        if ($tamanho -gt $limiteBytes) {
            & git -C $repositoryRoot reset --quiet -- $relativo
            $grandes += ('{0:N1} MB — {1}' -f ($tamanho / 1MB), $relativo)
        }
    }
    if ($grandes.Count -gt 0) {
        Write-SyncLog ("{0} arquivo(s) acima de {1:N0} MB retirados do commit; o push morreria neles." -f $grandes.Count, ($limiteBytes / 1MB))
        foreach ($g in $grandes) { Write-SyncLog "  fora: $g" }
    }

    & git -C $repositoryRoot diff --cached --quiet
    if ($LASTEXITCODE -eq 1) {
        $message = 'sync: {0:yyyy-MM-dd HH:mm:ss}' -f (Get-Date)
        # (3) Identidade própria da automação, só para este commit.
        & git -C $repositoryRoot `
            -c user.name='FORJA sync' `
            -c user.email='forja-sync@localhost' `
            commit -m $message
        if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar o commit.' }

        & git -C $repositoryRoot push origin main
        if ($LASTEXITCODE -ne 0) { throw 'Falha ao enviar o commit ao GitHub.' }
        Write-SyncLog "Commit enviado: $message"
    }
    elseif ($LASTEXITCODE -ne 0) {
        throw 'Falha ao verificar as alterações preparadas.'
    }
    else {
        Write-SyncLog 'Nenhuma alteração Git pendente.'
    }

    & (Join-Path $PSScriptRoot 'publish_large_assets.ps1') -RepositoryRoot $repositoryRoot

    $atras = (& git -C $repositoryRoot rev-list --count 'origin/main..main' 2>$null)
    $detalhe = if ($atras -and [int]$atras -gt 0) {
        "Sincronização concluída, mas `main` continua $atras commit(s) à frente de `origin/main`."
    } else {
        'Sincronização concluída; o remoto está em dia com o local.'
    }
    Write-SyncLog $detalhe
    Write-SyncStatus -Situacao 'OK' -Detalhe $detalhe -Grandes $grandes
}
catch {
    $erro = $_.Exception.Message
    Write-SyncLog ("ERRO: {0}" -f $erro)
    # Falha de rotina de segurança precisa gritar onde o operador está. Enquanto
    # o erro só existia no log, o GitHub pareceu ser cópia de segurança do acervo
    # por cinco dias sem ser.
    Write-SyncStatus -Situacao 'FALHOU' -Detalhe ("A sincronização não terminou: $erro`n`nEnquanto isto não for resolvido, o GitHub **não** é cópia de segurança atual deste repositório.") -Grandes $grandes
    throw
}
finally {
    if ($hasLock) { $mutex.ReleaseMutex() }
    $mutex.Dispose()
}

#>
