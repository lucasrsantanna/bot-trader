class TradingParams:
    # Parâmetros de risco
    RISK_PER_TRADE_PERCENT = 0.01  # % do capital total a ser arriscado por trade
    MAX_CAPITAL_RISK_PERCENT = 0.05 # % máximo do capital total em risco a qualquer momento

    # Parâmetros de scalping
    TAKE_PROFIT_PERCENT = 0.005    # 0.5% de lucro alvo
    STOP_LOSS_PERCENT = 0.002      # 0.2% de perda máxima

    # Parâmetros da IA
    AI_CONFIDENCE_THRESHOLD = 0.70 # Confiança mínima da IA para executar um trade

    # Símbolo de trading padrão
    DEFAULT_SYMBOL = "BTC/USDT"
    DEFAULT_TIMEFRAME = "1m"

trading_params = TradingParams()

