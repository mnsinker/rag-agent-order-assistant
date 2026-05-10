from dataclasses import dataclass
from typing import ClassVar, Type

from domain.nodes.base import Node
from domain.nodes.coupon import CouponEligibility, CouponDecision


@dataclass
class CouponEligibilityDTO:
    applicable: bool
    reason: str
    node: ClassVar[Type[Node]] = CouponEligibility

@dataclass
class CouponDecisionDTO:
    give_coupon: bool
    coupon_type: str    # 'discount' / 'full_reduction' / "none"
    amount: int         # 10, 20, etc
    reason: str
    policy_rule: str
    node: ClassVar[Type[Node]] = CouponDecision