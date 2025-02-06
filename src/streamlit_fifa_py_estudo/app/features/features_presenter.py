from pathlib import Path
from typing import List

from py_return_success_or_error import (
    ErrorReturn,
    SuccessReturn,
)

from streamlit_fifa_py_estudo.app.features.ler_csv_fifa.datasource.load_csv_pandas_datasource import (
    LoadCsvPandasDatasource, )
from streamlit_fifa_py_estudo.app.features.ler_csv_fifa.domain.usecase.ler_csv_fifa_usecase import (
    LerCsvFifaUseCase, )
from streamlit_fifa_py_estudo.app.features.salvar_bytes_csv_fifa.datasource.salvar_bytes_csv_fifa_datasource import (
    SalvarBytesCsvFifaDatasource, )
from streamlit_fifa_py_estudo.app.features.salvar_bytes_csv_fifa.domain.usecase.salvar_bytes_csv_fifa_usecase import (
    SalvarBytesCsvFifaUsecase, )
from streamlit_fifa_py_estudo.app.utils.erros import LoadCsvFifaError, SaveCsvFifaError
from streamlit_fifa_py_estudo.app.utils.parameters import (
    LoadCsvParameters,
    SaveCsvParameters,
)
from streamlit_fifa_py_estudo.app.utils.types import (
    LCFData,
    LCFUsecase,
    SCFData,
    SCFUsecase,
)


class FeaturesPresenter:
    """Classe responsável pela instanciação e execução dos casos de uso.
    
    Esta classe atua como uma fachada para os diferentes casos de uso da aplicação,
    gerenciando suas instâncias e chamadas de métodos.

    Attributes:
        Não possui atributos próprios.
    """

    def ler_csv_fifa(self, file_path: str) -> List[dict]:
        """Executa o caso de uso de leitura de arquivo CSV do FIFA.

        Realiza a validação do caminho do arquivo e executa o caso de uso
        para carregar os dados dos jogadores do FIFA.

        Args:
            file_path (str): Caminho completo para o arquivo CSV.

        Returns:
            List[dict]: Lista de dicionários contendo os dados dos jogadores.

        Raises:
            FileNotFoundError: Se o arquivo especificado não for encontrado.
            LoadCsvFifaError: Se ocorrer erro durante o carregamento do CSV.

        Example:
            ```python
            presenter = FeaturesPresenter()
            players = presenter.ler_csv_fifa("data/fifa23.csv")
            ```
        """

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        error: LoadCsvFifaError = LoadCsvFifaError()
        parameters: LoadCsvParameters = LoadCsvParameters(
            error=error, file_path=str(path))
        dataSource: LCFData = LoadCsvPandasDatasource()
        usecase: LCFUsecase = LerCsvFifaUseCase(dataSource)

        data = usecase.runNewThread(parameters)
        list_fifa_players: List[dict] = []

        if isinstance(data, SuccessReturn):

            list_fifa_players = data.result

        if isinstance(data, ErrorReturn):
            raise data.result

        return list_fifa_players

    def salvar_csv_fifa(self, csv_name: str, bytes_csv: bytes) -> Path:
        """Executa o caso de uso de salvamento de arquivo CSV do FIFA.

        Recebe os bytes do arquivo CSV e um nome, realiza a validação e salva
        o arquivo no sistema de arquivos.

        Args:
            csv_name (str): Nome do arquivo CSV a ser salvo (sem extensão)
            bytes_csv (bytes): Conteúdo do arquivo CSV em formato bytes

        Returns:
            Path: Caminho completo do arquivo salvo

        Raises:
            SaveCsvFifaError: Se ocorrer erro durante o salvamento do CSV

        Example:
            ```python
            presenter = FeaturesPresenter()
            with open('fifa23.csv', 'rb') as f:
                bytes_data = f.read()
                path = presenter.salvar_csv_fifa("novo_fifa", bytes_data)
            ```
        """
        error: SaveCsvFifaError = SaveCsvFifaError()
        parameters: SaveCsvParameters = SaveCsvParameters(
            error=error, csv_name=csv_name, bytes_csv=bytes_csv
        )
        dataSource: SCFData = SalvarBytesCsvFifaDatasource()
        usecase: SCFUsecase = SalvarBytesCsvFifaUsecase(dataSource)

        data = usecase.runNewThread(parameters)
        path = Path()

        if isinstance(data, SuccessReturn):
            path = data.result

        if isinstance(data, ErrorReturn):
            raise data.result

        return path
