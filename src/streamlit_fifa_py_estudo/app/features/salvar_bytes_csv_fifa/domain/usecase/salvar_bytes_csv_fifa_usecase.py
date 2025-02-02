from pathlib import Path

from py_return_success_or_error import (
    ErrorReturn,
    ReturnSuccessOrError,
)

from streamlit_fifa_py_estudo.app.utils.erros import SaveCsvFifaError
from streamlit_fifa_py_estudo.app.utils.parameters import SaveCsvParameters
from streamlit_fifa_py_estudo.app.utils.types import SCFUsecase


class SalvarBytesCsvFifaUsecase(SCFUsecase):
    def __call__(
            self,
            parameters: SaveCsvParameters) -> ReturnSuccessOrError[Path]:
        try:

            return self._resultDatasource(
                parameters=parameters, datasource=self._datasource
            )
        except Exception as e:
            return ErrorReturn(SaveCsvFifaError(str(e)))
