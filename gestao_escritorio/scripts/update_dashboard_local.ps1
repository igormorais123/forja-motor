param(
  [ValidateSet("Manual","Automation","Startup")]
  [string]$Mode = "Manual"
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Workspace = Split-Path -Parent $Root
$DataPath = Join-Path $Root "data\demandas.json"
$StatusPath = Join-Path $Root "data\status_integracoes.json"
$WhatsappPath = Join-Path $Root "data\whatsapp_candidates.json"
$DeliveriesPath = Join-Path $Root "data\entregas_fabio_osorio.json"
$ForjaStatusPath = Join-Path $Root "data\forja_status.json"
$AlertStatePath = Join-Path $Root "data\last_alerts.json"
$ApplyManualPath = Join-Path $Root "scripts\apply_manual_updates.py"
$HermesBridgePath = Join-Path $Root "scripts\hermes_bridge.py"
$ForjaSyncPath = Join-Path $Root "scripts\sync_forja_gestao.py"
$RunStartedAt = Get-Date

function Get-PythonExecutable {
  $candidate = Get-Command python -ErrorAction SilentlyContinue
  if ($candidate) { return $candidate.Source }
  $known = "C:\Python314\python.exe"
  if (Test-Path -LiteralPath $known) { return $known }
  throw "Python nao encontrado."
}

function Write-JsonAtomic {
  param([string]$Path, $Value, [int]$Depth = 12)
  $temp = "$Path.$([guid]::NewGuid().ToString('N')).tmp"
  try {
    $json = $Value | ConvertTo-Json -Depth $Depth
    [System.IO.File]::WriteAllText($temp, $json + [Environment]::NewLine, (New-Object System.Text.UTF8Encoding($false)))
    Move-Item -LiteralPath $temp -Destination $Path -Force
  } finally {
    if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Force -ErrorAction SilentlyContinue }
  }
}

$Python = Get-PythonExecutable

function Get-NowIso {
  return (Get-Date).ToString("yyyy-MM-ddTHH:mm:sszzz")
}

function Invoke-JsonCommand {
  param([scriptblock]$Block)
  try {
    $out = & $Block 2>$null
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) { throw "exit $LASTEXITCODE" }
    return @{ ok = $true; raw = ($out -join "`n") }
  } catch {
    return @{ ok = $false; error = $_.Exception.Message }
  }
}

