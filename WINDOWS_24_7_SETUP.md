# 💻 Rodar Bot 24/7 no Windows (Localmente)

**Objetivo:** Configurar o bot para rodar 24/7 no seu PC Windows sem precisar de VPS.

---

## 📋 REQUISITOS

- ✅ Windows 10/11
- ✅ PC ligado 24/7 (ou quase)
- ✅ Conexão internet estável
- ✅ Python 3.10+ instalado
- ✅ Projeto já funcionando

---

## 🎯 OPÇÕES DISPONÍVEIS

### Opção 1: Task Scheduler (Recomendado)
- ✅ Inicia automaticamente no boot
- ✅ Reinicia se crashar
- ✅ Roda em background
- ✅ Não precisa deixar terminal aberto
- ⚠️ Requer configuração inicial

### Opção 2: NSSM (Serviço Windows)
- ✅ Roda como serviço nativo Windows
- ✅ Auto-restart
- ✅ Logs automáticos
- ⚠️ Requer instalação de software

### Opção 3: PM2 (Node.js)
- ✅ Interface visual
- ✅ Logs estruturados
- ⚠️ Requer Node.js instalado

### Opção 4: Terminal Sempre Aberto
- ✅ Mais simples
- ❌ Precisa deixar terminal aberto
- ❌ Fecha se deslogar

---

## 🚀 OPÇÃO 1: TASK SCHEDULER (MELHOR)

### Passo 1: Desabilitar Suspensão

```powershell
# Abrir PowerShell como Administrador

# Desabilitar suspensão quando conectado
powercfg /change standby-timeout-ac 0

# Desabilitar desligamento de tela
powercfg /change monitor-timeout-ac 30

# Desabilitar hibernação (opcional)
powercfg /hibernate off
```

**Ou via Interface:**
1. Painel de Controle → Opções de Energia
2. Editar plano de energia
3. Colocar computador em suspensão: **Nunca**
4. Desligar vídeo: 30 minutos (economiza energia)

---

### Passo 2: Criar Script de Inicialização

Arquivo já criado: `windows/start_bot.bat`

**Conteúdo:**
```batch
@echo off
cd /d "c:\Users\lucas\Desktop\Bot Trader"
call venv\Scripts\activate
python src\main.py
pause
```

**Testar:**
```cmd
cd "c:\Users\lucas\Desktop\Bot Trader\windows"
start_bot.bat
```

Deve iniciar o bot normalmente.

---

### Passo 3: Configurar Task Scheduler

**Método A: Interface Gráfica**

1. Abrir **Agendador de Tarefas** (Task Scheduler)
   - Tecla Windows + R → `taskschd.msc`

2. Criar Tarefa Básica
   - Ação → Criar Tarefa Básica
   - Nome: `Bot Trader 24/7`
   - Descrição: `Crypto trading bot automático`

3. Gatilho (Trigger)
   - Quando: **Ao iniciar o sistema**
   - ✅ Marcar "Ativado"

4. Ação
   - Ação: **Iniciar um programa**
   - Programa: `C:\Users\lucas\Desktop\Bot Trader\windows\start_bot.bat`
   - Iniciar em: `C:\Users\lucas\Desktop\Bot Trader`

5. Condições
   - ❌ Desmarcar "Iniciar tarefa apenas se o computador estiver conectado à CA"
   - ❌ Desmarcar "Parar se o computador passar a usar bateria"

6. Configurações
   - ✅ Permitir que a tarefa seja executada sob demanda
   - ✅ Executar tarefa assim que possível após uma inicialização agendada ser perdida
   - Se a tarefa falhar, reiniciar a cada: **1 minuto**
   - Tentar reiniciar até: **999 vezes**

**Método B: Importar XML (Automático)**

1. Usar arquivo: `windows/BotTrader24-7.xml`
2. Task Scheduler → Importar Tarefa
3. Selecionar `BotTrader24-7.xml`
4. Ajustar caminho do usuário se necessário

---

### Passo 4: Testar Task Scheduler

```powershell
# Executar tarefa manualmente
schtasks /run /tn "Bot Trader 24/7"

# Verificar se está rodando
tasklist | findstr python

# Ver status da tarefa
schtasks /query /tn "Bot Trader 24/7" /fo LIST /v
```

---

## 🛠️ OPÇÃO 2: NSSM (SERVIÇO WINDOWS)

### Passo 1: Baixar NSSM

```powershell
# Download manual: https://nssm.cc/download
# Ou via PowerShell:
Invoke-WebRequest -Uri "https://nssm.cc/release/nssm-2.24.zip" -OutFile "nssm.zip"
Expand-Archive -Path "nssm.zip" -DestinationPath "C:\nssm"
```

### Passo 2: Instalar Serviço

