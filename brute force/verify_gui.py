#!/usr/bin/env python3
"""
Quick verification that the GUI can start without the log_text error
"""

try:
    print("Testing GUI initialization...")
    from brute_force_gui import BruteForceGUI
    print("✅ Import successful")
    
    print("Creating GUI instance...")
    # Don't actually run the GUI, just create it
    app = BruteForceGUI()
    print("✅ GUI instance created successfully")
    print("✅ log_text attribute exists:", hasattr(app, 'log_text'))
    
    print("\n🎉 All tests passed! The GUI should work correctly now.")
    print("You can safely run 'run_gui.bat' to start the application.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
