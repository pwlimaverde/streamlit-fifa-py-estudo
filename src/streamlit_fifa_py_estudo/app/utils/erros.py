from dataclasses import dataclass

from py_return_success_or_error import AppError


@dataclass
class LoadCsvFifaError(AppError):
    """Exceção lançada quando ocorre erro no carregamento do arquivo CSV FIFA.
    
    Attributes:
        message (str): Mensagem descritiva do erro. Padrão: 'Erro ao carregar o arquivo CSV'

    Example:
        ```python
        try:
            raise LoadCsvFifaError("Arquivo não encontrado")
        except LoadCsvFifaError as e:
            print(str(e))  # LoadCsvFifaError - Arquivo não encontrado
        ```
    """
    message: str = 'Erro ao carregar o arquivo CSV'

    def __str__(self) -> str:
        """Retorna a representação string do erro.

        Returns:
            str: String formatada com o prefixo da classe e a mensagem de erro.
        """
        return f'LoadCsvFifaError - {self.message}'

@dataclass
class SaveCsvFifaError(AppError):
    """Exceção lançada quando ocorre erro no salvamento do arquivo CSV FIFA.
    
    Attributes:
        message (str): Mensagem descritiva do erro. Padrão: 'Erro ao salvar o arquivo CSV'
    
    Example:
        ```python
        try:
            raise SaveCsvFifaError("Permissão negada")
        except SaveCsvFifaError as e:
            print(str(e))  # SaveCsvFifaError - Permissão negada
        ```
    """
    message: str = 'Erro ao salvar o arquivo CSV'

    def __str__(self) -> str:
        """Retorna a representação string do erro.

        Returns:
            str: String formatada com o prefixo da classe e a mensagem de erro.
        """
        return f'SaveCsvFifaError - {self.message}'