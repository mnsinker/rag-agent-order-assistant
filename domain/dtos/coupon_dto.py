from dataclasses import dataclass

@dataclass
class CouponEligibilityDTO:
    applicable: bool
    reason: str