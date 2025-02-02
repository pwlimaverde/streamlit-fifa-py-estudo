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
    potential: int
    club: str
    club_logo: str
    value: float
    wage: float
    special: int
    preferred_foot: str
    international_reputation: float
    weak_foot: float
    skill_moves: float
    work_rate: str
    body_type: str
    real_face: str
    position: str
    joined: Optional[date]
    loaned_from: Optional[str]
    contract_valid_until: float
    height_m: float
    weight_kg: float
    release_clause: float
    kit_number: float
    best_overall_rating: float
    year_joined: int

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

        # Tratar campos None
        loaned_from = row["Loaned From"] if row["Loaned From"] != "None" else None

        return cls(
            id=int(row["ID"]),
            name=row["Name"],
            age=int(row["Age"]),
            photo=row["Photo"],
            nationality=row["Nationality"],
            flag=row["Flag"],
            overall=int(row["Overall"]),
            potential=int(row["Potential"]),
            club=row["Club"],
            club_logo=row["Club Logo"],
            value=value,
            wage=wage,
            special=int(row["Special"]),
            preferred_foot=row["Preferred Foot"],
            international_reputation=float(row["International Reputation"]),
            weak_foot=float(row["Weak Foot"]),
            skill_moves=float(row["Skill Moves"]),
            work_rate=row["Work Rate"],
            body_type=row["Body Type"],
            real_face=row["Real Face"],
            position=row["Position"],
            joined=joined,
            loaned_from=loaned_from,
            contract_valid_until=float(row["Contract Valid Until"]),
            height_m=height_m,
            weight_kg=weight_kg,
            release_clause=release_clause,
            kit_number=float(row["Kit Number"]),
            best_overall_rating=float(row["Best Overall Rating"]),
            year_joined=int(row["Year_Joined"])
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
            'potential': self.potential,
            'club': self.club,
            'club_logo': self.club_logo,
            'value': self.value,
            'wage': self.wage,
            'special': self.special,
            'preferred_foot': self.preferred_foot,
            'international_reputation': self.international_reputation,
            'weak_foot': self.weak_foot,
            'skill_moves': self.skill_moves,
            'work_rate': self.work_rate,
            'body_type': self.body_type,
            'real_face': self.real_face,
            'position': self.position,
            'joined': self.joined.isoformat() if self.joined else None,
            'loaned_from': self.loaned_from,
            'contract_valid_until': self.contract_valid_until,
            'height_m': self.height_m,
            'weight_kg': self.weight_kg,
            'release_clause': self.release_clause,
            'kit_number': self.kit_number,
            'best_overall_rating': self.best_overall_rating,
            'year_joined': self.year_joined
        }
