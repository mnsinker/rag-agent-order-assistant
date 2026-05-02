from domain.dtos.order_summary_dto import OrderSummaryDTO
from domain.dtos.user_profile_dto import UserProfileDTO
from policies.coupon_policy import evaluate_coupon_policy


def test_coupon_new_user():
    user = UserProfileDTO(user_id="test_u1", level="new")
    order = OrderSummaryDTO(order_id="test_123", user_id=user.user_id, days=0, shipped=False, custom=False, amount=100)

    decision = evaluate_coupon_policy(order, user)

    assert decision.give_coupon is True
    assert decision.policy_rule == "coupon.new_user"
