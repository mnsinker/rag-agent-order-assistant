from dataclasses import dataclass

@dataclass
class RefundResult():
    refundable: bool
    reason: str