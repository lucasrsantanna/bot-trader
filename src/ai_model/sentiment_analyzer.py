from data_collector.news_sentiment import NewsSentimentCollector
from utils.logger import logger

class AISentimentAnalyzer:
    def __init__(self):
        self.news_collector = NewsSentimentCollector()

    async def analyze_news_sentiment(self):
        logger.info("Iniciando análise de sentimento das notícias.")
        news_with_sentiment = await self.news_collector.get_news_with_sentiment()
        
        if not news_with_sentiment:
            logger.warning("Nenhuma notícia encontrada para análise de sentimento.")
            return None

        # Exemplo simples de agregação de sentimento: média do score composto
        total_compound_score = sum(item["sentiment"]["compound"] for item in news_with_sentiment)
        average_compound_score = total_compound_score / len(news_with_sentiment)

        logger.info(f"Média do score de sentimento composto das notícias: {average_compound_score:.4f}")
        return {
            "average_compound_score": average_compound_score,
            "news_count": len(news_with_sentiment),
            "detailed_news": news_with_sentiment # Opcional: incluir notícias detalhadas
        }

# Exemplo de uso (para testes)
async def main():
    analyzer = AISentimentAnalyzer()
    sentiment_data = await analyzer.analyze_news_sentiment()
    if sentiment_data:
        print(f"Dados de Sentimento Agregado: {sentiment_data}")

if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Execução interrompida pelo usuário.")

