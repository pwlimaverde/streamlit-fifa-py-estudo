
import pandas as pd
import pytest

from streamlit_fifa_py_estudo.app.features.features_presenter import FeaturesPresenter
from streamlit_fifa_py_estudo.app.utils.erros import LoadCsvFifaError



def test_features_presenter_with_mock_data():
    # Arrange
    presenter = FeaturesPresenter()

    teste = presenter.ler_csv_fifa(
        'c:/PROJETOS/PYTHON/APPS/asimov/tests/asimov/projetos/streamlit_fifa/app/features/mock_presenter.csv',)
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
