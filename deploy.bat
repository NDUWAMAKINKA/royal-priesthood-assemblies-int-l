@echo off
setlocal
rem One-command deploy: pushes the site and API, then waits until both are live.
rem Usage:  deploy.bat
rem         deploy.bat -m "content: new devotional"
set "SCRIPT=%~dp0scripts\deploy.py"

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%SCRIPT%" %*
  exit /b %errorlevel%
)

where python >nul 2>nul
if %errorlevel%==0 (
  python "%SCRIPT%" %*
  exit /b %errorlevel%
)

echo Python 3 is required to deploy. Install it from https://python.org
exit /b 2
