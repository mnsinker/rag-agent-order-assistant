from domain.nodes.base import Node, NodeMeta

class RiskResult(Node):
    name = "RiskResult"
    meta = NodeMeta(
        category="decision",
        description="risk decision result for an order."
    )