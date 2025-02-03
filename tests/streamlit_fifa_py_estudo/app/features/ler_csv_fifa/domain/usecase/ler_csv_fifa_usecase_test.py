
from datetime import datetime
from unittest.mock import Mock

import pytest
from py_return_success_or_error import ErrorReturn, SuccessReturn

from streamlit_fifa_py_estudo.app.features.ler_csv_fifa.domain.models.fifa_player import FifaPlayer
from streamlit_fifa_py_estudo.app.features.ler_csv_fifa.domain.usecase.ler_csv_fifa_usecase import LerCsvFifaUseCase
from streamlit_fifa_py_estudo.app.utils.erros import LoadCsvFifaError
from streamlit_fifa_py_estudo.app.utils.parameters import LoadCsvParameters




@pytest.fixture
def mock_fifa_players():
    return [
        FifaPlayer(
            id=1,
            name="L. Goretzka",
            age=27,
            photo="https://cdn.sofifa.net/players/209/658/23_60.png",
            nationality="Germany",
            flag="https://cdn.sofifa.net/flags/de.png",
            overall=75,
            club="FC Bayern München",
            club_logo="https://cdn.sofifa.net/teams/21/30.png",
            value=91000000.0,
            wage=115000.0,
            position="SUB",
            joined=datetime.strptime("2018-07-01", "%Y-%m-%d").date(),
            contract_valid_until=2026.0,
            height_m=1.890,
            weight_kg=(180.81 * 0.453),
            release_clause=157000000.0,
        ),
        FifaPlayer(
            id=2,
            name="Bruno Fernandes",
            age=27,
            photo="https://cdn.sofifa.net/players/212/198/23_60.png",
            nationality="Portugal",
            flag="https://cdn.sofifa.net/flags/pt.png",
            overall=86,
            club="Manchester United",
            club_logo="https://cdn.sofifa.net/teams/11/30.png",
            value=78500000.0,
            wage=190000.0,
            position="LCM",
            joined=datetime.strptime("2020-01-30", "%Y-%m-%d").date(),
            contract_valid_until=2026.0,
            height_m=.1790,
            weight_kg=(152.145 * 0.453),
            release_clause=155000000.0,
        ),
        FifaPlayer(
            id=3,
            name="K. De Bruyne",
            age=31,
            photo="https://cdn.sofifa.net/players/192/985/23_60.png",
            nationality="Belgium",
            flag="https://cdn.sofifa.net/flags/be.png",
            overall=91,
            club="Manchester City",
            club_logo="https://cdn.sofifa.net/teams/10/30.png",
            value=107500000.0,
            wage=350000.0,
            position="RCM",
            joined=datetime.strptime("2015-08-30", "%Y-%m-%d").date(),
            contract_valid_until=2025.0,
            height_m=1.810,
            weight_kg=(154.35 * 0.453),
            release_clause=198900000.0,
        )
    ]


def test_ler_csv_fifa_usecase_success(mock_fifa_players):
    # Arrange
    error = LoadCsvFifaError()
    parameters = LoadCsvParameters(
        file_path="test.csv",
        error=error
    )

    mock_result_datasource = Mock(return_value=mock_fifa_players)

    usecase = LerCsvFifaUseCase(
        datasource=mock_result_datasource,
    )
    # Act
    teste = usecase(parameters)
    # Assert
    assert isinstance(teste, SuccessReturn)
    assert len(teste.result) == 3
    assert teste.result[0]['name'] == "K. De Bruyne"
    assert teste.result[1]['name'] == "Bruno Fernandes"
    assert teste.result[2]['name'] == "L. Goretzka"
    assert str(parameters) == "LoadCsvParameters(error=LoadCsvFifaError(message='Erro ao carregar o arquivo CSV'), file_path='test.csv')"


def test_ler_csv_fifa_usecase_error():
    # Arrange
    error = LoadCsvFifaError()
    parameters = LoadCsvParameters(
        file_path="test.csv",
        error=error
    )

    mock_result_datasource = Mock(side_effect=FileNotFoundError)

    usecase = LerCsvFifaUseCase(
        datasource=mock_result_datasource,
    )

    # Act
    teste = usecase(parameters)

    assert isinstance(teste, ErrorReturn)
    assert teste.result == error
    assert teste.result.message == "Erro ao carregar o arquivo CSV"
    assert str(
        teste.result) == "LoadCsvFifaError - Erro ao carregar o arquivo CSV"


def test_ler_csv_fifa_usecase_custom_data_exception():
    # Arrange
    error = LoadCsvFifaError()
    parameters = LoadCsvParameters(
        file_path="test.csv",
        error=error
    )

    mock_result_datasource = Mock(
        side_effect=Exception())

    usecase = LerCsvFifaUseCase(
        datasource=mock_result_datasource,
    )

    # Act
    result = usecase(parameters)

    # Assert
    assert isinstance(result, ErrorReturn)
    assert isinstance(result.result, LoadCsvFifaError)
    assert result.result.message == "Erro ao carregar o arquivo CSV"
    assert str(
        result.result) == "LoadCsvFifaError - Erro ao carregar o arquivo CSV"


def test_ler_csv_fifa_usecase_excecao(monkeypatch):
    error = LoadCsvFifaError()
    mock_result_datasource = Mock(
        side_effect=Exception())
    usecase = LerCsvFifaUseCase(datasource=mock_result_datasource)
    parameters = LoadCsvParameters(
        file_path="test.csv",
        error=error
    )

    def mock_result(*args, **kwargs):
        raise Exception("Erro simulado")

    monkeypatch.setattr(usecase, '_resultDatasource', mock_result)

    result = usecase(parameters)
    assert isinstance(result, ErrorReturn)
    assert isinstance(result.result, LoadCsvFifaError)
    assert "Erro simulado" in str(result.result.message)
