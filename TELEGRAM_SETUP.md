# 📱 Guia de Configuração do Telegram

Este guia explica como configurar as notificações do Telegram para o Bot Trader.

## 1️⃣ Criar Bot no Telegram

1. Abra o Telegram e procure por **@BotFather**
2. Inicie conversa com `/start`
3. Crie novo bot com `/newbot`
4. Escolha um nome (ex: "Meu Bot Trader")
5. Escolha um username (ex: "meu_bot_trader_bot")
6. **Copie o token** que aparece (formato: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## 2️⃣ Obter Chat ID

### Opção A: Usando Bot Existente
1. Procure por **@userinfobot** no Telegram
2. Inicie conversa com `/start`
3. Ele retornará seu **Chat ID** (formato: `123456789`)

### Opção B: Via API
1. Envie uma mensagem qualquer para seu bot criado no passo 1
2. Acesse no navegador:
   ```
   https://api.telegram.org/bot<SEU_TOKEN>/getUpdates
   ```
3. Procure por `"chat":{"id":123456789}` no JSON retornado
4. Copie o número do `id`

## 3️⃣ Configurar no .env

Edite o arquivo `.env` na raiz do projeto:

```env
# Telegram Notifications
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

**⚠️ Importante**:
- O token deve estar completo (incluindo o `:` e tudo depois)
- O chat_id é apenas o número, sem aspas

## 4️⃣ Testar Conexão

Execute o script de teste:

```bash
python -c "from src.utils.notifications import notifier; notifier.send_message('✅ Telegram configurado com sucesso!')"
```

Se receber a mensagem no Telegram, está tudo certo!

## 📬 Tipos de Notificações

O bot enviará automaticamente:

### 🔵 Sinais da IA
- Quando RSI/MACD indicarem BUY ou SELL
- Inclui: Confiança, Preço, RSI, MACD

### 🟢 Trade Aberto
- Quando abrir posição LONG/SHORT
- Inclui: Preço de entrada, Stop Loss, Take Profit

### 🔴 Trade Fechado
- Quando fechar por SL/TP
- Inclui: P&L em $ e %, motivo do fechamento

### ⚠️ Erros Críticos
- Quando ocorrer erro no loop principal
- Permite monitoramento 24/7

## 🔕 Desabilitar Notificações

Para desabilitar temporariamente, basta comentar no `.env`:

```env
# TELEGRAM_BOT_TOKEN=seu_token
# TELEGRAM_CHAT_ID=seu_chat_id
```

O bot detectará automaticamente e continuará funcionando sem notificações.

## 🛠️ Troubleshooting

### "Telegram não configurado"
- Verifique se `.env` existe e tem as variáveis corretas
- Reinicie o bot após editar `.env`

### "Failed to send Telegram notification"
- Verifique conexão com internet
- Confirme que o token está correto
- Certifique-se de ter enviado `/start` para o bot

### Notificações não chegam
- Abra o Telegram e inicie conversa com seu bot enviando `/start`
- Bots do Telegram só podem enviar mensagens para usuários que iniciaram conversa

## 📊 Exemplo de Notificação

```
🟢 TRADE ABERTO

📊 Par: BTC/USDT
🔵 Tipo: LONG
💰 Preço: $120,824.61
📦 Quantidade: 0.041382
🛑 Stop Loss: $120,582.96 (-0.20%)
🎯 Take Profit: $121,428.73 (+0.50%)
```

---

**✅ Fase 3 - Completa!**
Notificações Telegram implementadas seguindo recomendações do Manus AI.
