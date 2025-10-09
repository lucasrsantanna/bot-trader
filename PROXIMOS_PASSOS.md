# 📝 PRÓXIMOS PASSOS - Bot Trader

## ✅ O QUE JÁ FOI FEITO:

1. ✅ Estrutura completa de diretórios criada
2. ✅ Todos os arquivos Python organizados nos diretórios corretos
3. ✅ Arquivos `__init__.py` criados em todos os módulos
4. ✅ `requirements.txt` com todas as dependências
5. ✅ `.env.example` como template de configuração
6. ✅ `.gitignore` configurado para Python
7. ✅ `README.md` com documentação completa
8. ✅ Bugs de sintaxe corrigidos (aspas escapadas)

---

## 🚀 PRÓXIMOS PASSOS PARA VOCÊ:

### **Passo 1: Instalar Dependências** (OBRIGATÓRIO)

Abra o terminal no diretório do projeto e execute:

```bash
# Ativar ambiente virtual (se já criou)
# Windows:
venv\Scripts\activate

# Ou criar um novo ambiente virtual:
python -m venv venv
venv\Scripts\activate

# Instalar todas as bibliotecas
pip install -r requirements.txt

# Baixar dados do NLTK (necessário para análise de sentimento)
python -c "import nltk; nltk.download('vader_lexicon')"
```

**Possíveis problemas:**
- Se houver erro com alguma biblioteca, instale individualmente:
  ```bash
  pip install ccxt pandas numpy scikit-learn nltk beautifulsoup4 requests python-dotenv aiohttp python-telegram-bot textblob lxml
  ```

---

### **Passo 2: Configurar Credenciais da Binance** (OBRIGATÓRIO)

#### A. Criar Conta na Binance Testnet

1. Acesse: **https://testnet.binance.vision/**
2. Clique em "Login with GitHub"
3. Após login, clique em **"Generate HMAC_SHA256 Key"**
4. Você receberá:
   - **API Key** (ex: `abc123def456...`)
   - **Secret Key** (ex: `xyz789uvw012...`)
5. **COPIE E GUARDE** essas chaves com segurança

#### B. Criar Arquivo `.env`

1. Copie o arquivo `.env.example` e renomeie para `.env`:
   ```bash
   # Windows (PowerShell)
   Copy-Item .env.example .env

   # Ou manualmente: copie e cole o arquivo, renomeie para ".env"
   ```

2. Abra o arquivo `.env` com um editor de texto

3. Preencha com suas credenciais:
   ```env
   BINANCE_API_KEY=SUA_API_KEY_AQUI
   BINANCE_SECRET_KEY=SUA_SECRET_KEY_AQUI
   USE_TESTNET=true
   TELEGRAM_BOT_TOKEN=deixe_vazio_por_enquanto
   TELEGRAM_CHAT_ID=deixe_vazio_por_enquanto
   DEBUG=true
   LOG_LEVEL=INFO
   TIMEZONE=America/Sao_Paulo
   ```

---

### **Passo 3: Testar Conexão com a Binance** (RECOMENDADO)

Execute este teste para verificar se suas credenciais estão corretas:

```bash
python src/data_collector/binance_data.py
```

**Resultado esperado:**
- Deve mostrar dados OHLCV do BTC/USDT
- Deve mostrar o preço atual do Bitcoin

**Se der erro:**
- Verifique se as credenciais estão corretas no `.env`
- Verifique se você está usando a testnet (`USE_TESTNET=true`)
- Verifique se as dependências foram instaladas corretamente

---

### **Passo 4: Configurar Bot do Telegram** (OPCIONAL, mas recomendado)

Para receber notificações dos trades:

1. **Criar Bot:**
   - Abra o Telegram
   - Procure por **@BotFather**
   - Envie `/newbot`
   - Siga as instruções (escolha um nome e username)
   - **Copie o TOKEN** fornecido

2. **Obter Chat ID:**
   - Procure por **@userinfobot** no Telegram
   - Envie `/start`
   - **Copie o ID** mostrado

3. **Adicionar no `.env`:**
   ```env
   TELEGRAM_BOT_TOKEN=seu_token_aqui
   TELEGRAM_CHAT_ID=seu_chat_id_aqui
   ```

4. **Testar notificações:**
   ```bash
   python tests/test_notifications.py
   ```

---

### **Passo 5: Executar Backtesting** (ANTES de trading real!)

Teste a estratégia em dados históricos primeiro:

```bash
# 1. Baixar dados históricos
python src/backtesting/download_historical_data.py

# 2. Executar backtest
python src/backtesting/backtest_engine.py
```

**O que analisar:**
- Taxa de acerto (win rate)
- Lucro/prejuízo total
- Número de trades executados
- Drawdown máximo

---

### **Passo 6: Executar o Bot** (TESTNET!)

**⚠️ IMPORTANTE: Sempre comece com a TESTNET!**

```bash
python src/main.py
```

