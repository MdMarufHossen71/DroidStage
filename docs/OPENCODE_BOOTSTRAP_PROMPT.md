# OpenCode implementation prompt — DroidStage (Windows-first)

Copy the entire prompt below into OpenCode from the root of this repository.

---

You are the lead software architect and implementation engineer for **DroidStage**, an open-source, local-first, Windows-first browser-controlled Android workspace. Work directly in the current repository. Do not merely write a plan and stop: inspect the repo, validate the technical approach, implement the first real working vertical slice, run checks, fix problems, and update the documentation.

## 1. Product goal

Build a Windows application that runs locally on the user's PC and provides an Android workspace inside Chrome or Microsoft Edge. The first release must prioritize **Physical Device Bridge**: a real Android phone runs Android, while the PC/browser manages, views, and controls it. This is the realistic path for users with only 4 GB RAM.

A separate **Local Virtual Android** mode may be added later for PCs with sufficient RAM, CPU virtualization, disk space, and graphics support. Never promise that a full emulator will run well on 4 GB RAM. Do not make Android Studio IDE or Docker mandatory.

The product is not a cloud service. It must not require a user account, subscription, remote relay, telemetry, or upload of APKs/device data.

## 2. Hard product requirements

- Initial OS: Windows 11 x64. Keep Windows 10 22H2 compatibility in mind.
- Initial browsers: current Google Chrome and Microsoft Edge. Detect missing WebUSB/WebCodecs support and show a clear message. Do not claim Firefox/Safari support until tested.
- The user interface must run in a browser at a local address, normally `http://127.0.0.1:<port>`.
- User must be able to connect an Android phone through USB after enabling Developer options and USB debugging and approving the debugging prompt.
- The app must discover devices and clearly show connected, unauthorized, offline, and disconnected states.
- The app must provide a real, browser-embedded live Android screen with working pointer/touch and keyboard forwarding. Opening the ordinary scrcpy desktop window is not sufficient.
- The user must be able to select an APK, inspect its filename/size and available package metadata, explicitly confirm installation, install it, and receive an accurate result. Also implement package listing and launch/uninstall only after the basic path is stable.
- Support normal APKs first. Do not claim split APK/APKS/XAPK support until implemented and tested.
- Keep the project responsive on low-end Windows PCs. Use low-resource defaults and provide quality settings only after measuring.
- Include clear errors for missing tools, USB authorization, incompatible ABI/API, unsupported codecs, and missing browser features.
- Keep app data, settings, logs, and downloaded runtime dependencies outside the Git repository.

## 3. Be honest about Google Play and APK compatibility

Do not bundle Google Play Store, Google Play Services, Google APIs system images, Google binaries, or Google credentials in this repository or release. In Physical Device Bridge mode, Google services come from the user's own Android phone. For a future virtual mode, allow only user-initiated downloads from official Android SDK repositories and require the user to accept the relevant SDK license. Do not bypass licensing, Play Integrity, app protections, or anti-cheat. Explain that some apps will not run because of ABI, API level, DRM, device hardware, root/emulator detection, Play Integrity, or vendor policies.

## 4. First task: research and prove the transport before committing to architecture

The hardest requirement is rendering and controlling a physical Android device *inside the browser*. Do not fake this feature and do not assume that a normal scrcpy GUI window can be embedded in HTML.

Inspect current official documentation and maintained upstream code. At minimum evaluate:

- Official scrcpy: https://github.com/Genymobile/scrcpy
- Android SDK command-line tools: https://developer.android.com/tools
- Android Emulator command line: https://developer.android.com/studio/run/emulator-commandline
- OpenDroid Remote as a WebUSB/ADB/WebCodecs reference: https://github.com/hihumanzone/opendroid_remote
- Webscreen as a WebRTC streaming reference: https://github.com/huonwe/webscreen (AGPL-3.0; do not copy/bundle its code unless the license consequences are explicitly accepted)

Evaluate two approaches:

A. Browser-direct WebUSB + a maintained browser ADB implementation + scrcpy protocol + WebCodecs.
B. A small Windows loopback agent using official ADB/scrcpy components and a proven browser stream transport (WebRTC/WebSocket/WebCodecs).

For each approach, compare Windows reliability, Chrome/Edge support, installation friction, performance on a 4 GB PC, licensing, maintenance, security, and how APK install + video + touch control work.

Create `docs/adr/0001-physical-device-transport.md` with the chosen approach, alternatives rejected, license notes, and evidence. Build a proof of concept that discovers one physical Android device, renders its actual screen in the browser, and forwards at least basic input. Also prove APK installation. Do not proceed to a polished dashboard until this vertical slice works.

If neither approach can be completed in this session, implement the device-discovery + APK-install portion honestly, document the precise blocker, and leave live browser streaming clearly marked as not implemented. Never create fake screens, fake success states, or simulated APK installation.

## 5. Suggested implementation stack (change only with a documented reason)

