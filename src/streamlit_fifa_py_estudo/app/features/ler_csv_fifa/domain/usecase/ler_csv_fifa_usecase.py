from datetime import datetime
from typing import List

from py_return_success_or_error import (
    ErrorReturn,
    ReturnSuccessOrError,
    SuccessReturn,
)

from streamlit_fifa_py_estudo.app.features.ler_csv_fifa.domain.models.fifa_player import (
    FifaPlayer, )
from streamlit_fifa_py_estudo.app.utils.erros import LoadCsvFifaError
from streamlit_fifa_py_estudo.app.utils.parameters import LoadCsvParameters
from streamlit_fifa_py_estudo.app.utils.types import LCFUsecase


class LerCsvFifaUseCase(LCFUsecase):
    """Caso de uso para leitura e processamento de dados de jogadores do FIFA 23 de um CSV.

    Esta classe implementa a lógica de negócio para carregar dados de jogadores,
    aplicar filtros e ordenação, e converter os resultados em dicionários.

    Attributes:
        _datasource (LCFData): Fonte de dados que implementa a interface LCFData.
    """

    def __call__(
            self, parameters: LoadCsvParameters) -> ReturnSuccessOrError[List[dict]]:
        """Executa o caso de uso de leitura do CSV.

        Carrega os dados do CSV, aplica filtros para remover jogadores inativos
        ou com overall 0, ordena por overall e converte para dicionários.

        Args:
            parameters (LoadCsvParameters): Parâmetros para carregamento do CSV,
                incluindo o caminho do arquivo.

        Returns:
            ReturnSuccessOrError[List[dict]]:
                Em caso de sucesso: SuccessReturn contendo lista de dicionários com dados dos jogadores.
                Em caso de erro: ErrorReturn contendo detalhes do erro ocorrido.

        Example:
            ```python
            usecase = LerCsvFifaUseCase(datasource)
            params = LoadCsvParameters(file_path="fifa23.csv")
            result = usecase(params)
            if isinstance(result, SuccessReturn):
                players = result.result
            ```
        """
        # class responsável pelo tratamento da lista List[FifaPlayer] que vem
        # do datasource
        try:
            result_dict: List[dict] = []
            result = self._resultDatasource(
                parameters=parameters, datasource=self._datasource
            )
            if isinstance(result, SuccessReturn):
                data: List[FifaPlayer] = result.result
                data = [
                    player for player in data if player.overall > 0 and int(
                        player.contract_valid_until) >= datetime.today().year
                ]
                data = sorted(data, key=lambda x: x.overall, reverse=True)

                result_dict = [player.to_dict() for player in data]

            if isinstance(result, ErrorReturn):
                return result

            return SuccessReturn(result_dict)
        except Exception as e:
            return ErrorReturn(LoadCsvFifaError(str(e)))
