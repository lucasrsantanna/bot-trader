from config.trading_params import trading_params
from utils.logger import logger

class RiskManager:
    def __init__(self, initial_capital: float):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.risk_per_trade_percent = trading_params.RISK_PER_TRADE_PERCENT
        self.max_capital_risk_percent = trading_params.MAX_CAPITAL_RISK_PERCENT
        logger.info(f"Gerenciador de Risco inicializado com capital: {initial_capital}")

    def update_capital(self, new_capital: float):
        self.current_capital = new_capital
        logger.info(f"Capital atualizado para: {self.current_capital}")

    def calculate_position_size(self, entry_price: float, stop_loss_price: float) -> float:
        """
        Calcula o tamanho da posição com base no capital atual, risco por trade e stop-loss.
        Retorna a quantidade de criptomoeda a ser comprada/vendida.
        """
        if entry_price <= 0 or stop_loss_price <= 0:
            logger.error("Preço de entrada ou stop-loss deve ser positivo.")
            return 0.0

        if stop_loss_price >= entry_price: # Para compra, stop-loss deve ser menor que o preço de entrada
            logger.warning("Stop-loss deve ser menor que o preço de entrada para uma posição de compra.")
            return 0.0

        # Diferença percentual entre o preço de entrada e o stop-loss
        price_difference = (entry_price - stop_loss_price) / entry_price
        if price_difference <= 0:
            logger.error("Diferença de preço para stop-loss inválida.")
            return 0.0

        # Valor máximo em risco por trade
        risk_amount = self.current_capital * self.risk_per_trade_percent

        # Tamanho da posição em valor monetário (USD/USDT)
        position_value = risk_amount / price_difference

        # Quantidade de criptomoeda
        quantity = position_value / entry_price
        
        logger.info(f"Calculado tamanho da posição: {quantity:.6f} para risco de {risk_amount:.2f}")
        return quantity

    def check_max_risk_exposure(self, current_exposure: float) -> bool:
        """
        Verifica se a exposição atual excede o risco máximo permitido do capital total.
        """
        max_allowed_exposure = self.current_capital * self.max_capital_risk_percent
        if current_exposure > max_allowed_exposure:
            logger.warning(f"Exposição atual ({current_exposure:.2f}) excede o risco máximo permitido ({max_allowed_exposure:.2f}).")
            return False
        return True

# Exemplo de uso
if __name__ == '__main__':
    rm = RiskManager(initial_capital=10000.0)

    # Exemplo de cálculo de posição para compra
    entry = 20000.0
    stop_loss = 19900.0 # 0.5% de stop-loss
    position_size = rm.calculate_position_size(entry, stop_loss)
    print(f"Tamanho da posição para compra: {position_size:.6f} BTC")

    # Exemplo de verificação de risco máximo
    current_exposure = 300.0 # Exemplo de exposição em USD
    if rm.check_max_risk_exposure(current_exposure):
        print("Exposição dentro dos limites.")
    else:
        print("Exposição excede os limites!")

    rm.update_capital(10500.0)
    position_size_updated = rm.calculate_position_size(entry, stop_loss)
    print(f"Tamanho da posição com capital atualizado: {position_size_updated:.6f} BTC")

