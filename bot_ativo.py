"""
BOT TRADER ATIVO - Versão Testnet
Executa trading automatizado com monitoramento em tempo real
"""
import os
import sys
import time
import asyncio
import ccxt
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Carregar variáveis de ambiente
load_dotenv()

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================
class Config:
    # Binance
    API_KEY = os.getenv("BINANCE_API_KEY")
    SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

    # Trading
    SYMBOL = "BTC/USDT"
    TIMEFRAME = "1m"
    CAPITAL_INICIAL = 1000.0  # USD

    # Parâmetros de Risco
    RISK_PER_TRADE = 0.01  # 1%
    STOP_LOSS_PERCENT = 0.002  # 0.2%
    TAKE_PROFIT_PERCENT = 0.005  # 0.5%

    # IA
    AI_CONFIDENCE_THRESHOLD = 0.70  # 70%

    # Execução
    INTERVALO_SEGUNDOS = 60  # Executar a cada 60 segundos
    EXECUTAR_ORDENS = False  # MUDE PARA True PARA EXECUTAR ORDENS REAIS

# ==============================================================================
# CLASSE PRINCIPAL DO BOT
# ==============================================================================
class BotTrader:
    def __init__(self):
        self.config = Config()
        self.capital = self.config.CAPITAL_INICIAL
        self.posicao_aberta = None
        self.trades_executados = []
        self.ciclo = 0

        # Configurar exchange
        self.exchange = ccxt.binance({
            'apiKey': self.config.API_KEY,
            'secret': self.config.SECRET_KEY,
            'enableRateLimit': True,
        })
        self.exchange.set_sandbox_mode(True)

        # Analisador de sentimento
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

        self.log("=" * 80)
        self.log("BOT TRADER INICIADO")
        self.log("=" * 80)
        self.log(f"Simbolo: {self.config.SYMBOL}")
        self.log(f"Timeframe: {self.config.TIMEFRAME}")
        self.log(f"Capital Inicial: ${self.config.CAPITAL_INICIAL:.2f}")
        self.log(f"Risco por Trade: {self.config.RISK_PER_TRADE:.1%}")
        self.log(f"Stop Loss: {self.config.STOP_LOSS_PERCENT:.1%}")
        self.log(f"Take Profit: {self.config.TAKE_PROFIT_PERCENT:.1%}")
        self.log(f"Confianca Minima IA: {self.config.AI_CONFIDENCE_THRESHOLD:.0%}")
        self.log(f"Executar Ordens: {'SIM' if self.config.EXECUTAR_ORDENS else 'NAO (MODO SIMULACAO)'}")
        self.log("=" * 80)
        self.log("")

    def log(self, mensagem):
        """Log com timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {mensagem}")

    def coletar_dados(self):
        """Coleta dados OHLCV da Binance"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(
                self.config.SYMBOL,
                self.config.TIMEFRAME,
                limit=50
            )
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            self.log(f"[ERRO] Falha ao coletar dados: {e}")
            return None

    def calcular_indicadores(self, df):
        """Calcula indicadores técnicos"""
        # RSI
        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # MACD
        exp1 = df["close"].ewm(span=12, adjust=False).mean()
        exp2 = df["close"].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']

        # Médias Móveis
        df['sma_20'] = df["close"].rolling(window=20).mean()
        df['volume_ma'] = df["volume"].rolling(window=20).mean()

        return df

    def analisar_sentimento(self):
        """Análise de sentimento simplificada"""
        # Por enquanto, retorna sentimento neutro
        # Em produção, coletaria notícias reais
        noticias_exemplo = [
            "Bitcoin shows steady growth in current market conditions",
            "Crypto market maintains stable position amid volatility",
        ]

        scores = [self.sentiment_analyzer.polarity_scores(n)['compound'] for n in noticias_exemplo]
        return sum(scores) / len(scores) if scores else 0.0

    def gerar_sinal(self, df, sentimento):
        """Gera sinal de trading baseado em IA"""
        ultimo = df.iloc[-1]

        rsi = ultimo['rsi']
        macd_hist = ultimo['macd_hist']
        volume = ultimo['volume']
        volume_ma = ultimo['volume_ma']

        sinal = "HOLD"
        confianca = 0.5

        # Lógica de compra
        if rsi < 30 and macd_hist > 0 and sentimento > 0.1:
            sinal = "BUY"
            confianca = 0.75
            if volume > (volume_ma * 1.5):
                confianca = min(1.0, confianca + 0.1)

        # Lógica de venda
        elif rsi > 70 and macd_hist < 0 and sentimento < -0.1:
            sinal = "SELL"
            confianca = 0.75
            if volume > (volume_ma * 1.5):
                confianca = min(1.0, confianca + 0.1)

        return {
            'sinal': sinal,
            'confianca': confianca,
            'rsi': rsi,
            'macd_hist': macd_hist,
            'sentimento': sentimento,
            'preco': ultimo['close']
        }

    def calcular_posicao(self, preco_entrada):
        """Calcula tamanho da posição e níveis de S/L e T/P"""
        stop_loss = preco_entrada * (1 - self.config.STOP_LOSS_PERCENT)
        take_profit = preco_entrada * (1 + self.config.TAKE_PROFIT_PERCENT)

        diferenca_preco = (preco_entrada - stop_loss) / preco_entrada
        valor_risco = self.capital * self.config.RISK_PER_TRADE
        valor_posicao = valor_risco / diferenca_preco
        quantidade = valor_posicao / preco_entrada

        return {
            'quantidade': quantidade,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'valor_posicao': valor_posicao,
            'risco': valor_risco
        }

    def executar_ordem_compra(self, analise):
        """Executa ordem de compra"""
        preco = analise['preco']
        posicao = self.calcular_posicao(preco)

        self.log("")
        self.log("=" * 80)
        self.log("[EXECUTANDO ORDEM DE COMPRA]")
        self.log(f"Preco de Entrada: ${preco:,.2f}")
        self.log(f"Quantidade: {posicao['quantidade']:.6f} BTC")
        self.log(f"Valor da Posicao: ${posicao['valor_posicao']:.2f}")
        self.log(f"Stop Loss: ${posicao['stop_loss']:,.2f}")
        self.log(f"Take Profit: ${posicao['take_profit']:,.2f}")
        self.log(f"Risco: ${posicao['risco']:.2f}")

        if self.config.EXECUTAR_ORDENS:
            try:
                # EXECUTAR ORDEM REAL NA BINANCE
                ordem = self.exchange.create_market_order(
                    self.config.SYMBOL,
                    'buy',
                    posicao['quantidade']
                )
                self.log(f"[OK] Ordem executada! ID: {ordem.get('id', 'N/A')}")
            except Exception as e:
                self.log(f"[ERRO] Falha ao executar ordem: {e}")
                return
        else:
            self.log("[SIMULACAO] Ordem NAO foi enviada para a Binance")

        # Registrar posição aberta
        self.posicao_aberta = {
            'tipo': 'LONG',
            'preco_entrada': preco,
            'quantidade': posicao['quantidade'],
            'stop_loss': posicao['stop_loss'],
            'take_profit': posicao['take_profit'],
            'timestamp': datetime.now()
        }

        self.log("=" * 80)
        self.log("")

    def verificar_posicao(self, preco_atual):
        """Verifica se deve fechar posição por S/L ou T/P"""
        if not self.posicao_aberta:
            return

        pos = self.posicao_aberta

        # Verificar Take Profit
        if preco_atual >= pos['take_profit']:
            self.fechar_posicao(preco_atual, "TAKE PROFIT")

        # Verificar Stop Loss
        elif preco_atual <= pos['stop_loss']:
            self.fechar_posicao(preco_atual, "STOP LOSS")

    def fechar_posicao(self, preco_saida, motivo):
        """Fecha posição aberta"""
        pos = self.posicao_aberta

        pnl = (preco_saida - pos['preco_entrada']) * pos['quantidade']
        pnl_percent = ((preco_saida - pos['preco_entrada']) / pos['preco_entrada']) * 100

        self.log("")
        self.log("=" * 80)
        self.log(f"[FECHANDO POSICAO - {motivo}]")
        self.log(f"Preco de Entrada: ${pos['preco_entrada']:,.2f}")
        self.log(f"Preco de Saida: ${preco_saida:,.2f}")
        self.log(f"Quantidade: {pos['quantidade']:.6f} BTC")
        self.log(f"P&L: ${pnl:+.2f} ({pnl_percent:+.2f}%)")

        if self.config.EXECUTAR_ORDENS:
            try:
                ordem = self.exchange.create_market_order(
                    self.config.SYMBOL,
                    'sell',
                    pos['quantidade']
                )
                self.log(f"[OK] Ordem de venda executada! ID: {ordem.get('id', 'N/A')}")
            except Exception as e:
                self.log(f"[ERRO] Falha ao executar ordem de venda: {e}")
        else:
            self.log("[SIMULACAO] Ordem de venda NAO foi enviada")

        # Atualizar capital
        self.capital += pnl
        self.log(f"Capital Atualizado: ${self.capital:.2f}")

        # Registrar trade
        self.trades_executados.append({
            'entrada': pos['preco_entrada'],
            'saida': preco_saida,
            'pnl': pnl,
            'motivo': motivo,
            'timestamp': datetime.now()
        })

        self.posicao_aberta = None
        self.log("=" * 80)
        self.log("")

    async def executar_ciclo(self):
        """Executa um ciclo completo de análise"""
        self.ciclo += 1

        self.log("")
        self.log(f"{'='*80}")
        self.log(f"CICLO #{self.ciclo}")
        self.log(f"{'='*80}")

        # 1. Coletar dados
        self.log("[1/5] Coletando dados da Binance...")
        df = self.coletar_dados()
        if df is None:
            return

        # 2. Calcular indicadores
        self.log("[2/5] Calculando indicadores tecnicos...")
        df = self.calcular_indicadores(df)

        preco_atual = df['close'].iloc[-1]
        self.log(f"      Preco Atual: ${preco_atual:,.2f}")
        self.log(f"      RSI: {df['rsi'].iloc[-1]:.2f}")
        self.log(f"      MACD Hist: {df['macd_hist'].iloc[-1]:.4f}")

        # 3. Verificar posição aberta
        if self.posicao_aberta:
            self.log("[3/5] Verificando posicao aberta...")
            self.verificar_posicao(preco_atual)
            if self.posicao_aberta:  # Se ainda está aberta
                self.log(f"      Posicao LONG aberta em ${self.posicao_aberta['preco_entrada']:,.2f}")
                self.log(f"      S/L: ${self.posicao_aberta['stop_loss']:,.2f} | T/P: ${self.posicao_aberta['take_profit']:,.2f}")
                self.log("[4/5] Pulando analise (posicao ja aberta)")
                self.log("[5/5] Ciclo concluido")
                return

        # 4. Analisar sentimento
        self.log("[3/5] Analisando sentimento...")
        sentimento = self.analisar_sentimento()
        self.log(f"      Sentimento: {sentimento:.3f}")

        # 5. Gerar sinal
        self.log("[4/5] Gerando sinal de trading (IA)...")
        analise = self.gerar_sinal(df, sentimento)

        self.log(f"      Sinal: {analise['sinal']}")
        self.log(f"      Confianca: {analise['confianca']:.0%}")
        self.log(f"      Limite: {self.config.AI_CONFIDENCE_THRESHOLD:.0%}")

        # 6. Executar ação
        self.log("[5/5] Avaliando acao...")

        if analise['sinal'] == "BUY" and analise['confianca'] >= self.config.AI_CONFIDENCE_THRESHOLD:
            if not self.posicao_aberta:
                self.executar_ordem_compra(analise)
            else:
                self.log("      Ja existe posicao aberta. Nenhuma acao tomada.")
        else:
            self.log(f"      Nenhuma acao tomada (Sinal: {analise['sinal']}, Confianca: {analise['confianca']:.0%})")

        self.log("")
        self.log(f"[RESUMO] Capital: ${self.capital:.2f} | Trades: {len(self.trades_executados)} | Posicao: {'ABERTA' if self.posicao_aberta else 'FECHADA'}")
        self.log(f"{'='*80}")

    async def executar(self):
        """Loop principal do bot"""
        self.log("[BOT] Iniciando loop de execucao...")
        self.log(f"[BOT] Intervalo: {self.config.INTERVALO_SEGUNDOS} segundos")
        self.log(f"[BOT] Pressione Ctrl+C para parar")
        self.log("")

        try:
            while True:
                await self.executar_ciclo()
                self.log(f"[AGUARDANDO] Proximo ciclo em {self.config.INTERVALO_SEGUNDOS} segundos...")
                self.log("")
                await asyncio.sleep(self.config.INTERVALO_SEGUNDOS)

        except KeyboardInterrupt:
            self.log("")
            self.log("=" * 80)
            self.log("[BOT] Interrompido pelo usuario")
            self.log("=" * 80)
            self.mostrar_resumo_final()

    def mostrar_resumo_final(self):
        """Mostra resumo final da execução"""
        self.log("")
        self.log("RESUMO FINAL:")
        self.log(f"  Capital Inicial: ${self.config.CAPITAL_INICIAL:.2f}")
        self.log(f"  Capital Final: ${self.capital:.2f}")
        self.log(f"  P&L Total: ${self.capital - self.config.CAPITAL_INICIAL:+.2f}")
        self.log(f"  Ciclos Executados: {self.ciclo}")
        self.log(f"  Trades Executados: {len(self.trades_executados)}")

        if self.trades_executados:
            lucros = [t['pnl'] for t in self.trades_executados if t['pnl'] > 0]
            perdas = [t['pnl'] for t in self.trades_executados if t['pnl'] < 0]
            self.log(f"  Trades Vencedores: {len(lucros)}")
            self.log(f"  Trades Perdedores: {len(perdas)}")
            if len(self.trades_executados) > 0:
                win_rate = len(lucros) / len(self.trades_executados) * 100
                self.log(f"  Win Rate: {win_rate:.1f}%")

        self.log("=" * 80)

# ==============================================================================
# EXECUÇÃO
# ==============================================================================
if __name__ == "__main__":
    bot = BotTrader()
    asyncio.run(bot.executar())
