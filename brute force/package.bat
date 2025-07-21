@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo   7 Days to Die - Brute Force Mod
echo   Build and Package Script
echo ==========================================
echo.

:: Set variables
set "MOD_NAME=BruteForce"
set "VERSION=1.0.0"
set "SOURCE_DIR=%~dp0"
set "BUILD_DIR=%SOURCE_DIR%builds"
set "PACKAGE_DIR=%BUILD_DIR%\%MOD_NAME%_v%VERSION%"
set "ZIP_NAME=%MOD_NAME%_v%VERSION%.zip"

:: Create build directory
echo Creating build directory...
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"
mkdir "%BUILD_DIR%"
mkdir "%PACKAGE_DIR%"

echo.
echo Source Directory: %SOURCE_DIR%
echo Package Directory: %PACKAGE_DIR%
echo.

:: Copy mod files (excluding build files and git)
echo Copying mod files...

:: Core mod files
xcopy "%SOURCE_DIR%ModInfo.xml" "%PACKAGE_DIR%\" /y >nul
xcopy "%SOURCE_DIR%README.md" "%PACKAGE_DIR%\" /y >nul
xcopy "%SOURCE_DIR%install.bat" "%PACKAGE_DIR%\" /y >nul

:: Config directory
echo - Copying Config files...
xcopy "%SOURCE_DIR%Config" "%PACKAGE_DIR%\Config\" /s /e /i /y >nul

:: Scripts directory
echo - Copying Scripts files...
xcopy "%SOURCE_DIR%Scripts" "%PACKAGE_DIR%\Scripts\" /s /e /i /y >nul

:: Create additional documentation
echo.
echo Creating additional documentation...

:: Create installation instructions
echo Creating INSTALL.txt...
(
echo ==========================================
echo   BRUTE FORCE MOD - INSTALLATION GUIDE
echo ==========================================
echo.
echo AUTOMATIC INSTALLATION:
echo 1. Run install.bat as Administrator
echo 2. The script will find your 7 Days to Die installation
echo 3. Start the game and enjoy!
echo.
echo MANUAL INSTALLATION:
echo 1. Locate your 7 Days to Die installation directory
echo    Usually: Steam\steamapps\common\7 Days To Die\
echo 2. Create a "Mods" folder if it doesn't exist
echo 3. Copy this entire folder to: 7 Days To Die\Mods\BruteForce\
echo 4. Start the game
echo.
echo FEATURES:
echo - Craft Brute Force Tools at workbench
echo - Use tools on locked containers ^(safes, secure loot^)
echo - Progress through new Brute Force skill tree
echo - Craft Auto-Unlock Devices for guaranteed success
echo - Realistic success rates based on skill and tool quality
echo.
echo CRAFTING RECIPES:
echo Brute Force Tool:
echo - 2x Metal Pipe
echo - 1x Duct Tape  
echo - 3x Electrical Parts
echo - 2x Mechanical Parts
echo.
echo Auto-Unlock Device:
echo - 1x Brute Force Tool
echo - 5x Electrical Parts
echo - 1x Acid
echo.
echo COMPATIBILITY:
echo - Client-side mod ^(no server installation required^)
echo - Compatible with Alpha 21+
echo - Works with most other mods
echo.
echo SUPPORT:
echo If you encounter issues, check that:
echo - All mod files are in the correct location
echo - Game version is Alpha 21 or newer
echo - No conflicting mods that modify containers
echo.
echo VERSION: %VERSION%
echo ==========================================
) > "%PACKAGE_DIR%\INSTALL.txt"

:: Create changelog
echo Creating CHANGELOG.txt...
(
echo ==========================================
echo   BRUTE FORCE MOD - CHANGELOG
echo ==========================================
echo.
echo Version 1.0.0 ^(%date%^):
echo [NEW] Initial release
echo [NEW] Brute Force Tool with progressive success rates
echo [NEW] Auto-Unlock Device for guaranteed container opening
echo [NEW] New skill tree: Brute Force under Craftsmanship
echo [NEW] Realistic mechanics with cooldowns and tool degradation
echo [NEW] Support for safes and secure loot containers
echo [NEW] Experience rewards for successful and failed attempts
echo [NEW] Visual and audio feedback for all actions
echo [NEW] Configurable settings via mod_settings.xml
echo [NEW] Automatic installation script
echo [NEW] Comprehensive documentation
echo.
echo Features:
echo - Smart success calculation based on multiple factors
echo - Tool durability system with skill-based improvements
echo - Container lockdown after too many failed attempts
echo - Buff system for enhanced gameplay feedback
echo - Localization support for all text elements
echo.
echo ==========================================
) > "%PACKAGE_DIR%\CHANGELOG.txt"

