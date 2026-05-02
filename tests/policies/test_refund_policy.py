from domain.dtos.order_summary_dto import OrderSummaryDTO
from policies.refund_policy import evaluate_refund_policy


def test_refund_block_custom_product():
    order = OrderSummaryDTO(
        order_id="test999",
        user_id="test_u1",
        days=3,
        shipped=False,
        custom=True,
        amount=100,
    )
    decision = evaluate_refund_policy(order)
    assert decision.allowed is False
    assert decision.policy_rule == "refund.block.custom_product"


def test_refund_block_shipped_order():
    order = OrderSummaryDTO(
        order_id="test999",
        user_id="test_u1",
        days=3,
        shipped=True,
        custom=False,
        amount=100,
    )
    decision = evaluate_refund_policy(order)
    assert decision.allowed is False
    assert decision.policy_rule == "refund.block.shipped_order"


def test_refund_block_after_7_days():
    order = OrderSummaryDTO(
        order_id="test999",
        user_id="test_u1",
        days=8,
        shipped=False,
        custom=False,
        amount=100,
    )

    decision = evaluate_refund_policy(order)
    assert decision.allowed is False
    assert decision.policy_rule == "refund.block.after_7_days"

def test_refund_allow_standard():
    order = OrderSummaryDTO(
        order_id="test999",
        user_id="test_u1",
        days=3,
        shipped=False,
        custom=False,
        amount=100,
    )
    decision = evaluate_refund_policy(order)
    assert decision.allowed is True
    assert decision.policy_rule == "refund.allow.standard"

