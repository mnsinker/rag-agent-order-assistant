from dataclasses import dataclass
from typing import ClassVar, Type
from domain.nodes.base import Node
from domain.nodes.order import OrderSummary


@dataclass
class OrderSummaryDTO:
    order_id: str
    user_id: str
    days: int
    shipped: bool
    custom: bool
    amount: int
    node: ClassVar[Type[Node]] = OrderSummary

