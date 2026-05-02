from domain.dtos.coupon_dto import CouponDecisionDTO, CouponEligibilityDTO
from domain.dtos.order_summary_dto import OrderSummaryDTO
from domain.dtos.user_profile_dto import UserProfileDTO
from policies.coupon_policy import evaluate_coupon_policy



def decide_coupon(order: OrderSummaryDTO, user: UserProfileDTO) -> CouponDecisionDTO:
    return evaluate_coupon_policy(order, user)



def check_coupon(order: OrderSummaryDTO, user: UserProfileDTO) -> CouponEligibilityDTO:
    if user.level != 'vip':
        return CouponEligibilityDTO(False, 'only vip users can use coupon')

    if order.days > 7:
        return CouponEligibilityDTO(False, 'order too old')

    return CouponEligibilityDTO(True, "coupon applicable")



