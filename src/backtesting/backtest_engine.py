import pandas as pd
from utils.logger import logger
from ai_model.signal_generator import AISignalGenerator
from trading.risk_manager import RiskManager
from config.trading_params import trading_params

class BacktestEngine:
    def __init__(self, initial_capital: float = 10000.0):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = {}
        self.trades = []
        self.risk_manager = RiskManager(initial_capital)
        self.signal_generator = AISignalGenerator() # Usará a lógica simples por enquanto
        logger.info(f"BacktestEngine inicializado com capital: {initial_capital}")

    def _execute_trade(self, timestamp, symbol, action, price, quantity):
        trade = {
            "timestamp": timestamp,
            "symbol": symbol,
            "action": action,
            "price": price,
            "quantity": quantity,
            "pnl": 0.0,
            "capital_before": self.capital
        }

        if action == "BUY":
            cost = price * quantity
            if self.capital >= cost:
                self.capital -= cost
                self.positions[symbol] = {"entry_price": price, "quantity": quantity, "type": "long"}
                trade["status"] = "EXECUTED"
                logger.info(f"[{timestamp}] COMPRA {quantity:.6f} de {symbol} @ {price:.2f}. Capital restante: {self.capital:.2f}")
            else:
                trade["status"] = "REJECTED_INSUFFICIENT_FUNDS"
                logger.warning(f"[{timestamp}] COMPRA {symbol} REJEITADA: Fundos insuficientes. Capital: {self.capital:.2f}")
        elif action == "SELL":
            if symbol in self.positions and self.positions[symbol]["type"] == "long" and self.positions[symbol]["quantity"] >= quantity:
                revenue = price * quantity
                self.capital += revenue
                entry_price = self.positions[symbol]["entry_price"]
                pnl = (price - entry_price) * quantity
                trade["pnl"] = pnl
                self.positions.pop(symbol) # Fechar posição
                trade["status"] = "EXECUTED"
                logger.info(f"[{timestamp}] VENDA {quantity:.6f} de {symbol} @ {price:.2f}. P&L: {pnl:.2f}. Capital total: {self.capital:.2f}")
            else:
                trade["status"] = "REJECTED_NO_POSITION"
                logger.warning(f"[{timestamp}] VENDA {symbol} REJEITADA: Nenhuma posição ou quantidade insuficiente.")
        
        trade["capital_after"] = self.capital
        self.trades.append(trade)

    def run_backtest(self, historical_data: pd.DataFrame, sentiment_data: pd.DataFrame, symbol: str):
        logger.info(f"Iniciando backtest para {symbol}...")
        self.capital = self.initial_capital
        self.positions = {}
        self.trades = []

        # Combinar dados históricos e de sentimento (simplificado para este exemplo)
        # Em um cenário real, você precisaria de um merge mais sofisticado baseado em timestamp
        combined_data = historical_data.copy()
        # Adicionar colunas de sentimento ao combined_data se houver correspondência de tempo
        # Por simplicidade, vamos simular que o sentiment_data já está no historical_data
        # ou que a IA pode acessá-lo de alguma forma para cada timestamp.

        for i in range(len(combined_data)):
            timestamp = combined_data.index[i]
            current_candle = combined_data.iloc[i]
            current_price = current_candle["close"]

            # Simular dados de sentimento para cada ponto de tempo (substituir por dados reais)
            simulated_sentiment = {"average_compound_score": 0.05} # Exemplo

            # Gerar sinal da IA
            signal = self.signal_generator.generate_signal(combined_data.iloc[:i+1], simulated_sentiment)

            if signal["action"] == "BUY" and symbol not in self.positions:
                # Calcular tamanho da posição e SL/TP (simplificado)
                stop_loss_price = current_price * (1 - trading_params.STOP_LOSS_PERCENT)
                quantity = self.risk_manager.calculate_position_size(current_price, stop_loss_price)
                if quantity > 0:
                    self._execute_trade(timestamp, symbol, "BUY", current_price, quantity)

            elif signal["action"] == "SELL" and symbol in self.positions and self.positions[symbol]["type"] == "long":
                # Fechar posição existente
                quantity_to_sell = self.positions[symbol]["quantity"]
                self._execute_trade(timestamp, symbol, "SELL", current_price, quantity_to_sell)
            
            # Atualizar capital no risk manager
            self.risk_manager.update_capital(self.capital)

        logger.info(f"Backtest concluído. Capital final: {self.capital:.2f}")
        return pd.DataFrame(self.trades)

    def generate_report(self, trades_df: pd.DataFrame):
        if trades_df.empty:
            logger.warning("Nenhum trade para gerar relatório.")
            return "Nenhum trade executado durante o backtest."

        total_pnl = trades_df["pnl"].sum()
        num_trades = len(trades_df)
        winning_trades = trades_df[trades_df["pnl"] > 0]
        losing_trades = trades_df[trades_df["pnl"] < 0]
        win_rate = len(winning_trades) / num_trades if num_trades > 0 else 0

        report = f"\n--- Relatório de Backtest ---\n"
        report += f"Capital Inicial: {self.initial_capital:.2f}\n"
        report += f"Capital Final: {self.capital:.2f}\n"
        report += f"Lucro/Prejuízo Total: {total_pnl:.2f}\n"
        report += f"Número Total de Trades: {num_trades}\n"
        report += f"Trades Vencedores: {len(winning_trades)}\n"
        report += f"Trades Perdedores: {len(losing_trades)}\n"
        report += f"Taxa de Acerto: {win_rate:.2%}\n"
        report += f"---------------------------\n"
        logger.info("Relatório de backtest gerado.")
        return report

# Exemplo de uso (para testes)
if __name__ == '__main__':
    # Criar dados históricos de exemplo (substituir por dados reais)
    data = {
        'timestamp': pd.to_datetime(pd.date_range(start='2023-01-01', periods=100, freq='1min')),
        'open': [i + 100 for i in range(100)],
        'high': [i + 102 for i in range(100)],
        'low': [i + 98 for i in range(100)],
        'close': [i + 101 for i in range(100)],
        'volume': [1000 + i * 10 for i in range(100)],
    }
    historical_df = pd.DataFrame(data).set_index('timestamp')

    # Adicionar indicadores técnicos (simulados para este exemplo)
    historical_df['rsi'] = pd.Series([None]*99 + [35]) # Exemplo de RSI
    historical_df['macd_hist'] = pd.Series([None]*99 + [0.1]) # Exemplo de MACD Hist
    historical_df[f'volume_ma_{trading_params.DEFAULT_TIMEFRAME}'] = pd.Series([None]*99 + [150]) # Exemplo de Volume MA

    # Dados de sentimento de exemplo (simulados)
    sentiment_df = pd.DataFrame({
        'timestamp': pd.to_datetime(pd.date_range(start='2023-01-01', periods=100, freq='1min')),
        'average_compound_score': [0.1 if i % 10 < 5 else -0.1 for i in range(100)]
    }).set_index('timestamp')

    engine = BacktestEngine(initial_capital=10000.0)
    trades = engine.run_backtest(historical_df, sentiment_df, trading_params.DEFAULT_SYMBOL)
    print(engine.generate_report(trades))

