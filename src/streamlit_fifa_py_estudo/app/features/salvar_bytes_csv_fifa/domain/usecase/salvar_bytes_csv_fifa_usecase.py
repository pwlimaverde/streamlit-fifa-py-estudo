from pathlib import Path

from py_return_success_or_error import (
    ErrorReturn,
    ReturnSuccessOrError,
)

from streamlit_fifa_py_estudo.app.utils.erros import SaveCsvFifaError
from streamlit_fifa_py_estudo.app.utils.parameters import SaveCsvParameters
from streamlit_fifa_py_estudo.app.utils.types import SCFUsecase


class SalvarBytesCsvFifaUsecase(SCFUsecase):
    """Caso de uso para salvar dados de jogadores FIFA em formato CSV.

    Esta classe implementa a lógica de negócio para salvar dados recebidos em bytes
    em um arquivo CSV, utilizando um datasource específico.

    Attributes:
        _datasource (SCFData): Fonte de dados que implementa a interface SCFData.
    """

    def __call__(
            self,
            parameters: SaveCsvParameters) -> ReturnSuccessOrError[Path]:
        """Executa o caso de uso de salvamento do CSV.

        Tenta salvar os dados em bytes como um arquivo CSV usando o datasource configurado.
        Em caso de falha, retorna um erro encapsulado.

        Args:
            parameters (SaveCsvParameters): Parâmetros contendo os bytes do CSV
                e o nome do arquivo a ser salvo.

        Returns:
            ReturnSuccessOrError[Path]: 
                Em caso de sucesso: SuccessReturn contendo o caminho do arquivo salvo.
                Em caso de erro: ErrorReturn contendo SaveCsvFifaError com detalhes do erro.

        Example:
            ```python
            usecase = SalvarBytesCsvFifaUsecase(datasource)
            params = SaveCsvParameters(
                bytes_csv=csv_bytes,
                csv_name="fifa23_players"
            )
            result = usecase(params)
            if isinstance(result, SuccessReturn):
                file_path = result.result
            ```
        """
        try:
            return self._resultDatasource(
                parameters=parameters, datasource=self._datasource
            )
        except Exception as e:
            return ErrorReturn(SaveCsvFifaError(str(e)))
