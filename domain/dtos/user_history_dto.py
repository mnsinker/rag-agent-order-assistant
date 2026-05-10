from dataclasses import dataclass
from typing import ClassVar, Type
from domain.dtos.order_record_dto import OrderRecordDTO
from domain.nodes.base import Node
from domain.nodes.user import UserHistory


@dataclass
class UserHistoryDTO:
    user_id: str
    orders: list[OrderRecordDTO]
    node: ClassVar[Type[Node]] = UserHistory