"""
BOT TRADER DEMO - 3 Ciclos de Demonstração
"""
import os
import sys
import time
import ccxt
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

load_dotenv()

print("="*80)
print(" BOT TRADER - DEMONSTRACAO (3 CICLOS)")
print("="*80)
print()

# Config
SYMBOL = "BTC/USDT"
CAPITAL = 1000.0
EXECUTAR_ORDENS = False

# Setup
exchange = ccxt.binance({
    'apiKey': os.getenv("BINANCE_API_KEY"),
    'secret': os.getenv("BINANCE_SECRET_KEY"),
    'enableRateLimit': True,
})
exchange.set_sandbox_mode(True)

sentiment_analyzer = SentimentIntensityAnalyzer()
posicao_aberta = None
capital = CAPITAL

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

for ciclo in range(1, 4):
    print()
    print("="*80)
    log(f"CICLO #{ciclo}/3")
    print("="*80)

    # 1. Coletar dados
    log("[1/5] Coletando dados da Binance...")
    ohlcv = exchange.fetch_ohlcv(SYMBOL, '1m', limit=50)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

    # 2. Calcular indicadores
    log("[2/5] Calculando indicadores...")
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['rsi'] = 100 - (100 / (1 + gain / loss))

    exp1 = df["close"].ewm(span=12, adjust=False).mean()
    exp2 = df["close"].ewm(span=26, adjust=False).mean()
    df['macd'] = exp1 - exp2
    df['macd_hist'] = df['macd'] - df['macd'].ewm(span=9, adjust=False).mean()
    df['volume_ma'] = df["volume"].rolling(window=20).mean()

    preco = df['close'].iloc[-1]
    rsi = df['rsi'].iloc[-1]
    macd_hist = df['macd_hist'].iloc[-1]
    volume = df['volume'].iloc[-1]
    volume_ma = df['volume_ma'].iloc[-1]

    log(f"    Preco: ${preco:,.2f}")
    log(f"    RSI: {rsi:.2f}")
    log(f"    MACD Hist: {macd_hist:.4f}")

    # 3. Verificar posição
    log("[3/5] Verificando posicao...")
    if posicao_aberta:
        log(f"    Posicao ABERTA em ${posicao_aberta['preco']:,.2f}")
        log(f"    S/L: ${posicao_aberta['sl']:,.2f} | T/P: ${posicao_aberta['tp']:,.2f}")

        # Verificar S/L e T/P
        if preco >= posicao_aberta['tp']:
            pnl = (preco - posicao_aberta['preco']) * posicao_aberta['qtd']
            capital += pnl
            log(f"    [TAKE PROFIT ATINGIDO!]")
            log(f"    P&L: ${pnl:+.2f}")
            log(f"    Capital: ${capital:.2f}")
            posicao_aberta = None
        elif preco <= posicao_aberta['sl']:
            pnl = (preco - posicao_aberta['preco']) * posicao_aberta['qtd']
            capital += pnl
            log(f"    [STOP LOSS ATINGIDO!]")
            log(f"    P&L: ${pnl:+.2f}")
            log(f"    Capital: ${capital:.2f}")
            posicao_aberta = None
        else:
            log(f"    Posicao mantida")
    else:
        log(f"    Nenhuma posicao aberta")

    # 4. Sentimento
    log("[4/5] Analisando sentimento...")
    sentimento = 0.05  # Simulado
    log(f"    Sentimento: {sentimento:.3f}")

    # 5. Gerar sinal
    log("[5/5] Gerando sinal...")

    sinal = "HOLD"
    confianca = 0.5

    if rsi < 30 and macd_hist > 0 and sentimento > 0.1:
        sinal = "BUY"
        confianca = 0.75
        if volume > (volume_ma * 1.5):
            confianca = 0.85
    elif rsi > 70 and macd_hist < 0:
        sinal = "SELL"
        confianca = 0.75

    log(f"    Sinal: {sinal}")
    log(f"    Confianca: {confianca:.0%}")

    # Ação
    if sinal == "BUY" and confianca >= 0.70 and not posicao_aberta:
        log("")
        log(">>> EXECUTANDO COMPRA <<<")

        sl = preco * 0.998  # -0.2%
        tp = preco * 1.005  # +0.5%
        risco = capital * 0.01
        qtd = (risco / (preco - sl)) / preco

        log(f"    Preco: ${preco:,.2f}")
        log(f"    Quantidade: {qtd:.6f} BTC")
        log(f"    Stop Loss: ${sl:,.2f}")
        log(f"    Take Profit: ${tp:,.2f}")

        if not EXECUTAR_ORDENS:
            log(f"    [SIMULACAO] Ordem NAO enviada")

        posicao_aberta = {
            'preco': preco,
            'qtd': qtd,
            'sl': sl,
            'tp': tp
        }
    else:
        log(f"    Nenhuma acao tomada")

    print()
    log(f"[RESUMO] Capital: ${capital:.2f} | Posicao: {'ABERTA' if posicao_aberta else 'FECHADA'}")

    if ciclo < 3:
        log("Aguardando proximo ciclo (10s)...")
        time.sleep(10)

print()
print("="*80)
log("DEMONSTRACAO CONCLUIDA")
print("="*80)
print()
print(f"Capital Inicial: ${CAPITAL:.2f}")
print(f"Capital Final: ${capital:.2f}")
print(f"P&L: ${capital - CAPITAL:+.2f}")
print()
