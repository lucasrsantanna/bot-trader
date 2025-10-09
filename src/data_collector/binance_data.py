import ccxt
import pandas as pd
import asyncio
from config.settings import settings
from utils.logger import logger

class BinanceDataCollector:
    def __init__(self, symbol='BTC/USDT', timeframe='1m', limit=100):
        self.exchange = ccxt.binance({
            'apiKey': settings.BINANCE_API_KEY,
            'secret': settings.BINANCE_SECRET_KEY,
            'options': {
                'defaultType': 'future', # Ou 'spot' dependendo do seu interesse
            },
            'enableRateLimit': True, # Para evitar exceder os limites de requisição
        })
        self.symbol = symbol
        self.timeframe = timeframe
        self.limit = limit

    async def fetch_ohlcv(self):
        try:
            # ccxt fetch_ohlcv retorna uma lista de listas
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=self.limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            logger.info(f"Dados OHLCV de {self.symbol} ({self.timeframe}) coletados com sucesso.")
            return df
        except ccxt.NetworkError as e:
            logger.error(f"Erro de rede ao coletar dados da Binance: {e}")
            return None
        except ccxt.ExchangeError as e:
            logger.error(f"Erro da Exchange Binance ao coletar dados: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao coletar dados da Binance: {e}")
            return None

    async def fetch_current_price(self):
        try:
            ticker = self.exchange.fetch_ticker(self.symbol)
            current_price = ticker['last']
            logger.info(f"Preço atual de {self.symbol}: {current_price}")
            return current_price
        except ccxt.NetworkError as e:
            logger.error(f"Erro de rede ao buscar preço atual da Binance: {e}")
            return None
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


