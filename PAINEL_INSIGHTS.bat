@echo off
title Painel de Insights - Bot Trader
cls
echo ======================================================================
echo                    PAINEL DE INSIGHTS
echo ======================================================================
echo.
echo Este painel mostra:
echo   - Analise automatica de performance
echo   - Insights sobre seus trades
echo   - Recomendacoes de acao
echo   - Sugestoes de ajustes
echo.
echo O painel vai abrir no navegador em:
echo http://localhost:8503
echo.
echo IMPORTANTE: Deixe esta janela ABERTA
echo.
echo ======================================================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat

echo Iniciando painel de insights...
echo.

streamlit run painel_insights.py --server.port 8503

pause
