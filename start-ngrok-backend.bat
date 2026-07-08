@echo off
echo Starting ngrok for the IslamGuard backend on port 8000...
echo Copy the HTTPS forwarding URL and set:
echo FB_REDIRECT_URI=https://YOUR-NGROK-DOMAIN/api/facebook/callback
echo.
ngrok http 8000
pause
