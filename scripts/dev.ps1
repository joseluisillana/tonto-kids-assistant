[CmdletBinding()]
param(
    [ValidateSet("backend", "web", "all")]
    [string]$Service = "all",

    [switch]$AllowLan
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$VenvPython = if ($env:OS -eq "Windows_NT") {
    Join-Path (Join-Path (Join-Path $RepoRoot ".venv") "Scripts") "python.exe"
} else {
    Join-Path (Join-Path (Join-Path $RepoRoot ".venv") "bin") "python"
}

function Assert-DevEnvironment {
    if (-not (Test-Path $VenvPython)) {
        throw "Python virtual environment not found. Run ./scripts/setup-dev.ps1 first."
    }

    if (-not (Test-Path (Join-Path (Join-Path $RepoRoot "web") "node_modules"))) {
        throw "Web dependencies not found. Run ./scripts/setup-dev.ps1 first."
    }
}

function Start-Backend {
    Assert-DevEnvironment
    $BackendHost = if ($AllowLan) { "0.0.0.0" } else { "127.0.0.1" }
    $ReloadArgs = if ($env:TONTO_BACKEND_RELOAD -eq "0") { @() } else { @("--reload") }
    $BackendArgs = @("-m", "uvicorn", "backend.main:app", "--host", $BackendHost, "--port", "8000") + $ReloadArgs

    Write-Host "Starting backend on ${BackendHost}:8000"
    if ($AllowLan) {
        Write-Host "LAN mode enabled. Use the Windows PC IP or resolvable hostname in TONTO_BACKEND_URL from the Raspberry Pi."
        Write-Host "Example: TONTO_BACKEND_URL=http://<windows-pc-ip>:8000"
    }

    if ($env:TONTO_AGENT_BACKGROUND -eq "1") {
        $AgentPidPath = $env:TONTO_AGENT_BACKEND_PID_PATH
        $AgentOutLogPath = $env:TONTO_AGENT_BACKEND_OUT_LOG
        $AgentErrLogPath = $env:TONTO_AGENT_BACKEND_ERR_LOG

        if (-not $AgentPidPath -or -not $AgentOutLogPath -or -not $AgentErrLogPath) {
            throw "Agent background mode requires TONTO_AGENT_BACKEND_PID_PATH, TONTO_AGENT_BACKEND_OUT_LOG, and TONTO_AGENT_BACKEND_ERR_LOG."
        }

        $AgentDir = Split-Path -Parent $AgentPidPath
        $AgentRunnerPath = Join-Path $AgentDir "backend-runner.py"

        New-Item -ItemType Directory -Force -Path $AgentDir | Out-Null
        Set-Content -Path $AgentRunnerPath -Encoding utf8 -Value @"
import os
import sys

import uvicorn

sys.path.insert(0, os.getcwd())

out_log = os.environ["TONTO_AGENT_BACKEND_OUT_LOG"]
err_log = os.environ["TONTO_AGENT_BACKEND_ERR_LOG"]
host = os.environ["TONTO_AGENT_BACKEND_HOST"]

os.makedirs(os.path.dirname(out_log), exist_ok=True)
stdout = open(out_log, "a", buffering=1, encoding="utf-8")
stderr = open(err_log, "a", buffering=1, encoding="utf-8")
os.dup2(stdout.fileno(), 1)
os.dup2(stderr.fileno(), 2)
sys.stdout = stdout
sys.stderr = stderr

print(f"Starting backend on {host}:8000", flush=True)
uvicorn.run("backend.main:app", host=host, port=8000, reload=False)
"@

        $StartProcessParameters = @{
            FilePath = $VenvPython
            ArgumentList = @($AgentRunnerPath)
            WorkingDirectory = $RepoRoot
            PassThru = $true
        }
        if ($env:OS -eq "Windows_NT") {
            $StartProcessParameters.WindowStyle = "Hidden"
        }

        $Process = Start-Process @StartProcessParameters
        Set-Content -Path $AgentPidPath -Value $Process.Id -Encoding ascii
        return
    }

    Push-Location $RepoRoot
    try {
        & $VenvPython @BackendArgs
    } finally {
        Pop-Location
    }
}

function Start-Web {
    Assert-DevEnvironment
    $env:VITE_BACKEND_URL = "http://127.0.0.1:8000"
    Push-Location (Join-Path $RepoRoot "web")
    try {
        npm run dev -- --host 127.0.0.1 --port 5173
    } finally {
        Pop-Location
    }
}

function Start-ServiceWindow {
    param(
        [string]$WindowTitle,
        [string]$ScriptCommand
    )

    $Pwsh = Get-Command pwsh -ErrorAction SilentlyContinue
    if (-not $Pwsh) {
        $Pwsh = Get-Command powershell -ErrorAction SilentlyContinue
    }
    if (-not $Pwsh) {
        throw "PowerShell executable was not found."
    }

    $Command = "Set-Location '$RepoRoot'; `$Host.UI.RawUI.WindowTitle = '$WindowTitle'; $ScriptCommand"
    Start-Process -FilePath $Pwsh.Source -ArgumentList @("-NoExit", "-ExecutionPolicy", "Bypass", "-Command", $Command)
}

switch ($Service) {
    "backend" {
        Start-Backend
    }
    "web" {
        Start-Web
    }
    "all" {
        Assert-DevEnvironment
        $BackendCommand = ".\scripts\dev.ps1 -Service backend"
        if ($AllowLan) {
            $BackendCommand = "$BackendCommand -AllowLan"
        }

        Start-ServiceWindow -WindowTitle "TONTO Backend" -ScriptCommand $BackendCommand
        Start-ServiceWindow -WindowTitle "TONTO Web" -ScriptCommand ".\scripts\dev.ps1 -Service web"
        Write-Host "Started backend and web in separate PowerShell windows."
        if ($AllowLan) {
            Write-Host "Backend: http://0.0.0.0:8000 (use the Windows PC IP or hostname from Raspberry Pi)"
        } else {
            Write-Host "Backend: http://127.0.0.1:8000"
        }
        Write-Host "Web:     http://127.0.0.1:5173"
    }
}
