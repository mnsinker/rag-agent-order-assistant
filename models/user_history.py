from dataclasses import dataclass

@dataclass
class OrderRecord:
    order_id: str
    amount: float

@dataclass
class UserHistory:
    user_id: str
    orders: list[OrderRecord]