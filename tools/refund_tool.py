from services.order_service import get_order_summary
from domain.dtos.refund_dto import RefundEligibilityDTO, RefundExecutionResultDTO
from errors.validation import ValidationError


def check_refund(order_id: str) -> RefundEligibilityDTO:
    order_summary = get_order_summary(order_id)
    if order_summary is None:
        raise ValidationError("order_id not found")

    if order_summary.custom:
        return RefundEligibilityDTO(False, "custom product doesn't support refund")
    if order_summary.shipped:
        return RefundEligibilityDTO(False, "product is already shipped")
    if order_summary.days > 7:
        return RefundEligibilityDTO(False, "product is more than 7 days")
    return RefundEligibilityDTO(True, "eligible for refund")


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


def create_refund(order_id: str, eligibility: RefundEligibilityDTO | None = None) -> RefundExecutionResultDTO:
    if eligibility and not eligibility.refundable:
        return RefundExecutionResultDTO(False, 'not eligible to refund')
    return RefundExecutionResultDTO(True, 'refund initiated')
