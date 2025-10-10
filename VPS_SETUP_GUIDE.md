# 🚀 Guia Completo: Deploy VPS 24/7

**Objetivo:** Configurar o bot para rodar 24/7 em um servidor VPS Linux.

---

## 📋 ÍNDICE

1. [Escolha do VPS](#1-escolha-do-vps)
2. [Configuração Inicial](#2-configuração-inicial)
3. [Instalação de Dependências](#3-instalação-de-dependências)
4. [Deploy do Bot](#4-deploy-do-bot)
5. [Systemd Service](#5-systemd-service)
6. [Monitoramento](#6-monitoramento)
7. [Segurança](#7-segurança)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Escolha do VPS

### 🏆 Recomendações

| Provider | Plano | RAM | CPU | Preço/mês | Link |
|----------|-------|-----|-----|-----------|------|
| **DigitalOcean** | Basic Droplet | 1GB | 1 vCPU | $6 | digitalocean.com |
| **Vultr** | Regular Performance | 1GB | 1 vCPU | $6 | vultr.com |
| **Contabo** | Cloud VPS S | 4GB | 2 vCPU | €5 (~$5.50) | contabo.com |
| **AWS Lightsail** | $3.50 plan | 512MB | 1 vCPU | $3.50 | aws.amazon.com/lightsail |

### ✅ Requisitos Mínimos
- **RAM:** 512MB (recomendado 1GB)
- **CPU:** 1 vCPU
- **Storage:** 10GB SSD
- **OS:** Ubuntu 22.04 LTS ou Debian 12
- **Rede:** 1TB tráfego/mês

### 💡 Nossa Recomendação
**DigitalOcean Basic Droplet ($6/mês)**
- Interface simples
- Boa documentação
- SSH fácil de configurar
- $200 em créditos grátis para novos usuários

---

## 2. Configuração Inicial

### 2.1 Criar VPS

**DigitalOcean:**
1. Acesse https://digitalocean.com
2. Create → Droplets
3. Escolha:
   - **Image:** Ubuntu 22.04 LTS
   - **Plan:** Basic ($6/mês)
   - **Datacenter:** Escolha o mais próximo (ex: São Paulo, NYC)
   - **Authentication:** SSH Key (mais seguro) ou Password
4. Create Droplet

### 2.2 Conectar via SSH

```bash
# Conectar ao VPS (substituir IP pelo seu)
ssh root@SEU_IP_VPS

# Se usar SSH key
ssh -i ~/.ssh/sua_chave root@SEU_IP_VPS
```

### 2.3 Atualizar Sistema

```bash
# Atualizar pacotes
sudo apt update && sudo apt upgrade -y

# Instalar utilitários
sudo apt install -y curl wget git vim htop
```

### 2.4 Criar Usuário (Segurança)

```bash
# Criar usuário bot (não rodar como root!)
sudo adduser bottrader

# Adicionar ao grupo sudo
sudo usermod -aG sudo bottrader

# Trocar para o usuário
su - bottrader
```

---

## 3. Instalação de Dependências

### 3.1 Python 3.11

```bash
# Verificar versão do Python
python3 --version

# Se < 3.10, instalar Python 3.11
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# Definir Python 3.11 como padrão
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
```

### 3.2 Git

```bash
# Já instalado no passo 2.3
git --version
```

### 3.3 Pip

```bash
sudo apt install -y python3-pip
pip3 --version
```

---

## 4. Deploy do Bot

### 4.1 Clonar Repositório

```bash
# Navegar para home
cd ~

# Clonar repo (substituir pela sua URL)
git clone https://github.com/lucasrsantanna/bot-trader.git

# Entrar no diretório
cd bot-trader
```

### 4.2 Criar Ambiente Virtual

```bash
# Criar venv
python3 -m venv venv

# Ativar venv
source venv/bin/activate

# Verificar
which python  # Deve mostrar /home/bottrader/bot-trader/venv/bin/python
```

### 4.3 Instalar Dependências

```bash
# Instalar requirements
pip install -r requirements.txt

# Verificar instalação
pip list
```

### 4.4 Configurar .env

```bash
# Copiar exemplo
cp .env.example .env

# Editar com suas credenciais
nano .env
```

**Configurar:**
```env
# Binance API
BINANCE_API_KEY=sua_api_key_aqui
BINANCE_SECRET_KEY=sua_secret_key_aqui
USE_TESTNET=true  # ou false para produção

# Telegram (opcional)
TELEGRAM_BOT_TOKEN=seu_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui

# Alpha Vantage (se usar)
ALPHA_VANTAGE_API_KEY=sua_key_aqui
```

**Salvar:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 4.5 Testar Execução Manual

```bash
# Ativar venv se não estiver ativo
source venv/bin/activate

# Rodar bot
python src/main.py

# Deve ver:
# - "CryptoBot inicializado"
# - "Atualizando dados de mercado..."
# - Logs de operação
```

**Testar por 2-3 minutos e parar:** `Ctrl+C`

---

## 5. Systemd Service

### 5.1 Criar Service File

```bash
# Criar arquivo de serviço
sudo nano /etc/systemd/system/bot-trader.service
```

**Conteúdo:**
```ini
[Unit]
Description=Crypto Trading Bot
After=network.target

[Service]
Type=simple
User=bottrader
WorkingDirectory=/home/bottrader/bot-trader
Environment="PATH=/home/bottrader/bot-trader/venv/bin"
ExecStart=/home/bottrader/bot-trader/venv/bin/python src/main.py
Restart=always
RestartSec=10
StandardOutput=append:/home/bottrader/bot-trader/logs/bot.log
StandardError=append:/home/bottrader/bot-trader/logs/bot-error.log

[Install]
WantedBy=multi-user.target
```

**Salvar:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 5.2 Criar Diretório de Logs

```bash
mkdir -p ~/bot-trader/logs
```

### 5.3 Habilitar e Iniciar Service

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar para iniciar no boot
sudo systemctl enable bot-trader

# Iniciar serviço
sudo systemctl start bot-trader

# Verificar status
sudo systemctl status bot-trader
```

**Deve aparecer:** `Active: active (running)`

### 5.4 Comandos Úteis

```bash
# Ver logs em tempo real
sudo journalctl -u bot-trader -f

# Ver últimas 100 linhas
sudo journalctl -u bot-trader -n 100

# Parar bot
sudo systemctl stop bot-trader

# Reiniciar bot
sudo systemctl restart bot-trader

# Verificar status
sudo systemctl status bot-trader

# Ver arquivo de log
tail -f ~/bot-trader/logs/bot.log
```

---

## 6. Monitoramento

### 6.1 Script de Monitoramento

Criar script para verificar se bot está rodando:

```bash
nano ~/bot-trader/monitor.sh
```

**Conteúdo:**
```bash
#!/bin/bash

# Verificar se serviço está ativo
if systemctl is-active --quiet bot-trader; then
    echo "✅ Bot está rodando"

    # Verificar uso de recursos
    echo ""
    echo "📊 Recursos:"
    ps aux | grep "python src/main.py" | grep -v grep | awk '{print "CPU: "$3"% | RAM: "$4"% | PID: "$2}'

    # Últimas 5 linhas do log
    echo ""
    echo "📝 Últimas operações:"
    tail -n 5 ~/bot-trader/logs/bot.log
else
    echo "❌ Bot NÃO está rodando!"
    echo "Tentando reiniciar..."
    sudo systemctl restart bot-trader
fi
```

**Tornar executável:**
```bash
chmod +x ~/bot-trader/monitor.sh
```

**Executar:**
```bash
~/bot-trader/monitor.sh
```

### 6.2 Cron para Monitoramento Automático

```bash
# Editar crontab
crontab -e
```

**Adicionar (verifica a cada 5 minutos):**
```bash
*/5 * * * * /home/bottrader/bot-trader/monitor.sh >> /home/bottrader/bot-trader/logs/monitor.log 2>&1
```

### 6.3 Script de Backup Diário

```bash
nano ~/bot-trader/backup.sh
```

**Conteúdo:**
```bash
#!/bin/bash

BACKUP_DIR=~/bot-trader-backups
DATE=$(date +%Y%m%d_%H%M%S)

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# Backup do banco de dados
if [ -f ~/bot-trader/bot_data.db ]; then
    cp ~/bot-trader/bot_data.db $BACKUP_DIR/bot_data_$DATE.db
    echo "✅ Backup DB: bot_data_$DATE.db"
fi

# Backup do arquivo de dados
if [ -f ~/bot-trader/bot_dados.json ]; then
    cp ~/bot-trader/bot_dados.json $BACKUP_DIR/bot_dados_$DATE.json
    echo "✅ Backup JSON: bot_dados_$DATE.json"
fi

# Remover backups com mais de 7 dias
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.json" -mtime +7 -delete

echo "✅ Backup completo!"
```

**Tornar executável:**
```bash
chmod +x ~/bot-trader/backup.sh
```

**Adicionar ao crontab (backup diário às 3h):**
```bash
crontab -e
```

**Adicionar:**
```bash
0 3 * * * /home/bottrader/bot-trader/backup.sh >> /home/bottrader/bot-trader/logs/backup.log 2>&1
```

---

## 7. Segurança

### 7.1 Firewall (UFW)

```bash
# Instalar UFW
sudo apt install -y ufw

# Configurar regras
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 8501/tcp  # Se usar Streamlit dashboard

# Ativar firewall
sudo ufw enable

# Verificar status
sudo ufw status
```

### 7.2 SSH Hardening

```bash
# Editar config SSH
sudo nano /etc/ssh/sshd_config
```

**Modificar:**
```bash
# Desabilitar login root
PermitRootLogin no

# Desabilitar autenticação por senha (apenas SSH key)
PasswordAuthentication no

# Mudar porta SSH (opcional, ex: 2222)
Port 2222
```

**Reiniciar SSH:**
```bash
sudo systemctl restart sshd
```

### 7.3 Fail2Ban

```bash
# Instalar Fail2Ban (protege contra brute force)
sudo apt install -y fail2ban

# Criar configuração
sudo nano /etc/fail2ban/jail.local
```

**Conteúdo:**
```ini
[sshd]
enabled = true
port = 2222
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```

**Iniciar:**
```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 7.4 Permissões do .env

```bash
# .env deve ter permissões restritas
chmod 600 ~/bot-trader/.env
```

---

## 8. Troubleshooting

### Bot não inicia

```bash
# Verificar logs de erro
sudo journalctl -u bot-trader -n 50

# Verificar se .env existe
ls -la ~/bot-trader/.env

# Testar manualmente
cd ~/bot-trader
source venv/bin/activate
python src/main.py
```

### Erro de dependências

```bash
# Reinstalar requirements
cd ~/bot-trader
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Bot travando/crashando

```bash
# Verificar memória
free -h

# Verificar CPU
htop

# Ver logs
tail -f ~/bot-trader/logs/bot.log

# Aumentar RestartSec no service
sudo nano /etc/systemd/system/bot-trader.service
# Mudar RestartSec=10 para RestartSec=30
sudo systemctl daemon-reload
sudo systemctl restart bot-trader
```

### Não conecta à Binance

```bash
# Verificar conectividade
ping api.binance.com

# Verificar se API keys estão corretas
cat ~/bot-trader/.env | grep BINANCE

# Testar API manualmente
python3 -c "import ccxt; exchange = ccxt.binance(); print(exchange.fetch_ticker('BTC/USDT'))"
```

### Database corrompido

```bash
# Verificar integridade
sqlite3 ~/bot-trader/bot_data.db "PRAGMA integrity_check;"

# Se corrompido, restaurar backup
cp ~/bot-trader-backups/bot_data_YYYYMMDD_HHMMSS.db ~/bot-trader/bot_data.db
sudo systemctl restart bot-trader
```

---

## 9. Atualizar Bot

```bash
# Parar bot
sudo systemctl stop bot-trader

# Pull mudanças
cd ~/bot-trader
git pull origin main

# Atualizar dependências
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Reiniciar bot
sudo systemctl start bot-trader

# Verificar
sudo systemctl status bot-trader
```

---

## 10. Comandos Rápidos

```bash
# Status
sudo systemctl status bot-trader

# Logs em tempo real
sudo journalctl -u bot-trader -f

# Reiniciar
sudo systemctl restart bot-trader

# Parar
sudo systemctl stop bot-trader

# Iniciar
sudo systemctl start bot-trader

# Monitorar recursos
~/bot-trader/monitor.sh

# Backup manual
~/bot-trader/backup.sh

# Ver últimas 20 linhas do log
tail -n 20 ~/bot-trader/logs/bot.log
```

---

## ✅ Checklist Pós-Deploy

- [ ] VPS criado e conectado via SSH
- [ ] Python 3.11 instalado
- [ ] Repositório clonado
- [ ] Dependências instaladas
- [ ] .env configurado
- [ ] Bot testado manualmente
- [ ] Systemd service criado e ativo
- [ ] Logs sendo gerados corretamente
- [ ] Firewall configurado
- [ ] SSH hardening aplicado
- [ ] Fail2Ban instalado
- [ ] Script de monitoramento funcionando
- [ ] Backup diário agendado
- [ ] Telegram recebendo notificações (se configurado)
- [ ] Bot rodando por 24h sem crash

---

## 📊 Custos Mensais Estimados

- **VPS:** $6/mês (DigitalOcean)
- **Binance API:** Grátis
- **Telegram:** Grátis
- **Total:** **$6/mês**

---

## 🎯 Próximos Passos Após Deploy

1. **Monitorar por 48h** - Verificar se não há crashes
2. **Analisar primeiros trades** - Win rate, P&L
3. **Ajustar parâmetros** - Se necessário
4. **Considerar produção** - Após 100+ trades em testnet

---

**🏆 Deploy VPS Completo!**
Bot rodando 24/7, monitorado, com backup e seguro.
