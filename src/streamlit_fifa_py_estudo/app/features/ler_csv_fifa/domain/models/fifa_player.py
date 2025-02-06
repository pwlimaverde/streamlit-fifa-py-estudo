from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class FifaPlayer:
    """Classe para representar dados de jogadores do FIFA 23.

    Esta classe modela os atributos e características de um jogador do FIFA 23,
    incluindo informações pessoais, profissionais e estatísticas.

    Attributes:
        id (int): Identificador único do jogador.
        name (str): Nome completo do jogador.
        age (int): Idade do jogador.
        photo (str): URL da foto do jogador.
        nationality (str): Nacionalidade do jogador.
        flag (str): URL da bandeira do país do jogador.
        overall (int): Classificação geral do jogador (0-100).
        club (str): Nome do clube atual do jogador.
        club_logo (str): URL do logo do clube.
        value (float): Valor de mercado do jogador em libras.
        wage (float): Salário semanal do jogador em libras.
        position (str): Posição principal do jogador em campo.
        joined (Optional[date]): Data em que o jogador se juntou ao clube atual.
        contract_valid_until (float): Ano de término do contrato atual.
        height_m (float): Altura do jogador em metros.
        weight_kg (float): Peso do jogador em quilogramas.
        release_clause (float): Valor da cláusula de rescisão em libras.
    """
    id: int
    name: str
    age: int
    photo: str
    nationality: str
    flag: str
    overall: int
    club: str
    club_logo: str
    value: float
    wage: float
    position: str
    joined: Optional[date]
    contract_valid_until: float
    height_m: float
    weight_kg: float
    release_clause: float

    @classmethod
    def from_csv_row(cls, row: dict) -> "FifaPlayer":
        """Cria uma instância de FifaPlayer a partir de uma linha do CSV.

        Args:
            row (dict): Dicionário contendo os dados de uma linha do arquivo CSV,
                onde as chaves são os nomes das colunas.

        Returns:
            FifaPlayer: Nova instância de FifaPlayer com os dados fornecidos.

        Example:
            ```python
            csv_row = {
                "ID": "158023",
                "Name": "L. Messi",
                "Age": "35",
                # ... outros campos
            }
            player = FifaPlayer.from_csv_row(csv_row)
            ```
        """
        joined = None
        if row["Joined"]:
            joined = date.fromisoformat(row["Joined"])

        # Converter campos numéricos
        value = float(str(row["Value(£)"]).replace(
            ',', '')) if row["Value(£)"] else 0.0
        wage = float(str(row["Wage(£)"]).replace(
            ',', '')) if row["Wage(£)"] else 0.0
        release_clause = float(str(row["Release Clause(£)"]).replace(
            ',', '')) if row["Release Clause(£)"] else 0.0
        height_m = round(float(
            row["Height(cm.)"] /
            100), 2) if row["Height(cm.)"] else 0.0
        weight_kg = round(float(
            row["Weight(lbs.)"] *
            0.453), 2) if row["Weight(lbs.)"] else 0.0

        return cls(
            id=int(row["ID"]),
            name=row["Name"],
            age=int(row["Age"]),
            photo=row["Photo"],
            nationality=row["Nationality"],
            flag=row["Flag"],
            overall=int(row["Overall"]),
            club=row["Club"],
            club_logo=row["Club Logo"],
            value=value,
            wage=wage,
            position=row["Position"],
            joined=joined,
            contract_valid_until=float(row["Contract Valid Until"]),
            height_m=height_m,
            weight_kg=weight_kg,
            release_clause=release_clause,
        )

    def to_dict(self) -> dict:
        """Converte a instância de FifaPlayer em um dicionário.

            Método que converte todos os atributos do jogador em um dicionário,
            facilitando a serialização e manipulação dos dados.

            Returns:
                dict: Dicionário contendo todos os atributos do jogador.
                    As chaves são os nomes dos atributos e os valores são seus respectivos conteúdos.

            Example:
                ```python
                player = FifaPlayer(id=158023, name="L. Messi", ...)
                player_dict = player.to_dict()
                print(player_dict['name'])  # Output: "L. Messi"
                ```
        """
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'photo': self.photo,
            'nationality': self.nationality,
            'flag': self.flag,
            'overall': self.overall,
            'club': self.club,
            'club_logo': self.club_logo,
            'value': self.value,
            'wage': self.wage,
            'position': self.position,
            'joined': self.joined.isoformat() if self.joined else None,
            'contract_valid_until': self.contract_valid_until,
            'height_m': self.height_m,
            'weight_kg': self.weight_kg,
            'release_clause': self.release_clause,
        }
