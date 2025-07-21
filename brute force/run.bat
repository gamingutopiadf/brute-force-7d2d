@echo off
echo ==========================================
echo   7 Days to Die Brute Force Tool
echo ==========================================
echo.
echo Choose your version:
echo.
echo 1. Basic Brute Force Tool
echo    - Simple keyboard automation
echo    - Manual success detection
echo    - Hotkey controls (Plus/F2/F3)
echo.
echo 2. Advanced Brute Force Tool  
echo    - Visual success detection
echo    - Screen capture analysis
echo    - OCR text recognition
echo    - Automatic stopping when successful
echo.
echo 3. Setup/Install Dependencies
echo    - Install required Python packages
echo    - Check Python installation
echo.
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting Basic Brute Force Tool...
    ".venv\Scripts\python.exe" brute_force_bot.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Advanced Brute Force Tool...
    ".venv\Scripts\python.exe" advanced_brute_force.py
) else if "%choice%"=="3" (
    echo.
    echo Running setup...
    call setup.bat
) else if "%choice%"=="4" (
    echo.
    echo Goodbye!
    exit /b 0
) else (
    echo.
    echo Invalid choice. Please try again.
    pause
    goto :start
)

echo.
pause
