from io import BytesIO
from pathlib import Path
from typing import Optional

import pandas as pd

from streamlit_fifa_py_estudo.app.utils.consts import PASTA_DATASETS
from streamlit_fifa_py_estudo.app.utils.parameters import SaveCsvParameters
from streamlit_fifa_py_estudo.app.utils.types import SCFData


def validate_fifa_csv(bytes_csv: bytes) -> tuple[bool, Optional[str]]:
    """Valida se um arquivo CSV em bytes contém os dados esperados de jogadores FIFA.

    Verifica se o CSV possui as colunas necessárias com os tipos de dados corretos
    para ser considerado um arquivo válido de dados de jogadores FIFA.

    Args:
        bytes_csv (bytes): Conteúdo do arquivo CSV em formato bytes.

    Returns:
        tuple[bool, Optional[str]]: Uma tupla contendo:
            - bool: True se o arquivo é válido, False caso contrário
            - Optional[str]: Mensagem de erro se houver falha na validação, 
              None se o arquivo for válido

    Example:
        ```python
        with open('fifa23.csv', 'rb') as f:
            bytes_data = f.read()
            is_valid, error = validate_fifa_csv(bytes_data)
            if not is_valid:
                print(f"Erro na validação: {error}")
        ```
    """
    expected_columns = {
        'ID': 'int64',
        'Name': 'object',
        'Age': 'int64',
        'Photo': 'object',
        'Nationality': 'object',
        'Flag': 'object',
        'Overall': 'int64',
        'Club': 'object',
        'Club Logo': 'object',
        'Value(£)': 'float64',
        'Wage(£)': 'float64',
        'Position': 'object',
        'Joined': 'object',
        'Contract Valid Until': 'float64',
        'Height(cm.)': 'float64',
        'Weight(lbs.)': 'float64',
        'Release Clause(£)': 'float64',
    }

    try:
        df = pd.read_csv(BytesIO(bytes_csv))
        if 'Height(cm.)' in df.columns:
            df['Height(cm.)'] = df['Height(cm.)'].astype(float)
        if 'Weight(lbs.)' in df.columns:
            df['Weight(lbs.)'] = df['Weight(lbs.)'].astype(float)

        # Verifica colunas presentes
        missing_cols = set(expected_columns.keys()) - set(df.columns)
        if missing_cols:
            return False, f"Colunas ausentes: {', '.join(missing_cols)}"

        # Verifica tipos de dados
        for col, expected_type in expected_columns.items():
            if str(df[col].dtype) != expected_type:
                return False, f"Coluna {col} tem tipo {
                    df[col].dtype}, esperado {expected_type}"

        return True, 'Capos esperados presentes e com tipos corretos'

    except Exception as e:
        return False, f"Erro ao ler CSV: {str(e)}"


class SalvarBytesCsvFifaDatasource(SCFData):
    """Classe para salvar dados de jogadores FIFA recebidos em formato bytes.

    Esta classe implementa a interface SCFData e é responsável por validar e 
    salvar os dados do FIFA recebidos em formato bytes em um arquivo CSV.

    Attributes:
        Não possui atributos próprios.
    """

    def __call__(self, parameters: SaveCsvParameters) -> Path:
        """Salva os dados em bytes como um arquivo CSV.

        Valida se os dados recebidos são um CSV válido de jogadores FIFA e
        salva em arquivo na pasta de datasets.

        Args:
            parameters (SaveCsvParameters): Parâmetros contendo os bytes do CSV
                e o nome do arquivo a ser salvo.

        Returns:
            Path: Caminho completo do arquivo CSV salvo.

        Raises:
            ValueError: Se os dados do CSV forem inválidos.

        Example:
            ```python
            datasource = SalvarBytesCsvFifaDatasource()
            params = SaveCsvParameters(
                bytes_csv=csv_bytes,
                csv_name="fifa23_players"
            )
            file_path = datasource(params)
            ```
        """
        is_valid, error_msg = validate_fifa_csv(parameters.bytes_csv)
        if not is_valid:
            raise ValueError(f"CSV inválido: {error_msg}")
        
        PASTA_DATASETS.mkdir(exist_ok=True)
        path = PASTA_DATASETS / f'{parameters.csv_name}.csv'

        with open(path, 'wb') as file:
            file.write(parameters.bytes_csv)
        return path
