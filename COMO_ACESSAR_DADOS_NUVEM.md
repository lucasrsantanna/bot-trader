# 📱 Como Acessar Dados LIVE da Nuvem

## Seu Repositório GitHub

**URL:** https://github.com/lucasrsantanna/bot-trader

---

## 📂 Onde Estão os Dados?

### Opção 1: Via Browser (Mais Fácil)

1. Acesse: **https://github.com/lucasrsantanna/bot-trader**
2. Procure a pasta: **`cloud_data/`**
3. Clique em **`BTC_USDT_5m.json`**
4. Veja os dados em tempo real (atualizado a cada sincronização)

---

### Opção 2: URL Raw (Para Aplicativos)

**Para ler os dados em qualquer aplicação (celular, app, etc):**

```
Timeframe 5 minutos:
https://raw.githubusercontent.com/lucasrsantanna/bot-trader/main/cloud_data/BTC_USDT_5m.json

Timeframe 1 hora:
https://raw.githubusercontent.com/lucasrsantanna/bot-trader/main/cloud_data/BTC_USDT_1h.json

Timeframe 1 dia:
https://raw.githubusercontent.com/lucasrsantanna/bot-trader/main/cloud_data/BTC_USDT_1d.json
```

---

### Opção 3: Clonar o Repositório

Para ter os dados locais em outro computador:

```bash
git clone https://github.com/lucasrsantanna/bot-trader.git
cd bot-trader
# Os dados estão em: cloud_data/
```

---

## 📊 O Que Você Verá

Arquivo: `cloud_data/BTC_USDT_5m.json`

```json
{
  "symbol": "BTC/USDT",
  "timeframe": "5m",
  "timestamp": "2025-10-24T16:30:00.123456",
  "count": 50,
  "data": [
    {
      "Date": "2025-10-24 16:25:00+00:00",
      "Open": 110303.32,
      "High": 110444.28,
      "Low": 110128.12,
      "Close": 110359.96,
      "Volume": 15.75,
      "EMA9": 110312.45,
      "EMA21": 110245.67,
      "EMA50": 110156.89,
      "RSI": 45.2,
      "MACD": 125.3
    },
    ... (49 mais velas)
  ]
}
```

---

## 🔄 Quando os Dados Atualizam?

- **A cada ciclo de gráfico** (~30 segundos)
- **Quando você roda a GUI** em seu PC
- Os dados são salvos e sincronizados automaticamente

---

## 💻 Código Para Acessar de Qualquer Lugar

### Python

```python
import requests
import json

# Buscar dados 5m
url = "https://raw.githubusercontent.com/lucasrsantanna/bot-trader/main/cloud_data/BTC_USDT_5m.json"
response = requests.get(url)
data = response.json()

print(f"Última atualização: {data['timestamp']}")
print(f"Total de velas: {data['count']}")
print(f"Preço atual: ${data['data'][-1]['Close']:,.2f}")
```

### JavaScript/Node.js

```javascript
fetch('https://raw.githubusercontent.com/lucasrsantanna/bot-trader/main/cloud_data/BTC_USDT_5m.json')
  .then(res => res.json())
  .then(data => {
    console.log('Última atualização:', data.timestamp);
    console.log('Preço atual:', data.data[data.data.length - 1].Close);
  });
```

### cURL (Terminal/PowerShell)

```bash
curl -s https://raw.githubusercontent.com/lucasrsantanna/bot-trader/main/cloud_data/BTC_USDT_5m.json | jq .data[-1].Close
```

---

## 📱 Em um Celular/Navegador

### Android
1. Abra o navegador
2. Cole a URL: `https://github.com/lucasrsantanna/bot-trader/tree/main/cloud_data`
3. Veja os arquivos JSON
4. Toque em um arquivo para ver os dados

### iOS
Mesmo procedimento que Android

### Desktop
1. Abra navegador
2. Vá para: `https://github.com/lucasrsantanna/bot-trader`
3. Pasta: `cloud_data/`
4. Clique no arquivo JSON desejado

---

## 🎯 Dados Disponíveis

Cada arquivo JSON contém:

| Campo | Descrição |
|-------|-----------|
| `symbol` | Par de trading (BTC/USDT) |
| `timeframe` | Período (5m, 1h, 1d) |
| `timestamp` | Hora da última atualização |
| `count` | Número de velas |
| `data` | Array com velas OHLCV + indicadores |

**Campos de cada vela:**
- `Date` - Timestamp da vela
- `Open` - Preço de abertura
- `High` - Máximo da vela
- `Low` - Mínimo da vela
- `Close` - Preço de fechamento
- `Volume` - Volume de trading
- `EMA9`, `EMA21`, `EMA50` - Médias móveis exponenciais
- `RSI` - Relative Strength Index
- `MACD` - Moving Average Convergence Divergence

---

## ✅ Verificar Sincronização

Para confirmar que os dados estão sendo sincronizados:

1. **No seu PC:** Rode a GUI
   ```bash
   python teste_simples.py
   ```

2. **No GitHub:** Acesse
   ```
   https://github.com/lucasrsantanna/bot-trader/tree/main/cloud_data
   ```

3. **Verifique:** O timestamp do arquivo deve ser recente (agora)

4. **Se tiver dúvida:** Git log mostra quando foi o último commit
   ```bash
   git log --oneline | head -5
   ```

---

## 🚀 Em Viagem (Sem seu PC)

Quando estiver viajando sem seu computador:

1. **Acesse via browser:**
   ```
   https://github.com/lucasrsantanna/bot-trader/tree/main/cloud_data
   ```

2. **Ou via API (em um app):**
   ```
   https://raw.githubusercontent.com/lucasrsantanna/bot-trader/main/cloud_data/BTC_USDT_5m.json
   ```

3. **Os dados estarão sempre lá** (atualizados até a última vez que seu PC rodou a GUI)

---

## 📝 Resumo

| Situação | URL |
|----------|-----|
| Ver no browser | `github.com/lucasrsantanna/bot-trader/tree/main/cloud_data` |
| Ler em app (JSON) | `raw.githubusercontent.com/lucasrsantanna/bot-trader/main/cloud_data/BTC_USDT_5m.json` |
| Clonar repositório | `git clone https://github.com/lucasrsantanna/bot-trader.git` |
| Ver histórico | `github.com/lucasrsantanna/bot-trader/commits/main/cloud_data` |

---

**Pronto!** Seus dados LIVE estão na nuvem e acessíveis de qualquer lugar! 🚀
