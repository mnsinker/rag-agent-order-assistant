from dataclasses import dataclass
from typing import ClassVar, Type
from domain.entities.base import Entity
from domain.entities.order import Order


@dataclass
class ShippingResultDTO:
    shipped: bool
    shipping_status: str
    entity: ClassVar[Type[Entity]] = Order