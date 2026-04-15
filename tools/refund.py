from models.refund import RefundExecutionResult
from services.order_service import get_order_summary
from models.refund import RefundEligibility
from errors.validation import ValidationError


def check_refund(order_id: str) -> RefundEligibility:
    order_summary = get_order_summary(order_id)
    if order_summary is None:
        raise ValidationError("order_id not found")

    if order_summary.custom:
        return RefundEligibility(False, "custom product doesn't support refund")
    if order_summary.shipped:
        return RefundEligibility(False, "product is already shipped")
    if order_summary.days > 7:
        return RefundEligibility(False, "product is more than 7 days")
    return RefundEligibility(True, "eligible for refund")


'''
before:
    if order_summary is None:
        return make_response(False, None, "order_id not found")
    if order_summary.custom:
        return make_response(True, RefundResult(False, "custom product doesn't support refund"))
    if order_summary.shipped:
        return make_response(True, RefundResult(False, "product is already shipped"))
    if order_summary.days > 7:
        return make_response(True, RefundResult(False, "product is more than 7 days"))
    return make_response(True, RefundResult(True, "eligible for refund"))
'''


def create_refund(order_id: str, eligibility: RefundEligibility | None = None) -> RefundExecutionResult:
    if eligibility and not eligibility.refundable:
        return RefundExecutionResult(False, 'not eligible to refund')
    return RefundExecutionResult(True, 'refund initiated')
