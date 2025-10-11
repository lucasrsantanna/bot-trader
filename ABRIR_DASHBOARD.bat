@echo off
title Dashboard - Bot Trader
cls
echo ======================================================================
echo                    ABRINDO DASHBOARD
echo ======================================================================
echo.
echo O dashboard vai abrir no navegador em:
echo http://localhost:8501
echo.
echo IMPORTANTE: Deixe esta janela ABERTA enquanto usa o dashboard
echo.
echo ======================================================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat

echo Iniciando servidor Streamlit...
echo.

streamlit run dashboard.py

pause
