from dataclasses import dataclass
from typing import ClassVar, Type

from domain.nodes.base import Node
from domain.nodes.credit import CreditScore


@dataclass
class CreditScoreDTO:
    score: int
    node: ClassVar[Type[Node]] = CreditScore
