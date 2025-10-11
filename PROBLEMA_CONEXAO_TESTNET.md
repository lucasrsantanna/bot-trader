# 📋 RELATÓRIO: PROBLEMA DE CONEXÃO BINANCE TESTNET

**Data:** 10/10/2025
**Horário:** 14:10 BRT
**Status:** ⚠️ Em resolução

---

## 🎯 OBJETIVO
Fazer o bot conectar na **Binance Testnet** (testnet.binance.vision) para operar com dinheiro fake.

---

## ❌ PROBLEMA ATUAL

O bot **NÃO consegue conectar** na Binance Testnet. Retorna erro:
```
ERROR - binance does not have a testnet/sandbox URL for sapi endpoints
```

---

## 🔍 CAUSA RAIZ

O **ccxt** está tentando acessar endpoints `sapi` que a Testnet **não possui**. Além disso, há **3 arquivos com configurações conflitantes**:

| Arquivo | Status | Problemas |
|---------|--------|-----------|
| `src/data_collector/binance_data.py` | ✅ **CORRETO** | URLs e config corretas |
| `src/trading/executor.py` | ❌ **ERRADO** | URLs erradas + falta `import os` |
| `bot_automatico.py` | ❌ **ERRADO** | URLs erradas |

---

## 📝 HISTÓRICO DE TENTATIVAS

### **Tentativa 1:** Script start_bot.bat fechava imediatamente
- **Problema:** Comando `tee` não existe no Windows
- **Solução:** Removi o `| tee` da linha 59
- **Resultado:** ✅ Janela ficou aberta

### **Tentativa 2:** ModuleNotFoundError: No module named 'config'
- **Problema:** Python não encontrava os módulos
- **Solução:** Adicionei `PYTHONPATH` no start_bot.bat (linha 36-37)
- **Resultado:** ✅ Módulos carregados

### **Tentativa 3:** SyntaxError em model_trainer.py
- **Problema:** Aspas escapadas `\"timestamp\"`
- **Solução:** Corrigi para `"timestamp"`
- **Resultado:** ✅ Syntax error resolvido

### **Tentativa 4:** Invalid Api-Key ID (-2008)
- **Problema:** API Keys configuradas mas URL estava errada
- **Solução:** Atualizei `.env` com novas keys do testnet
- **Keys usadas:**
  ```
  API_KEY: ZI46pLZLbKX8zn4fIey1gQEyxkJX4u7bqjGT0ykIXfTIv1kxzE7jqHtGqpIDWGTO
  SECRET_KEY: IFFbcMeSMQnW8KuxP6bRXNJMmrcbYgyPjAf5AzE8Ts0C6zN1DTiLUWYgzB5DUWSY
  ```
- **Resultado:** ❌ Ainda deu erro de API inválida

### **Tentativa 5:** Corrigir URLs para binance.vision
- **Problema:** Código apontava para `api.binance.com` (produção)
- **Solução:** Configurei URLs da testnet em `binance_data.py`:
  ```python
  self.exchange.urls['api'] = 'https://testnet.binance.vision'
  self.exchange.hostname = 'testnet.binance.vision'
  ```
- **Resultado:** ❌ Ainda deu erro

### **Tentativa 6:** Desabilitar endpoints sapi
- **Problema:** ccxt tentava acessar `/sapi/` que testnet não tem
- **Solução:** Adicionei em `binance_data.py`:
  ```python
  'fetchCurrencies': False,
  self.exchange.options['loadMarkets'] = False
  ```
- **Resultado:** ⏳ **Aguardando teste** (Lucas alterou 3 arquivos manualmente)

---

## 📊 ESTADO DOS 3 ARQUIVOS

### ✅ **binance_data.py** (CORRETO)
**Localização:** `src/data_collector/binance_data.py`

