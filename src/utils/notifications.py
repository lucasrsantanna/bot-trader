import requests
import time
from functools import wraps
from config.settings import settings
from utils.logger import logger

def retry_telegram(retries=2, delay=1):
    """Decorator para retry em envio de mensagens Telegram"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt == retries:
                        logger.error(f"Falha no Telegram após {retries} tentativas: {e}")
                        return False
                    logger.warning(f"Telegram retry {attempt+1}/{retries} em {delay}s")
                    time.sleep(delay)
            return False
        return wrapper
    return decorator

class Notifier:
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.telegram_api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        self.enabled = bool(self.bot_token and self.chat_id)

        if not self.enabled:
            logger.warning("Telegram não configurado. Notificações desabilitadas. Configure TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID no .env")

    @retry_telegram(retries=2, delay=1)
    def send_message(self, message, silent=False):
        """
        Envia mensagem via Telegram

        Args:
            message: Texto da mensagem
            silent: Se True, não faz log de erro se falhar (útil para notificações não-críticas)
        """
        if not self.enabled:
            if not silent:
                logger.debug(f"Telegram desabilitado. Mensagem: {message}")
            return False

        try:
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(self.telegram_api_url, data=payload, timeout=5)
            response.raise_for_status()
            logger.info(f"✓ Telegram enviado: {message[:50]}...")
            return True
        except requests.exceptions.RequestException as e:
            raise  # Re-raise para o decorator retry lidar

    def send_trade_opened(self, symbol, side, price, quantity, sl, tp):
        """Notificação formatada de trade aberto"""
        message = f"""
🟢 *TRADE ABERTO*

📊 Par: `{symbol}`
🔵 Tipo: *{side.upper()}*
💰 Preço: `${price:.2f}`
📦 Quantidade: `{quantity:.6f}`
🛑 Stop Loss: `${sl:.2f}` ({((sl/price - 1) * 100):.2f}%)
🎯 Take Profit: `${tp:.2f}` ({((tp/price - 1) * 100):.2f}%)
        """
        return self.send_message(message.strip())

    def send_trade_closed(self, symbol, pnl, pnl_percent, reason):
        """Notificação formatada de trade fechado"""
        emoji = "🟢" if pnl > 0 else "🔴"
        message = f"""
{emoji} *TRADE FECHADO*

📊 Par: `{symbol}`
💵 P&L: `${pnl:.2f}` ({pnl_percent:.2f}%)
📌 Motivo: *{reason.replace('_', ' ').title()}*
        """
        return self.send_message(message.strip())

    def send_signal(self, action, confidence, price, rsi, macd_hist):
        """Notificação de sinal da IA"""
        emoji = "🔵" if action == "BUY" else "🔴" if action == "SELL" else "⚪"
        message = f"""
{emoji} *SINAL IA: {action}*

🎯 Confiança: `{confidence:.0%}`
💰 Preço: `${price:.2f}`
📈 RSI: `{rsi:.1f}`
📊 MACD Hist: `{macd_hist:.2f}`
        """
        return self.send_message(message.strip(), silent=True)

    def send_error(self, error_msg):
        """Notificação de erro crítico"""
        message = f"⚠️ *ERRO CRÍTICO*\n\n`{error_msg}`"
        return self.send_message(message)

notifier = Notifier()

