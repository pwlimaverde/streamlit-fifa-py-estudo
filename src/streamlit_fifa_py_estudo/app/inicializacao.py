from typing import List

import pandas as pd
import streamlit as st

from streamlit_fifa_py_estudo.app.features.features_presenter import FeaturesPresenter
from streamlit_fifa_py_estudo.app.utils.consts import PASTA_DATASETS


def atualizar_lista_arquivos():
    """Atualiza a lista de arquivos datasets na sessão do Streamlit.

    Obtém a lista de arquivos de datasets disponíveis e armazena na variável
    de sessão 'arquivos_datasets' do Streamlit.
    """
    paths = listar_arquivos_datasets()
    st.session_state.arquivos_datasets = paths


def set_data():
    """Inicializa os dados na sessão do Streamlit.

    Verifica se já existem dados carregados na sessão. Caso não existam,
    carrega o primeiro arquivo CSV da lista de datasets disponíveis e
    armazena na variável de sessão 'data'.
    """
    presenter = FeaturesPresenter()
    if 'data' not in st.session_state:
        paths = listar_arquivos_datasets()
        df_list = presenter.ler_csv_fifa(PASTA_DATASETS / f'{paths[0]}.csv')
        st.session_state.data = df_list


def upload_data():
    """Permite fazer upload de arquivo CSV via interface do Streamlit.

    Cria um componente de upload de arquivo na sidebar do Streamlit que aceita
    arquivos CSV. Quando um arquivo é carregado, seus bytes são lidos para
    posterior processamento.

    Returns:
        bytes: Conteúdo do arquivo CSV em formato de bytes se um arquivo
            for carregado.
    """
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


def listar_arquivos_datasets() -> List[str]:
    """Lista todos os arquivos CSV disponíveis na pasta datasets.

    Busca recursivamente todos os arquivos com extensão .csv no diretório
    definido em PASTA_DATASETS e retorna uma lista com os nomes dos arquivos
    sem a extensão.

    Returns:
        List[str]: Lista contendo os nomes dos arquivos CSV encontrados,
            sem a extensão .csv.

    Raises:
        ValueError: Se ocorrer algum erro durante a listagem dos arquivos,
            com a mensagem de erro detalhada.
    """
    try:
        paths = list(PASTA_DATASETS.glob('*.csv'))
        nomes_arquivos = [path.stem for path in paths]
        return nomes_arquivos
    except Exception as e:
        raise ValueError(f"Erro ao listar arquivos: {str(e)}")


def select_dataset():
    """Permite selecionar um dataset através da interface do Streamlit.

    Cria um componente de seleção na interface que lista os datasets disponíveis.
    Quando um dataset é selecionado, seus dados são carregados na sessão do Streamlit
    através do FeaturesPresenter.

    Args:
        None

    Returns:
        None

    Example:
        O usuário pode selecionar um dataset da lista suspensa e os dados
        serão automaticamente carregados na sessão do Streamlit para uso
        posterior na aplicação.
    """
    presenter = FeaturesPresenter()
    coluna = 'name'
    df_datasets = pd.DataFrame(
        st.session_state.arquivos_datasets,
        columns=[coluna])

    datasets = df_datasets['name'].unique()
    dataset = st.sidebar.selectbox('Selecione a fonte de dados', datasets)
    df_list = presenter.ler_csv_fifa(PASTA_DATASETS / f'{dataset}.csv')
    st.session_state.data = df_list


def inicializacao():
    # execução das funções de inicialização
    atualizar_lista_arquivos()
    set_data()
    upload_data()
    select_dataset()
