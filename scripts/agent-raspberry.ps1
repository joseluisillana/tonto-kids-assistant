[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("preflight", "exec")]
    [string]$Action,

    [string]$Command
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-EnvOrDefault {
    param(
        [string]$Name,
        [string]$DefaultValue
    )

    $Value = [Environment]::GetEnvironmentVariable($Name)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        return $DefaultValue
    }

    return $Value
}

function ConvertTo-BashSingleQuoted {
    param([string]$Value)

    return "'" + ($Value -replace "'", "'\''") + "'"
}

function Assert-LocalSshReady {
    if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) {
        throw "OpenSSH client 'ssh' was not found."
    }

    if (-not (Test-Path -LiteralPath $PiSshKey)) {
        throw "Dedicated SSH key not found at $PiSshKey. Generate and install it before running Raspberry agent commands."
    }
}

function New-RemoteRepoBootstrap {
    $QuotedRepo = ConvertTo-BashSingleQuoted -Value $PiRepo

    return @"
repo=$QuotedRepo
if [ "`$repo" != "`${repo#\~/}" ]; then
  repo="`$HOME/`${repo#\~/}"
fi
if [ ! -d "`$repo" ]; then
  echo "Raspberry repo not found: `$repo" >&2
  exit 1
fi
cd "`$repo"
"@
}

function Invoke-RaspberrySsh {
    param([string]$RemoteCommand)

    $SshTarget = "${PiUser}@${PiHost}"
    $NormalizedCommand = ($RemoteCommand -replace "`r`n", "`n").Trim()
    $RemoteShellCommand = "sh -lc " + (ConvertTo-BashSingleQuoted -Value $NormalizedCommand)
    $SshArgs = @(
        "-o", "BatchMode=yes",
        "-o", "IdentitiesOnly=yes",
        "-o", "ConnectTimeout=5",
        "-i", $PiSshKey,
        $SshTarget,
        $RemoteShellCommand
    )

    & ssh @SshArgs
}

function Invoke-RaspberryPreflight {
    $BackendUrl = Get-EnvOrDefault -Name "TONTO_BACKEND_URL" -DefaultValue ""
    $QuotedBackendUrl = ConvertTo-BashSingleQuoted -Value $BackendUrl
    $RepoBootstrap = New-RemoteRepoBootstrap

    $RemoteCommand = @"
set -eu
echo "== identity =="
hostname
whoami

echo "== repository =="
$RepoBootstrap
pwd
git status --short --branch

echo "== tools =="
missing=0
for tool in git python3 curl arecord aplay espeak; do
  if command -v "`$tool" >/dev/null 2>&1; then
    command -v "`$tool"
  else
    echo "missing: `$tool" >&2
    missing=1
  fi
done
if [ "`$missing" -ne 0 ]; then
  exit 1
fi

echo "== python environment =="
if [ ! -x ".venv/bin/python" ]; then
  echo "missing: .venv/bin/python" >&2
  exit 1
fi
.venv/bin/python --version
.venv/bin/python -c 'import sys; print(sys.executable)'

backend_url=$QuotedBackendUrl
if [ -n "`$backend_url" ]; then
  echo "== backend health =="
  backend_url="`${backend_url%/}"
  echo "Checking `$backend_url/health"
  curl --fail --silent --show-error --connect-timeout 5 --max-time 10 "`$backend_url/health"
  echo
fi
"@

    Invoke-RaspberrySsh -RemoteCommand $RemoteCommand
    exit $LASTEXITCODE
}

function Invoke-RaspberryExec {
    if ([string]::IsNullOrWhiteSpace($Command)) {
        throw "-Command is required when -Action exec is used."
    }

    $RepoBootstrap = New-RemoteRepoBootstrap
    $RemoteCommand = @"
set -eu
$RepoBootstrap
$Command
"@

    Invoke-RaspberrySsh -RemoteCommand $RemoteCommand
    exit $LASTEXITCODE
}

$DefaultKey = Join-Path (Join-Path $HOME ".ssh") "tonto_agent_ed25519"
$PiHost = Get-EnvOrDefault -Name "TONTO_PI_HOST" -DefaultValue "tonto-pi.local"
$PiUser = Get-EnvOrDefault -Name "TONTO_PI_USER" -DefaultValue "tonto-pi-user"
$PiSshKey = Get-EnvOrDefault -Name "TONTO_PI_SSH_KEY" -DefaultValue $DefaultKey
$PiRepo = Get-EnvOrDefault -Name "TONTO_PI_REPO" -DefaultValue "~/tonto-kids-assistant"

if ($Action -eq "exec" -and [string]::IsNullOrWhiteSpace($Command)) {
    throw "-Command is required when -Action exec is used."
}

Assert-LocalSshReady

switch ($Action) {
    "preflight" { Invoke-RaspberryPreflight }
    "exec" { Invoke-RaspberryExec }
}
