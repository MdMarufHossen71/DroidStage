# Changelog

All notable changes to DroidStage will be documented here.

The project has not made an application release yet.

## Unreleased

- Add initial project specification and Windows-first development plan.
- Define Physical Device Bridge as the first target for low-memory PCs.
- Define Local Virtual Android as an optional later mode.

## 0.1.0-pre - 2026-11-17

### Added
- Local FastAPI agent (loopback-only, Origin validation, per-session token).
- Physical Android device discovery via official adb with state parsing.
- APK metadata inspection, explicit-confirmation install, package list/launch/uninstall.
- Screenshot, file push/pull, and logcat tools.
- React + Vite browser dashboard with capability detection.
- Windows doctor/setup/start/stop/uninstall scripts + checksum helper.
- Unit tests (device parsing, APK validation, API validation, session security, file paths).
- Playwright smoke E2E (mocked agent).
- ADR 0001 documenting transport decision.

### Not implemented
- Live browser-embedded screen streaming and input forwarding.
