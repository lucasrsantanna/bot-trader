"""
PAINEL DE INSIGHTS - Bot Trader
Análises automáticas e recomendações
"""
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Insights - Bot Trader",
    page_icon="💡",
    layout="wide"
)

DADOS_FILE = "bot_dados.json"

def carregar_dados():
    if os.path.exists(DADOS_FILE):
        with open(DADOS_FILE, 'r') as f:
            return json.load(f)
    return None

def analisar_performance(dados):
    """Analisa performance e gera insights"""
    insights = []

    # Capital
    capital_atual = dados['capital']
    capital_inicial = dados['capital_inicial']
    variacao = capital_atual - capital_inicial
    variacao_pct = (variacao / capital_inicial) * 100

    if variacao_pct > 10:
        insights.append({
            "tipo": "success",
            "titulo": "🎉 Excelente Performance!",
            "mensagem": f"Lucro de {variacao_pct:.2f}%! Continue com a estratégia atual.",
            "acao": "Mantenha os parâmetros"
        })
    elif variacao_pct > 0:
        insights.append({
            "tipo": "info",
            "titulo": "👍 Performance Positiva",
            "mensagem": f"Lucro de {variacao_pct:.2f}%. Está no caminho certo!",
            "acao": "Continue monitorando"
        })
    elif variacao_pct > -10:
        insights.append({
            "tipo": "warning",
            "titulo": "⚠️ Prejuízo Moderado",
            "mensagem": f"Prejuízo de {abs(variacao_pct):.2f}%. Considere ajustar estratégia.",
            "acao": "Revise Stop Loss e Take Profit"
        })
    else:
        insights.append({
            "tipo": "error",
            "titulo": "🚨 Prejuízo Significativo",
            "mensagem": f"Prejuízo de {abs(variacao_pct):.2f}%. Ação necessária!",
            "acao": "Pause o bot e revise completamente a estratégia"
        })

    # Win Rate
    if dados['trades']:
        lucrativos = [t for t in dados['trades'] if t['pnl'] > 0]
        win_rate = (len(lucrativos) / len(dados['trades'])) * 100

        if win_rate >= 60:
            insights.append({
                "tipo": "success",
                "titulo": "🎯 Excelente Win Rate!",
                "mensagem": f"{win_rate:.1f}% de trades lucrativos. Estratégia muito eficaz!",
                "acao": "Pode aumentar ligeiramente o risco por trade"
            })
        elif win_rate >= 40:
            insights.append({
                "tipo": "info",
                "titulo": "📊 Win Rate Aceitável",
                "mensagem": f"{win_rate:.1f}% de trades lucrativos. Normal para trading.",
                "acao": "Mantenha o foco na gestão de risco"
            })
        else:
            insights.append({
                "tipo": "warning",
                "titulo": "⚠️ Win Rate Baixo",
                "mensagem": f"Apenas {win_rate:.1f}% de trades lucrativos.",
                "acao": "Considere aumentar Take Profit ou apertar Stop Loss"
            })

        # Sequências
        sequencia_atual = 0
        ultimo_resultado = None

        for trade in reversed(dados['trades'][-5:]):
            resultado = "lucro" if trade['pnl'] > 0 else "prejuizo"

            if ultimo_resultado == resultado:
                sequencia_atual += 1
            else:
                break

            ultimo_resultado = resultado

        if sequencia_atual >= 3:
            if ultimo_resultado == "prejuizo":
                insights.append({
                    "tipo": "error",
                    "titulo": "🔴 Sequência de Prejuízos",
                    "mensagem": f"{sequencia_atual} prejuízos seguidos. Mercado pode estar contra você.",
                    "acao": "PAUSE o bot e aguarde condições melhores"
                })
            else:
                insights.append({
                    "tipo": "success",
                    "titulo": "🟢 Sequência de Lucros",
                    "mensagem": f"{sequencia_atual} lucros seguidos! Está em boa fase.",
                    "acao": "Continue, mas não aumente o risco"
                })

    # Análise de Stop Loss
    config = dados['config']
    stop_loss_pct = config['stop_loss'] * 100
    take_profit_pct = config['take_profit'] * 100
    ratio = take_profit_pct / stop_loss_pct if stop_loss_pct > 0 else 0

    if ratio < 2:
        insights.append({
            "tipo": "warning",
            "titulo": "⚠️ Ratio Risk/Reward Baixo",
            "mensagem": f"Ratio atual: 1:{ratio:.1f}. Idealmente deveria ser 1:2 ou maior.",
            "acao": f"Aumente Take Profit para {stop_loss_pct * 2:.2f}% ou reduza Stop Loss"
        })
    elif ratio >= 2:
        insights.append({
            "tipo": "success",
            "titulo": "✅ Bom Ratio Risk/Reward",
            "mensagem": f"Ratio 1:{ratio:.1f} é adequado para trading.",
            "acao": "Mantenha esses valores"
        })

    # Análise de intervalo
    intervalo = config['intervalo']

    if intervalo < 30:
        insights.append({
            "tipo": "info",
            "titulo": "⚡ Intervalo Muito Rápido",
            "mensagem": f"Analisando a cada {intervalo}s. Muitas operações podem gerar overtrading.",
            "acao": "Considere aumentar para 60s se houver muitos trades pequenos"
        })
    elif intervalo > 120:
        insights.append({
            "tipo": "info",
            "titulo": "🐢 Intervalo Lento",
            "mensagem": f"Analisando a cada {intervalo}s. Pode perder oportunidades.",
            "acao": "Considere reduzir para 60s se houver poucas operações"
        })

    return insights

