from dataclasses import dataclass


@dataclass
class RefundEligibilityDTO:
    refundable: bool
    reason: str


@dataclass
class RefundExecutionResultDTO:
    success: bool
    message: str
    refund_id: str = ""
