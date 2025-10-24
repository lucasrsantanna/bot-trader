# 🚀 Setup - Sincronização LIVE na Nuvem

## Problema
Você precisa acessar dados LIVE do bot de qualquer lugar (viagens, etc), sem depender do computador estar ligado.

## Solução
Sistema de **Cloud Sync com GitHub** que:
- ✅ Fetch dados LIVE de BTC/USDT
- ✅ Salva em JSON automáticamente
- ✅ Sincroniza com GitHub (grátis)
- ✅ Acessa de qualquer dispositivo/internet

---

## PASSO 1: Configurar GitHub

### 1.1 - Se NÃO tem repositório Git ainda:

```bash
cd "c:\Users\lucas\Desktop\Bot Trader"
git init
git add .
git commit -m "Initial commit - Bot Trader"
```

### 1.2 - Conectar com GitHub (remoto):

```bash
git remote add origin https://github.com/SEU_USUARIO/bot-trader.git
git branch -M main
git push -u origin main
```

**Onde:**
- `SEU_USUARIO` = seu username do GitHub
- `bot-trader` = nome do repositório (crie em github.com)

---

## PASSO 2: Configurar Git Credentials (Uma vez)

**Windows - Usar Git Credential Manager:**

```bash
git config --global credential.helper wincred
```

Ou **via SSH:**

```bash
# Gerar chave SSH
ssh-keygen -t ed25519 -C "seu_email@gmail.com"

# Adicionar em GitHub > Settings > SSH Keys
cat ~/.ssh/id_ed25519.pub
```

---

## PASSO 3: Usar o Cloud Sync

### 3.1 - Automático (recomendado):

O bot já sincroniza automaticamente:

```python
# No chart_data.py (já integrado)
df = provider.get_ohlcv_with_indicators('BTC/USDT', '5m')
# ↓ Sincroniza automaticamente com GitHub
```

### 3.2 - Manual (quando quiser):

```python
from cloud_sync import CloudSync

sync = CloudSync()

# Salvar dados
sync.save_live_data('BTC/USDT', '5m', dados)

# Sincronizar com GitHub
sync.sync_to_github("Dados LIVE sincronizados")

# Obter URL (para acessar de qualquer lugar)
url = sync.get_cloud_data_url('BTC/USDT', '5m')
print(url)
```

---

## PASSO 4: Acessar Dados de Qualquer Lugar

### Via Browser (direto no GitHub):
```
https://github.com/SEU_USUARIO/bot-trader/blob/main/cloud_data/BTC_USDT_5m.json
```

### Via Python (outro dispositivo):
```python
import requests
import json

url = "https://raw.githubusercontent.com/SEU_USUARIO/bot-trader/main/cloud_data/BTC_USDT_5m.json"
response = requests.get(url)
data = response.json()

print(f"Dados: {data['count']} velas")
print(f"Última atualização: {data['timestamp']}")
```

### Via Notebook/Celular:
1. Acesse: `https://github.com/SEU_USUARIO/bot-trader`
2. Pasta `cloud_data/`
3. Clique no arquivo JSON
4. Veja os dados (atualizados em tempo real)

---

## PASSO 5: Estrutura de Arquivos

Após sincronizar, você terá:

```
Bot Trader/
├── cloud_data/                    # Dados LIVE sincronizados
│   ├── BTC_USDT_5m.json          # Últimas 50 velas 5m
│   ├── BTC_USDT_1h.json          # Últimas 50 velas 1h
│   └── BTC_USDT_1d.json          # Últimas 50 velas 1d
│
├── bot_trader_gui_v2.py
├── chart_data.py                  # Integrado com cloud_sync
├── cloud_sync.py                  # Novo módulo
└── .gitignore                     # (importante!)
```

---

## PASSO 6: .gitignore (importante!)

Crie arquivo `.gitignore`:

```bash
# Não sincronize arquivos sensíveis
.env
*.log
__pycache__/
*.pyc
bot_dados.json          # Dados locais
config/                 # Configurações locais
*.db
.DS_Store
```

```bash
git add .gitignore
git commit -m "Add .gitignore"
git push
```

---

