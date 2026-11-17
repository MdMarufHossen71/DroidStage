# Development (Windows first)

The application implementation has not started. The coding agent should choose and pin supported tool versions after checking current official documentation.

## Target developer environment

- Windows 11 x64 first; Windows 10 22H2 compatibility is a secondary target.
- PowerShell 7 preferred; Windows PowerShell 5.1 compatibility for launch scripts is desirable where practical.
- Git for Windows.
- Node.js LTS for the browser UI.
- Python 3.12+ only if the chosen local agent uses Python.
- No Android Studio IDE and no Docker dependency.

## First development session

1. Install Git and Node.js LTS if missing.
2. Install Python only if the selected backend requires it.
3. Open this repository folder in OpenCode.
4. Paste the full instructions from [OPENCODE_BOOTSTRAP_PROMPT.md](OPENCODE_BOOTSTRAP_PROMPT.md).
5. Let the agent inspect the current repository, verify technical choices against official documentation and maintained upstream projects, implement the first vertical slice, and run tests.

## Local conventions

- Keep all generated runtime downloads outside the repository, under a user data/cache directory.
- Never commit SDK archives, AVD images, APK files, device logs, or secrets.
- Prefer PowerShell scripts with strict error handling and clear progress output.
- Pin runtime dependencies and document supported versions.
- Make setup repeatable and idempotent.
- Do not silently elevate to Administrator.