```python
class BinanceDataCollector:
    def __init__(self, symbol='BTC/USDT', timeframe='1m', limit=100):
        import os
        use_testnet = os.getenv('USE_TESTNET', 'false').lower() == 'true'

        if use_testnet:
            self.exchange = ccxt.binance({
                'apiKey': settings.BINANCE_API_KEY,
                'secret': settings.BINANCE_SECRET_KEY,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',              # ✅ SPOT testnet
                    'fetchCurrencies': False,           # ✅ Evita sapi
                },
            })
            # ✅ URLs corretas
            self.exchange.urls['api'] = 'https://testnet.binance.vision'
            self.exchange.hostname = 'testnet.binance.vision'
            # ✅ Desabilita load_markets
            self.exchange.options['loadMarkets'] = False
```

---

### ❌ **executor.py** (ERRADO - Lucas alterou)
**Localização:** `src/trading/executor.py`

**Problemas identificados:**
```python
# ❌ PROBLEMA 1: Falta import os no início do arquivo
# Linha 1-3 não tem: import os

class OrderExecutor:
    def __init__(self):
        # ❌ PROBLEMA 2: Usa os.getenv sem ter importado 'os'
        if os.getenv("USE_TESTNET", 'false').lower() == 'true':  # ERRO!

            # ❌ PROBLEMA 3: defaultType errado
            exchange_config['options'] = {
                'defaultType': 'future',  # Deveria ser 'spot'
            }

            # ❌ PROBLEMA 4: URLs erradas
            exchange_config['urls'] = {
                'api': {
                    'public': 'https://testnet.binancefuture.com/fapi/v1',  # ERRADO
                    'private': 'https://testnet.binancefuture.com/fapi/v1', # ERRADO
                }
            }
            # ❌ PROBLEMA 5: Falta fetchCurrencies: False
            # ❌ PROBLEMA 6: Falta loadMarkets: False
            # ❌ PROBLEMA 7: Não seta exchange.urls['api'] após criar
```

**URLs corretas deveriam ser:**
- ✅ `https://testnet.binance.vision/api/v3`

---

### ❌ **bot_automatico.py** (ERRADO - Lucas alterou)
**Localização:** `bot_automatico.py` (raiz)

**Problemas identificados:**
```python
class BotAutomatico:
    def __init__(self):
        # ❌ PROBLEMA 1: defaultType errado
        if os.getenv("USE_TESTNET", 'false').lower() == 'true':
            exchange_config['options'] = {
                'defaultType': 'future',  # Deveria ser 'spot'
                'testnet': True,
            }

            # ❌ PROBLEMA 2: URLs erradas
            exchange_config['urls'] = {
                'api': {
                    'public': 'https://testnet.binancefuture.com/fapi/v1',  # ERRADO
                    'private': 'https://testnet.binancefuture.com/fapi/v1', # ERRADO
                }
            }
            # ❌ PROBLEMA 3: Falta fetchCurrencies: False
            # ❌ PROBLEMA 4: Falta loadMarkets: False
            # ❌ PROBLEMA 5: Não seta exchange.urls['api'] após criar
```

---

## 🔧 SOLUÇÃO NECESSÁRIA

### **Correções para executor.py:**

```python
# 1. Adicionar no topo do arquivo (após outras imports)
import os

class OrderExecutor:
    def __init__(self):
        import os  # Ou adicionar no topo
        use_testnet = os.getenv('USE_TESTNET', 'false').lower() == 'true'

        if use_testnet:
            # Para Testnet, usar modo sandbox
            self.exchange = ccxt.binance({
                'apiKey': settings.BINANCE_API_KEY,
                'secret': settings.BINANCE_SECRET_KEY,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',          # ✅ CORRIGIDO
                    'fetchCurrencies': False,       # ✅ ADICIONADO
                },
            })
            # ✅ Setar URLs manualmente após criação
            self.exchange.urls['api'] = 'https://testnet.binance.vision'
            self.exchange.hostname = 'testnet.binance.vision'
            self.exchange.options['loadMarkets'] = False
        else:
            # Produção - Futures
            self.exchange = ccxt.binance({
                'apiKey': settings.BINANCE_API_KEY,
                'secret': settings.BINANCE_SECRET_KEY,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future',
                }
            })
```

