

from unittest.mock import patch

import pandas as pd
import pytest

from streamlit_fifa_py_estudo.app.features.ler_csv_fifa.datasource.load_csv_pandas_datasource import (
    LoadCsvPandasDatasource, )
from streamlit_fifa_py_estudo.app.utils.erros import LoadCsvFifaError
from streamlit_fifa_py_estudo.app.utils.parameters import LoadCsvParameters


def test_load_csv_pandas_datasource_with_mock_data():
    # Arrange
    error = LoadCsvFifaError()
    parameters = LoadCsvParameters(
        file_path='c:/PROJETOS/PYTHON/APPS/asimov/tests/asimov/projetos/streamlit_fifa/app/features/ler_csv_fifa/datasource/mock_data.csv',
        error=error)

    # Act
    datasource = LoadCsvPandasDatasource()
    result = datasource(parameters)

    # Assert
    assert len(result) == 3
    assert result[0].name == 'L. Goretzka'
    assert result[0].age == 27
    assert result[0].overall == 87
    assert result[1].name == 'Bruno Fernandes'
    assert result[2].name == 'M. Acuña'


def test_load_csv_pandas_datasource_with_empty_data():
    # Arrange
    mock_df = pd.DataFrame()
    error = LoadCsvFifaError()
    parameters = LoadCsvParameters(file_path='dummy_path', error=error)

    # Act
    with patch('pandas.read_csv', return_value=mock_df):
        datasource = LoadCsvPandasDatasource()
        result = datasource(parameters)

    # Assert
    assert len(result) == 0


def test_load_csv_pandas_datasource_file_not_found():
    # Arrange
    error = LoadCsvFifaError()
    parameters = LoadCsvParameters(
        file_path='non_existent_file.csv', error=error)

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        datasource = LoadCsvPandasDatasource()
        datasource(parameters)
