[CmdletBinding()]
param(
    [switch]$SkipPython,
    [switch]$SkipWeb
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$VenvDir = Join-Path $RepoRoot ".venv"
$CacheDir = Join-Path $RepoRoot ".cache"
$PipCacheDir = Join-Path $CacheDir "pip"
$NpmCacheDir = Join-Path $CacheDir "npm"
$VenvPython = if ($env:OS -eq "Windows_NT") {
    Join-Path (Join-Path $VenvDir "Scripts") "python.exe"
} else {
    Join-Path (Join-Path $VenvDir "bin") "python"
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

function Invoke-HostPython {
    param([string[]]$Arguments)

    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        Invoke-CheckedCommand -FilePath $python.Source -Arguments $Arguments
        return
    }

    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) {
        Invoke-CheckedCommand -FilePath $py.Source -Arguments (@("-3") + $Arguments)
        return
    }

    throw "Python was not found. Install Python 3 before running setup."
}

function Install-PythonRequirements {
    param([string]$RequirementsPath)

    if (Test-Path $RequirementsPath) {
        Write-Host "Installing Python requirements from $RequirementsPath"
        Invoke-CheckedCommand -FilePath $VenvPython -Arguments @("-m", "pip", "install", "--cache-dir", $PipCacheDir, "-r", $RequirementsPath)
    }
}

function Test-VenvPip {
    if (-not (Test-Path $VenvPython)) {
        return $false
    }

    & $VenvPython -m pip --version *> $null
    return $LASTEXITCODE -eq 0
}

function Reset-Venv {
    if (Test-Path $VenvDir) {
        $ResolvedRepo = (Resolve-Path $RepoRoot).Path
        $ResolvedVenv = (Resolve-Path $VenvDir).Path
        if (-not $ResolvedVenv.StartsWith($ResolvedRepo)) {
            throw "Refusing to remove venv outside repository: $ResolvedVenv"
        }

        Write-Host "Removing incomplete Python virtual environment at $VenvDir"
        Remove-Item -LiteralPath $VenvDir -Recurse -Force
    }
}

Push-Location $RepoRoot
try {
    New-Item -ItemType Directory -Force -Path $PipCacheDir | Out-Null
    New-Item -ItemType Directory -Force -Path $NpmCacheDir | Out-Null

    if (-not $SkipPython) {
        if (-not (Test-Path $VenvPython)) {
            Write-Host "Creating Python virtual environment at $VenvDir"
            Invoke-HostPython -Arguments @("-m", "venv", $VenvDir)
        }

        if (-not (Test-VenvPip)) {
            Reset-Venv
            Write-Host "Creating Python virtual environment at $VenvDir"
            Invoke-HostPython -Arguments @("-m", "venv", $VenvDir)
        }

        if (-not (Test-VenvPip)) {
            throw "Python virtual environment was created, but pip is not available inside .venv."
        }

        Write-Host "Upgrading pip inside .venv"
        Invoke-CheckedCommand -FilePath $VenvPython -Arguments @("-m", "pip", "install", "--cache-dir", $PipCacheDir, "--upgrade", "pip")

        Install-PythonRequirements -RequirementsPath (Join-Path (Join-Path $RepoRoot "backend") "requirements.txt")
        Install-PythonRequirements -RequirementsPath (Join-Path (Join-Path $RepoRoot "client") "requirements.txt")
        Install-PythonRequirements -RequirementsPath (Join-Path $RepoRoot "requirements-dev.txt")
    }

    if (-not $SkipWeb) {
        $WebDir = Join-Path $RepoRoot "web"
        if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
            throw "npm was not found. Install Node.js before running web setup."
        }

        Push-Location $WebDir
        try {
            if (Test-Path (Join-Path $WebDir "package-lock.json")) {
                Write-Host "Installing web dependencies with npm ci"
                Invoke-CheckedCommand -FilePath "npm" -Arguments @("ci", "--cache", $NpmCacheDir)
            } else {
                Write-Host "Installing web dependencies with npm install"
                Invoke-CheckedCommand -FilePath "npm" -Arguments @("install", "--cache", $NpmCacheDir)
            }
        } finally {
            Pop-Location
        }
    }

    Write-Host "Development environment is ready."
} finally {
    Pop-Location
}
