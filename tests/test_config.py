import unittest
import os
from config.settings import Settings
from config.trading_params import TradingParams

class TestConfig(unittest.TestCase):

    def setUp(self):
        # Configurar variáveis de ambiente para teste
        os.environ["BINANCE_API_KEY"] = "test_api_key"
        os.environ["BINANCE_SECRET_KEY"] = "test_secret_key"
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_bot_token"
        os.environ["TELEGRAM_CHAT_ID"] = "test_chat_id"
        # Recarregar settings para pegar as novas variáveis de ambiente
        from importlib import reload
        import config.settings
        reload(config.settings)
        self.settings = config.settings.settings

    def tearDown(self):
        # Limpar variáveis de ambiente após o teste
        del os.environ["BINANCE_API_KEY"]
        del os.environ["BINANCE_SECRET_KEY"]
        del os.environ["TELEGRAM_BOT_TOKEN"]
        del os.environ["TELEGRAM_CHAT_ID"]
        # Recarregar settings para o estado original
        from importlib import reload
        import config.settings
        reload(config.settings)

    def test_settings_loading(self):
        self.assertEqual(self.settings.BINANCE_API_KEY, "test_api_key")
        self.assertEqual(self.settings.BINANCE_SECRET_KEY, "test_secret_key")
        self.assertEqual(self.settings.TELEGRAM_BOT_TOKEN, "test_bot_token")
        self.assertEqual(self.settings.TELEGRAM_CHAT_ID, "test_chat_id")
        self.assertTrue(self.settings.DEBUG)
        self.assertEqual(self.settings.LOG_LEVEL, "INFO")

    def test_trading_params(self):
        params = TradingParams()
        self.assertEqual(params.RISK_PER_TRADE_PERCENT, 0.01)
        self.assertEqual(params.MAX_CAPITAL_RISK_PERCENT, 0.05)
        self.assertEqual(params.TAKE_PROFIT_PERCENT, 0.005)
        self.assertEqual(params.STOP_LOSS_PERCENT, 0.002)
        self.assertEqual(params.AI_CONFIDENCE_THRESHOLD, 0.70)
        self.assertEqual(params.DEFAULT_SYMBOL, "BTC/USDT")
        self.assertEqual(params.DEFAULT_TIMEFRAME, "1m")

if __name__ == '__main__':
    unittest.main()

