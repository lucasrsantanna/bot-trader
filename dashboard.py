"""
DASHBOARD WEB - BOT TRADER
Interface visual para controlar e monitorar o bot de trading
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import os
import ccxt
from dotenv import load_dotenv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Configurar página
st.set_page_config(
    page_title="Bot Trader Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar env
load_dotenv()

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .status-running {
        color: #00ff00;
        font-weight: bold;
    }
    .status-stopped {
        color: #ff0000;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'bot_running' not in st.session_state:
    st.session_state.bot_running = False
if 'trades' not in st.session_state:
    st.session_state.trades = []
if 'capital' not in st.session_state:
    st.session_state.capital = 1000.0
if 'posicao' not in st.session_state:
    st.session_state.posicao = None
if 'historico_precos' not in st.session_state:
    st.session_state.historico_precos = []
if 'logs' not in st.session_state:
    st.session_state.logs = []

# Funções auxiliares
def adicionar_log(mensagem):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {mensagem}")
    if len(st.session_state.logs) > 50:
        st.session_state.logs = st.session_state.logs[-50:]

def coletar_dados_binance(symbol, timeframe='1m', limit=50):
    try:
        exchange = ccxt.binance({
            'apiKey': os.getenv("BINANCE_API_KEY"),
            'secret': os.getenv("BINANCE_SECRET_KEY"),
            'enableRateLimit': True,
        })
        exchange.set_sandbox_mode(True)

        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        st.error(f"Erro ao coletar dados: {e}")
        return None

def calcular_indicadores(df):
    # RSI
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # MACD
    exp1 = df["close"].ewm(span=12, adjust=False).mean()
    exp2 = df["close"].ewm(span=26, adjust=False).mean()
    df['macd'] = exp1 - exp2
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']

    # Volume MA
    df['volume_ma'] = df["volume"].rolling(window=20).mean()

    return df

def gerar_sinal(df, sentimento, confidence_threshold):
    ultimo = df.iloc[-1]

    rsi = ultimo['rsi']
    macd_hist = ultimo['macd_hist']
    volume = ultimo['volume']
    volume_ma = ultimo['volume_ma']

    sinal = "HOLD"
    confianca = 0.5

    if rsi < 30 and macd_hist > 0 and sentimento > 0.1:
        sinal = "BUY"
        confianca = 0.75
        if volume > (volume_ma * 1.5):
            confianca = min(1.0, confianca + 0.1)
    elif rsi > 70 and macd_hist < 0 and sentimento < -0.1:
        sinal = "SELL"
        confianca = 0.75
        if volume > (volume_ma * 1.5):
            confianca = min(1.0, confianca + 0.1)

    return {
        'sinal': sinal,
        'confianca': confianca,
        'rsi': rsi,
        'macd_hist': macd_hist,
        'preco': ultimo['close']
    }

# =============================================================================
# HEADER
# =============================================================================
st.markdown('<p class="main-header">📈 BOT TRADER DASHBOARD</p>', unsafe_allow_html=True)

# =============================================================================
# SIDEBAR - CONFIGURAÇÕES
# =============================================================================
st.sidebar.title("⚙️ Configurações")

st.sidebar.subheader("1. Par de Trading")
symbol = st.sidebar.selectbox(
    "Selecione o par:",
    ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT"]
)

st.sidebar.subheader("2. Parâmetros de Risco")
capital_inicial = st.sidebar.number_input(
    "Capital Inicial (USD):",
    min_value=100.0,
    max_value=100000.0,
    value=1000.0,
    step=100.0
)

risk_per_trade = st.sidebar.slider(
    "Risco por Trade (%):",
    min_value=0.1,
    max_value=5.0,
    value=1.0,
    step=0.1
) / 100

stop_loss = st.sidebar.slider(
    "Stop Loss (%):",
    min_value=0.1,
    max_value=2.0,
    value=0.2,
    step=0.1
) / 100

take_profit = st.sidebar.slider(
    "Take Profit (%):",
    min_value=0.1,
    max_value=5.0,
    value=0.5,
    step=0.1
) / 100

st.sidebar.subheader("3. Inteligência Artificial")
ai_confidence = st.sidebar.slider(
    "Confiança Mínima da IA (%):",
    min_value=50,
    max_value=95,
    value=70,
    step=5
) / 100

st.sidebar.subheader("4. Execução")
executar_ordens = st.sidebar.checkbox(
    "🚨 Executar Ordens Reais",
    value=False,
    help="ATENÇÃO: Apenas para Testnet!"
)

intervalo = st.sidebar.select_slider(
    "Intervalo de Atualização:",
    options=[10, 30, 60, 120, 300],
    value=60,
    format_func=lambda x: f"{x}s"
)

st.sidebar.markdown("---")

# Botões de controle
col_start, col_stop = st.sidebar.columns(2)

if col_start.button("▶️ Iniciar", use_container_width=True):
    st.session_state.bot_running = True
    st.session_state.capital = capital_inicial
    adicionar_log("Bot iniciado!")
    st.rerun()

if col_stop.button("⏹️ Parar", use_container_width=True):
    st.session_state.bot_running = False
    adicionar_log("Bot parado!")
    st.rerun()

# =============================================================================
# MAIN CONTENT
# =============================================================================

# Status do Bot
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.session_state.bot_running:
        st.markdown("### 🟢 Status: <span class='status-running'>RODANDO</span>", unsafe_allow_html=True)
    else:
        st.markdown("### 🔴 Status: <span class='status-stopped'>PARADO</span>", unsafe_allow_html=True)

with col2:
    st.metric(
        "💰 Capital",
        f"${st.session_state.capital:.2f}",
        f"{st.session_state.capital - capital_inicial:+.2f}"
    )

with col3:
    st.metric(
        "📊 Trades",
        len(st.session_state.trades)
    )

with col4:
    if st.session_state.posicao:
        st.metric("📍 Posição", "ABERTA", "LONG")
    else:
        st.metric("📍 Posição", "FECHADA", "-")

st.markdown("---")

# =============================================================================
# DADOS EM TEMPO REAL
# =============================================================================

if st.session_state.bot_running or st.button("🔄 Atualizar Dados Manualmente"):
    # Coletar dados
    with st.spinner("Coletando dados da Binance..."):
        df = coletar_dados_binance(symbol)

    if df is not None:
        # Calcular indicadores
        df = calcular_indicadores(df)

        # Dados atuais
        preco_atual = df['close'].iloc[-1]
        rsi_atual = df['rsi'].iloc[-1]
        macd_hist_atual = df['macd_hist'].iloc[-1]

        # Adicionar ao histórico
        st.session_state.historico_precos.append({
            'timestamp': datetime.now(),
            'preco': preco_atual
        })
        if len(st.session_state.historico_precos) > 100:
            st.session_state.historico_precos = st.session_state.historico_precos[-100:]

        # Gerar sinal
        sentimento = 0.05  # Simplificado
        analise = gerar_sinal(df, sentimento, ai_confidence)

        # =============================================================================
        # MÉTRICAS PRINCIPAIS
        # =============================================================================
        st.subheader("📊 Métricas em Tempo Real")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Preço", f"${preco_atual:,.2f}")

        with col2:
            delta_color = "normal" if 30 <= rsi_atual <= 70 else "inverse"
            st.metric("RSI", f"{rsi_atual:.1f}",
                     "Sobrecomprado" if rsi_atual > 70 else ("Sobrevendido" if rsi_atual < 30 else "Normal"),
                     delta_color=delta_color)

        with col3:
            st.metric("MACD Hist", f"{macd_hist_atual:.2f}")

        with col4:
            sinal_emoji = "🟢" if analise['sinal'] == "BUY" else ("🔴" if analise['sinal'] == "SELL" else "🟡")
            st.metric("Sinal IA", f"{sinal_emoji} {analise['sinal']}")

        with col5:
            confianca_color = "normal" if analise['confianca'] >= ai_confidence else "inverse"
            st.metric("Confiança", f"{analise['confianca']:.0%}", delta_color=confianca_color)

        st.markdown("---")

        # =============================================================================
        # GRÁFICOS
        # =============================================================================
        tab1, tab2, tab3 = st.tabs(["📈 Preço & Indicadores", "📊 RSI", "💹 MACD"])

        with tab1:
            # Gráfico de Candlestick
            fig = go.Figure()

            # Candlestick
            fig.add_trace(go.Candlestick(
                x=df['timestamp'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='Preço'
            ))

            # Volume
            colors = ['red' if df['close'].iloc[i] < df['open'].iloc[i] else 'green'
                     for i in range(len(df))]

            fig.add_trace(go.Bar(
                x=df['timestamp'],
                y=df['volume'],
                name='Volume',
                marker_color=colors,
                yaxis='y2',
                opacity=0.3
            ))

            fig.update_layout(
                title=f'{symbol} - Gráfico de Preço',
                yaxis_title='Preço (USD)',
                yaxis2=dict(title='Volume', overlaying='y', side='right'),
                xaxis_rangeslider_visible=False,
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            # Gráfico RSI
            fig_rsi = go.Figure()

            fig_rsi.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['rsi'],
                mode='lines',
                name='RSI',
                line=dict(color='blue', width=2)
            ))

            # Linhas de referência
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Sobrecomprado")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Sobrevendido")
            fig_rsi.add_hline(y=50, line_dash="dot", line_color="gray")

            fig_rsi.update_layout(
                title='Índice de Força Relativa (RSI)',
                yaxis_title='RSI',
                xaxis_title='Tempo',
                height=400
            )

            st.plotly_chart(fig_rsi, use_container_width=True)

        with tab3:
            # Gráfico MACD
            fig_macd = go.Figure()

            fig_macd.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['macd'],
                mode='lines',
                name='MACD',
                line=dict(color='blue')
            ))

            fig_macd.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['macd_signal'],
                mode='lines',
                name='Signal',
                line=dict(color='orange')
            ))

            # Histograma
            colors_macd = ['green' if val >= 0 else 'red' for val in df['macd_hist']]
            fig_macd.add_trace(go.Bar(
                x=df['timestamp'],
                y=df['macd_hist'],
                name='Histogram',
                marker_color=colors_macd
            ))

            fig_macd.update_layout(
                title='MACD (Moving Average Convergence Divergence)',
                yaxis_title='Valor',
                xaxis_title='Tempo',
                height=400
            )

            st.plotly_chart(fig_macd, use_container_width=True)

        # =============================================================================
        # DECISÃO DA IA
        # =============================================================================
        st.markdown("---")
        st.subheader("🤖 Decisão da Inteligência Artificial")

        col1, col2 = st.columns([2, 1])

        with col1:
            if analise['confianca'] >= ai_confidence:
                if analise['sinal'] == "BUY":
                    st.success(f"✅ **SINAL DE COMPRA** com {analise['confianca']:.0%} de confiança")
                    st.write(f"**Recomendação:** Executar ordem de COMPRA")
                    st.write(f"- Preço de Entrada: ${analise['preco']:,.2f}")
                    st.write(f"- Stop Loss: ${analise['preco'] * (1-stop_loss):,.2f}")
                    st.write(f"- Take Profit: ${analise['preco'] * (1+take_profit):,.2f}")
                elif analise['sinal'] == "SELL":
                    st.warning(f"🔻 **SINAL DE VENDA** com {analise['confianca']:.0%} de confiança")
                else:
                    st.info(f"➡️ **MANTER POSIÇÃO** ({analise['confianca']:.0%} confiança)")
            else:
                st.info(f"⏸️ **AGUARDAR** - Confiança ({analise['confianca']:.0%}) abaixo do limite ({ai_confidence:.0%})")

        with col2:
            st.metric("RSI Atual", f"{analise['rsi']:.2f}")
            st.metric("MACD Hist", f"{analise['macd_hist']:.4f}")
            st.metric("Sentimento", f"{sentimento:.3f}")

        # Logs
        adicionar_log(f"Dados atualizados - Preço: ${preco_atual:,.2f}, Sinal: {analise['sinal']} ({analise['confianca']:.0%})")

# =============================================================================
# HISTÓRICO DE TRADES
# =============================================================================
st.markdown("---")
st.subheader("📜 Histórico de Trades")

if st.session_state.trades:
    df_trades = pd.DataFrame(st.session_state.trades)
    st.dataframe(df_trades, use_container_width=True)

    # Estatísticas
    total_pnl = df_trades['pnl'].sum()
    trades_lucrativos = len(df_trades[df_trades['pnl'] > 0])
    win_rate = (trades_lucrativos / len(df_trades) * 100) if len(df_trades) > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("P&L Total", f"${total_pnl:+.2f}")
    with col2:
        st.metric("Trades Lucrativos", f"{trades_lucrativos}/{len(df_trades)}")
    with col3:
        st.metric("Win Rate", f"{win_rate:.1f}%")
else:
    st.info("Nenhum trade executado ainda.")

# =============================================================================
# LOGS
# =============================================================================
st.markdown("---")
st.subheader("📋 Registro de Atividades")

if st.session_state.logs:
    log_text = "\n".join(st.session_state.logs[-20:])  # Últimos 20 logs
    st.text_area("Logs:", log_text, height=200)
else:
    st.info("Nenhuma atividade registrada.")

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem;'>
    <p>Bot Trader Dashboard v1.0 | Criado com Streamlit ❤️</p>
    <p><strong>⚠️ AVISO:</strong> Use apenas na Testnet. Trading envolve riscos.</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh se o bot estiver rodando
if st.session_state.bot_running:
    time.sleep(intervalo)
    st.rerun()
