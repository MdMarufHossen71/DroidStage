# Technology choices and research notes

These are candidate technologies, not final decisions. Before implementation, verify current versions, licenses, APIs, Windows support, and maintenance activity.

## Candidate stack

| Area | Candidate | Notes |
|---|---|---|
| Browser UI | React + TypeScript + Vite | Static/local web interface; keep bundle light |
| UI tests | Vitest + Playwright | Unit tests and real Chromium integration tests |
| Physical-device control | ADB protocol / WebUSB | Evaluate browser-native access versus a local agent |
| Screen/control protocol | Official scrcpy server/protocol | Do not assume the desktop GUI itself embeds into a browser |
| Browser decoding | WebCodecs, with capability detection | Test H.264/H.265 support in supported browsers |
| Local agent (if needed) | Python 3.12+ + FastAPI | Small loopback-only service, not a public server |
| Virtual device (later) | Android SDK CLI + Emulator | `sdkmanager`, `avdmanager`, `emulator`, `adb` |
| Local settings | SQLite or a small versioned JSON config | Choose the simplest reliable option |
| Windows scripts | PowerShell + small `.bat` launchers | No Docker and no Android Studio IDE requirement |

## Reference projects / official sources to evaluate

- Android SDK command-line tools: https://developer.android.com/tools — official documentation for `sdkmanager`, `avdmanager`, and the Emulator.
- Android Emulator: https://developer.android.com/studio/run/emulator-commandline — official command-line usage.
- scrcpy: https://github.com/Genymobile/scrcpy — official upstream project; Apache-2.0. Verify exact release, bundled server version, and license notices before using or downloading binaries.
- OpenDroid Remote: https://github.com/hihumanzone/opendroid_remote — a browser-oriented WebUSB/ADB/WebCodecs implementation worth auditing for feasibility and license compatibility; do not blindly copy or depend on it.
- Webscreen: https://github.com/huonwe/webscreen — a WebRTC-based browser streaming reference; AGPL-3.0, so a license review is required before any code reuse or bundling.
- GitHub CLI: https://cli.github.com/manual/gh_repo_create — repository bootstrap documentation.

## Decision rules

1. Prefer the smallest maintainable solution that provides a real browser-embedded screen and input path.
2. Evaluate WebUSB only with a clear Chrome/Edge support check and a fallback/error message.
3. If a separate local agent is needed, bind only to loopback and authenticate each browser session.
4. Do not bundle proprietary Google Play components or redistribute Android system images.
5. Do not introduce a dependency whose license conflicts with the repository's MIT license without an explicit legal/maintainer decision.
6. Record major design choices in `docs/adr/` using short Architecture Decision Records.