function Update-LocalDemandState {
  param($DemandData)
  foreach ($item in $DemandData.demandas) {
    if (-not $item.pasta) { continue }
    $folder = Join-Path $Workspace $item.pasta
    $attachDir = Join-Path $folder "Anexos do email"
    $control = Join-Path $folder "ANEXOS_EMAIL_RECEBIDOS_OU_PENDENTES.txt"
    if (-not $item.PSObject.Properties.Name.Contains("local")) {
      $item | Add-Member -NotePropertyName local -NotePropertyValue ([pscustomobject]@{})
    }
    $item.local | Add-Member -Force -NotePropertyName folderExists -NotePropertyValue (Test-Path -LiteralPath $folder)
    $commandExists = $false
    if (Test-Path -LiteralPath $folder) {
      $commandExists = ((Get-ChildItem -LiteralPath $folder -File -Filter "COMANDO*.md" -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0)
    }
    $item.local | Add-Member -Force -NotePropertyName comandoMd -NotePropertyValue $commandExists
    $item.local | Add-Member -Force -NotePropertyName anexosControle -NotePropertyValue (Test-Path -LiteralPath $control)
    if (Test-Path -LiteralPath $attachDir) {
      $item.local | Add-Member -Force -NotePropertyName anexosDiretosNoDisco -NotePropertyValue ((Get-ChildItem -LiteralPath $attachDir -File -ErrorAction SilentlyContinue | Measure-Object).Count)
    } else {
      $item.local | Add-Member -Force -NotePropertyName anexosDiretosNoDisco -NotePropertyValue 0
    }
  }
}

function Sync-WhatsappDemandCards {
  param($DemandData)
  if (-not (Test-Path -LiteralPath $WhatsappPath)) { return }
  try {
    $wa = Get-Content -LiteralPath $WhatsappPath -Raw -Encoding UTF8 | ConvertFrom-Json
  } catch {
    return
  }
  foreach ($candidate in $wa.candidates) {
    $mediaNeedsReview = ($candidate.PSObject.Properties.Name.Contains("audioMissingMediaWindow") -and [int]$candidate.audioMissingMediaWindow -gt 0)
    if ([int]$candidate.candidateDemandMessages -le 0 -and -not [bool]$candidate.unansweredHint -and -not $mediaNeedsReview) { continue }
    $isFabio = ($candidate.chatId -eq "60855441973370@lid")
    $slug = if ($isFabio) { "fabio-medina-osorio" } else { "igor-hermes-contexto" }
    $folderName = if ($isFabio) { "WhatsApp - Fabio Medina Osorio - triagem de demandas" } else { "WhatsApp - Igor Hermes - contexto de organizacao" }
    $id = "whatsapp-$slug"
    $folder = Join-Path $Workspace $folderName
    $commandPath = Join-Path $folder "COMANDO_DO_WHATSAPP.md"
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
    $keywords = @($candidate.keywords) -join ", "
    $audioLine = ""
    if ($candidate.PSObject.Properties.Name.Contains("audioIncomingWindow") -and [int]$candidate.audioIncomingWindow -gt 0) {
      $audioLine = "recebidos=$($candidate.audioIncomingWindow); com caminho registrado=$($candidate.audioPathRecordedWindow); materializados na origem consultada=$($candidate.audioMaterializedWindow); sem arquivo acessivel=$($candidate.audioMissingMediaWindow); ultimo audio=$($candidate.audioLastAt)"
    }
    $mediaObservation = if ($mediaNeedsReview) { "WhatsApp processado em modo sanitizado; ha $($candidate.audioMissingMediaWindow) audio(s) recebido(s) sem arquivo acessivel na origem consultada. Triar relevancia; se algum for essencial, recuperar/requisitar reenvio e manter a demanda especifica aberta." } elseif ($candidate.PSObject.Properties.Name.Contains("audioIncomingWindow") -and [int]$candidate.audioIncomingWindow -gt 0) { "WhatsApp processado em modo sanitizado; ha $($candidate.audioIncomingWindow) audio(s) recebido(s), todos com materializacao indicada, para revisar/transcrever." } else { "WhatsApp processado em modo sanitizado; revisar conversa para anexos ou arquivos recebidos." }
    $commandText = @"
# Comando originado de WhatsApp (sanitizado)

Origem: WhatsApp/Hermes
Contato: $($candidate.chatName)
ChatId: $($candidate.chatId)
Atualizado: $(Get-NowIso)

Resumo operacional:
$($candidate.summary)

Sinais de demanda:
- mensagens analisadas na janela: $($candidate.messagesWindow)
- mensagens recebidas na janela: $($candidate.incomingWindow)
- mensagens enviadas na janela: $($candidate.outgoingWindow)
- sinais por palavra-chave nas mensagens recebidas: $($candidate.candidateDemandMessages)
- palavras-chave detectadas: $keywords
- audios recebidos: $audioLine
- midias recebidas sem arquivo acessivel: $($candidate.incomingMediaMissingWindow)
- ultima mensagem recebida: $($candidate.lastIncomingAt)
- ultima mensagem enviada: $($candidate.lastOutgoingAt)
- pendencia aparente de resposta: $($candidate.unansweredHint)
- pendencia de materializacao para triagem: $mediaNeedsReview

Tarefa:
Abrir a conversa correspondente no WhatsApp/Hermes, classificar o pedido concreto, criar uma demanda especifica no painel quando houver pedido de peca, peticao, parecer, memoriais, prazo ou documento, e anexar documentos recebidos por canal seguro quando existirem. Midia registrada sem arquivo acessivel nao pode ser tratada como lida. Este arquivo nao transcreve conversa bruta.
"@
    $commandText | Set-Content -LiteralPath $commandPath -Encoding UTF8

    $existing = @($DemandData.demandas | Where-Object { $_.id -eq $id }) | Select-Object -First 1
    $urgency = if ([bool]$candidate.unansweredHint) { "alta" } else { "media" }
    $title = if ($isFabio) { "WhatsApp - Fabio Medina Osorio - revisar demanda recente" } else { "WhatsApp - Igor Hermes - revisar organizacao/contexto" }
    $case = if ($isFabio) { "Fabio Medina Osorio / escritorio" } else { "Igor Hermes / contexto de organizacao" }
    $next = if ($mediaNeedsReview) { "Triar os audios sem arquivo acessivel; se algum for essencial a uma demanda especifica, recuperar ou solicitar reenvio antes do fechamento." } elseif ($isFabio) { "Abrir o WhatsApp do Fabio, confirmar o pedido concreto e transformar em tarefa especifica se houver peca ou prazo." } else { "Abrir a conversa de contexto Igor/Hermes e aproveitar apenas o que ajudar a organizar as demandas do escritorio." }
    if ($null -eq $existing) {
      $newItem = [pscustomobject][ordered]@{
        id = $id
        titulo = $title
        clienteOuCaso = $case
        origem = "whatsapp"
        emailsRecebidos = @()
        emailsResposta = @()
        pasta = $folderName
        recebidoEm = if ($candidate.lastIncomingAt) { $candidate.lastIncomingAt } else { $candidate.lastAt }
        prazo = $null
        prazoTexto = "sem prazo extraido automaticamente; revisar conversa"
        resumo = $candidate.summary
        proximaAcao = $next
        status = "aberta"
        respondidoComConteudo = $false
        evidenciaResposta = ""
        urgenciaManual = $urgency
        anexos = [pscustomobject][ordered]@{
          diretosBaixados = $null
          diretosEsperados = $null
          externosPendentes = $true
          observacao = $mediaObservation
        }
        tags = @("WhatsApp", "Hermes", "triagem", $(if ($isFabio) { "chefe do escritorio" } else { "contexto" }))
      }
      $DemandData.demandas += $newItem
    } else {
      $existing.recebidoEm = if ($candidate.lastIncomingAt) { $candidate.lastIncomingAt } else { $candidate.lastAt }
      $existing.resumo = $candidate.summary
      $existing.proximaAcao = $next
      $existing.urgenciaManual = $urgency
      # O cartão genérico de triagem representa a conversa, não cada nova demanda.
      # Uma baixa auditada não pode ser revertida só porque o retrato sanitizado
      # voltou a encontrar palavras-chave no mesmo chat. Novos pedidos concretos
      # entram como demanda própria pelo e-mail, pela fila Hermes ou manualmente.
      if ($existing.status -ne "cumprida") {
        $existing.status = "aberta"
        $existing.respondidoComConteudo = $false
      }
      $existing.pasta = $folderName
      $existing.prazoTexto = "sem prazo extraido automaticamente; revisar conversa"
      $existing.anexos.observacao = $mediaObservation
    }
  }
}

$data = Get-Content -LiteralPath $DataPath -Raw -Encoding UTF8 | ConvertFrom-Json
$data.updatedAt = Get-NowIso

Update-LocalDemandState -DemandData $data

$whatsappStatus = Invoke-JsonCommand { & "C:\Users\IgorPC\.hermes\bin\hermes-whatsapp-personal-access.ps1" -Action status }
# O guardião pode reiniciar o coletor quando detecta a sessão desconectada e,
# nessa janela curta, devolver exit 1 mesmo com o QR já pronto. Uma segunda
# leitura bounded separa essa corrida transitória de falha real.
if (-not $whatsappStatus.ok) {
  Start-Sleep -Seconds 1
  $whatsappStatus = Invoke-JsonCommand { & "C:\Users\IgorPC\.hermes\bin\hermes-whatsapp-personal-access.ps1" -Action status }
}
$phoneHealth = Invoke-JsonCommand { & "C:\Users\IgorPC\.hermes\bin\codex-phone.ps1" -Action health }

$status = [ordered]@{
  updatedAt = Get-NowIso
  mode = $Mode
  gmailLocal = [ordered]@{
    ok = $false
    state = "nao_verificado"
    authRequired = $false
  }
  whatsappPersonal = [ordered]@{
    ok = $false
    state = "nao_verificado"
  }
  phoneAlert = [ordered]@{
    ok = $false
    state = "nao_verificado"
  }
  calendar = [ordered]@{
    ok = $true
    state = "diario_9h"
    title = "Revisar painel de demandas do escritorio"
    eventId = "ng681949ks18rfb9q00e9p6uh8"
    schedule = "Diariamente as 9h"
    url = "https://www.google.com/calendar/event?eid=bmc2ODE5NDlrczE4cmZiOXEwMGU5cDZ1aDhfMjAyNjA3MDhUMTIwMDAwWiB2aWN0b3Jtb3JhaXN2YXNjb25jZWxvc0Bt"
  }
  deliveries = [ordered]@{
    ok = $false
    state = "nao_verificado"
  }
  hermesBridge = [ordered]@{
    ok = $false
    state = "nao_verificado"
  }
}

$gmailUpdater = Join-Path $Root "scripts\gmail_gws_update.py"
$GwsAvailable = (Test-Path -LiteralPath (Join-Path $HOME "AppData\Roaming\npm\gws.cmd")) -or [bool](Get-Command gws -ErrorAction SilentlyContinue)
if ($GwsAvailable) {
  try {
    $gmailRaw = & $Python $gmailUpdater --root $Root 2>$null
    if ($gmailRaw) {
      $gmailStatus = ($gmailRaw -join "`n") | ConvertFrom-Json
      $status.gmailLocal.ok = [bool]$gmailStatus.ok
      $status.gmailLocal.state = if ($gmailStatus.ok) { "ok" } elseif ($gmailStatus.authRequired) { "precisa_login" } else { "erro" }
      $status.gmailLocal.authRequired = [bool]$gmailStatus.authRequired
      $status.gmailLocal.message = $gmailStatus.message
      $status.gmailLocal.newInbound = $gmailStatus.newInbound
      $status.gmailLocal.sentScanned = $gmailStatus.sentScanned
      $status.gmailLocal.responsesMarked = $gmailStatus.responsesMarked
      $status.gmailLocal.responsesRepaired = $gmailStatus.responsesRepaired
      $status.gmailLocal.attachmentsExpected = $gmailStatus.attachmentsExpected
      $status.gmailLocal.attachmentsDownloaded = $gmailStatus.attachmentsDownloaded
      $status.gmailLocal.attachmentErrors = $gmailStatus.attachmentErrors
      if ($gmailStatus.error) { $status.gmailLocal.error = $gmailStatus.error }
      $data = Get-Content -LiteralPath $DataPath -Raw -Encoding UTF8 | ConvertFrom-Json
      $data.updatedAt = Get-NowIso
      Update-LocalDemandState -DemandData $data
    }
  } catch {
    $status.gmailLocal.state = "erro"
    $status.gmailLocal.error = $_.Exception.Message
  }
} else {
  $status.gmailLocal.state = "gws_nao_encontrado"
  $status.gmailLocal.message = "CLI gws nao encontrado no PATH."
}

$deliveryAuditor = Join-Path $Root "scripts\audit_delivered_docs.py"
if ($GwsAvailable) {
  try {
    $deliveryRaw = & $Python $deliveryAuditor 2>$null
    if ($deliveryRaw) {
      $deliveryStatus = ($deliveryRaw -join "`n") | ConvertFrom-Json
      $status.deliveries.ok = [bool]$deliveryStatus.ok
      $status.deliveries.state = if ($deliveryStatus.ok) { "ok" } elseif ($deliveryStatus.authRequired) { "precisa_login" } else { "erro" }
      $status.deliveries.sentScanned = $deliveryStatus.sentScanned
      $status.deliveries.deliveriesFound = $deliveryStatus.deliveriesFound
      $status.deliveries.attachmentsExpected = $deliveryStatus.attachmentsExpected
      $status.deliveries.attachmentsDownloaded = $deliveryStatus.attachmentsDownloaded
      $status.deliveries.attachmentErrors = $deliveryStatus.attachmentErrors
      $status.deliveries.report = $deliveryStatus.report
      $status.deliveries.archiveFolder = $deliveryStatus.archiveFolder
      if ($deliveryStatus.error) { $status.deliveries.error = $deliveryStatus.error }
    }
  } catch {
    $status.deliveries.state = "erro"
    $status.deliveries.error = $_.Exception.Message
  }
}

if ($whatsappStatus.ok) {
  $status.whatsappPersonal.ok = ($whatsappStatus.raw -match "state=connected" -and $whatsappStatus.raw -match "connected=True")
  $status.whatsappPersonal.state = if ($status.whatsappPersonal.ok) { "connected" } else { "verificar" }
  $status.whatsappPersonal.summary = (($whatsappStatus.raw -split "`n") | Select-Object -First 3) -join " | "
} else {
  $status.whatsappPersonal.state = "erro"
  $status.whatsappPersonal.error = $whatsappStatus.error
}

if ($phoneHealth.ok) {
  try {
    $phone = $phoneHealth.raw | ConvertFrom-Json
    $status.phoneAlert.ok = [bool]$phone.ok
    $status.phoneAlert.state = $phone.operational_channel
    $status.phoneAlert.degraded = $phone.android_alert_degraded
  } catch {
    $status.phoneAlert.ok = ($phoneHealth.raw -match '"ok":\s*true')
    $status.phoneAlert.state = "macrodroid"
  }
} else {
  $status.phoneAlert.state = "erro"
  $status.phoneAlert.error = $phoneHealth.error
}

$remotePy = @'
import sqlite3, json, datetime, os, re
path='/root/.hermes/state/whatsapp-personal/messages.sqlite'
targets=[
  ('60855441973370@lid','Fabio Medina Osorio'),
  ('168032760508457@lid','ClawdBot - INTEIA - Igor')
]
keywords=['prazo','urgente','hoje','amanha','peticao','peca','memoriais','parecer','recurso','embargos','minuta','anexo','processo','protocolo']
now=datetime.datetime.now(datetime.timezone.utc)
cut=int((now-datetime.timedelta(hours=96)).timestamp())
conn=sqlite3.connect(path)
conn.row_factory=sqlite3.Row
out=[]
for chat_id, label in targets:
    rows=list(conn.execute("""
      select chat_id, chat_name, sender_name, direction, timestamp, body, has_media, message_type, media_type, media_paths
      from messages
      where chat_id=? and timestamp>=?
      order by timestamp desc
      limit 200
    """, (chat_id, cut)))
    incoming=[r for r in rows if str(r['direction']).lower() in ('in','incoming','from_contact','received')]
    outgoing=[r for r in rows if str(r['direction']).lower() in ('out','outgoing','sent','from_me')]
    kw_hits={}
    candidate_count=0
    last_candidate_ts=None
    audio_rows=[]
    for r in incoming:
        body=(r['body'] or '').lower()
        hits=[k for k in keywords if k in body]
        if hits:
            candidate_count += 1
            last_candidate_ts = max(last_candidate_ts or 0, int(r['timestamp'] or 0))
            for h in hits:
                kw_hits[h]=kw_hits.get(h,0)+1
        mt=(r['message_type'] or '').lower()
        media=(r['media_type'] or '').lower()
        if int(r['has_media'] or 0) and ('audio' in mt or 'audio' in media or 'ptt' in mt or 'ptt' in media):
            audio_rows.append(r)
    def media_paths(row):
        raw=row['media_paths']
        if not raw:
            return []
        try:
            parsed=json.loads(raw)
        except (TypeError, json.JSONDecodeError):
            parsed=raw
        if isinstance(parsed, dict):
            parsed=list(parsed.values())
        if not isinstance(parsed, list):
            parsed=[parsed]
        return [str(p) for p in parsed if p]
    def has_materialized_media(row):
        return any(os.path.isfile(p) for p in media_paths(row))
    incoming_media=[r for r in incoming if int(r['has_media'] or 0)]
    incoming_media_with_path=[r for r in incoming_media if media_paths(r)]
    incoming_media_missing=[r for r in incoming_media if not has_materialized_media(r)]
    audio_with_path=[r for r in audio_rows if media_paths(r)]
    audio_materialized=[r for r in audio_rows if has_materialized_media(r)]
    audio_missing=[r for r in audio_rows if not has_materialized_media(r)]
    last_ts=max([int(r['timestamp'] or 0) for r in rows], default=None)
    last_in=max([int(r['timestamp'] or 0) for r in incoming], default=None)
    last_out=max([int(r['timestamp'] or 0) for r in outgoing], default=None)
    def fmt(ts):
        if not ts: return None
        return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=-3))).isoformat()
    audio_last=max([int(r['timestamp'] or 0) for r in audio_rows], default=None)
    summary = 'Ha sinais de demanda/prazo em mensagens recebidas no periodo recente; revisar conversa no WhatsApp.' if candidate_count else 'Sem sinal forte de nova demanda por palavra-chave nas mensagens recebidas no periodo recente.'
    if audio_rows:
        summary = f'{summary} Ha {len(audio_rows)} audio(s) recebido(s) que precisam de triagem/transcricao.'
    if audio_missing:
        summary = f'{summary} Pendencia de triagem: {len(audio_missing)} audio(s) recebido(s) nao possuem arquivo acessivel na origem consultada; se algum for essencial, ele bloqueia a demanda especifica.'
    out.append({
      'chatId': chat_id,
      'chatName': label,
      'messagesWindow': len(rows),
      'incomingWindow': len(incoming),
      'outgoingWindow': len(outgoing),
      'lastAt': fmt(last_ts),
      'lastIncomingAt': fmt(last_in),
      'lastOutgoingAt': fmt(last_out),
      'candidateDemandMessages': candidate_count,
      'keywords': sorted(kw_hits.keys())[:12],
      'summary': summary,
      'unansweredHint': bool(last_in and (not last_out or last_out < last_in)),
      'audioIncomingWindow': len(audio_rows),
      'audioPathRecordedWindow': len(audio_with_path),
      'audioMaterializedWindow': len(audio_materialized),
      'audioMissingMediaWindow': len(audio_missing),
      'incomingMediaWindow': len(incoming_media),
      'incomingMediaPathRecordedWindow': len(incoming_media_with_path),
      'incomingMediaMissingWindow': len(incoming_media_missing),
      'audioLastAt': fmt(audio_last)
    })
