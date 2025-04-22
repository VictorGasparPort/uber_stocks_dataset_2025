import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import pearsonr, spearmanr

# Configurações gerais do dashboard
st.set_page_config(
    page_title="Análise Completa - Uber Stocks",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS unificado para todo o dashboard
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
        margin: 2rem 0;
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
    
    .insight-box {
        background-color: #1A1A1A;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        border: 1px solid #333333;
    }
    
    .insight-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #CCCCCC;
    }
    
    .recommendation-list {
        margin-left: 2rem;
        list-style-type: circle;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    try:
        dados = pd.read_csv("D:/Portfolio/Uber Stocks Dataset 2025/data/processed/uber_stock_data_atualizado.csv")
        dados['Date'] = pd.to_datetime(dados['Date'])
        return dados.sort_values('Date')
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

def home():
    st.markdown("<div class='main-title'>🚕 Análise Completa das Ações da Uber</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,6,1])
    with col2:
        st.image("https://logos-world.net/wp-content/uploads/2021/08/Uber-Logo.png", width=300)
    
    st.markdown("""
    <div class='insight-box'>
        <div class='insight-text'>
        <h3 style='color: #FFFFFF; margin-bottom: 1rem;'>Sobre o Dashboard</h3>
        Análise técnica completa das ações da Uber Technologies Inc. (NYSE: UBER) contendo:
        <ul class='recommendation-list'>
            <li>Análise de tendências históricas</li>
            <li>Padrões de volatilidade diária</li>
            <li>Comportamento sazonal</li>
            <li>Relação volume-preço</li>
            <li>Indicadores técnicos avançados</li>
        </ul>
        Dados históricos desde o IPO até a atualidade
        </div>
    </div>
    """, unsafe_allow_html=True)

def pagina_abertura_fechamento():
    dados = carregar_dados()
    if dados is None:
        return

    st.markdown("<div class='main-title'>📈 Diferença Abertura-Fechamento</div>", unsafe_allow_html=True)
    
    # Análise
    dados['Diferenca'] = dados['Close'] - dados['Open']
    estatisticas = dados['Diferenca'].describe()
    dias_positivos = (dados['Diferenca'] > 0).sum()

    # Métricas
    cols = st.columns(4)
    metrics = [
        ("Dias Positivos", dias_positivos, ""),
        ("Média Diária", estatisticas['mean'], "$"),
        ("Máxima Diária", estatisticas['max'], "$"),
        ("Mínima Diária", estatisticas['min'], "$")
    ]
    
    for col, (title, value, prefix) in zip(cols, metrics):
        with col:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>{title}</h3>
                    <p style='font-size: 2rem; margin: 0.5rem 0;'>{prefix}{value:,.2f}</p>
                </div>
            """, unsafe_allow_html=True)

    # Gráfico
    st.markdown("<div class='section-title'>Distribuição das Diferenças Diárias</div>", unsafe_allow_html=True)
    fig = px.histogram(dados, x="Diferenca", nbins=50, template="plotly_dark")
    fig.update_traces(marker_color='#FFFFFF', marker_line_color='#000000')
    st.plotly_chart(fig, use_container_width=True)

    # Insights
    st.markdown("""
    <div class='insight-box'>
        <div class='insight-text'>
            <h3 style='color: #FFFFFF; margin-bottom: 1rem;'>📌 Interpretação Técnica</h3>
            A diferença diária entre os preços de abertura e fechamento revela:
            <ul class='recommendation-list'>
                <li>Dias positivos indicam fechamento acima da abertura (otimismo)</li>
                <li>Amplitude média de $%.2f mostra volatilidade intraday</li>
                <li>Máxima histórica de $%.2f em 05/12/2024</li>
            </ul>
        </div>
    </div>
    """ % (estatisticas['mean'], estatisticas['max']), unsafe_allow_html=True)

    st.markdown("""
    <div class='insight-box'>
        <div class='insight-text'>
            <h3 style='color: #FFFFFF; margin-bottom: 1rem;'>🎯 Recomendações Estratégicas</h3>
            <ul class='recommendation-list'>
                <li>Monitorar dias com diferenças superiores a $5.00</li>
                <li>Considerar estratégias de day trading em dias voláteis</li>
                <li>Correlacionar com volume negociado para confirmação</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

def pagina_volatilidade():
    dados = carregar_dados()
    if dados is None:
        return

    st.markdown("<div class='main-title'>📉 Análise de Volatilidade</div>", unsafe_allow_html=True)
    
    # Cálculos
    dados['Volatilidade'] = dados['High'] - dados['Low']
    estatisticas = dados['Volatilidade'].describe()
    top5 = dados.nlargest(5, 'Volatilidade')

    # Métricas
    cols = st.columns(3)
    metrics = [
        ("Média Diária", estatisticas['mean'], "$"),
        ("Máxima Histórica", estatisticas['max'], "$"),
        ("Dias > $5.00", sum(dados['Volatilidade'] > 5), "")
    ]
    
    for col, (title, value, prefix) in zip(cols, metrics):
        with col:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>{title}</h3>
                    <p style='font-size: 2rem; margin: 0.5rem 0;'>{prefix}{value:,.2f}</p>
                </div>
            """, unsafe_allow_html=True)

    # Gráfico
    st.markdown("<div class='section-title'>Top 5 Dias Mais Voláteis</div>", unsafe_allow_html=True)
    fig = px.bar(
        top5,
        x="Date",
        y="Volatilidade",
        template="plotly_dark",
        text="Volatilidade",
        color_discrete_sequence=["#FFFFFF"]
    )
    fig.update_traces(texttemplate='$%{text:.2f}')
    st.plotly_chart(fig, use_container_width=True)

    # Insights
    st.markdown("""
    <div class='insight-box'>
        <div class='insight-text'>
            <h3 style='color: #FFFFFF; margin-bottom: 1rem;'>📌 Padrões de Volatilidade</h3>
            <ul class='recommendation-list'>
                <li>Picos de volatilidade correlacionados com eventos macroeconômicos</li>
                <li>Média histórica de $%.2f por dia</li>
                <li>25%% dos dias com volatilidade acima de $%.2f</li>
            </ul>
        </div>
    </div>
    """ % (estatisticas['mean'], estatisticas['75%']), unsafe_allow_html=True)

    st.markdown("""
    <div class='insight-box'>
        <div class='insight-text'>
            <h3 style='color: #FFFFFF; margin-bottom: 1rem;'>🎯 Estratégias Recomendadas</h3>
            <ul class='recommendation-list'>
                <li>Usar ordens stop-loss em dias de alta volatilidade</li>
                <li>Aproveitar oportunidades de arbitragem</li>
                <li>Monitorar notícias em dias com volatilidade acima da média</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

def pagina_medias_moveis():
    dados = carregar_dados()
    if dados is None:
        return

    st.markdown("<div class='main-title'>📊 Médias Móveis</div>", unsafe_allow_html=True)
    
    # Cálculos
    dados['MM7'] = dados['Close'].rolling(7).mean()
    dados['MM30'] = dados['Close'].rolling(30).mean()
    cruzamentos = sum((dados['MM7'] > dados['MM30']).diff() == True)

    # Métricas
    cols = st.columns(3)
    metrics = [
        ("Média 7 Dias", dados['MM7'].iloc[-1], "$"),
        ("Média 30 Dias", dados['MM30'].iloc[-1], "$"),
        ("Cruzamentos", cruzamentos, "")
    ]
    
    for col, (title, value, prefix) in zip(cols, metrics):
        with col:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>{title}</h3>
                    <p style='font-size: 2rem; margin: 0.5rem 0;'>{prefix}{value:,.2f}</p>
                </div>
            """, unsafe_allow_html=True)

    # Gráfico
    st.markdown("<div class='section-title'>Comparativo de Médias Móveis</div>", unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dados['Date'], y=dados['Close'], name='Preço', line=dict(color='white')))
    fig.add_trace(go.Scatter(x=dados['Date'], y=dados['MM7'], name='MM7', line=dict(color='#1E90FF', dash='dot')))
    fig.add_trace(go.Scatter(x=dados['Date'], y=dados['MM30'], name='MM30', line=dict(color='#00BFFF', dash='dot')))
    fig.update_layout(template="plotly_dark", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # Insights
    st.markdown("""
    <div class='insight-box'>
        <div class='insight-text'>
            <h3 style='color: #FFFFFF; margin-bottom: 1rem;'>📌 Sinais Técnicos</h3>
            <ul class='recommendation-list'>
                <li>MM7 acima da MM30: Tendência de alta</li>
                <li>MM7 abaixo da MM30: Tendência de baixa</li>
                <li>%d cruzamentos significativos no período</li>
            </ul>
        </div>
    </div>
    """ % cruzamentos, unsafe_allow_html=True)

    st.markdown("""
    <div class='insight-box'>
        <div class='insight-text'>
            <h3 style='color: #FFFFFF; margin-bottom: 1rem;'>🎯 Estratégias de Trading</h3>
            <ul class='recommendation-list'>
                <li>Comprar em cruzamentos ascendentes</li>
                <li>Vender parcial em cruzamentos descendentes</li>
                <li>Usar como filtro para outras estratégias</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

def pagina_volume_preco():
    dados = carregar_dados()
    if dados is None:
        return

    st.markdown("<div class='main-title'>🔍 Volume vs Preço</div>", unsafe_allow_html=True)
    
    # Cálculos
    corr_pearson, p_pearson = pearsonr(dados['Volume'], dados['Close'])
    corr_spearman, p_spearman = spearmanr(dados['Volume'], dados['Close'])

    # Métricas
    cols = st.columns(2)
    metrics = [
        ("Correlação Pearson", corr_pearson, ""),
        ("Correlação Spearman", corr_spearman, "")
    ]
    
    for col, (title, value, prefix) in zip(cols, metrics):
        with col:
            st.markdown(f"""
                <div class='metric-card'>
                    <h3>{title}</h3>
                    <p style='font-size: 2rem; margin: 0.5rem 0;'>{prefix}{value:.2f}</p>
                </div>
            """, unsafe_allow_html=True)

    # Gráfico
    st.markdown("<div class='section-title'>Relação Volume-Preço</div>", unsafe_allow_html=True)
    fig = px.scatter(
        dados,
        x="Volume",
        y="Close",
        trendline="lowess",
        template="plotly_dark",
        color_discrete_sequence=["#00FF7F"]
    )
    fig.update_traces(marker=dict(size=5, opacity=0.5))
    st.plotly_chart(fig, use_container_width=True)

    # Insights
    st.markdown("""
    <div class='insight-box'>
        <div class='insight-text'>
            <h3 style='color: #FFFFFF; margin-bottom: 1rem;'>📌 Interpretação Estatística</h3>
            <ul class='recommendation-list'>
                <li>Correlação Pearson (linear): %.2f</li>
                <li>Correlação Spearman (monotônica): %.2f</li>
                <li>p-valor Pearson: %.4f</li>
            </ul>
        </div>
    </div>
    """ % (corr_pearson, corr_spearman, p_pearson), unsafe_allow_html=True)

    st.markdown("""
    <div class='insight-box'>
        <div class='insight-text'>
            <h3 style='color: #FFFFFF; margin-bottom: 1rem;'>🎯 Ações Recomendadas</h3>
            <ul class='recommendation-list'>
                <li>Validar sinais de volume com análise técnica</li>
                <li>Considerar anomalias de volume para reversões</li>
                <li>Integrar a análise em modelos preditivos</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

def pagina_sazonalidade():
    dados = carregar_dados()
    if dados is None:
        return

    st.markdown("<div class='main-title'>📅 Padrões Sazonais</div>", unsafe_allow_html=True)
    
    # Processamento
    dados['Mês'] = dados['Date'].dt.month_name()
    media_mensal = dados.groupby('Mês')['Close'].mean().reset_index()

    # Gráfico
    st.markdown("<div class='section-title'>Desempenho Mensal Médio</div>", unsafe_allow_html=True)
    fig = px.line(
        media_mensal,
        x="Mês",
        y="Close",
        template="plotly_dark",
        markers=True,
        color_discrete_sequence=["#FFD700"]
    )
    fig.update_traces(line_width=3)
    st.plotly_chart(fig, use_container_width=True)

    # Insights
    melhor_mes = media_mensal.loc[media_mensal['Close'].idxmax()]
    pior_mes = media_mensal.loc[media_mensal['Close'].idxmin()]

    st.markdown("""
    <div class='insight-box'>
        <div class='insight-text'>
            <h3 style='color: #FFFFFF; margin-bottom: 1rem;'>📌 Tendências Sazonais</h3>
            <ul class='recommendation-list'>
                <li>Melhor desempenho em <b>%s</b> (Média: $%.2f)</li>
                <li>Pior desempenho em <b>%s</b> (Média: $%.2f)</li>
                <li>Amplitude sazonal: $%.2f</li>
            </ul>
        </div>
    </div>
    """ % (melhor_mes['Mês'], melhor_mes['Close'], pior_mes['Mês'], pior_mes['Close'], 
          melhor_mes['Close'] - pior_mes['Close']), unsafe_allow_html=True)

    st.markdown("""
    <div class='insight-box'>
        <div class='insight-text'>
            <h3 style='color: #FFFFFF; margin-bottom: 1rem;'>🎯 Estratégias Sazonais</h3>
            <ul class='recommendation-list'>
                <li>Aumentar exposição em meses fortes</li>
                <li>Proteger posições em meses fracos</li>
                <li>Considerar efeitos calendário</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sistema de navegação
paginas = {
    "Home": home,
    "Abertura vs Fechamento": pagina_abertura_fechamento,
    "Volatilidade Diária": pagina_volatilidade,
    "Médias Móveis": pagina_medias_moveis,
    "Volume vs Preço": pagina_volume_preco,
    "Padrões Sazonais": pagina_sazonalidade
}

with st.sidebar:
    st.markdown("## 🗂️ Navegação")
    pagina_selecionada = st.radio("Selecione a Análise:", list(paginas.keys()))
    
    st.markdown("---")
    st.markdown("**Fonte dos Dados:**  \nYahoo Finance")
    st.markdown("**Período Analisado:**  \n2019-2024")
    st.markdown("---")
    st.markdown("**Desenvolvido por:**  \n[Seu Nome]")

# Executar a página selecionada
paginas[pagina_selecionada]()