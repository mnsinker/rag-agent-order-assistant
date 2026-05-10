from dataclasses import dataclass
from typing import ClassVar, Type

from domain.nodes.base import Node
from domain.nodes.refund import RefundDecision, RefundExecution


@dataclass
class RefundDecisionDTO:
    allowed: bool
    reason: str
    policy_rule: str
    node: ClassVar[Type[Node]] = RefundDecision



@dataclass
class RefundExecutionResultDTO:
    success: bool
    message: str
    refund_id: str
    node: ClassVar[Type[Node]] = RefundExecution




