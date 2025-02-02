import pandas as pd
import streamlit as st


def format_currency(value):
    return value / 1e3

def teams():

    df_data = pd.DataFrame(st.session_state.data)

    clubes = df_data['club'].unique()
    club = st.sidebar.selectbox('Selecione um clube', clubes)
    df_players_club = df_data[(df_data['club'] == club)].set_index('name')

    st.image(df_players_club.iloc[0]['club_logo'])
    st.markdown(f"## {club}")

    clunas = [
        'age',
        'photo',
        'flag',
        'overall',
        'value',
        'wage_formatted',
        'joined',
        'height_m',
        'weight_kg',
        'contract_valid_until',
        'release_clause'
    ]
    df_players_club['wage_formatted'] = df_players_club['wage'].apply(
        format_currency)

    st.dataframe(
        df_players_club[clunas],
        column_config={
            'overall': st.column_config.ProgressColumn(
                min_value=0,
                max_value=100,
                format='%d',
            ),
            'wage_formatted': st.column_config.ProgressColumn(
                'weekly wage',
                min_value=0,
                max_value=df_players_club['wage_formatted'].max(),
                format='£ %.2f K',
            ),
            'photo': st.column_config.ImageColumn(),
            'flag': st.column_config.ImageColumn('country'),
        })


teams()
