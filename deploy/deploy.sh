#!/bin/bash
#
# Script de Deploy Automático - Bot Trader VPS
# Uso: ./deploy.sh
#

set -e  # Parar em caso de erro

echo "🚀 Iniciando deploy do Bot Trader..."
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se está rodando como root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}❌ Não execute como root! Use o usuário bottrader${NC}"
    exit 1
fi

# Variáveis
BOT_DIR="$HOME/bot-trader"
VENV_DIR="$BOT_DIR/venv"
LOG_DIR="$BOT_DIR/logs"
SERVICE_NAME="bot-trader"

# 1. Verificar dependências
echo "📦 Verificando dependências..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 não encontrado!${NC}"
    echo "Instale com: sudo apt install python3 python3-venv python3-pip"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git não encontrado!${NC}"
    echo "Instale com: sudo apt install git"
    exit 1
fi

echo -e "${GREEN}✅ Dependências OK${NC}"
echo ""

# 2. Clonar/Atualizar repositório
if [ ! -d "$BOT_DIR" ]; then
    echo "📥 Clonando repositório..."
    cd ~
    git clone https://github.com/lucasrsantanna/bot-trader.git
    cd "$BOT_DIR"
else
    echo "🔄 Atualizando repositório..."
    cd "$BOT_DIR"

    # Salvar mudanças locais (se houver)
    if [ -f ".env" ]; then
        cp .env .env.backup
        echo "💾 Backup do .env criado"
    fi

    git stash
    git pull origin main
    git stash pop || true

    # Restaurar .env se foi backupeado
    if [ -f ".env.backup" ]; then
        mv .env.backup .env
        echo "✅ .env restaurado"
    fi
fi

echo -e "${GREEN}✅ Código atualizado${NC}"
echo ""

# 3. Criar ambiente virtual
if [ ! -d "$VENV_DIR" ]; then
    echo "🐍 Criando ambiente virtual..."
    python3 -m venv venv
else
    echo "🐍 Ambiente virtual já existe"
fi

echo -e "${GREEN}✅ Virtual env OK${NC}"
echo ""

# 4. Ativar venv e instalar dependências
echo "📚 Instalando dependências..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo -e "${GREEN}✅ Dependências instaladas${NC}"
echo ""

# 5. Criar diretório de logs
mkdir -p "$LOG_DIR"
echo -e "${GREEN}✅ Diretório de logs criado${NC}"
echo ""

# 6. Verificar .env
if [ ! -f "$BOT_DIR/.env" ]; then
    echo -e "${YELLOW}⚠️  Arquivo .env não encontrado!${NC}"
    echo ""
    echo "Criando .env a partir do exemplo..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais!${NC}"
    echo "Execute: nano $BOT_DIR/.env"
    echo ""
    read -p "Pressione ENTER depois de configurar o .env..."
fi

# Verificar se .env tem as chaves necessárias
if ! grep -q "BINANCE_API_KEY" .env || ! grep -q "BINANCE_SECRET_KEY" .env; then
    echo -e "${RED}❌ .env não configurado corretamente!${NC}"
    echo "Configure BINANCE_API_KEY e BINANCE_SECRET_KEY no .env"
    exit 1
fi

echo -e "${GREEN}✅ .env configurado${NC}"
echo ""

# 7. Testar execução
echo "🧪 Testando execução do bot..."
timeout 10s python src/main.py || {
    if [ $? -eq 124 ]; then
        echo -e "${GREEN}✅ Bot inicializado com sucesso (timeout esperado)${NC}"
    else
        echo -e "${RED}❌ Erro ao inicializar bot!${NC}"
        echo "Verifique os logs acima"
        exit 1
    fi
}
echo ""

# 8. Instalar systemd service
echo "⚙️  Configurando systemd service..."

# Copiar service file
sudo cp deploy/bot-trader.service /etc/systemd/system/

# Substituir username se necessário
sudo sed -i "s/bottrader/$USER/g" /etc/systemd/system/bot-trader.service

# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar service
sudo systemctl enable bot-trader

echo -e "${GREEN}✅ Systemd service instalado${NC}"
echo ""

# 9. Perguntar se deseja iniciar o bot
read -p "🚀 Deseja iniciar o bot agora? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo systemctl restart bot-trader
    sleep 2

    # Verificar status
    if sudo systemctl is-active --quiet bot-trader; then
        echo -e "${GREEN}✅ Bot iniciado com sucesso!${NC}"
        echo ""
        echo "📊 Status:"
        sudo systemctl status bot-trader --no-pager -l
    else
        echo -e "${RED}❌ Erro ao iniciar bot!${NC}"
        echo "Verifique os logs: sudo journalctl -u bot-trader -n 50"
        exit 1
    fi
else
    echo "Bot não iniciado. Para iniciar: sudo systemctl start bot-trader"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Deploy completo!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Comandos úteis:"
echo ""
echo "  Ver logs em tempo real:"
echo "    sudo journalctl -u bot-trader -f"
echo ""
echo "  Ver status:"
echo "    sudo systemctl status bot-trader"
echo ""
echo "  Reiniciar bot:"
echo "    sudo systemctl restart bot-trader"
echo ""
echo "  Parar bot:"
echo "    sudo systemctl stop bot-trader"
echo ""
echo "  Ver logs de arquivo:"
echo "    tail -f ~/bot-trader/logs/bot.log"
echo ""
echo "  Monitorar recursos:"
echo "    ~/bot-trader/deploy/monitor.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

deactivate  # Desativar venv
