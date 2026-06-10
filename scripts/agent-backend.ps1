[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("start", "stop", "status", "health")]
    [string]$Action,

    [switch]$AllowLan
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$AgentDir = Join-Path (Join-Path $RepoRoot ".cache") "agent"
$PidPath = Join-Path $AgentDir "backend.pid"
$OutLogPath = Join-Path $AgentDir "backend.out.log"
$ErrLogPath = Join-Path $AgentDir "backend.err.log"
$HealthUrl = "http://127.0.0.1:8000/health"
$DevScript = Join-Path $PSScriptRoot "dev.ps1"

function New-AgentDirectory {
    New-Item -ItemType Directory -Force -Path $AgentDir | Out-Null
}

function Clear-PidFile {
    if (-not (Test-Path $PidPath)) {
        return
    }

    try {
        Remove-Item -LiteralPath $PidPath -Force -ErrorAction Stop
    } catch {
        Set-Content -Path $PidPath -Value "" -Encoding ascii
    }
}

function Get-RecordedPid {
    if (-not (Test-Path $PidPath)) {
        return $null
    }

    $RawPid = (Get-Content -Raw $PidPath).Trim()
    if (-not $RawPid) {
        return $null
    }

    $PidValue = 0
    if (-not [int]::TryParse($RawPid, [ref]$PidValue)) {
        throw "Invalid backend PID file: $PidPath"
    }

    return $PidValue
}

