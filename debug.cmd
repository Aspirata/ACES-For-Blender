@echo off

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed.
    pause
    exit

) else (
    echo Python is already installed.
)

pip install pyqt6

echo Running ACES Installer.py...
python "ACES Installer.py"
pause