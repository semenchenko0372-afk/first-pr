@echo off
chcp 65001 >nul
set "BOOK=%~1"
if "%BOOK%"=="" (
  echo.
  echo   Перетащите файл книги .txt мышкой прямо на этот файл OZVUCHIT.bat
  echo.
  pause
  exit /b
)

set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY python --version >nul 2>&1 && set "PY=python"
if not defined PY (
  echo Python не найден. Устанавливаю его автоматически...
  winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
  echo.
  echo Python установлен. Закройте это окно и снова перетащите книгу на OZVUCHIT.bat
  pause
  exit /b
)

echo Подготовка, первый раз может занять минуту...
%PY% -m pip install --quiet --upgrade edge-tts
%PY% "%~dp0ozvuchka.py" "%BOOK%"
echo.
pause