print(json.dumps({'updatedAt': datetime.datetime.now().astimezone().isoformat(), 'privacy':'sanitized-no-raw-chat', 'candidates': out}, ensure_ascii=True))
'@

$status.whatsappPersonal.sanitizedExport = [ordered]@{ ok = $false; state = "nao_verificado" }
try {
  $waJson = $remotePy | & ssh -o BatchMode=yes -o ConnectTimeout=12 hermes python3 -
  if ($LASTEXITCODE -ne 0 -or -not $waJson) { throw "export sanitizado indisponivel" }
  $waPayload = ($waJson -join "`n") | ConvertFrom-Json
  if ($waPayload.privacy -ne "sanitized-no-raw-chat") { throw "contrato de privacidade ausente" }
  Write-JsonAtomic -Path $WhatsappPath -Value $waPayload -Depth 8
  $status.whatsappPersonal.sanitizedExport.ok = $true
  $status.whatsappPersonal.sanitizedExport.state = "ok"
  $status.whatsappPersonal.sanitizedExport.updatedAt = $waPayload.updatedAt
} catch {
  $status.whatsappPersonal.sanitizedExport.state = "ultimo_retrato_preservado"
  $status.whatsappPersonal.sanitizedExport.error = $_.Exception.Message
}

Sync-WhatsappDemandCards -DemandData $data
Update-LocalDemandState -DemandData $data

