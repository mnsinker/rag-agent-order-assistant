from domain.dtos.coupon_dto import CouponEligibilityDTO
from domain.dtos.order_summary_dto import OrderSummaryDTO
from domain.dtos.user_profile_dto import UserProfileDTO


def check_coupon(order: OrderSummaryDTO, user: UserProfileDTO) -> CouponEligibilityDTO:
    if user.level != 'vip':
        return CouponEligibilityDTO(False, 'only vip users can use coupon')

    if order.days > 7:
        return CouponEligibilityDTO(False, 'order too old')

    return CouponEligibilityDTO(True, "coupon applicable")



def apply_coupon(coupon_elig: CouponEligibilityDTO):
    if not coupon_elig.applicable:
        return "coupon not applied"
    return "coupon applied successfully"