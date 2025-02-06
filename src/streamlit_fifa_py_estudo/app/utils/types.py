"""Tipos personalizados usados no projeto FIFA.

Este módulo define aliases de tipos para simplificar anotações de tipo
em casos de uso e fontes de dados.

TypeAliases:
    LCFUsecase: Tipo para caso de uso de leitura de CSV FIFA
    LCFData: Tipo para fonte de dados de leitura de CSV FIFA 
    SCFUsecase: Tipo para caso de uso de salvamento de CSV FIFA
"""
from pathlib import Path
from typing import List, TypeAlias

from py_return_success_or_error import (
    Datasource,
    UsecaseBaseCallData,
)

from streamlit_fifa_py_estudo.app.features.ler_csv_fifa.domain.models.fifa_player import (
    FifaPlayer, )
from streamlit_fifa_py_estudo.app.utils.parameters import (
    LoadCsvParameters,
    SaveCsvParameters,
)

# Type aliases
LCFUsecase: TypeAlias = UsecaseBaseCallData[
    List[dict],
    List[FifaPlayer],
    LoadCsvParameters
]
"""Tipo para caso de uso de leitura de CSV FIFA.

TypeAlias que representa um caso de uso que:
- Recebe parâmetros do tipo LoadCsvParameters
- Processa uma lista de FifaPlayer
- Retorna uma lista de dicionários
"""
LCFData: TypeAlias = Datasource[List[FifaPlayer], LoadCsvParameters]
"""Tipo para fonte de dados de leitura de CSV FIFA.

TypeAlias que representa uma fonte de dados que:
- Recebe parâmetros do tipo LoadCsvParameters  
- Retorna uma lista de FifaPlayer
"""
SCFUsecase: TypeAlias = UsecaseBaseCallData[
    Path,
    Path,
    SaveCsvParameters
]
"""Tipo para caso de uso de salvamento de CSV FIFA.

TypeAlias que representa um caso de uso que:
- Recebe parâmetros do tipo SaveCsvParameters
- Processa e retorna um Path do arquivo salvo
"""
SCFData: TypeAlias = Datasource[Path, SaveCsvParameters]
"""Tipo para fonte de dados de salvamento de CSV FIFA.

TypeAlias que representa uma fonte de dados que:
- Recebe parâmetros do tipo SaveCsvParameters
- Retorna um Path do arquivo salvo

Example:
    ```python
    class SalvarCSVDataSource(SCFData):
        def __call__(self, parameters: SaveCsvParameters) -> Path:
            # implementação
            return path
    ```
"""