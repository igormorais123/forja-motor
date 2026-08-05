param(
  [string]$SshAlias = "hermes"
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

python (Join-Path $Root "scripts\hermes_bridge.py") --ssh-alias $SshAlias --install sync
