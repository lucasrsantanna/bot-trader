# ✅ CHECKLIST RÁPIDO - Configuração do Bot Trader

Use esta checklist para configurar seu bot rapidamente!

---

## 📦 FASE 1: INSTALAÇÃO (15-20 minutos)

### 1.1 Ambiente Python
```bash
□ Verificar Python instalado (python --version)
□ Deve ser 3.9 ou superior
```

### 1.2 Ambiente Virtual
```bash
□ python -m venv venv
□ Windows: venv\Scripts\activate
□ Linux/Mac: source venv/bin/activate
```

### 1.3 Dependências
```bash
□ pip install -r requirements.txt
□ python -c "import nltk; nltk.download('vader_lexicon')"
```

**✅ Teste:** Execute `python -c "import ccxt, pandas, nltk"` - não deve dar erro

---

## 🔑 FASE 2: CREDENCIAIS (10 minutos)

### 2.1 Binance Testnet
```bash
□ Acessar https://testnet.binance.vision/
□ Login com GitHub
□ Clicar "Generate HMAC_SHA256 Key"
□ Copiar API Key
□ Copiar Secret Key
```

### 2.2 Criar arquivo .env
```bash
□ Copiar .env.example para .env
□ Abrir .env em editor de texto
□ Colar BINANCE_API_KEY=sua_key_aqui
□ Colar BINANCE_SECRET_KEY=sua_secret_aqui
□ Salvar arquivo
```

**✅ Teste:** Execute `python src/data_collector/binance_data.py` - deve mostrar dados do BTC

---

## 📱 FASE 3: TELEGRAM (OPCIONAL - 5 minutos)

```bash
□ Abrir Telegram
□ Procurar @BotFather
□ Enviar /newbot
□ Seguir instruções
□ Copiar TOKEN
□ Procurar @userinfobot
□ Copiar CHAT_ID
□ Adicionar ambos no .env
```

**✅ Teste:** Execute `python tests/test_notifications.py` - deve receber mensagem no Telegram

---

## 🧪 FASE 4: TESTES (10 minutos)

### 4.1 Teste de Configuração
```bash
□ python tests/test_config.py
□ Deve exibir: "Configurações carregadas com sucesso!"
```

### 4.2 Teste de Coleta de Dados
```bash
□ python src/data_collector/binance_data.py
□ Deve mostrar dados OHLCV e preço atual
```

### 4.3 Teste de Indicadores
```bash
□ python src/indicators/technical_indicators.py
□ Deve mostrar DataFrame com RSI, MACD, etc.
```

### 4.4 Teste de Sinais
```bash
□ python src/ai_model/signal_generator.py
□ Deve gerar sinais de exemplo (BUY/SELL/HOLD)
```

---

## 📊 FASE 5: BACKTESTING (15 minutos)

### 5.1 Download de Dados
```bash
□ python src/backtesting/download_historical_data.py
□ Aguardar download (pode demorar)
□ Verificar se data/historical/ tem arquivos
```

### 5.2 Executar Backtest
```bash
□ python src/backtesting/backtest_engine.py
□ Analisar relatório gerado
□ Verificar win rate
□ Verificar P&L total
```

**⚠️ Se win rate < 50% ou P&L negativo:**
- Ajuste parâmetros em config/trading_params.py
- Execute novamente o backtest
- Repita até obter resultados positivos

---

## 🚀 FASE 6: EXECUTAR BOT (TESTNET!)

### 6.1 Verificação Final
```bash
□ Confirmar USE_TESTNET=true no .env
□ Confirmar credenciais corretas
□ Confirmar capital inicial em src/main.py (linha 148)
```

### 6.2 Executar
```bash
□ python src/main.py
□ Observar logs no terminal
□ Aguardar sinais de compra/venda
□ Verificar notificações no Telegram
```

