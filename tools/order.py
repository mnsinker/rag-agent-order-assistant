from models.order import OrderSummary
from services.order_service import get_order_summary


def get_order(order_id: str) -> OrderSummary:
    return get_order_summary(order_id)