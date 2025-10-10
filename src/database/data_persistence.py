"""
Sistema de Persistência de Dados - Recomendação Manus AI
Armazena OHLCV, indicadores, sinais da IA e trades completos para análise futura
"""
import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path

class DataPersistence:
    def __init__(self, db_path="bot_data.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Cria tabelas se não existirem"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabela OHLCV + Indicadores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                symbol TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                rsi REAL,
                macd REAL,
                macd_signal REAL,
                macd_hist REAL,
                volume_ma REAL,
                sma_10 REAL,
                ema_20 REAL
            )
        """)

        # Tabela de Sinais da IA
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                symbol TEXT,
                signal TEXT,
                confidence REAL,
                rsi REAL,
                macd_hist REAL,
                price REAL,
                volume REAL,
                executed BOOLEAN DEFAULT 0
            )
        """)

        # Tabela de Trades
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                open_time DATETIME,
                close_time DATETIME,
                symbol TEXT,
                type TEXT,
                entry_price REAL,
                exit_price REAL,
                quantity REAL,
                stop_loss REAL,
                take_profit REAL,
                pnl REAL,
                pnl_percent REAL,
                close_reason TEXT
            )
        """)

        # Índices para performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_market_timestamp ON market_data(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_signals_timestamp ON signals(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_trades_open_time ON trades(open_time)")

        conn.commit()
        conn.close()
        print(f"[DB] Banco de dados inicializado: {self.db_path}")

    def save_market_data(self, df, symbol):
        """Salva OHLCV + indicadores"""
        conn = sqlite3.connect(self.db_path)
        df_copy = df.copy()
        df_copy['symbol'] = symbol

        # Resetar index para incluir timestamp
        df_copy = df_copy.reset_index()

        df_copy.to_sql('market_data', conn, if_exists='append', index=False)
        conn.close()
        print(f"[DB] {len(df_copy)} registros de mercado salvos para {symbol}")

    def save_signal(self, signal_data):
        """Salva sinal gerado pela IA"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO signals (timestamp, symbol, signal, confidence, rsi, macd_hist, price, volume, executed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now(),
            signal_data.get('symbol', 'BTC/USDT'),
            signal_data['action'],
            signal_data['confidence'],
            signal_data.get('rsi'),
            signal_data.get('macd_hist'),
            signal_data.get('price'),
            signal_data.get('volume'),
            signal_data.get('executed', False)
        ))
        conn.commit()
        conn.close()
        print(f"[DB] Sinal salvo: {signal_data['action']} ({signal_data['confidence']:.0%})")

    def save_trade(self, trade_data):
        """Salva trade completo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO trades (
                open_time, close_time, symbol, type, entry_price, exit_price,
                quantity, stop_loss, take_profit, pnl, pnl_percent, close_reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trade_data['open_time'],
            trade_data['close_time'],
            trade_data['symbol'],
            trade_data['type'],
            trade_data['entry_price'],
            trade_data['exit_price'],
            trade_data['quantity'],
            trade_data['stop_loss'],
            trade_data['take_profit'],
            trade_data['pnl'],
            trade_data['pnl_percent'],
            trade_data['close_reason']
        ))
        conn.commit()
        conn.close()
        print(f"[DB] Trade salvo: {trade_data['type']} | P&L: ${trade_data['pnl']:.2f}")

    def get_performance_metrics(self):
        """Retorna métricas de desempenho"""
        conn = sqlite3.connect(self.db_path)
        trades_df = pd.read_sql("SELECT * FROM trades", conn)

        if len(trades_df) == 0:
            conn.close()
            return None

        winning_trades = trades_df[trades_df['pnl'] > 0]
        losing_trades = trades_df[trades_df['pnl'] < 0]

        metrics = {
            'total_trades': len(trades_df),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': len(winning_trades) / len(trades_df) * 100 if len(trades_df) > 0 else 0,
            'total_pnl': trades_df['pnl'].sum(),
            'average_win': winning_trades['pnl'].mean() if len(winning_trades) > 0 else 0,
            'average_loss': losing_trades['pnl'].mean() if len(losing_trades) > 0 else 0,
            'max_drawdown': trades_df['pnl'].cumsum().min(),
            'largest_win': trades_df['pnl'].max(),
            'largest_loss': trades_df['pnl'].min(),
            'profit_factor': abs(winning_trades['pnl'].sum() / losing_trades['pnl'].sum()) if len(losing_trades) > 0 and losing_trades['pnl'].sum() != 0 else 0
        }

        conn.close()
        return metrics

    def get_recent_trades(self, limit=10):
        """Retorna últimos N trades"""
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM trades ORDER BY close_time DESC LIMIT {limit}"
        trades_df = pd.read_sql(query, conn)
        conn.close()
        return trades_df

    def get_recent_signals(self, limit=20):
        """Retorna últimos N sinais"""
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM signals ORDER BY timestamp DESC LIMIT {limit}"
        signals_df = pd.read_sql(query, conn)
        conn.close()
        return signals_df

    def get_market_data(self, symbol='BTC/USDT', hours=24):
        """Retorna dados de mercado das últimas N horas"""
        conn = sqlite3.connect(self.db_path)
        query = f"""
            SELECT * FROM market_data
            WHERE symbol = '{symbol}'
            AND timestamp >= datetime('now', '-{hours} hours')
            ORDER BY timestamp ASC
        """
        market_df = pd.read_sql(query, conn)
        conn.close()
        return market_df

    def export_to_csv(self, table_name, output_path=None):
        """Exporta tabela para CSV"""
        if output_path is None:
            output_path = f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        df.to_csv(output_path, index=False)
        conn.close()
        print(f"[DB] Dados exportados para: {output_path}")
        return output_path

# Exemplo de uso
if __name__ == "__main__":
    db = DataPersistence("bot_data_test.db")

    # Testar salvamento de sinal
    signal_test = {
        'symbol': 'BTC/USDT',
        'action': 'BUY',
        'confidence': 0.75,
        'rsi': 35.6,
        'macd_hist': 0.1,
        'price': 120500.0,
        'volume': 1500000,
        'executed': True
    }
    db.save_signal(signal_test)

    # Testar salvamento de trade
    trade_test = {
        'open_time': datetime.now(),
        'close_time': datetime.now(),
        'symbol': 'BTC/USDT',
        'type': 'LONG',
        'entry_price': 120500.0,
        'exit_price': 121100.0,
        'quantity': 0.041,
        'stop_loss': 120300.0,
        'take_profit': 121100.0,
        'pnl': 24.60,
        'pnl_percent': 0.5,
        'close_reason': 'take_profit'
    }
    db.save_trade(trade_test)

    # Ver métricas
    metrics = db.get_performance_metrics()
    if metrics:
        print("\n=== MÉTRICAS ===")
        for key, value in metrics.items():
            print(f"{key}: {value}")
