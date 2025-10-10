@echo off
REM ================================================
REM  Bot Trader - Monitor Script (Windows)
REM  Verifica status, recursos e logs do bot
REM ================================================

TITLE Bot Trader - Monitor

COLOR 0B

cls
echo ================================================
echo    BOT TRADER - MONITOR
echo ================================================
echo Data: %date% %time%
echo.

REM Mudar para diretório do projeto
cd /d "c:\Users\lucas\Desktop\Bot Trader"

REM ================================================
echo ================================================
echo  STATUS DO PROCESSO
echo ================================================

REM Verificar se Python está rodando
tasklist /fi "imagename eq python.exe" /fo csv /nh | find /i "python.exe" >nul
if %errorlevel%==0 (
    echo [OK] Bot esta RODANDO
    echo.

    REM Mostrar detalhes do processo
    echo Detalhes do processo:
    for /f "tokens=2,5" %%a in ('tasklist /fi "imagename eq python.exe" /fo csv /nh ^| find /i "python"') do (
        echo   PID: %%a
        echo   Memoria: %%b
    )
) else (
    echo [ERRO] Bot NAO esta rodando!
    echo.
    echo Tentando reiniciar...
    start "" "windows\start_bot.bat"
    timeout /t 3 >nul

    REM Verificar novamente
    tasklist /fi "imagename eq python.exe" /fo csv /nh | find /i "python.exe" >nul
    if %errorlevel%==0 (
        echo [OK] Bot reiniciado com sucesso!
    ) else (
        echo [ERRO] Falha ao reiniciar bot!
    )
)

echo.

REM ================================================
echo ================================================
echo  RECURSOS DO SISTEMA
echo ================================================

REM CPU e Memória total
echo Sistema:
wmic cpu get loadpercentage /value | find "LoadPercentage"
wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /value | find "="

echo.

REM ================================================
echo ================================================
echo  ULTIMAS OPERACOES (LOG)
echo ================================================

if exist "logs\bot.log" (
    echo Ultimas 10 linhas do log:
    echo.
    powershell -Command "Get-Content 'logs\bot.log' -Tail 10"
) else (
    echo [AVISO] Arquivo de log nao encontrado
)

echo.

REM ================================================
echo ================================================
echo  ESTATISTICAS DO BANCO
echo ================================================

if exist "bot_data.db" (
    echo Database encontrado: bot_data.db

    REM Verificar tamanho
    for %%F in (bot_data.db) do echo   Tamanho: %%~zF bytes

    REM Se sqlite3 estiver instalado, mostrar stats
    where sqlite3 >nul 2>&1
    if %errorlevel%==0 (
        echo.
        echo   Estatisticas:
        sqlite3 bot_data.db "SELECT COUNT(*) as 'Trades' FROM trades;" 2>nul
        sqlite3 bot_data.db "SELECT COUNT(*) as 'Sinais' FROM signals;" 2>nul
    ) else (
        echo   [INFO] Instale sqlite3 para ver estatisticas completas
    )
) else (
    echo [AVISO] Database ainda nao foi criado
)

echo.

REM ================================================
echo ================================================
echo  CONECTIVIDADE
echo ================================================

echo Testando conexao com Binance...
ping -n 1 api.binance.com >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Conexao com Binance OK
) else (
    echo [ERRO] Sem conexao com Binance!
)

echo.

REM ================================================
echo ================================================
echo  COMANDOS UTEIS
echo ================================================
echo.
echo   Ver logs ao vivo:
echo     powershell Get-Content logs\bot.log -Wait -Tail 20
echo.
echo   Reiniciar bot:
echo     windows\start_bot.bat
echo.
echo   Fazer backup:
echo     windows\backup.bat
echo.
echo ================================================
echo.

pause
