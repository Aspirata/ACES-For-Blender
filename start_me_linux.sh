#!/bin/bash
echo "Choose mode:"
echo "1. Install"
echo "2. Uninstall"
read -p "Enter 1 for install or 2 for uninstall: " mode

if [ "$mode" == "1" ]; then
    echo "You chose install mode."
    
    if ! command -v python3 &> /dev/null; then
        echo "Python not found. Please install Python..."
        read -p "Press Enter to close this window..."
        exit 1
    fi

    echo "Running install_universal.py..."
    python3 Scripts/install_universal.py
fi

if [ "$mode" == "2" ]; then
    echo "You chose uninstall mode."
    echo "Running uninstall_universal.py..."
    python3 Scripts/uninstall_universal.py
fi
