import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Relatório de Volatilidade Diária",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo personalizado
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stApp {
        background-color: black;
        color: white;
    }
    .report-title, .section-title, .content {
        text-align: center;
    }
    .report-title {
        font-size: 37.44px; /* Halved */
        font-weight: bold;
        color: white;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 30.58px; /* Halved */
        font-weight: bold;
        color: white;
        margin-top: 40px;
        margin-bottom: 20px;
    }
    .content {
        font-size: 19.66px; /* Halved */
        color: white;
        margin: 0 auto;
        max-width: 800px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Conteúdo do relatório
st.markdown('<div class="report-title">📊 INSIGHTS SOBRE A VOLATILIDADE DIÁRIA</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="content">
        A volatilidade diária foi calculada com base na diferença entre os preços mais altos (High) e mais baixos (Low) de cada dia.<br>
        A média da volatilidade diária é de <b>$1.64</b>, com um desvio padrão de <b>$0.83</b>.<br>
        O menor valor de volatilidade registrado foi de <b>$0.39</b>, enquanto o maior foi de <b>$7.75</b>.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="section-title">📋 DETALHES ADICIONAIS</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="content">
        Estatísticas adicionais:<br>
        - Mediana da volatilidade: <b>$1.43</b><br>
        - Primeiro quartil (Q1): <b>$1.10</b><br>
        - Terceiro quartil (Q3): <b>$2.00</b><br>
        - Total de dias analisados: <b>1444</b>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="section-title">📅 DIAS COM MAIOR VOLATILIDADE</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="content">
        - Data: <b>2024-12-05 00:00:00</b>, Volatilidade: <b>$7.75</b><br>
        - Data: <b>2021-04-29 00:00:00</b>, Volatilidade: <b>$6.11</b><br>
        - Data: <b>2020-03-19 00:00:00</b>, Volatilidade: <b>$5.56</b><br>
        - Data: <b>2021-03-04 00:00:00</b>, Volatilidade: <b>$5.55</b><br>
        - Data: <b>2024-08-06 00:00:00</b>, Volatilidade: <b>$5.32</b>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="section-title">💡 RECOMENDAÇÕES</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="content">
        - Dias com alta volatilidade podem indicar oportunidades para investidores ativos que buscam lucrar com oscilações rápidas.<br>
        - Para investidores mais conservadores, é importante evitar operar em dias de alta volatilidade, pois os riscos são maiores.<br>
        - Monitorar notícias e eventos externos que possam impactar o mercado é essencial para antecipar dias de alta volatilidade.
    </div>
    """,
    unsafe_allow_html=True
)
