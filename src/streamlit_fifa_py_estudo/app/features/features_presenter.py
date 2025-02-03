from pathlib import Path
from typing import List

from py_return_success_or_error import (
    ErrorReturn,
    SuccessReturn,
)

from streamlit_fifa_py_estudo.app.features.ler_csv_fifa.datasource.load_csv_pandas_datasource import (
    LoadCsvPandasDatasource, )
from streamlit_fifa_py_estudo.app.features.ler_csv_fifa.domain.usecase.ler_csv_fifa_usecase import (
    LerCsvFifaUseCase, )
from streamlit_fifa_py_estudo.app.features.salvar_bytes_csv_fifa.datasource.salvar_bytes_csv_fifa_datasource import (
    SalvarBytesCsvFifaDatasource, )
from streamlit_fifa_py_estudo.app.features.salvar_bytes_csv_fifa.domain.usecase.salvar_bytes_csv_fifa_usecase import (
    SalvarBytesCsvFifaUsecase, )
from streamlit_fifa_py_estudo.app.utils.erros import LoadCsvFifaError, SaveCsvFifaError
from streamlit_fifa_py_estudo.app.utils.parameters import (
    LoadCsvParameters,
    SaveCsvParameters,
)
from streamlit_fifa_py_estudo.app.utils.types import (
    LCFData,
    LCFUsecase,
    SCFData,
    SCFUsecase,
)


class FeaturesPresenter:

    def ler_csv_fifa(self, file_path: str) -> List[dict]:

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        error: LoadCsvFifaError = LoadCsvFifaError()
        parameters: LoadCsvParameters = LoadCsvParameters(
            error=error, file_path=str(path))
        dataSource: LCFData = LoadCsvPandasDatasource()
        usecase: LCFUsecase = LerCsvFifaUseCase(dataSource)

        data = usecase.runNewThread(parameters)
        list_fifa_players: List[dict] = []

        if isinstance(data, SuccessReturn):

            list_fifa_players = data.result

        if isinstance(data, ErrorReturn):
            raise data.result

        return list_fifa_players

    def salvar_csv_fifa(self, csv_name: str, bytes_csv: bytes) -> Path:
        print()
        print('*************')
        print(csv_name)
        print(type(bytes_csv))
        error: SaveCsvFifaError = SaveCsvFifaError()
        parameters: SaveCsvParameters = SaveCsvParameters(
            error=error, csv_name=csv_name, bytes_csv=bytes_csv
        )
        dataSource: SCFData = SalvarBytesCsvFifaDatasource()
        usecase: SCFUsecase = SalvarBytesCsvFifaUsecase(dataSource)

        data = usecase.runNewThread(parameters)
        path = Path()

        if isinstance(data, SuccessReturn):
            path = data.result

        if isinstance(data, ErrorReturn):
            raise data.result

        return path
