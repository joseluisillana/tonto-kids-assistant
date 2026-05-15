[CmdletBinding()]
param(
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ExportRoot = if ($OutputPath) {
    if ([System.IO.Path]::IsPathRooted($OutputPath)) {
        $OutputPath
    } else {
        Join-Path $RepoRoot $OutputPath
    }
} else {
    Join-Path (Join-Path $RepoRoot "exports") "notebooklm"
}

function Get-RelativePath {
    param([string]$Path)

    $resolvedRepo = (Resolve-Path $RepoRoot).Path
    $resolvedPath = (Resolve-Path $Path).Path
    if (-not $resolvedPath.StartsWith($resolvedRepo, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Source is outside repository: $resolvedPath"
    }

    return $resolvedPath.Substring($resolvedRepo.Length + 1)
}

function Get-ExportName {
    param([string]$RelativePath)

    return $RelativePath -replace '[\\/]', '__'
}

function Assert-InsideRepo {
    param([string]$Path)

    $resolvedRepo = (Resolve-Path $RepoRoot).Path
    $fullPath = [System.IO.Path]::GetFullPath($Path)
    if (-not $fullPath.StartsWith($resolvedRepo, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to write outside repository: $fullPath"
    }
}

Assert-InsideRepo -Path $ExportRoot

if (Test-Path $ExportRoot) {
    $resolvedRepo = (Resolve-Path $RepoRoot).Path
    $resolvedExport = (Resolve-Path $ExportRoot).Path
    if (-not $resolvedExport.StartsWith($resolvedRepo, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to remove export outside repository: $resolvedExport"
    }

    Remove-Item -LiteralPath $ExportRoot -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $ExportRoot | Out-Null

$sourcePatterns = @(
    "README.md",
    "AGENTS.md",
    "docs\*.md",
    "docs\project-journal\*.md",
    "docs\research\*.md",
    "specs\*.md",
    "web\README.md"
)

$sources = New-Object System.Collections.Generic.List[object]

foreach ($pattern in $sourcePatterns) {
    $matches = Get-ChildItem -Path (Join-Path $RepoRoot $pattern) -File -ErrorAction SilentlyContinue | Sort-Object FullName
    foreach ($match in $matches) {
        $relativePath = Get-RelativePath -Path $match.FullName
        $exportName = Get-ExportName -RelativePath $relativePath
        $destination = Join-Path $ExportRoot $exportName

        Copy-Item -LiteralPath $match.FullName -Destination $destination -Force

        $sources.Add([pscustomobject]@{
            Source = $relativePath
            Export = $exportName
        }) | Out-Null
    }
}

$indexPath = Join-Path $ExportRoot "INDEX.md"
$indexLines = New-Object System.Collections.Generic.List[string]
$indexLines.Add("# NotebookLM Source Export") | Out-Null
$indexLines.Add("") | Out-Null
$indexLines.Add("Generated from repository documentation. This folder is derived output and is ignored by Git.") | Out-Null
$indexLines.Add("") | Out-Null
$indexLines.Add("Use these files as NotebookLM sources, but keep final project documentation in the repository.") | Out-Null
$indexLines.Add("") | Out-Null
$indexLines.Add("## Sources") | Out-Null
$indexLines.Add("") | Out-Null

foreach ($source in $sources) {
    $indexLines.Add(("- {0} from {1}" -f $source.Export, $source.Source)) | Out-Null
}

Set-Content -LiteralPath $indexPath -Value $indexLines -Encoding utf8

Write-Host ("Exported {0} NotebookLM source files to {1}" -f $sources.Count, $ExportRoot)
