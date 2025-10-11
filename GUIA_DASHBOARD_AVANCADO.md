## 🎮 DASHBOARD AVANÇADO - CONTROLE TOTAL DO BOT

## 🚀 COMO USAR

### 1️⃣ Executar Bot + Dashboard Juntos

**Terminal 1 - Bot:**
```
Duplo clique: EXECUTAR_BOT.bat
```

**Terminal 2 - Dashboard:**
```
Duplo clique: DASHBOARD_AVANCADO.bat
```

**Navegador:**
```
Abra automaticamente: http://localhost:8502
```

---

## 🎛️ CONTROLES DISPONÍVEIS

### ⏯️ Pausar/Retomar Bot

**Como funciona:**
1. Clique no botão **⏸️ PAUSAR** na barra lateral
2. Bot para de analisar mercado
3. Posições abertas continuam sendo monitoradas
4. Clique **▶️ RETOMAR** para continuar

**Quando usar:**
- Você quer analisar o mercado antes de continuar
- Notícias importantes acontecendo
- Fim do dia de trading

---

### 🎯 Entrada/Saída Manual

**Tipos de ordem:**

#### 1. COMPRA (LONG)
- **O que faz:** Abre posição comprando BTC
- **Quando usar:** Você vê oportunidade de alta
- **Resultado:** Bot compra e define Stop Loss/Take Profit

#### 2. VENDA (SHORT)
- **O que faz:** Em SPOT, fecha posição aberta
- **Quando usar:** Você quer realizar lucro ou cortar prejuízo
- **Resultado:** Fecha posição atual

#### 3. FECHAR POSIÇÃO
- **O que faz:** Fecha qualquer posição aberta
- **Quando usar:** Emergência ou fim do dia
- **Resultado:** Vende tudo no preço atual

**Como executar:**
1. Selecione o tipo de ordem no dropdown
2. Clique **✅ Executar Ordem Manual**
3. Veja no terminal do bot: `[DASHBOARD] Entrada manual: BUY`
4. Ordem executada em ~5 segundos

---

### ⚙️ Ajustar Parâmetros em Tempo Real

**Parâmetros ajustáveis:**

#### ⏱️ Intervalo (10-300 segundos)
- **Padrão:** 60s
- **Menor (10s):** Análises mais frequentes, mais trades
- **Maior (300s):** Análises espaçadas, menos trades
- **Efeito:** Aplica IMEDIATAMENTE no próximo ciclo

#### 💸 Risco por Trade (0.5-5%)
- **Padrão:** 1%
- **Menor (0.5%):** Mais conservador
- **Maior (5%):** Mais agressivo
- **Efeito:** Próximo trade usa novo valor

#### 🛑 Stop Loss (0.1-2%)
- **Padrão:** 0.2%
- **Menor (0.1%):** Stop mais apertado (menos perda, mais stops acionados)
- **Maior (2%):** Stop mais largo (mais perda tolerada)
- **Efeito:** Próximo trade usa novo valor

#### 🎯 Take Profit (0.1-5%)
- **Padrão:** 0.5%
- **Menor (0.1%):** Realiza lucro rápido
- **Maior (5%):** Aguarda mais lucro
- **Efeito:** Próximo trade usa novo valor

**Como salvar:**
1. Ajuste os sliders na barra lateral
2. Clique **💾 Salvar Parâmetros**
3. Veja confirmação: `✅ Parâmetros atualizados!`
4. Próximo trade usa novos valores

---

## 📊 VISUALIZAÇÕES

### Tab 1: Visão Geral

**Métricas principais:**
- 💰 **P&L Total:** Lucro/Prejuízo acumulado
- 💵 **Capital Atual:** Quanto você tem agora
- 💵 **Capital Inicial:** Quanto começou
- 🎯 **Win Rate:** % de trades lucrativos

**Posição Atual:**
- Tipo (LONG/SHORT)
- Preço de entrada
- Quantidade em BTC
- Stop Loss e Take Profit
- Potencial lucro/perda

**Configurações Atuais:**
- Tabela com todos os parâmetros
- Fácil visualização do que está ativo

---

### Tab 2: Trades

**Histórico completo:**
- Data/Hora de cada trade
- Preço de entrada e saída
- Quantidade negociada
- P&L (colorido: verde = lucro, vermelho = prejuízo)
- Motivo (Stop Loss, Take Profit, Ordem Manual)

**Estatísticas:**
- 💚 Lucro Total
- 💔 Prejuízo Total
- 📊 P&L Médio por trade

---

### Tab 3: Gráficos

**Evolução do Capital:**
- Linha do tempo mostrando crescimento/queda
- Visualize performance ao longo do tempo

**P&L por Trade:**
- Gráfico de barras
- Verde = lucro, Vermelho = prejuízo
- Veja padrões de performance

---

### Tab 4: Logs

