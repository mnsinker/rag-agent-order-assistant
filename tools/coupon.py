from models.coupon import CouponEligibility
from models.order import OrderSummary
from models.user import UserProfile


def check_coupon(order: OrderSummary, user: UserProfile) -> CouponEligibility:
    if user.level != 'vip':
        return CouponEligibility(False, 'only vip users can use coupon')

    if order.days > 7:
        return CouponEligibility(False, 'order too old')

    return CouponEligibility(True, "coupon applicable")



def apply_coupon(coupon_elig: CouponEligibility):
    if not coupon_elig.applicable:
        return "coupon not applied"
    return "coupon applied successfully"