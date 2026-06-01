[CmdletBinding()]
param(
    [ValidateSet("web", "all")]
    [string]$Target = "all"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
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

function Invoke-WebBuild {
    Push-Location (Join-Path $RepoRoot "web")
    try {
        if (-not (Test-Path "node_modules")) {
            throw "Web dependencies not found. Run ./scripts/setup-dev.ps1 first."
        }

        Invoke-CheckedCommand -FilePath $Npm -Arguments @("run", "build")
    } finally {
        Pop-Location
    }
}

switch ($Target) {
    "web" {
        Invoke-WebBuild
    }
    "all" {
        & (Join-Path $PSScriptRoot "test.ps1") -Target python
        Invoke-WebBuild
    }
}
