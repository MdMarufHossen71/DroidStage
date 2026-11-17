# Roadmap

This roadmap describes intended milestones, not completed features. Milestones should be closed only after automated tests and manual Windows/device verification.

## M0 — Research and proof of concept

- [ ] Verify latest supported Windows/Chrome/Edge APIs.
- [ ] Compare WebUSB/browser-ADB and Windows local-agent approaches.
- [ ] Verify a maintained scrcpy-protocol/WebCodecs or WebRTC transport.
- [ ] Record dependency license and redistribution review.
- [ ] Demonstrate one physical phone discovered and its screen rendered inside Chrome/Edge.
- [ ] Demonstrate one APK installation with a clear confirmation step.

## M1 — Windows foundation

- [ ] Hardware and OS capability detection.
- [ ] One-command local start/stop scripts.
- [ ] Localhost-only service and origin/session security.
- [ ] Runtime/dependency detection with official download links and checksum verification.
- [ ] Structured logs and diagnostics export.

## M2 — Physical Device Bridge MVP

- [ ] USB device discovery and authorization states.
- [ ] Device metadata panel.
- [ ] APK install/uninstall/launch.
- [ ] Browser-embedded live screen.
- [ ] Pointer/touch and keyboard forwarding.
- [ ] Disconnect/reconnect and cleanup handling.
- [ ] Low-resource video preset.

## M3 — Useful device tools

- [ ] File transfer.
- [ ] Screenshot.
- [ ] Optional screen recording, only if transport supports it reliably.
- [ ] Logcat viewer with redaction controls.
- [ ] App/package list and APK metadata.
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
