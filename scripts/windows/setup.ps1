#Requires -Version 5.1
param()

$ErrorActionPreference = "Stop"

Write-Host "DroidStage setup"
Write-Host "==============="

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js LTS is required. Install from https://nodejs.org/ and rerun."
    exit 1
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python 3.12+ is required. Install from https://www.python.org/ and rerun."
    exit 1
}

$agentDir = Join-Path $PSScriptRoot "..\..\apps\agent"
$agentDir = (Resolve-Path $agentDir).Path
$req = Join-Path $agentDir "requirements.txt"
if (Test-Path $req) {
    Write-Host "Installing Python dependencies (agent)..."
    python -m pip install -r $req
}

$webDir = Join-Path $PSScriptRoot "..\..\apps\web"
$webDir = (Resolve-Path $webDir).Path
if (Test-Path (Join-Path $webDir "package.json")) {
    Write-Host "Installing Node dependencies (web)..."
    Push-Location $webDir
    npm install
    Pop-Location
}

if (-not (Get-Command adb -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host "adb was not found."
    Write-Host "Download Android platform-tools from the official site:"
    Write-Host "https://developer.android.com/tools/releases/platform-tools"
    Write-Host "Extract outside this repository and add adb to PATH, or set DROIDSTAGE_ADB to adb.exe."
}

Write-Host ""
Write-Host ""
Write-Host "Checksum helper: scripts/windows/verify-checksum.ps1 -Path <file> -ExpectedSha256 <hash>"
Write-Host "Setup complete. Run Start-DroidStage.ps1 to launch."
