#!/usr/bin/env python3
"""
Test hotkeys functionality for the brute force GUI
"""

import time
from brute_force_gui import BruteForceGUI

def test_hotkeys():
    """Simple test to verify hotkeys are working"""
    print("Testing hotkey functionality...")
    print("This will start the GUI. Test these hotkeys:")
    print("  F9  - Start brute force")
    print("  F10 - Stop brute force") 
    print("  F11 - Pause/Resume")
    print("  Ctrl+F12 - Emergency stop")
    print("Close the GUI window when done testing.")
    
    app = BruteForceGUI()
    app.run()

if __name__ == "__main__":
    test_hotkeys()
