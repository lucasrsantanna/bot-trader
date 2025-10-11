@echo off
title Dashboard Avancado - Bot Trader
cls
echo ======================================================================
echo                  DASHBOARD AVANCADO - BOT TRADER
echo ======================================================================
echo.
echo Este dashboard permite:
echo   - Pausar/Retomar o bot
echo   - Forcar entradas/saidas manuais
echo   - Ajustar parametros em tempo real
echo   - Ver graficos e logs ao vivo
echo.
echo O dashboard vai abrir no navegador em:
echo http://localhost:8502
echo.
echo IMPORTANTE: Deixe esta janela ABERTA enquanto usa o dashboard
echo.
echo ======================================================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat

echo Iniciando dashboard avancado...
echo.

streamlit run dashboard_avancado.py --server.port 8502

pause
