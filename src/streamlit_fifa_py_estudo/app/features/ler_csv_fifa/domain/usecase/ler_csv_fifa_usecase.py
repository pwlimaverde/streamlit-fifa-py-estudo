from datetime import datetime
from typing import List

from py_return_success_or_error import (
    ErrorReturn,
    ReturnSuccessOrError,
    SuccessReturn,
)

from streamlit_fifa_py_estudo.app.features.ler_csv_fifa.domain.models.fifa_player import (
    FifaPlayer, )
from streamlit_fifa_py_estudo.app.utils.erros import LoadCsvFifaError
from streamlit_fifa_py_estudo.app.utils.parameters import LoadCsvParameters
from streamlit_fifa_py_estudo.app.utils.types import LCFUsecase


class LerCsvFifaUseCase(LCFUsecase):
    def __call__(
            self, parameters: LoadCsvParameters) -> ReturnSuccessOrError[List[dict]]:
        """Carrega um arquivo CSV com dados de jogadores do FIFA 23"""
        try:
            result_dict: List[dict] = []
            result = self._resultDatasource(
                parameters=parameters, datasource=self._datasource
            )
            if isinstance(result, SuccessReturn):
                data: List[FifaPlayer] = result.result
                data = [
                    player for player in data if player.overall > 0 and int(
                        player.contract_valid_until) >= datetime.today().year
                ]
                data = sorted(data, key=lambda x: x.overall, reverse=True)

                result_dict = [player.to_dict() for player in data]

            if isinstance(result, ErrorReturn):
                return result

            return SuccessReturn(result_dict)
        except Exception as e:
            return ErrorReturn(LoadCsvFifaError(str(e)))
