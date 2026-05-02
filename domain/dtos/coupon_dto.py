from dataclasses import dataclass
from typing import ClassVar, Type
from domain.entities.base import Entity
from domain.entities.coupon import Coupon


@dataclass
class CouponEligibilityDTO:
    applicable: bool
    reason: str
    entity: ClassVar[Type[Entity]] = Coupon

@dataclass
class CouponDecisionDTO:
    give_coupon: bool
    coupon_type: str    # 'discount' / 'full_reduction' / "none"
    amount: int         # 10, 20, etc
    reason: str
    policy_rule: str
    entity: ClassVar[Type[Entity]] = Coupon