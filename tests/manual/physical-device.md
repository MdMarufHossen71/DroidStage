# Manual test checklist - physical Android device

Prerequisites: Windows 11, Chrome/Edge, Python 3.12, Node LTS, Android platform-tools on PATH, USB cable, Android phone with Developer options + USB debugging enabled.

1. Run `scripts/windows/doctor.ps1` - verify adb/Node/Python reported.
2. Run `Start-DroidStage.bat`.
3. Confirm browser opens local URL with token.
4. Connect phone; approve USB debugging prompt.
5. Click Refresh devices; phone appears as `device`.
6. Disconnect/reconnect cable; state updates after refresh.
7. Revoke authorization on phone; state shows `unauthorized`.
8. Select an APK; verify filename/size/metadata shown.
9. Install without checking confirmation -> button disabled.
10. Check confirmation and install; verify result (Success/Failed) accurate.
11. List packages; launch/uninstall a test app with confirmation.
12. Run `Stop-DroidStage.ps1`; verify process stopped.
13. Verify no app data left in repo; data under %LOCALAPPDATA%\DroidStage.
