@echo off
REM ================================================
REM  Bot Trader - Backup Script (Windows)
REM  Faz backup do banco de dados e configurações
REM ================================================

TITLE Bot Trader - Backup

COLOR 0E

cls
echo ================================================
echo    BOT TRADER - BACKUP
echo ================================================
echo Data: %date% %time%
echo.

REM Mudar para diretório do projeto
cd /d "c:\Users\lucas\Desktop\Bot Trader"

REM Criar diretório de backup
set BACKUP_DIR=bot-trader-backups
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Timestamp para nomes de arquivo
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,8%_%datetime:~8,6%

echo Destino: %BACKUP_DIR%
echo.

set BACKUP_COUNT=0

REM ================================================
echo ================================================
echo  FAZENDO BACKUP
echo ================================================
echo.

REM 1. Backup do banco de dados
if exist "bot_data.db" (
    echo [1/4] Backup Database...
    copy /Y "bot_data.db" "%BACKUP_DIR%\bot_data_%TIMESTAMP%.db" >nul
    if %errorlevel%==0 (
        echo       [OK] bot_data_%TIMESTAMP%.db
        set /a BACKUP_COUNT+=1
    ) else (
        echo       [ERRO] Falha no backup do database
    )
) else (
    echo [1/4] [SKIP] bot_data.db nao encontrado
)

echo.

REM 2. Backup do JSON (se existir)
if exist "bot_dados.json" (
    echo [2/4] Backup JSON...
    copy /Y "bot_dados.json" "%BACKUP_DIR%\bot_dados_%TIMESTAMP%.json" >nul
    if %errorlevel%==0 (
        echo       [OK] bot_dados_%TIMESTAMP%.json
        set /a BACKUP_COUNT+=1
    ) else (
        echo       [ERRO] Falha no backup do JSON
    )
) else (
    echo [2/4] [SKIP] bot_dados.json nao encontrado
)

echo.

REM 3. Backup dos logs
if exist "logs" (
    echo [3/4] Backup Logs...

    REM Usar PowerShell para compactar
    powershell -Command "Compress-Archive -Path 'logs\*' -DestinationPath '%BACKUP_DIR%\logs_%TIMESTAMP%.zip' -Force" 2>nul
    if %errorlevel%==0 (
        echo       [OK] logs_%TIMESTAMP%.zip
        set /a BACKUP_COUNT+=1
    ) else (
        REM Fallback: copiar pasta inteira
        xcopy /E /I /Y "logs" "%BACKUP_DIR%\logs_%TIMESTAMP%\" >nul
        if %errorlevel%==0 (
            echo       [OK] logs_%TIMESTAMP%\ (pasta)
            set /a BACKUP_COUNT+=1
        ) else (
            echo       [ERRO] Falha no backup dos logs
        )
    )
) else (
    echo [3/4] [SKIP] Diretorio logs nao encontrado
)

echo.

REM 4. Backup do .env
if exist ".env" (
    echo [4/4] Backup .env...
    copy /Y ".env" "%BACKUP_DIR%\.env_%TIMESTAMP%" >nul
    if %errorlevel%==0 (
        echo       [OK] .env_%TIMESTAMP%
        set /a BACKUP_COUNT+=1
    ) else (
        echo       [ERRO] Falha no backup do .env
    )
) else (
    echo [4/4] [SKIP] .env nao encontrado
)

echo.

REM ================================================
echo ================================================
echo  RESUMO
echo ================================================
echo.
echo [OK] %BACKUP_COUNT% arquivos salvos em backup
echo      Local: %BACKUP_DIR%\
echo.

REM ================================================
echo ================================================
echo  ESTATISTICAS
echo ================================================
echo.

REM Contar arquivos de backup
for /f %%A in ('dir /b "%BACKUP_DIR%\*" 2^>nul ^| find /c /v ""') do set TOTAL_FILES=%%A
echo   Total de arquivos: %TOTAL_FILES%

REM Tamanho total
for /f "tokens=3" %%A in ('dir /-c "%BACKUP_DIR%" ^| find "File(s)"') do set SIZE=%%A
echo   Espaco usado: %SIZE% bytes

echo.

REM Listar últimos 5 backups de DB
if exist "%BACKUP_DIR%\bot_data_*.db" (
    echo   Ultimos backups de DB:
    for /f "delims=" %%F in ('dir /b /o-d "%BACKUP_DIR%\bot_data_*.db" 2^>nul') do (
        set COUNT_DB=0
        set /a COUNT_DB+=1
        if !COUNT_DB! LEQ 5 (
            for %%S in ("%BACKUP_DIR%\%%F") do (
                echo     - %%F (%%~zS bytes^)
            )
        )
    )
)

echo.

REM ================================================
echo ================================================
echo  LIMPEZA (Opcional)
echo ================================================
echo.

REM Perguntar se deseja limpar backups antigos
choice /C YN /M "Deseja remover backups com mais de 30 dias"
if %errorlevel%==1 (
    echo.
    echo Limpando backups antigos...

    REM Usar PowerShell para deletar arquivos antigos
    powershell -Command "Get-ChildItem '%BACKUP_DIR%' | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item -Force" 2>nul

    echo [OK] Limpeza concluida
) else (
    echo.
    echo [INFO] Limpeza ignorada
)

echo.

REM ================================================
echo ================================================
echo  COMO RECUPERAR UM BACKUP
echo ================================================
echo.
echo   1. Parar o bot (fechar janela ou Ctrl+C)
echo.
echo   2. Restaurar database:
echo      copy "%BACKUP_DIR%\bot_data_TIMESTAMP.db" "bot_data.db"
echo.
echo   3. Reiniciar bot:
echo      windows\start_bot.bat
echo.
echo ================================================
echo.

REM Verificar integridade do DB (se sqlite3 instalado)
where sqlite3 >nul 2>&1
if %errorlevel%==0 (
    if exist "bot_data.db" (
        echo Verificando integridade do database...
        for /f "delims=" %%I in ('sqlite3 bot_data.db "PRAGMA integrity_check;" 2^>nul') do (
            if "%%I"=="ok" (
                echo [OK] Database integro
            ) else (
                echo [AVISO] Possivel problema no database: %%I
                echo Considere restaurar um backup recente
            )
        )
        echo.
    )
)

REM Log do backup
echo %date% %time% - Backup manual - %BACKUP_COUNT% arquivos >> "%BACKUP_DIR%\backup.log"

echo Backup completo!
echo.
pause
