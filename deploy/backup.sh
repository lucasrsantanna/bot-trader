#!/bin/bash
#
# Script de Backup - Bot Trader
# Faz backup do banco de dados e arquivos de configuração
# Uso: ./backup.sh [manual|auto]
#

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Variáveis
BOT_DIR="$HOME/bot-trader"
BACKUP_DIR="$HOME/bot-trader-backups"
DATE=$(date +%Y%m%d_%H%M%S)
MODE=${1:-manual}

# Criar diretório de backup
mkdir -p "$BACKUP_DIR"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}💾 BACKUP BOT TRADER${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Modo: $MODE"
echo ""

BACKUP_COUNT=0

# 1. Backup do banco de dados
if [ -f "$BOT_DIR/bot_data.db" ]; then
    echo -n "Backup DB... "
    cp "$BOT_DIR/bot_data.db" "$BACKUP_DIR/bot_data_$DATE.db"
    echo -e "${GREEN}✅${NC} bot_data_$DATE.db"
    ((BACKUP_COUNT++))
else
    echo -e "${YELLOW}⚠️  bot_data.db não encontrado${NC}"
fi

# 2. Backup do arquivo JSON (se existir)
if [ -f "$BOT_DIR/bot_dados.json" ]; then
    echo -n "Backup JSON... "
    cp "$BOT_DIR/bot_dados.json" "$BACKUP_DIR/bot_dados_$DATE.json"
    echo -e "${GREEN}✅${NC} bot_dados_$DATE.json"
    ((BACKUP_COUNT++))
fi

# 3. Backup dos logs (últimos 7 dias)
if [ -d "$BOT_DIR/logs" ]; then
    echo -n "Backup Logs... "
    tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" -C "$BOT_DIR" logs/ 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅${NC} logs_$DATE.tar.gz"
        ((BACKUP_COUNT++))
    else
        echo -e "${YELLOW}⚠️  Nenhum log para fazer backup${NC}"
    fi
fi

# 4. Backup do .env (importante!)
if [ -f "$BOT_DIR/.env" ]; then
    echo -n "Backup .env... "
    cp "$BOT_DIR/.env" "$BACKUP_DIR/.env_$DATE"
    # Proteger arquivo de configuração
    chmod 600 "$BACKUP_DIR/.env_$DATE"
    echo -e "${GREEN}✅${NC} .env_$DATE"
    ((BACKUP_COUNT++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ $BACKUP_COUNT arquivos salvos em backup${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 5. Limpar backups antigos (manter últimos 30 dias)
RETENTION_DAYS=30

if [ "$MODE" = "auto" ]; then
    echo "🧹 Limpando backups com mais de $RETENTION_DAYS dias..."

    DELETED=0

    # Deletar DBs antigos
    DELETED_DB=$(find "$BACKUP_DIR" -name "bot_data_*.db" -mtime +$RETENTION_DAYS -delete -print | wc -l)
    ((DELETED+=DELETED_DB))

    # Deletar JSONs antigos
    DELETED_JSON=$(find "$BACKUP_DIR" -name "bot_dados_*.json" -mtime +$RETENTION_DAYS -delete -print | wc -l)
    ((DELETED+=DELETED_JSON))

    # Deletar logs antigos
    DELETED_LOGS=$(find "$BACKUP_DIR" -name "logs_*.tar.gz" -mtime +$RETENTION_DAYS -delete -print | wc -l)
    ((DELETED+=DELETED_LOGS))

    # Deletar .env antigos (manter apenas últimos 7)
    ENV_COUNT=$(ls -1 "$BACKUP_DIR"/.env_* 2>/dev/null | wc -l)
    if [ $ENV_COUNT -gt 7 ]; then
        ls -1t "$BACKUP_DIR"/.env_* | tail -n +8 | xargs rm -f
        DELETED_ENV=$((ENV_COUNT - 7))
        ((DELETED+=DELETED_ENV))
    fi

    if [ $DELETED -gt 0 ]; then
        echo -e "${GREEN}✅ $DELETED backups antigos removidos${NC}"
    else
        echo "✅ Nenhum backup antigo para remover"
    fi
    echo ""
fi

# 6. Estatísticas dos backups
echo "📊 ESTATÍSTICAS DE BACKUP"
echo ""

TOTAL_BACKUPS=$(ls -1 "$BACKUP_DIR" | wc -l)
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)

echo "   Total de arquivos: $TOTAL_BACKUPS"
echo "   Espaço usado: $BACKUP_SIZE"
echo ""

# Listar últimos 5 backups de DB
if ls "$BACKUP_DIR"/bot_data_*.db 1> /dev/null 2>&1; then
    echo "   Últimos 5 backups de DB:"
    ls -1t "$BACKUP_DIR"/bot_data_*.db | head -5 | while read file; do
        SIZE=$(du -h "$file" | cut -f1)
        NAME=$(basename "$file")
        echo "     - $NAME ($SIZE)"
    done
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 7. Instruções de recuperação
if [ "$MODE" = "manual" ]; then
    echo "💡 COMO RECUPERAR UM BACKUP:"
    echo ""
    echo "   1. Parar o bot:"
    echo "      sudo systemctl stop bot-trader"
    echo ""
    echo "   2. Restaurar database:"
    echo "      cp $BACKUP_DIR/bot_data_YYYYMMDD_HHMMSS.db $BOT_DIR/bot_data.db"
    echo ""
    echo "   3. Reiniciar bot:"
    echo "      sudo systemctl start bot-trader"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
fi

# 8. Verificar integridade do DB (se sqlite3 instalado)
if command -v sqlite3 &> /dev/null && [ -f "$BOT_DIR/bot_data.db" ]; then
    echo "🔍 Verificando integridade do banco..."
    INTEGRITY=$(sqlite3 "$BOT_DIR/bot_data.db" "PRAGMA integrity_check;" 2>&1)

    if [ "$INTEGRITY" = "ok" ]; then
        echo -e "${GREEN}✅ Database íntegro${NC}"
    else
        echo -e "${YELLOW}⚠️  Possível problema no database:${NC}"
        echo "$INTEGRITY"
        echo ""
        echo "Considere restaurar um backup recente"
    fi
    echo ""
fi

# 9. Log do backup
echo "$(date '+%Y-%m-%d %H:%M:%S') - Backup $MODE - $BACKUP_COUNT arquivos" >> "$BACKUP_DIR/backup.log"

exit 0