```cmd
# Abrir CMD como Administrador
cd C:\nssm\nssm-2.24\win64

# Instalar serviço (abre GUI)
nssm install BotTrader

# Configurar:
# Path: C:\Users\lucas\Desktop\Bot Trader\venv\Scripts\python.exe
# Startup directory: C:\Users\lucas\Desktop\Bot Trader
# Arguments: src\main.py

# Ou via linha de comando:
nssm install BotTrader "C:\Users\lucas\Desktop\Bot Trader\venv\Scripts\python.exe" "src\main.py"
nssm set BotTrader AppDirectory "C:\Users\lucas\Desktop\Bot Trader"
nssm set BotTrader AppStdout "C:\Users\lucas\Desktop\Bot Trader\logs\bot.log"
nssm set BotTrader AppStderr "C:\Users\lucas\Desktop\Bot Trader\logs\bot-error.log"
```

### Passo 3: Gerenciar Serviço

```cmd
# Iniciar serviço
nssm start BotTrader

# Parar serviço
nssm stop BotTrader

# Reiniciar serviço
nssm restart BotTrader

# Ver status
nssm status BotTrader

# Remover serviço
nssm remove BotTrader confirm
```

**Ou via Services:**
- Windows + R → `services.msc`
- Procurar "BotTrader"
- Botão direito → Iniciar/Parar/Reiniciar

---

## 📊 OPÇÃO 3: PM2 (NODE.JS)

### Passo 1: Instalar Node.js

Baixar: https://nodejs.org/ (LTS version)

### Passo 2: Instalar PM2

```cmd
npm install -g pm2
npm install -g pm2-windows-startup

# Configurar startup
pm2-startup install
```

### Passo 3: Iniciar Bot com PM2

```cmd
cd "C:\Users\lucas\Desktop\Bot Trader"

# Iniciar bot
pm2 start venv/Scripts/python.exe --name bot-trader -- src/main.py

# Salvar para auto-start
pm2 save

# Ver status
pm2 status

# Ver logs
pm2 logs bot-trader

# Monitorar
pm2 monit
```

### Comandos PM2

```cmd
# Listar processos
pm2 list

# Parar
pm2 stop bot-trader

# Reiniciar
pm2 restart bot-trader

# Remover
pm2 delete bot-trader

# Ver logs
pm2 logs bot-trader --lines 100
```

---

## 🖥️ OPÇÃO 4: TERMINAL SEMPRE ABERTO

### Método 1: CMD Minimizado

1. Criar atalho de `start_bot.bat`
2. Botão direito → Propriedades
3. Atalho → Executar: **Minimizada**
4. OK

5. Colocar atalho na pasta Startup:
   - Windows + R → `shell:startup`
   - Copiar atalho para lá

### Método 2: PowerShell Persistente

```powershell
# Criar arquivo: windows/start_bot_hidden.vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c ""C:\Users\lucas\Desktop\Bot Trader\windows\start_bot.bat""", 0, False
```

**Executar:**
```cmd
wscript "C:\Users\lucas\Desktop\Bot Trader\windows\start_bot_hidden.vbs"
```

---

## 🔍 MONITORAMENTO

### Script de Monitor (Windows)

Arquivo: `windows/monitor_bot.bat`

**Uso:**
```cmd
cd "C:\Users\lucas\Desktop\Bot Trader\windows"
monitor_bot.bat
```

**Mostra:**
- Status do processo Python
- Uso de CPU/RAM
- Últimas linhas do log
- Estatísticas do database

---

## ⚙️ CONFIGURAÇÕES IMPORTANTES

### 1. Energia (Crítico!)

**Via PowerShell (Admin):**
```powershell
# Criar plano de energia "Always On"
powercfg /duplicatescheme 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c

# Desabilitar suspensão
powercfg /change standby-timeout-ac 0
powercfg /change standby-timeout-dc 0

# Desabilitar hibernação
powercfg /hibernate off

# Desabilitar desligamento de HD
powercfg /change disk-timeout-ac 0

# Tela pode desligar (economiza)
powercfg /change monitor-timeout-ac 30
```

**Via Interface:**
1. Painel de Controle → Opções de Energia
2. Criar plano: "Bot Trading 24/7"
3. Configurar:
   - Desligar vídeo: 30 min
   - Suspender: Nunca
   - Hibernar: Nunca

---

### 2. Atualizações do Windows

**Evitar restart automático:**

1. Windows + R → `gpedit.msc`
2. Configuração do Computador → Modelos Administrativos → Componentes do Windows → Windows Update
3. "Configurar Atualizações Automáticas"
4. Ativado → 2 - Notificar para download e notificar para instalação

**Ou via PowerShell (Admin):**
```powershell
# Pausar updates por 7 dias
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" -Name "PauseUpdatesExpiryTime" -Value ([DateTime]::Now.AddDays(7).ToString("yyyy-MM-ddTHH:mm:ssZ"))
```

---

### 3. Firewall

**Permitir Python (se necessário):**

```powershell
# PowerShell (Admin)
New-NetFirewallRule -DisplayName "Python - Bot Trader" -Direction Outbound -Program "C:\Users\lucas\Desktop\Bot Trader\venv\Scripts\python.exe" -Action Allow
```

---

### 4. Antivírus

