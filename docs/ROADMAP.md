# Roadmap

This roadmap describes intended milestones, not completed features. Milestones should be closed only after automated tests and manual Windows/device verification.

## M0 - Research and proof of concept

- [x] Compare WebUSB/browser-ADB and Windows local-agent approaches (ADR 0001).
- [x] Record dependency license and redistribution review (ADR 0001).
- [x] Demonstrate APK installation with a clear confirmation step (agent + UI).
- [ ] Verify latest supported Windows/Chrome/Edge APIs (feature detection in UI only).
- [ ] Verify a maintained scrcpy-protocol/WebCodecs or WebRTC transport (blocked).
- [ ] Demonstrate one physical phone discovered and its screen rendered inside Chrome/Edge (streaming not implemented).

## M1 - Windows foundation

- [x] One-command local start/stop scripts.
- [x] Localhost-only service and origin/session security.
- [ ] Hardware and OS capability detection (doctor.ps1 basic).
- [ ] Runtime/dependency detection with official download links and checksum verification (partial).
- [ ] Structured logs and diagnostics export.

## M2 - Physical Device Bridge MVP

- [x] USB device discovery and authorization states (via adb).
- [x] Device metadata panel.
- [x] APK install/uninstall/launch (install tested via unit tests; device required for E2E).
- [x] Screenshot, file push/pull, logcat (adb-backed, unit-tested paths).
- [ ] Browser-embedded live screen (not implemented).
- [ ] Pointer/touch and keyboard forwarding (not implemented).
- [ ] Disconnect/reconnect and cleanup handling (partial).
- [ ] Low-resource video preset (not applicable yet).

## M3 - Useful device tools

- [x] File transfer (push/pull).
- [x] Screenshot.
- [ ] Optional screen recording, only if transport supports it reliably.
- [x] Logcat viewer (basic).
- [x] App/package list and APK metadata.
- [ ] Device rotation and basic navigation buttons.

## M4 — Local Virtual Android (optional)

- [ ] Virtualization and hardware preflight.
- [ ] SDK command-line installer.
- [ ] One AVD profile at a time.
- [ ] Official Google Play image selection where available and licensed.
- [ ] Browser-embedded stream and control.
- [ ] Clear warning for low-RAM PCs.

## M5 — Distribution and stability

- [ ] Windows release packaging and code-signing plan.
- [ ] Dependency inventory / SBOM.
- [ ] Automated CI, lint, type-check, tests, and build.
- [ ] Upgrade and clean-uninstall flows.
- [ ] Accessibility, localization, and contributor documentation.
- [ ] Manual test matrix covering 4 GB / 8 GB / 16 GB PCs and several Android devices.
