import webbrowser as we

import streamlit as st

st.markdown('# FIFA23 OFICIAL DATASET! :soccer:')

botao = st.button('Acesse os dados no Kaggle')

if botao:
    we.open_new_tab(
        'https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data'
    )

st.markdown(
    """
    O conjunto de dados
    de jogadores de futebol de 2017 a 2023 fornece informações
    abrangentes sobre jogadores de futebol profissionais.
    O conjunto de dados contém uma ampla gama de atributos, incluindo dados demográficos
    do jogador, características físicas, estatísticas de jogo, detalhes do contrato e
    afiliações de clubes.

    Com **mais de 17.000 registros**, este conjunto de dados oferece um recurso valioso para
    analistas de futebol, pesquisadores e entusiastas interessados em explorar vários
    aspectos do mundo do futebol, pois permite estudar atributos de jogadores, métricas de
    desempenho, avaliação de mercado, análise de clubes, posicionamento de jogadores e
    desenvolvimento do jogador ao longo do tempo.
"""
)
