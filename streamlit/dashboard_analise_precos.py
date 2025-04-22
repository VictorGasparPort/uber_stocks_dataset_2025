import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(page_title="Análise das Ações da Uber", layout="wide", initial_sidebar_state="expanded")

# CSS personalizado para melhor estilização
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #1E3D59;
        font-size: 2.5rem !important;
    }
    .stSubheader {
        color: #2B4F76;
    }
    .spacer {
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Título centralizado e maior
st.markdown("<h1 style='text-align: center; font-size: 5rem;'>Análise das Ações da Uber</h1>", unsafe_allow_html=True)
st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)  # Espaço adicional

# Função para carregar dados
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Month'] = data['Date'].dt.month
    data['Month_Name'] = data['Date'].dt.strftime('%B')
    return data

try:
    # Carregando dados
    data = load_data('../data/processed/uber_stock_data_atualizado.csv')
    
    # Análise da Evolução do Preço
    st.markdown("<h1 style='text-align: center;'>Evolução dos preços das ações</h1>", unsafe_allow_html=True)  # Título centralizado
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)  # Espaço adicional

    # Criando gráfico interativo de tendência
    fig_trend = px.line(data, x='Date', y='Adj Close', 
                        template='plotly_white')  # Removido o title do px.line

    fig_trend.update_traces(line_color='#FFFFFF', line_width=1)
    fig_trend.update_layout(
        height=600,
        title_text='',  # Remove o título interno do gráfico
        xaxis_title="Data",
        yaxis_title="Preço ($)",
        title_x=0.5,
        margin=dict(t=20),  # Reduz espaço superior
        showlegend=False
    )

    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)  # Espaço adicional

    # Análise Mensal
    st.markdown("<h1 style='text-align: center;'>Distribuição Mensal dos Preços</h1>", unsafe_allow_html=True)  # Título centralizado
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)  # Espaço adicional

    # Criando box plot mensal

    fig_box = px.box(data, x='Month_Name', y='Adj Close', 
                    template='plotly_white')
    fig_box.update_traces(line_color='#FFFFFF', line_width=3)
    fig_box.update_layout(
        height=600,
        title_text='',  # Remove o título do gráfico
        xaxis_title="Mês",
        yaxis_title="Preço ($)",
        margin=dict(t=10),  # Reduz espaço superior do gráfico
        showlegend=False
    )

    st.plotly_chart(fig_box, use_container_width=True)

    # Insights da Análise
    st.subheader("Principais Insights")
    
    # Calculando insights
    monthly_avg = data.groupby('Month_Name')['Adj Close'].mean().sort_values()
    top_months = monthly_avg.nlargest(3).index.tolist()
    bottom_months = monthly_avg.nsmallest(3).index.tolist()
    
    # CSS personalizado para os insights
    st.markdown("""
        <style>
        .insight-box {
            background-color: white;
            color: black;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            font-size: 18px;
            line-height: 1.6;
        }
        .insight-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)
    # Calculando insights aprimorados
    monthly_avg = data.groupby('Month')['Adj Close'].mean()
    monthly_avg_sorted = monthly_avg.sort_values()
    top_months = monthly_avg_sorted.nlargest(3).index.tolist()
    bottom_months = monthly_avg_sorted.nsmallest(3).index.tolist()

    # Mapeando os números dos meses para nomes
    month_mapping = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
                     7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
    top_months_names = [month_mapping[month] for month in top_months]
    bottom_months_names = [month_mapping[month] for month in bottom_months]

    # Exibindo insights em formato vertical com melhorias
    st.markdown(f"""
    <div class="insight-box" style="background-color: white; border-radius: 10px; color: black; padding: 20px;">
        <div class="insight-title" style="font-size: 24px; font-weight: bold; margin-bottom: 15px;">📈 Análise de Tendência</div>
        - A ação mostrou crescimento significativo desde seu IPO em 2019<br>
        - Negociação inicial em torno de $41<br>
        - Faixa atual de negociação: $64-70<br>
        - Demonstra forte valorização a longo prazo
    </div>
    
    <div class="insight-box" style="background-color: white; border-radius: 10px; color: black; padding: 20px;">
        <div class="insight-title" style="font-size: 24px; font-weight: bold; margin-bottom: 15px;">📊 Padrões Sazonais</div>
        - <b>Meses de Pico (maior preço médio):</b> {', '.join(top_months_names)}<br>
        - <b>Meses de Baixa (menor preço médio):</b> {', '.join(bottom_months_names)}<br>
        - Diferença média entre os meses de pico e baixa: ${monthly_avg_sorted.max() - monthly_avg_sorted.min():.2f}
    </div>
    """, unsafe_allow_html=True)
    # Recomendações de Investimento
    st.subheader("💡 Recomendações de Investimento")
    
    # CSS personalizado para as recomendações
    st.markdown("""
        <style>
        .investment-rec {
            background-color: white;
            color: black;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            font-size: 18px;
            line-height: 1.6;
        }
        .rec-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="investment-rec">
        <div class="rec-title">1. Investidores de Longo Prazo:</div>
        • Considere comprar durante meses historicamente baixos<br>
        • Foco em manter posições por períodos prolongados
    </div>
    
    <div class="investment-rec">
        <div class="rec-title">2. Traders Ativos:</div>
        • Monitore padrões sazonais para potenciais pontos de entrada e saída<br>
        • Preste atenção aos meses historicamente altos e baixos
    </div>
    
    <div class="investment-rec">
        <div class="rec-title">3. Gestão de Risco:</div>
        • Sempre considere as condições do mercado e notícias da empresa<br>
        • Diversifique os investimentos adequadamente
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
