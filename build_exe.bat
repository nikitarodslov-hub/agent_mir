@echo off
echo ============================================
echo   Miraphone Agent - Build EXE
echo ============================================
echo.

echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building application...
pyinstaller miraphone_agent.spec --noconfirm

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Done!
echo   Application folder: dist\MiraphoneAgent\
echo   Run: MiraphoneAgent.exe
echo ============================================
echo.
pause
