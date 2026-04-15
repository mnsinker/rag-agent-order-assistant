from dataclasses import dataclass

@dataclass
class CouponEligibility:
    applicable: bool
    reason: str