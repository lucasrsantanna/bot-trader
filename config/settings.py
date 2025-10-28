import os
from dotenv import load_dotenv

# Carrega .env.testnet se existir (para desenvolvimento com Testnet)
# Caso contrário, carrega .env (para produção ou desenvolvimento local)
env_file = '.env.testnet' if os.path.exists('.env.testnet') else '.env'
load_dotenv(env_file)

# Log para debug (opcional - pode remover se preferir)
if os.path.exists('.env.testnet'):
    print(f"[CONFIG] Usando credenciais do arquivo: .env.testnet (Testnet Mode)")
else:
    print(f"[CONFIG] Usando credenciais do arquivo: .env (Local/Production Mode)")

class Settings:
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    # Configurações gerais
    DEBUG = True
    LOG_LEVEL = "INFO"
    TIMEZONE = "America/Sao_Paulo"

settings = Settings()

