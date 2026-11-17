# Security Policy

## Supported versions

There is no released application yet. Security fixes will target the latest supported release once releases begin.

## Reporting a vulnerability

Please do not publish exploit details in a public issue. Use GitHub's **Report a vulnerability** feature (private vulnerability reporting) on this repository when enabled. If it is unavailable, contact the repository owner through the contact details on the GitHub profile and request a private reporting channel.

Include the affected version or commit, impact, reproduction steps, and any suggested mitigation. Do not include real users' APKs, credentials, private device data, or personal information.

## Security requirements for contributors

- Local API and WebSocket listeners must bind to `127.0.0.1` by default.
- Do not expose ADB TCP ports to the network.
- Do not provide arbitrary shell execution through HTTP/WebSocket endpoints.
- Validate all input and file paths; enforce upload limits; use temporary directories safely.
- Use subprocess argument arrays rather than shell command strings.
- Apply timeouts and terminate child processes on shutdown.
- Verify hashes/signatures for downloaded tools where upstream provides them.
- Never bundle or request users' Google credentials.
- Do not silently install APKs or grant Android permissions.
- Do not transmit device information, APKs, logs, or screen captures to third parties.
