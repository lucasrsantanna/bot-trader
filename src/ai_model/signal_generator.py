import pandas as pd
from utils.logger import logger
from config.trading_params import trading_params

class AISignalGenerator:
    def __init__(self, model=None):
        self.model = model  # Pode ser um modelo de ML treinado

    def generate_signal(self, market_data: pd.DataFrame, sentiment_data: dict):
        """
        Gera um sinal de trading (COMPRA, VENDA, MANTER) com base em dados de mercado e sentimento.
        Para a versão inicial, usaremos uma lógica simples. Posteriormente, pode ser substituído por um modelo de ML.
        """
        if market_data.empty:
            logger.warning("Dados de mercado vazios, não é possível gerar sinal.")
            return {"action": "HOLD", "confidence": 0.5}

        latest_data = market_data.iloc[-1]
        current_price = latest_data["close"]
        rsi = latest_data.get("rsi")
        macd_hist = latest_data.get("macd_hist")
        volume = latest_data.get("volume")
        volume_ma = latest_data.get(f"volume_ma_{trading_params.DEFAULT_TIMEFRAME}") # Ajustar nome da coluna

        # Agregação de sentimento
        avg_sentiment_score = sentiment_data.get("average_compound_score", 0)

        signal = "HOLD"
        confidence = 0.5

        # Lógica de sinalização inicial (exemplo simplificado)
        # Esta lógica será substituída ou aprimorada por um modelo de IA treinado
        if rsi is not None and macd_hist is not None:
            # Condição de compra: RSI baixo (sobrevendido) e MACD histograma positivo (momentum de alta)
            if rsi < 30 and macd_hist > 0 and avg_sentiment_score > 0.1:
                signal = "BUY"
                confidence = 0.75 # Exemplo de confiança
            # Condição de venda: RSI alto (sobrecomprado) e MACD histograma negativo (momentum de baixa)
            elif rsi > 70 and macd_hist < 0 and avg_sentiment_score < -0.1:
                signal = "SELL"
                confidence = 0.75 # Exemplo de confiança
            # Aumentar confiança se houver volume significativo acompanhando o sinal
            if volume is not None and volume_ma is not None and volume > (volume_ma * 1.5):
                confidence = min(1.0, confidence + 0.1)

        logger.info(f"Sinal gerado: {signal} com confiança {confidence:.2f}. Preço: {current_price:.2f}, RSI: {rsi:.2f}, MACD Hist: {macd_hist:.2f}, Sentimento: {avg_sentiment_score:.2f}")
        
        return {"action": signal, "confidence": confidence}

# Exemplo de uso (para testes)
if __name__ == '__main__':
    # Criar dados de mercado de exemplo
    data = {
        'close': [10, 11, 12, 13, 14, 15, 14, 13, 12, 11, 10, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
        'volume': [100, 110, 120, 130, 140, 150, 140, 130, 120, 110, 100, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270]
    }
    df_test = pd.DataFrame(data)
    
    # Adicionar indicadores técnicos (simulados para este exemplo)
    df_test['rsi'] = pd.Series([None]*29 + [35]) # Exemplo de RSI
    df_test['macd_hist'] = pd.Series([None]*29 + [0.1]) # Exemplo de MACD Hist
    df_test[f'volume_ma_{trading_params.DEFAULT_TIMEFRAME}'] = pd.Series([None]*29 + [150]) # Exemplo de Volume MA

    # Dados de sentimento de exemplo
    sentiment_example = {"average_compound_score": 0.2, "news_count": 5}

    generator = AISignalGenerator()
    signal = generator.generate_signal(df_test, sentiment_example)
    print(f"Sinal gerado: {signal}")

    sentiment_negative_example = {"average_compound_score": -0.2, "news_count": 5}
    df_test['rsi'] = pd.Series([None]*29 + [75])
    df_test['macd_hist'] = pd.Series([None]*29 + [-0.1])
    signal_neg = generator.generate_signal(df_test, sentiment_negative_example)
    print(f"Sinal gerado (negativo): {signal_neg}")

    sentiment_neutral_example = {"average_compound_score": 0.0, "news_count": 5}
    df_test['rsi'] = pd.Series([None]*29 + [50])
    df_test['macd_hist'] = pd.Series([None]*29 + [0.0])
    signal_neutral = generator.generate_signal(df_test, sentiment_neutral_example)
    print(f"Sinal gerado (neutro): {signal_neutral}")

