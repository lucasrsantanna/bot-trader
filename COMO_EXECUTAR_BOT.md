# 🚀 COMO EXECUTAR O BOT MANUALMENTE

## Método 1: Executar via Duplo Clique (MAIS FÁCIL)

### Passo 1: Abrir o bot
1. Navegue até a pasta: `C:\Users\lucas\Desktop\Bot Trader\windows\`
2. **Duplo clique** em `start_bot.bat`
3. Uma janela preta (terminal) vai abrir

### Passo 2: Acompanhar a execução
Você verá mensagens como:
```
======================================================================
 BOT AUTOMATICO INICIADO
======================================================================
Capital: $603.68
Trades executados: 3
Posicao: ABERTA/FECHADA
Modo: SIMULACAO
======================================================================

[INICIO] Loop automatico (intervalo: 60s)
Pressione Ctrl+C para parar

[23:20:34] [ANALISE] Preco: $111,970.00 | RSI: 51.7 | Sinal: HOLD (50%)
```

### Passo 3: Aguardar sinais
O bot vai:
- ✅ Coletar dados a cada 60 segundos
- ✅ Calcular RSI e MACD
- ✅ Mostrar o sinal gerado (BUY/SELL/HOLD)

**Quando houver uma entrada:**
```
======================================================================
[EXECUTANDO COMPRA]
Preco: $111,341.29
Quantidade: 0.041408 BTC
Valor: $4,611.00
Stop Loss: $111,118.48
Take Profit: $111,898.64
[SIMULACAO] Ordem NAO enviada para Binance
======================================================================
```

### Passo 4: Para parar o bot
- Pressione `Ctrl + C` no terminal
- Ou simplesmente feche a janela

---

## Método 2: Ver Logs em Tempo Real (2 Janelas)

### Janela 1: Executar o bot
```batch
cd "C:\Users\lucas\Desktop\Bot Trader"
windows\start_bot.bat
```

### Janela 2: Monitorar bot_dados.json
Abra outro terminal e execute:
```batch
cd "C:\Users\lucas\Desktop\Bot Trader"
python -c "import json, time; [print(json.dumps(json.load(open('bot_dados.json')), indent=2)) or time.sleep(5) for _ in iter(int, 1)]"
```

Ou simplesmente abra o arquivo `bot_dados.json` no VSCode e ele vai atualizar automaticamente!

---

## Método 3: Forçar Entrada Imediata (Para Teste)

Se você quiser **ver uma entrada acontecer agora**, vou criar um script de teste:

### teste_entrada_forcada.py
Execute este script para forçar o bot a fazer uma análise e potencialmente entrar:

```python
# Este script força o bot a analisar o mercado AGORA
# e mostra se há condições para entrada
```

---

## 📊 Como Interpretar os Sinais

### 🟢 Sinal de COMPRA (BUY)
```
[ANALISE] Preco: $111,341.29 | RSI: 35.2 | Sinal: BUY (75%)

======================================================================
[EXECUTANDO COMPRA]
Preco: $111,341.29
Quantidade: 0.041408 BTC
Stop Loss: $111,118.48  ← Vende se cair 0.2%
Take Profit: $111,898.64 ← Vende se subir 0.5%
[SIMULACAO] Ordem NAO enviada
======================================================================
```

**O que aconteceu:**
- RSI < 40 (35.2 = sobrevendido)
- Bot decidiu COMPRAR
- Definiu Stop Loss e Take Profit
- **Modo SIMULAÇÃO:** Não enviou ordem real

### 🔴 Sinal de VENDA (SELL)
```
[ANALISE] Preco: $112,500.00 | RSI: 68.4 | Sinal: SELL (75%)

======================================================================
[FECHANDO POSICAO - TAKE PROFIT]
Entrada: $111,341.29
Saida: $112,500.00
P&L: $+48.00 (+0.43%)
[SIMULACAO] Venda NAO enviada
Capital: $651.68
======================================================================
```

**O que aconteceu:**
- RSI > 60 (68.4 = sobrecomprado)
- Bot decidiu VENDER
- Lucro de $48.00 (+0.43%)
- Capital atualizado para $651.68

### ⚪ Sinal de MANTER (HOLD)
```
[ANALISE] Preco: $111,970.00 | RSI: 51.7 | Sinal: HOLD (50%)
```

**O que aconteceu:**
- RSI entre 40 e 60 (zona neutra)
- Bot decidiu NÃO fazer nada
- Aguarda próximo ciclo (60 segundos)

---

## 🎯 Configurações para Mais Entradas

Se quiser que o bot execute **mais entradas**, você pode ajustar:

### Arquivo: bot_dados.json (linha 151)
```json
{
  "config": {
    "intervalo": 60  ← Mudar para 30 (analisa a cada 30s)
  }
}
```

### Ou ajustar thresholds no código:
**Arquivo:** `bot_automatico.py` (linha ~160)

```python
# Tornar bot mais agressivo
if rsi < 45:  # Era 40, agora 45 (mais entradas de compra)
    sinal = "BUY"
elif rsi > 55:  # Era 60, agora 55 (mais entradas de venda)
    sinal = "SELL"
```

---

## 📁 Arquivos Importantes

### 1. bot_dados.json
Atualizações em tempo real:
- Capital atual
- Trades executados
- Posição aberta/fechada
- Logs de todas as operações

### 2. Logs do terminal
Saída visual do bot em execução

### 3. Dashboard (Opcional)
Se quiser visualizar graficamente:
```batch
cd "C:\Users\lucas\Desktop\Bot Trader"
venv\Scripts\streamlit run dashboard.py
```
Abre em: http://localhost:8501

---

## ⚙️ Ativar Ordens REAIS (CUIDADO!)

**ATENÇÃO:** Só faça isso se tiver certeza!

### Arquivo: bot_dados.json (linha 150)
```json
{
  "config": {
    "executar_ordens": true  ← Mudar de false para true
  }
}
```

**Quando ativado:**
- ⚠️ Bot vai enviar ordens REAIS para Binance Testnet
- ⚠️ Usa saldo real da conta Testnet
- ⚠️ Requer API Keys válidas

---

## 🐛 Solução de Problemas

### Bot não abre
- Verifique se `venv` está criado
- Execute: `python -m venv venv`
- Execute: `venv\Scripts\pip install -r requirements.txt`

### Bot fecha imediatamente
- Erro de módulos faltando
- Execute novamente e leia a mensagem de erro

### Bot não gera sinais
- Mercado pode estar em zona neutra (RSI 40-60)
- Aguarde alguns minutos
- Ou force teste com script abaixo

---

## 🧪 Script de Teste Rápido

Vou criar um script que você pode executar para ver **análise imediata**:
