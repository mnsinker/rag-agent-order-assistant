from domain.nodes.order import ShippingStatus
from domain.nodes.refund import RefundDecision, RefundExecution
from domain.nodes.risk import RiskResult
from domain.nodes.coupon import CouponDecision, CouponEligibility

INTENT_TO_NODES = {
    "risk_check": [RiskResult],

    "check_refund": [RefundDecision],
    "create_refund": [RefundExecution],

    "get_shipping_status": [ShippingStatus],

    "check_coupon": [CouponEligibility],
    "apply_coupon": [CouponDecision],
    "decide_coupon": [CouponDecision],
}