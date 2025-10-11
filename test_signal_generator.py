"""
Teste 2: SignalGenerator
Valida cálculo de indicadores (RSI, MACD) e geração de sinais
"""
import sys
import asyncio
sys.path.insert(0, 'src')

from data_collector.binance_data import BinanceDataCollector
from ai_model.signal_generator import SignalGenerator

async def main():
    print("="*70)
    print(" TESTE 2: SIGNAL GENERATOR")
    print("="*70)
    print()

    # Coletar dados
    print("[1] Coletando dados de mercado...")
    collector = BinanceDataCollector(symbol='BTC/USDT', timeframe='1m', limit=100)
    df = await collector.fetch_ohlcv()
    print(f"    OK - {len(df)} candles coletados")
    print(f"    Ultimo preco: ${df['close'].iloc[-1]:,.2f}")
    print()

    # Gerar sinais
    print("[2] Inicializando SignalGenerator...")
    generator = SignalGenerator()
    print("    OK - Generator inicializado")
    print()

    print("[3] Gerando sinal de trading...")
    signal = generator.generate_signal(df)

    if signal:
        print(f"    OK - Sinal gerado com sucesso")
        print()
        print("[4] Detalhes do Sinal:")
        print(f"    Sinal: {signal['signal']}")
        print(f"    Preco: ${signal['price']:,.2f}")
        print(f"    RSI: {signal['rsi']:.2f}")
        print(f"    MACD: {signal['macd']:.4f}")
        print(f"    Signal Line: {signal['signal_line']:.4f}")
        print(f"    Confianca: {signal['confidence']:.1f}%")
        print()

        # Interpretar sinal
        print("[5] Interpretacao:")
        if signal['signal'] == 'BUY':
            print(f"    -> COMPRA recomendada (RSI {signal['rsi']:.1f} indica sobrevenda)")
        elif signal['signal'] == 'SELL':
            print(f"    -> VENDA recomendada (RSI {signal['rsi']:.1f} indica sobrecompra)")
        else:
            print(f"    -> MANTER posicao (RSI {signal['rsi']:.1f} esta neutro)")
        print()

        # Analisar MACD
        macd_diff = signal['macd'] - signal['signal_line']
        print("[6] Analise MACD:")
        if macd_diff > 0:
            print(f"    -> MACD acima da Signal Line (+{macd_diff:.4f}) = Momentum de ALTA")
        else:
            print(f"    -> MACD abaixo da Signal Line ({macd_diff:.4f}) = Momentum de BAIXA")
        print()

        print("="*70)
        print(" TESTE 2: SUCESSO")
        print("="*70)
    else:
        print("    ERRO - Nao foi possivel gerar sinal")
        print("="*70)
        print(" TESTE 2: FALHOU")
        print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
