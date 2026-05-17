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
$indexLines.Add('For routine NotebookLM refreshes, prefer `NOTEBOOKLM_COMBINED.md` so one source can be replaced instead of re-uploading many duplicated files.') | Out-Null
$indexLines.Add("") | Out-Null
$indexLines.Add("## Sources") | Out-Null
$indexLines.Add("") | Out-Null

foreach ($source in $sources) {
    $indexLines.Add(("- {0} from {1}" -f $source.Export, $source.Source)) | Out-Null
}

Set-Content -LiteralPath $indexPath -Value $indexLines -Encoding utf8

$combinedPath = Join-Path $ExportRoot "NOTEBOOKLM_COMBINED.md"
$combinedLines = New-Object System.Collections.Generic.List[string]
$combinedLines.Add("# TONTO Kids Assistant - NotebookLM Combined Source") | Out-Null
$combinedLines.Add("") | Out-Null
$combinedLines.Add("Generated from repository documentation. This file is derived output and is ignored by Git.") | Out-Null
$combinedLines.Add("") | Out-Null
$combinedLines.Add("Use this single file as the primary NotebookLM source when you want to replace one document instead of re-importing many duplicated files.") | Out-Null
$combinedLines.Add("") | Out-Null
$combinedLines.Add("Keep final project documentation in the repository. NotebookLM remains a reading and synthesis layer.") | Out-Null
$combinedLines.Add("") | Out-Null
$combinedLines.Add("## Included Sources") | Out-Null
$combinedLines.Add("") | Out-Null

foreach ($source in $sources) {
    $combinedLines.Add(('- `{0}` exported as `{1}`' -f $source.Source, $source.Export)) | Out-Null
}

foreach ($source in $sources) {
    $sourcePath = Join-Path $RepoRoot $source.Source
    $content = (Get-Content -LiteralPath $sourcePath -Raw -Encoding utf8).TrimEnd()

    $combinedLines.Add("") | Out-Null
    $combinedLines.Add("---") | Out-Null
    $combinedLines.Add("") | Out-Null
    $sourceHeading = '## Source: {0}' -f $source.Source
    $combinedLines.Add($sourceHeading) | Out-Null
    $combinedLines.Add("") | Out-Null
    $combinedLines.Add($content) | Out-Null
}

Set-Content -LiteralPath $combinedPath -Value $combinedLines -Encoding utf8

Write-Host ("Exported {0} NotebookLM source files and 1 combined source file to {1}" -f $sources.Count, $ExportRoot)
