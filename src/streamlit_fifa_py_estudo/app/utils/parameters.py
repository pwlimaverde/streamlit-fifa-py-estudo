from dataclasses import dataclass

from py_return_success_or_error import ParametersReturnResult

from streamlit_fifa_py_estudo.app.utils.erros import LoadCsvFifaError, SaveCsvFifaError


@dataclass
class LoadCsvParameters(ParametersReturnResult):
    """Parâmetros para carregar um arquivo CSV"""
    file_path: str
    error: LoadCsvFifaError

    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class SaveCsvParameters(ParametersReturnResult):
    """Parâmetros para carregar um arquivo CSV"""
    csv_name: str
    bytes_csv: bytes
    error: SaveCsvFifaError

    def __str__(self) -> str:
        return self.__repr__()