Write-JsonAtomic -Path $DataPath -Value $data -Depth 12
if (Test-Path -LiteralPath $ApplyManualPath) {
  & $Python $ApplyManualPath | Out-Null
  $data = Get-Content -LiteralPath $DataPath -Raw -Encoding UTF8 | ConvertFrom-Json
}
if (Test-Path -LiteralPath $HermesBridgePath) {
  & $Python $HermesBridgePath --ssh-alias hermes --quiet sync | Out-Null
  $bridgeExit = $LASTEXITCODE
  $bridgeStatusPath = Join-Path $Root "data\hermes_bridge_status.json"
  if (Test-Path -LiteralPath $bridgeStatusPath) {
    try {
      $bridgeStatus = Get-Content -LiteralPath $bridgeStatusPath -Raw -Encoding UTF8 | ConvertFrom-Json
      $status.hermesBridge.ok = [bool]$bridgeStatus.ok
      $status.hermesBridge.state = if ($bridgeStatus.ok) { "ok" } else { "erro" }
      $status.hermesBridge.updatedAt = $bridgeStatus.updatedAt
      if ($bridgeStatus.error) { $status.hermesBridge.error = $bridgeStatus.error }
    } catch {
      $status.hermesBridge.state = "estado_invalido"
      $status.hermesBridge.error = $_.Exception.Message
    }
  } elseif ($bridgeExit -ne 0) {
    $status.hermesBridge.state = "erro"
  }
  $data = Get-Content -LiteralPath $DataPath -Raw -Encoding UTF8 | ConvertFrom-Json
}
$status.forjaSidecar = [ordered]@{ ok = $false; state = "nao_verificado" }
if (Test-Path -LiteralPath $ForjaSyncPath) {
  try {
    & $Python $ForjaSyncPath --reconcile --apply | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "sincronizacao N3 terminou com exit $LASTEXITCODE" }
    & $Python $ForjaSyncPath --legacy --apply | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "sincronizacao FORJA terminou com exit $LASTEXITCODE" }
    $status.forjaSidecar.ok = $true
    $status.forjaSidecar.state = "ok"
    $status.forjaSidecar.updatedAt = Get-NowIso
    if (Test-Path -LiteralPath $ForjaStatusPath) {
      $forjaPayload = Get-Content -LiteralPath $ForjaStatusPath -Raw -Encoding UTF8 | ConvertFrom-Json
      $forjaByDemand = @{}
      foreach ($property in $forjaPayload.items.PSObject.Properties) {
        $forjaByDemand[$property.Name] = $property.Value
      }
      $linked = 0
      $conflicts = 0
      $artifactFailures = 0
      foreach ($item in $data.demandas) {
        if (-not $forjaByDemand.ContainsKey([string]$item.id)) { continue }
        $linked += 1
        $forjaItem = $forjaByDemand[[string]$item.id]
        $lifecycle = [string]$forjaItem.lifecycleStatus
        # Uma entrega interna ao escritório pode estar cumprida e, ao mesmo
        # tempo, a versão protocolável permanecer bloqueada por fonte material.
        # O enriquecimento do painel já reconhece essa separação; o resumo da
        # integração precisa usar a mesma regra para não fabricar divergência.
        $managementFulfilled = $item.status -eq "cumprida" -and -not [string]::IsNullOrWhiteSpace([string]$item.evidenciaResposta)
        if ($item.status -eq "cumprida" -and $lifecycle -in @("not_run","queued","running","blocked","ready_for_review","draft_awaiting_review") -and -not $managementFulfilled) { $conflicts += 1 }
        if ($item.status -eq "pronta_para_revisao" -and $lifecycle -notin @("ready_for_review","draft_awaiting_review")) { $conflicts += 1 }
        $auditArtifacts = ([string]$forjaItem.version).StartsWith("N3.0-r2") -or [string]$forjaItem.mode -eq "finalized_product_overlay"
        if ($auditArtifacts) {
          foreach ($artifact in @($forjaItem.artifacts)) {
            if ($artifact.PSObject.Properties.Name -contains "exists" -and -not [bool]$artifact.exists) { $artifactFailures += 1 }
          }
        }
      }
      $status.forjaSidecar.linked = $linked
      $status.forjaSidecar.total = @($data.demandas).Count
      $status.forjaSidecar.coveragePercent = if (@($data.demandas).Count) { [math]::Round(100 * $linked / @($data.demandas).Count, 1) } else { 100 }
      $status.forjaSidecar.conflicts = $conflicts
      $status.forjaSidecar.artifactFailures = $artifactFailures
      $status.forjaSidecar.message = "$linked/$(@($data.demandas).Count) demandas vinculadas; $conflicts divergencia(s); $artifactFailures artefato(s) ausente(s)."
    }
  } catch {
    $status.forjaSidecar.state = "pendente"
    $status.forjaSidecar.error = $_.Exception.Message
  }
}
$status.durationSeconds = [math]::Round(((Get-Date) - $RunStartedAt).TotalSeconds, 1)
Write-JsonAtomic -Path $StatusPath -Value $status -Depth 10

