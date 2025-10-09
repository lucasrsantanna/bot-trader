import asyncio
import pandas as pd
from datetime import datetime

from config.settings import settings
from config.trading_params import trading_params
from utils.logger import logger
from utils.notifications import notifier

from data_collector.binance_data import BinanceDataCollector
from data_collector.news_sentiment import NewsSentimentCollector
from indicators.technical_indicators import calculate_rsi, calculate_macd, calculate_moving_average, calculate_volume_ma
from ai_model.sentiment_analyzer import AISentimentAnalyzer
from ai_model.signal_generator import AISignalGenerator
from ai_model.model_trainer import AIModelTrainer # Para carregar o modelo treinado
from trading.risk_manager import RiskManager
from trading.position_manager import PositionManager
from trading.executor import OrderExecutor

class CryptoBot:
    def __init__(self, initial_capital: float = 10000.0):
        self.symbol = trading_params.DEFAULT_SYMBOL
        self.timeframe = trading_params.DEFAULT_TIMEFRAME
        self.initial_capital = initial_capital

        self.binance_collector = BinanceDataCollector(self.symbol, self.timeframe)
        self.news_sentiment_collector = NewsSentimentCollector()
        self.ai_sentiment_analyzer = AISentimentAnalyzer()
        self.ai_signal_generator = AISignalGenerator() # Pode carregar um modelo treinado aqui
        self.risk_manager = RiskManager(initial_capital)
        self.position_manager = PositionManager()
        self.order_executor = OrderExecutor()

        self.historical_data = pd.DataFrame() # Para armazenar dados OHLCV recentes
        self.current_price = None

        logger.info("CryptoBot inicializado.")
        notifier.send_message("CryptoBot inicializado com sucesso!")

    async def _update_market_data(self):
        logger.info("Atualizando dados de mercado...")
        new_ohlcv = await self.binance_collector.fetch_ohlcv()
        if new_ohlcv is not None and not new_ohlcv.empty:
            # Concatena os novos dados e remove duplicatas/mantém os mais recentes
            self.historical_data = pd.concat([self.historical_data, new_ohlcv]).drop_duplicates().sort_index()
            # Manter apenas um número razoável de velas para análise (ex: últimas 200)
            self.historical_data = self.historical_data.tail(200)
            
            # Calcular indicadores técnicos
            self.historical_data = calculate_rsi(self.historical_data)
            self.historical_data = calculate_macd(self.historical_data)
            self.historical_data = calculate_moving_average(self.historical_data, window=10, type='sma')
            self.historical_data = calculate_moving_average(self.historical_data, window=20, type='ema')
            self.historical_data = calculate_volume_ma(self.historical_data)

            self.current_price = self.historical_data['close'].iloc[-1]
            logger.info(f"Dados de mercado atualizados. Último preço: {self.current_price}")
        else:
            logger.warning("Falha ao obter novos dados OHLCV.")

    async def _update_sentiment_data(self):
        logger.info("Atualizando dados de sentimento...")
        sentiment_analysis_result = await self.ai_sentiment_analyzer.analyze_news_sentiment()
        if sentiment_analysis_result:
            return sentiment_analysis_result
        return {"average_compound_score": 0.0, "news_count": 0}

    async def _execute_trading_logic(self):
        if self.historical_data.empty or self.current_price is None:
            logger.warning("Dados de mercado insuficientes para executar lógica de trading.")
            return

        # 1. Gerar sinal da IA
        sentiment_data = await self._update_sentiment_data()
        signal = self.ai_signal_generator.generate_signal(self.historical_data, sentiment_data)

        action = signal["action"]
        confidence = signal["confidence"]

        logger.info(f"Sinal da IA: {action} com confiança {confidence:.2f}")

        # 2. Verificar confiança da IA e gerenciamento de risco
        if confidence < trading_params.AI_CONFIDENCE_THRESHOLD:
            logger.info(f"Confiança da IA ({confidence:.2f}) abaixo do limite ({trading_params.AI_CONFIDENCE_THRESHOLD:.2f}). Nenhuma ação será tomada.")
            return

        # 3. Gerenciar posições existentes
        open_position = self.position_manager.get_position(self.symbol)
        if open_position:
            closed_position = self.position_manager.update_position_status(self.symbol, self.current_price)
            if closed_position: # Posição foi fechada por SL/TP
                notifier.send_message(f"Posição para {self.symbol} fechada por {closed_position['close_reason']}. P&L: {closed_position['pnl']:.2f}")
                self.risk_manager.update_capital(self.risk_manager.current_capital + closed_position['pnl']) # Atualizar capital
                open_position = None # Resetar para permitir nova entrada

        # 4. Executar nova ordem se houver sinal e não houver posição aberta
        if action == "BUY" and open_position is None:
            # Calcular stop-loss e take-profit
            stop_loss_price = self.current_price * (1 - trading_params.STOP_LOSS_PERCENT)
            take_profit_price = self.current_price * (1 + trading_params.TAKE_PROFIT_PERCENT)

            # Calcular tamanho da posição
            quantity = self.risk_manager.calculate_position_size(self.current_price, stop_loss_price)
            if quantity > 0 and self.risk_manager.check_max_risk_exposure(self.current_price * quantity):
                order = await self.order_executor.create_market_order(self.symbol, 'buy', quantity)
                if order:
                    self.position_manager.open_position(self.symbol, 'long', self.current_price, quantity, stop_loss_price, take_profit_price)
                    notifier.send_message(f"COMPRA {quantity:.6f} de {self.symbol} @ {self.current_price:.2f}. SL: {stop_loss_price:.2f}, TP: {take_profit_price:.2f}")
            else:
                logger.warning("Não foi possível abrir posição de compra: tamanho inválido ou risco excedido.")

        elif action == "SELL" and open_position is None: # Para short selling, se permitido e implementado
            # Lógica similar para short selling
            logger.info("Sinal de VENDA, mas short selling não implementado ou sem posição aberta.")

        elif action == "HOLD":
            logger.info("Sinal de MANTER. Nenhuma ação de trading tomada.")

    async def run(self, interval_seconds=60):
        logger.info(f"Iniciando CryptoBot. Intervalo de execução: {interval_seconds} segundos.")
        while True:
            try:
                await self._update_market_data()
                await self._execute_trading_logic()
            except Exception as e:
                logger.error(f"Erro no loop principal do bot: {e}")
                notifier.send_message(f"Erro crítico no CryptoBot: {e}")
            await asyncio.sleep(interval_seconds)

