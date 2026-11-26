@echo off
title AI Cyberattack Threat Radar - Live Ingestion Server
echo ===================================================================
echo   GLOBAL AI CYBERATTACK THREAT RADAR - 24/7 CONTINUOUS TELEMETRY
echo ===================================================================
echo.
echo [*] Checking dependencies...
python -c "import bs4, reportlab" 2>nul
if %errorlevel% neq 0 (
    echo [*] Installing required packages...
    pip install -r requirements.txt
)
echo.
echo [*] Launching Multi-Stream Live Server on http://localhost:8080 ...
echo [*] Press Ctrl+C at any time to stop.
echo.
python server.py
pause
