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
$Npm = if ($env:OS -eq "Windows_NT") { "npm.cmd" } else { "npm" }

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

    $LocalTempDir = Join-Path $RepoRoot ".cache\pytest-temp"
    New-Item -ItemType Directory -Force -Path $LocalTempDir | Out-Null
    $BaseTempDir = Join-Path $LocalTempDir ("basetemp-" + ([guid]::NewGuid().ToString("N")))
    New-Item -ItemType Directory -Force -Path $BaseTempDir | Out-Null

    $PreviousTemp = $env:TEMP
    $PreviousTmp = $env:TMP
    $PreviousTmpDir = $env:TMPDIR
    $PreviousDontWriteBytecode = $env:PYTHONDONTWRITEBYTECODE

    Push-Location $RepoRoot
    try {
        $env:TEMP = $LocalTempDir
        $env:TMP = $LocalTempDir
        $env:TMPDIR = $LocalTempDir
        $env:PYTHONDONTWRITEBYTECODE = "1"
        Invoke-CheckedCommand -FilePath $VenvPython -Arguments @(Join-Path (Join-Path $RepoRoot "scripts") "check_syntax.py")
        Invoke-CheckedCommand -FilePath $VenvPython -Arguments @(
            "-m",
            "pytest",
            "-p",
            "no:cacheprovider",
            "--basetemp",
            $BaseTempDir,
            "tests"
        )
    } finally {
        $env:TEMP = $PreviousTemp
        $env:TMP = $PreviousTmp
        $env:TMPDIR = $PreviousTmpDir
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

        Invoke-CheckedCommand -FilePath $Npm -Arguments @("run", "test")
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
