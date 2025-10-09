import os
from dotenv import load_dotenv

load_dotenv()

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