def analisar_trades_recentes(dados):
    """Analisa últimos trades para insights"""
    insights = []

    if not dados['trades']:
        return insights

    # Últimos 5 trades
    ultimos = dados['trades'][-5:]

    # P&L médio
    pnl_medio = sum(t['pnl'] for t in ultimos) / len(ultimos)

    if pnl_medio > 10:
        insights.append({
            "tipo": "success",
            "titulo": "💰 Últimos Trades Lucrativos",
            "mensagem": f"P&L médio dos últimos {len(ultimos)} trades: ${pnl_medio:.2f}",
            "acao": "Estratégia está funcionando bem!"
        })
    elif pnl_medio < -10:
        insights.append({
            "tipo": "error",
            "titulo": "💸 Últimos Trades Negativos",
            "mensagem": f"P&L médio dos últimos {len(ultimos)} trades: ${pnl_medio:.2f}",
            "acao": "Revise a estratégia urgentemente"
        })

    # Motivos de fechamento
    stop_loss_count = sum(1 for t in ultimos if t['motivo'] == 'STOP LOSS')
    take_profit_count = sum(1 for t in ultimos if t['motivo'] == 'TAKE PROFIT')

    if stop_loss_count > take_profit_count * 2:
        insights.append({
            "tipo": "warning",
            "titulo": "🛑 Muitos Stop Loss",
            "mensagem": f"{stop_loss_count} Stop Loss vs {take_profit_count} Take Profit nos últimos trades",
            "acao": "Considere alargar o Stop Loss ou apertar critério de entrada"
        })

    return insights

def recomendacoes_acao(dados):
    """Gera recomendações de ação"""
    recomendacoes = []

    # Verificar posição atual
    if dados.get('posicao'):
        pos = dados['posicao']

        # Tempo em posição
        abertura = datetime.fromisoformat(pos['timestamp'])
        tempo_aberto = (datetime.now() - abertura).total_seconds() / 60

        if tempo_aberto > 60:
            recomendacoes.append({
                "tipo": "warning",
                "titulo": "⏰ Posição Aberta Há Muito Tempo",
                "mensagem": f"Posição {pos['tipo']} aberta há {int(tempo_aberto)} minutos",
                "acao": "Considere fechar manualmente se não está movimentando"
            })

    else:
        recomendacoes.append({
            "tipo": "info",
            "titulo": "💤 Sem Posição Aberta",
            "mensagem": "Bot está aguardando condições ideais para entrar",
            "acao": "Aguarde sinal de BUY ou force entrada se vir oportunidade"
        })

    # Verificar capital
    capital_atual = dados['capital']
    capital_inicial = dados['capital_inicial']

    if capital_atual < capital_inicial * 0.7:
        recomendacoes.append({
            "tipo": "error",
            "titulo": "🚨 Capital em Nível Crítico",
            "mensagem": f"Você perdeu {((capital_inicial - capital_atual) / capital_inicial * 100):.1f}% do capital",
            "acao": "PARE O BOT e revise completamente a estratégia"
        })

    return recomendacoes

