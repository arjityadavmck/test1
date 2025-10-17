#!/usr/bin/env python3
"""
TestCase Generator Desktop App Launcher
=======================================

Quick launcher script for the desktop UI application.
This handles the Python path setup and launches the main app.

Usage:
    python launch_ui.py
    
Or make executable and run directly:
    chmod +x launch_ui.py
    ./launch_ui.py
"""

import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import and run the main app
try:
    from ui_app.main import main
    
    if __name__ == "__main__":
        print("🚀 Starting TestCase Generator Desktop App...")
        main()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have installed the required dependencies:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting application: {e}")
    sys.exit(1)