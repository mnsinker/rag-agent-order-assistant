from domain.nodes.base import Node, NodeMeta


class OrderSummary(Node):
    name = "OrderSummary"
    meta = NodeMeta(
        category="view",
        description="a compact order view used by decision workflows.",
    )

class OrderRecord(Node):
    name = "OrderRecord"
    meta = NodeMeta(
        category="view",
        description="a historical order record used in user history.",
    )

class ShippingStatus(Node):
    name = "ShippingStatus"
    meta = NodeMeta(
        category="view",
        description="shipping status of an order.",
    )