# 🚀 Deploy Scripts - Bot Trader

Scripts para deploy e gerenciamento do bot em VPS Linux.

---

## 📁 Arquivos

### 1. `deploy.sh` - Script de Deploy Automático
**Uso:**
```bash
bash deploy.sh
```

**O que faz:**
- ✅ Clona/atualiza repositório
- ✅ Cria ambiente virtual Python
- ✅ Instala dependências
- ✅ Configura systemd service
- ✅ Testa execução
- ✅ Inicia o bot (opcional)

**Requisitos:**
- Ubuntu 22.04 ou Debian 12
- Python 3.10+
- Git
- Acesso sudo

---

### 2. `bot-trader.service` - Systemd Service
**Uso:**
```bash
# Copiar manualmente (ou usar deploy.sh)
sudo cp bot-trader.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bot-trader
sudo systemctl start bot-trader
```

**Recursos:**
- ✅ Auto-restart em caso de crash
- ✅ Logs estruturados
- ✅ Inicia automaticamente no boot
- ✅ Proteções de segurança

**Comandos:**
```bash
# Status
sudo systemctl status bot-trader

# Logs em tempo real
sudo journalctl -u bot-trader -f

# Reiniciar
sudo systemctl restart bot-trader

# Parar
sudo systemctl stop bot-trader

# Desabilitar auto-start
sudo systemctl disable bot-trader
```

---

### 3. `monitor.sh` - Script de Monitoramento
**Uso:**
```bash
bash monitor.sh
```

**O que mostra:**
- ✅ Status do serviço (rodando/parado)
- ✅ Uso de CPU e RAM
- ✅ Últimas 8 linhas do log
- ✅ Erros recentes
- ✅ Estatísticas do banco (trades, sinais, win rate)
- ✅ Conectividade com Binance

**Auto-restart:**
Se detectar que o bot parou, tenta reiniciar automaticamente.

**Agendamento (opcional):**
```bash
# Rodar a cada 5 minutos
crontab -e

# Adicionar:
*/5 * * * * /home/bottrader/bot-trader/deploy/monitor.sh >> /home/bottrader/bot-trader/logs/monitor.log 2>&1
```

---

### 4. `backup.sh` - Script de Backup
**Uso:**
```bash
# Backup manual
bash backup.sh manual

# Backup automático (limpa backups antigos)
bash backup.sh auto
```

**O que faz backup:**
- ✅ `bot_data.db` - Banco de dados SQLite
- ✅ `bot_dados.json` - Arquivo de estado (se existir)
- ✅ `logs/` - Logs do bot
- ✅ `.env` - Configurações (protegido com chmod 600)

**Localização dos backups:**
```
~/bot-trader-backups/
├── bot_data_20251010_143022.db
├── bot_dados_20251010_143022.json
├── logs_20251010_143022.tar.gz
├── .env_20251010_143022
└── backup.log
```

**Retenção:**
- Database/JSON: 30 dias
- Logs: 30 dias
- .env: últimos 7 backups

**Agendamento (recomendado):**
```bash
crontab -e

# Backup diário às 3h da manhã
0 3 * * * /home/bottrader/bot-trader/deploy/backup.sh auto >> /home/bottrader/bot-trader/logs/backup.log 2>&1
```

**Recuperar backup:**
```bash
# 1. Parar bot
sudo systemctl stop bot-trader

# 2. Restaurar DB
cp ~/bot-trader-backups/bot_data_YYYYMMDD_HHMMSS.db ~/bot-trader/bot_data.db

# 3. Reiniciar
sudo systemctl start bot-trader
```

---

## 🚀 Quick Start - Deploy Completo

### Passo 1: Criar VPS
- Provider: DigitalOcean, Vultr, Contabo
- OS: Ubuntu 22.04 LTS
- RAM: 1GB mínimo
- Criar usuário `bottrader`

### Passo 2: Conectar e Preparar
```bash
# SSH no VPS
ssh root@SEU_IP

# Criar usuário
adduser bottrader
usermod -aG sudo bottrader
su - bottrader

# Atualizar sistema
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-venv python3-pip sqlite3
```

### Passo 3: Deploy
```bash
# Baixar apenas o script de deploy
curl -o deploy.sh https://raw.githubusercontent.com/lucasrsantanna/bot-trader/main/deploy/deploy.sh
chmod +x deploy.sh

# Executar deploy
bash deploy.sh
```

### Passo 4: Configurar .env
```bash
nano ~/bot-trader/.env

# Adicionar:
BINANCE_API_KEY=sua_chave
BINANCE_SECRET_KEY=sua_secret
USE_TESTNET=true
TELEGRAM_BOT_TOKEN=seu_token  # Opcional
TELEGRAM_CHAT_ID=seu_chat_id  # Opcional
```

