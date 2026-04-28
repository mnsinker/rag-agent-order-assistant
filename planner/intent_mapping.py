from domain.entities.order import Order
from domain.entities.risk import Risk
from domain.entities.coupon import Coupon

INTENT_TO_ENTITIES = {
    "risk_check": [Risk],

    "check_refund": [Order],
    "create_refund": [Order],

    "get_shipping_status": [Order],

    "check_coupon": [Coupon],
    "apply_coupon": [Coupon],
}