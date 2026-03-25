from models.order_summary import OrderSummary
def get_order_summary(order_id: str) -> OrderSummary | None:
    order = {
        "123": {"days": 3, "shipped": True, "custom": False},
        "456": {"days": 4, "shipped": False, "custom": False},
        "789": {"days": 8, "shipped": True, "custom": True}
         }

    data = order.get(order_id)

    if data is None:
        return None

    return OrderSummary(order_id, data.get("days"), data.get("shipped"), data.get("custom"))

