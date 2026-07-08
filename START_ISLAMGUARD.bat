@echo off
cd /d "%~dp0"
echo Starting IslamGuard backend and frontend...
echo.
start "IslamGuard API" cmd /k ""%~dp0start-backend.bat""
timeout /t 2 /nobreak > nul
start "IslamGuard frontend" cmd /k ""%~dp0start-frontend.bat""
timeout /t 4 /nobreak > nul
start http://127.0.0.1:5173/shield
echo.
echo Two terminal windows should now be open.
echo Keep both windows open while using the app.
pause
