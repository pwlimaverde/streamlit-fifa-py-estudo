from io import BytesIO
from pathlib import Path
from typing import Optional

import pandas as pd

from streamlit_fifa_py_estudo.app.utils.consts import PASTA_DATASETS
from streamlit_fifa_py_estudo.app.utils.parameters import SaveCsvParameters
from streamlit_fifa_py_estudo.app.utils.types import SCFData


def validate_fifa_csv(bytes_csv: bytes) -> tuple[bool, Optional[str]]:
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
    def __call__(self, parameters: SaveCsvParameters) -> Path:
        """Carrega um arquivo CSV com dados de jogadores do FIFA 23"""

        is_valid, error_msg = validate_fifa_csv(parameters.bytes_csv)
        print(is_valid)
        print(error_msg)
        if not is_valid:
            raise ValueError(f"CSV inválido: {error_msg}")
        PASTA_DATASETS.mkdir(exist_ok=True)
        path = PASTA_DATASETS / f'{parameters.csv_name}.csv'

        with open(path, 'wb') as file:
            file.write(parameters.bytes_csv)
        return path
