from dataclasses import dataclass

@dataclass
class OrderSummary():
    order_id: str
    days: int
    shipped: bool
    custom: bool

