from domain.nodes.base import Node, NodeMeta


class RefundDecision(Node):
    name = "RefundDecision"
    meta = NodeMeta(
        category="policy_result",
        description="refund eligibility result produced by refund policy."
    )

class RefundExecution(Node):
    name = "RefundExecution"
    meta = NodeMeta(
        category="execution_result",
        description="result of executing a refund action."
    )