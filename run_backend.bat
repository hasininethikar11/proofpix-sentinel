@echo off
setlocal
cd /d "%~dp0backend"
if not exist ".venv\Scripts\python.exe" (
  echo Please run setup_windows.bat first.
  pause
  exit /b 1
)
call ".venv\Scripts\activate.bat"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
