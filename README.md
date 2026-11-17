# DroidStage

**Your Local Android Lab — browser-controlled, Windows-first, open source.**

DroidStage is planned as a local-first Windows application that gives users a browser-based workspace for connecting Android devices, installing and managing APKs, viewing and controlling a device, and (as an optional advanced mode) running a local Android Virtual Device.

> **Project status: pre-alpha / project scaffold.** This repository currently contains the project specification and development guidance. The application is not implemented yet. Do not treat planned features as working software.

## The core idea

Open DroidStage on your Windows PC, open its local dashboard in Chrome or Edge, connect an Android phone, and work with that device from the browser.

DroidStage has two runtime modes with different hardware requirements:

| Mode | What runs Android? | Target hardware | Priority |
|---|---|---:|---|
| **Physical Device Bridge** | Your connected Android phone | Designed to be practical on 4 GB PC RAM, subject to browser/OS overhead | First |
| **Local Virtual Android** | An Android Emulator running on the PC | Higher-memory PCs; not promised to work well on 4 GB RAM | Later |

The 4 GB goal is realistic only when the Android phone does the Android processing. Running a full Android emulator, Windows, and a browser together on a 4 GB PC is not a realistic baseline.

## Planned capabilities

- Browser dashboard served locally on `127.0.0.1`.
- Connect and identify physical Android devices over USB.
- Install, update, launch, and uninstall APKs.
- Show a live device screen in the browser and forward user input.
- Device status, Android version, model, storage information, and useful diagnostics.
- Copy files between the PC and Android device.
- Screenshots, optional recording, and logs.
- Low-bandwidth / low-resource streaming presets.
- Optional virtual-device mode using Android SDK command-line tools.
- Google Play support only where the selected device or officially licensed Google Play system image provides it.

All items above are goals, not claims that the features already exist.

## Important limitations and expectations

1. **DroidStage does not make the browser itself an Android runtime.** In Physical Device Bridge mode, a real Android phone runs Android and the browser is the control surface. In Virtual Android mode, a local emulator runs on the PC.
2. **4 GB PC support means Physical Device Bridge first.** It does not mean a full emulator will run smoothly on 4 GB RAM.
3. **Google Play is not bundled.** DroidStage must not redistribute Google Play Store, Google Play Services, Google APIs images, or other proprietary Google components. Use an actual Android phone with Play services, or download a compatible official image through the Android SDK and accept its license yourself.
4. **Not every APK works on every device.** CPU ABI, Android API level, hardware features, DRM, Play Integrity, anti-cheat, and app policies can prevent installation or execution.
5. **Browser support:** the first release targets current Chromium-based browsers (Google Chrome and Microsoft Edge) on Windows. WebUSB and WebCodecs availability must be checked at runtime. Firefox support is not promised for the initial release.
6. **No cloud requirement:** core operation should be local. The app must not require an account, relay server, telemetry, or subscription.

## Windows-first goals

- Windows 10 (22H2) and Windows 11, 64-bit, are the initial target. Test on Windows 11 first.
- PowerShell scripts for setup, start, stop, diagnostics, and clean removal.
- No Android Studio IDE requirement.
- No Docker requirement.
- No administrator rights unless a specific optional dependency genuinely requires them; explain why before requesting elevation.
- Keep dependencies small and download them from official sources with checksum/signature verification where available.

## Quick start (planned)

The application is not ready to run yet. Once an MVP release is published, the intended flow will be:

1. Download the signed/verified Windows release from GitHub Releases.
2. Extract it to a writable folder.
3. Run `Start-DroidStage.ps1` or the provided `.bat` launcher.
4. Open the displayed local URL in Chrome or Edge.
5. Enable Developer options and USB debugging on the Android phone, connect it by USB, and approve the debugging prompt.
6. Select the device in DroidStage and install an APK after reviewing its source and requested permissions.

For development setup and the first implementation task, see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) and [docs/OPENCODE_BOOTSTRAP_PROMPT.md](docs/OPENCODE_BOOTSTRAP_PROMPT.md).

## Architecture overview

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). The intended design separates:

- a React + TypeScript browser UI;
- a small Windows local agent for operations that need host access;
- a Physical Device adapter (ADB / WebUSB / scrcpy-protocol approach, to be validated by a working proof of concept);
- a separate optional Virtual Device adapter using Android SDK command-line tools;
- a runtime capability and hardware check so unsupported features are not shown as available.

The implementation must choose a technically proven browser video/input transport. It must not claim that a normal `scrcpy` desktop window is a browser-embedded stream.

## Security and privacy

- Bind the local service to loopback (`127.0.0.1`) only by default.
- Do not expose ADB over the LAN or public internet.
- Do not expose arbitrary shell execution to the browser UI.
- Use an allowlist of backend operations, strict input validation, request size limits, subprocess timeouts, and safe temporary-file handling.
- Validate `Origin` and use a per-session token for local API / WebSocket access.
- Never silently install an APK. Require an explicit user action and show the file name, size, and available package metadata first.
- Do not upload APKs, logs, device identifiers, or screenshots anywhere.
- Do not add telemetry or analytics by default.
- See [SECURITY.md](SECURITY.md).

## Open source and third-party components

DroidStage source code is licensed under the MIT License. This does **not** change the license of third-party software, Android SDK components, device firmware, Google Play components, or APKs. Each dependency must keep its own license and notices. Do not copy or bundle third-party code or binaries until its license and redistribution terms have been reviewed.

Potential technologies and reference projects are listed in [docs/TECHNOLOGY_DECISIONS.md](docs/TECHNOLOGY_DECISIONS.md). They are candidates to evaluate, not automatic dependencies.

## Contributing

Contributions are welcome once the implementation begins. Read [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), and the issue templates before opening an issue or pull request.

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md). Initial milestones:

1. Windows system checks and safe local service foundation.
2. Reliable physical-device discovery and APK installation.
3. Working browser-embedded live screen and input control.
4. File transfer, logs, screenshots, and low-resource presets.
5. Optional Virtual Android mode for capable PCs.
6. Packaging, signing, release automation, and broader testing.

## Disclaimer

DroidStage is an independent open-source project and is not affiliated with Google, Android, Microsoft, or the developers of third-party components. Android is a trademark of Google LLC. Use only APKs you are legally allowed to install and test.