function Test-ProcessAlive {
    param([int]$ProcessId)

    try {
        Get-Process -Id $ProcessId -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

function Invoke-HealthCheck {
    try {
        $Response = Invoke-RestMethod -Uri $HealthUrl -Method Get -TimeoutSec 3
        $Status = $Response.status
        return [pscustomobject]@{
            Ok = ($Status -eq "ok")
            Status = $Status
            Error = $null
        }
    } catch {
        return [pscustomobject]@{
            Ok = $false
            Status = $null
            Error = $_.Exception.Message
        }
    }
}

function Wait-BackendHealth {
    param([int]$ProcessId)

    $Deadline = (Get-Date).AddSeconds(30)

    while ((Get-Date) -lt $Deadline) {
        if (-not (Test-ProcessAlive -ProcessId $ProcessId)) {
            throw "Backend process $ProcessId exited before health became available. Logs: $OutLogPath and $ErrLogPath"
        }

        $Health = Invoke-HealthCheck
        if ($Health.Ok) {
            return
        }

        Start-Sleep -Milliseconds 500
    }

    throw "Backend did not become healthy at $HealthUrl within 30 seconds. Logs: $OutLogPath and $ErrLogPath"
}

function Start-AgentBackend {
    New-AgentDirectory

    $ExistingPid = Get-RecordedPid
    if ($null -ne $ExistingPid -and (Test-ProcessAlive -ProcessId $ExistingPid)) {
        throw "Recorded backend PID $ExistingPid is already running. Use -Action status or -Action stop first."
    }

    if ($null -ne $ExistingPid) {
        Clear-PidFile
    }

    Set-Content -Path $OutLogPath -Value "" -Encoding utf8
    Set-Content -Path $ErrLogPath -Value "" -Encoding utf8

    $PreviousAgentBackground = $env:TONTO_AGENT_BACKGROUND
    $PreviousAgentPidPath = $env:TONTO_AGENT_BACKEND_PID_PATH
    $PreviousAgentOutLog = $env:TONTO_AGENT_BACKEND_OUT_LOG
    $PreviousAgentErrLog = $env:TONTO_AGENT_BACKEND_ERR_LOG
    $PreviousAgentHost = $env:TONTO_AGENT_BACKEND_HOST
    $PreviousBackendReload = $env:TONTO_BACKEND_RELOAD

    try {
        $env:TONTO_AGENT_BACKGROUND = "1"
        $env:TONTO_AGENT_BACKEND_PID_PATH = $PidPath
        $env:TONTO_AGENT_BACKEND_OUT_LOG = $OutLogPath
        $env:TONTO_AGENT_BACKEND_ERR_LOG = $ErrLogPath
        $env:TONTO_AGENT_BACKEND_HOST = if ($AllowLan) { "0.0.0.0" } else { "127.0.0.1" }
        $env:TONTO_BACKEND_RELOAD = "0"

        if ($AllowLan) {
            & $DevScript -Service backend -AllowLan
        } else {
            & $DevScript -Service backend
        }
    } finally {
        $env:TONTO_AGENT_BACKGROUND = $PreviousAgentBackground
        $env:TONTO_AGENT_BACKEND_PID_PATH = $PreviousAgentPidPath
        $env:TONTO_AGENT_BACKEND_OUT_LOG = $PreviousAgentOutLog
        $env:TONTO_AGENT_BACKEND_ERR_LOG = $PreviousAgentErrLog
        $env:TONTO_AGENT_BACKEND_HOST = $PreviousAgentHost
        $env:TONTO_BACKEND_RELOAD = $PreviousBackendReload
    }

    $BackendPid = Get-RecordedPid
    if ($null -eq $BackendPid) {
        throw "Backend did not write a PID file at $PidPath."
    }

    try {
        Wait-BackendHealth -ProcessId $BackendPid
    } catch {
        if (Test-ProcessAlive -ProcessId $BackendPid) {
            Stop-Process -Id $BackendPid -ErrorAction SilentlyContinue
        }
        Clear-PidFile
        throw
    }

    Write-Host "Backend started."
    Write-Host "PID:    $BackendPid"
    Write-Host "Health: $HealthUrl"
    Write-Host "Logs:   $OutLogPath"
    Write-Host "        $ErrLogPath"
}

function Stop-AgentBackend {
    $RecordedPid = Get-RecordedPid
    if ($null -eq $RecordedPid) {
        Write-Host "No recorded backend PID found at $PidPath."
        return
    }

    if (-not (Test-ProcessAlive -ProcessId $RecordedPid)) {
        Write-Host "Recorded backend PID $RecordedPid is not running. Removing stale PID file."
        Clear-PidFile
        return
    }

    Stop-Process -Id $RecordedPid -ErrorAction Stop
    Start-Sleep -Seconds 1

    if (Test-ProcessAlive -ProcessId $RecordedPid) {
        Write-Warning "Recorded backend PID $RecordedPid is still running after stop request."
    } else {
        Clear-PidFile
        Write-Host "Stopped recorded backend PID $RecordedPid."
    }

    $Health = Invoke-HealthCheck
    if ($Health.Ok) {
        Write-Warning "Backend health still responds at $HealthUrl. Another process may be serving port 8000."
    }
}

function Show-AgentBackendStatus {
    $RecordedPid = Get-RecordedPid
    $Health = Invoke-HealthCheck

    if ($null -eq $RecordedPid) {
        Write-Host "PID:    none recorded"
        Write-Host "Alive:  false"
    } else {
        Write-Host "PID:    $RecordedPid"
        Write-Host "Alive:  $(Test-ProcessAlive -ProcessId $RecordedPid)"
    }

    if ($Health.Ok) {
        Write-Host "Health: ok ($HealthUrl)"
    } elseif ($Health.Error) {
        Write-Host "Health: unavailable ($($Health.Error))"
    } else {
        Write-Host "Health: unexpected status '$($Health.Status)' ($HealthUrl)"
    }

    Write-Host "Logs:   $OutLogPath"
    Write-Host "        $ErrLogPath"
}

function Show-AgentBackendHealth {
    $Health = Invoke-HealthCheck
    if ($Health.Ok) {
        Write-Host "Health: ok ($HealthUrl)"
        return
    }

    if ($Health.Error) {
        throw "Backend health check failed at ${HealthUrl}: $($Health.Error)"
    }

    throw "Backend health check returned unexpected status '$($Health.Status)' at $HealthUrl."
}

switch ($Action) {
    "start" { Start-AgentBackend }
    "stop" { Stop-AgentBackend }
    "status" { Show-AgentBackendStatus }
    "health" { Show-AgentBackendHealth }
}
