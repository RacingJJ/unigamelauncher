@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo       UniGame Launcher - Build
echo ========================================

py -m pip install --upgrade pip
if errorlevel 1 goto :failed
py -m pip install -r requirements-build.txt
if errorlevel 1 goto :failed
py UniGameLauncher_v1_2.py --build
if errorlevel 1 goto :failed

echo.
echo Build finished. Check the dist folder.
pause
exit /b 0

:failed
echo.
echo Build failed. Review the error above.
pause
exit /b 1
