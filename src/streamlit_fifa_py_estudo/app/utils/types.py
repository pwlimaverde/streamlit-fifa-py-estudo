from typing import List, TypeAlias

from py_return_success_or_error import (
    Datasource,
    UsecaseBaseCallData,
)

from streamlit_fifa_py_estudo.app.features.ler_csv_fifa.domain.models.fifa_player import FifaPlayer
from streamlit_fifa_py_estudo.app.utils.parameters import LoadCsvParameters


LCFUsecase: TypeAlias = UsecaseBaseCallData[
    List[dict],
    List[FifaPlayer],
    LoadCsvParameters
]

LCFData: TypeAlias = Datasource[List[FifaPlayer], LoadCsvParameters]
