import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from utils.logger import logger
import asyncio

# Certifique-se de ter o 'vader_lexicon' baixado para o NLTK
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except nltk.downloader.DownloadError:
    nltk.download('vader_lexicon')

class NewsSentimentCollector:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.news_sources = {
            "coindesk": "https://www.coindesk.com/",
            # Adicionar outras fontes aqui, ou APIs de notícias
        }

    async def _scrape_coindesk(self):
        articles = []
        try:
            response = requests.get(self.news_sources["coindesk"])
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Exemplo de como encontrar artigos no CoinDesk (pode precisar de ajustes)
            # Isso é um exemplo e pode quebrar se a estrutura do site mudar
            headlines = soup.find_all('h4', class_='card-title') # Exemplo de tag e classe
            for headline in headlines:
                title = headline.get_text(strip=True)
                link = headline.find('a')['href'] if headline.find('a') else "#"
                articles.append({"title": title, "link": link})
            logger.info(f"Scraped {len(articles)} articles from CoinDesk.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao fazer web scraping do CoinDesk: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao processar CoinDesk: {e}")
        return articles

    async def get_latest_news(self):
        all_news = []
        # Exemplo de web scraping
        coindesk_news = await self._scrape_coindesk()
        all_news.extend(coindesk_news)

        # Placeholder para APIs de notícias
        # api_news = await self._fetch_from_news_api()
        # all_news.extend(api_news)

        return all_news

    def analyze_sentiment(self, text):
        if not text:
            return {"compound": 0, "neg": 0, "neu": 0, "pos": 0}
        sentiment = self.analyzer.polarity_scores(text)
        return sentiment

    async def get_news_with_sentiment(self):
        news_items = await self.get_latest_news()
        news_with_sentiment = []
        for item in news_items:
            sentiment_scores = self.analyze_sentiment(item.get("title", ""))
            item["sentiment"] = sentiment_scores
            news_with_sentiment.append(item)
        logger.info(f"Análise de sentimento concluída para {len(news_with_sentiment)} notícias.")
        return news_with_sentiment

# Exemplo de uso (para testes)
async def main():
    collector = NewsSentimentCollector()
    news = await collector.get_news_with_sentiment()
    if news:
        for item in news[:5]: # Mostrar as 5 primeiras notícias com sentimento
            print(f"Título: {item.get('title')}\nSentimento: {item.get('sentiment')}\n")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Execução interrompida pelo usuário.")

