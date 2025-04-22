import streamlit as st
import pandas as pd
import plotly.express as px  # Importação faltante
import seaborn as sns
import matplotlib.pyplot as plt

# Configuração inicial do Streamlit
st.set_page_config(
    page_title="Análise de Abertura e Fechamento - Uber Stocks",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Atualize o CSS no início do código
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    
    .main {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    .main-font {
        font-size: 18px;  /* Aumentado de 16px */
        line-height: 1.8;  /* Mais espaçamento entre linhas */
        color: #FFFFFF;
        margin-bottom: 25px;  /* Espaço entre parágrafos */
    }
    
    .header-style {
        color: #FFFFFF;
        font-size: 26px;  /* Aumentado de 24px */
        margin: 40px 0 25px 0;  /* Mais espaço acima e abaixo */
        padding-bottom: 12px;
        border-bottom: 2px solid #FFFFFF;
        font-weight: 500;
    }
    
    .bullet-point {
        margin-left: 25px;  /* Indentação aumentada */
        margin-bottom: 15px;  /* Espaço entre bullets */
        font-size: 18px;
    }
    
    .metric-value {
        font-weight: 500;  /* Peso da fonte ajustado */
        color: #F8F9FA;
        letter-spacing: 0.5px;
    }
    
    .stPlotlyChart {
        margin-top: 30px !important;  /* Espaço acima do gráfico */
    }
    
    /* Aumentar espaçamento geral entre seções */
    .stMarkdown {
        margin-bottom: 40px !important;
    }
    </style>
""", unsafe_allow_html=True)


# Função para análise (mantida igual)
def analisar_diferenca_abertura_fechamento(dados, coluna_abertura, coluna_fechamento):
    if coluna_abertura not in dados.columns or coluna_fechamento not in dados.columns:
        st.error("As colunas especificadas não existem no DataFrame.")
        return None

    dados['Diferenca'] = dados[coluna_fechamento] - dados[coluna_abertura]
    dias_fechamento_maior = (dados['Diferenca'] > 0).sum()
    estatisticas_diferenca = dados['Diferenca'].describe()

    insights = {
        "resumo": {
            "dias_fechamento_maior": dias_fechamento_maior,
            "media": estatisticas_diferenca['mean'],
            "mediana": estatisticas_diferenca['50%'],
            "maximo": estatisticas_diferenca['max'],
            "minimo": estatisticas_diferenca['min']
        },
        "interpretacao": "Diferenças positivas sugerem otimismo no mercado, enquanto diferenças negativas indicam pessimismo.",
        "recomendacoes": [
            "Monitorar dias com grandes diferenças para identificar eventos impactantes.",
            "Usar a análise como indicador para estratégias de day trading.",
            "Incluir variáveis como volume negociado para análises mais completas."
        ]
    }

    return insights

# Carregar dados
data_path = "D:/Portfolio/Uber Stocks Dataset 2025/data/processed/uber_stock_data_atualizado.csv"
dados = pd.read_csv(data_path)

# Título do dashboard
st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>Dashboard de Análise: Diferença entre Abertura e Fechamento</h1>", 
            unsafe_allow_html=True)

# Colunas fixas para análise
coluna_abertura = "Open"
coluna_fechamento = "Close"

# Análise e exibição de insights
insights = analisar_diferenca_abertura_fechamento(dados, coluna_abertura, coluna_fechamento)

if insights:
    # Seção de Resumo
    st.markdown("<div class='header-style'>Resumo dos Insights</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class='main-font'>
            <div class='bullet-point'>Em <span class='metric-value'>{insights['resumo']['dias_fechamento_maior']}</span> dias, o preço de fechamento foi maior que o de abertura</div>
            <div class='bullet-point'>Estatísticas descritivas da diferença:</div>
            <div style='margin-left: 40px;'>
                • Média: <span class='metric-value'>{insights['resumo']['media']:.2f}</span><br>
                • Mediana: <span class='metric-value'>{insights['resumo']['mediana']:.2f}</span><br>
                • Máximo: <span class='metric-value'>{insights['resumo']['maximo']:.2f}</span><br>
                • Mínimo: <span class='metric-value'>{insights['resumo']['minimo']:.2f}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Seção de Interpretação
    st.markdown("<div class='header-style' style='margin-top: 30px;'>Interpretação</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class='main-font'>
            {insights["interpretacao"]}
        </div>
    """, unsafe_allow_html=True)

    # Seção de Recomendações
    st.markdown("<div class='header-style' style='margin-top: 30px;'>Recomendações</div>", unsafe_allow_html=True)
    recomendacoes_html = "<div class='main-font'>" + "".join(
        [f"<div class='bullet-point'>{recomendacao}</div>" for recomendacao in insights['recomendacoes']]
    ) + "</div>"
    st.markdown(recomendacoes_html, unsafe_allow_html=True)

    # Gráfico interativo com tema escuro
    st.markdown("<div class='header-style' style='margin-top: 30px;'>Distribuição das Diferenças (Fechamento - Abertura)</div>", 
                unsafe_allow_html=True)
    fig = px.histogram(
        dados,
        x="Diferenca",
        nbins=30,
        color_discrete_sequence=["#FFFFFF"],  # Barras brancas
        template="plotly_dark",  # Tema escuro
        opacity=0.7
    )
    fig.update_traces(
        marker_line_color="#000000",  # Contorno preto
        marker_line_width=1
    )
    # No layout do gráfico, atualize os tamanhos das fontes:
    fig.update_layout(
        font=dict(size=14, color="#FFFFFF"),  # Aumentado de 12px
        xaxis=dict(
            title_font=dict(size=16),  # Aumentado de 14px
            tickfont=dict(size=14)     # Aumentado de 12px
        ),
        yaxis=dict(
            title_font=dict(size=16),  # Aumentado de 14px
            tickfont=dict(size=14)     # Aumentado de 12px
        )
)
    st.plotly_chart(fig, use_container_width=True)