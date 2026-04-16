@echo off
chcp 65001 >nul
echo ============================================
echo   Miraphone Agent — Сборка .exe
echo ============================================
echo.

echo Устанавливаю PyInstaller...
pip install pyinstaller

echo.
echo Собираю приложение...
pyinstaller miraphone_agent.spec --noconfirm

if errorlevel 1 (
    echo.
    echo [ОШИБКА] Сборка завершилась с ошибкой.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Готово!
echo   Папка с программой: dist\MiraphoneAgent\
echo   Запускать: MiraphoneAgent.exe
echo ============================================
echo.
pause
