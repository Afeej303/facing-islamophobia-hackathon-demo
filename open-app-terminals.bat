@echo off
start "IslamGuard API" cmd /k ""%~dp0start-backend.bat""
start "IslamGuard frontend" cmd /k ""%~dp0start-frontend.bat""
