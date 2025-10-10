# 🚀 Como Rodar o Bot 24/7 no Windows (SIMPLES)

**3 opções para você escolher:**

---

## ⚡ OPÇÃO 1: Duplo-Clique (MAIS FÁCIL)

### Passo Único:
1. Ir na pasta: `C:\Users\lucas\Desktop\Bot Trader\windows`
2. **Duplo-clique** em `start_bot.bat`

✅ **Pronto!** Uma janela preta vai abrir com o bot rodando.

**⚠️ IMPORTANTE:** Não feche essa janela! Deixe ela aberta (pode minimizar).

---

## 🤖 OPÇÃO 2: Task Scheduler (AUTO-START)

### Vantagem: Bot inicia sozinho quando você ligar o PC

### Passo 1: Desabilitar Suspensão
1. Clicar com botão direito no **ícone da bateria** (barra inferior)
2. Opções de energia
3. **"Colocar computador em suspensão"** → Mudar para **"Nunca"**

### Passo 2: Importar Tarefa
1. Pressionar **Windows + R**
2. Digitar: `taskschd.msc` e dar Enter
3. Clicar em **"Ação"** (menu superior) → **"Importar Tarefa"**
4. Navegar até: `C:\Users\lucas\Desktop\Bot Trader\windows\BotTrader24-7.xml`
5. Clicar **"Abrir"**
6. Clicar **"OK"**

### Passo 3: Iniciar Tarefa
**Opção A - Via Interface:**
1. No Agendador de Tarefas (ainda aberto)
2. Procurar **"Bot Trader 24/7"** na lista
3. Botão direito → **"Executar"**

**Opção B - Via Comando:**
1. Pressionar **Windows + R**
2. Digitar: `cmd` e dar Enter
3. Copiar e colar:
```cmd
schtasks /run /tn "Bot Trader 24/7"
```

✅ **Pronto!** Bot rodando em background (não aparece janela).

### Como verificar se está rodando?
1. Abrir **Gerenciador de Tarefas** (Ctrl+Shift+Esc)
2. Aba **"Detalhes"**
3. Procurar **"python.exe"** na lista

---

## 📊 OPÇÃO 3: Monitor (Ver Status)

### Para ver se o bot está funcionando:
1. Ir em: `C:\Users\lucas\Desktop\Bot Trader\windows`
2. Duplo-clique em `monitor_bot.bat`

Vai mostrar:
```
================================================
   BOT TRADER - MONITOR
================================================

STATUS DO PROCESSO
[OK] Bot esta RODANDO
   PID: 12345
   Memoria: 50 MB

RECURSOS DO SISTEMA
Sistema:
   CPU: 5%
   Memoria: 45% usada

ULTIMAS OPERACOES (LOG)
[Últimas 10 linhas do que o bot está fazendo]

ESTATISTICAS DO BANCO
   Total de Trades: 5
   Win Rate: 60%

CONECTIVIDADE
[OK] Conexao com Binance OK
```

---

## ❓ Qual Opção Escolher?

| Opção | Quando usar |
|-------|------------|
| **Opção 1** (Duplo-clique) | Teste rápido, ver logs na tela |
| **Opção 2** (Task Scheduler) | Rodar 24/7, auto-start no boot |
| **Opção 3** (Monitor) | Ver se está funcionando |

---

## 🛑 Como Parar o Bot?

### Se usou Opção 1 (Duplo-clique):
- Fechar a janela preta
- Ou apertar `Ctrl+C` na janela

### Se usou Opção 2 (Task Scheduler):
**Opção A - Matar processo:**
1. **Ctrl+Shift+Esc** (Gerenciador de Tarefas)
2. Aba **"Detalhes"**
3. Clicar com botão direito em **"python.exe"**
4. **"Finalizar tarefa"**

**Opção B - Via comando:**
```cmd
taskkill /f /im python.exe
```

---

## 💾 Backup

### Para fazer backup do banco de dados:
1. Ir em: `C:\Users\lucas\Desktop\Bot Trader\windows`
2. Duplo-clique em `backup.bat`

Vai criar backup em: `C:\Users\lucas\Desktop\Bot Trader\bot-trader-backups\`

---

## ⚙️ Configurações Importantes

### 1. PC ligado 24/7
Para o bot funcionar 24/7, o PC precisa estar:
- ✅ Ligado
- ✅ Com internet
- ✅ Sem suspensão automática

### 2. Desabilitar suspensão (IMPORTANTE!)
1. Painel de Controle → Opções de Energia
2. **"Colocar computador em suspensão"** → **"Nunca"**
3. **"Desligar vídeo"** → 30 minutos (pode deixar, economiza)

---

## 📱 Notificações no Telegram (Opcional)

Se você configurou o Telegram no `.env`:
- Você vai receber mensagens no celular quando:
  - ✅ Bot abrir uma posição
  - ✅ Bot fechar uma posição
  - ✅ Sinais da IA (BUY/SELL)
  - ⚠️ Erros críticos

---

## 🆘 Problemas Comuns

### "Não consigo encontrar o arquivo .bat"
- Certifique-se de estar em: `C:\Users\lucas\Desktop\Bot Trader\windows`

### "Janela fecha imediatamente"
- Abra o arquivo editando: Botão direito → Editar
- Verifique se os caminhos estão corretos

### "python não é reconhecido"
- Python não está instalado ou não está no PATH
- Reinstale Python marcando "Add to PATH"

### "Bot para sozinho"
- Verifique se PC não entrou em suspensão
- Veja logs em: `C:\Users\lucas\Desktop\Bot Trader\logs\bot-error.log`

---

## ✅ Checklist Rápido

**Antes de iniciar:**
- [ ] Python instalado
- [ ] `.env` configurado (API keys da Binance)
- [ ] Suspensão desabilitada
- [ ] Internet estável

**Para testar:**
- [ ] Duplo-clique em `start_bot.bat`
- [ ] Bot inicia sem erros
- [ ] Aparece "CryptoBot inicializado"
- [ ] Não fecha sozinho

**Para 24/7:**
- [ ] Task Scheduler configurado
- [ ] Tarefa importada
- [ ] Testado depois de reiniciar PC

---

## 💰 Custos

**Rodar localmente 24/7:**
- PC Desktop: ~R$40-80/mês (energia)
- Laptop: ~R$12-25/mês (energia)

**Alternativa VPS:**
- DigitalOcean/Vultr: $6/mês (~R$30/mês)
- Vantagem: Não depende do PC ligado
- Ver: [VPS_SETUP_GUIDE.md](VPS_SETUP_GUIDE.md)

---

## 📞 Resumo em 3 Linhas

1. **Teste rápido:** Duplo-clique em `windows/start_bot.bat`
2. **24/7 automático:** Importar `BotTrader24-7.xml` no Task Scheduler
3. **Ver status:** Duplo-clique em `windows/monitor_bot.bat`

---

**🎉 É isso! Escolha uma opção e comece a tradear!**
