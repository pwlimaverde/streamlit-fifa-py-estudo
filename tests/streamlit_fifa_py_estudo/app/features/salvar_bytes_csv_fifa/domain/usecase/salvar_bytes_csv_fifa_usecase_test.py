from unittest.mock import Mock

import pytest
from py_return_success_or_error import ErrorReturn, SuccessReturn

from streamlit_fifa_py_estudo.app.features.salvar_bytes_csv_fifa.domain.usecase.salvar_bytes_csv_fifa_usecase import (
    SalvarBytesCsvFifaUsecase, )
from streamlit_fifa_py_estudo.app.utils.consts import PASTA_DATASETS
from streamlit_fifa_py_estudo.app.utils.erros import SaveCsvFifaError
from streamlit_fifa_py_estudo.app.utils.parameters import SaveCsvParameters


@pytest.fixture
def mock_path_file():
    return PASTA_DATASETS / "fifa_mock.csv"


def get_mock_bytes_fifa() -> bytes:
    mock_data = """,ID,Name,Age,Photo,Nationality,Flag,Overall,Potential,Club,Club Logo,Value(£),Wage(£),Special,Preferred Foot,International Reputation,Weak Foot,Skill Moves,Work Rate,Body Type,Real Face,Position,Joined,Loaned From,Contract Valid Until,Height(cm.),Weight(lbs.),Release Clause(£),Kit Number,Best Overall Rating,Year_Joined
0,209658,L. Goretzka,27,https://cdn.sofifa.net/players/209/658/23_60.png,Germany,https://cdn.sofifa.net/flags/de.png,87,88,FC Bayern München,https://cdn.sofifa.net/teams/21/30.png,91000000.0,115000.0,2312,Right,4.0,4.0,3.0,High/ Medium,Unique,Yes,SUB,2018-07-01,None,2026.0,189.0,180.81,157000000.0,8.0,0.0,2018
1,212198,Bruno Fernandes,27,https://cdn.sofifa.net/players/212/198/23_60.png,Portugal,https://cdn.sofifa.net/flags/pt.png,86,87,Manchester United,https://cdn.sofifa.net/teams/11/30.png,78500000.0,190000.0,2305,Right,3.0,3.0,4.0,High/ High,Unique,Yes,LCM,2020-01-30,None,2026.0,179.0,152.145,155000000.0,8.0,0.0,2020
2,224334,M. Acuña,30,https://cdn.sofifa.net/players/224/334/23_60.png,Argentina,https://cdn.sofifa.net/flags/ar.png,85,85,Sevilla FC,https://cdn.sofifa.net/teams/481/30.png,46500000.0,46000.0,2303,Left,2.0,3.0,3.0,High/ High,Stocky (170-185),No,LB,2020-09-14,None,2024.0,172.0,152.145,97700000.0,19.0,0.0,2020"""

    return mock_data.encode('utf-8')


def test_salvar_bytes_csv_fifa_usecase_success(mock_path_file):

    # Arrange
    error = SaveCsvFifaError()
    parameters = SaveCsvParameters(
        csv_name='fifa_mock',
        bytes_csv=get_mock_bytes_fifa(),
        error=error)

    mock_result_datasource = Mock(return_value=mock_path_file)

    usecase = SalvarBytesCsvFifaUsecase(
        datasource=mock_result_datasource,
    )
    # Act
    teste = usecase(parameters)
    # Assert
    assert isinstance(teste, SuccessReturn)
    assert teste.result == mock_path_file
    assert str(
        parameters) == "SaveCsvParameters(error=SaveCsvFifaError - Erro ao salvar o arquivo CSV, csv_name='fifa_mock'"


def test_ler_csv_fifa_usecase_error():
    # Arrange
    error = SaveCsvFifaError()
    parameters = SaveCsvParameters(
        csv_name='fifa_mock',
        bytes_csv=get_mock_bytes_fifa(),
        error=error)

    mock_result_datasource = Mock(
        side_effect=ValueError("CSV inválido: teste mock erro"))

    usecase = SalvarBytesCsvFifaUsecase(
        datasource=mock_result_datasource,
    )

    # Act
    teste = usecase(parameters)

    assert isinstance(teste, ErrorReturn)
    assert teste.result == error
    assert teste.result.message == "Erro ao salvar o arquivo CSV"
    assert str(
        teste.result) == "SaveCsvFifaError - Erro ao salvar o arquivo CSV"


def test_ler_csv_fifa_usecase_excecao(monkeypatch):
    error = SaveCsvFifaError()
    mock_result_datasource = Mock(
        side_effect=Exception())
    usecase = SalvarBytesCsvFifaUsecase(datasource=mock_result_datasource)
    parameters = SaveCsvParameters(
        csv_name='fifa_mock',
        bytes_csv=get_mock_bytes_fifa(),
        error=error)

    def mock_result(*args, **kwargs):
        raise Exception("Erro simulado")

    monkeypatch.setattr(usecase, '_resultDatasource', mock_result)

    result = usecase(parameters)
    assert isinstance(result, ErrorReturn)
    assert isinstance(result.result, SaveCsvFifaError)
    assert "Erro simulado" in str(result.result.message)
