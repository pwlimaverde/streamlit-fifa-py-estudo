

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

