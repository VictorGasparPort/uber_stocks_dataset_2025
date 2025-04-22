import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt

# Função de análise
def analisar_relacao_volume_preco(dados, coluna_volume, coluna_preco):
    """
    Analisa a relação entre o volume negociado e o preço de fechamento.

    Parâmetros:
    - dados (pd.DataFrame): DataFrame contendo os dados de mercado.
    - coluna_volume (str): Nome da coluna com o volume negociado.
    - coluna_preco (str): Nome da coluna com o preço de fechamento.

    Retorna:
    - dict: Insights detalhados sobre a relação entre volume e preço de fechamento.
    """
    # Verificar se as colunas existem no DataFrame
    if coluna_volume not in dados.columns or coluna_preco not in dados.columns:
        raise ValueError("As colunas especificadas não existem no DataFrame.")

    # Estatísticas descritivas
    estatisticas_volume = dados[coluna_volume].describe()
    estatisticas_preco = dados[coluna_preco].describe()

    # Calcular a correlação de Pearson e Spearman
    correlacao_pearson, p_valor_pearson = pearsonr(dados[coluna_volume], dados[coluna_preco])
    correlacao_spearman, p_valor_spearman = spearmanr(dados[coluna_volume], dados[coluna_preco])

    # Criar gráfico interativo com Plotly
    import plotly.express as px

    fig = px.scatter(
        dados,
        x=coluna_volume,
        y=coluna_preco,
        title="Relação entre Volume Negociado e Preço de Fechamento",
        labels={coluna_volume: "Volume Negociado", coluna_preco: "Preço de Fechamento ($)"},
        opacity=0.6,
    )
    fig.update_layout(
        title_font_size=24,
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        margin=dict(l=0, r=0, t=50, b=0),  # Ajustar margens para ocupar toda a largura
    )
    st.plotly_chart(fig, use_container_width=True)  # Permitir que o gráfico ocupe toda a largura

    # Insights detalhados
    insights = {
        "resumo": f"""
        <div style='background-color: white; color: black; padding: 15px; border-radius: 10px;'>
            <h3 style='color: black;'>📊 Resumo da Análise</h3>
            <p>A análise da relação entre o volume negociado e o preço de fechamento revelou os seguintes pontos:</p>
            <ul>
                <li>Correlação de Pearson: {correlacao_pearson:.2f} (p-valor: {p_valor_pearson:.4f})</li>
                <li>Correlação de Spearman: {correlacao_spearman:.2f} (p-valor: {p_valor_spearman:.4f})</li>
            </ul>
        </div>
        """,
        "estatisticas_volume": f"""
        <div style='background-color: white; color: black; padding: 15px; border-radius: 10px; margin-top: 20px;'>
            <h3 style='color: black;'>📈 Estatísticas Descritivas do Volume</h3>
            <ul>
                <li>Média: {estatisticas_volume['mean']:.2f}</li>
                <li>Mediana: {estatisticas_volume['50%']:.2f}</li>
                <li>Máximo: {estatisticas_volume['max']:.2f}</li>
                <li>Mínimo: {estatisticas_volume['min']:.2f}</li>
            </ul>
        </div>
        """,
        "estatisticas_preco": f"""
        <div style='background-color: white; color: black; padding: 15px; border-radius: 10px; margin-top: 20px;'>
            <h3 style='color: black;'>📉 Estatísticas Descritivas do Preço de Fechamento</h3>
            <ul>
                <li>Média: {estatisticas_preco['mean']:.2f}</li>
                <li>Mediana: {estatisticas_preco['50%']:.2f}</li>
                <li>Máximo: {estatisticas_preco['max']:.2f}</li>
                <li>Mínimo: {estatisticas_preco['min']:.2f}</li>
            </ul>
        </div>
        """,
        "interpretacao": """
        <div style='background-color: white; color: black; padding: 15px; border-radius: 10px; margin-top: 20px;'>
            <h3 style='color: black;'>🔍 Interpretação</h3>
            <p>A correlação de Pearson mede a relação linear entre o volume negociado e o preço de fechamento.</p>
            <p>Já a correlação de Spearman avalia a relação monotônica entre as variáveis:</p>
            <ul>
                <li>Valores próximos de 1 indicam uma forte correlação positiva.</li>
                <li>Valores próximos de -1 indicam uma forte correlação negativa.</li>
                <li>Valores próximos de 0 indicam pouca ou nenhuma correlação.</li>
            </ul>
        </div>
        """,
        "recomendacoes": [
            """
            <div style='background-color: white; color: black; padding: 15px; border-radius: 10px; margin-top: 20px;'>
                <h3 style='color: black;'>💡 Recomendações</h3>
                <ul>
                    <li>Se a correlação for significativa, considere monitorar o volume negociado como um indicador para prever movimentos no preço de fechamento.</li>
                    <li>Realize análises adicionais para identificar fatores externos que possam influenciar tanto o volume quanto o preço.</li>
                    <li>Considere criar modelos preditivos que incluam o volume como uma variável explicativa para o preço de fechamento.</li>
                </ul>
            </div>
            """
        ]
    }

    return insights

# Interface do Streamlit
st.set_page_config(layout="wide")  # Configurar layout para ocupar toda a largura
st.title("Análise da Relação entre Volume e Preço de Fechamento")

# Carregar o DataFrame diretamente do caminho especificado
caminho_arquivo = r"D:\Portfolio\Uber Stocks Dataset 2025\data\processed\uber_stock_data_atualizado.csv"
try:
    dados = pd.read_csv(caminho_arquivo)

    # Chamada da função e exibição dos insights
    insights_relacao = analisar_relacao_volume_preco(dados, 'Volume', 'Close')

    #st.subheader("Resumo da Análise")
    st.markdown(f"<div style='font-size: 24px;'>{insights_relacao['resumo']}</div>", unsafe_allow_html=True)

    #st.subheader("Estatísticas Descritivas do Volume")
    st.markdown(f"<div style='font-size: 24px;'>{insights_relacao['estatisticas_volume']}</div>", unsafe_allow_html=True)

    #st.subheader("Estatísticas Descritivas do Preço de Fechamento")
    st.markdown(f"<div style='font-size: 24px;'>{insights_relacao['estatisticas_preco']}</div>", unsafe_allow_html=True)

    #st.subheader("Interpretação")
    st.markdown(f"<div style='font-size: 24px;'>{insights_relacao['interpretacao']}</div>", unsafe_allow_html=True)

    #st.subheader("Recomendações")
    for recomendacao in insights_relacao["recomendacoes"]:
        st.markdown(f"<div style='font-size: 24px;'>- {recomendacao}</div>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error(f"Arquivo não encontrado no caminho: {caminho_arquivo}")
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
