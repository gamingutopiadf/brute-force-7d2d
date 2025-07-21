#!/usr/bin/env python3
"""
Test script to verify all packages are installed correctly
"""

print("🔍 Testing package imports...")
print("=" * 40)

try:
    import pynput
    print("✓ pynput imported successfully")
    print(f"  Version: {pynput.__version__ if hasattr(pynput, '__version__') else 'Unknown'}")
except ImportError as e:
    print(f"✗ pynput failed: {e}")

try:
    import keyboard
    print("✓ keyboard imported successfully")
    print(f"  Version: {keyboard.__version__ if hasattr(keyboard, '__version__') else 'Unknown'}")
except ImportError as e:
    print(f"✗ keyboard failed: {e}")

try:
    import pyautogui
    print("✓ pyautogui imported successfully")
    print(f"  Version: {pyautogui.__version__ if hasattr(pyautogui, '__version__') else 'Unknown'}")
except ImportError as e:
    print(f"✗ pyautogui failed: {e}")

try:
    import cv2
    print("✓ opencv-python imported successfully")
    print(f"  Version: {cv2.__version__}")
except ImportError as e:
    print(f"✗ opencv-python failed: {e}")

try:
    import numpy
    print("✓ numpy imported successfully")
    print(f"  Version: {numpy.__version__}")
except ImportError as e:
    print(f"✗ numpy failed: {e}")

try:
    from PIL import Image
    print("✓ pillow (PIL) imported successfully")
    print(f"  Version: {Image.__version__ if hasattr(Image, '__version__') else 'Unknown'}")
except ImportError as e:
    print(f"✗ pillow failed: {e}")

print("=" * 40)
print("🎉 Package test complete!")
print()
print("If all packages show ✓, you're ready to run the brute force tool!")
print("Run: python brute_force_bot.py")
print("Then press + (Plus key) to start brute forcing in-game!")
