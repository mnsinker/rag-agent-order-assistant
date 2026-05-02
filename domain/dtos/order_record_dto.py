from dataclasses import dataclass
from typing import ClassVar, Type

from domain.entities.base import Entity
from domain.entities.order import Order


@dataclass
class OrderRecordDTO:
    order_id: str
    amount: float
    entity: ClassVar[Type[Entity]] = Order