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
    ),
    "get_shipping_status": Tool(
        name="get_shipping_status",
        description="check shipping status",
        func=get_shipping_status,
    ),
    "get_user": Tool(
        name="get_user",
        description="get user profile",
        func=get_user,
    ),
    "get_user_history": Tool(
        name="get_user_history",
        description="get user history",
        func=get_user_history,
    ),
    "get_user_credit": Tool(
        name="get_user_credit",
        description="get user credits",
        func=get_user_credit,
    ),
    "risk_check": Tool(
        name="risk_check",
        description="check whether order has risk",
        func=risk_check,
    ),
    "check_coupon": Tool(
        name="check_coupon",
        description="check coupon eligibility",
        func=check_coupon,
    ),
    "decide_coupon": Tool(
        name="decide_coupon",
        description="decide whether to give coupon",
        func=decide_coupon,
    ),
    "check_refund": Tool(
        name="check_refund",
        description="check whether order is refundable",
        func=check_refund,
        order_id=str,
    ),
    'create_refund': Tool(
        name="create_refund",
        description="execute refund",
        func=create_refund,
    )
}