## TESTE RÁPIDO

```bash
# 1. Abra PowerShell
cd "c:\Users\lucas\Desktop\Bot Trader"

# 2. Teste o cloud sync
python -c "from cloud_sync import CloudSync; sync = CloudSync(); print(f'[OK] Cloud Sync pronto: {sync.data_dir}')"

# 3. Rode a GUI (sincroniza automaticamente)
python teste_simples.py

# 4. Verifique GitHub
# Vá para: https://github.com/SEU_USUARIO/bot-trader/tree/main/cloud_data
# Veja os JSONs sendo atualizados
```

---

## 📊 Exemplo de Dados Sincronizados

Arquivo: `cloud_data/BTC_USDT_5m.json`

```json
{
  "symbol": "BTC/USDT",
  "timeframe": "5m",
  "timestamp": "2025-10-24T15:30:00.123456",
  "count": 50,
  "data": [
    {
      "Date": "2025-10-24 15:25:00+00:00",
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
    ...
  ]
}
```

---

## ⚙️ Automação (Opcional)

Para sincronizar **cada 30 minutos** automaticamente:

### Windows - Usar Task Scheduler:

```batch
# sync_cloud.bat
@echo off
cd "c:\Users\lucas\Desktop\Bot Trader"
python -c "from cloud_sync import CloudSync; CloudSync().sync_to_github('Auto-sync dados LIVE')"
```

Agendar via Task Scheduler:
- `Ação → Criar Tarefa`
- `Gatilho: A cada 30 minutos`
- `Ação: Executar sync_cloud.bat`

---

## 🔐 Segurança

### Não sincronize:
- `.env` (API keys, secrets)
- Dados sensíveis
- Arquivos temporários

### Use `.gitignore`:
```
.env
*.key
*.secret
bot_dados_local.json
```

### Se vazou API key:
```bash
git filter-branch --force --index-filter 'git rm -r --cached --ignore-unmatch .env' --prune-empty --tag-name-filter cat -- --all
```

---

## 📱 Acessar de Celular/Notebook

### Opção 1: GitHub Web
- Link: `https://github.com/SEU_USUARIO/bot-trader`
- Pasta: `cloud_data/`
- Ver arquivo JSON

### Opção 2: Git Clone
```bash
git clone https://github.com/SEU_USUARIO/bot-trader.git
cd bot-trader
# Veja os dados em cloud_data/
```

### Opção 3: URL Raw (para integrar em apps)
```
https://raw.githubusercontent.com/SEU_USUARIO/bot-trader/main/cloud_data/BTC_USDT_5m.json
```

---

## 🆘 Troubleshooting

### "git: command not found"
```bash
# Instalar Git: https://git-scm.com/download/win
```

### "fatal: Not a git repository"
```bash
cd "c:\Users\lucas\Desktop\Bot Trader"
git init
git remote add origin https://github.com/SEU_USUARIO/bot-trader.git
```

### "Permission denied (publickey)"
```bash
# Configurar SSH keys ou usar HTTPS com token
git remote set-url origin https://github.com/SEU_USUARIO/bot-trader.git
```

### Dados não sincronizam
```bash
# Verificar status
git status

# Fazer commit manual
git add cloud_data/
git commit -m "Manual sync"
git push
```

---

## ✅ Checklist

- [ ] Repositório GitHub criado
- [ ] Git configurado localmente
- [ ] Credentials configuradas (SSH ou HTTPS)
- [ ] `.gitignore` criado e commitado
- [ ] Primeiro `git push` bem-sucedido
- [ ] `cloud_sync.py` em funcionamento
- [ ] Arquivos JSON aparecem em `cloud_data/`
- [ ] GitHub mostra arquivos atualizados
- [ ] URL raw funciona no browser
- [ ] Pode acessar de outro dispositivo

---

## 🎯 Próximos Passos

1. **Setup completo** (seguir passos acima)
2. **Testar sincronização** (rodara GUI e verificar GitHub)
3. **Acessar de outro dispositivo** (comprovar que funciona)
4. **Integrar com mobile app** (ler dados do GitHub em viagens)

---

**Dúvidas?** Me chama! 🚀
