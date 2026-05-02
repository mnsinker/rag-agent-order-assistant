from dataclasses import dataclass
from typing import ClassVar, Type

from domain.entities.base import Entity
from domain.entities.credit import Credit


@dataclass
class CreditScoreDTO:
    score: int
    entity: ClassVar[Type[Entity]] = Credit
