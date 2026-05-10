from dataclasses import dataclass
from typing import ClassVar, Type

from domain.nodes.base import Node
from domain.nodes.risk import RiskResult


@dataclass
class RiskResultDTO:
    risk: bool
    risk_level: str
    risk_score: int
    reason: str
    policy_rule: str
    node: ClassVar[Type[Node]] = RiskResult