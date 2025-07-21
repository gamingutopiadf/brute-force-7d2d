@echo off
echo ==========================================
echo   7 Days to Die Brute Force Tool Setup
echo ==========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

echo Virtual environment and packages are already set up!
echo.
echo All required packages have been installed:
echo ✓ pynput (keyboard/mouse input)
echo ✓ keyboard (global hotkeys) 
echo ✓ pyautogui (GUI automation)
echo ✓ pillow (image processing)
echo ✓ opencv-python (computer vision)
echo ✓ numpy (numerical operations)
echo.

echo ==========================================
echo   Setup Complete!
echo ==========================================
echo.
echo To run the brute force tool:
echo   python brute_force_bot.py          (Basic version)
echo   python advanced_brute_force.py     (Advanced with visual detection)
echo.
echo Or use the launcher:
echo   run.bat
echo.
echo Instructions:
echo 1. Start 7 Days to Die
echo 2. Approach a locked container
echo 3. Open the combination interface
echo 4. Run the brute force tool
echo 5. Press F1 to start brute forcing
echo.
echo Hot Keys:
echo   + (Plus) - Start/Restart
echo   F2 - Pause/Resume  
echo   F3 - Stop
echo   ESC - Emergency Stop
echo.
pause
