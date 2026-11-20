#Requires -Version 5.1
param()

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$agentDir = Join-Path $repoRoot "apps\agent"
$webDir = Join-Path $repoRoot "apps\web"

$dataDir = Join-Path $env:LOCALAPPDATA "DroidStage"
New-Item -ItemType Directory -Force -Path $dataDir | Out-Null
$pidFile = Join-Path $dataDir "agent.pid"

# Stop previous
if (Test-Path $pidFile) {
    try {
        $oldPid = Get-Content $pidFile
        Stop-Process -Id $oldPid -Force -ErrorAction SilentlyContinue
    } catch {}
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
}

# Build web if needed
if (-not (Test-Path (Join-Path $webDir "dist\index.html"))) {
    Write-Host "Building web UI..."
    Push-Location $webDir
    npm run build
    Pop-Location
}

# Generate token
$token = [guid]::NewGuid().ToString("N")
$env:DROIDSTAGE_TOKEN = $token
$env:DROIDSTAGE_PORT = "8787"

$python = (Get-Command python).Source
$env:PYTHONPATH = $agentDir
$agentProc = Start-Process -FilePath $python -ArgumentList "-m", "app.main" -WorkingDirectory $agentDir -PassThru -WindowStyle Hidden
$agentProc.Id | Out-File $pidFile

# Wait for health
$ready = $false
for ($i = 0; $i -lt 50; $i++) {
    try {
        $r = Invoke-WebRequest -Uri "http://127.0.0.1:8787/api/health" -UseBasicParsing -TimeoutSec 1
        if ($r.StatusCode -eq 200) { $ready = $true; break }
    } catch {}
    Start-Sleep -Milliseconds 200
}

$url = "http://127.0.0.1:8787/?token=$token"
if ($ready) {
    Write-Host "DroidStage running at $url"
    Start-Process $url
} else {
    Write-Warning "Agent did not become ready. Check logs."
    Write-Host "URL: $url"
}