:: Create mod info summary
echo Creating MOD_INFO.txt...
(
echo ==========================================
echo   BRUTE FORCE CONTAINER MOD
echo ==========================================
echo.
echo Name: Brute Force Container Mod
echo Version: %VERSION%
echo Author: Community Mod
echo Game: 7 Days to Die
echo Compatibility: Alpha 21+
echo Type: Client-side Gameplay Enhancement
echo.
echo DESCRIPTION:
echo This mod adds realistic brute force mechanics for opening
echo locked containers without traditional lockpicking. Create
echo specialized tools and develop skills to systematically
echo attempt combinations on safes and secure loot containers.
echo.
echo KEY FEATURES:
echo ✓ Two craftable tools: Brute Force Tool and Auto-Unlock Device
echo ✓ New skill progression system under Craftsmanship tree
echo ✓ Realistic success rates that improve with practice
echo ✓ Tool degradation and cooldown systems for balance
echo ✓ Experience rewards and visual/audio feedback
echo ✓ Configurable settings for server administrators
echo ✓ No server-side installation required
echo.
echo INSTALLATION:
echo Run install.bat or manually copy to Mods folder
echo.
echo FILES INCLUDED:
echo - ModInfo.xml ^(mod metadata^)
echo - Config folder ^(game modifications^)
echo - Scripts folder ^(custom behaviors^)
echo - Documentation ^(guides and info^)
echo - install.bat ^(automatic installer^)
echo.
echo ==========================================
) > "%PACKAGE_DIR%\MOD_INFO.txt"

:: Check if we have PowerShell for ZIP creation
echo.
echo Checking for PowerShell...
powershell -Command "Get-Command Compress-Archive" >nul 2>&1
if %errorlevel% equ 0 (
    echo Creating ZIP package...
    powershell -Command "Compress-Archive -Path '%PACKAGE_DIR%\*' -DestinationPath '%BUILD_DIR%\%ZIP_NAME%' -Force"
    if exist "%BUILD_DIR%\%ZIP_NAME%" (
        echo ✓ ZIP package created successfully: %ZIP_NAME%
    ) else (
        echo ✗ Failed to create ZIP package
    )
) else (
    echo PowerShell Compress-Archive not available. ZIP creation skipped.
    echo You can manually zip the contents of: %PACKAGE_DIR%
)

:: Create file list for verification
echo.
echo Creating file verification list...
echo ==========================================> "%PACKAGE_DIR%\FILE_LIST.txt"
echo   BRUTE FORCE MOD - FILE LIST>> "%PACKAGE_DIR%\FILE_LIST.txt"
echo ==========================================>> "%PACKAGE_DIR%\FILE_LIST.txt"
echo.>> "%PACKAGE_DIR%\FILE_LIST.txt"
dir "%PACKAGE_DIR%" /s /b | findstr /v "FILE_LIST.txt" >> "%PACKAGE_DIR%\FILE_LIST.txt"

:: Summary
echo.
echo ==========================================
echo   BUILD COMPLETE
echo ==========================================
echo.
echo Package created at: %PACKAGE_DIR%
if exist "%BUILD_DIR%\%ZIP_NAME%" echo ZIP file created: %BUILD_DIR%\%ZIP_NAME%
echo.
echo Package contents:
echo - Core mod files ^(ModInfo.xml, Config, Scripts^)
echo - Installation script ^(install.bat^)
echo - Documentation ^(README.md, INSTALL.txt, etc.^)
echo - File verification list
echo.
echo Ready for distribution!
echo.

:: Open build folder
echo Opening build folder...
start "" "%BUILD_DIR%"

echo.
echo Press any key to exit...
pause >nul
