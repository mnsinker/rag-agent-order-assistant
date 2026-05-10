from dataclasses import dataclass
from typing import ClassVar, Type
from domain.nodes.base import Node
from domain.nodes.order import OrderRecord


@dataclass
class OrderRecordDTO:
    order_id: str
    amount: float
    node: ClassVar[Type[Node]] = OrderRecord