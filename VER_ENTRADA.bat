@echo off
color 0A
cls
echo ======================================================================
echo           BOT TRADER - EXECUTAR E VER ENTRADAS
echo ======================================================================
echo.
echo Este script vai:
echo    - Executar o bot em tempo real
echo    - Mostrar analise a cada 60 segundos
echo    - Indicar quando houver ENTRADA (BUY/SELL)
echo.
echo Modo: SIMULACAO (nao envia ordens reais)
echo.
echo ======================================================================
echo Pressione qualquer tecla para INICIAR o bot...
pause >nul

cd /d "%~dp0"

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Executar bot
cls
echo ======================================================================
echo                    BOT EXECUTANDO
echo ======================================================================
echo.
echo Analisando mercado a cada 60 segundos...
echo Pressione Ctrl+C para PARAR o bot
echo.
echo ======================================================================
echo.

python bot_automatico.py

echo.
echo ======================================================================
echo Bot encerrado
echo ======================================================================
pause
