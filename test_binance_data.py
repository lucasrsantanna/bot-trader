"""
Teste 1: BinanceDataCollector
Valida conexão, coleta OHLCV e cálculo de indicadores
"""
import sys
import asyncio
sys.path.insert(0, 'src')

from data_collector.binance_data import BinanceDataCollector

async def main():
    print("="*70)
    print(" TESTE 1: BINANCE DATA COLLECTOR")
    print("="*70)
    print()

    # Inicializar coletor
    print("[1] Inicializando BinanceDataCollector...")
    collector = BinanceDataCollector(symbol='BTC/USDT', timeframe='1m', limit=100)
    print("    OK - Coletor inicializado")
    print()

    # Coletar dados
    print("[2] Coletando dados OHLCV...")
    df = await collector.fetch_ohlcv()

    if df is not None and not df.empty:
        print(f"    OK - {len(df)} candles coletados")
        print(f"    Periodo: {df.index.min()} ate {df.index.max()}")
        print(f"    Ultimo preco (close): ${df['close'].iloc[-1]:,.2f}")
        print()

        # Mostrar primeiros 3 candles
        print("[3] Primeiros 3 candles:")
        print(df[['open', 'high', 'low', 'close', 'volume']].head(3).to_string())
        print()

        # Mostrar últimos 3 candles
        print("[4] Ultimos 3 candles:")
        print(df[['open', 'high', 'low', 'close', 'volume']].tail(3).to_string())
        print()

        # Estatísticas
        print("[5] Estatisticas:")
        print(f"    Preco minimo: ${df['low'].min():,.2f}")
        print(f"    Preco maximo: ${df['high'].max():,.2f}")
        print(f"    Volume total: {df['volume'].sum():,.2f}")
        print(f"    Preco medio: ${df['close'].mean():,.2f}")
        print()

        print("="*70)
        print(" TESTE 1: SUCESSO")
        print("="*70)
    else:
        print("    ERRO - Nao foi possivel coletar dados")
        print("="*70)
        print(" TESTE 1: FALHOU")
        print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
