from dataclasses import dataclass

from py_return_success_or_error import AppError


@dataclass
class LoadCsvFifaError(AppError):
    """Classe de erro para LoadCsvFifa"""
    message: str = 'Erro ao carregar o arquivo CSV'

    def __str__(self) -> str:
        """Retorna a representação em string do erro genérico.

        Returns:
                str: A representação em string do erro genérico.
        """
        return f'LoadCsvFifaError - {self.message}'
