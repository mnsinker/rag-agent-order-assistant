from domain.dtos.order_summary_dto import OrderSummaryDTO
from domain.dtos.refund_dto import RefundDecisionDTO


def evaluate_refund_policy(order_summary: OrderSummaryDTO) -> RefundDecisionDTO:
    # policy 规则
    if order_summary.custom:
        return RefundDecisionDTO(
            allowed=False,
            reason="custom product doesn't support refund",
            policy_rule="refund.block.custom_product", )
    if order_summary.shipped:
        return RefundDecisionDTO(
            allowed=False,
            reason="product is already shipped",
            policy_rule="refund.block.shipped_order",
        )
    if order_summary.days > 7:
        return RefundDecisionDTO(
            allowed=False,
            reason="product is more than 7 days",
            policy_rule="refund.block.after_7_days",
        )
    return RefundDecisionDTO(
        allowed=True,
        reason="eligible for refund",
        policy_rule="refund.allow.standard",
    )