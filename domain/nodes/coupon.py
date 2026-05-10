from domain.nodes.base import Node, NodeMeta

class CouponEligibility(Node):
    name = "CouponEligibility"
    meta = NodeMeta(
        category="policy_result",
        description="whether an existing coupon can be applied."
    )

class CouponDecision(Node):
    name = "CouponDecision"
    meta = NodeMeta(
        category="decision",
        description="whether the system should issue a coupon."
    )