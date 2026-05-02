from dataclasses import dataclass
from typing import ClassVar, Type
from domain.entities.base import Entity
from domain.entities.order import Order


@dataclass
class OrderSummaryDTO:
    order_id: str
    user_id: str
    days: int
    shipped: bool
    custom: bool
    amount: int
    entity: ClassVar[Type[Entity]] = Order

