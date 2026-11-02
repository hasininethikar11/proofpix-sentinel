@echo off
setlocal
cd /d "%~dp0backend"
echo === PROOFPIX SENTINEL setup ===
where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher 'py' was not found. Install Python 3.11 or 3.12 from python.org and select Add Python to PATH.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  py -m venv .venv
  if errorlevel 1 goto failed
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
if errorlevel 1 goto failed
python -m pip install -r requirements.txt
if errorlevel 1 goto failed
echo.
echo === Running automated backend tests ===
python -m pytest -q
if errorlevel 1 goto failed
echo.
echo Setup and tests completed successfully. To start the backend, double-click run_backend.bat in the project root.
pause
exit /b 0
:failed
echo.
echo Setup or tests failed. Please take a screenshot of this window and share it for troubleshooting.
pause
exit /b 1
