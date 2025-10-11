@echo off
echo ======================================================================
echo  TESTE RAPIDO DO BOT - ANALISE IMEDIATA
echo ======================================================================
echo.
echo Este script vai:
echo 1. Coletar dados de mercado AGORA
echo 2. Calcular RSI e MACD
echo 3. Gerar sinal de trading (BUY/SELL/HOLD)
echo 4. Mostrar se haveria entrada
echo.
echo Pressione qualquer tecla para comecar...
pause >nul

cd /d "%~dp0"

echo.
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo [INFO] Executando analise de mercado...
echo.

python -c "import asyncio; exec(open('test_strategy_complete.py').read())"

echo.
echo ======================================================================
echo  ANALISE CONCLUIDA
echo ======================================================================
echo.
echo Para executar o bot em LOOP (a cada 60s):
echo    1. Execute: windows\start_bot.bat
echo    2. Aguarde sinais aparecerem
echo.
pause
