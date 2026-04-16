class Relation():
    def __init__(self, source, target, predicate):
        self.source = source
        self.target = target
        self.predicate = predicate


RELATIONS = [
    Relation("Order", "User", "belongs_to"),
    Relation("User", "Order", "has_orders"),
    Relation("Order", "Coupon", "can_apply"),
]