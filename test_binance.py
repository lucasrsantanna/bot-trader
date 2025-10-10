import ccxt
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
secret_key = os.getenv('BINANCE_SECRET_KEY')

print(f"API Key: {api_key[:20]}...")
print(f"Secret Key: {secret_key[:20]}...")
print()

# Testar com diferentes configurações
configs = [
    {
        'name': 'Testnet SPOT (binance.vision)',
        'config': {
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'},
            'urls': {
                'api': {
                    'public': 'https://testnet.binance.vision/api/v3',
                    'private': 'https://testnet.binance.vision/api/v3',
                }
            }
        }
    },
    {
        'name': 'Testnet FUTURES',
        'config': {
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
            'sandbox': True,
        }
    },
]

for test in configs:
    print(f"Testando: {test['name']}")
    try:
        exchange = ccxt.binance(test['config'])

        # Testar fetch ticker (público)
        ticker = exchange.fetch_ticker('BTC/USDT')
        print(f"  ✅ Ticker público: ${ticker['last']}")

        # Testar account info (privado - requer API key)
        balance = exchange.fetch_balance()
        print(f"  ✅ Balance privado: OK")
        print(f"  ✅ FUNCIONOU!\n")
        break

    except Exception as e:
        print(f"  ❌ Erro: {e}\n")
