from domain.nodes.base import Node, NodeMeta

class UserProfile(Node):
    name = "UserProfile"
    meta = NodeMeta(
        category="view",
        description="basic user profile used for decision workflows.",
    )

class UserHistory(Node):
    name = "UserHistory"
    meta = NodeMeta(
        category="view",
        description="historical order behavior of a user",
    )