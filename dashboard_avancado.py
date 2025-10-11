"""
DASHBOARD AVANÇADO - Bot Trader
Com controles em tempo real do bot
"""
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import time

# Configuração da página
st.set_page_config(
    page_title="Bot Trader - Controle Total",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Arquivos
DADOS_FILE = "bot_dados.json"
CONTROLE_FILE = "bot_controle.json"

def carregar_dados():
    """Carrega dados do bot"""
    if os.path.exists(DADOS_FILE):
        with open(DADOS_FILE, 'r') as f:
            return json.load(f)
    return None

def carregar_controles():
    """Carrega controles do bot"""
    if os.path.exists(CONTROLE_FILE):
        with open(CONTROLE_FILE, 'r') as f:
            return json.load(f)
    return {
        "pausado": False,
        "forcar_entrada": None,
        "forcar_saida": False,
        "novo_intervalo": None,
        "novos_parametros": None,
        "timestamp": datetime.now().isoformat()
    }

def salvar_controles(controles):
    """Salva controles para o bot ler"""
    controles["timestamp"] = datetime.now().isoformat()
    with open(CONTROLE_FILE, 'w') as f:
        json.dump(controles, f, indent=2)

def atualizar_config_bot(novos_params):
    """Atualiza configurações do bot em tempo real"""
    dados = carregar_dados()
    if dados:
        dados['config'].update(novos_params)
        with open(DADOS_FILE, 'w') as f:
            json.dump(dados, f, indent=2)
        return True
    return False

# Título
st.title("🤖 Bot Trader - Dashboard Avançado")

# Sidebar - Controles
st.sidebar.header("🎮 Controles do Bot")

dados = carregar_dados()
controles = carregar_controles()

# Status do bot
if dados:
    col1, col2, col3 = st.columns(3)

    with col1:
        if controles.get("pausado"):
            st.error("⏸️ BOT PAUSADO")
        else:
            st.success("▶️ BOT ATIVO")

    with col2:
        st.metric("💰 Capital", f"${dados['capital']:.2f}")

    with col3:
        st.metric("📊 Trades", len(dados['trades']))

# ========== CONTROLES PRINCIPAIS ==========
st.sidebar.subheader("⏯️ Controle de Execução")

col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("⏸️ PAUSAR" if not controles.get("pausado") else "▶️ RETOMAR",
                 use_container_width=True,
                 type="primary"):
        controles["pausado"] = not controles.get("pausado")
        salvar_controles(controles)
        st.rerun()

with col2:
    if st.button("🔄 Atualizar", use_container_width=True):
        st.rerun()

# ========== ENTRADA/SAÍDA MANUAL ==========
st.sidebar.subheader("🎯 Entrada/Saída Manual")

tipo_ordem = st.sidebar.selectbox(
    "Tipo de Ordem",
    ["Nenhuma", "COMPRA (LONG)", "VENDA (SHORT)", "FECHAR POSIÇÃO"]
)

if st.sidebar.button("✅ Executar Ordem Manual", use_container_width=True, type="secondary"):
    if tipo_ordem == "COMPRA (LONG)":
        controles["forcar_entrada"] = "BUY"
        st.sidebar.success("✅ Ordem de COMPRA enviada ao bot!")
    elif tipo_ordem == "VENDA (SHORT)":
        controles["forcar_entrada"] = "SELL"
        st.sidebar.success("✅ Ordem de VENDA enviada ao bot!")
    elif tipo_ordem == "FECHAR POSIÇÃO":
        controles["forcar_saida"] = True
        st.sidebar.success("✅ Fechamento de posição solicitado!")

    salvar_controles(controles)
    time.sleep(1)
    st.rerun()

# ========== PARÂMETROS EM TEMPO REAL ==========
st.sidebar.subheader("⚙️ Ajustar Parâmetros")

if dados:
    config = dados['config']

    novo_intervalo = st.sidebar.slider(
        "⏱️ Intervalo (segundos)",
        min_value=10,
        max_value=300,
        value=config.get('intervalo', 60),
        step=10
    )

    novo_risco = st.sidebar.slider(
        "💸 Risco por Trade (%)",
        min_value=0.5,
        max_value=5.0,
        value=config.get('risk_per_trade', 0.01) * 100,
        step=0.5
    ) / 100

    novo_stop = st.sidebar.slider(
        "🛑 Stop Loss (%)",
        min_value=0.1,
        max_value=2.0,
        value=config.get('stop_loss', 0.002) * 100,
        step=0.1
    ) / 100

    novo_take = st.sidebar.slider(
        "🎯 Take Profit (%)",
        min_value=0.1,
        max_value=5.0,
        value=config.get('take_profit', 0.005) * 100,
        step=0.1
    ) / 100

    if st.sidebar.button("💾 Salvar Parâmetros", use_container_width=True):
        novos_params = {
            'intervalo': novo_intervalo,
            'risk_per_trade': novo_risco,
            'stop_loss': novo_stop,
            'take_profit': novo_take
        }

        if atualizar_config_bot(novos_params):
            controles["novos_parametros"] = novos_params
            salvar_controles(controles)
            st.sidebar.success("✅ Parâmetros atualizados!")
            time.sleep(1)
            st.rerun()

# ========== ÁREA PRINCIPAL ==========

if dados:
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "💼 Trades", "📈 Gráficos", "📝 Logs"])

    # TAB 1: Visão Geral
    with tab1:
        st.subheader("📊 Resumo do Bot")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            lucro = dados['capital'] - dados['capital_inicial']
            lucro_pct = (lucro / dados['capital_inicial']) * 100
            st.metric(
                "💰 P&L Total",
                f"${lucro:.2f}",
                f"{lucro_pct:+.2f}%",
                delta_color="normal"
            )

        with col2:
            st.metric("💵 Capital Atual", f"${dados['capital']:.2f}")

        with col3:
            st.metric("💵 Capital Inicial", f"${dados['capital_inicial']:.2f}")

        with col4:
            trades_lucrativos = [t for t in dados['trades'] if t['pnl'] > 0]
            win_rate = (len(trades_lucrativos) / len(dados['trades']) * 100) if dados['trades'] else 0
            st.metric("🎯 Win Rate", f"{win_rate:.1f}%")

        # Posição Atual
        st.subheader("📍 Posição Atual")

        if dados.get('posicao'):
            pos = dados['posicao']

            col1, col2 = st.columns(2)

            with col1:
                st.info(f"""
                **Tipo:** {pos['tipo']}
                **Preço Entrada:** ${pos['preco_entrada']:,.2f}
                **Quantidade:** {pos['quantidade']:.6f} BTC
                **Abertura:** {pos['timestamp']}
                """)

            with col2:
                st.warning(f"""
                **Stop Loss:** ${pos['stop_loss']:,.2f}
                **Take Profit:** ${pos['take_profit']:,.2f}
                **Potencial Lucro:** +{((pos['take_profit'] - pos['preco_entrada']) / pos['preco_entrada'] * 100):.2f}%
                **Potencial Perda:** {((pos['stop_loss'] - pos['preco_entrada']) / pos['preco_entrada'] * 100):.2f}%
                """)
        else:
            st.success("✅ Nenhuma posição aberta no momento")

        # Configurações Atuais
        st.subheader("⚙️ Configurações Atuais")

        config_df = pd.DataFrame([
            {"Parâmetro": "Par de Trading", "Valor": config['symbol']},
            {"Parâmetro": "Timeframe", "Valor": config['timeframe']},
            {"Parâmetro": "Intervalo", "Valor": f"{config['intervalo']}s"},
            {"Parâmetro": "Risco/Trade", "Valor": f"{config['risk_per_trade']*100:.2f}%"},
            {"Parâmetro": "Stop Loss", "Valor": f"{config['stop_loss']*100:.2f}%"},
            {"Parâmetro": "Take Profit", "Valor": f"{config['take_profit']*100:.2f}%"},
            {"Parâmetro": "Confiança Mín.", "Valor": f"{config['ai_confidence']*100:.0f}%"},
            {"Parâmetro": "Executar Ordens", "Valor": "✅ SIM" if config['executar_ordens'] else "❌ NÃO (Simulação)"}
        ])

        st.dataframe(config_df, use_container_width=True, hide_index=True)

    # TAB 2: Trades
    with tab2:
        st.subheader("💼 Histórico de Trades")

        if dados['trades']:
            trades_df = pd.DataFrame(dados['trades'])
            trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])
            trades_df = trades_df.sort_values('timestamp', ascending=False)

            # Formatar colunas
            trades_df['pnl_formatado'] = trades_df.apply(
                lambda x: f"${x['pnl']:+.2f} ({x['pnl_percent']:+.2f}%)",
                axis=1
            )

            # Colorir P&L
            def colorir_pnl(val):
                if '+' in str(val):
                    return 'background-color: #90EE90'
                elif '-' in str(val):
                    return 'background-color: #FFB6C6'
                return ''

            trades_display = trades_df[['timestamp', 'entrada', 'saida', 'quantidade', 'pnl_formatado', 'motivo']].copy()
            trades_display.columns = ['Data/Hora', 'Entrada ($)', 'Saída ($)', 'Quantidade (BTC)', 'P&L', 'Motivo']

            st.dataframe(
                trades_display.style.applymap(colorir_pnl, subset=['P&L']),
                use_container_width=True,
                hide_index=True
            )

            # Estatísticas
            col1, col2, col3 = st.columns(3)

            with col1:
                total_lucro = sum(t['pnl'] for t in dados['trades'] if t['pnl'] > 0)
                st.metric("💚 Lucro Total", f"${total_lucro:.2f}")

            with col2:
                total_prejuizo = sum(t['pnl'] for t in dados['trades'] if t['pnl'] < 0)
                st.metric("💔 Prejuízo Total", f"${total_prejuizo:.2f}")

            with col3:
                pnl_medio = sum(t['pnl'] for t in dados['trades']) / len(dados['trades'])
                st.metric("📊 P&L Médio", f"${pnl_medio:.2f}")
        else:
            st.info("📭 Nenhum trade executado ainda")

    # TAB 3: Gráficos
    with tab3:
        st.subheader("📈 Evolução do Capital")

        if dados['trades']:
            # Criar série temporal de capital
            capital_evolution = [dados['capital_inicial']]
            for trade in dados['trades']:
                capital_evolution.append(capital_evolution[-1] + trade['pnl'])

            chart_df = pd.DataFrame({
                'Trade': range(len(capital_evolution)),
                'Capital': capital_evolution
            })

            st.line_chart(chart_df.set_index('Trade'))

            # Gráfico de P&L por trade
            st.subheader("📊 P&L por Trade")

            pnl_df = pd.DataFrame({
                'Trade': range(1, len(dados['trades']) + 1),
                'P&L': [t['pnl'] for t in dados['trades']]
            })

            st.bar_chart(pnl_df.set_index('Trade'))
        else:
            st.info("📭 Execute trades para ver gráficos")

    # TAB 4: Logs
    with tab4:
        st.subheader("📝 Logs do Bot")

        if dados.get('logs'):
            # Mostrar últimos 50 logs
            logs_recentes = dados['logs'][-50:]

            for log in reversed(logs_recentes):
                if "ERRO" in log:
                    st.error(log)
                elif "COMPRA" in log or "BUY" in log:
                    st.success(log)
                elif "VENDA" in log or "SELL" in log:
                    st.warning(log)
                elif "STOP LOSS" in log:
                    st.error(log)
                elif "TAKE PROFIT" in log:
                    st.success(log)
                else:
                    st.text(log)
        else:
            st.info("📭 Nenhum log disponível")

else:
    st.warning("⚠️ bot_dados.json não encontrado. Execute o bot primeiro!")
    st.info("Execute: EXECUTAR_BOT.bat")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("🤖 Bot Trader Dashboard v2.0")
st.sidebar.caption("⚡ Controle em Tempo Real")
st.sidebar.caption(f"🕐 Última atualização: {datetime.now().strftime('%H:%M:%S')}")