### 6.3 Monitoramento (Primeiras Horas)
```bash
□ Verificar se está coletando dados
□ Verificar se está gerando sinais
□ Verificar se executa ordens
□ Verificar stop-loss/take-profit funcionando
□ Anotar performance inicial
```

**Para parar:** Pressione `Ctrl + C`

---

## 🎛️ FASE 7: AJUSTES (Contínuo)

### 7.1 Parâmetros de Trading
Edite [config/trading_params.py](config/trading_params.py):

```python
□ RISK_PER_TRADE_PERCENT    # Quanto arriscar por trade
□ TAKE_PROFIT_PERCENT       # Quanto de lucro alvo
□ STOP_LOSS_PERCENT         # Quanto de perda aceitar
□ AI_CONFIDENCE_THRESHOLD   # Confiança mínima para trade
```

### 7.2 Símbolos e Timeframes
```python
□ DEFAULT_SYMBOL     # BTC/USDT, ETH/USDT, etc.
□ DEFAULT_TIMEFRAME  # 1m, 5m, 15m, 1h, etc.
```

### 7.3 Análise de Performance
Após 24-48h de execução:
```bash
□ Calcular win rate real
□ Calcular P&L total
□ Comparar com backtest
□ Ajustar parâmetros se necessário
```

---

## ⚠️ ANTES DE IR PARA PRODUÇÃO

### Checklist de Segurança:
```bash
□ Testei por pelo menos 1-2 semanas na testnet
□ Win rate consistente > 55%
□ P&L positivo por 7+ dias consecutivos
□ Entendo todos os parâmetros de risco
□ Tenho capital que posso perder
□ API Keys da Binance real criadas
□ Permissions corretas (Spot Trading habilitado)
□ IP whitelist configurado (recomendado)
□ 2FA habilitado na Binance
□ Começando com capital PEQUENO (ex: $100-500)
□ Monitoramento constante nos primeiros dias
```

### Mudar para Produção:
```bash
□ Gerar novas API Keys na Binance REAL
□ Editar .env: USE_TESTNET=false
□ Editar .env: BINANCE_API_KEY=key_real
□ Editar .env: BINANCE_SECRET_KEY=secret_real
□ Reduzir capital inicial se for primeiro uso real
□ Executar python src/main.py
□ MONITORAR CONSTANTEMENTE
```

---

## 🆘 TROUBLESHOOTING RÁPIDO

### Erro: "No module named 'ccxt'"
```bash
Solução: pip install -r requirements.txt
```

### Erro: "KeyError: BINANCE_API_KEY"
```bash
Solução: Criar arquivo .env com suas credenciais
```

### Erro: "AuthenticationError"
```bash
Solução: Verificar API Keys no .env
Solução: Gerar novas keys na Binance Testnet
```

### Bot não executa trades
```bash
Verificar: Confiança da IA nos logs
Solução: Diminuir AI_CONFIDENCE_THRESHOLD
Verificar: Se há sinais sendo gerados
Solução: Aguardar mais volatilidade no mercado
```

### Muitas perdas consecutivas
```bash
Solução: PARAR O BOT imediatamente
Solução: Revisar parâmetros de trading
Solução: Executar backtest novamente
Solução: Verificar se mercado está muito volátil
```

---

## 📚 DOCUMENTAÇÃO COMPLETA

- **Instalação detalhada:** [PROXIMOS_PASSOS.md](PROXIMOS_PASSOS.md)
- **Visão geral:** [README.md](README.md)
- **Status do projeto:** [STATUS_DO_PROJETO.md](STATUS_DO_PROJETO.md)

---

## ✅ CHECKLIST CONCLUÍDO?

Quando você completar todas as fases acima:

🎉 **Parabéns! Seu bot está operacional!** 🎉

**Lembre-se:**
- ⚠️ Trading tem riscos
- 📊 Monitore sempre
- 💰 Use capital que pode perder
- 🧪 Teste muito na testnet primeiro

**Boa sorte!** 🚀
