@echo off

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Starting installation...
    start /wait %PYTHON_INSTALLER% InstallAllUsers=1 PrependPath=1
    echo Installation completed.
) else (
    echo Python is already installed.
)

echo Choose mode:
echo 1. Install
echo 2. Uninstall
set /p mode=Enter 1 for install or 2 for uninstall: 

if "%mode%"=="1" (
    echo You chose install mode.

    echo Running install_universal_v2.py...
    python Scripts/install_universal_v2.py
    pause
)

if "%mode%"=="2" (
    echo You chose uninstall mode.

    echo Running uninstall_universal_v2.py...
    python Scripts/uninstall_universal.py
    pause
)