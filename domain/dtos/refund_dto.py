from dataclasses import dataclass
from typing import ClassVar, Type
from domain.entities.base import Entity
from domain.entities.refund import Refund


@dataclass
class RefundDecisionDTO:
    allowed: bool
    reason: str
    policy_rule: str
    entity: ClassVar[Type[Entity]] = Refund



@dataclass
class RefundExecutionResultDTO:
    success: bool
    message: str
    refund_id: str
    entity: ClassVar[Type[Entity]] = Refund




