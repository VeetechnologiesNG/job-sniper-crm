@echo off
title Job Sniper CRM - 23 Application Daily Quota Engine
cd /d "%~dp0"
echo ========================================================
echo        Starting Job Sniper CRM (23 Daily Quota Engine)
echo ========================================================
echo.
echo Launching Streamlit on port 8502...
echo.
python -m streamlit run app.py --server.port 8502 --server.headless false
pause
