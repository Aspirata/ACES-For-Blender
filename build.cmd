@echo off

python -m pip install -r requirements.txt

python -m nuitka ^
  --standalone ^
  --onefile ^
  --enable-plugin=pyside6 ^
  --include-data-dir=ACES=ACES ^
  --windows-console-mode=disable ^
  blender_aces_manager.py

pause