**Logs em tempo real:**
- Últimos 50 eventos do bot
- Colorido por tipo:
  - 🟢 Verde: Compras, Take Profit
  - 🟡 Amarelo: Vendas
  - 🔴 Vermelho: Erros, Stop Loss
  - ⚪ Branco: Info geral

---

## 🔄 FLUXO DE COMUNICAÇÃO

```
DASHBOARD (você)          bot_controle.json          BOT (executando)
      ↓                          ↓                          ↓
  Clica botão    →    Salva comando    →    Lê a cada ciclo
  "Pausar"                pausado=true         Bot pausa
      ↓                          ↓                          ↓
  Ajusta slider  →    Salva novos params  →  Aplica valores
  Stop Loss 0.5%         stop_loss=0.005      Próximo trade
      ↓                          ↓                          ↓
  Força entrada  →    forcar_entrada=BUY  →  Executa compra
  COMPRA                                      Imediatamente
```

**Arquivos usados:**
- `bot_controle.json` - Comandos do dashboard para o bot
- `bot_dados.json` - Dados do bot para o dashboard

---

## 💡 EXEMPLOS DE USO

### Exemplo 1: Pausar para analisar

**Situação:** Mercado muito volátil, quer dar uma pausa

1. No dashboard, clique **⏸️ PAUSAR**
2. No terminal do bot: `[DASHBOARD] Bot pausado pelo dashboard`
3. Bot para de analisar, mas monitora posição aberta
4. Analise o mercado tranquilamente
5. Quando pronto, clique **▶️ RETOMAR**
6. Bot volta a funcionar normalmente

---

### Exemplo 2: Entrada manual

**Situação:** RSI está em 35 (quase sobrevendido), você quer entrar agora

1. Selecione **COMPRA (LONG)**
2. Clique **✅ Executar Ordem Manual**
3. No terminal: `[DASHBOARD] Entrada manual: BUY`
4. Em ~5s: `[EXECUTANDO COMPRA]`
5. Posição aberta aparece no dashboard
6. Acompanhe P&L em tempo real

---

### Exemplo 3: Ajustar Stop Loss

**Situação:** Você quer dar mais espaço para o preço respirar

1. No dashboard, mova slider **🛑 Stop Loss** de 0.2% para 0.5%
2. Clique **💾 Salvar Parâmetros**
3. Confirmação: `✅ Parâmetros atualizados!`
4. Próximo trade abre com Stop Loss de 0.5%
5. Trades atuais mantêm Stop Loss original

---

### Exemplo 4: Fechar posição manual

**Situação:** Notícia ruim saiu, quer sair da posição

1. Selecione **FECHAR POSIÇÃO**
2. Clique **✅ Executar Ordem Manual**
3. No terminal: `[DASHBOARD] Fechamento manual solicitado`
4. Posição fecha no preço atual
5. P&L é calculado e salvo
6. Dashboard atualiza mostrando trade fechado

---

## 🎯 MELHORES PRÁTICAS

### ✅ Faça:
- **Monitore regularmente** - Clique Atualizar a cada 1-2 minutos
- **Ajuste devagar** - Mude 1 parâmetro por vez
- **Teste primeiro** - Teste mudanças em simulação antes de real
- **Documente** - Anote quais configurações funcionaram melhor

### ❌ Não faça:
- **Mudar durante trade** - Aguarde posição fechar
- **Forçar entradas aleatórias** - Siga a análise técnica
- **Fechar dashboard** - Deixe aberto enquanto bot roda
- **Trocar tudo de uma vez** - Ajuste gradualmente

---

## 🚨 TROUBLESHOOTING

### Dashboard não atualiza
**Solução:** Clique no botão **🔄 Atualizar**

### Botão não funciona
**Solução:**
1. Verifique se bot está rodando
2. Veja se arquivo `bot_controle.json` foi criado
3. Aguarde 5-10 segundos (bot lê a cada ciclo)

### Parâmetros não aplicam
**Solução:**
1. Clique **💾 Salvar Parâmetros**
2. Aguarde próximo ciclo do bot
3. Veja no terminal: `[DASHBOARD] Parametros atualizados!`

### Bot não pausa
**Solução:**
1. Clique novamente no botão
2. Verifique logs no terminal
3. Última opção: Ctrl+C no terminal

---

## 📋 ATALHOS DE TECLADO

| Tecla | Ação |
|-------|------|
| **R** | Atualizar página |
| **Ctrl+C** | Parar bot (no terminal) |
| **F5** | Recarregar dashboard |
| **Ctrl+Shift+R** | Limpar cache e recarregar |

---

## 🎉 CONCLUSÃO

Agora você tem **CONTROLE TOTAL** do bot:

✅ Pausar/Retomar quando quiser
✅ Forçar entradas e saídas manuais
✅ Ajustar parâmetros em tempo real
✅ Visualizar tudo em gráficos bonitos
✅ Acompanhar logs ao vivo

**Tudo sem parar o bot! 🚀**

---

**Dúvidas?** Execute e teste! A melhor forma de aprender é usando! 😊
