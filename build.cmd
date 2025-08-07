@echo off

pyinstaller --onefile --noconsole --add-data "ACES;ACES" "blender_aces_manager.py"

if exist "blender_aces_manager.exe" del "blender_aces_manager.exe"
move "dist\blender_aces_manager.exe" .\