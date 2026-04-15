from errors.validation import ValidationError
from models.order import OrderSummary
def get_order_summary(order_id: str) -> OrderSummary | None:
    order = {
        "123": {"user": "u1", "days": 3, "shipped": True, "custom": False, "amount": 1000.00},
        "456": {"user": "u2", "days": 4, "shipped": False, "custom": False, "amount": 800.00},
        "789": {"user": "u1", "days": 8, "shipped": True, "custom": True, "amount": 2000.00},
         }

    data = order.get(order_id)

    if data is None:
        raise ValidationError(f"order {order_id} not found")

    return OrderSummary(order_id,
                        data.get("user"),
                        data.get("days"),
                        data.get("shipped"),
                        data.get("custom"),
                        data.get("amount")
                        )

