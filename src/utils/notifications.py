import requests
from config.settings import settings
from utils.logger import logger

class Notifier:
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.telegram_api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_message(self, message):
        if not self.bot_token or not self.chat_id:
            logger.warning("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set. Cannot send Telegram notification.")
            return

        try:
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(self.telegram_api_url, data=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            logger.info(f"Telegram notification sent: {message}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Telegram notification: {e}")

notifier = Notifier()

