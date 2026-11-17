# Contributing to DroidStage

Thanks for considering a contribution. The project is currently a specification scaffold; implementation work should follow the roadmap and keep the 4 GB Physical Device Bridge goal realistic.

## Before starting

1. Search existing issues and pull requests to avoid duplicate work.
2. For substantial changes, open an issue first and describe the problem, proposed approach, Windows versions tested, and hardware used.
3. Do not commit APK files, Android system images, Google components, SDK archives, emulator disk images, credentials, device dumps, or personal logs.
4. Do not add a dependency until its maintenance status, license, security posture, and redistribution terms have been reviewed.

## Development principles

- Windows-first; test on Windows 11 and keep Windows 10 compatibility in mind.
- Do not require Android Studio IDE or Docker.
- Keep the 4 GB use case on Physical Device Bridge mode. Do not claim a 4 GB PC can comfortably run a full emulator.
- Keep services local and bind to loopback by default.
- Never add telemetry, remote relay, or account requirements without a separately discussed proposal.
- Prefer small, testable modules and explicit runtime interfaces.
- Never report a feature as implemented unless the full user-facing path works.

## Pull requests

- Keep each PR focused.
- Include tests for changed behavior.
- Run formatting, linting, type checks, and tests relevant to the change.
- Update README and documentation when behavior, requirements, limitations, or setup steps change.
- Include a short test report: Windows version, browser, RAM, CPU, Android device/model, Android version, and commands run. Do not include personal identifiers or private device logs.
- Explain third-party code, binaries, or protocol compatibility changes and include license notices where required.

## Reporting security issues

Do not post exploitable security vulnerabilities in public issues. Follow [SECURITY.md](SECURITY.md).
