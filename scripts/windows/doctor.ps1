#Requires -Version 5.1
param()

$ErrorActionPreference = "Continue"

function Check($name, $value) {
    Write-Host ("{0,-28} {1}" -f $name, $value)
}

Write-Host "DroidStage doctor"
Write-Host "================="

# OS
try {
    $os = Get-CimInstance Win32_OperatingSystem
    Check "OS" $os.Caption
    Check "Architecture" $env:PROCESSOR_ARCHITECTURE
    Check "Total RAM (GB)" ([math]::Round($os.TotalVisibleMemorySize / 1MB, 2))
} catch { Check "OS" "unknown" }

# CPU virtualization (best effort)
try {
    $virt = (Get-CimInstance Win32_Processor).VirtualizationFirmwareEnabled
    Check "CPU virtualization" $(if ($virt) { "enabled" } else { "disabled/unknown" })
} catch { Check "CPU virtualization" "unknown" }

# Free disk on system drive
try {
    $drive = Get-PSDrive -Name ($env:SystemDrive.TrimEnd(':'))
    Check "Free disk (GB)" ([math]::Round($drive.Free / 1GB, 2))
} catch { Check "Free disk" "unknown" }

# Browsers
foreach ($p in @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
    "C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
)) {
    if (Test-Path $p) { Check "Browser" $p; break }
}
if (-not (Get-Command chrome -ErrorAction SilentlyContinue)) {
    # already printed if found above; if none found, note
    if (-not (Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe")) {
        Check "Chrome" "not found"
    }
}

# Runtimes
Check "Node.js" $(if (Get-Command node -ErrorAction SilentlyContinue) { (node --version) } else { "missing" })
Check "Python" $(if (Get-Command python -ErrorAction SilentlyContinue) { (python --version) } else { "missing" })
Check "adb" $(if (Get-Command adb -ErrorAction SilentlyContinue) { "found" } else { "missing (install Android platform-tools)" })

# Ports
Check "Agent port" "8787 (default)"

Write-Host ""
Write-Host "Doctor finished. Missing items are not fatal; install them before starting."
