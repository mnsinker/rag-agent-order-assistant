from dataclasses import dataclass
from domain.dtos.order_record_dto import OrderRecordDTO


@dataclass
class UserHistoryDTO:
    user_id: str
    orders: list[OrderRecordDTO]