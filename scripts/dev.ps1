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

    Write-Host "Starting backend on ${BackendHost}:8000"
    if ($AllowLan) {
        Write-Host "LAN mode enabled. Use the Windows PC IP or resolvable hostname in TONTO_BACKEND_URL from the Raspberry Pi."
        Write-Host "Example: TONTO_BACKEND_URL=http://<windows-pc-ip>:8000"
    }

    Push-Location $RepoRoot
    try {
        & $VenvPython -m uvicorn backend.main:app --host $BackendHost --port 8000 --reload
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
