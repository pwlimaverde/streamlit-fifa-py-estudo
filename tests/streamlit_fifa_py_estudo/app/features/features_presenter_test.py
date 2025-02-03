
import pandas as pd
import pytest

from streamlit_fifa_py_estudo.app.features.features_presenter import FeaturesPresenter
from streamlit_fifa_py_estudo.app.utils.consts import PASTA_DATASETS
from streamlit_fifa_py_estudo.app.utils.erros import LoadCsvFifaError, SaveCsvFifaError


@pytest.fixture(scope="function", autouse=True)
def cleanup_fifa_mock():
    yield
    mock_file = PASTA_DATASETS / "fifa_mock.csv"
    if mock_file.exists():
        mock_file.unlink()


def get_mock_bytes_fifa() -> bytes:
    mock_data = """,ID,Name,Age,Photo,Nationality,Flag,Overall,Potential,Club,Club Logo,Value(£),Wage(£),Special,Preferred Foot,International Reputation,Weak Foot,Skill Moves,Work Rate,Body Type,Real Face,Position,Joined,Loaned From,Contract Valid Until,Height(cm.),Weight(lbs.),Release Clause(£),Kit Number,Best Overall Rating,Year_Joined
0,209658,L. Goretzka,27,https://cdn.sofifa.net/players/209/658/23_60.png,Germany,https://cdn.sofifa.net/flags/de.png,87,88,FC Bayern München,https://cdn.sofifa.net/teams/21/30.png,91000000.0,115000.0,2312,Right,4.0,4.0,3.0,High/ Medium,Unique,Yes,SUB,2018-07-01,None,2026.0,189.0,180.81,157000000.0,8.0,0.0,2018
1,212198,Bruno Fernandes,27,https://cdn.sofifa.net/players/212/198/23_60.png,Portugal,https://cdn.sofifa.net/flags/pt.png,86,87,Manchester United,https://cdn.sofifa.net/teams/11/30.png,78500000.0,190000.0,2305,Right,3.0,3.0,4.0,High/ High,Unique,Yes,LCM,2020-01-30,None,2026.0,179.0,152.145,155000000.0,8.0,0.0,2020
2,224334,M. Acuña,30,https://cdn.sofifa.net/players/224/334/23_60.png,Argentina,https://cdn.sofifa.net/flags/ar.png,85,85,Sevilla FC,https://cdn.sofifa.net/teams/481/30.png,46500000.0,46000.0,2303,Left,2.0,3.0,3.0,High/ High,Stocky (170-185),No,LB,2020-09-14,None,2024.0,172.0,152.145,97700000.0,19.0,0.0,2020"""

    return mock_data.encode('utf-8')


def get_mock_invalid_bytes_fifa() -> bytes:
    # CSV inválido: colunas faltando e tipos errados
    mock_data = """,ID,Name
0,abc,123,
1,def,xyz,"""
    return mock_data.encode('utf-8')


def test_features_presenter_with_mock_data():
    # Arrange
    presenter = FeaturesPresenter()

    teste = presenter.ler_csv_fifa(
        'C:/PROJETOS/PYTHON/APPS/streamlit-fifa-py-estudo/tests/streamlit_fifa_py_estudo/app/datasets/mock_data.csv',)
    print()

    assert len(teste) == 2
    assert teste[0]['name'] == 'L. Goretzka'
    assert teste[1]['name'] == 'Bruno Fernandes'


def test_features_presenter_file_not_found():
    # Arrange
    presenter = FeaturesPresenter()
    invalid_path = "invalid/path/file.csv"

    # Act/Assert
    with pytest.raises(FileNotFoundError) as exc_info:
        presenter.ler_csv_fifa(invalid_path)
    assert str(exc_info.value) == f"Arquivo não encontrado: {invalid_path}"


def test_features_presenter_invalid_csv_data(tmp_path):
    # Arrange
    presenter = FeaturesPresenter()
    invalid_csv = tmp_path / "invalid.csv"

    # Create invalid CSV file with missing required columns
    invalid_data = {
        'Column1': [1, 2, 3],
        'Column2': ['A', 'B', 'C']
    }
    df = pd.DataFrame(invalid_data)
    df.to_csv(invalid_csv, index=False)

    # Act/Assert
    try:
        presenter.ler_csv_fifa(str(invalid_csv))
        assert False, "Esperava-se um erro LoadCsvFifaError"
    except LoadCsvFifaError as exc:
        assert str(exc) == 'LoadCsvFifaError - Erro ao carregar o arquivo CSV'


def test_features_presenter_salvar_csv_fifa():
    # Arrange
    presenter = FeaturesPresenter()

    # Act
    result = presenter.salvar_csv_fifa(
        csv_name='fifa_mock',
        bytes_csv=get_mock_bytes_fifa())

    # Assert
    assert result == PASTA_DATASETS / "fifa_mock.csv"
    assert result.exists()


def test_features_presenter_salvar_csv_fifa_invalid_data():
    # Arrange
    presenter = FeaturesPresenter()

    # Act & Assert
    with pytest.raises(SaveCsvFifaError) as exc_info:
        presenter.salvar_csv_fifa(
            csv_name='fifa_mock_invalid',
            bytes_csv=get_mock_invalid_bytes_fifa())

    # Verifica mensagem de erro específica
    assert "SaveCsvFifaError - Erro ao salvar o arquivo CSV" in str(
        exc_info.value)
