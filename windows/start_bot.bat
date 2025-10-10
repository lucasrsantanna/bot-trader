@echo off
REM ================================================
REM  Bot Trader - Start Script (Windows)
REM  Inicia o bot com ambiente virtual ativado
REM ================================================

TITLE Bot Trader 24/7

REM Cores para output
COLOR 0A

echo ================================================
echo    BOT TRADER - INICIANDO
echo ================================================
echo.

REM Mudar para diretório do projeto
cd /d "c:\Users\lucas\Desktop\Bot Trader"
echo [INFO] Diretorio: %CD%
echo.

REM Verificar se venv existe
if not exist "venv\Scripts\activate.bat" (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Execute: python -m venv venv
    pause
    exit /b 1
)

REM Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo.

REM Adicionar diretório src ao PYTHONPATH
set PYTHONPATH=%CD%;%CD%\src;%PYTHONPATH%
echo [INFO] PYTHONPATH configurado
echo.

REM Verificar se .env existe
if not exist ".env" (
    echo [AVISO] Arquivo .env nao encontrado!
    echo Copie .env.example para .env e configure suas credenciais.
    pause
    exit /b 1
)

REM Criar diretório de logs se não existir
if not exist "logs" mkdir logs

REM Exibir informações
echo [INFO] Python:
python --version
echo.
echo [INFO] Iniciando bot...
echo [INFO] Pressione Ctrl+C para parar
echo.
echo ================================================
echo    BOT RODANDO
echo ================================================
echo.

REM Iniciar bot (logs serão salvos em logs\bot.log)
python src\main.py 2>&1

REM Se bot parar, pausar para ver erro
echo.
echo ================================================
echo [AVISO] Bot parou!
echo ================================================
echo.
pause
