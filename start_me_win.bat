@echo off
echo Choose mode:
echo 1. Install
echo 2. Uninstall
set /p mode=Enter 1 for install or 2 for uninstall: 

if "%mode%"=="1" (
    echo You chose install mode.
    where python >nul 2>nul

    if %errorlevel% neq 0 (
        echo Python not found. Installing Python...
        start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1
        echo Python installed.
    )

    echo Running install_universal_v2.py...
    python Scripts/install_universal_v2.py
    pause
)

if "%mode%"=="2" (
    echo You chose uninstall mode.
    echo Running uninstall_win.py...
    python Scripts/uninstall_universal.py
    pause
)