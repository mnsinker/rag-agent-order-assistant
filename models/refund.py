from dataclasses import dataclass


@dataclass
class RefundEligibility():
    refundable: bool
    reason: str


@dataclass
class RefundExecutionResult():
    success: bool
    message: str
    refund_id: str = ""
