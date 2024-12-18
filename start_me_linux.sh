#!/bin/bash

if ! command -v python3 &> /dev/null; then
    echo "Python not found. Please install Python..."
    read -p "Press Enter to close this window..."
    exit 1
else
    echo "Python is already installed."
fi

echo "Running combined_installer_universal_v2.py..."
python3 Scripts/combined_installer_universal_v2.py
pause