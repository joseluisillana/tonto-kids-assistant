[CmdletBinding()]
param(
    [ValidateSet("python", "web", "all")]
    [string]$Target = "all"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$VenvPython = if ($env:OS -eq "Windows_NT") {
    Join-Path (Join-Path (Join-Path $RepoRoot ".venv") "Scripts") "python.exe"
} else {
    Join-Path (Join-Path (Join-Path $RepoRoot ".venv") "bin") "python"
}

function Invoke-CheckedCommand {
    param(
        [string]$FilePath,
        [string[]]$Arguments
    )

    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $FilePath $($Arguments -join ' ')"
    }
}

function Invoke-PythonChecks {
    if (-not (Test-Path $VenvPython)) {
        throw "Python virtual environment not found. Run ./scripts/setup-dev.ps1 first."
    }

    $PreviousDontWriteBytecode = $env:PYTHONDONTWRITEBYTECODE

    Push-Location $RepoRoot
    try {
        $env:PYTHONDONTWRITEBYTECODE = "1"
        Invoke-CheckedCommand -FilePath $VenvPython -Arguments @("-c", @"
import ast
from pathlib import Path

roots = [Path("backend"), Path("client"), Path("shared"), Path("tests")]
for root in roots:
    for path in root.rglob("*.py"):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
print("Python syntax OK")
"@)
        Invoke-CheckedCommand -FilePath $VenvPython -Arguments @("-m", "pytest", "-p", "no:cacheprovider", "tests")
    } finally {
        $env:PYTHONDONTWRITEBYTECODE = $PreviousDontWriteBytecode
        Pop-Location
    }
}

function Invoke-WebChecks {
    Push-Location (Join-Path $RepoRoot "web")
    try {
        if (-not (Test-Path "node_modules")) {
            throw "Web dependencies not found. Run ./scripts/setup-dev.ps1 first."
        }

        Invoke-CheckedCommand -FilePath "npm" -Arguments @("run", "typecheck")
    } finally {
        Pop-Location
    }
}

switch ($Target) {
    "python" {
        Invoke-PythonChecks
    }
    "web" {
        Invoke-WebChecks
    }
    "all" {
        Invoke-PythonChecks
        Invoke-WebChecks
    }
}
