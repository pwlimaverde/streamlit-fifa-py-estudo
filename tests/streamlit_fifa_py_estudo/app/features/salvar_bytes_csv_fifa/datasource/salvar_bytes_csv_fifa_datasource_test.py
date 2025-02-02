
import pytest

from streamlit_fifa_py_estudo.app.features.salvar_bytes_csv_fifa.datasource.salvar_bytes_csv_fifa_datasource import (
    SalvarBytesCsvFifaDatasource, )
from streamlit_fifa_py_estudo.app.utils.consts import PASTA_DATASETS
from streamlit_fifa_py_estudo.app.utils.erros import SaveCsvFifaError
from streamlit_fifa_py_estudo.app.utils.parameters import SaveCsvParameters


@pytest.fixture(scope="function", autouse=True)
def cleanup_fifa_mock():
    print("\nIniciando fixture de limpeza...")
    yield
    mock_file = PASTA_DATASETS / "fifa_mock.csv"
    print("\nExecutando limpeza após teste...")
    print(f"Verificando arquivo: {mock_file}")
    print(f"Arquivo existe? {mock_file.exists()}")
    if mock_file.exists():
        mock_file.unlink()
        print(f"Arquivo removido: {mock_file}")
    else:
        print("Arquivo não encontrado para remoção")


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


def get_mock_invalid_types_fifa() -> bytes:
    mock_data = """,ID,Name,Age,Photo,Nationality,Flag,Overall,Potential,Club,Club Logo,Value(£),Wage(£),Special,Preferred Foot,International Reputation,Weak Foot,Skill Moves,Work Rate,Body Type,Real Face,Position,Joined,Loaned From,Contract Valid Until,Height(cm.),Weight(lbs.),Release Clause(£),Kit Number,Best Overall Rating,Year_Joined
0,invalid_id,L. Goretzka,abc,https://photo.png,Germany,https://flag.png,not_number,88,Club,https://logo.png,invalid,115000.0,2312,Right,4.0,4.0,3.0,High/ Medium,Unique,Yes,SUB,2018-07-01,None,2026.0,189.0,180.81,157000000.0,8.0,0.0,text"""
    return mock_data.encode('utf-8')


def get_mock_corrupted_bytes_fifa() -> bytes:
    # Simula bytes corrompidos que causarão erro na leitura
    return b'\x80\x81\x82\x83'


def test_salvar_bytes_csv_fifa_datasource_with_mock_data():
    # Arrange
    error = SaveCsvFifaError()
    parameters = SaveCsvParameters(
        csv_name='fifa_mock',
        bytes_csv=get_mock_bytes_fifa(),
        error=error)

    # Act
    datasource = SalvarBytesCsvFifaDatasource()
    result = datasource(parameters)
    print()
    print(result.absolute())
    print(str(result))
    # Assert
    assert result.exists()
    assert str(result).endswith('fifa_mock.csv')


def test_salvar_bytes_csv_fifa_datasource_with_invalid_data():
    # Arrange
    error = SaveCsvFifaError()
    parameters = SaveCsvParameters(
        csv_name='fifa_mock_invalid',
        bytes_csv=get_mock_invalid_bytes_fifa(),
        error=error)

    # Act & Assert
    datasource = SalvarBytesCsvFifaDatasource()
    with pytest.raises(ValueError) as exc_info:
        datasource(parameters)

    # Verifica mensagem de erro específica
    assert "CSV inválido" in str(exc_info.value)


def test_salvar_bytes_csv_fifa_datasource_invalid_types():
    # Arrange
    error = SaveCsvFifaError()
    parameters = SaveCsvParameters(
        csv_name='fifa_mock_types',
        bytes_csv=get_mock_invalid_types_fifa(),
        error=error)

    # Act & Assert
    datasource = SalvarBytesCsvFifaDatasource()
    with pytest.raises(ValueError) as exc_info:
        datasource(parameters)

    assert "Coluna ID tem tipo" in str(exc_info.value)


def test_salvar_bytes_csv_fifa_datasource_read_error():
    # Arrange
    error = SaveCsvFifaError()
    parameters = SaveCsvParameters(
        csv_name='fifa_mock_corrupted',
        bytes_csv=get_mock_corrupted_bytes_fifa(),
        error=error)

    # Act & Assert
    datasource = SalvarBytesCsvFifaDatasource()
    with pytest.raises(ValueError) as exc_info:
        datasource(parameters)

    assert "Erro ao ler CSV" in str(exc_info.value)
