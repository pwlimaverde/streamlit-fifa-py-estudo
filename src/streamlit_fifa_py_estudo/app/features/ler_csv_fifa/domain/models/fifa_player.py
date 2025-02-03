from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class FifaPlayer:
    """Classe para representar dados de jogadores do FIFA 23"""
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
        # Converter campos de data
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
