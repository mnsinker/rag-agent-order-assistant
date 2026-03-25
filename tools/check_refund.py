from services.order_service import get_order_summary
from utils.make_response import make_response
from models.refund import RefundResult
def check_refund(order_id: str) -> dict:
    order_summary = get_order_summary(order_id)

    if order_summary is None:
        return make_response(False, None, "order_id not found")
    if order_summary.custom:
        return make_response(True, RefundResult(False, "custom product doesn't support refund"))
    if order_summary.shipped:
        return make_response(True, RefundResult(False, "product is already shipped"))
    if order_summary.days > 7:
        return make_response(True, RefundResult(False, "product is more than 7 days"))
    return make_response(True, RefundResult(True, "eligible for refund"))