---

### **Correções para bot_automatico.py:**

```python
class BotAutomatico:
    def __init__(self):
        # Configuração da Exchange
        use_testnet = os.getenv("USE_TESTNET", 'false').lower() == 'true'

        if use_testnet:
            self.exchange = ccxt.binance({
                'apiKey': os.getenv("BINANCE_API_KEY"),
                'secret': os.getenv("BINANCE_SECRET_KEY"),
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',          # ✅ CORRIGIDO
                    'fetchCurrencies': False,       # ✅ ADICIONADO
                },
            })
            # ✅ Setar URLs manualmente
            self.exchange.urls['api'] = 'https://testnet.binance.vision'
            self.exchange.hostname = 'testnet.binance.vision'
            self.exchange.options['loadMarkets'] = False
            print("[INFO] Usando Binance Testnet - SPOT")
        else:
            self.exchange = ccxt.binance({
                'apiKey': os.getenv("BINANCE_API_KEY"),
                'secret': os.getenv("BINANCE_SECRET_KEY"),
                'enableRateLimit': True,
                'options': {'defaultType': 'future'}
            })
            print("[INFO] Usando Binance Produção - FUTURES")
```

---

## 📌 INFORMAÇÕES IMPORTANTES

**Testnet usada:** https://testnet.binance.vision (SPOT Testnet)
**API Keys:** Geradas em testnet.binance.vision
**Tipo:** SPOT (não Futures)
**Permissões:** TRADE, USER_DATA, USER_STREAM ✅

**Arquivo `.env` atual:**
```env
BINANCE_API_KEY=ZI46pLZLbKX8zn4fIey1gQEyxkJX4u7bqjGT0ykIXfTIv1kxzE7jqHtGqpIDWGTO
BINANCE_SECRET_KEY=IFFbcMeSMQnW8KuxP6bRXNJMmrcbYgyPjAf5AzE8Ts0C6zN1DTiLUWYgzB5DUWSY
USE_TESTNET=true
```

---

## 🔄 POR QUE SPOT E NÃO FUTURES?

As API Keys foram geradas em **testnet.binance.vision**, que é a **Testnet de SPOT**, não de Futures.

- ❌ **Testnet Futures:** `testnet.binancefuture.com` (requer keys diferentes)
- ✅ **Testnet Spot:** `testnet.binance.vision` (nossas keys atuais)

Por isso o código deve usar `defaultType: 'spot'` e URLs `testnet.binance.vision`.

---

## ⏭️ PRÓXIMOS PASSOS

1. ✅ Corrigir `executor.py` com as mudanças acima
2. ✅ Corrigir `bot_automatico.py` com as mudanças acima
3. ✅ Testar `start_bot.bat` novamente
4. ✅ Verificar se conecta sem erro
5. ✅ Confirmar que dados OHLCV são coletados

---

## 📊 RESUMO DOS ERROS

| Erro | O que era | O que deve ser |
|------|-----------|----------------|
| **URL** | `testnet.binancefuture.com` | `testnet.binance.vision` |
| **Type** | `future` | `spot` |
| **Configs** | Nenhuma | `fetchCurrencies: False` + `loadMarkets: False` |
| **Import** | Falta `import os` | `import os` no topo |

---

## ✅ VALIDAÇÃO FINAL

Quando estiver correto, o log deve mostrar:
```
INFO - Atualizando dados de mercado...
INFO - Dados OHLCV de BTC/USDT (1m) coletados com sucesso.
INFO - Dados de mercado atualizados. Último preço: 95234.50
```

**SEM ERROS** de `Invalid Api-Key` ou `sapi endpoints`.

---

**Documento criado para compartilhamento com assistente de IA.**
**Aguardando correções nos arquivos `executor.py` e `bot_automatico.py`.**
