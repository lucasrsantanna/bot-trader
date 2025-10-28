# 🔑 Credenciais da Binance Testnet

Este documento contém as **credenciais públicas da Binance Testnet** configuradas neste projeto.

---

## ⚠️ IMPORTANTE

- ✅ **Estas são credenciais de TESTNET** (sem dinheiro real)
- ✅ **É SEGURO compartilhar no GitHub** - não há riscos financeiros
- ✅ **Use apenas para desenvolvimento e testes**
- ❌ **NUNCA use estas keys para trading real**

---

## 📋 Credenciais Atuais

As credenciais abaixo estão configuradas no arquivo **`.env.testnet`**:

```bash
BINANCE_API_KEY=DUelhtBgpTPf5k2xvFNTf2WpRjGlIr64zbrOegpThi1VdgxE7902EHJ9AheTopMj
BINANCE_SECRET_KEY=bbPEuRe1LajqKWRzEx8Wu5UsFhuITkwu0xmmBKfqIslHbZtbXjTVVw46WJuooO2o
USE_TESTNET=true
```

---

## 🚀 Como Usar

### **Opção 1: Usar as credenciais compartilhadas (Recomendado para iniciantes)**

O arquivo `.env.testnet` já está no repositório com as keys configuradas.

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/lucasrsantanna/bot-trader.git
   cd bot-trader
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o bot:**
   ```bash
   python src/main.py
   ```

**Pronto!** O bot detectará automaticamente o arquivo `.env.testnet` e usará as credenciais da Testnet.

---

### **Opção 2: Criar suas próprias credenciais**

Se preferir criar suas próprias API keys da Testnet:

1. **Acesse a Binance Testnet:**
   - 🔗 https://testnet.binance.vision/

2. **Faça login:**
   - Use sua conta GitHub ou crie uma nova

3. **Gere suas API Keys:**
   - Acesse: https://testnet.binance.vision/key-generation
   - Clique em **"Generate HMAC_SHA256 Key"**
   - **⚠️ ATENÇÃO:** A Secret Key só aparece UMA VEZ! Copie imediatamente.

4. **Configure no projeto:**
   - Edite o arquivo `.env.testnet` com suas novas keys
   - Ou crie um arquivo `.env` local (será ignorado pelo Git)

---

## 🔒 Segurança: Testnet vs Produção

### **Testnet (.env.testnet):**
- ✅ Pode ser compartilhado publicamente
- ✅ Não tem dinheiro real
- ✅ Usado para desenvolvimento e testes
- 📄 Arquivo: `.env.testnet` (commitado no Git)

### **Produção (.env):**
- ❌ **NUNCA compartilhe no Git**
- ❌ Contém credenciais com acesso a dinheiro real
- ❌ Use apenas localmente ou em servidores seguros
- 🚫 Arquivo: `.env` (protegido pelo `.gitignore`)

---

## 🛠️ Sistema de Configuração

O projeto foi configurado para detectar automaticamente qual arquivo usar:

```python
# config/settings.py detecta automaticamente:
# 1. Se .env.testnet existe → usa Testnet (seguro para compartilhar)
# 2. Se não existe → usa .env (suas credenciais privadas)
```

**Logs ao iniciar:**
```bash
[CONFIG] Usando credenciais do arquivo: .env.testnet (Testnet Mode)
```

---

## 🔄 Fluxos de Uso

### **Desenvolvedor Iniciante:**
1. Clone o repositório
2. Execute `python src/main.py`
3. ✅ Funciona automaticamente com `.env.testnet`

### **Desenvolvedor Avançado:**
1. Clone o repositório
2. Crie arquivo `.env` local com suas próprias keys
3. `.env` tem prioridade sobre `.env.testnet`
4. ✅ Suas credenciais ficam privadas

### **Produção (Trading Real):**
1. **⚠️ CUIDADO:** Só faça se souber o que está fazendo!
2. Renomeie/delete `.env.testnet`
3. Crie `.env` com credenciais REAIS da Binance
4. Configure `USE_TESTNET=false`
5. ✅ Bot opera com dinheiro real (RISCO!)

---

## 📊 Limites da Testnet

A Binance Testnet tem algumas limitações:

- 💰 Dinheiro virtual (não real)
- 🕒 Pode ter instabilidade ocasional
- 📉 Dados de mercado podem diferir levemente da produção
- 🔄 Saldo resetado periodicamente pela Binance

**Para obter saldo virtual:**
- Acesse https://testnet.binance.vision/
- Vá em "Faucet" para receber USDT/BTC virtuais

---

## 🆘 Problemas Comuns

### **Erro: Invalid API Key**
**Solução:**
- Verifique se as keys no `.env.testnet` estão corretas
- Gere novas keys em https://testnet.binance.vision/key-generation

### **Erro: Network Error**
**Solução:**
- A Testnet pode estar temporariamente indisponível
- Tente novamente em alguns minutos
- Verifique sua conexão com internet

### **Bot não encontra .env.testnet**
**Solução:**
- Certifique-se de que está na raiz do projeto
- Verifique se o arquivo `.env.testnet` existe
- Faça `git pull` para garantir que tem a versão mais recente

---

## 📚 Recursos Úteis

- 🌐 **Testnet Homepage:** https://testnet.binance.vision/
- 🔑 **Gerar API Keys:** https://testnet.binance.vision/key-generation
- 💰 **Faucet (Obter fundos virtuais):** https://testnet.binance.vision/ → Faucet
- 📖 **Documentação Binance API:** https://binance-docs.github.io/apidocs/spot/en/
- 📖 **Guia do Projeto:** Ver `README.md`

---

## ✅ Checklist Rápido

Antes de começar a usar o bot:

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Arquivo `.env.testnet` existe no projeto
- [ ] Conexão com internet funcionando
- [ ] (Opcional) Telegram configurado para notificações

**Tudo pronto? Execute:**
```bash
python src/main.py
```

---

## 🔄 Atualizações

**Última atualização:** 2025-10-26

Se as credenciais atuais pararem de funcionar, você pode:
1. Gerar novas keys em https://testnet.binance.vision/
2. Atualizar o arquivo `.env.testnet`
3. Fazer commit (é seguro - é testnet!)

---

**Happy Testing! 🚀**
