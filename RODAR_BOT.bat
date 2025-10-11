@echo off
cls
echo ======================================================================
echo                    BOT TRADER EM EXECUCAO
echo ======================================================================
echo.
echo O bot vai analisar o mercado a cada 60 segundos
echo Quando encontrar oportunidade (RSI ^< 40 ou ^> 60) vai mostrar:
echo.
echo    [ANALISE] Preco: $XXX,XXX | RSI: XX.X ^| Sinal: BUY/SELL
echo.
echo    [EXECUTANDO COMPRA/VENDA]
echo    Stop Loss: -0.2%%
echo    Take Profit: +0.5%%
echo.
echo Pressione Ctrl+C para PARAR
echo ======================================================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat
python bot_automatico.py

pause
