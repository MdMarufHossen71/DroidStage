# Development (Windows first)

The application implementation has not started. The coding agent should choose and pin supported tool versions after checking current official documentation.

## Target developer environment

- Windows 11 x64 first; Windows 10 22H2 compatibility is a secondary target.
- PowerShell 7 preferred; Windows PowerShell 5.1 compatibility for launch scripts is desirable where practical.
- Git for Windows.
- Node.js LTS for the browser UI.
- Python 3.12+ only if the chosen local agent uses Python.
- No Android Studio IDE and no Docker dependency.

## Running the implemented vertical slice

1. Install Node.js LTS and Python 3.12+.
2. `cd apps/agent && python -m pip install -r requirements.txt`
3. `cd apps/web && npm install`
4. Install Android platform-tools and ensure `adb` is on PATH (optional for discovery).
5. Start: `./Start-DroidStage.ps1`
6. Stop: `./Stop-DroidStage.ps1`

Checks:
- `cd apps/agent && python -m pytest`
- `cd apps/web && npm test && npm run build`
- `cd apps/web && npm run lint`

## Local conventions

- Keep all generated runtime downloads outside the repository, under a user data/cache directory.
- Never commit SDK archives, AVD images, APK files, device logs, or secrets.
- Prefer PowerShell scripts with strict error handling and clear progress output.
- Pin runtime dependencies and document supported versions.
- Make setup repeatable and idempotent.
- Do not silently elevate to Administrator.
