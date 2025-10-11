"""
BOT AUTOMATICO - Executa trades e salva em arquivo JSON
Para uso com o dashboard
"""
import os
import json
import time
import ccxt
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

load_dotenv()

# Arquivo para persistir dados entre execuções
ARQUIVO_DADOS = "bot_dados.json"

class BotAutomatico:
    def __init__(self):
        # Carregar ou inicializar dados
        self.dados = self.carregar_dados()

        # Exchange
        # Configuração da Exchange
        use_testnet = os.getenv('USE_TESTNET', 'false').lower() == 'true'

        if use_testnet:
            self.exchange = ccxt.binance({
                'apiKey': os.getenv("BINANCE_API_KEY"),
                'secret': os.getenv("BINANCE_SECRET_KEY"),
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                },
            })
            self.exchange.set_sandbox_mode(True)
            print("[INFO] Usando Binance Testnet SPOT")
        else:
            self.exchange = ccxt.binance({
                'apiKey': os.getenv("BINANCE_API_KEY"),
                'secret': os.getenv("BINANCE_SECRET_KEY"),
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future',
                }
            })
            print("[INFO] Usando Binance Produção (Futures)")
        # set_sandbox_mode(True) é redundante ou pode causar conflito com a configuração manual da URL
        # Se você estiver usando a testnet de futuros, a URL precisa ser explícita.
        # Se for spot testnet, a URL é 'https://testnet.binance.vision/api/v3'
        # Certifique-se de que 'defaultType' e 'urls' estão corretos para o ambiente que você quer testar.


        # Analyzer
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

        print("="*70)
        print(" BOT AUTOMATICO INICIADO")
        print("="*70)
        print(f"Capital: ${self.dados['capital']:.2f}")
        print(f"Trades executados: {len(self.dados['trades'])}")
        print(f"Posicao: {'ABERTA' if self.dados['posicao'] else 'FECHADA'}")
        print(f"Modo: {'REAL' if self.dados['config']['executar_ordens'] else 'SIMULACAO'}")
        print("="*70)
        print()

    def carregar_dados(self):
        """Carrega dados salvos ou cria novos"""
        if os.path.exists(ARQUIVO_DADOS):
            with open(ARQUIVO_DADOS, 'r') as f:
                return json.load(f)

        # Dados padrão
        return {
            'capital': 1000.0,
            'capital_inicial': 1000.0,
            'trades': [],
            'posicao': None,
            'logs': [],
            'config': {
                'symbol': 'BTC/USDT',
                'timeframe': '1m',
                'risk_per_trade': 0.01,
                'stop_loss': 0.002,
                'take_profit': 0.005,
                'ai_confidence': 0.70,
                'executar_ordens': False,
                'intervalo': 60
            },
            'ultima_atualizacao': None
        }

    def salvar_dados(self):
        """Salva dados em arquivo"""
        self.dados['ultima_atualizacao'] = datetime.now().isoformat()
        with open(ARQUIVO_DADOS, 'w') as f:
            json.dump(self.dados, f, indent=2)

    def log(self, mensagem):
        """Adiciona log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {mensagem}"
        print(log_msg)
        self.dados['logs'].append(log_msg)
        if len(self.dados['logs']) > 100:
            self.dados['logs'] = self.dados['logs'][-100:]

    def coletar_dados(self):
        """Coleta dados OHLCV"""
        try:
            symbol = self.dados['config']['symbol']
            timeframe = self.dados['config']['timeframe']

            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=50)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            self.log(f"ERRO ao coletar dados: {e}")
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

        # Volume MA
        df['volume_ma'] = df["volume"].rolling(window=20).mean()

        return df

    def gerar_sinal(self, df):
        """Gera sinal de trading"""
        ultimo = df.iloc[-1]

        rsi = ultimo['rsi']
        macd_hist = ultimo['macd_hist']
        volume = ultimo['volume']
        volume_ma = ultimo['volume_ma']

        sentimento = 0.05  # Simplificado

        sinal = "HOLD"
        confianca = 0.5

        # Ajustado para RSI 40/60 (mais realista)
        # Condição de COMPRA - mais flexível
        if rsi < 40:
            if macd_hist > 0:
                sinal = "BUY"
                confianca = 0.80
            elif macd_hist > -5:  # MACD não muito negativo
                sinal = "BUY"
                confianca = 0.75
            else:
                sinal = "BUY"
                confianca = 0.70

            # Aumentar confiança com volume
            if volume > (volume_ma * 1.5):
                confianca = min(0.95, confianca + 0.10)

        # Condição de VENDA
        elif rsi > 60:
            if macd_hist < 0:
                sinal = "SELL"
                confianca = 0.80
            else:
                sinal = "SELL"
                confianca = 0.70

        return {
            'sinal': sinal,
            'confianca': confianca,
            'rsi': rsi,
            'macd_hist': macd_hist,
            'preco': ultimo['close']
        }

    def executar_compra(self, analise):
        """Executa ordem de compra"""
        config = self.dados['config']
        preco = analise['preco']

        # Calcular posição
        stop_loss_preco = preco * (1 - config['stop_loss'])
        take_profit_preco = preco * (1 + config['take_profit'])

        diferenca = (preco - stop_loss_preco) / preco
        valor_risco = self.dados['capital'] * config['risk_per_trade']
        valor_posicao = valor_risco / diferenca
        quantidade = valor_posicao / preco

        self.log("")
        self.log("="*70)
        self.log("[EXECUTANDO COMPRA]")
        self.log(f"Preco: ${preco:,.2f}")
        self.log(f"Quantidade: {quantidade:.6f} BTC")
        self.log(f"Valor: ${preco * quantidade:.2f}")
        self.log(f"Stop Loss: ${stop_loss_preco:,.2f}")
        self.log(f"Take Profit: ${take_profit_preco:,.2f}")

        if config['executar_ordens']:
            try:
                ordem = self.exchange.create_market_order(
                    config['symbol'],
                    'buy',
                    quantidade
                )
                self.log(f"[OK] Ordem executada! ID: {ordem.get('id', 'N/A')}")
            except Exception as e:
                self.log(f"[ERRO] Falha ao executar: {e}")
                return
        else:
            self.log("[SIMULACAO] Ordem NAO enviada para Binance")

        # Salvar posição
        self.dados['posicao'] = {
            'tipo': 'LONG',
            'preco_entrada': preco,
            'quantidade': quantidade,
            'stop_loss': stop_loss_preco,
            'take_profit': take_profit_preco,
            'timestamp': datetime.now().isoformat()
        }

        self.log("="*70)
        self.log("")
        self.salvar_dados()

    def verificar_posicao(self, preco_atual):
        """Verifica se deve fechar posição"""
        if not self.dados['posicao']:
            return

        pos = self.dados['posicao']

        # Take Profit
        if preco_atual >= pos['take_profit']:
            self.fechar_posicao(preco_atual, "TAKE PROFIT")
        # Stop Loss
        elif preco_atual <= pos['stop_loss']:
            self.fechar_posicao(preco_atual, "STOP LOSS")

    def fechar_posicao(self, preco_saida, motivo):
        """Fecha posição"""
        pos = self.dados['posicao']
        config = self.dados['config']

        pnl = (preco_saida - pos['preco_entrada']) * pos['quantidade']
        pnl_percent = ((preco_saida - pos['preco_entrada']) / pos['preco_entrada']) * 100

        self.log("")
        self.log("="*70)
        self.log(f"[FECHANDO POSICAO - {motivo}]")
        self.log(f"Entrada: ${pos['preco_entrada']:,.2f}")
        self.log(f"Saida: ${preco_saida:,.2f}")
        self.log(f"P&L: ${pnl:+.2f} ({pnl_percent:+.2f}%)")

        if config['executar_ordens']:
            try:
                ordem = self.exchange.create_market_order(
                    config['symbol'],
                    'sell',
                    pos['quantidade']
                )
                self.log(f"[OK] Venda executada! ID: {ordem.get('id', 'N/A')}")
            except Exception as e:
                self.log(f"[ERRO] Falha ao vender: {e}")
        else:
            self.log("[SIMULACAO] Venda NAO enviada")

        # Atualizar capital
        self.dados['capital'] += pnl
        self.log(f"Capital: ${self.dados['capital']:.2f}")

        # Registrar trade
        trade = {
            'timestamp': datetime.now().isoformat(),
            'entrada': pos['preco_entrada'],
            'saida': preco_saida,
            'quantidade': pos['quantidade'],
            'pnl': pnl,
            'pnl_percent': pnl_percent,
            'motivo': motivo
        }
        self.dados['trades'].append(trade)

        self.dados['posicao'] = None
        self.log("="*70)
        self.log("")
        self.salvar_dados()

    def executar_ciclo(self):
        """Executa um ciclo"""
        # Coletar dados
        df = self.coletar_dados()
        if df is None:
            return

        # Calcular indicadores
        df = self.calcular_indicadores(df)
        preco_atual = df['close'].iloc[-1]

        # Verificar posição aberta
        if self.dados['posicao']:
            self.verificar_posicao(preco_atual)
            if self.dados['posicao']:  # Ainda aberta
                pos = self.dados['posicao']
                pnl_atual = (preco_atual - pos['preco_entrada']) * pos['quantidade']
                self.log(f"[POSICAO ABERTA] P&L: ${pnl_atual:+.2f}")
                return

        # Gerar sinal
        analise = self.gerar_sinal(df)

        self.log(f"[ANALISE] Preco: ${preco_atual:,.2f} | RSI: {analise['rsi']:.1f} | Sinal: {analise['sinal']} ({analise['confianca']:.0%})")

        # Executar trade
        if analise['sinal'] == "BUY" and analise['confianca'] >= self.dados['config']['ai_confidence']:
            self.executar_compra(analise)

    def executar_loop(self):
        """Loop principal"""
        intervalo = self.dados['config']['intervalo']

        self.log(f"[INICIO] Loop automatico (intervalo: {intervalo}s)")
        self.log("Pressione Ctrl+C para parar")
        self.log("")

        try:
            while True:
                self.executar_ciclo()
                self.salvar_dados()
                time.sleep(intervalo)

        except KeyboardInterrupt:
            self.log("")
            self.log("[PARADO] Bot interrompido")
            self.salvar_dados()
            self.mostrar_resumo()

    def mostrar_resumo(self):
        """Mostra resumo"""
        print("")
        print("="*70)
        print(" RESUMO")
        print("="*70)
        print(f"Capital Inicial: ${self.dados['capital_inicial']:.2f}")
        print(f"Capital Final: ${self.dados['capital']:.2f}")
        print(f"P&L Total: ${self.dados['capital'] - self.dados['capital_inicial']:+.2f}")
        print(f"Trades: {len(self.dados['trades'])}")

        if self.dados['trades']:
            lucrativos = [t for t in self.dados['trades'] if t['pnl'] > 0]
            win_rate = (len(lucrativos) / len(self.dados['trades'])) * 100
            print(f"Win Rate: {win_rate:.1f}%")

        print("="*70)

if __name__ == "__main__":
    bot = BotAutomatico()
    bot.executar_loop()