**O que vai acontecer:**
- O bot vai coletar dados da Binance a cada 60 segundos
- Vai analisar notícias e sentimento
- Vai calcular indicadores técnicos
- Vai gerar sinais de compra/venda
- Vai executar trades automaticamente (na testnet)
- Vai enviar notificações no Telegram (se configurado)

**Para parar o bot:**
- Pressione `Ctrl + C` no terminal

---

## ⚙️ AJUSTES E OTIMIZAÇÕES:

### Ajustar Parâmetros de Trading

Edite o arquivo [config/trading_params.py](config/trading_params.py):

```python
# Quanto você quer arriscar por trade?
RISK_PER_TRADE_PERCENT = 0.01  # 1% (aumente ou diminua)

# Quanto de lucro você quer por trade? (scalping = pequeno)
TAKE_PROFIT_PERCENT = 0.005    # 0.5% (ajuste conforme seu objetivo)

# Quanto de perda você aceita? (stop-loss)
STOP_LOSS_PERCENT = 0.002      # 0.2% (sempre menor que take profit)

# Qual confiança mínima da IA para executar?
AI_CONFIDENCE_THRESHOLD = 0.70 # 70% (aumente para ser mais conservador)

# Qual criptomoeda negociar?
DEFAULT_SYMBOL = "BTC/USDT"    # Pode mudar para ETH/USDT, BNB/USDT, etc.

# Qual timeframe usar?
DEFAULT_TIMEFRAME = "1m"       # 1m = 1 minuto (scalping)
                               # Opções: 1m, 5m, 15m, 1h, 4h, 1d
```

### Melhorar a IA

O bot atualmente usa lógica simples baseada em:
- RSI < 30 + MACD positivo + sentimento positivo = COMPRA
- RSI > 70 + MACD negativo + sentimento negativo = VENDA

**Para melhorar:**
1. Coletar dados históricos
2. Treinar um modelo de machine learning
3. Edite [src/ai_model/model_trainer.py](src/ai_model/model_trainer.py)
4. Use scikit-learn, TensorFlow ou PyTorch

---

## 🐛 SOLUÇÃO DE PROBLEMAS COMUNS:

### Erro: "ModuleNotFoundError: No module named 'ccxt'"
**Solução:** As dependências não foram instaladas
```bash
pip install -r requirements.txt
```

### Erro: "KeyError: BINANCE_API_KEY"
**Solução:** O arquivo `.env` não foi criado ou está vazio
- Copie `.env.example` para `.env`
- Preencha com suas credenciais

### Erro: "ccxt.AuthenticationError"
**Solução:** Credenciais da Binance incorretas
- Verifique se copiou corretamente a API Key e Secret
- Certifique-se de estar usando a testnet
- Gere novas chaves em https://testnet.binance.vision/

### Erro: "Request failed with code 400"
**Solução:** Pode ser problema de permissões da API
- Na Binance Testnet, verifique se a API tem permissão de "Spot & Margin Trading"

### Bot não está executando trades
**Possíveis causas:**
1. Confiança da IA abaixo do threshold
   - Diminua `AI_CONFIDENCE_THRESHOLD` em trading_params.py
2. Não há sinais de compra/venda
   - Verifique os logs para ver os sinais gerados
3. Mercado muito estável (sem volatilidade)
   - Espere por mais movimento de preço

---

## 📊 MONITORAMENTO:

### Ver Logs em Tempo Real

Os logs são exibidos no terminal onde você executou o bot.

**Exemplo de log:**
```
2024-10-08 22:30:00 | INFO | Dados de mercado atualizados. Último preço: 67234.50
2024-10-08 22:30:05 | INFO | Sinal gerado: BUY com confiança 0.75
2024-10-08 22:30:06 | INFO | COMPRA 0.001500 de BTC/USDT @ 67234.50. SL: 67100.00, TP: 67570.00
```

### Verificar Posições Abertas

O bot mostra no terminal quando:
- Abre uma posição (COMPRA)
- Fecha por take-profit (lucro)
- Fecha por stop-loss (perda)

---

## 🚀 INDO PARA PRODUÇÃO (Dinheiro Real):

**⚠️ SOMENTE APÓS TESTAR MUITO NA TESTNET!**

1. Crie conta na Binance real: **https://www.binance.com/**
2. Gere API Keys na conta real (com permissões de trading)
3. Mude no `.env`:
   ```env
   USE_TESTNET=false
   BINANCE_API_KEY=sua_api_key_real
   BINANCE_SECRET_KEY=sua_secret_real
   ```
4. **COMECE COM CAPITAL PEQUENO!**
5. Monitore constantemente nos primeiros dias

---

## 📞 PRECISA DE AJUDA?

1. Verifique o [README.md](README.md) para documentação geral
2. Leia os comentários no código - eles explicam cada função
3. Abra uma issue no GitHub (se estiver usando Git)

---

**⚡ Boa sorte com seu bot trader! ⚡**

**Lembre-se:** Trading envolve risco. Este bot é educacional. Sempre teste antes de usar dinheiro real!
