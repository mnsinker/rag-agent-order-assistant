from domain.dtos.order_summary_dto import OrderSummaryDTO
from policies.refund_policy import evaluate_refund_policy
from services.order_service import get_order_summary
from domain.dtos.refund_dto import RefundDecisionDTO, RefundExecutionResultDTO
from errors.validation import ValidationError


def check_refund(order: OrderSummaryDTO) -> RefundDecisionDTO:
    return evaluate_refund_policy(order) # call policy layer




def create_refund(
        order_id: str,
        decision: RefundDecisionDTO | None = None
) -> RefundExecutionResultDTO:

    if decision and not decision.allowed:
        return RefundExecutionResultDTO(False, 'not eligible to refund', refund_id="")

    return RefundExecutionResultDTO(True, 'refund initiated', refund_id=f'refund_{order_id}')


