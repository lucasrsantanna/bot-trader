@echo off
cls
echo ======================================================================
echo                    BOT TRADER - MODO DEBUG
echo ======================================================================
echo.
echo Este script mostra TODOS os erros se houver problema
echo.
echo ======================================================================
echo.

cd /d "%~dp0"

echo [1] Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo     OK - Ambiente ativado
echo.

echo [2] Configurando PYTHONPATH...
set PYTHONPATH=%CD%;%CD%\src;%PYTHONPATH%
echo     OK - PYTHONPATH configurado
echo.

echo [3] Verificando Python...
python --version
echo.

echo [4] Executando bot...
echo ======================================================================
echo.

python bot_automatico.py

echo.
echo ======================================================================
echo BOT ENCERRADO
echo ======================================================================
echo.
echo Se houver erro acima, copie a mensagem e me envie!
echo.
pause
