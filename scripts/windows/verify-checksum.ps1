#Requires -Version 5.1
param(
    [Parameter(Mandatory=$true)][string]$Path,
    [Parameter(Mandatory=$true)][string]$ExpectedSha256
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $Path)) { throw "File not found: $Path" }
$actual = (Get-FileHash -Path $Path -Algorithm SHA256).Hash
if ($actual -ne $ExpectedSha256.ToUpper()) {
    throw "Checksum mismatch for $Path`nExpected: $ExpectedSha256`nActual:   $actual"
}
Write-Host "Checksum OK: $Path"
