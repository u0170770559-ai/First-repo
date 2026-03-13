@echo off
REM Alarm Clock Launcher for Windows
REM Double-click this file to run the Alarm Clock application

echo Starting Alarm Clock...
pythonw.exe gui.py

if errorlevel 1 (
    echo Failed to start with pythonw.exe, trying python.exe...
    python.exe gui.py
)

if errorlevel 1 (
    echo Error: Could not start Alarm Clock.
    echo Please make sure Python is installed and added to your PATH.
    pause
)