### Passo 5: Verificar
```bash
# Status
sudo systemctl status bot-trader

# Logs
sudo journalctl -u bot-trader -f

# Monitor
bash ~/bot-trader/deploy/monitor.sh
```

---

## 📊 Monitoramento Contínuo

### Setup Completo de Monitoramento

```bash
# 1. Tornar scripts executáveis
cd ~/bot-trader/deploy
chmod +x deploy.sh monitor.sh backup.sh

# 2. Configurar cron jobs
crontab -e
```

**Adicionar:**
```bash
# Monitorar a cada 5 minutos
*/5 * * * * /home/bottrader/bot-trader/deploy/monitor.sh >> /home/bottrader/bot-trader/logs/monitor.log 2>&1

# Backup diário às 3h
0 3 * * * /home/bottrader/bot-trader/deploy/backup.sh auto >> /home/bottrader/bot-trader/logs/backup.log 2>&1

# Limpar logs antigos (>30 dias) toda segunda às 4h
0 4 * * 1 find /home/bottrader/bot-trader/logs -name "*.log" -mtime +30 -delete
```

---

## 🔒 Segurança

### Firewall (UFW)
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp  # SSH
sudo ufw enable
```

### SSH Hardening
```bash
sudo nano /etc/ssh/sshd_config

# Configurar:
PermitRootLogin no
PasswordAuthentication no  # Apenas SSH key
Port 2222  # Porta customizada (opcional)

sudo systemctl restart sshd
```

### Fail2Ban
```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 🛠️ Troubleshooting

### Bot não inicia
```bash
# Ver erro específico
sudo journalctl -u bot-trader -n 50

# Testar manualmente
cd ~/bot-trader
source venv/bin/activate
python src/main.py
```

### Dependências faltando
```bash
cd ~/bot-trader
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Database corrompido
```bash
# Verificar integridade
sqlite3 ~/bot-trader/bot_data.db "PRAGMA integrity_check;"

# Se corrompido, restaurar backup
sudo systemctl stop bot-trader
cp ~/bot-trader-backups/bot_data_LATEST.db ~/bot-trader/bot_data.db
sudo systemctl start bot-trader
```

### Bot travando
```bash
# Ver uso de recursos
htop

# Ver logs
tail -f ~/bot-trader/logs/bot.log

# Reiniciar
sudo systemctl restart bot-trader
```

---

## 📝 Logs

### Localizações
- **Systemd logs:** `sudo journalctl -u bot-trader -f`
- **Bot logs:** `~/bot-trader/logs/bot.log`
- **Error logs:** `~/bot-trader/logs/bot-error.log`
- **Monitor logs:** `~/bot-trader/logs/monitor.log`
- **Backup logs:** `~/bot-trader/logs/backup.log`

### Ver logs específicos
```bash
# Última hora
sudo journalctl -u bot-trader --since "1 hour ago"

# Hoje
sudo journalctl -u bot-trader --since today

# Apenas erros
sudo journalctl -u bot-trader -p err

# Seguir em tempo real
sudo journalctl -u bot-trader -f
```

---

## 🔄 Atualizar Bot

```bash
# Método 1: Via git (recomendado)
cd ~/bot-trader
sudo systemctl stop bot-trader
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl start bot-trader

# Método 2: Re-executar deploy.sh
bash ~/bot-trader/deploy/deploy.sh
```

---

## 📱 Integração Telegram

**Após configurar TELEGRAM_BOT_TOKEN no .env:**

```bash
# Testar notificação
cd ~/bot-trader
source venv/bin/activate
python -c "from src.utils.notifications import notifier; notifier.send_message('✅ Bot VPS ativo!')"
```

Você receberá notificações automáticas:
- 🟢 Trade aberto
- 🔴 Trade fechado
- 🔵 Sinais da IA
- ⚠️ Erros críticos

---

## ✅ Checklist Pós-Deploy

- [ ] Bot iniciado: `sudo systemctl status bot-trader`
- [ ] Logs sendo gerados: `ls -lh ~/bot-trader/logs/`
- [ ] Database criado: `ls -lh ~/bot-trader/bot_data.db`
- [ ] Cron jobs configurados: `crontab -l`
- [ ] Firewall ativo: `sudo ufw status`
- [ ] Telegram funcionando (se configurado)
- [ ] Backup manual testado: `bash backup.sh manual`
- [ ] Monitor funcionando: `bash monitor.sh`
- [ ] Bot rodando por 24h sem crash

---

## 🎯 Próximos Passos

1. **Monitorar por 48h** - Verificar estabilidade
2. **Analisar primeiros trades** - Win rate, P&L
3. **Ajustar configurações** - RSI, stop-loss, etc
4. **Coletar dados** - 100+ trades para análise
5. **Considerar produção** - Sair do testnet

---

**Criado por:** Claude Code
**Baseado em:** Recomendações Manus AI
**Versão:** 1.0 - Fase 4 VPS Deployment
