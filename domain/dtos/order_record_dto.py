from dataclasses import dataclass

@dataclass
class OrderRecordDTO:
    order_id: str
    amount: float