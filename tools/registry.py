from domain.dtos.credit_dto import CreditScoreDTO
from domain.dtos.order_summary_dto import OrderSummaryDTO
from domain.dtos.refund_dto import RefundDecisionDTO
from domain.dtos.user_profile_dto import UserProfileDTO
from tools.base import Tool
from tools.credit_tool import get_user_credit
from tools.order_tool import get_order
from tools.refund_tool import check_refund, create_refund
from tools.risk_tool import risk_check
from tools.shipping_tool import get_shipping_status
from tools.user_tool import get_user, get_user_history
from tools.coupon_tool import check_coupon, decide_coupon

tools = {
    "get_order": Tool(
        name="get_order",
        description="get order",
        func=get_order,
        order_id=str,
    ),
    "get_shipping_status": Tool(
        name="get_shipping_status",
        description="check shipping status",
        func=get_shipping_status,
        order_id=str
    ),
    "get_user": Tool(
        name="get_user",
        description="get user profile",
        func=get_user,
        order=OrderSummaryDTO,
    ),
    "get_user_history": Tool(
        name="get_user_history",
        description="get user history",
        func=get_user_history,
        user=UserProfileDTO,
    ),
    "get_user_credit": Tool(
        name="get_user_credit",
        description="get user credits",
        func=get_user_credit,
        user=UserProfileDTO,
    ),
    "risk_check": Tool(
        name="risk_check",
        description="check whether order has risk",
        func=risk_check,
        order=OrderSummaryDTO,
        user=UserProfileDTO,
        credit=CreditScoreDTO,
    ),
    "check_coupon": Tool(
        name="check_coupon",
        description="check coupon eligibility",
        func=check_coupon,
        order=OrderSummaryDTO,
        user=UserProfileDTO,
    ),
    "decide_coupon": Tool(
        name="decide_coupon",
        description="decide whether to give coupon",
        func=decide_coupon,
        order=OrderSummaryDTO,
        user=UserProfileDTO,
    ),
    "check_refund": Tool(
        name="check_refund",
        description="check whether order is refundable",
        func=check_refund,
        order_id=str,
        order=OrderSummaryDTO,
        user=UserProfileDTO,
    ),
    'create_refund': Tool(
        name="create_refund",
        description="execute refund",
        func=create_refund,
        order_id=str,
        decision=RefundDecisionDTO,
    )
}