- Frontend: React + TypeScript + Vite.
- Local agent, only if required: Python 3.12+ + FastAPI + WebSocket.
- Device control: ADB / WebUSB; scrcpy protocol for screen/control where feasible.
- Browser video: WebCodecs and/or WebRTC with feature detection.
- Tests: Vitest for frontend logic, pytest for Python, Playwright for Chromium end-to-end checks.
- Windows setup: PowerShell scripts plus `.bat` launchers.
- No Docker requirement. No Android Studio IDE requirement.

Use currently maintained stable versions, pin dependencies, and check upstream release notes. Avoid unnecessary frameworks and heavy dependencies.

## 6. Security requirements — non-negotiable

- Any local HTTP/WebSocket server must bind to `127.0.0.1` by default, not `0.0.0.0`.
- Validate Origin and use a random per-session token for privileged local API/WebSocket requests.
- Do not expose ADB TCP ports to LAN or public internet.
- Never expose arbitrary PowerShell, CMD, or shell execution to the browser.
- Use an allowlist of operations and subprocess argument arrays (never concatenate untrusted strings into a shell command).
- Apply strict request/upload size limits, safe temp paths, timeouts, output limits, and process cleanup.
- Require an explicit user gesture/confirmation before APK installation, uninstall, reset, or any destructive action.
- Do not store Google passwords, access tokens, or unnecessary device serials.
- Redact serial numbers and sensitive device information in logs.
- No analytics, telemetry, crash upload, cloud sync, relay, or automatic file upload.
- Do not auto-download or execute binaries from untrusted mirrors. Use official upstream releases and verify SHA-256/checksums/signatures where published.
- Keep third-party license notices and do not redistribute proprietary Google components.

## 7. Repository organization

Keep the repo clean and modular. A reasonable target (adapt as needed):

```text
apps/
  web/                    # React dashboard
  agent/                  # optional local Windows agent
packages/
  shared/                 # shared types and schemas
core/
  device/                 # physical device abstraction
  apk/                    # APK metadata and install workflows
  streaming/              # browser screen transport
  emulator/               # later virtual-device adapter
scripts/windows/          # setup/start/stop/doctor/clean scripts
config/                   # safe defaults and schemas
assets/                   # only original project assets
 docs/
  adr/
tests/
.github/
```

Do not create empty directories just for appearance. Use a monorepo only if it actually helps development.

## 8. User experience requirements

Create a clean, fast, professional dashboard with:

- Device status and connection action.
- A central phone/screen workspace with loading, disconnected, unauthorized, and unsupported states.
- APK drop zone and file picker with explicit installation confirmation.
- Installed apps list with package name, version, and launch/uninstall actions where supported.
- Compact device information and diagnostics.
- A low-resource preset (lower resolution/frame rate/bitrate) as the default.
- Helpful empty states and actionable error messages; do not use fake device data in production mode.
- Keyboard accessibility, responsive layout, and clear focus states.

## 9. Windows setup and startup

Provide scripts with strict error handling and clear output:

- `scripts/windows/doctor.ps1`: inspect OS, architecture, RAM, CPU virtualization where detectable, browser availability, required runtimes, free disk, and device tools. Never crash when a check is unavailable; mark it unknown.
- `scripts/windows/setup.ps1`: install/check only required dependencies, explain each download, verify checksums, store tools outside the repo, and avoid admin elevation.
- `Start-DroidStage.ps1` plus `Start-DroidStage.bat`: start the required local components and open the local dashboard.
- `Stop-DroidStage.ps1`: stop only the processes started by DroidStage.
- `Uninstall-DroidStage.ps1` or a documented clean command: remove app-managed files only; never remove the user's Android SDK or unrelated tools.

Scripts must be idempotent and must not overwrite user data without confirmation. Do not hardcode the developer's machine paths.

## 10. Quality gates

- Add unit tests for device state parsing, APK validation, API validation, and session security.
- Add browser tests for the main connection and APK interaction flows using mocks only in test mode.
- Add at least one manual test checklist for a real Android phone.
- Run formatting, lint, type checks, unit tests, build, and available integration tests.
- Do not report tests as passing unless they were actually run.
- Do not suppress type/lint failures just to get a green build.
- Add dependency/license inventory and document any bundled binaries.

## 11. Work process

1. Inspect every existing repository file before editing.
2. Summarize the repo state and identify missing prerequisites.
3. Research and record the transport ADR.
4. Implement the smallest real end-to-end physical-device vertical slice.
5. Add tests and Windows scripts.
6. Run all available checks and fix failures.
7. Update `README.md`, `docs/ROADMAP.md`, `CHANGELOG.md`, and `docs/DEVELOPMENT.md` to reflect what actually works.
8. Keep a short `TASKS.md` with completed, in-progress, and blocked items.
9. Finish with a truthful report: implemented features, exact commands run, test results, limitations, and next tasks.

Do not ask me to make routine choices. Use sensible defaults and document them. If a critical API or license question is uncertain, research it rather than guessing. Do not stop after creating a pretty frontend: prioritize real device connectivity and real APK installation.

**Start now.**
