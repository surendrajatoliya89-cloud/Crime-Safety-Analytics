@echo off
title CrimeWatch Analytics - Web Server
cd /d "%~dp0"
echo ========================================================
echo Starting CrimeWatch Analytics Web Application...
echo ========================================================
echo.
echo Opening browser at: http://127.0.0.1:5000
start http://127.0.0.1:5000
echo.
echo Server running. Press Ctrl+C in this window to stop.
.\venv\Scripts\python.exe app.py
pause
