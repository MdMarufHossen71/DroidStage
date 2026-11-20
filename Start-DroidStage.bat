@echo off
setlocal
powershell -ExecutionPolicy Bypass -File "%~dp0Start-DroidStage.ps1"
if errorlevel 1 pause
endlocal