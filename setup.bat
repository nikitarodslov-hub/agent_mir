@echo off
chcp 65001 >nul
echo ============================================
echo   Miraphone Agent — Установка зависимостей
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден.
    echo Скачайте Python 3.9+ с https://python.org и установите.
    echo При установке поставьте галочку "Add Python to PATH"
    pause
    exit /b 1
)

echo Устанавливаю зависимости...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ОШИБКА] Не удалось установить зависимости.
    pause
    exit /b 1
)

echo.
echo Готово! Теперь запустите start.bat
echo.
pause