if __name__ == '__main__':
    # Para executar, certifique-se de que as variáveis de ambiente estão configuradas
    # e que o modelo de IA (se usado) está treinado e salvo.
    # Exemplo de como treinar e carregar um modelo (se você tiver dados históricos)
    # trainer = AIModelTrainer()
    # # Supondo que você tenha um arquivo CSV com dados de treinamento
    # training_data_path = "ai_model/sample_training_data.csv" 
    # if os.path.exists(training_data_path):
    #     data_for_training = trainer.load_data(training_data_path)
    #     if not data_for_training.empty and trainer.train_model(data_for_training):
    #         trainer.save_model()
    # else:
    #     logger.warning(f"Arquivo de dados de treinamento não encontrado: {training_data_path}. O bot usará lógica simples.")

    # Carregar o modelo treinado para o signal_generator se existir
    # if trainer.load_model():
    #     CryptoBot.ai_signal_generator.model = trainer.model

    bot = CryptoBot(initial_capital=1000.0) # Defina seu capital inicial aqui
    try:
        asyncio.run(bot.run(interval_seconds=60)) # Executa a cada 60 segundos
    except KeyboardInterrupt:
        logger.info("CryptoBot interrompido pelo usuário.")
        notifier.send_message("CryptoBot interrompido.")

