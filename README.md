# 🤖 Bot Trader com IA - Scalping em Criptomoedas

Bot de day trading automatizado com análise de sentimento de notícias e indicadores técnicos para o mercado de criptomoedas.

## 📋 Características

- **Estratégia:** Scalping com análise técnica e sentimento de mercado
- **Exchange:** Binance (Spot/Futures)
- **Timeframe:** 1 minuto (configurável)
- **IA/ML:** Geração de sinais baseada em:
  - Indicadores técnicos (RSI, MACD, Volume)
  - Análise de sentimento de notícias (VADER + web scraping)
- **Gerenciamento de Risco:** Stop-loss automático e cálculo de posição
- **Backtesting:** Engine para testar estratégias em dados históricos
- **Notificações:** Telegram (opcional)

---

## 🏗️ Estrutura do Projeto

```
Bot Trader/
├── config/                    # Configurações
│   ├── settings.py           # Configurações gerais e .env
│   └── trading_params.py     # Parâmetros de trading
├── src/
│   ├── data_collector/       # Coleta de dados
│   │   ├── binance_data.py   # Dados OHLCV da Binance
│   │   └── news_sentiment.py # Notícias e sentimento
│   ├── ai_model/             # Módulo de IA
│   │   ├── sentiment_analyzer.py  # Análise de sentimento
│   │   ├── signal_generator.py    # Geração de sinais
│   │   └── model_trainer.py       # Treinamento de modelo
│   ├── trading/              # Execução de trades
│   │   ├── executor.py       # Execução de ordens
│   │   ├── risk_manager.py   # Gerenciamento de risco
│   │   └── position_manager.py    # Gestão de posições
│   ├── backtesting/          # Backtesting
│   │   ├── backtest_engine.py     # Engine de backtest
│   │   └── download_historical_data.py  # Download de dados
│   ├── indicators/           # Indicadores técnicos
│   │   └── technical_indicators.py
│   ├── utils/                # Utilitários
│   │   ├── logger.py         # Sistema de logs
│   │   └── notifications.py  # Notificações
│   └── main.py               # Ponto de entrada principal
├── tests/                    # Testes unitários
├── data/                     # Dados e modelos
│   ├── historical/           # Dados históricos
│   └── models/               # Modelos treinados
├── notebooks/                # Jupyter notebooks (análise exploratória)
├── .env.example              # Template de variáveis de ambiente
├── .gitignore                # Arquivos ignorados pelo Git
├── requirements.txt          # Dependências Python
└── README.md                 # Este arquivo
```

---

## 🚀 Instalação

### 1. Pré-requisitos

- Python 3.9 ou superior
- Conta na Binance (ou Binance Testnet)
- Bot do Telegram (opcional, para notificações)

### 2. Clone o Repositório

```bash
git clone <seu-repositorio>
cd "Bot Trader"
```

### 3. Crie um Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 5. Baixe Dados do NLTK

```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

### 6. Configure as Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas credenciais
# Use um editor de texto para preencher:
# - BINANCE_API_KEY
# - BINANCE_SECRET_KEY
# - TELEGRAM_BOT_TOKEN (opcional)
# - TELEGRAM_CHAT_ID (opcional)
```

---

## 🔑 Obtendo Credenciais

### Binance Testnet (Recomendado para Testes)

1. Acesse: [https://testnet.binance.vision/](https://testnet.binance.vision/)
2. Faça login com sua conta GitHub
3. Clique em "Generate HMAC_SHA256 Key"
4. Copie a API Key e Secret Key
5. Cole no arquivo `.env`

### Bot do Telegram (Opcional)

1. Abra o Telegram e fale com [@BotFather](https://t.me/BotFather)
2. Use o comando `/newbot` e siga as instruções
3. Copie o token fornecido
4. Para obter o CHAT_ID: fale com [@userinfobot](https://t.me/userinfobot)
5. Cole ambos no arquivo `.env`

---

## 💻 Uso

### Executar o Bot

```bash
python src/main.py
```

### Executar Backtesting

```bash
# Primeiro, baixe dados históricos
python src/backtesting/download_historical_data.py

# Execute o backtest
python src/backtesting/backtest_engine.py
```

### Executar Testes

```bash
# Teste de configuração
python tests/test_config.py

# Teste de logger
python tests/test_logger.py

# Teste de notificações
python tests/test_notifications.py
```

---

## ⚙️ Configuração

### Parâmetros de Trading

Edite [config/trading_params.py](config/trading_params.py):

```python
RISK_PER_TRADE_PERCENT = 0.01      # 1% do capital por trade
MAX_CAPITAL_RISK_PERCENT = 0.05    # 5% máximo em risco
TAKE_PROFIT_PERCENT = 0.005        # 0.5% de lucro alvo
STOP_LOSS_PERCENT = 0.002          # 0.2% de perda máxima
AI_CONFIDENCE_THRESHOLD = 0.70     # Confiança mínima da IA
DEFAULT_SYMBOL = "BTC/USDT"        # Par de trading
DEFAULT_TIMEFRAME = "1m"           # Timeframe (1m, 5m, 15m, etc.)
```

---

## 📊 Como Funciona

### Fluxo de Execução

1. **Coleta de Dados:**
   - Dados OHLCV em tempo real da Binance (via `ccxt`)
   - Notícias de criptomoedas (web scraping + APIs)

2. **Análise:**
   - Cálculo de indicadores técnicos (RSI, MACD, Volume MA)
   - Análise de sentimento de notícias (VADER)

3. **Geração de Sinal:**
   - IA combina dados de mercado + sentimento
   - Retorna: `BUY`, `SELL` ou `HOLD` com nível de confiança

4. **Execução:**
   - Se confiança > threshold: executa ordem de mercado
   - Calcula tamanho de posição baseado em risco
   - Define stop-loss e take-profit automaticamente

5. **Monitoramento:**
   - Monitora posições abertas
   - Fecha por stop-loss, take-profit ou sinal de venda
   - Envia notificações via Telegram

---

## ⚠️ Avisos Importantes

- **RISCO:** Trading de criptomoedas envolve risco elevado. Use apenas capital que pode perder.
- **TESTNET PRIMEIRO:** Sempre teste na Binance Testnet antes de usar dinheiro real.
- **NÃO GARANTIA DE LUCRO:** Este bot é educacional. Não há garantia de lucros.
- **RESPONSABILIDADE:** Você é responsável por suas próprias decisões de trading.
- **SEGURANÇA:** Nunca compartilhe suas API Keys. Mantenha o arquivo `.env` seguro.

---

## 🛠️ Desenvolvimento

### Melhorias Futuras

- [ ] Implementar modelos de ML mais avançados (LSTM, Transformers)
- [ ] Adicionar suporte para múltiplos pares de trading
- [ ] Criar dashboard web interativo (Dash/Plotly)
- [ ] Implementar estratégias adicionais (arbitragem, grid trading)
- [ ] Melhorar análise de sentimento (FinBERT, Twitter API)
- [ ] Adicionar testes unitários completos
- [ ] Implementar logging avançado e alertas

### Contribuindo

Pull requests são bem-vindos! Para mudanças maiores, abra uma issue primeiro.

---

## 📝 Licença

Este projeto é para fins educacionais. Use por sua própria conta e risco.

---

## 📞 Suporte

- **Issues:** Abra uma issue no GitHub
- **Documentação:** Consulte os comentários no código

---

**⚡ Happy Trading! ⚡**
