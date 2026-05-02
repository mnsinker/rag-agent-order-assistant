from domain.dtos.coupon_dto import CouponDecisionDTO
from domain.dtos.order_summary_dto import OrderSummaryDTO
from domain.dtos.user_profile_dto import UserProfileDTO


def evaluate_coupon_policy(
        order: OrderSummaryDTO,
        user: UserProfileDTO
) -> CouponDecisionDTO:
    # 新用户
    if user.level == "new":
        return CouponDecisionDTO(
            give_coupon=True,
            coupon_type="discount",
            amount=10,
            reason="new user promotion",
            policy_rule="coupon.new_user"
        )

    # 非VIP, 高客单
    if user.level != "vip" and order.amount >= 1000:
        return CouponDecisionDTO(
            give_coupon=True,
            coupon_type="full_reduction",
            amount=50,
            reason="non-vip high value order",
            policy_rule="coupon.non_vip_high_amount",
        )

    # VIP 不给券 (已经很好)
    if user.level == "vip":
        return CouponDecisionDTO(
            give_coupon=False,
            coupon_type="none",
            amount=0,
            reason="vip no need coupon",
            policy_rule="coupon.skip.vip",
        )
    return CouponDecisionDTO(
        give_coupon=False,
        coupon_type="none",
        amount=0,
        reason="no promotion",
        policy_rule="coupon.default",
    )