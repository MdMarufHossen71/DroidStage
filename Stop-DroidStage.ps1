#Requires -Version 5.1
param()

$ErrorActionPreference = "Continue"
$dataDir = Join-Path $env:LOCALAPPDATA "DroidStage"
$pidFile = Join-Path $dataDir "agent.pid"

if (Test-Path $pidFile) {
    $oldPid = Get-Content $pidFile
    try { Stop-Process -Id $oldPid -Force -ErrorAction Stop; Write-Host "Stopped agent (PID $oldPid)." } catch { Write-Host "Agent not running." }
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
} else {
    Write-Host "No PID file found."
}
