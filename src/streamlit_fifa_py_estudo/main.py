from typing import List

import pandas as pd
import streamlit as st

from streamlit_fifa_py_estudo.app.features.features_presenter import FeaturesPresenter
from streamlit_fifa_py_estudo.app.utils.consts import PASTA_DATASETS


def select_dataset():
    presenter = FeaturesPresenter()
    coluna = 'name'
    df_datasets = pd.DataFrame(
        st.session_state.arquivos_datasets,
        columns=[coluna])

    datasets = df_datasets['name'].unique()
    dataset = st.sidebar.selectbox('Selecione a fonte de dados', datasets)
    df_list = presenter.ler_csv_fifa(PASTA_DATASETS / f'{dataset}.csv')
    st.session_state.data = df_list


def atualizar_lista_arquivos():
    paths = listar_arquivos_datasets()
    st.session_state.arquivos_datasets = paths


def listar_arquivos_datasets() -> List[str]:
    """Lista todos os arquivos CSV na pasta datasets"""
    try:
        paths = list(PASTA_DATASETS.glob('*.csv'))
        nomes_arquivos = [path.stem for path in paths]
        return nomes_arquivos
    except Exception as e:
        raise ValueError(f"Erro ao listar arquivos: {str(e)}")


def set_data():
    presenter = FeaturesPresenter()
    if 'data' not in st.session_state:
        paths = listar_arquivos_datasets()
        df_list = presenter.ler_csv_fifa(PASTA_DATASETS / f'{paths[0]}.csv')
        st.session_state.data = df_list


def upload_data():
    presenter = FeaturesPresenter()
    uploaded_file = st.sidebar.file_uploader(
        "Escolha um arquivo CSV", type="csv")
    if uploaded_file is not None:
        try:
            bytes_csv = uploaded_file.read()
            presenter.salvar_csv_fifa(
                uploaded_file.name.replace(
                    '.csv', ''), bytes_csv)

            atualizar_lista_arquivos()

            st.toast("Arquivo salvo com sucesso!", icon="✅")

        except Exception as e:
            st.toast(f"Erro ao salvar arquivo: {str(e)}", icon="❌")


def main():
    st.set_page_config(layout="wide")
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

    # Roteamento de páginas
    atualizar_lista_arquivos()
    set_data()
    upload_data()
    select_dataset()

    paginas.run()


if __name__ == '__main__':
    main()
