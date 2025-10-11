@echo off
title BOT TRADER - Executando
color 0A
cd /d "%~dp0"
call venv\Scripts\activate.bat
cls
echo ======================================================================
echo                         BOT INICIADO
echo ======================================================================
echo.
echo Analisando mercado a cada 60 segundos...
echo Para parar: Pressione Ctrl+C
echo.
echo ======================================================================
echo.
python bot_automatico.py
echo.
echo ======================================================================
echo                         BOT ENCERRADO
echo ======================================================================
pause
