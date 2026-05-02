from dataclasses import dataclass
from typing import ClassVar, Type
from domain.entities.base import Entity
from domain.entities.risk import Risk


@dataclass
class RiskResultDTO:
    risk: bool
    risk_level: str
    risk_score: int
    reason: str
    policy_rule: str
    entity: ClassVar[Type[Entity]] = Risk