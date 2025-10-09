from utils.logger import logger
import pandas as pd

class PositionManager:
    def __init__(self):
        self.positions = {}
        logger.info("Gerenciador de Posições inicializado.")

    def open_position(self, symbol: str, position_type: str, entry_price: float, quantity: float, stop_loss: float = None, take_profit: float = None):
        """
        Abre uma nova posição.
        position_type: 'long' ou 'short'
        """
        if symbol in self.positions:
            logger.warning(f"Já existe uma posição aberta para {symbol}. Feche a posição existente antes de abrir uma nova.")
            return False

        self.positions[symbol] = {
            "symbol": symbol,
            "type": position_type,
            "entry_price": entry_price,
            "quantity": quantity,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "open_time": pd.Timestamp.now(),
            "status": "open"
        }
        logger.info(f"Posição {position_type} aberta para {symbol}: Preço de entrada={entry_price}, Quantidade={quantity}")
        return True

    def close_position(self, symbol: str, exit_price: float, close_reason: str = "manual"):
        """
        Fecha uma posição existente.
        """
        if symbol not in self.positions:
            logger.warning(f"Nenhuma posição aberta para {symbol} para fechar.")
            return None

        position = self.positions[symbol]
        position["exit_price"] = exit_price
        position["close_time"] = pd.Timestamp.now()
        position["status"] = "closed"
        position["close_reason"] = close_reason

        # Calcular P&L
        if position["type"] == "long":
            pnl = (exit_price - position["entry_price"]) * position["quantity"]
        else: # short
            pnl = (position["entry_price"] - exit_price) * position["quantity"]
        position["pnl"] = pnl

        logger.info(f"Posição para {symbol} fechada. P&L: {pnl:.2f}. Razão: {close_reason}")
        del self.positions[symbol] # Remover a posição fechada
        return position

    def get_position(self, symbol: str):
        """
        Retorna os detalhes de uma posição aberta.
        """
        return self.positions.get(symbol)

    def get_all_open_positions(self):
        """
        Retorna todas as posições abertas.
        """
        return self.positions

    def update_position_status(self, symbol: str, current_price: float):
        """
        Atualiza o status de uma posição aberta com base no preço atual e verifica SL/TP.
        """
        position = self.get_position(symbol)
        if not position:
            return None

        # Calcular P&L não realizado
        if position["type"] == "long":
            unrealized_pnl = (current_price - position["entry_price"]) * position["quantity"]
        else: # short
            unrealized_pnl = (position["entry_price"] - current_price) * position["quantity"]
        position["unrealized_pnl"] = unrealized_pnl

        # Verificar Stop Loss
        if position["stop_loss"] and (
            (position["type"] == "long" and current_price <= position["stop_loss"]) or
            (position["type"] == "short" and current_price >= position["stop_loss"])
        ):
            logger.warning(f"Stop Loss atingido para {symbol} em {current_price}. Fechando posição.")
            return self.close_position(symbol, current_price, "stop_loss")

        # Verificar Take Profit
        if position["take_profit"] and (
            (position["type"] == "long" and current_price >= position["take_profit"]) or
            (position["type"] == "short" and current_price <= position["take_profit"])
        ):
            logger.info(f"Take Profit atingido para {symbol} em {current_price}. Fechando posição.")
            return self.close_position(symbol, current_price, "take_profit")

        return position

# Exemplo de uso
if __name__ == '__main__':
    pm = PositionManager()

    # Abrir uma posição longa
    pm.open_position("BTC/USDT", "long", 20000.0, 0.01, stop_loss=19900.0, take_profit=20100.0)
    print("Posições abertas:", pm.get_all_open_positions())

    # Atualizar status da posição com preço atual
    current_price_update = 20050.0
    updated_position = pm.update_position_status("BTC/USDT", current_price_update)
    print(f"Posição atualizada em {current_price_update}: {updated_position}")

    # Simular atingir Stop Loss
    current_price_sl = 19890.0
    closed_position_sl = pm.update_position_status("BTC/USDT", current_price_sl)
    print(f"Posição fechada por SL em {current_price_sl}: {closed_position_sl}")
    print("Posições abertas após SL:", pm.get_all_open_positions())

    # Abrir nova posição e simular atingir Take Profit
    pm.open_position("ETH/USDT", "long", 1500.0, 0.1, stop_loss=1490.0, take_profit=1510.0)
    current_price_tp = 1515.0
    closed_position_tp = pm.update_position_status("ETH/USDT", current_price_tp)
    print(f"Posição fechada por TP em {current_price_tp}: {closed_position_tp}")
    print("Posições abertas após TP:", pm.get_all_open_positions())

