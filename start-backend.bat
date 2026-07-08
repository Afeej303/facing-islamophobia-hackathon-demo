@echo off
cd /d "%~dp0backend"
"%~dp0.venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8000
echo.
echo Backend stopped. If this was unexpected, copy the message above.
pause
