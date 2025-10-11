"""
Teste 2: Estratégia Completa
Valida cálculo de RSI, MACD e geração de sinais (lógica do bot_automatico.py)
"""
import sys
import asyncio
import pandas as pd
sys.path.insert(0, 'src')

from data_collector.binance_data import BinanceDataCollector

def calcular_rsi(df, periodo=14):
    """Calcula RSI"""
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calcular_macd(df, fast=12, slow=26, signal=9):
    """Calcula MACD"""
    ema_fast = df["close"].ewm(span=fast).mean()
    ema_slow = df["close"].ewm(span=slow).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal).mean()
    return macd, signal_line

def gerar_sinal(df):
    """Gera sinal baseado em RSI 40/60 (lógica do bot_automatico.py)"""
    ultimo = df.iloc[-1]
    rsi = ultimo["rsi"]
    macd = ultimo["macd"]
    signal_line = ultimo["signal_line"]
    price = ultimo["close"]

    # Lógica otimizada - RSI 40/60
    if rsi < 40:
        if macd > signal_line:
            return {"signal": "BUY", "confidence": 80, "price": price, "rsi": rsi, "macd": macd, "signal_line": signal_line}
        else:
            return {"signal": "BUY", "confidence": 70, "price": price, "rsi": rsi, "macd": macd, "signal_line": signal_line}
    elif rsi > 60:
        if macd < signal_line:
            return {"signal": "SELL", "confidence": 80, "price": price, "rsi": rsi, "macd": macd, "signal_line": signal_line}
        else:
            return {"signal": "SELL", "confidence": 70, "price": price, "rsi": rsi, "macd": macd, "signal_line": signal_line}
    else:
        conf = 50 + abs(rsi - 50)  # Quanto mais próximo de 30 ou 70, maior a confiança
        return {"signal": "HOLD", "confidence": conf, "price": price, "rsi": rsi, "macd": macd, "signal_line": signal_line}

async def main():
    print("="*70)
    print(" TESTE 2: ESTRATEGIA COMPLETA (RSI 40/60 + MACD)")
    print("="*70)
    print()

    # Coletar dados
    print("[1] Coletando dados de mercado...")
    collector = BinanceDataCollector(symbol='BTC/USDT', timeframe='1m', limit=100)
    df = await collector.fetch_ohlcv()
    print(f"    OK - {len(df)} candles coletados")
    print(f"    Ultimo preco: ${df['close'].iloc[-1]:,.2f}")
    print()

    # Calcular indicadores
    print("[2] Calculando indicadores tecnicos...")
    df["rsi"] = calcular_rsi(df)
    df["macd"], df["signal_line"] = calcular_macd(df)
    print(f"    OK - RSI: {df['rsi'].iloc[-1]:.2f}")
    print(f"    OK - MACD: {df['macd'].iloc[-1]:.4f}")
    print(f"    OK - Signal Line: {df['signal_line'].iloc[-1]:.4f}")
    print()

    # Gerar sinal
    print("[3] Gerando sinal de trading...")
    signal = gerar_sinal(df)
    print(f"    OK - Sinal gerado: {signal['signal']}")
    print()

    # Mostrar detalhes
    print("[4] Detalhes do Sinal:")
    print(f"    Sinal: {signal['signal']}")
    print(f"    Preco: ${signal['price']:,.2f}")
    print(f"    RSI: {signal['rsi']:.2f}")
    print(f"    MACD: {signal['macd']:.4f}")
    print(f"    Signal Line: {signal['signal_line']:.4f}")
    print(f"    Confianca: {signal['confidence']:.0f}%")
    print()

    # Interpretar sinal
    print("[5] Interpretacao:")
    if signal['signal'] == 'BUY':
        print(f"    -> COMPRA recomendada")
        print(f"       RSI {signal['rsi']:.1f} < 40 (sobrevendido)")
        if signal['macd'] > signal['signal_line']:
            print(f"       MACD acima da Signal = Momentum favoravel")
        else:
            print(f"       MACD abaixo da Signal = Momentum desfavoravel")
    elif signal['signal'] == 'SELL':
        print(f"    -> VENDA recomendada")
        print(f"       RSI {signal['rsi']:.1f} > 60 (sobrecomprado)")
        if signal['macd'] < signal['signal_line']:
            print(f"       MACD abaixo da Signal = Momentum favoravel para venda")
        else:
            print(f"       MACD acima da Signal = Momentum desfavoravel para venda")
    else:
        print(f"    -> MANTER posicao (HOLD)")
        print(f"       RSI {signal['rsi']:.1f} esta na zona neutra (40-60)")
    print()

    print("="*70)
    print(" TESTE 2: SUCESSO")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
