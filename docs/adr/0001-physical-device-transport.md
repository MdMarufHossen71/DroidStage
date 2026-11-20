# ADR 0001 - Physical device transport

Status: Accepted (M0 vertical slice)
Date: 2026-11-17

## Context

DroidStage's hardest requirement is a real Android screen rendered and controlled inside Chrome/Edge, plus APK install. Two candidate transports were evaluated.

## Options

### A. Browser-direct: WebUSB + browser ADB + scrcpy protocol + WebCodecs

- Pros: no local agent, no install friction beyond browser.
- Cons: WebUSB availability/permission UX varies; implementing/maintaining an ADB client and scrcpy protocol in TypeScript is high risk; APK install requires pushing bytes over WebUSB with no host filesystem; security review burden; harder to support official adb tooling and error messages; no proven end-to-end reference that we can ship without copying code of uncertain license.
- Windows reliability: medium-low for a solo maintainer.
- 4 GB PC: good (no extra process), but browser work is heavy.
- Licensing: clean if implemented from scratch, but large effort.

### B. Small Windows loopback agent: official ADB + allowlisted operations; browser UI over localhost HTTP/WebSocket

- Pros: uses official, maintained `adb`/platform-tools; subprocess argument arrays; clear errors; testable; keeps secrets/serials server-side; browser stays a UI. Can add proven stream transport later (scrcpy server -> agent -> WebRTC/WebSocket/WebCodecs) without changing UI contract.
- Cons: requires installing platform-tools (official source, checksum verified); local process to manage.
- Windows reliability: high.
- 4 GB PC: acceptable; agent is lightweight Python/FastAPI.
- Security: manageable with loopback bind, Origin validation, per-session token, allowlist.

## Decision

Choose Approach B for the first vertical slice.

- Device discovery and APK install are implemented through the loopback agent using official `adb` when available.
- Live browser-embedded screen streaming is NOT yet implemented. It is tracked as blocked in TASKS.md with the precise blocker: no scrcpy server/WebCodecs/WebRTC transport has been validated end-to-end in this repository, and no physical Android device is available in this development environment to prove it. We will not fake it.
- Approach A is rejected for now because of maintenance/security risk and lack of a verified implementation; it may be revisited if a maintained, license-compatible browser ADB/scrcpy library is found.

## License notes

- scrcpy: Apache-2.0 (upstream Genymobile/scrcpy). Not bundled in this repository. Any future use must verify the exact release and ship license notices.
- Android SDK platform-tools: Google terms; user installs from official Android developer site; not redistributed here.
- Webscreen: AGPL-3.0. Not copied or bundled. Any reuse would require license acceptance and is out of scope.
- OpenDroid Remote: referenced only; not copied or depended on. License/quality not verified for reuse.

## Evidence

- Environment check: Chrome present, Python 3.12 + FastAPI/uvicorn available, Node 24 available, no `adb` on PATH.
- No Android device available in this dev environment, so live streaming cannot be truthfully demonstrated.

## Consequences

- README/ROADMAP state that live browser streaming is not implemented.
- `apps/agent` implements device discovery + APK install only.
- Windows scripts guide users to install official platform-tools.