# Interface
st.title("💡 Painel de Insights - Bot Trader")

dados = carregar_dados()

if dados:
    # Botão de atualizar
    if st.button("🔄 Atualizar Insights", type="primary"):
        st.rerun()

    st.markdown("---")

    # Análise de Performance
    st.header("📊 Análise de Performance")

    insights_perf = analisar_performance(dados)

    for insight in insights_perf:
        if insight["tipo"] == "success":
            st.success(f"**{insight['titulo']}**\n\n{insight['mensagem']}\n\n✅ **Ação:** {insight['acao']}")
        elif insight["tipo"] == "warning":
            st.warning(f"**{insight['titulo']}**\n\n{insight['mensagem']}\n\n⚠️ **Ação:** {insight['acao']}")
        elif insight["tipo"] == "error":
            st.error(f"**{insight['titulo']}**\n\n{insight['mensagem']}\n\n🚨 **Ação:** {insight['acao']}")
        else:
            st.info(f"**{insight['titulo']}**\n\n{insight['mensagem']}\n\n💡 **Ação:** {insight['acao']}")

    st.markdown("---")

    # Análise de Trades Recentes
    st.header("📈 Análise de Trades Recentes")

    insights_trades = analisar_trades_recentes(dados)

    if insights_trades:
        for insight in insights_trades:
            if insight["tipo"] == "success":
                st.success(f"**{insight['titulo']}**\n\n{insight['mensagem']}\n\n✅ **Ação:** {insight['acao']}")
            elif insight["tipo"] == "error":
                st.error(f"**{insight['titulo']}**\n\n{insight['mensagem']}\n\n🚨 **Ação:** {insight['acao']}")
            else:
                st.warning(f"**{insight['titulo']}**\n\n{insight['mensagem']}\n\n⚠️ **Ação:** {insight['acao']}")
    else:
        st.info("Execute alguns trades para ver análises detalhadas")

    st.markdown("---")

    # Recomendações
    st.header("🎯 Recomendações de Ação")

    recomendacoes = recomendacoes_acao(dados)

    for rec in recomendacoes:
        if rec["tipo"] == "error":
            st.error(f"**{rec['titulo']}**\n\n{rec['mensagem']}\n\n🚨 **Ação:** {rec['acao']}")
        elif rec["tipo"] == "warning":
            st.warning(f"**{rec['titulo']}**\n\n{rec['mensagem']}\n\n⚠️ **Ação:** {rec['acao']}")
        else:
            st.info(f"**{rec['titulo']}**\n\n{rec['mensagem']}\n\n💡 **Ação:** {rec['acao']}")

    st.markdown("---")

    # Métricas Rápidas
    st.header("⚡ Métricas Rápidas")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        variacao = ((dados['capital'] - dados['capital_inicial']) / dados['capital_inicial']) * 100
        st.metric("ROI", f"{variacao:+.2f}%")

    with col2:
        if dados['trades']:
            lucrativos = [t for t in dados['trades'] if t['pnl'] > 0]
            win_rate = (len(lucrativos) / len(dados['trades'])) * 100
            st.metric("Win Rate", f"{win_rate:.1f}%")
        else:
            st.metric("Win Rate", "0%")

    with col3:
        if dados['trades']:
            pnl_medio = sum(t['pnl'] for t in dados['trades']) / len(dados['trades'])
            st.metric("P&L Médio", f"${pnl_medio:.2f}")
        else:
            st.metric("P&L Médio", "$0.00")

    with col4:
        config = dados['config']
        ratio = (config['take_profit'] / config['stop_loss']) if config['stop_loss'] > 0 else 0
        st.metric("Risk/Reward", f"1:{ratio:.1f}")

else:
    st.warning("⚠️ bot_dados.json não encontrado!")
    st.info("Execute o bot primeiro: EXECUTAR_BOT.bat")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("💡 Painel de Insights v1.0")
st.sidebar.caption(f"🕐 {datetime.now().strftime('%H:%M:%S')}")
