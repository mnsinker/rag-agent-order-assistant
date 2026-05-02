from dataclasses import dataclass
from typing import ClassVar, Type
from domain.dtos.order_record_dto import OrderRecordDTO
from domain.entities.base import Entity
from domain.entities.user import User


@dataclass
class UserHistoryDTO:
    user_id: str
    orders: list[OrderRecordDTO]
    entity: ClassVar[Type[Entity]] = User