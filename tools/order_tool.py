from domain.dtos.order_summary_dto import OrderSummaryDTO
from services.order_service import get_order_summary


def get_order(order_id: str) -> OrderSummaryDTO:
    return get_order_summary(order_id)