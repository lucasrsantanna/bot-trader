"""
BOT PARA MADRUGADA - Range Trading Strategy
Estratégia otimizada para períodos de baixo volume
"""
import os
import ccxt
import pandas as pd
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configurações
SYMBOL = "BTC/USDT"
CAPITAL_INICIAL = 1000.0
EXECUTAR_ORDENS = False  # Modo simulação

# Parâmetros de Range Trading (madrugada)
RANGE_PERCENT = 0.003  # 0.3% de range
TAKE_PROFIT = 0.002    # 0.2% lucro (menor que diurno)
STOP_LOSS = 0.001      # 0.1% perda (mais apertado)
TEMPO_ESPERA = 30      # Segundos entre verificações

class BotMadrugada:
    def __init__(self):
        self.capital = CAPITAL_INICIAL
        self.posicao = None
        self.trades = []

        # Setup Binance
        self.exchange = ccxt.binance({
            'apiKey': os.getenv("BINANCE_API_KEY"),
            'secret': os.getenv("BINANCE_SECRET_KEY"),
            'enableRateLimit': True,
        })
        self.exchange.set_sandbox_mode(True)

        # Detectar range inicial
        self.range_superior = None
        self.range_inferior = None

        print("="*70)
        print(" BOT MADRUGADA - RANGE TRADING")
        print("="*70)
        print(f"Simbolo: {SYMBOL}")
        print(f"Capital: ${CAPITAL_INICIAL:.2f}")
        print(f"Range: {RANGE_PERCENT:.1%}")
        print(f"Take Profit: {TAKE_PROFIT:.1%}")
        print(f"Stop Loss: {STOP_LOSS:.1%}")
        print(f"Modo: {'REAL' if EXECUTAR_ORDENS else 'SIMULACAO'}")
        print("="*70)
        print()

    def log(self, msg):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    def coletar_dados(self):
        """Coleta dados recentes"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(SYMBOL, '1m', limit=30)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            return df
        except Exception as e:
            self.log(f"ERRO ao coletar dados: {e}")
            return None

    def detectar_range(self, df):
        """Detecta suporte e resistência dos últimos 30 minutos"""
        high = df['high'].max()
        low = df['low'].min()

        # Range = diferença entre máxima e mínima
        range_size = high - low
        preco_medio = (high + low) / 2

        # Se range muito pequeno, usar % fixa
        if range_size < (preco_medio * 0.002):  # < 0.2%
            self.range_superior = preco_medio * (1 + RANGE_PERCENT/2)
            self.range_inferior = preco_medio * (1 - RANGE_PERCENT/2)
        else:
            self.range_superior = high
            self.range_inferior = low

        self.log(f"Range detectado: ${self.range_inferior:,.2f} - ${self.range_superior:,.2f}")
        self.log(f"Range size: {((self.range_superior - self.range_inferior)/self.range_inferior)*100:.2f}%")

    def verificar_oportunidade(self, preco_atual):
        """Verifica se deve comprar ou vender baseado no range"""

        # Se já tem posição, verificar S/L e T/P
        if self.posicao:
            return self.verificar_posicao_aberta(preco_atual)

        # Sem posição - procurar entrada
        distancia_superior = (self.range_superior - preco_atual) / preco_atual
        distancia_inferior = (preco_atual - self.range_inferior) / preco_atual

        # Compra próximo ao SUPORTE (limite inferior)
        if distancia_inferior < 0.001:  # Dentro de 0.1% do suporte
            self.log(f"[OPORTUNIDADE] Preco proximo ao SUPORTE!")
            self.log(f"  Preco: ${preco_atual:,.2f}")
            self.log(f"  Suporte: ${self.range_inferior:,.2f}")
            self.log(f"  Alvo (resistencia): ${self.range_superior:,.2f}")
            return "BUY"

        # Aguardar se no meio do range
        return "HOLD"

    def verificar_posicao_aberta(self, preco_atual):
        """Verifica se deve fechar posição"""
        pos = self.posicao

        # Take Profit - chegou na resistência?
        if preco_atual >= pos['take_profit']:
            self.fechar_posicao(preco_atual, "TAKE PROFIT")
            return "CLOSE"

        # Stop Loss
        if preco_atual <= pos['stop_loss']:
            self.fechar_posicao(preco_atual, "STOP LOSS")
            return "CLOSE"

        # Ainda dentro do range
        pnl_atual = (preco_atual - pos['preco_entrada']) * pos['quantidade']
        pnl_percent = ((preco_atual - pos['preco_entrada']) / pos['preco_entrada']) * 100

        self.log(f"[POSICAO ABERTA] P&L: ${pnl_atual:+.2f} ({pnl_percent:+.2f}%)")

        return "HOLD"

    def executar_compra(self, preco):
        """Executa ordem de compra"""
        # Calcular posição
        valor_risco = self.capital * 0.01  # 1% do capital
        stop_loss_preco = preco * (1 - STOP_LOSS)
        take_profit_preco = self.range_superior  # Vender na resistência

        # Quantidade baseada no risco
        diferenca = preco - stop_loss_preco
        quantidade = (valor_risco / diferenca) / preco

        self.log("")
        self.log("="*70)
        self.log("[EXECUTANDO COMPRA - RANGE TRADING]")
        self.log(f"Preco de Entrada: ${preco:,.2f}")
        self.log(f"Quantidade: {quantidade:.6f} BTC")
        self.log(f"Valor: ${preco * quantidade:.2f}")
        self.log(f"Stop Loss: ${stop_loss_preco:,.2f} (-{STOP_LOSS:.2%})")
        self.log(f"Take Profit: ${take_profit_preco:,.2f} (na resistencia)")
        self.log(f"Risco: ${valor_risco:.2f}")

        lucro_potencial = (take_profit_preco - preco) * quantidade
        self.log(f"Lucro Potencial: ${lucro_potencial:.2f}")

        if not EXECUTAR_ORDENS:
            self.log("[SIMULACAO] Ordem NAO foi enviada")

        self.posicao = {
            'preco_entrada': preco,
            'quantidade': quantidade,
            'stop_loss': stop_loss_preco,
            'take_profit': take_profit_preco,
            'timestamp': datetime.now()
        }

        self.log("="*70)
        self.log("")

    def fechar_posicao(self, preco_saida, motivo):
        """Fecha posição"""
        pos = self.posicao

        pnl = (preco_saida - pos['preco_entrada']) * pos['quantidade']
        pnl_percent = ((preco_saida - pos['preco_entrada']) / pos['preco_entrada']) * 100

        self.log("")
        self.log("="*70)
        self.log(f"[FECHANDO POSICAO - {motivo}]")
        self.log(f"Entrada: ${pos['preco_entrada']:,.2f}")
        self.log(f"Saida: ${preco_saida:,.2f}")
        self.log(f"Quantidade: {pos['quantidade']:.6f} BTC")
        self.log(f"P&L: ${pnl:+.2f} ({pnl_percent:+.2f}%)")

        self.capital += pnl
        self.log(f"Capital Total: ${self.capital:.2f}")

        # Registrar trade
        trade = {
            'timestamp': datetime.now(),
            'entrada': pos['preco_entrada'],
            'saida': preco_saida,
            'quantidade': pos['quantidade'],
            'pnl': pnl,
            'pnl_percent': pnl_percent,
            'motivo': motivo
        }
        self.trades.append(trade)

        self.log(f"Total de Trades: {len(self.trades)}")
        self.log("="*70)
        self.log("")

        self.posicao = None

    def executar_ciclo(self):
        """Executa um ciclo de verificação"""
        # Coletar dados
        df = self.coletar_dados()
        if df is None:
            return

        preco_atual = df['close'].iloc[-1]

        # Detectar/atualizar range a cada ciclo
        self.detectar_range(df)

        # Verificar oportunidade
        acao = self.verificar_oportunidade(preco_atual)

        if acao == "BUY":
            self.executar_compra(preco_atual)
        elif acao == "HOLD":
            if not self.posicao:
                self.log(f"[AGUARDANDO] Preco: ${preco_atual:,.2f} | Range: ${self.range_inferior:,.2f} - ${self.range_superior:,.2f}")

    def executar(self, ciclos=10):
        """Loop principal"""
        self.log(f"[INICIO] Executando {ciclos} ciclos (intervalo: {TEMPO_ESPERA}s)")
        self.log("")

        for i in range(ciclos):
            self.log(f"--- CICLO {i+1}/{ciclos} ---")
            self.executar_ciclo()

            if i < ciclos - 1:
                time.sleep(TEMPO_ESPERA)

            self.log("")

        # Resumo final
        self.log("="*70)
        self.log(" RESUMO FINAL")
        self.log("="*70)
        self.log(f"Capital Inicial: ${CAPITAL_INICIAL:.2f}")
        self.log(f"Capital Final: ${self.capital:.2f}")
        self.log(f"P&L Total: ${self.capital - CAPITAL_INICIAL:+.2f}")
        self.log(f"Trades Executados: {len(self.trades)}")

        if self.trades:
            lucrativos = [t for t in self.trades if t['pnl'] > 0]
            prejuizo = [t for t in self.trades if t['pnl'] < 0]

            self.log(f"Trades Lucrativos: {len(lucrativos)}")
            self.log(f"Trades com Prejuizo: {len(prejuizo)}")

            if len(self.trades) > 0:
                win_rate = (len(lucrativos) / len(self.trades)) * 100
                self.log(f"Win Rate: {win_rate:.1f}%")

            self.log("")
            self.log("Detalhes dos Trades:")
            for i, t in enumerate(self.trades, 1):
                self.log(f"  {i}. {t['timestamp'].strftime('%H:%M:%S')} | "
                        f"${t['entrada']:,.2f} -> ${t['saida']:,.2f} | "
                        f"P&L: ${t['pnl']:+.2f} ({t['pnl_percent']:+.2f}%) | "
                        f"{t['motivo']}")

        self.log("="*70)

if __name__ == "__main__":
    bot = BotMadrugada()

    print("\nEste bot vai executar 10 ciclos de 30 segundos cada (~5 minutos total)")
    print("Estrategia: Range Trading (otimizada para madrugada/baixo volume)")
    print("\nPressione Ctrl+C para parar antecipadamente\n")

    try:
        bot.executar(ciclos=10)
    except KeyboardInterrupt:
        print("\n\n[INTERROMPIDO] Bot parado pelo usuario")
        if bot.posicao:
            print("ATENCAO: Voce tem uma posicao aberta!")