**Adicionar exceção:**
1. Windows Security → Proteção contra vírus e ameaças
2. Gerenciar configurações
3. Exclusões → Adicionar exclusão
4. Pasta: `C:\Users\lucas\Desktop\Bot Trader`

---

## 📝 LOGS

### Localizações
```
C:\Users\lucas\Desktop\Bot Trader\logs\
├── bot.log          # Logs do bot
├── bot-error.log    # Erros
├── monitor.log      # Monitor (se usar cron)
└── backup.log       # Backups
```

### Ver logs em tempo real

**PowerShell:**
```powershell
Get-Content "C:\Users\lucas\Desktop\Bot Trader\logs\bot.log" -Wait -Tail 20
```

**CMD:**
```cmd
powershell Get-Content 'logs\bot.log' -Wait -Tail 20
```

---

## 🔄 BACKUP AUTOMÁTICO (WINDOWS)

### Criar Tarefa de Backup

1. Task Scheduler → Criar Tarefa Básica
2. Nome: "Bot Trader Backup"
3. Gatilho: **Diariamente** às 3:00
4. Ação: `windows\backup.bat`

**Ou via PowerShell:**
```powershell
$action = New-ScheduledTaskAction -Execute "C:\Users\lucas\Desktop\Bot Trader\windows\backup.bat"
$trigger = New-ScheduledTaskTrigger -Daily -At 3am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Bot Trader Backup" -Description "Backup diário do bot"
```

---

## ⚠️ VANTAGENS vs DESVANTAGENS

### ✅ Vantagens (Local)
- **Grátis** (sem custo de VPS)
- Controle total
- Fácil debugar
- Acesso físico

### ❌ Desvantagens (Local)
- Depende do PC ligado 24/7
- Consome energia (~R$30-50/mês)
- Não roda se PC desligar
- Vulnerável a quedas de energia
- Barulho/calor do PC ligado

### 💡 Recomendação

**Para testes (1-2 semanas):** Local ✅
**Para produção long-term:** VPS ✅

**Motivo:** VPS custa $6/mês vs ~R$40/mês de energia do PC ligado 24/7.

---

## 🔋 ECONOMIA DE ENERGIA

### Otimizações

```powershell
# Desligar tela após inatividade (economiza)
powercfg /change monitor-timeout-ac 10

# Desabilitar Fast Startup (evita bugs)
powercfg /hibernate off

# Modo de desempenho balanceado
powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e
```

### Monitorar Consumo

1. Task Manager (Ctrl+Shift+Esc)
2. Performance → CPU
3. Ver consumo em Watts (se disponível)

**Estimativa:**
- PC Desktop: 100-200W → ~R$40-80/mês
- Laptop: 30-60W → ~R$12-25/mês

---

## ✅ CHECKLIST

### Configuração Inicial
- [ ] Python funcionando
- [ ] Bot testado manualmente
- [ ] `.env` configurado
- [ ] Suspensão desabilitada
- [ ] `start_bot.bat` funcionando

### Task Scheduler (Recomendado)
- [ ] Tarefa criada
- [ ] Configurado para reiniciar
- [ ] Testado manualmente
- [ ] Reiniciou PC e verificou

### NSSM (Alternativo)
- [ ] NSSM instalado
- [ ] Serviço criado
- [ ] Logs configurados
- [ ] Testado start/stop

### Monitoramento
- [ ] `monitor_bot.bat` testado
- [ ] Telegram configurado (opcional)
- [ ] Logs sendo gerados

### Backup
- [ ] Tarefa de backup criada
- [ ] Backup manual testado
- [ ] Local de backup definido

### Segurança
- [ ] Atualizações pausadas/configuradas
- [ ] Firewall configurado
- [ ] Antivírus com exceção

---

## 🆘 TROUBLESHOOTING

### Bot não inicia no boot
```powershell
# Verificar tarefa
schtasks /query /tn "Bot Trader 24/7" /fo LIST /v

# Ver logs
Get-EventLog -LogName Application -Source "Task Scheduler" -Newest 10
```

### Bot fecha sozinho
```cmd
# Verificar se PC entrou em suspensão
powercfg /requests

# Ver eventos de energia
Get-EventLog -LogName System -Source "Power-Troubleshooter" -Newest 10
```

### Alto uso de CPU
```cmd
# Ver uso do Python
tasklist /fi "imagename eq python.exe" /v

# Matar processo
taskkill /im python.exe /f
```

---

## 🎯 RECOMENDAÇÃO FINAL

**MELHOR OPÇÃO PARA VOCÊ:**

**Task Scheduler** ✅
- Nativo do Windows
- Não precisa instalar nada
- Auto-restart
- Simples de configurar

**Passos:**
1. Criar `start_bot.bat` ✅ (já existe)
2. Desabilitar suspensão
3. Importar `windows/BotTrader24-7.xml` no Task Scheduler
4. Reiniciar PC e testar

**Tempo:** 10 minutos
**Custo:** R$0 (usa PC que já tem)

---

**📌 PRÓXIMO:** Vou criar os scripts Windows agora!
