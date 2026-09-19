@echo off
rem Starts the App Server. Works from any folder once this directory is on PATH.
rem First run (no .venv yet) calls setup.ps1 to verify/install Python and dependencies.
set "ROOT=%~dp0"
if not exist "%ROOT%.venv\Scripts\python.exe" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%ROOT%setup.ps1" -NoRun || exit /b 1
)
cd /d "%ROOT%"
".venv\Scripts\python.exe" -m app.main %*
