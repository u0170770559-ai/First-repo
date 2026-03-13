#!/usr/bin/env python3
"""
Alarm Clock Launcher - Windows No-Console Version
Double-click this file to run the Alarm Clock without a console window.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the GUI
from gui import main

if __name__ == '__main__':
    main()
