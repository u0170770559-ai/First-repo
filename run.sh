#!/bin/bash
# Alarm Clock Launcher for Linux/macOS
# Run: chmod +x run.sh && ./run.sh
# Or double-click in file manager (if configured to run scripts)

cd "$(dirname "$0")"

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    python3 gui.py
elif command -v python &> /dev/null; then
    python gui.py
else
    echo "Error: Python is not installed or not in PATH"
    read -p "Press Enter to exit..."
    exit 1
fi
