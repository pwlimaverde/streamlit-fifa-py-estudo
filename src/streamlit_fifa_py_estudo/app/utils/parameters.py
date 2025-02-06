from dataclasses import dataclass

from py_return_success_or_error import ParametersReturnResult

from streamlit_fifa_py_estudo.app.utils.erros import LoadCsvFifaError, SaveCsvFifaError


@dataclass
class LoadCsvParameters(ParametersReturnResult):
    """Parâmetros para carregar um arquivo CSV do FIFA.

    Attributes:
        file_path (str): Caminho do arquivo CSV a ser carregado
        error (LoadCsvFifaError): Instância de erro para tratamento de falhas

    Example:
        ```python
        params = LoadCsvParameters(
            file_path="data/fifa23.csv",
            error=LoadCsvFifaError()
        )
        ```
    """
    file_path: str
    error: LoadCsvFifaError

    def __str__(self) -> str:
        """Retorna representação string dos parâmetros.

        Returns:
            str: String formatada com os atributos da classe
        """
        return self.__repr__()


@dataclass
class SaveCsvParameters(ParametersReturnResult):
    """Parâmetros para salvar dados em arquivo CSV do FIFA.

    Attributes:
        csv_name (str): Nome do arquivo CSV a ser salvo (sem extensão)
        bytes_csv (bytes): Conteúdo do arquivo CSV em formato bytes
        error (SaveCsvFifaError): Instância de erro para tratamento de falhas

    Example:
        ```python
        params = SaveCsvParameters(
            csv_name="fifa23_players",
            bytes_csv=b"content...",
            error=SaveCsvFifaError()
        )
        ```
    """
    csv_name: str
    bytes_csv: bytes
    error: SaveCsvFifaError

    def __str__(self) -> str:
        """Retorna representação string dos parâmetros.

        Returns:
            str: String formatada com os atributos da classe
        """
        return "SaveCsvParameters(error={}, csv_name='{}'".format(
            self.error, self.csv_name)
