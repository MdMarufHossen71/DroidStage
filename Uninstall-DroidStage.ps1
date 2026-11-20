#Requires -Version 5.1
param([switch]$Force)

$ErrorActionPreference = "Continue"
$dataDir = Join-Path $env:LOCALAPPDATA "DroidStage"

if (-not $Force) {
    $ans = Read-Host "Remove DroidStage local data at $dataDir? (y/N)"
    if ($ans -ne "y") { Write-Host "Cancelled."; exit 0 }
}

if (Test-Path $dataDir) {
    Remove-Item -Recurse -Force $dataDir
    Write-Host "Removed $dataDir"
} else {
    Write-Host "Nothing to remove."
}

Write-Host "Note: Python/Node/Android platform-tools are not removed."
