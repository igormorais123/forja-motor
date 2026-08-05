$ErrorActionPreference = "Stop"
Write-Host "Abrindo login local do Gmail/Google Workspace. Entre com a conta correta e autorize o acesso."
$GwsCmd = Join-Path $env:APPDATA "npm\gws.cmd"
if (Test-Path -LiteralPath $GwsCmd) {
  & $GwsCmd auth login
} else {
  gws auth login
}
Write-Host "Login finalizado. Volte ao painel e clique em Atualizar agora."
