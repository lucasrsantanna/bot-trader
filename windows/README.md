# 💻 Scripts Windows - Bot Trader 24/7

Scripts para rodar o bot 24/7 localmente no Windows.

---

## 📁 Arquivos

### 1. `start_bot.bat` - Iniciar Bot
**Uso:**
```cmd
cd "C:\Users\lucas\Desktop\Bot Trader\windows"
start_bot.bat
```

**O que faz:**
- ✅ Ativa ambiente virtual Python
- ✅ Verifica se .env existe
- ✅ Cria diretório de logs
- ✅ Inicia o bot
- ✅ Exibe erros se bot crashar

---

### 2. `monitor_bot.bat` - Monitorar Bot
**Uso:**
```cmd
cd "C:\Users\lucas\Desktop\Bot Trader\windows"
monitor_bot.bat
```

**O que mostra:**
- ✅ Status do processo Python
- ✅ Uso de CPU/RAM
- ✅ Últimas 10 linhas do log
- ✅ Estatísticas do database
- ✅ Conectividade Binance
- ✅ Auto-restart se detectar parado

---

### 3. `backup.bat` - Backup Manual
**Uso:**
```cmd
cd "C:\Users\lucas\Desktop\Bot Trader\windows"
backup.bat
```

**O que faz backup:**
- ✅ `bot_data.db` → Database SQLite
- ✅ `bot_dados.json` → Estado do bot
- ✅ `logs/` → Logs compactados
- ✅ `.env` → Configurações

**Localização:** `bot-trader-backups/`

**Retenção:** Pergunta se deseja limpar backups >30 dias

---

### 4. `BotTrader24-7.xml` - Tarefa Agendada
**Uso:**
1. Abrir **Agendador de Tarefas** (Task Scheduler)
2. Ação → Importar Tarefa
3. Selecionar `BotTrader24-7.xml`
4. Verificar caminho do usuário
5. OK

**Configurações:**
- ✅ Inicia no boot do sistema
- ✅ Reinicia a cada 1min se falhar (999x)
- ✅ Roda mesmo em bateria
- ✅ Requer rede disponível

---

## 🚀 Setup Rápido (3 Passos)

### Passo 1: Desabilitar Suspensão
```powershell
# PowerShell como Administrador
powercfg /change standby-timeout-ac 0
powercfg /change monitor-timeout-ac 30
```

**Ou via Interface:**
- Painel de Controle → Opções de Energia
- Suspender: **Nunca**

---

### Passo 2: Importar Tarefa Agendada
1. Tecla Windows + R → `taskschd.msc`
2. Ação → Importar Tarefa
3. Selecionar: `C:\Users\lucas\Desktop\Bot Trader\windows\BotTrader24-7.xml`
4. OK

---

### Passo 3: Testar
```cmd
# Iniciar manualmente
schtasks /run /tn "Bot Trader 24/7"

# Verificar se está rodando
tasklist | findstr python

# Monitorar
cd "C:\Users\lucas\Desktop\Bot Trader\windows"
monitor_bot.bat
```

---

## 📊 Comandos Úteis

### Task Scheduler (PowerShell)
```powershell
# Iniciar tarefa
schtasks /run /tn "Bot Trader 24/7"

# Parar tarefa (mata processo)
taskkill /f /im python.exe

# Ver status
schtasks /query /tn "Bot Trader 24/7" /fo LIST /v

# Desabilitar
schtasks /change /tn "Bot Trader 24/7" /disable

# Habilitar
schtasks /change /tn "Bot Trader 24/7" /enable

# Remover
schtasks /delete /tn "Bot Trader 24/7" /f
```

### Processos
```cmd
# Ver processos Python
tasklist | findstr python

# Matar Python
taskkill /f /im python.exe

# Ver uso de recursos
tasklist /fi "imagename eq python.exe" /v
```

### Logs
```powershell
# Ver log em tempo real
Get-Content "C:\Users\lucas\Desktop\Bot Trader\logs\bot.log" -Wait -Tail 20

# Ver últimas 50 linhas
Get-Content "C:\Users\lucas\Desktop\Bot Trader\logs\bot.log" -Tail 50

# Procurar erros
Select-String -Path "C:\Users\lucas\Desktop\Bot Trader\logs\bot.log" -Pattern "ERROR"
```

---

## 🔧 Configurações Adicionais

### 1. Startup Folder (Alternativo)
Se não quiser usar Task Scheduler:

1. Windows + R → `shell:startup`
2. Criar atalho de `start_bot.bat`
3. Copiar atalho para pasta Startup

---

### 2. Executar Minimizado
1. Botão direito em `start_bot.bat` → Criar atalho
2. Botão direito no atalho → Propriedades
3. Atalho → Executar: **Minimizada**
4. OK

---

### 3. Backup Automático Diário
```powershell
# PowerShell (Admin)
$action = New-ScheduledTaskAction -Execute "C:\Users\lucas\Desktop\Bot Trader\windows\backup.bat"
$trigger = New-ScheduledTaskTrigger -Daily -At 3am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Bot Trader Backup" -Description "Backup diário do bot"
```

---

## ⚠️ Troubleshooting

### Bot não inicia
```cmd
# Testar manualmente
cd "C:\Users\lucas\Desktop\Bot Trader"
call venv\Scripts\activate.bat
python src\main.py

# Ver erro
```

### "tee" não reconhecido
Editar `start_bot.bat`, linha 47:
```batch
REM Trocar:
python src\main.py 2>&1 | tee -a logs\bot.log

REM Por:
python src\main.py >> logs\bot.log 2>&1
```

### Task Scheduler não inicia
1. Verificar permissões do usuário
2. Executar Task Scheduler como Admin
3. Verificar caminho do arquivo está correto
4. Ver Event Viewer: Windows Logs → Application

---

## 📝 Checklist

### Configuração Inicial
- [ ] Python funcionando
- [ ] Bot testado com `start_bot.bat`
- [ ] Suspensão desabilitada
- [ ] .env configurado

### Task Scheduler
- [ ] Tarefa importada
- [ ] Testada manualmente
- [ ] Verificar após reiniciar PC

### Monitoramento
- [ ] `monitor_bot.bat` testado
- [ ] Telegram configurado (opcional)

### Backup
- [ ] `backup.bat` testado
- [ ] Tarefa diária configurada (opcional)
- [ ] Local de backup verificado

---

## 💰 Custos

**PC Desktop ligado 24/7:**
- Consumo: ~100-200W
- Custo/mês: R$40-80 (varia por região)

**Laptop ligado 24/7:**
- Consumo: ~30-60W
- Custo/mês: R$12-25

**VPS ($6/mês = ~R$30/mês)**
- Mais barato que PC desktop
- Não depende do PC ligado
- Não consome energia em casa

---

## 🎯 Recomendação

### Para Testes (1-2 semanas): ✅ Local
- Testar funcionamento
- Ver primeiros trades
- Ajustar parâmetros

### Para Produção (24/7): ✅ VPS
- Mais confiável
- Custo/benefício melhor
- Não depende do PC
- Ver: [VPS_SETUP_GUIDE.md](../VPS_SETUP_GUIDE.md)

---

## ✅ Vantagens vs Desvantagens

### ✅ Vantagens (Local)
- Grátis (hardware já existe)
- Controle total
- Fácil debugar
- Acesso físico ao PC

### ❌ Desvantagens (Local)
- PC precisa ficar ligado 24/7
- Custo de energia (R$40-80/mês)
- Barulho/calor
- Vulnerável a quedas de energia
- Não roda se desligar PC

---

**Criado por:** Claude Code
**Para:** Setup Windows 24/7
