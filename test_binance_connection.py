"""
Script de teste rápido para verificar conexão com Binance Testnet
"""
import os
import sys
import ccxt
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar exchange
api_key = os.getenv("BINANCE_API_KEY")
secret_key = os.getenv("BINANCE_SECRET_KEY")

if not api_key or not secret_key:
    print("[ERRO] API Keys nao encontradas no arquivo .env")
    sys.exit(1)

print("[OK] Credenciais carregadas com sucesso!")
print(f"API Key: {api_key[:10]}...")
print(f"Secret Key: {secret_key[:10]}...")
print()

# Criar conexão com Binance Testnet
try:
    exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': secret_key,
        'options': {
            'defaultType': 'spot',
        },
        'enableRateLimit': True,
    })

    # Usar testnet
    exchange.set_sandbox_mode(True)

    print("[TESTANDO] Conexao com Binance Testnet...")

    # Buscar preço atual do BTC/USDT
    ticker = exchange.fetch_ticker('BTC/USDT')
    current_price = ticker['last']

    print(f"[SUCESSO] CONEXAO BEM-SUCEDIDA!")
    print(f"[PRECO] Preco atual do BTC/USDT: ${current_price:,.2f}")
    print(f"[VOLUME] Volume 24h: ${ticker['quoteVolume']:,.2f}")
    print(f"[ALTA] Alta 24h: ${ticker['high']:,.2f}")
    print(f"[BAIXA] Baixa 24h: ${ticker['low']:,.2f}")
    print()

    # Testar saldo (se disponível na testnet)
    try:
        balance = exchange.fetch_balance()
        print("[SALDO] Saldo na conta Testnet:")
        for currency, amount in balance['total'].items():
            if amount > 0:
                print(f"   {currency}: {amount}")
    except Exception as e:
        print(f"[AVISO] Nao foi possivel obter saldo: {e}")

    print()
    print("[COMPLETO] Teste de conexao COMPLETO!")

except ccxt.AuthenticationError as e:
    print(f"[ERRO] ERRO DE AUTENTICACAO: {e}")
    print("Verifique se as API Keys estao corretas.")
except ccxt.NetworkError as e:
    print(f"[ERRO] ERRO DE REDE: {e}")
    print("Verifique sua conexao com a internet.")
except Exception as e:
    print(f"[ERRO] ERRO INESPERADO: {e}")
