from domain.nodes.base import Node, NodeMeta

class CreditScore(Node):
    name = "CreditScore"
    meta = NodeMeta(
        category="metric",
        description="credit score used as a risk signal."
    )