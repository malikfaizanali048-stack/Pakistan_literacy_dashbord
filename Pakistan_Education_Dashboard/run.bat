@echo off
echo ===================================================
echo Pakistan Education Dashboard - Launcher
echo ===================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python found!
echo.

REM Run the setup and launch script
echo Installing dependencies and launching dashboard...
echo.
python setup_and_run.py

if errorlevel 1 (
    echo.
    echo ===================================================
    echo An error occurred. Please check the error message above.
    echo ===================================================
    pause
    exit /b 1
)
