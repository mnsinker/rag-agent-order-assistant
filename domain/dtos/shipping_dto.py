from dataclasses import dataclass
from typing import ClassVar, Type
from domain.nodes.base import Node
from domain.nodes.order import ShippingStatus


@dataclass
class ShippingResultDTO:
    shipped: bool
    shipping_status: str
    node: ClassVar[Type[Node]] = ShippingStatus