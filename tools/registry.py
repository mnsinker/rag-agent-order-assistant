from models.coupon import CouponEligibility
from models.credit import CreditScore
from models.order import OrderSummary
from models.refund import RefundEligibility, RefundExecutionResult
from models.risk import RiskResult
from models.shipping import ShippingResult
from models.user import UserProfile
from models.user_history import UserHistory
from tools.base import Tool
from tools.credit import get_user_credit
from tools.order import get_order
from tools.refund import check_refund, create_refund
from tools.risk import risk_check
from tools.shipping import get_shipping_status
from tools.user import get_user, get_user_history
from tools.coupon import check_coupon, apply_coupon

tools = {
    "get_order": Tool(
        name="get_order",
        description="get order",
        func=get_order,
        order_id=str,
        output_type=OrderSummary,
    ),
    "get_user": Tool(
        name="get_user",
        description="get user profile",
        func=get_user,
        dependency_args=None,
        user_id=str,
        output_type=UserProfile,
    ),
    "get_user_history": Tool(
        name="get_user_history",
        description="get user history",
        func=get_user_history,
        user_id=str,
        output_type=UserHistory,
    ),
    "get_user_credit": Tool(
        name="get_user_credit",
        description="get user credits",
        func=get_user_credit,
        user_id=str,
        output_type=CreditScore,
    ),
    "risk_check": Tool(
        name="risk_check",
        description="check whether order has risk",
        func=risk_check,
        dependency_args={
            "order": OrderSummary,
            "user": UserProfile,
            "history": UserHistory,
            "credit": CreditScore,
        },
        output_type=RiskResult,
    ),
    "check_coupon": Tool(
        name="check_coupon",
        description="check coupon eligibility",
        func=check_coupon,
        dependency_args={
            'user': UserProfile,
            'order': OrderSummary,
        },
        output_type=CouponEligibility,
    ),
    "apply_coupon": Tool(
        name="apply_coupon",
        description="apply coupon",
        func=apply_coupon,
        dependency_args={'coupon_elig': CouponEligibility},
        output_type=str,
    ),
    "check_refund": Tool(
        name="check_refund",
        description="check whether order is refundable",
        func=check_refund,
        output_type=RefundEligibility,
        dependency_args=None,
        order_id=str,
    ),
    "get_shipping_status": Tool(
        name="get_shipping_status",
        description="check shipping status",
        func=get_shipping_status,
        output_type=ShippingResult,
        dependency_args=None,
        order_id=str
    ),
    'create_refund': Tool(
        name="create_refund",
        description="execute refund",
        func=create_refund,
        output_type=RefundExecutionResult,
        dependency_args={'eligibility': RefundEligibility},
        order_id=str,
    )

}
# eligibility=RefundEligibility
# print(tools['refund'].args)
# {'order_id': <class 'str'>, 'user_id': <class 'str'>}