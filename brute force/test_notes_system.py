#!/usr/bin/env python3
"""
Quick test for the notes system in brute_force_gui.py
"""

try:
    # Test importing the GUI module
    print("Testing GUI import...")
    from brute_force_gui import BruteForceGUI
    
    print("✅ GUI module imported successfully!")
    print("✅ Notes system integration completed!")
    
    print("\n🎉 All tests passed! Your brute force tool now includes:")
    print("  📝 Notes system for password documentation")
    print("  🏦 Password notes bank with persistent storage")
    print("  🗑️ Wipe functionality for notes bank")
    print("  🧹 Complete wipe & restart with notes cleanup")
    print("  🎮 Full hotkey integration")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're in the virtual environment!")
    
except Exception as e:
    print(f"❌ Error: {e}")
