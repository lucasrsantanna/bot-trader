import ccxt
import pandas as pd
import asyncio
import time
from functools import wraps
from config.settings import settings
from utils.logger import logger

def retry_with_backoff(retries=3, backoff_in_seconds=2):
    """
    Decorator para retry com exponential backoff
    Recomendação Manus AI - garante resiliência em operações 24/7
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except (ccxt.NetworkError, ccxt.RequestTimeout) as e:
                    if x == retries:
                        logger.error(f"Falha após {retries} tentativas: {e}")
                        raise
                    wait = (backoff_in_seconds * 2 ** x)
                    logger.warning(f"Erro {type(e).__name__}: {e}. Retry {x+1}/{retries} em {wait}s")
                    time.sleep(wait)
                    x += 1
        return wrapper
    return decorator

class BinanceDataCollector:
    def __init__(self, symbol='BTC/USDT', timeframe='1m', limit=100):
        # Configurar Testnet se USE_TESTNET=true
        import os
        use_testnet = os.getenv('USE_TESTNET', 'false').lower() == 'true'

        if use_testnet:
            # Para Testnet, usar modo sandbox
            self.exchange = ccxt.binance({
                'apiKey': settings.BINANCE_API_KEY,
                'secret': settings.BINANCE_SECRET_KEY,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                    'fetchCurrencies': False,  # Testnet não tem endpoint sapi
                },
            })
            # Setar URLs manualmente após criação
            self.exchange.urls['api'] = 'https://testnet.binance.vision'
            self.exchange.hostname = 'testnet.binance.vision'
            # Desabilitar load_markets automático (usa endpoints que testnet não tem)
            self.exchange.options['loadMarkets'] = False
        else:
            # Produção - Futures
            self.exchange = ccxt.binance({
                'apiKey': settings.BINANCE_API_KEY,
                'secret': settings.BINANCE_SECRET_KEY,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future',
                }
            })

        self.symbol = symbol
        self.timeframe = timeframe
        self.limit = limit

    @retry_with_backoff(retries=3, backoff_in_seconds=2)
    def _fetch_ohlcv_with_retry(self):
        """Método interno com retry automático"""
        return self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=self.limit)

    async def fetch_ohlcv(self):
        try:
            # ccxt fetch_ohlcv retorna uma lista de listas
            ohlcv = self._fetch_ohlcv_with_retry()
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            logger.info(f"Dados OHLCV de {self.symbol} ({self.timeframe}) coletados com sucesso.")
            return df
        except ccxt.ExchangeError as e:
            logger.error(f"Erro da Exchange Binance ao coletar dados: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao coletar dados da Binance: {e}")
            return None

    @retry_with_backoff(retries=3, backoff_in_seconds=2)
    def _fetch_ticker_with_retry(self):
        """Método interno com retry automático"""
        return self.exchange.fetch_ticker(self.symbol)

    async def fetch_current_price(self):
        try:
            ticker = self._fetch_ticker_with_retry()
            current_price = ticker['last']
            logger.info(f"Preço atual de {self.symbol}: {current_price}")
            return current_price
        except ccxt.ExchangeError as e:
            logger.error(f"Erro da Exchange Binance ao buscar preço atual: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar preço atual da Binance: {e}")
            return None

# Exemplo de uso (para testes)
async def main():
    collector = BinanceDataCollector()
    data = await collector.fetch_ohlcv()
    if data is not None:
        print(data.tail())
    
    price = await collector.fetch_current_price()
    if price is not None:
        print(f"Current Price: {price}")

if __name__ == '__main__':
    # Para rodar o exemplo, você precisará de um loop de eventos asyncio
    # e ter as chaves de API da Binance configuradas no .env
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Execução interrompida pelo usuário.")


