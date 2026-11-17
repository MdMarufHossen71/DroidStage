# Architecture

## Goals

DroidStage is a Windows-first, local-first Android workspace controlled from a browser. The first useful release must work with a real Android phone attached to a modest Windows PC. A full PC-hosted emulator is a separate, higher-resource mode.

## Runtime modes

### 1. Physical Device Bridge (MVP)

The Android phone performs Android app execution. Windows provides the local control/streaming components and browser UI. Required user setup is Android Developer options + USB debugging + explicit authorization of the PC.

Responsibilities:

- Discover connected Android devices and show authorized/unauthorized/offline states.
- Read only the device metadata required by the UI.
- Install/uninstall/launch APKs after explicit user action.
- Provide a real browser-embedded screen stream and input path.
- Transfer files and collect opt-in diagnostics.

**Critical design question:** prove the browser video and input transport before building the full UI. Evaluate WebUSB + a maintained browser ADB implementation + the scrcpy protocol/WebCodecs, or a small loopback Windows agent using ADB and a WebRTC/WebSocket stream. A desktop scrcpy window alone does not satisfy the browser-embedded requirement.

### 2. Local Virtual Android (later)

A Windows local agent manages Android SDK command-line tools (`sdkmanager`, `avdmanager`, `emulator`, `adb`) and one AVD at a time. The browser remains the user interface.

- This mode is optional and must not be required for the 4 GB use case.
- Detect virtualization, RAM, available disk, GPU/driver, and emulator compatibility before offering it.
- Use official Android SDK sources and make the user accept applicable SDK package licenses.
- Do not bundle Google Play system images or proprietary Google components in the repository or release archive.
- Do not promise that every APK/ABI/API combination will run.

## Proposed component boundaries

```text
Browser (Chrome / Edge)
  React + TypeScript UI
       | HTTPS not required for localhost, but use a secure local origin where required by browser APIs
       | authenticated REST / WebSocket OR direct WebUSB
       v
Windows Local Agent (only where host access is required)
  - session and capability manager
  - device adapter
  - APK operations
  - streaming adapter
  - optional emulator adapter
  - diagnostics and structured logs
       |
       +---- Physical Android phone (ADB / USB)
       |
       +---- Optional Android Emulator (ADB / localhost)
```

The final design may remove or reduce the local agent if browser WebUSB can safely provide the required device and APK operations. Record the decision in an Architecture Decision Record before committing to a complex transport.

## Streaming requirements

- Render the Android screen inside a browser element/canvas, not an external desktop window.
- Support touch, pointer, keyboard, and basic navigation controls.
- Start with low-resource defaults (for example, 720p maximum and 30 FPS); make limits configurable after measuring.
- Adapt quality to the device and browser capabilities.
- Avoid unnecessary transcoding and frame copies.
- Handle disconnect, USB permission revocation, screen rotation, browser tab close, and device sleep.
- Do not claim multi-touch, audio, recording, or gamepad support until each is implemented and tested.

## Security boundaries

- Default listener: `127.0.0.1` only.
- No ADB TCP listener exposed to LAN/public networks.
- Browser API operations must be allowlisted; never expose arbitrary shell commands.
- Validate `Origin`, use a per-session secret/token for local API/WebSocket endpoints, and reject requests from unknown origins.
- Use subprocess argument arrays, not shell-concatenated command strings.
- Apply timeouts, output limits, upload limits, safe file names, and cleanup.
- Require explicit user confirmation before installing an APK or executing a destructive operation.
- Do not collect telemetry or send files/device metadata to remote services.
- Treat APKs as untrusted files. Show available metadata and warn users to install only trusted APKs.

## Data and persistence

- Keep user settings and device profiles locally.
- Do not persist APK contents by default; use a temporary staging directory and clean it up.
- Never store Google passwords or OAuth tokens.
- Avoid storing device serials unless strictly necessary; redact them in logs.
- Provide a clear Reset/Clear Local Data operation.

## Error handling

Errors must be actionable and distinguish at least: missing driver/ADB, USB debugging off, device unauthorized, device offline, multiple devices, unsupported browser API, unsupported codec, incompatible APK ABI/API, insufficient disk/RAM, emulator virtualization unavailable, and user-denied permission.
