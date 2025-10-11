import os
import ccxt
from dotenv import load_dotenv

load_dotenv()

use_testnet = os.getenv('USE_TESTNET', 'false').lower() == 'true'

print(f"USE_TESTNET: {use_testnet}")
print(f"API_KEY: {os.getenv('BINANCE_API_KEY')[:10]}...")
print()

if use_testnet:
    exchange = ccxt.binance({
        'apiKey': os.getenv("BINANCE_API_KEY"),
        'secret': os.getenv("BINANCE_SECRET_KEY"),
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot',
        },
    })
    exchange.set_sandbox_mode(True)
    print("[INFO] Usando Binance Testnet SPOT")
else:
    exchange = ccxt.binance({
        'apiKey': os.getenv("BINANCE_API_KEY"),
        'secret': os.getenv("BINANCE_SECRET_KEY"),
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
        }
    })
    print("[INFO] Usando Binance Produção (Futures)")

print(f"Exchange URLs: {exchange.urls}")
print()

try:
    print("Tentando fetch_ohlcv...")
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1m', limit=5)
    print(f"✅ SUCESSO! Recebidos {len(ohlcv)} candles")
    print(f"Último preço: {ohlcv[-1][4]}")
except Exception as e:
    print(f"❌ ERRO: {e}")
