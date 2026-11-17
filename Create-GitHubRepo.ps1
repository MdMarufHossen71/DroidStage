# Creates the public GitHub repository and pushes this starter scaffold.
# Requires Git for Windows and GitHub CLI (gh), authenticated with an account
# that owns MdMarufHossen71. This script never deletes or overwrites user files.

$ErrorActionPreference = 'Stop'
$owner = 'MdMarufHossen71'
$repo = 'DroidStage'
$fullName = "$owner/$repo"
$description = 'A lightweight, open-source, browser-controlled Android workspace for local APK testing on Windows.'

function Stop-WithMessage([string]$Message) {
    Write-Host "`nERROR: $Message" -ForegroundColor Red
    exit 1
}

foreach ($command in @('git', 'gh')) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        Stop-WithMessage "'$command' is not installed or not on PATH. Install Git for Windows and GitHub CLI, then reopen PowerShell."
    }
}

Write-Host 'Checking GitHub CLI authentication...' -ForegroundColor Cyan
& gh auth status
if ($LASTEXITCODE -ne 0) {
    Stop-WithMessage "GitHub CLI is not authenticated. Run 'gh auth login' and choose GitHub.com, HTTPS, and your account, then rerun this script."
}

$currentLogin = (& gh api user --jq .login).Trim()
if ($LASTEXITCODE -ne 0 -or $currentLogin -ne $owner) {
    Stop-WithMessage "Authenticated GitHub account is '$currentLogin', but this scaffold targets '$owner'. Authenticate with the correct account before continuing."
}

Write-Host "Checking whether $fullName already exists..." -ForegroundColor Cyan
& gh repo view $fullName --json name | Out-Null
if ($LASTEXITCODE -eq 0) {
    Stop-WithMessage "The repository $fullName already exists. This script intentionally will not overwrite it. Clone it and merge the scaffold manually instead."
}

if (-not (Test-Path (Join-Path (Get-Location) 'README.md'))) {
    Stop-WithMessage 'Run this script from the extracted DroidStage-Starter folder (README.md was not found).'
}

if (-not (Test-Path '.git')) {
    Write-Host 'Initializing local Git repository...' -ForegroundColor Cyan
    & git init --initial-branch=main
    if ($LASTEXITCODE -ne 0) { Stop-WithMessage 'git init failed.' }
} else {
    $branch = (& git branch --show-current).Trim()
    if ($branch -ne 'main') {
        Write-Host "Current branch is '$branch'. The script will not rename an existing branch automatically." -ForegroundColor Yellow
    }
}

$gitName = (& git config user.name 2>$null)
$gitEmail = (& git config user.email 2>$null)
if ([string]::IsNullOrWhiteSpace($gitName)) {
    $gitName = Read-Host 'Enter the Git author name for this initial commit'
    if ([string]::IsNullOrWhiteSpace($gitName)) { Stop-WithMessage 'Git author name is required.' }
    & git config user.name $gitName
}
if ([string]::IsNullOrWhiteSpace($gitEmail)) {
    $gitEmail = Read-Host 'Enter the Git author email for this initial commit (can be your GitHub noreply email)'
    if ([string]::IsNullOrWhiteSpace($gitEmail)) { Stop-WithMessage 'Git author email is required.' }
    & git config user.email $gitEmail
}

& git add --all
if ($LASTEXITCODE -ne 0) { Stop-WithMessage 'git add failed.' }

& git rev-parse --verify HEAD *> $null
if ($LASTEXITCODE -ne 0) {
    & git commit -m 'chore: add DroidStage project foundation'
    if ($LASTEXITCODE -ne 0) { Stop-WithMessage 'Initial Git commit failed.' }
} else {
    Write-Host 'A local commit already exists; keeping existing history.' -ForegroundColor Yellow
}

$origin = (& git remote get-url origin 2>$null)
if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($origin)) {
    Stop-WithMessage "An 'origin' remote already exists ($origin). Review it manually before creating a remote repository."
}

Write-Host "Creating PUBLIC GitHub repository $fullName and pushing the current branch..." -ForegroundColor Cyan
& gh repo create $fullName --public --description $description --source . --remote origin --push
if ($LASTEXITCODE -ne 0) {
    Stop-WithMessage 'GitHub repository creation or push failed. Your local files and commit remain intact; inspect `git status` and `gh auth status`, then rerun after resolving the issue.'
}

Write-Host "`nSuccess! Public repository created: https://github.com/$fullName" -ForegroundColor Green
Write-Host 'Next: open the repository in OpenCode and use docs/OPENCODE_BOOTSTRAP_PROMPT.md.' -ForegroundColor Green
