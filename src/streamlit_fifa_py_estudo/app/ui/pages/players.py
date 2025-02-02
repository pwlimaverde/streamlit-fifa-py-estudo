import pandas as pd
import streamlit as st


def format_currency(value):
    """Formata valores monetários para formato compacto"""
    if value >= 1e9:  # bilhões
        return f"£{value / 1e9:.2f}B"
    elif value >= 1e6:  # milhões
        return f"£{value / 1e6:.2f}M"
    elif value >= 1e3:  # milhares
        return f"£{value / 1e3:.2f}K"
    else:
        return f"£{value:.0f}"


def inject_custom_css():
    st.markdown(
        """
        <style>
            .metric-container {
                display: grid;
                text-align: center;
                padding: 0.5rem;
            }

            .metric-label {
                font-size: min(max(12px, 1.1vw), 16px);
                margin-bottom: 0.2rem;
                text-align: left;
            }

            .metric-value {
                font-weight: bold;
                font-size: min(max(21px, 2.25vw), 35px);
                margin: 0;
                text-align: left;
            }
        </style>
    """, unsafe_allow_html=True
    )


def responsive_metric(container, label, value):
    inject_custom_css()
    container.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)


def players():

    df_data = pd.DataFrame(st.session_state.data)

    clubes = df_data['club'].unique()
    club = st.sidebar.selectbox('Selecione um clube', clubes)
    df_players_club = df_data[(df_data['club'] == club)]

    players = df_players_club['name'].unique()
    player = st.sidebar.selectbox('Selecione um jogador', players)

    player_stats = df_data[df_data['name'] == player].iloc[0]

    st.image(player_stats['photo'])
    st.title(player_stats['name'])
    st.markdown(f"**Clube:** {player_stats['club']}")
    st.markdown(f"**Posição:** {player_stats['position']}")

    coluna1, coluna2, coluna3, coluna4 = st.columns(4)

    coluna1.markdown(f"**Idade:** {player_stats['age']}")
    coluna2.markdown(f"**Altura:** {player_stats['height_m']}")
    coluna3.markdown(f"**Peso:** {player_stats['weight_kg']}")
    st.divider()

    st.subheader(f"**Overall:** {player_stats['overall']}")
    st.progress(player_stats['overall'] / 100)

    coluna1, coluna2, coluna3, coluna4 = st.columns(4)
    responsive_metric(
        coluna1,
        'Valor de mercado',
        format_currency(
            player_stats['value']))
    responsive_metric(
        coluna2,
        'Remuneração semanal',
        format_currency(
            player_stats['wage']))
    responsive_metric(
        coluna3,
        'Cláusula de rescisão',
        format_currency(
            player_stats['release_clause']))


players()
