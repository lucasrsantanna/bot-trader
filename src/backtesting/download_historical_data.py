import ccxt
import pandas as pd
import asyncio
from datetime import datetime, timedelta
from config.settings import settings
from utils.logger import logger

class HistoricalDataLoader:
    def __init__(self, symbol=\'BTC/USDT\', timeframe=\'1h\'):
        self.exchange = ccxt.binance({
            \'apiKey\': settings.BINANCE_API_KEY,
            \'secret\': settings.BINANCE_SECRET_KEY,
            \'options\': {
                \'defaultType\': \'future\', # Ou \'spot\' dependendo do seu interesse
            },
            \'enableRateLimit\': True,
        })
        self.symbol = symbol
        self.timeframe = timeframe
        logger.info(f"HistoricalDataLoader inicializado para {symbol} ({timeframe}).")

    async def download_ohlcv(self, start_date: str, end_date: str = None, output_file: str = None):
        """
        Baixa dados OHLCV históricos de um período específico.
        start_date e end_date devem ser strings no formato \'YYYY-MM-DD\'.
        """
        all_ohlcv = []
        since = self.exchange.parse8601(start_date + \'T00:00:00Z\')
        end_timestamp = self.exchange.parse8601(end_date + \'T23:59:59Z\') if end_date else self.exchange.milliseconds()

        logger.info(f"Iniciando download de dados históricos para {self.symbol} de {start_date} até {end_date if end_date else 'agora'}...")

        while since < end_timestamp:
            try:
                # O limite máximo de velas por requisição na Binance é 1000
                ohlcv_chunk = await self.exchange.fetch_ohlcv(self.symbol, self.timeframe, since, limit=1000)
                if not ohlcv_chunk:
                    break
                all_ohlcv.extend(ohlcv_chunk)
                since = ohlcv_chunk[-1][0] + 1 # Próxima requisição começa após a última vela
                logger.info(f"Coletados {len(ohlcv_chunk)} velas até {self.exchange.iso8601(ohlcv_chunk[-1][0])}")
                await asyncio.sleep(self.exchange.rateLimit / 1000) # Respeitar o rate limit
            except ccxt.NetworkError as e:
                logger.error(f"Erro de rede ao baixar dados históricos: {e}")
                await asyncio.sleep(5) # Esperar e tentar novamente
            except ccxt.ExchangeError as e:
                logger.error(f"Erro da Exchange ao baixar dados históricos: {e}")
                break
            except Exception as e:
                logger.error(f"Erro inesperado ao baixar dados históricos: {e}")
                break

        df = pd.DataFrame(all_ohlcv, columns=[\'timestamp\', \'open\', \'high\', \'low\', \'close\', \'volume\'])
        df[\'timestamp\'] = pd.to_datetime(df[\'timestamp\'], unit=\'ms\')
        df.set_index(\'timestamp\', inplace=True)

        if output_file:
            df.to_csv(output_file)
            logger.info(f"Dados históricos salvos em {output_file}")
        else:
            logger.info("Dados históricos baixados, mas não salvos em arquivo.")
        
        return df

# Exemplo de uso
async def main():
    loader = HistoricalDataLoader(symbol=\'BTC/USDT\', timeframe=\'1h\')
    # Baixar dados de 1 de janeiro de 2023 até 31 de dezembro de 2023
    df = await loader.download_ohlcv(\'2023-01-01\', \'2023-12-31\', \'historical_data/BTCUSDT_1h_2023.csv\')
    if df is not None and not df.empty:
        print(df.head())
        print(df.tail())

if __name__ == \'__main__\':
    import os
    os.makedirs(\'historical_data\', exist_ok=True)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Execução interrompida pelo usuário.")

