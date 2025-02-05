"""Módulo principal da aplicação FIFA Streamlit.

Este módulo configura e inicializa a aplicação Streamlit para visualização
de dados do FIFA, definindo a estrutura de navegação e páginas disponíveis.
"""

import streamlit as st
from streamlit_fifa_py_estudo.app.inicializacao import inicializacao

# Configuração das páginas de navegação
paginas = st.navigation(
    [
        st.Page(
            "app/ui/pages/home.py",
            title="Home",
            icon=":material/home:"),
        st.Page(
            "app/ui/pages/players.py",
            title="Players",
            icon=":material/folder_shared:"),
        st.Page(
            "app/ui/pages/teams.py",
            title="Teams",
            icon=":material/sports_and_outdoors:"),
    ])


def main() -> None:
    """Inicializa e executa a aplicação Streamlit.
    
    Configura o layout da página para wide, inicializa as configurações
    necessárias e executa o sistema de navegação entre páginas.
    
    Returns:
        None
    """
    st.set_page_config(layout="wide")
    inicializacao()
    paginas.run()


if __name__ == '__main__':
    main()
