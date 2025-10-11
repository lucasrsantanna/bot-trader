@echo off
title Testador Interativo - Bot Trader
cls
echo ======================================================================
echo                  TESTADOR INTERATIVO DOS CONTROLES
echo ======================================================================
echo.
echo Este programa vai GUIAR voce passo a passo para testar:
echo   1. Pausar/Retomar bot
echo   2. Fechar posicao manual
echo   3. Forcar compra manual
echo   4. Ajustar intervalo em tempo real
echo   5. Ajustar Stop Loss
echo.
echo IMPORTANTE: Execute EXECUTAR_BOT.bat ANTES de rodar este teste!
echo.
echo ======================================================================
echo.
pause

cd /d "%~dp0"
call venv\Scripts\activate.bat

cls
python testar_controles.py

pause
