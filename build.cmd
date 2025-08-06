@echo off
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    pip install pyinstaller
)

pyinstaller --onefile --noconsole --strip "ACES Installer.py"

if exist "ACES Installer.exe" del "ACES Installer.exe"
move "dist\ACES Installer.exe" .\