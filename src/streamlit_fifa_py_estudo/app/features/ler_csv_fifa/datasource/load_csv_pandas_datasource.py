from typing import List

import pandas as pd

from streamlit_fifa_py_estudo.app.features.ler_csv_fifa.domain.models.fifa_player import (
    FifaPlayer, )
from streamlit_fifa_py_estudo.app.utils.parameters import LoadCsvParameters
from streamlit_fifa_py_estudo.app.utils.types import LCFData


class LoadCsvPandasDatasource(LCFData):
    """Classe responsável por carregar dados de jogadores do FIFA 23 a partir de um arquivo CSV.

    Esta classe implementa a interface LCFData e utiliza o pandas para ler e processar
    os dados do arquivo CSV.

    Attributes:
        Não possui atributos próprios.
    """

    def __call__(self, parameters: LoadCsvParameters) -> List[FifaPlayer]:
        """Carrega e processa um arquivo CSV com dados de jogadores do FIFA 23.

        Args:
            parameters (LoadCsvParameters): Objeto contendo os parâmetros de carregamento,
                incluindo o caminho do arquivo CSV.

        Returns:
            List[FifaPlayer]: Lista de objetos FifaPlayer contendo os dados dos jogadores.

        Example:
            ```python
            datasource = LoadCsvPandasDatasource()
            parameters = LoadCsvParameters(file_path="fifa23_players.csv")
            players = datasource(parameters)
            ```
        """
        df = pd.read_csv(parameters.file_path, index_col=0)
        players = [
            FifaPlayer.from_csv_row(row)
            for row in df.to_dict('records')
        ]

        return players
