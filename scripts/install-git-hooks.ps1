[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$GitDir = Join-Path $RepoRoot ".git"
$HooksDir = Join-Path $GitDir "hooks"
$PreCommitPath = Join-Path $HooksDir "pre-commit"

if (-not (Test-Path $GitDir)) {
    throw "Git directory not found. Run this script from a cloned repository."
}

New-Item -ItemType Directory -Force -Path $HooksDir | Out-Null

$hook = @'
#!/bin/sh
set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"

if command -v pwsh >/dev/null 2>&1; then
  POWERSHELL_BIN="pwsh"
elif command -v powershell.exe >/dev/null 2>&1; then
  POWERSHELL_BIN="powershell.exe"
elif command -v powershell >/dev/null 2>&1; then
  POWERSHELL_BIN="powershell"
else
  echo "PowerShell was not found. Cannot export NotebookLM sources." >&2
  exit 1
fi

"$POWERSHELL_BIN" -NoProfile -ExecutionPolicy Bypass -File "$REPO_ROOT/scripts/export-docs-for-notebooklm.ps1"
'@

Set-Content -LiteralPath $PreCommitPath -Value $hook -Encoding ascii

Write-Host "Installed pre-commit hook at $PreCommitPath"
