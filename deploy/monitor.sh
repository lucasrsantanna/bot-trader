#!/bin/bash
#
# Script de Monitoramento - Bot Trader
# Verifica status, recursos e últimas operações
# Uso: ./monitor.sh
#

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Variáveis
SERVICE_NAME="bot-trader"
BOT_DIR="$HOME/bot-trader"
LOG_FILE="$BOT_DIR/logs/bot.log"
ERROR_LOG="$BOT_DIR/logs/bot-error.log"
DB_FILE="$BOT_DIR/bot_data.db"

# Função para printar header
print_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${CYAN}$1${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Header principal
clear
print_header "🤖 BOT TRADER - MONITOR"
echo -e "${BLUE}$(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo ""

# 1. Status do Serviço
print_header "📊 STATUS DO SERVIÇO"

if systemctl is-active --quiet $SERVICE_NAME; then
    echo -e "${GREEN}✅ Bot está RODANDO${NC}"

    # Tempo de uptime
    UPTIME=$(systemctl show $SERVICE_NAME --property=ActiveEnterTimestamp --value)
    echo -e "   Uptime desde: ${BLUE}$UPTIME${NC}"

    # Verificar se há erros recentes
    ERROR_COUNT=$(sudo journalctl -u $SERVICE_NAME --since "5 minutes ago" -p err | grep -c "error" || true)
    if [ $ERROR_COUNT -gt 0 ]; then
        echo -e "   ${YELLOW}⚠️  $ERROR_COUNT erros nos últimos 5min${NC}"
    fi
else
    echo -e "${RED}❌ Bot NÃO está rodando!${NC}"
    echo ""
    echo "🔄 Tentando reiniciar..."
    sudo systemctl restart $SERVICE_NAME
    sleep 2

    if systemctl is-active --quiet $SERVICE_NAME; then
        echo -e "${GREEN}✅ Bot reiniciado com sucesso${NC}"
    else
        echo -e "${RED}❌ Falha ao reiniciar! Verifique os logs.${NC}"
        echo ""
        echo "Últimas 10 linhas do erro:"
        sudo journalctl -u $SERVICE_NAME -n 10 --no-pager
        exit 1
    fi
fi

# 2. Recursos do Sistema
print_header "💻 RECURSOS DO SISTEMA"

# CPU e RAM do processo
if pgrep -f "python src/main.py" > /dev/null; then
    PROCESS_INFO=$(ps aux | grep "python src/main.py" | grep -v grep)
    CPU=$(echo $PROCESS_INFO | awk '{print $3}')
    RAM=$(echo $PROCESS_INFO | awk '{print $4}')
    PID=$(echo $PROCESS_INFO | awk '{print $2}')

    echo -e "   PID: ${BLUE}$PID${NC}"
    echo -e "   CPU: ${BLUE}$CPU%${NC}"
    echo -e "   RAM: ${BLUE}$RAM%${NC}"
else
    echo -e "${RED}   ❌ Processo Python não encontrado${NC}"
fi

echo ""

# Recursos totais do sistema
echo "   Sistema:"
TOTAL_MEM=$(free -h | awk '/^Mem:/ {print $2}')
USED_MEM=$(free -h | awk '/^Mem:/ {print $3}')
FREE_MEM=$(free -h | awk '/^Mem:/ {print $4}')
CPU_LOAD=$(uptime | awk -F'load average:' '{print $2}')

echo -e "   Memória: ${BLUE}$USED_MEM${NC} / $TOTAL_MEM (Livre: $FREE_MEM)"
echo -e "   CPU Load:${BLUE}$CPU_LOAD${NC}"

# Espaço em disco
DISK_USAGE=$(df -h $BOT_DIR | awk 'NR==2 {print $5}')
echo -e "   Disco: ${BLUE}$DISK_USAGE${NC} usado"

# 3. Último Log
print_header "📝 ÚLTIMAS OPERAÇÕES"

if [ -f "$LOG_FILE" ]; then
    echo "Últimas 8 linhas do log:"
    echo ""
    tail -n 8 "$LOG_FILE" | while IFS= read -r line; do
        # Colorir por nível de log
        if [[ $line == *"ERROR"* ]]; then
            echo -e "${RED}$line${NC}"
        elif [[ $line == *"WARNING"* ]]; then
            echo -e "${YELLOW}$line${NC}"
        elif [[ $line == *"INFO"* ]]; then
            echo -e "${GREEN}$line${NC}"
        else
            echo "$line"
        fi
    done
else
    echo -e "${YELLOW}⚠️  Log não encontrado: $LOG_FILE${NC}"
fi

# 4. Erros Recentes
if [ -f "$ERROR_LOG" ] && [ -s "$ERROR_LOG" ]; then
    print_header "⚠️  ERROS RECENTES"
    echo "Últimas 5 linhas do error.log:"
    echo ""
    tail -n 5 "$ERROR_LOG" | while IFS= read -r line; do
        echo -e "${RED}$line${NC}"
    done
fi

# 5. Database Stats
if [ -f "$DB_FILE" ]; then
    print_header "💾 ESTATÍSTICAS DO BANCO"

    # Verificar se sqlite3 está instalado
    if command -v sqlite3 &> /dev/null; then
        # Total de trades
        TOTAL_TRADES=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM trades;" 2>/dev/null || echo "0")
        echo -e "   Total de Trades: ${BLUE}$TOTAL_TRADES${NC}"

        # Total de sinais
        TOTAL_SIGNALS=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM signals;" 2>/dev/null || echo "0")
        echo -e "   Total de Sinais: ${BLUE}$TOTAL_SIGNALS${NC}"

        # Último trade (se houver)
        if [ "$TOTAL_TRADES" -gt 0 ]; then
            LAST_TRADE=$(sqlite3 "$DB_FILE" "SELECT symbol, type, pnl, pnl_percent FROM trades ORDER BY close_time DESC LIMIT 1;" 2>/dev/null)
            if [ ! -z "$LAST_TRADE" ]; then
                echo ""
                echo "   Último Trade:"
                SYMBOL=$(echo $LAST_TRADE | cut -d'|' -f1)
                TYPE=$(echo $LAST_TRADE | cut -d'|' -f2)
                PNL=$(echo $LAST_TRADE | cut -d'|' -f3)
                PNL_PCT=$(echo $LAST_TRADE | cut -d'|' -f4)

                if (( $(echo "$PNL > 0" | bc -l) )); then
                    echo -e "   ${GREEN}✅ $SYMBOL ($TYPE): +$PNL ($PNL_PCT%)${NC}"
                else
                    echo -e "   ${RED}❌ $SYMBOL ($TYPE): $PNL ($PNL_PCT%)${NC}"
                fi
            fi
        fi

        # Win Rate (se houver trades)
        if [ "$TOTAL_TRADES" -gt 5 ]; then
            WIN_RATE=$(sqlite3 "$DB_FILE" "SELECT ROUND(AVG(CASE WHEN pnl > 0 THEN 1.0 ELSE 0.0 END) * 100, 2) FROM trades;" 2>/dev/null || echo "0")
            echo -e "   Win Rate: ${BLUE}$WIN_RATE%${NC}"
        fi
    else
        echo -e "${YELLOW}   sqlite3 não instalado. Para ver stats: sudo apt install sqlite3${NC}"
    fi

    # Tamanho do DB
    DB_SIZE=$(du -h "$DB_FILE" | cut -f1)
    echo -e "   Tamanho DB: ${BLUE}$DB_SIZE${NC}"
fi

# 6. Conexão com Binance
print_header "🌐 CONECTIVIDADE"

# Ping Binance API
if ping -c 1 api.binance.com &> /dev/null; then
    echo -e "${GREEN}✅ Conexão com Binance OK${NC}"
else
    echo -e "${RED}❌ Sem conexão com Binance!${NC}"
fi

# 7. Resumo Final
print_header "✅ RESUMO"

if systemctl is-active --quiet $SERVICE_NAME; then
    echo -e "${GREEN}✅ Bot operacional${NC}"
else
    echo -e "${RED}❌ Bot com problemas${NC}"
fi

echo ""
echo "Comandos úteis:"
echo "  Ver logs ao vivo:    sudo journalctl -u bot-trader -f"
echo "  Reiniciar bot:       sudo systemctl restart bot-trader"
echo "  Ver logs completos:  tail -f $LOG_FILE"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
