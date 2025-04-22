import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configurações gerais do dashboard
st.set_page_config(
    page_title="Análise de Médias Móveis - Uber Stocks",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para o tema preto e branco
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap');
    
    :root {
        --primary-color: #FFFFFF;
        --background-color: #000000;
        --accent-color: #666666;
    }
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        background-color: var(--background-color);
        color: var(--primary-color);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 500;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        border-bottom: 2px solid var(--primary-color);
    }
    
    .metric-card {
        background-color: #111111;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid var(--accent-color);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 500;
        margin: 2rem 0 1rem;
        color: var(--primary-color);
    }
    
    .insight-text {
        font-size: 1.1rem;
        line-height: 1.8;
        margin: 1rem 0;
        padding: 1rem;
        background-color: #1A1A1A;
        border-radius: 6px;
    }
    
    .plot-container {
        margin-top: 2rem;
        background-color: var(--background-color);
    }
    </style>
""", unsafe_allow_html=True)

def carregar_dados():
    """Carrega e prepara os dados"""
    try:
        dados = pd.read_csv("D:/Portfolio/Uber Stocks Dataset 2025/data/processed/uber_stock_data_atualizado.csv")
        dados['Date'] = pd.to_datetime(dados['Date'])
        return dados.sort_values('Date')
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

def criar_grafico_medias_moveis(dados, coluna_preco):
    """Cria o gráfico interativo de médias móveis"""
    fig = go.Figure()
    
    # Adiciona o preço de fechamento
    fig.add_trace(go.Scatter(
        x=dados['Date'],
        y=dados[coluna_preco],
        name='Preço de Fechamento',
        line=dict(color='white', width=2)
    ))
    
    # Adiciona médias móveis
    for periodo in [7, 30]:
        coluna = f'Media_Movel_{periodo}'
        fig.add_trace(go.Scatter(
            x=dados['Date'],
            y=dados[coluna],
            name=f'Média Móvel {periodo} dias',
            line=dict(color='grey' if periodo == 7 else 'silver', width=1.5, dash='dot')
        ))
    
    # Configuração do layout
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Data', gridcolor='#333333'),
        yaxis=dict(title='Preço ($)', gridcolor='#333333'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=40),
        height=600
    )
    
    return fig

def main():
    """Função principal da aplicação"""
    st.markdown("<div class='main-title'>📈 Análise Técnica - Ações da Uber (UBER)</div>", unsafe_allow_html=True)
    
    dados = carregar_dados()
    if dados is None:
        return
    
    # Cálculo das médias móveis
    for periodo in [7, 30]:
        dados[f'Media_Movel_{periodo}'] = dados['Close'].rolling(window=periodo).mean()
    
    # Métricas principais
    preco_atual = dados['Close'].iloc[-1]
    media_7 = dados['Media_Movel_7'].iloc[-1]
    media_30 = dados['Media_Movel_30'].iloc[-1]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class='metric-card'>
                <h3>Preço Atual</h3>
                <p style='font-size: 2rem; margin: 0.5rem 0;'>${preco_atual:.2f}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='metric-card'>
                <h3>Média 7 Dias</h3>
                <p style='font-size: 2rem; margin: 0.5rem 0;'>${media_7:.2f}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='metric-card'>
                <h3>Média 30 Dias</h3>
                <p style='font-size: 2rem; margin: 0.5rem 0;'>${media_30:.2f}</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Gráfico
    st.markdown("<div class='section-title'>Histórico de Preços e Médias Móveis</div>", unsafe_allow_html=True)
    fig = criar_grafico_medias_moveis(dados, 'Close')
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    col_insights1, col_insights2 = st.columns(2)
    
    with col_insights1:
        st.markdown("<div class='section-title'>📌 Interpretação Técnica</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class='insight-text'>
            🔍 <strong>Padrões de Mercado:</strong><br>
            - Preço acima de ambas médias → Tendência de alta consolidada<br>
            - Preço entre as médias → Mercado em transição<br>
            - Preço abaixo de ambas médias → Tendência de baixa
            </div>
        """, unsafe_allow_html=True)
    
    with col_insights2:
        st.markdown("<div class='section-title'>🎯 Recomendações Estratégicas</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class='insight-text'>
            ⚡ <strong>Ações Sugeridas:</strong><br>
            - Cruzamento ascendente → Potencial sinal de compra<br>
            - Cruzamento descendente → Considerar proteção de capital<br>
            - Divergência persistente → Reavaliar estratégia
            </div>
        """, unsafe_allow_html=True)

# Barra lateral informativa
with st.sidebar:
    st.markdown("## ℹ️ Sobre os Dados")
    st.markdown("- Período: 2019-2024")
    st.markdown("- Fonte: Yahoo Finance")
    st.markdown("- Atualização: Diária")
    st.markdown("---")
    st.markdown("## 📊 Métricas Calculadas")
    st.markdown("- Médias Móveis Simples")
    st.markdown("- Tendências de Curto/Longo Prazo")
    st.markdown("- Análise de Cruzamentos")
    st.markdown("---")
    st.markdown("**Desenvolvido por:**  \n[Seu Nome]")

if __name__ == "__main__":
    main()