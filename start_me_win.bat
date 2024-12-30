@echo off

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Starting installation...
    start /wait Scripts\python-3.13_installer.exe /passive InstallAllUsers=1 PrependPath=1
    echo Installation completed.
    pause
    start "" "start_me_win.bat"
    exit
    
) else (
    echo Python is already installed.
)

pip install pyqt6

echo Running combined_installer_universal_v2.py...
python Scripts/combined_installer_universal_v2.py