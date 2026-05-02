from policies.refund_policy import evaluate_refund_policy
from services.order_service import get_order_summary
from domain.dtos.refund_dto import RefundDecisionDTO, RefundExecutionResultDTO
from errors.validation import ValidationError


def check_refund(order_id: str) -> RefundDecisionDTO:
    order_summary = get_order_summary(order_id)
    if order_summary is None:
        raise ValidationError("order_id not found")

    return evaluate_refund_policy(order_summary) # call policy layer




def create_refund(
        order_id: str,
        decision: RefundDecisionDTO | None = None
) -> RefundExecutionResultDTO:

    if decision and not decision.allowed:
        return RefundExecutionResultDTO(False, 'not eligible to refund')

    return RefundExecutionResultDTO(True, 'refund initiated', refund_id=f'refund_{order_id}')