# FORJA FILA (R1.1 Helena, 12/07/2026): regenerar a fila priorizada com o demandas.json
# recem-atualizado, ANTES do render - o painel nasce com a fila fresca. So publica com a
# flag filaPriorizadaV1 ligada; falha da fila nunca derruba o ciclo de atualizacao.
try {
  & $Python (Join-Path (Split-Path $Root -Parent) "_FORJA_HARNESS\forja_fila.py") | Out-Null
} catch { }

& $Python (Join-Path $Root "scripts\render_dashboard.py") | Out-Null

$alertState = @{}
if (Test-Path -LiteralPath $AlertStatePath) {
  try {
    $savedAlertState = Get-Content -LiteralPath $AlertStatePath -Raw | ConvertFrom-Json
    foreach ($property in $savedAlertState.PSObject.Properties) { $alertState[$property.Name] = $property.Value }
  } catch { $alertState = @{} }
}
$today = (Get-Date).ToString("yyyy-MM-dd")
$openUrgent = @()
foreach ($item in $data.demandas) {
  if ($item.status -eq "cumprida") { continue }
  if (-not $item.prazo) { continue }
  $due = [datetime]::MinValue
  if (-not [datetime]::TryParseExact([string]$item.prazo, "yyyy-MM-dd", [Globalization.CultureInfo]::InvariantCulture, [Globalization.DateTimeStyles]::None, [ref]$due)) { continue }
  $hours = ($due.Date.AddHours(23).AddMinutes(59) - (Get-Date)).TotalHours
  if ($hours -le 48) { $openUrgent += $item }
}
if ($openUrgent.Count -gt 0 -and $status.phoneAlert.ok) {
  $key = "urgent-$today"
  if (-not $alertState.ContainsKey($key)) {
    $titles = ($openUrgent | Select-Object -First 3 | ForEach-Object { $_.titulo }) -join " | "
    $overdue = $openUrgent | Where-Object { ([datetime]::ParseExact($_.prazo, "yyyy-MM-dd", $null)).Date -lt (Get-Date).Date }
    if ($overdue.Count -gt 0) {
      & "C:\Users\IgorPC\.hermes\bin\codex-phone.ps1" -Action alarm -Message "Demandas vencidas do escritorio: $titles" | Out-Null
    } else {
      & "C:\Users\IgorPC\.hermes\bin\codex-phone.ps1" -Action notify -Title "Demandas urgentes do escritorio" -Message $titles -Severity important | Out-Null
    }
    $alertState[$key] = (Get-NowIso)
    Write-JsonAtomic -Path $AlertStatePath -Value $alertState -Depth 5
  }
}

[pscustomobject]@{
  ok = $true
  updatedAt = $data.updatedAt
  dashboard = (Join-Path $Root "painel_gestao_escritorio.html")
  demands = $data.demandas.Count
  whatsapp = $status.whatsappPersonal.state
  phoneAlert = $status.phoneAlert.state
  hermesBridge = $status.hermesBridge.state
  durationSeconds = $status.durationSeconds
} | ConvertTo-Json -Depth 5
